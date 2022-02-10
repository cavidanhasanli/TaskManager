import pytest
from fastapi.testclient import TestClient

from app.main import app

from .test_signup import delete_test_user, test_create_user


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def test_login(test_app):
    test_create_user(test_app)
    response = test_app.post(
        "/api/v1/login", json={"password": "testpassword", "user_name": "test_user"}
    )
    assert response.status_code == 200


def test_login_wrong_password(test_app):
    response = test_app.post(
        "/api/v1/login", json={"password": "", "user_name": "test_user"}
    )
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "password"],
                "msg": "ensure this value has at least 7 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 7},
            }
        ]
    }
    assert response.status_code == 422


def test_login_wrong_username(test_app):
    response = test_app.post(
        "/api/v1/login",
        json={"password": "testpassword", "user_name": "nonexistinguser"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User with given username not found"}
    delete_test_user()
