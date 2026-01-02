import copy

from fastapi.testclient import TestClient
import src.app as app_module


import pytest


@pytest.fixture
def client():
    # snapshot activities and restore after test to keep tests isolated
    original = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    yield client
    app_module.activities = original


def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_and_unregister(client):
    email = "tester@mergington.edu"

    # signup
    r = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert r.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]

    # unregister
    r2 = client.post(f"/activities/Chess%20Club/unregister?email={email}")
    assert r2.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_not_found(client):
    r = client.post("/activities/Chess%20Club/unregister?email=not@there.edu")
    assert r.status_code == 404
