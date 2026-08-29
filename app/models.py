from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

CATEGORIES = ["Music", "Tech", "Art", "Sport", "Education", "Business", "Other"]


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(140), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=False, default="default-avatar.svg")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    events = db.relationship(
        "Event", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    short_description = db.Column(db.String(280), nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(140), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False, default=0.0)
    organizer = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Other")

    # "posting date" — used to sort the event feed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Event {self.title!r}>"
