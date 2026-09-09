# Auth Service Guide

This file explains the auth service after adding a repository layer.

## 1. What changed?

The auth service no longer talks directly to SQLAlchemy queries for user lookup and creation.

Instead, it calls a repository that handles those database actions.

That gives us a cleaner layered design:
- router = HTTP requests
- service = auth rules
- repository = database access
- model = ORM table mapping

## 2. Updated service example

```python
from sqlalchemy.orm import Session

from app.repositories.user_repository import create_user, get_user_by_email


def register_user(db: Session, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User already exists")

    return create_user(db, email, password)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    if user.password_hash != password:
        raise ValueError("Invalid credentials")

    return user
```

## 3. What moved into the repository?

The repository now handles:
- finding a user by email
- creating a new user row
- committing the transaction
- refreshing the new object

## 4. Syntax breakdown

### `get_user_by_email(db, email)`
This is a repository call.

The service asks the repository to look up the user instead of querying the model directly.

### `create_user(db, email, password)`
This creates the new user through the repository.

The service still decides *when* to create the user, but the repository decides *how* it is stored.

### `raise ValueError(...)`
The service still uses simple errors for the MVP.

That keeps the example easy to understand while the architecture stays layered.

## 5. Why this is better

This keeps the service focused on auth rules:
- does the user already exist?
- are the credentials valid?

The repository focuses on database details:
- query the user table
- insert new users
- persist changes

This separation makes the code easier to read, test, and extend.

## 6. Password note

The current example still stores the incoming password directly in `password_hash` for learning simplicity.

That is temporary. In a real app, this should be a hashed password.

## 7. Summary

After the repository layer was added, the auth service became a rule/orchestration layer instead of a direct database layer.
