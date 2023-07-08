import os
import logging
from logging.handlers import RotatingFileHandler
from config import DevelopmentConfig
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask.logging import default_handler
from click import echo

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


def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_cli_commands(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database!")
    else:
        app.logger.info("Database already contains the users table.")

    return app


# ----------------
# Helper Functions
# ----------------


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    app.debug = 1


def register_blueprints(app):
    from webapp.movie.routes import bp as movie_bp
    from webapp.auth.routes import bp as auth_bp

    app.register_blueprint(movie_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")


def configure_logging(app):
    if app.config["LOG_WITH_GUNICORN"]:
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler("instance/logs/flask-user-management.log", maxBytes=16384, backupCount=20)
        file_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)
    app.logger.info("Starting the Flask User Management App...")


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")
