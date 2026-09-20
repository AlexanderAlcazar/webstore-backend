from sqlalchemy.orm import Session, joinedload

from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemResponse, CartResponse
from app.schemas.product import ProductResponse


class CartUserNotFoundError(ValueError):
    """Raised when a cart operation targets a user that does not exist."""


class CartItemNotFoundError(ValueError):
    """Raised when an item is absent from the requested user's cart."""


class ProductNotAvailableError(ValueError):
    """Raised when a requested product is missing or inactive."""


class InsufficientStockError(ValueError):
    """Raised when a requested cart quantity exceeds product stock."""


def get_cart(db: Session, user_id: int) -> CartResponse:
    """Return the specified user's cart, including product details and subtotal."""
    _require_user(db, user_id)
    return _build_cart(user_id, _get_cart_items(db, user_id))


def add_item(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
) -> CartResponse:
    """Add to an existing product row or create a new item in the user's cart."""
    _require_user(db, user_id)
    product = _require_available_product(db, product_id)
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id,
        )
        .first()
    )
    new_quantity = quantity if cart_item is None else cart_item.quantity + quantity
    _require_stock(product, new_quantity)

    if cart_item is None:
        db.add(CartItem(user_id=user_id, product_id=product_id, quantity=quantity))
    else:
        cart_item.quantity = new_quantity

    db.commit()
    return _build_cart(user_id, _get_cart_items(db, user_id))


def update_item(
    db: Session,
    user_id: int,
    cart_item_id: int,
    quantity: int,
) -> CartResponse:
    """Replace the quantity of an item owned by the specified user."""
    _require_user(db, user_id)
    cart_item = _require_cart_item(db, user_id, cart_item_id)
    _require_stock(_require_available_product(db, cart_item.product_id), quantity)
    cart_item.quantity = quantity
    db.commit()
    return _build_cart(user_id, _get_cart_items(db, user_id))


def remove_item(db: Session, user_id: int, cart_item_id: int) -> None:
    """Delete an item only when it belongs to the specified user's cart."""
    _require_user(db, user_id)
    db.delete(_require_cart_item(db, user_id, cart_item_id))
    db.commit()


def _require_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise CartUserNotFoundError("User not found")
    return user


def _require_available_product(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None or not product.is_active:
        raise ProductNotAvailableError("Product not found")
    return product


def _require_cart_item(db: Session, user_id: int, cart_item_id: int) -> CartItem:
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_item_id,
            CartItem.user_id == user_id,
        )
        .first()
    )
    if cart_item is None:
        raise CartItemNotFoundError("Cart item not found")
    return cart_item


def _get_cart_items(db: Session, user_id: int) -> list[CartItem]:
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .order_by(CartItem.id)
        .all()
    )


def _require_stock(product: Product, quantity: int) -> None:
    if quantity > product.stock:
        raise InsufficientStockError("Requested quantity exceeds available stock")


def _build_cart(user_id: int, cart_items: list[CartItem]) -> CartResponse:
    items = [
        CartItemResponse(
            id=cart_item.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            product=ProductResponse.model_validate(cart_item.product),
        )
        for cart_item in cart_items
    ]
    return CartResponse(
        user_id=user_id,
        items=items,
        subtotal=sum(item.quantity * item.product.price for item in items),
    )
