from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.services import order_service


@pytest.fixture
def db():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def _create_user(db: Session, email: str) -> User:
    user = User(email=email, password_hash="hashed-password")
    db.add(user)
    db.commit()
    return user


def _create_product(
    db: Session,
    *,
    name: str,
    price: Decimal,
    stock: int,
    is_active: bool = True,
) -> Product:
    product = Product(
        name=name,
        description=f"{name} description",
        price=price,
        stock=stock,
        is_active=is_active,
    )
    db.add(product)
    db.commit()
    return product


def _add_cart_item(db: Session, user_id: int, product_id: int, quantity: int) -> None:
    db.add(CartItem(user_id=user_id, product_id=product_id, quantity=quantity))
    db.commit()


def test_checkout_creates_order_snapshots_reduces_stock_and_clears_cart(db):
    user = _create_user(db, "customer@example.com")
    notebook = _create_product(
        db,
        name="Notebook",
        price=Decimal("9.99"),
        stock=5,
    )
    pen = _create_product(
        db,
        name="Pen",
        price=Decimal("2.50"),
        stock=3,
    )
    _add_cart_item(db, user.id, notebook.id, 2)
    _add_cart_item(db, user.id, pen.id, 1)

    order = order_service.checkout(db, user.id)

    assert order.user_id == user.id
    assert order.status == "placed"
    assert order.total_amount == Decimal("22.48")
    assert [(item.product_id, item.quantity, item.unit_price) for item in order.items] == [
        (notebook.id, 2, Decimal("9.99")),
        (pen.id, 1, Decimal("2.50")),
    ]
    assert db.get(Product, notebook.id).stock == 3
    assert db.get(Product, pen.id).stock == 2
    assert db.query(CartItem).filter(CartItem.user_id == user.id).count() == 0


def test_checkout_rejects_empty_cart_without_creating_an_order(db):
    user = _create_user(db, "customer@example.com")

    with pytest.raises(order_service.EmptyCartError, match="Cart is empty"):
        order_service.checkout(db, user.id)

    assert db.query(Order).count() == 0


def test_checkout_rejects_insufficient_stock_without_partial_state(db):
    user = _create_user(db, "customer@example.com")
    in_stock = _create_product(
        db,
        name="Notebook",
        price=Decimal("9.99"),
        stock=5,
    )
    out_of_stock = _create_product(
        db,
        name="Pen",
        price=Decimal("2.50"),
        stock=1,
    )
    _add_cart_item(db, user.id, in_stock.id, 2)
    _add_cart_item(db, user.id, out_of_stock.id, 2)

    with pytest.raises(
        order_service.CheckoutInsufficientStockError,
        match="Requested quantity exceeds available stock",
    ):
        order_service.checkout(db, user.id)

    assert db.query(Order).count() == 0
    assert db.get(Product, in_stock.id).stock == 5
    assert db.get(Product, out_of_stock.id).stock == 1
    assert db.query(CartItem).filter(CartItem.user_id == user.id).count() == 2


def test_order_history_is_scoped_to_user_and_orders_newest_first(db):
    first_user = _create_user(db, "first@example.com")
    second_user = _create_user(db, "second@example.com")
    product = _create_product(
        db,
        name="Notebook",
        price=Decimal("9.99"),
        stock=10,
    )
    _add_cart_item(db, first_user.id, product.id, 1)
    first_order = order_service.checkout(db, first_user.id)
    _add_cart_item(db, second_user.id, product.id, 1)
    order_service.checkout(db, second_user.id)
    _add_cart_item(db, first_user.id, product.id, 1)
    second_order = order_service.checkout(db, first_user.id)

    history = order_service.get_order_history(db, first_user.id)

    assert [order.id for order in history] == [second_order.id, first_order.id]
    assert all(order.user_id == first_user.id for order in history)
    assert all(len(order.items) == 1 for order in history)
