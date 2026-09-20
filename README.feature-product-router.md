# Feature Branch README: `feature/product-router`

This branch exposes the first product API endpoints.

## Goal

Add product routes for listing active products and fetching a single product by id.

## Why This Branch Exists

Product service logic already has a clear direction, but users still need HTTP endpoints to browse the catalog through the API.

## Planned Work

- create a product router
- add `GET /products`
- add `GET /products/{id}`
- connect the router to `product_service.py`

## Expected Result

Users can browse products through the API with a clean separation between router and service layers.

## Likely Files

- `app/routers/product.py`
- `app/services/product_service.py`
- `app/main.py`

## Merge Back to Main

After this branch is merged, the backend exposes the first browsing endpoints for the store catalog.
