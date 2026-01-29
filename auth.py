import sqlite3
import bcrypt
from datetime import datetime
import config

def init_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(name, email, password):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(email, password):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email, password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return {'id': user[0], 'name': user[1], 'email': user[2]}
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {'id': user[0], 'name': user[1], 'email': user[2]}
    return None