import pytest
import os
os.environ["TESTING"] = "1"
os.environ["DB_HOST"] = "nonexistent"
from app import app   # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_hello(client):
    res = client.get("/hello")
    assert res.status_code == 200
    assert "message" in res.get_json()
