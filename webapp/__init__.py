import os
from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from webapp.movie.routes import bp as movie_bp
    from webapp.auth.routes import bp as auth_bp

    app.register_blueprint(movie_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app