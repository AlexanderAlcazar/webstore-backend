from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    """Describe the customer-safe product fields returned by browse endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: float
    stock: int
