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


def test_list_products_returns_active_products(client):
    product = SimpleNamespace(
        id=1,
        name="Notebook",
        description="A ruled notebook",
        price=9.99,
        stock=12,
        is_active=True,
    )

    with patch(
        "app.routers.products.product_service.list_active_products",
        return_value=[product],
    ) as list_active_products:
        response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Notebook",
            "description": "A ruled notebook",
            "price": 9.99,
            "stock": 12,
        }
    ]
    list_active_products.assert_called_once()


def test_get_product_returns_active_product(client):
    product = SimpleNamespace(
        id=1,
        name="Notebook",
        description="A ruled notebook",
        price=9.99,
        stock=12,
        is_active=True,
    )

    with patch(
        "app.routers.products.product_service.get_product_by_id",
        return_value=product,
    ) as get_product_by_id:
        response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Notebook",
        "description": "A ruled notebook",
        "price": 9.99,
        "stock": 12,
    }
    get_product_by_id.assert_called_once()


@pytest.mark.parametrize("product", [None, SimpleNamespace(is_active=False)])
def test_get_product_returns_not_found_for_missing_or_inactive_product(client, product):
    with patch(
        "app.routers.products.product_service.get_product_by_id",
        return_value=product,
    ):
        response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
