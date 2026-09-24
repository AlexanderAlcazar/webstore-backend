# WebStore Backend

A beginner-friendly FastAPI backend for a web store MVP. The implemented API
currently supports health checks, account access, product browsing, cart
management, checkout, and order history.

## Current capabilities

- FastAPI application and interactive API documentation
- SQLAlchemy database engine and request-scoped session dependency
- User registration and login with validated request bodies
- PBKDF2 password hashing with a random salt and constant-time verification
- SQLAlchemy models for users, products, carts, orders, and order items
- Checkout with stock validation, cart cleanup, and immutable item prices
- User-scoped order history

## Run locally

Set `DATABASE_URL` to a SQLAlchemy-compatible database connection string before
starting the app. The repository's fallback value is only a placeholder and is
not a usable local database configuration.

```powershell
$env:DATABASE_URL = "postgresql://USER:PASSWORD@localhost:5432/webstore"
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; FastAPI's interactive
documentation is at `/docs`.

## Implemented endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Returns `{"status": "ok"}` when the application is running. |
| `POST` | `/users/register` | Creates a user and returns public user data. |
| `POST` | `/users/login` | Verifies a user's credentials and returns public user data. |
| `POST` | `/users/{user_id}/checkout` | Creates an order from the user's cart. |
| `GET` | `/users/{user_id}/orders` | Returns the user's completed orders, newest first. |

Registration and login accept the same JSON body. Emails are trimmed and must
be syntactically valid; passwords must be between 1 and 255 characters.

```json
{
  "email": "customer@example.com",
  "password": "example-password"
}
```

A successful registration returns `201 Created`; successful login returns
`200 OK`. Both responses exclude the password hash:

```json
{
  "id": 1,
  "email": "customer@example.com"
}
```

Registering an existing email returns `409 Conflict`. Invalid login credentials
return `401 Unauthorized`, and invalid request data returns FastAPI's `422`
validation response.

## Project layout

```text
app/
  core/          Configuration and password-security helpers
  db/            SQLAlchemy base class, engine, and session dependency
  models/        ORM mappings for the web-store entities
  repositories/  Database access helpers
  routers/       HTTP endpoints
  schemas/       Request and response models
  services/      Application business logic
  main.py        FastAPI application entry point
tests/           Authentication and database-session tests
docs/            MVP scope, schema, and beginner guides
```

## Planned work

The API supports the MVP shopping flow. The feature guides describe the
implementation order and scope for each branch.

## Checkout and order history

Checkout uses the items already stored in the selected user's cart, so its
request body is empty. A successful `POST /users/{user_id}/checkout` returns
`201 Created` with the order ID, status, checkout-time total, timestamp, and
item snapshots (`product_id`, `quantity`, and `unit_price`). It reduces stock
and clears the cart in one database transaction.

An empty cart returns `400 Bad Request`; unavailable or insufficient stock
returns `409 Conflict`; and an unknown user returns `404 Not Found`. `GET
/users/{user_id}/orders` returns that user's orders with the same item snapshots
or an empty list when none exist.

## Reference documentation

- [MVP scope](docs/MVP_SCOPE.md)
- [Feature branch plan](docs/branch_plan.md)
- [Database schema](docs/schema.sql) and [schema explanation](docs/schema_explained.md)
- [API router guide](docs/api_router_guide.md)
- [Authentication service guide](docs/auth_service_guide.md)
- [Product service guide](docs/product_service_guide.md)
- [Database configuration and session guide](docs/config_and_db_setup_guide.md)

## Contribution style

- Keep branches focused on one feature.
- Preserve the simple router, service, repository, and model separation.
- Prefer readable MVP code over unnecessary abstractions.
- Update tests and relevant documentation with behavior changes.
