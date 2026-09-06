# Config and Database Session Setup Guide

This guide explains why the project separates configuration from database setup.

## 1. Why use a config file?

A config file keeps environment-specific values in one place.

For example, the database URL is not something you want hardcoded in many files. If the database host, username, password, or port changes, you only update one place.

Example:

```python
# app/core/config.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/webstore",
)
```

This keeps the app easier to:
- move between local and production environments
- secure credentials outside the codebase
- update settings without hunting through many files

## 2. How the config connects to the app

The database session file imports the config value:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

This means:
- the config gives the connection string
- the session file uses it to create the database engine
- the app later uses `SessionLocal` to create database sessions

## 3. Why use a session factory?

A session factory is a reusable way to create database sessions.

This is important because each request should get its own DB session. You do not want one global session shared across everything.

The standard pattern is:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This gives each request a fresh database session.

## 4. Why not put everything in one file?

If you keep everything in one script, the project becomes harder to maintain.

Separation of concern means:
- config decides values
- database layer manages connections
- models define tables
- endpoints handle API requests

This makes the codebase easier to understand and extend.

## 5. Standard beginner-friendly structure

A clean beginner project layout is:

```text
app/
  core/
    config.py
  db/
    base.py
    session.py
  models/
    user.py
    product.py
    cart_item.py
    order.py
    order_item.py
  main.py
```

This pattern is simple and matches how many FastAPI projects are organized.

## 6. What this gives you before writing routes

At this point, the app has:
- a database connection engine
- a session factory
- model classes that map to tables
- a clean place to store config values

This is the foundation needed before adding endpoints like:
- register/login
- list products
- add to cart
- checkout

## 7. Summary

The config file and session file are not extra complexity. They are the foundation of a proper backend.

They help you:
- keep database settings in one place
- create a reusable DB session
- keep app code cleaner
- prepare the project for routes and business logic
