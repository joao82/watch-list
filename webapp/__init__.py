import logging
from logging.handlers import RotatingFileHandler

from config import DevelopmentConfig

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.logging import default_handler

# -------------
# Configuration
# -------------


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please login to access this page"


# ----------------------------
# Application Factory Function
# ----------------------------


def create_app(config_class=DevelopmentConfig):
    # Create an instance of the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    app.config.from_object(config_class)

    # Configure logging
    if app.config["LOG_WITH_GUNICORN"]:
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler("logs/flask-user-management.log", maxBytes=16384, backupCount=20)
        file_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)
    app.logger.info("Starting the Flask User Management App...")

    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    app.debug = 1

    from webapp.movie.routes import bp as movie_bp
    from webapp.auth.routes import bp as auth_bp

    app.register_blueprint(movie_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
