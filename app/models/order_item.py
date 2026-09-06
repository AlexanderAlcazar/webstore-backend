from sqlalchemy import CheckConstraint, Decimal, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Decimal(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="order_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="order_items_unit_price_non_negative"),
    )
