from tests.conftest import login


def test_owner_can_view_edit_page(client, user_alice, alice_event):
    login(client, "alice@example.com", "password123")
    response = client.get(f"/event/{alice_event.id}/edit")
    assert response.status_code == 200


def test_other_user_cannot_edit_event(client, user_bob, alice_event):
    login(client, "bob@example.com", "password123")
    response = client.get(f"/event/{alice_event.id}/edit")
    assert response.status_code == 403


def test_other_user_cannot_delete_event(client, db, user_bob, alice_event):
    from app.models import Event

    login(client, "bob@example.com", "password123")
    response = client.post(f"/event/{alice_event.id}/delete")
    assert response.status_code == 403
    assert db.session.get(Event, alice_event.id) is not None


def test_anonymous_user_cannot_delete_event(client, alice_event):
    response = client.post(f"/event/{alice_event.id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert "login".encode() in response.request.path.encode()
