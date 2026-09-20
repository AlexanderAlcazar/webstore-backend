from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.repositories.user_repository import create_user, get_user_by_email


def register_user(db: Session, email: str, password: str):
    """Create a user with a securely hashed password.

    Raises:
        ValueError: If a user already has the submitted email address.
    """
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User already exists")

    return create_user(db, email, hash_password(password))


def login_user(db: Session, email: str, password: str):
    """Return the user whose credentials match the submitted values.

    Raises:
        ValueError: If the email is unknown or the password does not match.
    """
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    return user
