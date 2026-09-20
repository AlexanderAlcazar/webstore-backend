from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    """Return the user with the requested email address, if one exists."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password_hash: str):
    """Persist a user and return its refreshed ORM instance."""
    new_user = User(email=email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
