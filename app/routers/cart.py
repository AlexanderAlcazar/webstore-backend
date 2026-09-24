from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.cart import AddCartItemRequest, CartResponse, UpdateCartItemRequest
from app.services import cart_service

router = APIRouter(prefix="/users/{user_id}/cart", tags=["cart"])


@router.get("", response_model=CartResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    """Return one user's cart and its current product details."""
    try:
        return cart_service.get_cart(db, user_id)
    except cart_service.CartUserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/items", response_model=CartResponse)
def add_cart_item(
    user_id: int,
    request: AddCartItemRequest,
    db: Session = Depends(get_db),
):
    """Create or increment an item, subject to the available product stock."""
    try:
        return cart_service.add_item(db, user_id, request.product_id, request.quantity)
    except (
        cart_service.CartUserNotFoundError,
        cart_service.ProductNotAvailableError,
    ) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except cart_service.InsufficientStockError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.patch("/items/{cart_item_id}", response_model=CartResponse)
def update_cart_item(
    user_id: int,
    cart_item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
):
    """Replace an owned cart item's quantity."""
    try:
        return cart_service.update_item(db, user_id, cart_item_id, request.quantity)
    except (
        cart_service.CartUserNotFoundError,
        cart_service.CartItemNotFoundError,
        cart_service.ProductNotAvailableError,
    ) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except cart_service.InsufficientStockError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    user_id: int,
    cart_item_id: int,
    db: Session = Depends(get_db),
) -> Response:
    """Remove an owned cart item."""
    try:
        cart_service.remove_item(db, user_id, cart_item_id)
    except (
        cart_service.CartUserNotFoundError,
        cart_service.CartItemNotFoundError,
    ) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
