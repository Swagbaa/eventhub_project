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
    name = StringField("სახელი", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("ელფოსტა", validators=[DataRequired(), Email(), Length(max=140)])
    password = PasswordField("პაროლი", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        "გაიმეორეთ პაროლი",
        validators=[DataRequired(), EqualTo("password", message="პაროლები არ ემთხვევა")],
    )
    submit = SubmitField("რეგისტრაცია")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower().strip()).first():
            raise ValidationError("ეს ელფოსტა უკვე დარეგისტრირებულია.")


class LoginForm(FlaskForm):
    email = StringField("ელფოსტა", validators=[DataRequired(), Email()])
    password = PasswordField("პაროლი", validators=[DataRequired()])
    remember = BooleanField("დამახსოვრება")
    submit = SubmitField("შესვლა")


class EventForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired(), Length(max=140)])
    short_description = TextAreaField(
        "მოკლე აღწერა", validators=[DataRequired(), Length(max=280)]
    )
    full_description = TextAreaField("სრული აღწერა", validators=[DataRequired()])
    location = StringField("ლოკაცია (ქალაქი)", validators=[DataRequired(), Length(max=140)])
    date = DateField("თარიღი", validators=[DataRequired()], format="%Y-%m-%d")
    ticket_price = FloatField(
        "ბილეთის ფასი",
        validators=[Optional(), NumberRange(min=0, message="ფასი არ შეიძლება იყოს უარყოფითი")],
        default=0,
    )
    organizer = StringField("ორგანიზატორი", validators=[DataRequired(), Length(max=140)])
    category = SelectField(
        "კატეგორია", choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()]
    )
    submit = SubmitField("გამოქვეყნება")


class ProfileForm(FlaskForm):
    name = StringField("სახელი", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("ელფოსტა", validators=[DataRequired(), Email(), Length(max=140)])
    picture = FileField(
        "პროფილის სურათი", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"])]
    )
    submit = SubmitField("შენახვა")

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data.lower().strip()).first()
        if existing and existing.id != current_user.id:
            raise ValidationError("ეს ელფოსტა უკვე გამოიყენება სხვა მომხმარებლის მიერ.")
