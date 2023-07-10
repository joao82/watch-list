import re

"""
This file (test_users.py) contains the functional tests for the `users` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `auth` blueprint.
"""


def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/auth/login")
    assert response.status_code == 200
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Don't have an account?" in response.data


def test_valid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/login' page is posted to (POST)
    THEN check the response is valid
    """

    response = test_client.post(
        "/auth/login",
        data={"email": "test@test.com", "password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert re.search(r"Fast Furious 9", str(response.data))
    assert re.search(r"Justin Lin", str(response.data))
    assert re.search(r"2020", str(response.data))
    assert re.search(r"Login successful", str(response.data))


def test_valid_logout(test_client, init_database, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/logout' page is requested (POST)
    THEN check the response is valid
    """

    response = test_client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert re.search(r"Your are logged out", str(response.data))


def test_login_invalid_email(test_client, init_database):
    response = test_client.post(
        "/auth/login", data={"email": "patkennedy79gmail.com", "password": "FlaskIsAwesome"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid email address" in response.data
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data


def test_login_invalid_password(test_client, init_database):
    response = test_client.post(
        "/auth/login", data={"email": "test@test.com", "password": "FlaskIsAwesome"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid email address" not in response.data
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert re.search(r"Login credentials not correct", str(response.data))


def test_login_invalid_credentials(test_client, init_database):
    response = test_client.post(
        "/auth/login", data={"email": "patkennedy79@gmail.com", "password": "F"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Login credentials not correct" in response.data
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data


def test_get_login_page_already_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.get("/auth/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Already logged in! Redirecting to your User Profile page..." in response.data
    assert re.search(r"Fast Furious 9", str(response.data))
    assert re.search(r"Justin Lin", str(response.data))
    assert re.search(r"2020", str(response.data))


def test_post_login_page_already_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/auth/login", data={"email": "test@test.com", "password": "testpassword"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Already logged in! Redirecting to your User Profile page..." in response.data
    assert re.search(r"Fast Furious 9", str(response.data))
    assert re.search(r"Justin Lin", str(response.data))
    assert re.search(r"2020", str(response.data))


def test_registration_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """

    response = test_client.get("/auth/register")
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data


def test_registration_valid_credentials(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """

    response = test_client.post(
        "/auth/register",
        data={"email": "patkennedy79@yahoo.com", "password": "FlaskIsGreat", "confirm": "FlaskIsGreat"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"User registered successfully" not in response.data
    assert b"Don't have an account? Register here." not in response.data
    assert b"Title" not in response.data
    assert b"Director" not in response.data
    assert b"View" not in response.data
    assert b"Fast & Furious 9" not in response.data
    assert b"John Doe" not in response.data
    assert b"2010" not in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_registration_invalid_confirm_passwrd(test_client, init_database):
    response = test_client.post(
        "/auth/register",
        data={"email": "patkennedy79@hotmail.com", "password": "testpassword", "confirm_password": "FlaskIsGreat"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"This password did not match the one in the password field." in response.data
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data


def test_registration_invalid_email(test_client, init_database):
    response = test_client.post(
        "/auth/register",
        data={"email": "patkennedy79hotmail.com", "password": "testpassword", "confirm_password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid email address." in response.data
    assert b"Logout" not in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data


def test_duplicate_registration(test_client, init_database):
    # Register the new account
    response = test_client.post(
        "/auth/register",
        data={"email": "test@test.com", "password": "testpassword", "confirm_password": "testpassword"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email address already exists" in response.data
    assert b"Logout" not in response.data
    assert b"Register" in response.data
    assert b"Log in" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data
    assert b"Already have an account?" in response.data


def test_registration_when_logged_in(test_client, log_in_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST) when the user is logged in
    THEN check an error message is returned to the user
    """

    response = test_client.post(
        "/auth/register",
        data={"email": "test@test.com", "password": "testpassword", "confirm": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Already logged in! Redirecting to your User Profile page..." in response.data


def test_status_page(test_client):
    response = test_client.get("/auth/status")

    assert response.status_code == 200
    # assert b"Web Application: Active" in response.data
    # assert b"Configuration Type: config.TestingConfig" in response.data
    # assert b"Database initialized: True" in response.data
    # assert b"Database `users` table created: True" in response.data
    # assert b"Database `books` table created: True" in response.data


def test_page_not_found(test_client):
    response = test_client.get("/doesnotexist")

    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data
    assert b"Go to home" in response.data
    assert b"Log in" in response.data
    assert b"Register" in response.data
    assert b"Sorry, we couldn't find the page you're looking for" in response.data
    assert b"Email" not in response.data
    assert b"Password" not in response.data
    assert b"Confirm Password" not in response.data
    assert b"Already have an account?" not in response.data
    assert b"Don't have an account? Register here" not in response.data


def test_internal_error(test_client):
    pass


def test_page_forbidden(test_client):
    pass
