# schema.sql Explained (Line-by-Line)

This document explains each line of `db/schema.sql` in beginner-friendly terms.

---

## users table

`CREATE TABLE users (`
Creates a new table named `users`.

`id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,`
- `id`: column name.
- `INT`: whole number type.
- `PRIMARY KEY`: unique identifier for each row.
- `GENERATED ALWAYS AS IDENTITY`: auto-increment behavior for IDs.

`email VARCHAR(255) NOT NULL UNIQUE,`
- `VARCHAR(255)`: text up to 255 characters.
- `NOT NULL`: value is required.
- `UNIQUE`: no two users can share the same email.

`password_hash VARCHAR(255) NOT NULL,`
Stores hashed password text; must always exist.

`created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,`
Stores creation date/time.
- `DEFAULT CURRENT_TIMESTAMP`: auto-fills with current time.

`CHECK (LENGTH(TRIM(email)) > 0)`
Validation rule: email cannot be just blank spaces.

`);`
Ends the `users` table definition.

---

## products table

`CREATE TABLE products (`
Creates `products` table.

`id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,`
Auto-generated unique product ID.

`name VARCHAR(255) NOT NULL,`
Product name (required).

`description VARCHAR(1000),`
Optional product description up to 1000 characters.

`price DECIMAL(10, 2) NOT NULL,`
Money-like number:
- up to 10 total digits
- 2 digits after decimal
Required field.

`stock INT NOT NULL,`
Number of units available (required).

`is_active BOOLEAN NOT NULL DEFAULT TRUE,`
True/false flag for whether product is visible/available.
Defaults to `TRUE`.

`created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,`
When product row was created.

`CHECK (price >= 0),`
Price cannot be negative.

`CHECK (stock >= 0)`
Stock cannot be negative.

`);`
Ends `products` table definition.

---

## cart_items table

`CREATE TABLE cart_items (`
Creates `cart_items` table.

`id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,`
Auto-generated cart item ID.

`user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,`
- `user_id` is a **foreign key**.
- References `users.id` (foreign key target).
- `ON DELETE CASCADE`: if user is deleted, related cart items are deleted too.

`product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,`
- `product_id` is a **foreign key**.
- References `products.id` (foreign key target).
- If product is deleted, related cart rows are also removed.

`quantity INT NOT NULL,`
How many units user wants in cart (required).

`CONSTRAINT cart_items_user_product_unique UNIQUE (user_id, product_id),`
Named constraint:
same user cannot have duplicate rows for the same product.

`CHECK (quantity > 0)`
Quantity must be at least 1.

`);`
Ends `cart_items` table definition.

---

## orders table

`CREATE TABLE orders (`
Creates `orders` table.

`id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,`
Auto-generated order ID.

`user_id INT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,`
`user_id` is a **foreign key**.
Order belongs to one user.
References `users.id` (foreign key target).
`ON DELETE RESTRICT`: prevent deleting user if related orders exist.

`status VARCHAR(50) NOT NULL,`
Order status text (e.g., `pending`, `placed`, `cancelled`).

`total_amount DECIMAL(10, 2) NOT NULL,`
Total order price, required.

`created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,`
When order was created.

`CHECK (total_amount >= 0)`
Total cannot be negative.

`);`
Ends `orders` table definition.

---

## order_items table

`CREATE TABLE order_items (`
Creates `order_items` table (items inside an order).

`id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,`
Auto-generated order item ID.

`order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,`
`order_id` is a **foreign key**.
Links item to an order.
References `orders.id` (foreign key target).
If order is deleted, its order items are deleted too.

`product_id INT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,`
`product_id` is a **foreign key**.
Links item to a product.
References `products.id` (foreign key target).
`RESTRICT` prevents deleting product if it exists in past order records.

`quantity INT NOT NULL,`
Number of units bought for that product line.

`unit_price DECIMAL(10, 2) NOT NULL,`
Price per unit at purchase time (price snapshot).

`CHECK (quantity > 0),`
Bought quantity must be at least 1.

`CHECK (unit_price >= 0)`
Unit price cannot be negative.

`);`
Ends `order_items` table definition.

---

## Quick Foreign Key Summary

These columns are foreign keys in `schema.sql`:
- `cart_items.user_id -> users.id`
- `cart_items.product_id -> products.id`
- `orders.user_id -> users.id`
- `order_items.order_id -> orders.id`
- `order_items.product_id -> products.id`
