import pytest
from fastapi.testclient import TestClient

from app.main import app

from .test_signup import test_create_user


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_refresh_token(test_app):
    test_create_user(test_app)
    response = test_app.post(
        "/api/v1/login", json={"password": "testpassword", "user_name": "test_user"}
    )
    refresh_token = response.json()["refresh_token"]
    response = test_app.post(
        "/api/v1/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
