import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Database configuration
    MONGO_URI = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/worlds_ai_bot')
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'dream')  # Using the same secret as in Node.js
    
    # Frontend URL for CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://worldsaibot.com')
    
    # Email configuration
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    
    # CORS credentials
    CORS_CREDENTIALS = os.getenv('CORS_CREDENTIALS', 'true').lower() == 'true'