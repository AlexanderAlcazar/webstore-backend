# Auth Service Guide

This file explains the auth service after adding a repository layer.

## 1. What changed?

The auth service no longer talks directly to SQLAlchemy queries for user lookup and creation.

Instead, it calls a repository that handles those database actions.

That gives us a cleaner layered design:
- router = HTTP requests
- service = auth rules
- repository = database access
- model = ORM table mapping

## 2. Updated service example

```python
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.repositories.user_repository import create_user, get_user_by_email


def register_user(db: Session, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User already exists")

    return create_user(db, email, hash_password(password))


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    return user
```

## 3. What moved into the repository?

The repository now handles:
- finding a user by email
- creating a new user row
- committing the transaction
- refreshing the new object

## 4. Syntax breakdown

### `get_user_by_email(db, email)`
This is a repository call.

The service asks the repository to look up the user instead of querying the model directly.

### `create_user(db, email, password)`
This creates the new user through the repository.

The service still decides *when* to create the user, but the repository decides *how* it is stored.

### `raise ValueError(...)`
The service still uses simple errors for the MVP.

That keeps the example easy to understand while the architecture stays layered.

## 5. Why this is better

This keeps the service focused on auth rules:
- does the user already exist?
- are the credentials valid?

The repository focuses on database details:
- query the user table
- insert new users
- persist changes

This separation makes the code easier to read, test, and extend.

## 6. Password hashing

The auth service now hashes a password before passing it to the repository.
The repository persists only the resulting encoded value; it never receives the
plaintext password.

`app/core/security.py` uses Python's built-in PBKDF2 implementation. For each
new password, it generates a random salt and derives a key by repeatedly
applying SHA-256. The stored text contains the PBKDF2 scheme, algorithm,
format version, iteration count, salt, and derived key, so a later login can
safely recreate the same derivation.

During login, `verify_password` derives a key using the saved parameters and
uses a constant-time comparison to decide whether it matches. Invalid stored
formats and wrong passwords both return an invalid-credentials result.

### Password-hashing syntax breakdown

#### `hash_password(password)`

This helper receives the plaintext password only long enough to create a
database-safe hash:

```python
password_hash = hash_password(password)
return create_user(db, email, password_hash)
```

- `password` is the value supplied in the registration request.
- `hash_password(...)` generates a random salt, runs PBKDF2, and returns one
  text value containing the data needed for verification.
- `password_hash` is passed to the repository. The plaintext `password` is not
  stored in the `users` table.

An illustrative returned value looks like this:

```text
pbkdf2$v1$sha256$600000$MDEyMzQ1Njc4OWFiY2RlZg==$ZXhhbXBsZS1kZXJpdmVkLWtleS0zMi1ieXRlcw==
```

The `$` character separates the scheme, format version, algorithm, iteration
count, encoded salt, and encoded derived key. The real salt and derived key are
different every time a password is hashed.

#### `verify_password(password, user.password_hash)`

This helper checks a submitted login password against the saved hash:

```python
if not verify_password(password, user.password_hash):
    raise ValueError("Invalid credentials")
```

- `user.password_hash` is the encoded text read from the database.
- `verify_password(...)` uses `split("$")` to recover the saved parameters,
  salt, and expected derived key.
- It derives a new key from the submitted `password` with those saved
  parameters.
- It returns `True` only when `hmac.compare_digest(...)` finds the newly
  derived key and saved key identical. `not` changes `True` to `False` and
  vice versa, so the error runs only when verification fails.

## 7. Summary

After the repository layer was added, the auth service became a rule/orchestration layer instead of a direct database layer.
