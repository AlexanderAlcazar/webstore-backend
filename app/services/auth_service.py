from sqlalchemy.orm import Session

from app.repositories.user_repository import create_user, get_user_by_email


def register_user(db: Session, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User already exists")

    return create_user(db, email, password)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    if user.password_hash != password:
        raise ValueError("Invalid credentials")

    return user
