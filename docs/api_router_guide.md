# API Router Guide

This guide explains what a FastAPI router is and why the project uses one.

## 1. What is a router?

A router is a collection of related API endpoints.

Instead of putting every endpoint in `main.py`, you group endpoints by feature.

Example groups:
- auth router for registration and login
- product router for product listing and details
- cart router for cart actions
- order router for checkout and order history

## 2. Why use routers?

Routers keep the project organized.

They help you:
- separate features into different files
- keep `main.py` small
- make the code easier to read
- make it easier for beginners and contributors to find code

## 3. Example auth router

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
def register_user():
    pass

@router.post("/login")
def login_user():
    pass
```

This creates two routes:
- `POST /users/register`
- `POST /users/login`

## 4. What do `prefix` and `tags` do?

### `prefix`
The `prefix` is added to every route inside the router.

If the router uses:

```python
prefix="/users"
```

then:

```python
@router.post("/login")
```

becomes:

```text
/users/login
```

### `tags`
The `tags` value is used in the API docs.

It groups related endpoints together in Swagger UI.

## 5. How routers connect to `main.py`

A router does nothing until `main.py` includes it.

Example:

```python
from fastapi import FastAPI
from app.routers.auth import router as auth_router

app = FastAPI(title="Webstore API")
app.include_router(auth_router)
```

That tells FastAPI to use the auth routes.

## 6. Why this matters for the project

Routers are the main way we organize the backend by feature.

They help the code stay:
- modular
- beginner-friendly
- reusable
- easier to expand later

## 7. Summary

A router is a feature-based route group.

For this project:
- `app/routers/auth.py` handles auth endpoints
- later routers will handle products, cart, and orders
