import datetime
from webapp import db
from flask_login import current_user, login_required
from flask import Blueprint, redirect, render_template, session, url_for, request, flash, abort
from webapp.movie.forms import MovieForm, EditMovieForm, AddTagsForm
from webapp.models import Movie, User, Tag, Cast, Series
from flask import current_app
from pydantic import BaseModel, validatonError, validator

bp = Blueprint("movie", __name__, template_folder="templates", static_folder="static")


# --------------
# Helper Classes
# --------------


class MovieModel(BaseModel):
    """Class for parsing new movie data from a form."""

    title: str
    director: str
    rating: int

    @validator("rating")
    def movie_rating_check(cls, value):
        if value not in range(1, 6):
            raise ValueError("Movie rating must be a whole number between 1 and 5")
        return value


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@bp.errorhandler(403)
def page_forbidden(e):
    return render_template("403.html"), 500


@bp.route("/")
@login_required
def index():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        user = User.query.filter_by(id=current_user.id).first()
        movies = Movie.query.filter_by(userId=user.id).all()
    except Exception as e:
        abort(status=404, description=e)
    return render_template("movie.html", title="Movies Watchlist", movies_data=movies)


@bp.route("/movie/<int:movieId>", methods=["GET"])
@login_required
def movie(movieId):
    current_app.logger.info("getting the movie from the database...")
    movie = Movie.query.get_or_404(movieId)
    try:
        current_app.logger.debug("Get tags, cast and series with index: {}".format(movieId))
        tags = Tag.query.filter_by(movieId=movie.id)
        cast = Cast.query.filter_by(movieId=movie.id)
        series = Series.query.filter_by(movieId=movie.id)
    except Exception as e:
        current_app.logger.error("MovieId {} is causing an IndexError".format(movieId))
        abort(404)

    return render_template("movie_details.html", movie=movie, tags=tags, cast=cast, series=series)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    user = User.query.filter_by(id=current_user.id).first()
    form = MovieForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            movie = Movie(title=form.title.data, director=form.director.data, year=form.year.data, userId=user.id)
            db.session.add(movie)

            for actor in form.cast.data:
                cast = Cast(actor=actor, movieId=movie.id)
                db.session.add(cast)

            for tag in form.tags.data:
                tag = Tag(tag=tag, movieId=movie.id)
                db.session.add(tag)

            for serial in form.series.data:
                single_serial = Series(series=serial, movieId=movie.id)
                db.session.add(single_serial)

            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                current_app.logger.critical(f"Error while adding the movie: {movie.title.data} - {e}")
                current_app.logger.exception(e)
                flash("There was an error while creating your movie. Try again later.", "danger")
                return redirect(url_for("movie.add_movie"))

            if form.description.data != "":
                movie.description = form.description.data

            if form.video_link.data != "":
                movie.video_link = form.video_link.data

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.critical(f"Error while adding the movie: {movie.title.data} - {e}")
                current_app.logger.exception(e)
                flash("There was an error while creating your movie. Try again later.", "danger")
                return redirect(url_for("movie.add_movie"))

            flash("Your movie has been created!", "success")
            return redirect(url_for("movie.index"))

        else:
            flash("You must be logged in to add a movie!", "danger")
            return redirect(url_for("auth.login"))

    return render_template("new_movie.html", title="Movies Watchlist - Add Movie", form=form)


@bp.route("/edit/<int:movieId>", methods=["GET", "POST"])
@login_required
def edit_movie(movieId):
    movie = Movie.query.get_or_404(movieId)
    form = EditMovieForm(obj=movie)
    if form.validate_on_submit():
        try:
            movie.title = form.title.data
            movie.director = form.director.data
            movie.year = form.year.data
            movie.description = form.description.data
            movie.video_link = form.video_link.data

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Error while editing the movie: {movie.title.data} - {e}")
            current_app.logger.exception(e)
            flash("There was an error while editing your movie. Try again later.", "danger")
            return redirect(url_for("movie.edit_movie", movieId=movie.id))

        flash("The movie has been updated successfully!", "success")
        return redirect(url_for("movie.movie", movieId=movie.id))

    return render_template("movie_form.html", movie=movie, form=form)


@bp.route("/add/tags/<int:movieId>", methods=["GET", "POST"])
@login_required
def add_tags(movieId):
    tags = Tag.query.filter_by(movieId=movieId)
    form = AddTagsForm()
    if form.validate_on_submit():
        try:
            for tag in form.tags.data:
                tag = Tag(tag=tag, movieId=movieId)
                db.session.add(tag)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.critical(f"Error while adding the tag: {tag} - {e}")
            current_app.logger.exception(e)
            flash("There was an error while adding your tag. Try again later.", "danger")
            return redirect(url_for("movie.add_tags", movieId=movieId))

        flash("Your tag has been added!", "success")
        return redirect(url_for("movie.movie", movieId=movieId))

    return render_template("tag_form.html", tags=tags, form=form)


@bp.route("/movie/<int:movieId>/delete/tags/<int:tag_id>", methods=["GET", "POST"])
@login_required
def delete_tag(tag_id, movieId):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    form = AddTagsForm()
    db.session.delete(tag)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.critical(f"Error while deleting the tag: {tag} - {e}")
        current_app.logger.exception(e)
        flash("There was an error while deleting your tag. Try again later.", "danger")
        return redirect(url_for("movie.add_tags", movieId=movieId))

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


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def catch_all(path):
    return render_template("404.html"), 404
