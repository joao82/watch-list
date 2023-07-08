import os
from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import current_user, login_user, logout_user
from webapp import db
from webapp.models import User
from .forms import LoginForm, RegisterForm
import sqlalchemy as sa

bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


@bp.errorhandler(403)
def page_forbidden(e):
    return render_template("403.html"), 500


@bp.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("movie.index", user_id=current_user.id))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email address already exists", "danger")
            return redirect(url_for("auth.register"))
        else:
            user = User(email=form.email.data, password_plaintext=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html", title="Movies Watchlist - Register", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("movie.index", user_id=current_user.id))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(password_plaintext=form.password.data):
            flash("Login credentials not correct", category="danger")
            return redirect(url_for("auth.login"))
        else:
            login_user(user, remember=True)
            flash("Login successful", "success")
        return redirect(url_for("movie.index"))

    return render_template("login.html", title="Movies Watchlist - Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Your are logged out", "info")

    return redirect(url_for("auth.login"))


@bp.route("/status")
def status():
    engine = sa.create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    users_table_created = inspector.has_table("user")
    movies_table_created = inspector.has_table("movie")
    database_created = users_table_created and movies_table_created

    return render_template(
        "status.html",
        config_type=os.getenv("CONFIG_TYPE"),
        database_status=database_created,
        database_users_table_status=users_table_created,
        database_books_table_status=movies_table_created,
    )
