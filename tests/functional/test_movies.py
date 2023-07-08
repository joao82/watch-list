import os
import re


def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing and the user logged in
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the" in response.data
    assert b"Flask User Management Example!" in response.data
    assert b"Need an account?" in response.data
    assert b"Existing user?" in response.data


def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    response = test_client.post("/")
    assert response.status_code == 405
    assert b"Flask User Management Example!" not in response.data


def test_index_page_not_logged_in(test_client):
    response = test_client.post("/index", follow_redirects=True)
    assert response.status_code == 405


def test_index_page_logged_in(test_client, log_in_default_user):
    response = test_client.post("/index")
    assert response.status_code == 200


def test_get_add_movie_page(test_client, init_database, log_in_default_user):
    response = test_client.get("/add")
    assert response.status_code == 200
    assert b"Title" in response.data
    assert b"Director" in response.data
    assert b"Year" in response.data


def test_get_add_movie_page_not_logged_in(test_client):
    response = test_client.get("/add", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add a Book" not in response.data
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_post_add_movie_page(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add",
        data={"title": "The Guest List", "director": "Lucy Foley", "year": 2010, "movieId": 1},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_post_add_movie_page_not_logged_in(test_client):
    response = test_client.post(
        "/add",
        data={"title": "The Guest List", "director": "Lucy Foley", "year": 2010},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Title" not in response.data
    assert b"Release Date" not in response.data
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_post_rating_movie_page_invalid_movie_rating(test_client, log_in_default_user):
    response = test_client.post(
        "/movie/1/6",
        data={
            "rating": "6",
        },  # Invalid! Needs to be between 1-5
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_get_movie_list_logged_in(test_client, init_database, log_in_default_user):
    headers = [b"Title", b"Release Date", b""]
    data = [b"Fast & Furious 9", b"1010", b"view"]

    response = test_client.get("/index", follow_redirects=True)
    assert response.status_code == 200
    for header in headers:
        assert header in response.data
    for element in data:
        assert element in response.data


def test_post_add_movie_page_invalid_movie_field():
    pass


def test_get_single_movie_page_logged_in():
    pass


def test_get_single_movie_page_not_logged_in():
    pass


def test_get_home_page_not_logged_in():
    pass


def test_get_edit_movie_page_logged_in_own_book(test_client, log_in_default_user):
    response = test_client.get("/movie/1/edit", follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit Book" in response.data
    assert b"Title" in response.data
    assert b"Author" in response.data
    assert b"Rating" in response.data


def test_get_edit_movie_page_logged_in_not_owning_book(test_client, log_in_second_user):
    response = test_client.get("/movie/1/edit", follow_redirects=True)
    assert response.status_code == 403
    assert b"Edit Book" not in response.data


def test_get_edit_movie_page_not_logged_in(test_client):
    response = test_client.get("/movie/1/edit", follow_redirects=True)
    assert response.status_code == 200
    assert b"Edit Book" not in response.data
    assert b"Please log in to access this page." in response.data


def test_get_edit_movie_page_invalid_movie(test_client, log_in_default_user):
    response = test_client.get("/movie/379/edit", follow_redirects=True)
    assert response.status_code == 404
    assert b"Edit Book" not in response.data


def test_post_edit_movie_valid(test_client, log_in_default_user):
    response = test_client.post(
        "/mvie/1/edit",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2019"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert re.search(r"Book \(.*\) was updated!", str(response.data))
    assert b"Malibu Rising 2" in response.data
    assert b"Taylor J. Reid" in response.data
    assert b"2019" in response.data


def test_post_edit_movie_invalid_user(test_client, log_in_second_user):
    response = test_client.post(
        "/movie/1/edit",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2023"},
        follow_redirects=True,
    )
    assert response.status_code == 403
    assert not re.search(r"Movie \(.*\) was updated!", str(response.data))


def test_post_edit_movie_page_not_logged_in(test_client):
    response = test_client.post(
        "/movie/1/edit",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2020"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert not re.search(r"Movie \(.*\) was updated!", str(response.data))
    assert b"Please log in to access this page." in response.data


def test_get_edit_movie_page_invalid_book(test_client, log_in_default_user):
    response = test_client.post(
        "/movie/379/edit",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2023"},
        follow_redirects=True,
    )
    assert response.status_code == 404
    assert not re.search(r"Movie \(.*\) was updated!", str(response.data))
