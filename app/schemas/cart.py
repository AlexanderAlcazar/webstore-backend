from typing import Annotated

from pydantic import BaseModel, Field

from app.schemas.product import ProductResponse

PositiveInteger = Annotated[int, Field(gt=0)]


class AddCartItemRequest(BaseModel):
    product_id: PositiveInteger
    quantity: PositiveInteger


class UpdateCartItemRequest(BaseModel):
    quantity: PositiveInteger


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse


class CartResponse(BaseModel):
    user_id: int
    items: list[CartItemResponse]
    subtotal: float
