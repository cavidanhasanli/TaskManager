import pytest
from fastapi.testclient import TestClient

from app.main import app

from .test_signup import test_create_user


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_task_status(test_app):
    test_create_user(test_app)
    response = test_app.post(
        "/api/v1/login", json={"password": "testpassword", "user_name": "test_user"}
    )
    access_token = response.json()["access_token"]
    response = test_app.post(
        "/api/v1/task",
        json={"address": "149.126.117.161"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    task_id = response.json()["task_id"]
    response = test_app.get(f"/api/v1/status/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
