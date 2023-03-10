import datetime
import os
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import login_user, LoginManager, current_user, UserMixin, logout_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + os.environ.get('DB_USER') + ":" \
                                        + os.environ.get('DB_PASSWORD') + "@" + os.environ.get('DB_HOST')
app.config["SECRET_KEY"] = "MYSECRETKEY"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


def get_current_timestamp() -> datetime.datetime:
    """GetDate time implementation"""
    return datetime.datetime.now()


class UserModel(db.Model, UserMixin):
    """User model implementation"""

    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), default="")
    last_name = db.Column(db.String(64), default="")
    twises = db.relationship("TwisModel", backref="userid", cascade="all,delete,delete-orphan", single_parent=True,
                             order_by="desc(TwisModel.date)")

    @property
    def pk(self):
        return self.id

    def check_password(self, password: str) -> bool:
        """Check passed raw password with user assigned"""

        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def generate_hashed_password(raw_password: str) -> str:
        """Return hashed password"""

        return bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def __repr__(self) -> str:
        """Return a string representation of an instance"""

        return f"<UserModel(username='{self.username}', email='{self.email}')>"

    def __str__(self) -> str:
        """Return a string version of an instance"""

        first_name = self.first_name or ""
        last_name = self.last_name or ""
        fullname = " ".join([first_name, last_name]).rstrip()

        # return fullname or self.username
        return self.username


class TwisModel(db.Model):
    """Twis model implementation"""

    __tablename__ = "twises"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=get_current_timestamp().replace(microsecond=0).isoformat(' '))
    date_update = db.Column(db.DateTime, nullable=True)
    user_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)

    @property
    def pk(self):
        return self.id

    @property
    def twis_text(self):
        return self.value

    def __repr__(self) -> str:
        """Return a string representation of instance"""

        return f"<TwissModel(value='{self.value}')>"

    def __str__(self) -> str:
        """Return a string version of an instance"""
        return (f"twis_text={self.value}")


class SignUpForm(FlaskForm):
    """New user form"""

    username = StringField("Username", [DataRequired(), Length(max=128)])
    password = PasswordField("Password", [DataRequired(), Length(max=128)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    email = EmailField("Email", [DataRequired()])
    first_name = StringField("First Name", [Length(max=64)])
    last_name = StringField("Last Name", [Length(max=64)])

    submit = SubmitField("Sign Up")

    def validate_username(self, username: StringField) -> None:
        user = UserModel.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is already registered.")

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email: StringField) -> None:
        user = UserModel.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This email is already registered.")


class SignInForm(FlaskForm):
    """User login form"""

    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember Me", default=True)

    submit = SubmitField("Sign In")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    """User registration route"""
    form = SignUpForm()

    if form.validate_on_submit():
        # noinspection PyArgumentList
        db.session.add(
            UserModel(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=UserModel.generate_hashed_password(form.password.data)
            )
        )
        db.session.commit()
        flash("Account created. You can login now.", "success")
        return redirect(url_for("signin"))
    return render_template("signup.html", form=form)


@app.route("/signin/", methods=["GET", "POST"])
def signin():
    """User login route"""

    form = SignInForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)

            return redirect(url_for("twis_list"))

        else:
            flash("Incorrect username or password. Please check.", "danger")

    return render_template("signin.html", form=form)


@app.route("/logout/")
def logout():
    """User logout route"""

    logout_user()
    redirect_to = url_for("twis_list")

    return redirect(redirect_to)


class TwisForm(FlaskForm):
    """Twis message form implementation"""

    twis_text = TextAreaField("Message: ", [DataRequired(), Length(max=255)])


@app.route("/")
def twis_list():
    """List all messages route"""
    if current_user.is_authenticated:
        object_list = TwisModel.query.order_by(desc(TwisModel.date)).all()
    else:
        return redirect(url_for("signin"))

    return render_template("twis_list.html", object_list=object_list)


@app.route("/my_twises/", methods=["GET", "POST"])
@login_required
def twis_my_list():
    """List all current user messages route"""
    if current_user.is_authenticated:
        object_list = current_user.twises
    else:
        return redirect(url_for("signin"))

    return render_template("twis_list.html", object_list=object_list)


@app.route("/create/", methods=["GET", "POST"])
@login_required
def twis_create():
    """Create new message route"""
    form = TwisForm()
    if request.method == "POST":
        db.session.add(
            TwisModel(
                value=form.twis_text.data,
                date=get_current_timestamp().replace(microsecond=0).isoformat(' '),
                user_name=current_user.username,
                user_id=current_user.id
            )
        )
        db.session.commit()
        flash("New message added", "success")
        return redirect(url_for("twis_list"))

    return render_template("twis_form.html", form=form)


@app.route("/update/<int:pk>", methods=["GET", "POST"])
@login_required
def twis_update(pk: int):
    """Update message route"""
    twis: TwisModel = TwisModel.query.get_or_404(pk)
    form = TwisForm(obj=twis)
    if request.method == "POST":
        twis.value = form.twis_text.data
        twis.date_update = get_current_timestamp().replace(microsecond=0).isoformat(' ')
        db.session.add(twis)
        db.session.commit()
        flash("Time report has been updated", "success")

        return redirect(url_for("twis_list"))

    return render_template("twis_form.html", form=form)


@app.route("/delete/<int:pk>", methods=["GET", "POST"])
@login_required
def twis_delete(pk: int):
    """Delete message route"""
    twis: TwisModel = TwisModel.query.get_or_404(pk)

    if twis.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        db.session.delete(twis)
        db.session.commit()
        flash("Twis has been deleted", "success")

        return redirect(url_for("twis_list"))

    return render_template("twis_delete.html", object=twis)


if __name__ == "__main__":
    app.run()
