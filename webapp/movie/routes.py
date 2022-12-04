import datetime
from webapp import db
from flask_login import current_user, login_required
from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from webapp.movie.forms import MovieForm, EditMovieForm, AddTagsForm
from webapp.models import Movie, User, Tag, Cast, Series


bp = Blueprint(
    "movie", __name__, template_folder="templates", static_folder="static"
)


@bp.route("/")
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
    movies = Movie.query.filter_by(user_id=user.id).all()

    return render_template(
        "movie.html",
        title="Movies Watchlist",
        movies_data=movies
    )


@bp.route("/movie/<int:movie_id>", methods=['GET'])
@login_required
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    tags = Tag.query.filter_by(movie_id=movie.id)
    cast = Cast.query.filter_by(movie_id=movie.id)
    series = Series.query.filter_by(movie_id=movie.id)

    return render_template("movie_details.html",
                           movie=movie,
                           tags=tags,
                           cast=cast,
                           series=series)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_movie():
    user = User.query.filter_by(id=current_user.id).first()
    form = MovieForm()

    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            director=form.director.data,
            year=form.year.data,
            user_id=user.id
        )
        db.session.add(movie)
        db.session.commit()

        for actor in form.cast.data:
            cast = Cast(actor=actor,
                        movie_id=movie.id)
            db.session.add(cast)

        for tag in form.tags.data:
            tag = Tag(tag=tag,
                      movie_id=movie.id)
            db.session.add(tag)

        for serial in form.series.data:
            single_serial = Series(series=serial,
                                   movie_id=movie.id)
            db.session.add(single_serial)

        db.session.commit()
        return redirect(url_for("movie.index"))

    return render_template(
        "new_movie.html",
        title="Movies Watchlist - Add Movie",
        form=form
    )


@bp.route("/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = EditMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.director = form.director.data
        movie.year = form.year.data
        movie.description = form.description.data
        movie.video_link = form.video_link.data

        db.session.commit()
        return redirect(url_for("movie.movie", movie_id=movie.id))

    return render_template("movie_form.html", movie=movie, form=form)


@bp.route("/add/tags/<int:movie_id>", methods=["GET", "POST"])
@login_required
def add_tags(movie_id):
    tags = Tag.query.filter_by(movie_id=movie_id)
    form = AddTagsForm()
    if form.validate_on_submit():
        for tag in form.tags.data:
            tag = Tag(tag=tag, movie_id=movie_id)
            db.session.add(tag)
        db.session.commit()

        return redirect(url_for("movie.movie", movie_id=movie_id))

    return render_template("tag_form.html",
                           tags=tags,
                           form=form)


@bp.route("/delete/tags/<int:tag_id>", methods=["GET", "POST"])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Your tag has been deleted!', 'success')

    return render_template("tag_form.html",
                           tag=tag)


@bp.route("/movie/<int:movie_id>/watch", methods=["GET", "POST"])
@login_required
def watch_today(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    last_watched = datetime.datetime.today()
    movie.last_seen = last_watched
    db.session.commit()
    return redirect(url_for("movie.movie", movie_id=movie.id))


@bp.route("/movie/<int:movie_id>/<int:new_rating>", methods=["GET", "POST"])
@login_required
def rate_movie(movie_id, new_rating):
    movie = Movie.query.get_or_404(movie_id)
    movie.rating = new_rating
    db.session.commit()

    return redirect(url_for("movie.movie", movie_id=movie.id))


@bp.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    if current_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"

    return redirect(request.args.get("current_page"))
