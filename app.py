from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import pandas as pd
import hashlib
from werkzeug.utils import secure_filename
from functools import wraps
from blockchain.contract_manager import ContractManager
from blockchain.ipfs_simulator import IPFSSimulator
from utils.model_loader import ModelLoader
import auth
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = config.SECRET_KEY

auth.init_db()

contract_manager = ContractManager()
ipfs_simulator = IPFSSimulator()
model_loader = ModelLoader()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = auth.verify_user(email, password)
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if auth.create_user(name, email, password):
            return jsonify({'success': True, 'message': 'Account created successfully'})
        else:
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/diabetes')
@login_required
def diabetes():
    return render_template('diabetes.html', user_name=session.get('user_name'))

@app.route('/heart')
@login_required
def heart():
    return render_template('heart.html', user_name=session.get('user_name'))

@app.route('/predict/diabetes', methods=['POST'])
@login_required
def predict_diabetes():
    try:
        image_file = request.files.get('image_file')
        patient_id = request.form.get('patient_id', 'PATIENT_001')
        
        pregnancies = float(request.form.get('pregnancies'))
        glucose = float(request.form.get('glucose'))
        blood_pressure = float(request.form.get('blood_pressure'))
        skin_thickness = float(request.form.get('skin_thickness'))
        insulin = float(request.form.get('insulin'))
        bmi = float(request.form.get('bmi'))
        diabetes_pedigree = float(request.form.get('diabetes_pedigree'))
        age = float(request.form.get('age'))
        
        tabular_data = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]
        
        if not image_file:
            return jsonify({'error': 'Image file is required'}), 400
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
        image_file.save(image_path)
        
        tabular_result = model_loader.predict_diabetes_tabular(tabular_data)
        image_result = model_loader.predict_diabetes_image(image_path)
        
        final_prediction = 'Positive' if 'Positive' in tabular_result['prediction'] or 'Retinopathy' in image_result['prediction'] else 'Negative'
        final_confidence = (tabular_result['confidence'] + image_result['confidence']) / 2
        final_risk = 'High' if final_confidence >= 80 else 'Medium' if final_confidence >= 50 else 'Low'
        
        csv_data = ','.join(map(str, tabular_data))
        csv_hash = hashlib.sha256(csv_data.encode()).hexdigest()
        
        image_hash = ipfs_simulator.add_file(image_path)
        
        tx_hash = contract_manager.add_record(
            patient_id,
            'Diabetes',
            final_prediction,
            csv_hash,
            image_hash
        )
        
        result = {
            'disease': 'Diabetes',
            'prediction': final_prediction,
            'confidence': round(final_confidence, 2),
            'risk_level': final_risk,
            'tabular_result': tabular_result,
            'image_result': image_result,
            'blockchain_tx': tx_hash,
            'data_hash': csv_hash,
            'image_hash': image_hash
        }
        
        os.remove(image_path)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/heart', methods=['POST'])
@login_required
def predict_heart():
    try:
        image_file = request.files.get('image_file')
        patient_id = request.form.get('patient_id', 'PATIENT_001')
        
        age = float(request.form.get('age'))
        sex = float(request.form.get('sex'))
        cp = float(request.form.get('cp'))
        trestbps = float(request.form.get('trestbps'))
        chol = float(request.form.get('chol'))
        fbs = float(request.form.get('fbs'))
        restecg = float(request.form.get('restecg'))
        thalach = float(request.form.get('thalach'))
        exang = float(request.form.get('exang'))
        oldpeak = float(request.form.get('oldpeak'))
        slope = float(request.form.get('slope'))
        ca = float(request.form.get('ca'))
        thal = float(request.form.get('thal'))
        
        tabular_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        
        if not image_file:
            return jsonify({'error': 'Image file is required'}), 400
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
        image_file.save(image_path)
        
        tabular_result = model_loader.predict_heart_tabular(tabular_data)
        image_result = model_loader.predict_heart_image(image_path)
        
        final_prediction = 'Positive' if 'Disease' in tabular_result['prediction'] or 'Disease' in image_result['prediction'] else 'Negative'
        final_confidence = (tabular_result['confidence'] + image_result['confidence']) / 2
        final_risk = 'High' if final_confidence >= 80 else 'Medium' if final_confidence >= 50 else 'Low'
        
        csv_data = ','.join(map(str, tabular_data))
        csv_hash = hashlib.sha256(csv_data.encode()).hexdigest()
        
        image_hash = ipfs_simulator.add_file(image_path)
        
        tx_hash = contract_manager.add_record(
            patient_id,
            'Heart Disease',
            final_prediction,
            csv_hash,
            image_hash
        )
        
        result = {
            'disease': 'Heart Disease',
            'prediction': final_prediction,
            'confidence': round(final_confidence, 2),
            'risk_level': final_risk,
            'tabular_result': tabular_result,
            'image_result': image_result,
            'blockchain_tx': tx_hash,
            'data_hash': csv_hash,
            'image_hash': image_hash
        }
        
        os.remove(image_path)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        if config.CONTRACT_ADDRESS is None:
            print("Deploying smart contract...")
            contract_manager.compile_and_deploy()
            print(f"Contract deployed at: {config.CONTRACT_ADDRESS}")
        else:
            contract_manager.load_contract(config.CONTRACT_ADDRESS, config.CONTRACT_ABI)
            print("Contract loaded from config")
    except Exception as e:
        print(f"Error with contract: {e}")
        print("Attempting to deploy new contract...")
        contract_manager.compile_and_deploy()

    # Get port from environment variable for Render deployment
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)