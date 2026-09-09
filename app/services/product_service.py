from sqlalchemy.orm import Session

from app.models.product import Product


def list_active_products(db: Session):
    return db.query(Product).filter(Product.is_active.is_(True)).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
