# WebStore Backend

This repository contains a beginner-friendly FastAPI backend for a web store MVP.

The current project goal is to support a simple shopping flow: register, log in, browse products, manage a cart, place an order, and view order history.

## MVP Focus

- user registration
- user login
- product browsing
- cart management
- checkout and order creation
- order confirmation and order history

The project intentionally avoids advanced architecture and advanced auth features so the code stays readable and appropriate for an undergraduate full-stack project.

## Current Project State

The repository already includes:

- FastAPI app setup
- database config and session setup
- SQLAlchemy models for users, products, cart items, orders, and order items
- auth router and auth service foundations
- a user repository
- a product service
- project planning and learning docs under `docs/`

## Feature Branch Guides

Each planned feature branch has its own README so the scope stays small and easy to review.

| Branch | README | Purpose |
| --- | --- | --- |
| `feature/db-dependency` | [`README.feature-db-dependency.md`](README.feature-db-dependency.md) | Add the reusable FastAPI database dependency |
| `feature/auth-schemas-and-router` | [`README.feature-auth-schemas-and-router.md`](README.feature-auth-schemas-and-router.md) | Make auth endpoints usable with schemas and router wiring |
| `feature/password-hashing` | [`README.feature-password-hashing.md`](README.feature-password-hashing.md) | Replace plain password comparison with hashing |
| `feature/product-router` | [`README.feature-product-router.md`](README.feature-product-router.md) | Expose product listing and detail endpoints |
| `feature/cart-router` | [`README.feature-cart-router.md`](README.feature-cart-router.md) | Implement shopping cart endpoints |
| `feature/checkout-orders` | [`README.feature-checkout-orders.md`](README.feature-checkout-orders.md) | Implement checkout and order history |
| `feature/docs-readme` | [`README.feature-docs-readme.md`](README.feature-docs-readme.md) | Improve onboarding and contributor docs |

## Recommended Branch Order

1. `feature/db-dependency`
2. `feature/auth-schemas-and-router`
3. `feature/password-hashing`
4. `feature/product-router`
5. `feature/cart-router`
6. `feature/checkout-orders`
7. `feature/docs-readme`

This order follows the backend dependency chain and keeps implementation steps small.

## Useful Docs

- [`docs/MVP_SCOPE.md`](docs/MVP_SCOPE.md)
- [`docs/branch_plan.md`](docs/branch_plan.md)
- [`docs/schema.sql`](docs/schema.sql)
- [`docs/schema_explained.md`](docs/schema_explained.md)
- [`docs/api_router_guide.md`](docs/api_router_guide.md)
- [`docs/auth_service_guide.md`](docs/auth_service_guide.md)
- [`docs/product_service_guide.md`](docs/product_service_guide.md)

## Contribution Style

- keep branches focused on one feature
- keep layers simple: router, service, repository, model
- prefer readable MVP code over complex abstractions
- merge features back into `main` after the branch goal is complete
