from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


@pytest.fixture
def client():
    db = Mock()
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_register_user_returns_public_user_data(client):
    user = SimpleNamespace(id=1, email="customer@example.com", password_hash="secret")

    with patch("app.routers.auth.auth_service.register_user", return_value=user) as register:
        response = client.post(
            "/users/register",
            json={"email": "customer@example.com", "password": "secret"},
        )

    assert response.status_code == 201
    assert response.json() == {"id": 1, "email": "customer@example.com"}
    register.assert_called_once()


def test_register_user_returns_conflict_for_existing_email(client):
    with patch(
        "app.routers.auth.auth_service.register_user",
        side_effect=ValueError("User already exists"),
    ):
        response = client.post(
            "/users/register",
            json={"email": "customer@example.com", "password": "secret"},
        )

    assert response.status_code == 409
    assert response.json() == {"detail": "User already exists"}


def test_login_user_returns_public_user_data(client):
    user = SimpleNamespace(id=1, email="customer@example.com", password_hash="secret")

    with patch("app.routers.auth.auth_service.login_user", return_value=user) as login:
        response = client.post(
            "/users/login",
            json={"email": "customer@example.com", "password": "secret"},
        )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": "customer@example.com"}
    login.assert_called_once()


def test_login_user_returns_unauthorized_for_invalid_credentials(client):
    with patch(
        "app.routers.auth.auth_service.login_user",
        side_effect=ValueError("Invalid credentials"),
    ):
        response = client.post(
            "/users/login",
            json={"email": "customer@example.com", "password": "wrong"},
        )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_auth_endpoints_reject_invalid_request_body(client):
    response = client.post(
        "/users/login",
        json={"email": "not-an-email", "password": ""},
    )

    assert response.status_code == 422
