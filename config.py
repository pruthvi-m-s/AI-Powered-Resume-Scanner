import os

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///resume_scanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Secret key for session management
    SECRET_KEY = 'your-secret-key-here'  # Change this in production
    
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
