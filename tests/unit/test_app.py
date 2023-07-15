import pytest
from pydantic import ValidationError
from webapp.movie.routes import MovieModel


def test_validate_movie_data_nominal():
    movie_data = {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "year": 1994,
    }
    movie = MovieModel(**movie_data)
    assert movie.title == "The Shawshank Redemption"
    assert movie.director == "Frank Darabont"
    assert movie.year == 1994


# def test_validate_movie_data_invalid_rating(self):
#     movie_data = {
#         "title": "The Shawshank Redemption",
#         "director": "Frank Darabont",
#         "year": 1994,
#         "rating": 6,
#     }
#     with pytest.raises(ValidationError) as e:
#         movie = MovieModel(**movie_data)
#     assert "Movie rating must be a whole number between 1 and 5" in str(e.value)


def test_validate_movie_data_invalid_title():
    with pytest.raises(ValidationError):
        MovieModel(title=[1, 2, 3], director="Taylor Jenkins Reid", year="1994")  # Invalid


def test_validate_movie_data_missing_inputs():
    with pytest.raises(ValidationError):
        MovieModel()  # Missing input data!


def test_validate_book_data_missing_author():
    with pytest.raises(ValidationError):
        MovieModel(
            title="Malibu Rising",
            # Missing author!
            year="2021",
        )
