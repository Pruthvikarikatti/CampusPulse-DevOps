import pytest
from app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    import app as app_module

    test_database = tmp_path / "test_campuspulse.db"
    monkeypatch.setattr(app_module, "DATABASE", test_database)
    init_db()

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_submit_incident(client):
    response = client.post(
        "/",
        data={
            "title": "Wi-Fi not working",
            "category": "Wi-Fi / Internet",
            "location": "Computer Lab",
            "description": "Internet connection is unavailable.",
            "priority": "High",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Incident reported successfully!" in response.data
    assert b"Wi-Fi not working" in response.data