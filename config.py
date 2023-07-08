import os
from pathlib import Path

# Determine the folder of the top-level directory of this project
BASEDIR = Path.cwd()


class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", default="BAD_SECRET_KEY")
    # Database connection
    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "instance/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # OAuth
    OAUTHLIB_INSECURE_TRANSPORT = True
    # Logging
    LOG_WITH_GUNICORN = os.environ.get("LOG_WITH_GUNICORN", default=False)


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URI", default="sqlite:///" + os.path.join(BASEDIR, "instance/test.db")
    )
    WTF_CSRF_ENABLED = False
