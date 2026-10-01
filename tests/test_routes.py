def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "EventHub".encode() in response.data or b"Events" in response.data


def test_about_page_loads_without_login(client):
    response = client.get("/about")
    assert response.status_code == 200


def test_unknown_route_returns_404(client):
    response = client.get("/this-route-does-not-exist")
    assert response.status_code == 404


def test_event_detail_page(client, alice_event):
    response = client.get(f"/event/{alice_event.id}")
    assert response.status_code == 200
    assert b"Alice" in response.data


def test_missing_event_returns_404(client):
    response = client.get("/event/9999")
    assert response.status_code == 404


def test_add_event_requires_login(client):
    response = client.get("/event/add", follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.request.path.encode()
