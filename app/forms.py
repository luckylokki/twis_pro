from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.models import UserModel


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


class TwisForm(FlaskForm):
    """Twis message form implementation"""

    twis_text = TextAreaField("Message: ", [DataRequired(), Length(max=255)])
