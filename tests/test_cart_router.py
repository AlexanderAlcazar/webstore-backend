from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from app.services import cart_service


@pytest.fixture
def client():
    db = Mock()
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def _cart_response(quantity: int = 2):
    return {
        "user_id": 1,
        "items": [
            {
                "id": 8,
                "product_id": 3,
                "quantity": quantity,
                "product": {
                    "id": 3,
                    "name": "Notebook",
                    "description": "A ruled notebook",
                    "price": 9.99,
                    "stock": 10,
                },
            }
        ],
        "subtotal": quantity * 9.99,
    }


def test_cart_routes_delegate_to_service_and_return_lifecycle_responses(client):
    with (
        patch(
            "app.routers.cart.cart_service.get_cart",
            return_value={"user_id": 1, "items": [], "subtotal": 0},
        ) as get_cart,
        patch(
            "app.routers.cart.cart_service.add_item",
            return_value=_cart_response(),
        ) as add_item,
        patch(
            "app.routers.cart.cart_service.update_item",
            return_value=_cart_response(quantity=4),
        ) as update_item,
        patch("app.routers.cart.cart_service.remove_item") as remove_item,
    ):
        get_response = client.get("/users/1/cart")
        add_response = client.post(
            "/users/1/cart/items",
            json={"product_id": 3, "quantity": 2},
        )
        update_response = client.patch(
            "/users/1/cart/items/8",
            json={"quantity": 4},
        )
        remove_response = client.delete("/users/1/cart/items/8")

    assert get_response.status_code == 200
    assert get_response.json() == {"user_id": 1, "items": [], "subtotal": 0.0}
    assert add_response.status_code == 200
    assert add_response.json() == _cart_response()
    assert update_response.status_code == 200
    assert update_response.json() == _cart_response(quantity=4)
    assert remove_response.status_code == 204
    get_cart.assert_called_once()
    add_item.assert_called_once()
    update_item.assert_called_once()
    remove_item.assert_called_once()


@pytest.mark.parametrize(
    ("method", "url", "payload"),
    [
        ("post", "/users/1/cart/items", {"product_id": 0, "quantity": 1}),
        ("post", "/users/1/cart/items", {"product_id": 1, "quantity": 0}),
        ("patch", "/users/1/cart/items/8", {"quantity": 0}),
    ],
)
def test_cart_routes_reject_non_positive_input(client, method, url, payload):
    response = getattr(client, method)(url, json=payload)

    assert response.status_code == 422


def test_cart_routes_translate_ownership_and_stock_errors(client):
    with patch(
        "app.routers.cart.cart_service.update_item",
        side_effect=cart_service.CartItemNotFoundError("Cart item not found"),
    ):
        missing_response = client.patch(
            "/users/1/cart/items/8",
            json={"quantity": 2},
        )

    with patch(
        "app.routers.cart.cart_service.add_item",
        side_effect=cart_service.InsufficientStockError(
            "Requested quantity exceeds available stock"
        ),
    ):
        stock_response = client.post(
            "/users/1/cart/items",
            json={"product_id": 3, "quantity": 2},
        )

    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Cart item not found"}
    assert stock_response.status_code == 409
    assert stock_response.json() == {
        "detail": "Requested quantity exceeds available stock"
    }
