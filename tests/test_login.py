from tests.conftest import login


def test_register_creates_user_and_redirects_to_login(client, db):
    from app.models import User

    response = client.post(
        "/register",
        data={
            "name": "Nina",
            "email": "nina@example.com",
            "password": "supersecret",
            "confirm_password": "supersecret",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert User.query.filter_by(email="nina@example.com").first() is not None


def test_login_with_correct_credentials_succeeds(client, user_alice):
    response = login(client, "alice@example.com", "password123")
    assert response.status_code == 200
    assert b"Add Event" in response.data
    assert "Alice".encode() in response.data


def test_login_with_wrong_password_fails(client, user_alice):
    response = login(client, "alice@example.com", "wrong-password")
    assert response.status_code == 200
    assert b"Add Event" not in response.data


def test_logout_clears_session(client, user_alice):
    login(client, "alice@example.com", "password123")
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
