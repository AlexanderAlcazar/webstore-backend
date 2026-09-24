from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from app.services import order_service


@pytest.fixture
def client():
    db = Mock()
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def _order_response(order_id: int = 9):
    return {
        "id": order_id,
        "user_id": 1,
        "status": "placed",
        "total_amount": 22.48,
        "created_at": datetime(2026, 1, 2, 3, 4, 5),
        "items": [
            {
                "product_id": 3,
                "quantity": 2,
                "unit_price": 9.99,
            }
        ],
    }


def test_order_routes_delegate_and_return_checkout_and_history_responses(client):
    created_order = _order_response()
    history = [_order_response(order_id=10), created_order]

    with (
        patch(
            "app.routers.orders.order_service.checkout",
            return_value=created_order,
        ) as checkout,
        patch(
            "app.routers.orders.order_service.get_order_history",
            return_value=history,
        ) as get_order_history,
    ):
        checkout_response = client.post("/users/1/checkout")
        history_response = client.get("/users/1/orders")

    assert checkout_response.status_code == 201
    assert checkout_response.json() == {
        **_order_response(),
        "created_at": "2026-01-02T03:04:05",
    }
    assert history_response.status_code == 200
    assert history_response.json() == [
        {
            **_order_response(order_id=10),
            "created_at": "2026-01-02T03:04:05",
        },
        {
            **_order_response(),
            "created_at": "2026-01-02T03:04:05",
        },
    ]
    checkout.assert_called_once()
    get_order_history.assert_called_once()


@pytest.mark.parametrize(
    ("error", "expected_status", "expected_detail"),
    [
        (order_service.OrderUserNotFoundError("User not found"), 404, "User not found"),
        (order_service.EmptyCartError("Cart is empty"), 400, "Cart is empty"),
        (
            order_service.CheckoutProductNotAvailableError(
                "Product is no longer available"
            ),
            409,
            "Product is no longer available",
        ),
        (
            order_service.CheckoutInsufficientStockError(
                "Requested quantity exceeds available stock"
            ),
            409,
            "Requested quantity exceeds available stock",
        ),
    ],
)
def test_checkout_route_translates_expected_errors(
    client,
    error,
    expected_status,
    expected_detail,
):
    with patch("app.routers.orders.order_service.checkout", side_effect=error):
        response = client.post("/users/1/checkout")

    assert response.status_code == expected_status
    assert response.json() == {"detail": expected_detail}


def test_order_history_returns_not_found_for_unknown_user(client):
    with patch(
        "app.routers.orders.order_service.get_order_history",
        side_effect=order_service.OrderUserNotFoundError("User not found"),
    ):
        response = client.get("/users/1/orders")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
