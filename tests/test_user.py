import fastapi_jwt_auth
import pytest
from fastapi.testclient import TestClient

from app.main import app

from .test_signup import test_create_user


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_user(test_app):
    test_create_user(test_app)
    response = test_app.post(
        "/api/v1/login", json={"password": "testpassword", "user_name": "test_user"}
    )
    access_token = response.json()["access_token"]
    response = test_app.get(
        "/api/v1/user", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"user": "test_user", "email": "test_mail@gmail.com"}


def test_user_invalid_header(test_app):
    with pytest.raises(fastapi_jwt_auth.exceptions.InvalidHeaderError):
        test_app.get("/api/v1/user", headers={"Authorization": "Bearer "})
