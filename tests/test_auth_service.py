from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from app.core.security import hash_password, verify_password
from app.services.auth_service import login_user, register_user


def test_hash_password_stores_encoded_value_instead_of_plaintext():
    password = "practice-password"

    stored_hash = hash_password(password)

    assert stored_hash != password
    assert password not in stored_hash
    assert len(stored_hash) <= 255
    assert verify_password(password, stored_hash)


def test_hash_password_uses_a_different_salt_for_each_password():
    password = "practice-password"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
    assert verify_password(password, first_hash)
    assert verify_password(password, second_hash)


def test_verify_password_rejects_invalid_and_malformed_hashes():
    stored_hash = hash_password("practice-password")

    assert not verify_password("incorrect-password", stored_hash)
    assert not verify_password("practice-password", "not-a-password-hash")


def test_register_user_persists_a_hash_instead_of_the_submitted_password():
    db = Mock()

    with (
        patch("app.services.auth_service.get_user_by_email", return_value=None),
        patch("app.services.auth_service.create_user") as create_user,
    ):
        register_user(db, "customer@example.com", "practice-password")

    stored_hash = create_user.call_args.args[2]
    assert stored_hash != "practice-password"
    assert verify_password("practice-password", stored_hash)


def test_login_user_accepts_the_correct_password():
    db = Mock()
    user = SimpleNamespace(
        email="customer@example.com",
        password_hash=hash_password("practice-password"),
    )

    with patch("app.services.auth_service.get_user_by_email", return_value=user):
        assert login_user(db, "customer@example.com", "practice-password") is user


def test_login_user_rejects_an_incorrect_password():
    db = Mock()
    user = SimpleNamespace(
        email="customer@example.com",
        password_hash=hash_password("practice-password"),
    )

    with patch("app.services.auth_service.get_user_by_email", return_value=user):
        with pytest.raises(ValueError, match="Invalid credentials"):
            login_user(db, "customer@example.com", "incorrect-password")
