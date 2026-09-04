# MVP Scope

## Goal
This MVP is for students who want a reliable way to buy items online without waiting for seller replies. A user can register, browse products, add items to cart, checkout, receive order confirmation, and view order history.

## Must-have Features (v1)
- User registration
- User login
- Basic authentication only (email + password credential verification)
- Browse products
- Add items to cart
- Checkout and place order
- Receive order confirmation
- View order history

## Non-goals (v1)
- Recommendations
- Real payment integration
- Seller reviews
- Advanced authentication (OAuth, social login, MFA, password reset flows)

## User Flows (v1)
1. Register/Login: user creates an account or logs in.
2. Browse Products: user views product list and product details.
3. Cart: user adds or removes items and updates quantity.
4. Checkout: user places an order; system verifies stock and creates order.
5. Confirmation + History: user sees order confirmation and can view past orders.

## Acceptance Criteria (v1)
- Register/Login: valid credentials log in successfully, invalid credentials are rejected.
- Browse Products: only active products are listed, and product detail includes price and stock.
- Cart: user can add, update, and remove cart items; quantity cannot exceed available stock.
- Checkout: order is created from cart items, and product stock is reduced after order placement.
- Confirmation + History: user receives an order confirmation with order ID and can view only their own order history.

## Database Schema Draft (v1)

### users
- id (PK)
- email (UNIQUE, NOT NULL)
- password_hash (NOT NULL)
- created_at (NOT NULL)

Constraints:
- email must be unique
- email cannot be empty

### products
- id (PK)
- name (NOT NULL)
- description (NULL allowed)
- price (NOT NULL)
- stock (NOT NULL)
- is_active (NOT NULL, default true)
- created_at (NOT NULL)

Constraints:
- price >= 0
- stock >= 0

### cart_items
- id (PK)
- user_id (FK -> users.id, NOT NULL)
- product_id (FK -> products.id, NOT NULL)
- quantity (NOT NULL)

Constraints:
- quantity > 0
- (user_id, product_id) unique to prevent duplicate cart rows per product

### orders
- id (PK)
- user_id (FK -> users.id, NOT NULL)
- status (NOT NULL)
- total_amount (NOT NULL)
- created_at (NOT NULL)

Constraints:
- total_amount >= 0

### order_items
- id (PK)
- order_id (FK -> orders.id, NOT NULL)
- product_id (FK -> products.id, NOT NULL)
- quantity (NOT NULL)
- unit_price (NOT NULL)

Constraints:
- quantity > 0
- unit_price >= 0
