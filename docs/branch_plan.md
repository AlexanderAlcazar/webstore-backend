# Branch Plan

This file explains the next backend steps using separate Git branches for separate features.

The goal is to keep the project organized, beginner-friendly, and within MVP scope.

## Current Project State

Right now, the project already has:

- MVP scope documentation
- database schema documentation
- SQLAlchemy models for users, products, cart items, orders, and order items
- database config and session setup
- a FastAPI app with a working `/health` endpoint
- an auth router
- an auth service
- a user repository
- a product service

This means the project has a strong foundation and is ready to move into real feature implementation.

## Why use separate branches?

Each branch should focus on one feature or one small architectural step.

This helps because:

- each feature is isolated
- changes are easier to review
- mistakes are easier to undo
- the project stays organized
- `main` stays more stable

For this project, branches should stay small and focused.

## Branch 1: `feature/db-dependency`

### Goal
Create a reusable FastAPI database dependency.

### Why this comes first
Routers will need a clean way to access the database session.

### Work in this branch
- create `get_db()` function
- yield a database session per request
- close the session after the request finishes

### Result
Routers can receive `db: Session` cleanly through FastAPI dependencies.

## Branch 2: `feature/auth-schemas-and-router`

### Goal
Make the auth router actually usable.

### Work in this branch
- create Pydantic request schemas for register and login
- create response shape for auth endpoints
- connect the auth router to `auth_service.py`
- return real responses instead of `pass`

### Result
`POST /users/register` and `POST /users/login` become real endpoints.

## Branch 3: `feature/password-hashing`

### Goal
Replace plain password comparison with proper hashing.

### Work in this branch
- hash password before saving new users
- verify hashed password at login
- keep the implementation simple and readable

### Result
Auth becomes safer while staying MVP-friendly.

## Branch 4: `feature/product-router`

### Goal
Expose the first product endpoints.

### Work in this branch
- create product router
- add `GET /products`
- add `GET /products/{id}`
- connect router to `product_service.py`

### Result
Users can browse the product catalog through the API.

## Branch 5: `feature/cart-router`

### Goal
Implement the shopping cart API.

### Work in this branch
- create cart router
- add endpoint to add item to cart
- add endpoint to update quantity
- add endpoint to remove item
- add endpoint to view cart

### Result
Users can build and manage a cart.

## Branch 6: `feature/checkout-orders`

### Goal
Implement order placement and order history.

### Work in this branch
- create checkout endpoint
- create order and order items from cart contents
- reduce product stock
- clear purchased cart items
- add endpoint to view user order history

### Result
The core webstore purchase flow works end-to-end.

## Branch 7: `feature/docs-readme`

### Goal
Improve contributor onboarding and project clarity.

### Work in this branch
- organize and review beginner docs
- link important docs from `README.md`
- explain project structure and setup steps

### Result
New contributors can understand the project more quickly.

## Recommended Order

Use this order:

1. `feature/db-dependency`
2. `feature/auth-schemas-and-router`
3. `feature/password-hashing`
4. `feature/product-router`
5. `feature/cart-router`
6. `feature/checkout-orders`
7. `feature/docs-readme`

## Why this order makes sense

This order follows the dependency chain of the backend:

- routers need the DB dependency
- auth needs schemas and service wiring
- auth should hash passwords before becoming more complete
- users should be able to browse products before using carts
- carts should exist before checkout
- docs are easiest to clean up after the implementation settles

## Scope Reminder

Stay within undergraduate MVP scope:

- do not add microservices
- do not add advanced auth flows yet
- do not add unnecessary abstractions
- keep router, service, repository, and model layers simple
- prefer small working features over complex architecture

## Summary

The project is now past setup and ready for feature implementation.

The next practical branch to start on is:

`feature/db-dependency`

After that, move directly into auth router wiring and schemas.
