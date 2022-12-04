from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from webapp import db, login


class User(UserMixin, db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    movie = db.relationship('Movie', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Movie(db.Model):
    __table_name__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True))
    rating = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(300), nullable=True)
    video_link = db.Column(db.String(300), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tags = db.relationship('Tag', backref='author', lazy='dynamic')
    casts = db.relationship('Cast', backref='author', lazy='dynamic')
    series = db.relationship('Series', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<id: {self.id}, title: {self.title}, director: {self.director} '


class Tag(db.Model):
    __table_name__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __repr__(self):
        return f'<id: {self.id}, tag: {self.tag}, movie id: {self.movie_id}'


class Cast(db.Model):
    __table_name__ = 'cast'

    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(100), nullable=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __repr__(self):
        return f'<id: {self.id}, actor: {self.actor}, movie id: {self.movie_id}'


class Series(db.Model):
    __table_name__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(100), nullable=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __repr__(self):
        return f'<id: {self.id}, series: {self.series}, movie id: {self.movie_id}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
