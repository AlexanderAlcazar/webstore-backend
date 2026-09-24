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

## API Contract

Until a trusted authenticated-user dependency is added, every cart route identifies
the user through its path:

- `GET /users/{user_id}/cart`
- `POST /users/{user_id}/cart/items`
- `PATCH /users/{user_id}/cart/items/{cart_item_id}`
- `DELETE /users/{user_id}/cart/items/{cart_item_id}`

Add requests contain a positive `product_id` and positive `quantity`:

```json
{
  "product_id": 3,
  "quantity": 2
}
```

Adding an already-present product increases that item's quantity instead of creating
a duplicate row. Add and update requests reject quantities above available stock.
Cart responses include each item's product details and a subtotal; an empty cart
returns an empty `items` list and a `0.0` subtotal. Cart items may be changed or
removed only through the owning user's path.

## Likely Files

- `app/routers/cart.py`
- cart service or repository files if introduced
- `app/models/cart_item.py`
- `app/main.py`

## Merge Back to Main

After this branch is merged, the backend supports the cart stage of the purchasing flow.
