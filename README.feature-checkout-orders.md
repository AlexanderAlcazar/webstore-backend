# Feature Branch README: `feature/checkout-orders`

This branch implements the final purchase step and order history.

## Goal

Create checkout behavior that turns cart contents into an order and expose order history to the user.

## Why This Branch Exists

Checkout depends on products and carts already existing, so it belongs later in the branch order as the end-to-end purchase flow step.

## Planned Work

- create a checkout endpoint
- create an order and order items from cart contents
- reduce product stock
- clear purchased cart items
- add an endpoint to view user order history

## Expected Result

The core web store flow works end to end: cart contents can be purchased and users can view their past orders.

## Likely Files

- order or checkout router files
- order service files
- `app/models/order.py`
- `app/models/order_item.py`
- `app/main.py`

## Merge Back to Main

After this branch is merged, the project supports the main purchase and order-history experience of the MVP.
