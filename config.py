# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI =  os.environ.get('JAWSDB_MARIA_URL') or 'sqlite:///efbi.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Login settings
    LOGIN_DISABLED = False
   
   # User login settings
    USER_LOGIN_URL = '/user/login'  # Update with your user login route
    USER_LOGIN_VIEW = 'user.login'  # Update with the appropriate user login view function

    # Admin login settings
    ADMIN_LOGIN_URL = '/admin/login'  # Update with your admin login route
    ADMIN_LOGIN_VIEW = 'admin.login'  # Update with the appropriate admin login view function

    # Set this to True to enable debugging and auto-reload on code changes
    DEBUG = False
