import fastapi_jwt_auth
import pytest
from fastapi.testclient import TestClient

from app.main import app

from .test_signup import test_create_user


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_create_task(test_app):
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
    assert response.status_code == 200


def test_create_task_wrong_ip(test_app):
    response = test_app.post(
        "/api/v1/login", json={"password": "testpassword", "user_name": "test_user"}
    )
    access_token = response.json()["access_token"]
    response = test_app.post(
        "/api/v1/task",
        json={"address": "21131113"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Task not created: '21131113' does not appear to be an IPv4 or IPv6 address"
    }


def test_create_invalid_header(test_app):
    with pytest.raises(fastapi_jwt_auth.exceptions.InvalidHeaderError):
        test_app.post(
            "/api/v1/task",
            headers={"Authorization": "Bearer "},
        )
