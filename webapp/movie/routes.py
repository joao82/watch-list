import datetime
from webapp import db
from flask_login import current_user, login_required
from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from webapp.movie.forms import MovieForm, EditMovieForm, AddTagsForm
from webapp.models import Movie, User, Tag, Cast, Series


bp = Blueprint("movie", __name__, template_folder="templates", static_folder="static")


@bp.route("/")
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
    movies = Movie.query.filter_by(userId=user.id).all()

    return render_template("movie.html", title="Movies Watchlist", movies_data=movies)


@bp.route("/movie/<int:movieId>", methods=["GET"])
@login_required
def movie(movieId):
    movie = Movie.query.get_or_404(movieId)
    tags = Tag.query.filter_by(movieId=movie.id)
    cast = Cast.query.filter_by(movieId=movie.id)
    series = Series.query.filter_by(movieId=movie.id)

    return render_template("movie_details.html", movie=movie, tags=tags, cast=cast, series=series)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    user = User.query.filter_by(id=current_user.id).first()
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(title=form.title.data, director=form.director.data, year=form.year.data, userId=user.id)
        db.session.add(movie)
        db.session.commit()

        for actor in form.cast.data:
            cast = Cast(actor=actor, movieId=movie.id)
            db.session.add(cast)

        for tag in form.tags.data:
            tag = Tag(tag=tag, movieId=movie.id)
            db.session.add(tag)

        for serial in form.series.data:
            single_serial = Series(series=serial, movieId=movie.id)
            db.session.add(single_serial)

        if form.description.data != "":
            movie.description = form.description.data

        if form.video_link.data != "":
            movie.video_link = form.video_link.data

        db.session.commit()
        return redirect(url_for("movie.index"))

    return render_template("new_movie.html", title="Movies Watchlist - Add Movie", form=form)


@bp.route("/edit/<int:movieId>", methods=["GET", "POST"])
@login_required
def edit_movie(movieId):
    movie = Movie.query.get_or_404(movieId)
    form = EditMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data

        db.session.commit()
        return redirect(url_for("movie.movie", movieId=movie.id))

    return render_template("movie_form.html", movie=movie, form=form)


@bp.route("/add/tags/<int:movieId>", methods=["GET", "POST"])
@login_required
def add_tags(movieId):
    tags = Tag.query.filter_by(movieId=movieId)
    form = AddTagsForm()
    if form.validate_on_submit():
        for tag in form.tags.data:
            tag = Tag(tag=tag, movieId=movieId)
            db.session.add(tag)
        db.session.commit()

        return redirect(url_for("movie.movie", movieId=movieId))

    return render_template("tag_form.html", tags=tags, form=form)


@bp.route("/movie/<int:movieId>/delete/tags/<int:tag_id>", methods=["GET", "POST"])
@login_required
def delete_tag(tag_id, movieId):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    form = AddTagsForm()
    db.session.delete(tag)
    db.session.commit()
    flash("Your tag has been deleted!", "success")
    return redirect(url_for("movie.movie", movieId=movieId))


@bp.route("/movie/<int:movieId>/watch", methods=["GET", "POST"])
@login_required
def watch_today(movieId):
    movie = Movie.query.get_or_404(movieId)
    last_watched = datetime.datetime.today()
    movie.last_seen = last_watched
    db.session.commit()
    return redirect(url_for("movie.movie", movieId=movie.id))


@bp.route("/movie/<int:movieId>/<int:new_rating>", methods=["GET", "POST"])
@login_required
def rate_movie(movieId, new_rating):
    movie = Movie.query.get_or_404(movieId)
    movie.rating = new_rating
    db.session.commit()

    return redirect(url_for("movie.movie", movieId=movie.id))


@bp.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
