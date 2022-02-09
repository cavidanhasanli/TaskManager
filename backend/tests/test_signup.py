import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

def test_create_user(test_app):
    response = test_app.post("/api/v1/create", json={
        "email": "user1@example.com",
        "password": "strings",
        "user_name": "string1"
        })
    assert response.status_code == 200
    