# Product Service Guide

This file explains the first service layer file for products.

## 1. What is the service layer?

The service layer holds business logic.

The router receives HTTP requests, but the service decides what the app should do with the data.

For products, the service should:
- list active products
- fetch one product by id

## 2. Example service file

```python
from sqlalchemy.orm import Session

from app.models.product import Product


def list_active_products(db: Session):
    return db.query(Product).filter(Product.is_active.is_(True)).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
```

## 3. Syntax breakdown

### `db: Session`
This tells the function to accept a SQLAlchemy database session.

The session is what the app uses to talk to the database.

### `db.query(Product)`
This starts a query against the `products` table through the ORM model.

### `.filter(Product.is_active.is_(True))`
This keeps only products where `is_active` is true.

### `.all()`
Returns all matching rows as a list.

### `.first()`
Returns the first matching row, or `None` if nothing matches.

## 4. Why this is useful

The router should stay simple.

Instead of putting database query logic directly in the endpoint, the endpoint can call the service.

This keeps code cleaner and easier to reuse later.

## 5. How the router will use it

A future product router will likely call:

```python
products = list_active_products(db)
product = get_product_by_id(db, product_id)
```

That lets the router focus on HTTP and the service focus on database behavior.

## 6. Summary

The service layer is where product-related logic lives.

For this project, the first product service functions are:
- `list_active_products`
- `get_product_by_id`
