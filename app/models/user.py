from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint("length(trim(email)) > 0", name="users_email_not_blank"),
    )
