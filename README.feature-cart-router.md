# Feature Branch README: `feature/cart-router`

This branch adds the shopping cart API.

## Goal

Implement endpoints for viewing a cart and managing cart items.

## Why This Branch Exists

The MVP shopping flow needs a place for users to build up items before checkout, so cart operations should be isolated into their own feature branch.

## Planned Work

- create a cart router
- add endpoint to add an item to the cart
- add endpoint to update item quantity
- add endpoint to remove an item
- add endpoint to view the cart

## Expected Result

Users can build and manage a cart through clear API endpoints.

## Likely Files

- `app/routers/cart.py`
- cart service or repository files if introduced
- `app/models/cart_item.py`
- `app/main.py`

## Merge Back to Main

After this branch is merged, the backend supports the cart stage of the purchasing flow.
