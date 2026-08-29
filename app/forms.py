from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from app.models import CATEGORIES, User


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=140)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("password", message="Password doesn't match")],
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower().strip()).first():
            raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Enter")


class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=140)])
    short_description = TextAreaField(
        "Short description", validators=[DataRequired(), Length(max=280)]
    )
    full_description = TextAreaField("Full description", validators=[DataRequired()])
    location = StringField("Location (City)", validators=[DataRequired(), Length(max=140)])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    ticket_price = FloatField(
        "Ticket price",
        validators=[Optional(), NumberRange(min=0, message="Price can't be negative")],
        default=0,
    )
    organizer = StringField("Organizer", validators=[DataRequired(), Length(max=140)])
    category = SelectField(
        "Category", choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()]
    )
    submit = SubmitField("Publish")


class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=140)])
    picture = FileField(
        "Profile picture", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"])]
    )
    submit = SubmitField("Save")

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data.lower().strip()).first()
        if existing and existing.id != current_user.id:
            raise ValidationError("This email is already used by another user.")
