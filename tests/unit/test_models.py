import re


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == "joao82@gmail.com"
    assert new_user.password_hashed != "FlaskIsAwesome"
    assert new_user.__repr__() == "<User: joao82@gmail.com>"


def test_new_movie(new_movie):
    assert new_movie.title == "Fast & Furious 9"
    assert new_movie.director == "Justin Lin"

    assert new_movie.userId == 1
    assert repr(new_movie) == "<Movie: Fast & Furious 9>"


def test_new_tag(new_tag):
    assert new_tag.tag == "actions"
    assert new_tag.movieId == 1


def test_new_cast(new_cast):
    assert new_cast.actor == "Vin Diesel"
    assert new_cast.movieId == 1


def test_new_series(new_series):
    assert new_series.series == "Fast & Furious 10"
    assert new_series.movieId == 1


def test_generate_password_hash(new_user):
    new_user.set_password("FlaskIsAwesome")
    assert new_user.password_hashed != "FlaskIsAwesome"
    assert new_user.check_password("FlaskIsAwesome") is True
    assert new_user.check_password("FlaskIsNotAwesome") is False


def test_is_password_correct(new_user):
    password = "FlaskIsAwesome"
    assert new_user.is_password_correct(password) == True
    assert new_user.check_password("FlaskIsAwesome") is True


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == "17"


def test_update_movie(new_movie):
    """
    GIVEN a Movie model
    WHEN a new Movie is updated
    THEN check the title, director, year, rating, description and video_link fields are updated correctly
    """
    movie = new_movie

    movie.update(new_title="Fast & Furious 3")
    assert movie.title == "Fast & Furious 3"
    assert movie.director == "Justin Lin"
    assert movie.year == 2020

    movie.update(new_director="Taylor J. Reid")
    assert movie.title == "Fast & Furious 3"
    assert movie.director == "Taylor J. Reid"
    assert movie.year == 2020

    movie.update(new_year=2019)
    assert movie.title == "Fast & Furious 3"
    assert movie.director == "Taylor J. Reid"
    assert movie.year == 2019

    movie.update(new_rating="4")
    assert movie.title == "Fast & Furious 3"
    assert movie.director == "Taylor J. Reid"
    assert movie.year == 2019
    assert movie.rating == 4

    movie.update(
        new_title="movie Lovers",
        new_director="Emily Henry",
        new_year="2010",
        new_rating="2",
        new_description="description test",
        new_video_link="https://www.youtube.com/watch?v=ZQ-YX-5bAs0",
    )
    assert movie.title == "movie Lovers"
    assert movie.director == "Emily Henry"
    assert movie.year == 2010
    assert movie.rating == 2
    assert movie.description == "description test"
    assert movie.video_link == "https://www.youtube.com/watch?v=ZQ-YX-5bAs0"


def test_movie_repr(new_movie):
    retval = repr(new_movie)
    match = "<Movie: Fast & Furious 9>"
    assert match == retval


def test_user_repr(new_user):
    retval = repr(new_user)
    match = "<User: joao82@gmail.com>"
    assert match == retval


def test_tag_repr(new_tag):
    retval = repr(new_tag)
    match = "<id: None, tag: actions, movieId: 1"
    assert match == retval


def test_cast_repr(new_cast):
    retval = repr(new_cast)
    match = "<id: None, actor: Vin Diesel, movieId: 1"
    assert match == retval


def test_series_repr(new_series):
    retval = repr(new_series)
    match = "<id: None, series: Fast & Furious 10, movieId: 1"
    assert match == retval


# def test_load_user(new_user):
#     retval = load_user(1)
#     match = new_user.id
#     assert match == retval


def test_update_last_seen_movie(new_movie):
    pass
    # movie = new_movie

    # movie.update(new_title="Fast NOT Furious")
    # assert movie.title == "Fast NOT Furious"
    # assert movie.director == "Justin Lin"
    # assert movie.year == 2020
    # assert movie.last_seen is not None
