import datetime

import pytest

from app import create_app
from app.extensions import db as _db
from app.models import Event, User


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


@pytest.fixture()
def user_alice(db):
    user = User(name="Alice", email="alice@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def user_bob(db):
    user = User(name="Bob", email="bob@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def alice_event(db, user_alice):
    event = Event(
        title="Alice's Jazz Night",
        short_description="An evening of live jazz.",
        full_description="Doors open at 7pm, music starts at 8pm.",
        location="Tbilisi",
        date=datetime.date.today() + datetime.timedelta(days=10),
        ticket_price=15.0,
        organizer="Alice Events Co.",
        category="Music",
        author_id=user_alice.id,
    )
    db.session.add(event)
    db.session.commit()
    return event


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )
