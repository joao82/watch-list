import os
import pytest
from webapp import create_app, db
from webapp.models import User, Movie, Tag, Cast, Series

# --------
# Fixtures
# --------


@pytest.fixture(scope="module")
def new_user():
    user = User("joao82@gmail.com", "FlaskIsAwesome")
    return user


@pytest.fixture(scope="module")
def new_movie():
    movie = Movie("Fast & Furious 9", "Justin Lin", 2020, 1)
    return movie


@pytest.fixture(scope="module")
def new_tag():
    tag = Tag("actions", 1)
    return tag


@pytest.fixture(scope="module")
def new_cast():
    cast = Cast("Vin Diesel", 1)
    return cast


@pytest.fixture(scope="module")
def new_series():
    series = Series("Fast & Furious 10", 1)
    return series


@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()
    default_user = User(email="patkennedy79@gmail.com", password_plaintext="FlaskIsAwesome")
    second_user = User(email="patrick@yahoo.com", password_plaintext="FlaskIsTheBest987")
    db.session.add(default_user)
    db.session.add(second_user)
    db.session.commit()

    movie1 = Movie(title="Fast & Furious 9", director="John Doe", year=2010, userId=1)
    db.session.add(movie1)
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="function")
def log_in_default_user(test_client):
    test_client.post("/login", data={"email": "patkennedy79@gmail.com", "password": "FlaskIsAwesome"})
    # this is where the testing happens!
    yield
    # Log out the user
    test_client.get("/logout")


@pytest.fixture(scope="function")
def log_in_second_user(test_client):
    test_client.post("login", data={"email": "codingdevz@gmail.com", "password": "FlaskIsTheBest"})
    # this is where the testing happens!
    yield
    # Log out the user
    test_client.get("/logout")


@pytest.fixture(scope="module")
def cli_test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()
    runner = flask_app.test_cli_runner()
    # this is where the testing happens!
    yield runner
