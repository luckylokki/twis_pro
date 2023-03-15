from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from app.forms import SignUpForm, SignInForm
from app.models import UserModel, get_current_timestamp
from app import db

users = Blueprint('users', __name__)


@users.route("/signup/", methods=["GET", "POST"])
def signup():
    """User registration route"""
    form = SignUpForm()

    if form.validate_on_submit():
        db.session.add(
            UserModel(
                username=form.username.data.strip(),
                date_create=get_current_timestamp().replace(microsecond=0).isoformat(' '),
                email=form.email.data.strip(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=UserModel.generate_hashed_password(form.password.data)
            )
        )
        db.session.commit()
        flash("Account created. You can login now.", "success")
        return redirect(url_for("users.signin"))
    return render_template("signup.html", form=form)


@users.route("/signin/", methods=["GET", "POST"])
def signin():
    """User login route"""

    form = SignInForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data.strip()).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)

            return redirect(url_for("main.twis_list"))

        else:
            flash("Incorrect username or password. Please check.", "danger")

    return render_template("signin.html", form=form)


@users.route("/logout/")
def logout():
    """User logout route"""

    logout_user()
    redirect_to = url_for("users.signin")

    return redirect(redirect_to)

@users.route("/profile")
@login_required
def profile():
    """User profile view route"""
    return render_template("profile.html")