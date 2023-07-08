import os
import pytest
from webapp import create_app, db
from webapp.models import User, Movie, Tag, Cast, Series

# --------
# Fixtures
# --------


@pytest.fixture(scope="module")
def new_user():
    user = User(email="joao82@gmail.com", password_plaintext="FlaskIsAwesome")
    return user


@pytest.fixture(scope="module")
def new_movie():
    movie = Movie(
        title="Fast & Furious 9",
        director="Justin Lin",
        year=2020,
        description="Hobbs has Dominic and Brian reassemble their crew to take down a team of mercenaries: Dominic unexpectedly gets sidetracked with facing his presumed deceased girlfriend, Letty.",
        video_link="https://www.youtube.com/embed/dKi5XoeTN0k",
        userId=1,
    )
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

    default_user = User(email="test@test.com", password_plaintext="testpassword")
    db.session.add(default_user)
    db.session.commit()

    second_user = User(email="test2@test.com", password_plaintext="testpassword")
    db.session.add(second_user)

    default_movie = Movie(
        title="Fast Furious 9",
        director="Justin Lin",
        year=2020,
        description="Hobbs has Dominic and Brian reassemble their crew to take down a team of mercenaries: Dominic unexpectedly gets sidetracked with facing his presumed deceased girlfriend, Letty.",
        video_link="https://www.youtube.com/embed/dKi5XoeTN0k",
        userId=1,
    )

    db.session.add(default_movie)
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope="function")
def log_in_default_user(test_client, init_database):
    test_client.post("/auth/login", data={"email": "test@test.com", "password": "testpassword"})
    # this is where the testing happens!
    yield
    # Log out the user
    test_client.get("/auth/logout")


@pytest.fixture(scope="function")
def log_in_second_user(test_client, init_database):
    test_client.post("auth/login", data={"email": "test2@test.com", "password": "testpassword"})
    # this is where the testing happens!
    yield
    # Log out the user
    test_client.get("/auth/logout")


@pytest.fixture(scope="module")
def cli_test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()
    runner = flask_app.test_cli_runner()
    # this is where the testing happens!
    yield runner
