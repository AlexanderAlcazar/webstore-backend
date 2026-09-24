from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User


class OrderUserNotFoundError(ValueError):
    """Raised when an order operation targets a user that does not exist."""


class EmptyCartError(ValueError):
    """Raised when checkout is requested for a cart without items."""


class CheckoutProductNotAvailableError(ValueError):
    """Raised when a cart item references an unavailable product."""


class CheckoutInsufficientStockError(ValueError):
    """Raised when a cart item quantity exceeds current product stock."""


def checkout(db: Session, user_id: int) -> Order:
    """Create an order from a cart and persist all inventory changes together."""
    try:
        _require_user(db, user_id)
        cart_items = _get_cart_items(db, user_id)
        if not cart_items:
            raise EmptyCartError("Cart is empty")

        _validate_cart_items(cart_items)
        total_amount = sum(
            (
                Decimal(cart_item.product.price) * cart_item.quantity
                for cart_item in cart_items
            ),
            start=Decimal("0"),
        )
        order = Order(user_id=user_id, status="placed", total_amount=total_amount)
        db.add(order)
        db.flush()

        for cart_item in cart_items:
            product = cart_item.product
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=cart_item.quantity,
                    unit_price=product.price,
                )
            )
            product.stock -= cart_item.quantity
            db.delete(cart_item)

        db.commit()
        return _get_order(db, order.id)
    except (
        OrderUserNotFoundError,
        EmptyCartError,
        CheckoutProductNotAvailableError,
        CheckoutInsufficientStockError,
        SQLAlchemyError,
    ):
        db.rollback()
        raise


def get_order_history(db: Session, user_id: int) -> list[Order]:
    """Return a user's orders, newest first, with their purchased items."""
    _require_user(db, user_id)
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc(), Order.id.desc())
        .all()
    )


def _require_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise OrderUserNotFoundError("User not found")
    return user


def _get_cart_items(db: Session, user_id: int) -> list[CartItem]:
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .order_by(CartItem.id)
        .all()
    )


def _validate_cart_items(cart_items: list[CartItem]) -> None:
    for cart_item in cart_items:
        product = cart_item.product
        if product is None or not product.is_active:
            raise CheckoutProductNotAvailableError("Product is no longer available")
        if cart_item.quantity > product.stock:
            raise CheckoutInsufficientStockError(
                "Requested quantity exceeds available stock"
            )


def _get_order(db: Session, order_id: int) -> Order:
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .one()
    )
