# config.py

class Config:
    SECRET_KEY = 'b81522c4d254ceab980967fcca020da3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use your preferred database URI
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
