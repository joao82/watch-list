from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from webapp import db
from webapp.models import User

from .forms import LoginForm, RegisterForm

bp = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


@bp.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movie.index', user_id=current_user.id))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully", "success")
        return redirect(url_for("auth.login"))

    return render_template(
        "register.html", title="Movies Watchlist - Register", form=form
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movie.index', user_id=current_user.id))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Login credentials not correct", category="danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=True)
        return redirect(url_for("movie.index"))

    return render_template("login.html", title="Movies Watchlist - Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash('Your are logged out', 'info')

    return redirect(url_for("auth.login"))
