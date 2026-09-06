# SQLAlchemy Model Syntax Guide (Beginner)

This guide explains the minimum syntax needed to model a SQL table in Python with SQLAlchemy 2.0 style.

## 1. Imports

```python
from sqlalchemy import String, Integer, DateTime, Boolean, DECIMAL, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
```

- `Mapped[...]`: type annotation SQLAlchemy uses for ORM fields.
- `mapped_column(...)`: defines the actual DB column.
- `relationship(...)`: links models at ORM level (not a DB column by itself).
- `Base`: parent class for all models.

## 2. Basic Model Template

```python
class ModelName(Base):
    __tablename__ = "table_name"

    id: Mapped[int] = mapped_column(primary_key=True)

    __table_args__ = (
        # optional table constraints
    )
```

Required pieces:
- `class ... (Base)`
- `__tablename__ = "..."` (special SQLAlchemy dunder attribute)
- at least one primary key column

## 3. Common Column Patterns

### Primary key
```python
id: Mapped[int] = mapped_column(primary_key=True)
```

### Required text
```python
email: Mapped[str] = mapped_column(String(255), nullable=False)
```

### Unique value
```python
email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
```

### Optional text
```python
description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
```

### Numeric money-like field
```python
price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
```

### Boolean with default
```python
is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
```

### Timestamp with DB default
```python
created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())
```

## 4. Foreign Key Syntax

```python
user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
```

- `ForeignKey("users.id")` means this column references `users.id`.
- `ondelete="CASCADE"` matches DB delete behavior.

## 5. Relationship Syntax (ORM convenience)

```python
user: Mapped["User"] = relationship(back_populates="cart_items")
```

- Helps navigate objects in Python (`cart_item.user`).
- Does not replace DB foreign keys.

## 6. Table-Level Constraints

```python
__table_args__ = (
    CheckConstraint("quantity > 0", name="cart_items_quantity_positive"),
)
```

Use this for rules like:
- non-negative price/stock
- non-blank email
- positive quantities

## 7. Example: Minimal User Model

```python
from sqlalchemy import String, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("length(trim(email)) > 0", name="users_email_not_blank"),
    )
```

## 8. Mapping Rule of Thumb

For each SQL table:
- one model class
- each SQL column -> one `mapped_column`
- each SQL foreign key -> `ForeignKey(...)`
- each SQL check/unique rule -> matching SQLAlchemy constraint/column option
