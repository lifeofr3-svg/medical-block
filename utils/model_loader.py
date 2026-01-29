import torch
import pickle
import numpy as np
from torchvision import models
import torch.nn as nn
from PIL import Image
from torchvision import transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ModelLoader:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.models = {}
        self.scalers = {}
        print("ModelLoader initialized with lazy loading (models load on first use)")

    def _load_diabetes_tabular_model(self):
        """Lazy load diabetes XGBoost model and scaler"""
        if 'diabetes_xgb' not in self.models:
            print("Loading diabetes tabular model...")
            with open(f'{self.model_dir}/diabetes_xgboost_model.pkl', 'rb') as f:
                self.models['diabetes_xgb'] = pickle.load(f)
            with open(f'{self.model_dir}/diabetes_scaler.pkl', 'rb') as f:
                self.scalers['diabetes'] = pickle.load(f)
            print("✓ Diabetes tabular model loaded")

    def _load_diabetes_image_model(self):
        """Lazy load diabetes retinal image model"""
        if 'diabetes_retinal' not in self.models:
            print("Loading diabetes image model...")
            model_retinal = models.efficientnet_b0(weights=None)
            num_features = model_retinal.classifier[1].in_features
            model_retinal.classifier = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(num_features, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 2)
            )
            model_retinal.load_state_dict(torch.load(f'{self.model_dir}/diabetes_retinal_model.pth', map_location=device))
            model_retinal.to(device)
            model_retinal.eval()
            self.models['diabetes_retinal'] = model_retinal
            print("✓ Diabetes image model loaded")

    def _load_heart_tabular_model(self):
        """Lazy load heart XGBoost model and scaler"""
        if 'heart_xgb' not in self.models:
            print("Loading heart tabular model...")
            with open(f'{self.model_dir}/heart_xgboost_model.pkl', 'rb') as f:
                self.models['heart_xgb'] = pickle.load(f)
            with open(f'{self.model_dir}/heart_scaler.pkl', 'rb') as f:
                self.scalers['heart'] = pickle.load(f)
            print("✓ Heart tabular model loaded")

    def _load_heart_image_model(self):
        """Lazy load heart ECG image model"""
        if 'heart_ecg' not in self.models:
            print("Loading heart image model...")
            model_ecg = models.resnet50(weights=None)
            num_features_ecg = model_ecg.fc.in_features
            model_ecg.fc = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(num_features_ecg, 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 2)
            )
            model_ecg.load_state_dict(torch.load(f'{self.model_dir}/heart_ecg_model.pth', map_location=device))
            model_ecg.to(device)
            model_ecg.eval()
            self.models['heart_ecg'] = model_ecg
            print("✓ Heart image model loaded")
    
    def predict_diabetes_tabular(self, data):
        self._load_diabetes_tabular_model()
        data_scaled = self.scalers['diabetes'].transform([data])
        prediction = self.models['diabetes_xgb'].predict(data_scaled)[0]
        proba = self.models['diabetes_xgb'].predict_proba(data_scaled)[0]

        return {
            'prediction': 'Positive' if prediction == 1 else 'Negative',
            'confidence': float(max(proba) * 100),
            'risk_level': self.get_risk_level(max(proba))
        }
    
    def predict_diabetes_image(self, image_path):
        self._load_diabetes_image_model()
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = self.models['diabetes_retinal'](image_tensor)
            probs = torch.softmax(output, dim=1)
            confidence, predicted = torch.max(probs, 1)

        prediction = predicted.item()
        confidence_score = confidence.item() * 100

        return {
            'prediction': 'Has Diabetic Retinopathy' if prediction == 1 else 'No Diabetic Retinopathy',
            'confidence': float(confidence_score),
            'risk_level': self.get_risk_level(confidence.item())
        }
    
    def predict_heart_tabular(self, data):
        self._load_heart_tabular_model()
        data_scaled = self.scalers['heart'].transform([data])
        prediction = self.models['heart_xgb'].predict(data_scaled)[0]
        proba = self.models['heart_xgb'].predict_proba(data_scaled)[0]

        return {
            'prediction': 'Heart Disease Detected' if prediction == 1 else 'No Heart Disease',
            'confidence': float(max(proba) * 100),
            'risk_level': self.get_risk_level(max(proba))
        }
    
    def predict_heart_image(self, image_path):
        self._load_heart_image_model()
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = self.models['heart_ecg'](image_tensor)
            probs = torch.softmax(output, dim=1)
            confidence, predicted = torch.max(probs, 1)

        prediction = predicted.item()
        confidence_score = confidence.item() * 100

        return {
            'prediction': 'Heart Disease Detected' if prediction == 1 else 'Normal ECG',
            'confidence': float(confidence_score),
            'risk_level': self.get_risk_level(confidence.item())
        }
    
    def get_risk_level(self, confidence):
        if confidence >= 0.8:
            return 'High'
        elif confidence >= 0.5:
            return 'Medium'
        else:
            return 'Low'