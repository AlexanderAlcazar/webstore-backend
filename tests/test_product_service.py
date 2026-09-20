from unittest.mock import Mock

from app.models.product import Product
from app.services.product_service import list_active_products


def test_list_active_products_filters_out_inactive_products():
    db = Mock()
    query = db.query.return_value
    query.filter.return_value = query

    list_active_products(db)

    db.query.assert_called_once_with(Product)
    filter_clause = query.filter.call_args.args[0]
    assert filter_clause.compare(Product.is_active.is_(True))
