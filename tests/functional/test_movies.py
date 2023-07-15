import re

# --------------
# Home page
# --------------


def test_home_page_not_logged_in(test_client):
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


def test_home_page_logged_in(test_client, log_in_default_user):
    response = test_client.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert b"Fast Furious 9" in response.data
    assert b"Justin Lin" in response.data
    assert b"2020" in response.data


def test_home_page_post(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is posted to (POST)
    THEN check that a '405' (Method Not Allowed) status code is returned
    """
    response = test_client.post("/")

    assert response.status_code == 405
    assert b"Flask User Management Example!" not in response.data


# --------------
# Index page
# --------------


def test_index_page_not_logged_in(test_client):
    response = test_client.get("/index", follow_redirects=True)
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Don't have an account?" in response.data


def test_index_page_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.get("/index")
    assert response.status_code == 200
    assert b"Fast Furious 9" in response.data
    assert b"Justin Lin" in response.data
    assert b"2020" in response.data


def test_index_page_logged_in_no_movies_added(test_client):
    test_client.post(
        "/auth/register",
        data={"email": "test22@test.com", "password": "testpassword", "confirm_password": "testpassword"},
    )
    test_client.post("/auth/login", data={"email": "test22@test.com", "password": "testpassword"})
    response = test_client.get("/index", follow_redirects=True)

    assert response.status_code == 200
    assert b"You haven't added any movies" in response.data
    assert b"Fast Furious 9" not in response.data
    assert b"Justin Lin" not in response.data
    assert b"2020" not in response.data


# --------------
# Add movie form page
# --------------


def test_get_add_movie_page(test_client, init_database, log_in_default_user):
    response = test_client.get("/add")
    assert response.status_code == 200
    assert b"Title" in response.data
    assert b"Director" in response.data
    assert b"Year" in response.data
    assert b"Cast" in response.data
    assert b"Series" in response.data
    assert b"Tags" in response.data
    assert b"Description" in response.data
    assert b"Video link" in response.data
    assert b"Add Movie" in response.data


def test_get_add_movie_not_logged_in(test_client):
    response = test_client.get("/add", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add a Book" not in response.data
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_post_add_movie(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add",
        data={"title": "The Guest List", "director": "Lucy Foley", "year": 2010, "movieId": 1},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_post_add_movie_not_logged_in(test_client):
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


def test_post_add_movie_invalid_year_movie_field(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add",
        data={"title": "The Guest List", "director": "Lucy Foley", "year": "lucy", "movieId": 2},
    )
    assert response.status_code == 200
    assert b"Error with movie data submitted!" in response.data
    assert b"Fast Furious 9" not in response.data


def test_post_add_movie_missing_required_fields(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add",
        data={"title": "The Guest List", "director": "", "year": "", "movieId": 2},
    )
    assert response.status_code == 200
    assert b"Error with movie data submitted!" in response.data
    assert b"Fast Furious 9" not in response.data


# --------------
# Single movie page
# --------------


def test_get_single_movie_page_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.get("/movie/1")

    assert response.status_code == 200
    assert b"Fast Furious 9" in response.data
    assert b"Hobbs has Dominic and Brian reassemble their crew" in response.data
    assert b"Not watched yet" in response.data


def test_get_single_movie_page_not_logged_in(
    test_client,
    init_database,
):
    response = test_client.get("/movie/1")

    assert response.status_code == 302
    assert b"Fast Furious 9" not in response.data
    assert b"Hobbs has Dominic and Brian reassemble their crew" not in response.data
    assert b"Not watched yet" not in response.data


# --------------
# Rating a movie
# --------------


def test_post_rating_movie_invalid_movie_rating(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/movie/1/6",
        data={"rating": 6},
    )
    assert response.status_code == 500
    assert b"OOOOPS! Something went wrong on the server." in response.data
    assert b"The administrator has been notified. Sorry for the inconvenience!" in response.data
    assert b"Fast & Furious 9" not in response.data


def test_post_rating_movie_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/movie/1/5",
        data={"rating": 5},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"OOOOPS! Something went wrong on the server." not in response.data
    assert b"The administrator has been notified. Sorry for the inconvenience!" not in response.data
    assert b"Fast Furious 9" in response.data
    assert b"Hobbs has Dominic and Brian reassemble their crew" in response.data
    assert b"Not watched yet" in response.data


def test_post_rating_movie_not_logged_in(test_client, init_database):
    response = test_client.post(
        "/movie/1/5",
        data={"rating": 5},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data


# --------------
# Watch today movie
# --------------


def test_post_watched_date_movie_invalid_date(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/movie/1/watch",
        data={"last_seen": "2023-07-08 48:19:29.808763"},
    )
    assert response.status_code == 302


def test_post_watched_date_movie_logged_in(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/movie/1/watch",
        data={"last_seen": "2023-07-08 18:19:29.808763"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_post_watched_date_movie_not_logged_in(test_client, init_database):
    response = test_client.post(
        "/movie/1/watch",
        data={"last_seen": "2023-07-08 18:19:29.808763"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_post_watched_date_movie_not_found(test_client, init_database):
    response = test_client.post(
        "/movie/12/watch",
        data={"last_seen": "2023-07-08 18:19:29.808763"},
        follow_redirects=True,
    )
    assert response.status_code == 200


# --------------
# Edit movie form page
# --------------


def test_get_edit_movie_page_logged_in_own_movie(test_client, init_database, log_in_default_user):
    response = test_client.get("/edit/1")
    assert response.status_code == 200
    assert b"Title" in response.data
    assert b"Director" in response.data
    assert b"Year" in response.data
    assert b"Description" in response.data
    assert b"Video link" in response.data
    assert b"Submit" in response.data
    assert re.search(r"Fast Furious 9", str(response.data))
    assert re.search(r"Justin Lin", str(response.data))
    assert re.search(r"2020", str(response.data))
    assert re.search(r"Hobbs has Dominic and Brian", str(response.data))
    assert re.search(r"https://www.youtube.com/embed/dKi5XoeTN0k", str(response.data))


def test_get_edit_movie_page_logged_in_not_owning_movie(test_client, init_database, log_in_second_user):
    response = test_client.get("/edit/1")
    assert response.status_code == 500
    assert b"OOOOPS! Something went wrong on the server." in response.data
    assert b"The administrator has been notified. Sorry for the inconvenience!" in response.data
    assert b"Back" in response.data
    assert b"Title" not in response.data
    assert b"Director" not in response.data
    assert b"Year" not in response.data


def test_get_edit_movie_page_not_logged_in(test_client):
    response = test_client.get("/edit/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Please login to access this page" in response.data


def test_get_edit_movie_page_invalid_movie(test_client, init_database, log_in_default_user):
    response = test_client.get("/edit/33", follow_redirects=True)
    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data
    assert b"Sorry, we couldn't find the page" in response.data
    assert b"Go to home" in response.data


def test_post_edit_movie_valid(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "edit/1",
        data={
            "title": "Malibu Rising 2",
            "director": "Taylor J. Reid",
            "year": "2019",
            "description": "Dominic Toretto",
            "video_link": "https://www.youtube.com/embed/mw2AqdB5EVA",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert re.search(r"The movie has been updated successfully!", str(response.data))
    assert b"Malibu Rising 2" in response.data
    assert b"Dominic Toretto" in response.data


def test_post_edit_movie_invalid_user(test_client, init_database, log_in_second_user):
    response = test_client.post(
        "/edit/1",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2023"},
        follow_redirects=True,
    )
    assert response.status_code == 500
    assert not re.search(r"The movie has been updated successfully!", str(response.data))
    assert b"OOOOPS! Something went wrong on the server." in response.data
    assert b"The administrator has been notified. Sorry for the inconvenience!" in response.data
    assert b"Back" in response.data


def test_post_edit_movie_page_not_logged_in(test_client, init_database):
    response = test_client.post(
        "/edit/1",
        data={"title": "Malibu Rising 2", "director": "Taylor J. Reid", "year": "2020"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert not re.search(r"The movie has been updated successfully!", str(response.data))
    assert b"Please login to access this page" in response.data


def test_post_edit_movie_page_invalid_movie(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/edit/333",
        data={"title": "Malibu Rising 2", "author": "Taylor J. Reid", "year": "2023"},
        follow_redirects=True,
    )
    assert response.status_code == 404
    assert not re.search(r"The movie has been updated successfully!", str(response.data))


# --------------
# Add tags form page
# --------------


def test_get_add_tags_page_logged_in_own_movie(test_client, init_database, log_in_default_user):
    response = test_client.get("/add/tags/1")
    assert response.status_code == 200


def test_get_add_tags_page_logged_in_not_own_movie(test_client, init_database, log_in_second_user):
    response = test_client.get("/add/tags/1")
    assert response.status_code == 200


def test_get_add_tags_page_not_logged_in(test_client, init_database):
    response = test_client.get("/add/tags/1")
    assert response.status_code == 302


def test_post_add_tags_invalid_movie(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add/tags/12",
        data={"title": "Malibu Rising 2", "author": "Taylor J. Reid", "year": "2023"},
        follow_redirects=True,
    )

    assert response.status_code == 404


def test_post_add_tags(test_client, init_database, log_in_default_user):
    response = test_client.post(
        "/add/tags/1",
        data={"tag": "tag1 tag2 tag3"},
        follow_redirects=True,
    )

    assert response.status_code == 200
