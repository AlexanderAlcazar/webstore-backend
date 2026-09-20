from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.product import Product
from app.models.user import User
from app.services import cart_service


@pytest.fixture
def db():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def _create_user(db: Session, email: str = "customer@example.com") -> User:
    user = User(email=email, password_hash="hashed-password")
    db.add(user)
    db.commit()
    return user


def _create_product(
    db: Session,
    *,
    name: str = "Notebook",
    price: Decimal = Decimal("9.99"),
    stock: int = 5,
    is_active: bool = True,
) -> Product:
    product = Product(
        name=name,
        description="A ruled notebook",
        price=price,
        stock=stock,
        is_active=is_active,
    )
    db.add(product)
    db.commit()
    return product


def test_cart_lifecycle_merges_items_and_returns_subtotal(db):
    user = _create_user(db)
    product = _create_product(db)

    cart = cart_service.add_item(db, user.id, product.id, 2)
    merged_cart = cart_service.add_item(db, user.id, product.id, 1)
    updated_cart = cart_service.update_item(db, user.id, cart.items[0].id, 4)
    cart_service.remove_item(db, user.id, cart.items[0].id)
    empty_cart = cart_service.get_cart(db, user.id)

    assert cart.model_dump() == {
        "user_id": user.id,
        "items": [
            {
                "id": cart.items[0].id,
                "product_id": product.id,
                "quantity": 2,
                "product": {
                    "id": product.id,
                    "name": "Notebook",
                    "description": "A ruled notebook",
                    "price": 9.99,
                    "stock": 5,
                },
            }
        ],
        "subtotal": 19.98,
    }
    assert merged_cart.items[0].quantity == 3
    assert merged_cart.subtotal == 29.97
    assert updated_cart.items[0].quantity == 4
    assert updated_cart.subtotal == 39.96
    assert empty_cart.model_dump() == {
        "user_id": user.id,
        "items": [],
        "subtotal": 0.0,
    }


def test_cart_service_rejects_unavailable_or_overstocked_products(db):
    user = _create_user(db)
    active_product = _create_product(db, stock=2)
    inactive_product = _create_product(db, name="Archived", is_active=False)

    with pytest.raises(
        cart_service.ProductNotAvailableError,
        match="Product not found",
    ):
        cart_service.add_item(db, user.id, inactive_product.id, 1)

    with pytest.raises(
        cart_service.ProductNotAvailableError,
        match="Product not found",
    ):
        cart_service.add_item(db, user.id, 999, 1)

    with pytest.raises(
        cart_service.InsufficientStockError,
        match="Requested quantity exceeds available stock",
    ):
        cart_service.add_item(db, user.id, active_product.id, 3)


def test_cart_service_scopes_updates_and_removals_to_owner(db):
    owner = _create_user(db)
    other_user = _create_user(db, email="other@example.com")
    product = _create_product(db)
    cart = cart_service.add_item(db, owner.id, product.id, 1)
    cart_item_id = cart.items[0].id

    with pytest.raises(cart_service.CartItemNotFoundError, match="Cart item not found"):
        cart_service.update_item(db, other_user.id, cart_item_id, 2)

    with pytest.raises(cart_service.CartItemNotFoundError, match="Cart item not found"):
        cart_service.remove_item(db, other_user.id, cart_item_id)

    assert cart_service.get_cart(db, owner.id).items[0].quantity == 1


def test_cart_service_rejects_missing_user(db):
    with pytest.raises(cart_service.CartUserNotFoundError, match="User not found"):
        cart_service.get_cart(db, 999)
