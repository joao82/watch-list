from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp import db, login
from typing import Optional


class NotFoundError(Exception):
    pass


class NotAuthorizedError(Exception):
    pass


class User(UserMixin, db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hashed = db.Column(db.String(300), nullable=False)
    registered_on = db.Column(db.DateTime(timezone=True), nullable=False)

    # Define the relationship to the `Movie` class
    movie = db.relationship("Movie", backref="user", lazy="dynamic")

    def __init__(self, email: str, password_plaintext: str, method: str = "sha256"):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext, method=method)
        self.registered_on = datetime.now()

    def __repr__(self):
        return f"<User: {self.email}>"

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext: str, method: str = "sha256"):
        return generate_password_hash(password_plaintext, method=method)

    def check_password(self, password_plaintext):
        return check_password_hash(self.password_hashed, password_plaintext)


class Movie(db.Model):
    __table_name__ = "movie"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True))
    rating = db.Column(db.Integer(), nullable=False, default=0)
    description = db.Column(db.String(300), nullable=True)
    video_link = db.Column(db.String(300), nullable=True)

    userId = db.Column(db.Integer(), db.ForeignKey("user.id"))

    tags = db.relationship("Tag", backref="movie", lazy="dynamic")
    casts = db.relationship("Cast", backref="movie", lazy="dynamic")
    series = db.relationship("Series", backref="movie", lazy="dynamic")

    def __init__(
        self,
        title: str,
        director: str,
        year: int,
        userId: int,
        description: Optional[str] = "",
        video_link: Optional[str] = "",
    ):
        """Create a new Video object using the title, director, rating, description, video_link of the video."""
        self.title = title
        self.director = director
        self.year = year
        self.description = description
        self.video_link = video_link
        self.userId = userId

    def update(
        self,
        new_title: str = "",
        new_director: str = "",
        new_year: str = "",
        new_last_seen: str = "",
        new_rating: str = "",
        new_description: str = "",
        new_video_link: str = "",
    ):
        """Update the attributes of the movie."""
        if new_title:
            self.title = new_title
        if new_director:
            self.director = new_director
        if new_year:
            self.year = int(new_year)
        if new_last_seen:
            self.last_seen = new_last_seen
        if new_rating:
            self.rating = int(new_rating)
        if new_description:
            self.description = new_description
        if new_video_link:
            self.video_link = new_video_link

    def __repr__(self):
        return f"<Movie: {self.title}>"


class Tag(db.Model):
    __table_name__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    tag = db.Column(db.String(100), nullable=True)
    movieId = db.Column(db.Integer(), db.ForeignKey("movie.id"))

    def __init__(self, tag: str, movieId: int):
        self.tag = tag
        self.movieId = movieId

    def __repr__(self):
        return f"<id: {self.id}, tag: {self.tag}, movieId: {self.movieId}"


class Cast(db.Model):
    __table_name__ = "cast"

    id = db.Column(db.Integer(), primary_key=True)
    actor = db.Column(db.String(100), nullable=True)
    movieId = db.Column(db.Integer(), db.ForeignKey("movie.id"))

    def __init__(self, actor: str, movieId: int):
        self.actor = actor
        self.movieId = movieId

    def __repr__(self):
        return f"<id: {self.id}, actor: {self.actor}, movieId: {self.movieId}"


class Series(db.Model):
    __table_name__ = "series"

    id = db.Column(db.Integer(), primary_key=True)
    series = db.Column(db.String(100), nullable=True)
    movieId = db.Column(db.Integer(), db.ForeignKey("movie.id"))

    def __init__(self, series: str, movieId: int):
        self.series = series
        self.movieId = movieId

    def __repr__(self):
        return f"<id: {self.id}, series: {self.series}, movieId: {self.movieId}"


@login.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None
