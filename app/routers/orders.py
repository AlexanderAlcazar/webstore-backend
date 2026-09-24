from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderResponse
from app.services import order_service

router = APIRouter(prefix="/users/{user_id}", tags=["orders"])


@router.post("/checkout", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(user_id: int, db: Session = Depends(get_db)):
    """Purchase the user's cart and return the created order."""
    try:
        return order_service.checkout(db, user_id)
    except order_service.OrderUserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except order_service.EmptyCartError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except (
        order_service.CheckoutProductNotAvailableError,
        order_service.CheckoutInsufficientStockError,
    ) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.get("/orders", response_model=list[OrderResponse])
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    """Return the user's completed orders, newest first."""
    try:
        return order_service.get_order_history(db, user_id)
    except order_service.OrderUserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
