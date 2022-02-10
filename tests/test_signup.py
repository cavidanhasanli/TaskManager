import pytest
from fastapi.testclient import TestClient

from app.main import app
from user.models import User


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)


def delete_test_user():
    try:
        qry = User.delete().where(User.user_name == "test_user")
        qry.execute()

    except Exception:
        pass


def test_create_user(test_app):
    delete_test_user()
    response = test_app.post(
        "/api/v1/create",
        json={
            "email": "test_mail@gmail.com",
            "password": "testpassword",
            "user_name": "test_user",
        },
    )
    assert response.status_code == 200


def test_create_user_duplicate(test_app):
    response = test_app.post(
        "/api/v1/create",
        json={
            "email": "test_mail@gmail.com",
            "password": "testpassword",
            "user_name": "test_user",
        },
    )
    delete_test_user()
    assert response.status_code == 400
