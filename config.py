import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/recrutement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    """Configuration développement"""
    DEBUG = True
    TESTING = False
    # Utiliser SQLite pour le développement local (pas besoin de MySQL)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///recrutement.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recrutement.db'


class ProductionConfig(Config):
    """Configuration production"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/recrutement.db'

class TestingConfig(Config):
    """Configuration test"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
