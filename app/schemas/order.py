from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemResponse(BaseModel):
    """Describe an immutable product snapshot from a completed order."""

    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    """Describe a completed order and the items purchased in it."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemResponse]
