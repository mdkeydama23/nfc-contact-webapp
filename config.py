# config.py

class Config:
    SECRET_KEY = 'b81522c4d254ceab980967fcca020da3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use your preferred database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Login settings
    LOGIN_DISABLED = False
    LOGIN_URL = '/admin/login'
    LOGIN_VIEW = 'admin.login'

    # Flask-WTF settings (if using forms)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = '8ab83592b434b2e3e448e7813a4653a0'

    # Set this to True to enable debugging and auto-reload on code changes
    DEBUG = True
