import os
from dotenv import load_dotenv

load_dotenv()

# Blockchain Configuration
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS", "0x22859a802657c4012d90Ba3259a707aD4559f6A9")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0xbb92e4d51d7947e632be0fb260f4dd9aba3e7b63a50e466259ff800889d49305")

# Application Configuration
MODEL_DIR = "models"
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'csv'}

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
DATABASE_PATH = os.getenv("DATABASE_PATH", "users.db")

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Smart Contract Configuration
CONTRACT_ADDRESS = None
CONTRACT_ABI = None