# User Repository Guide

This file explains the user repository and why it exists.

## 1. What is a repository?

A repository is the part of the backend that handles database access.

It sits between the service layer and the SQLAlchemy model/session.

## 2. Example repository file

```python
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password_hash: str):
    new_user = User(email=email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

## 3. Syntax breakdown

### `db: Session`
The repository receives a SQLAlchemy session.

That session lets the repository run queries and write changes.

### `db.query(User)`
This starts a query against the `users` table through the ORM model.

### `.filter(User.email == email)`
This narrows the query to the matching email.

### `.first()`
This returns the first matching record or `None`.

### `new_user = User(...)`
This creates a new ORM object that maps to a row in the database.

### `db.add(new_user)`
This stages the new object for insertion.

### `db.commit()`
This writes the staged change to the database.

### `db.refresh(new_user)`
This reloads the saved object so it includes generated fields like `id`.

## 4. Why use a repository?

Without a repository, service code starts to include database query details.

With a repository, the app becomes cleaner:
- router = HTTP layer
- service = business rules
- repository = data access
- model = table mapping

## 5. What the repository does in auth

For auth, the repository handles:
- finding a user by email
- creating a new user

The service decides:
- whether a user can be created
- whether credentials are valid

## 6. Summary

The user repository is a thin database access layer that keeps SQLAlchemy queries out of the service code.
