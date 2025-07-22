import os

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///quizmaster.sqlite3"
    
    # Flask-Security / Flask-Login
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'thisshouldbekeptsecret'
    SECRET_KEY = "superquizsecret"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    
    # CSRF protection (used later for forms if needed)
    WTF_CSRF_ENABLED = True

    # Optional: folder for exporting reports/CSVs
    EXPORT_FOLDER = os.path.join(os.getcwd(), 'exports')
