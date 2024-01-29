
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment


db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()


def create_app():
    """
    Create and configure the Flask application.

    Returns:
    - Flask: The configured Flask application instance.

    Usage:
        app = create_app()
        app.run()
    """

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)



    # Register blueprints
    from app.admin_routes import admin_bp
    from app.main_routes import main_bp
    from app.user_routes import user_bp
    from app.tag_routes import tag_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(tag_bp)

    return app
 