# Feature Branch README: `feature/db-dependency`

This branch adds the reusable database dependency that FastAPI routes will use.

## Goal

Create a `get_db()` dependency that provides a SQLAlchemy session per request and closes it afterward.

## Why This Branch Exists

Routers need a clean and repeatable way to access the database without manually creating sessions inside every endpoint.

This branch establishes that shared dependency before more route work is added.

## Planned Work

- create `get_db()` in the database layer
- yield a request-scoped session
- close the session after the request finishes
- make the dependency ready for router use

## Expected Result

Routers can receive `db: Session` through FastAPI dependency injection in a standard and readable way.

## Likely Files

- `app/db/session.py`
- `app/main.py`
- router files that begin using the dependency

## Merge Back to Main

After this branch is complete, `main` gains the shared database dependency that future feature branches can reuse.
