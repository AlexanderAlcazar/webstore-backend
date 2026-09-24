from unittest.mock import Mock, patch

from app.db.session import get_db


def test_get_db_yields_a_session_and_closes_it():
    session = Mock()

    with patch("app.db.session.SessionLocal", return_value=session):
        dependency = get_db()

        assert next(dependency) is session

        dependency.close()

    session.close.assert_called_once_with()


def test_get_db_closes_session_after_route_error():
    session = Mock()

    with patch("app.db.session.SessionLocal", return_value=session):
        dependency = get_db()
        next(dependency)

        try:
            dependency.throw(RuntimeError("endpoint failed"))
        except RuntimeError as error:
            assert str(error) == "endpoint failed"

    session.close.assert_called_once_with()
