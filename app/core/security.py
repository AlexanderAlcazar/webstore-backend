"""Password hashing helpers used by authentication services."""

import base64
import binascii
import hashlib
import hmac
import secrets


# PBKDF2 is built into Python, so it is a practical way to learn the password
# hashing flow without adding a dependency. SHA-256 is the hash function that
# PBKDF2 repeatedly applies while deriving the stored password value.
_HASH_SCHEME = "pbkdf2"
_HASH_VERSION = "v1"
_ALGORITHM = "sha256"
_ITERATIONS = 600_000
_SALT_BYTES = 16
_DERIVED_KEY_BYTES = 32
_MAX_ITERATIONS = 2_000_000


def hash_password(password: str) -> str:
    """Create an encoded PBKDF2 password hash suitable for database storage."""
    # A unique random salt means the same password produces a different stored
    # value for every user, preventing precomputed-hash lookup attacks.
    salt = secrets.token_bytes(_SALT_BYTES)
    derived_key = hashlib.pbkdf2_hmac(
        _ALGORITHM,
        password.encode("utf-8"),
        salt,
        _ITERATIONS,
        dklen=_DERIVED_KEY_BYTES,
    )

    # Store a format version plus the parameters, salt, and derived key so
    # verification can reproduce this derivation even if defaults change later.
    return "$".join(
        (
            _HASH_SCHEME,
            _HASH_VERSION,
            _ALGORITHM,
            str(_ITERATIONS),
            _encode(salt),
            _encode(derived_key),
        )
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Return whether a password matches a previously encoded PBKDF2 hash."""
    try:
        (
            scheme,
            version,
            algorithm,
            iterations_text,
            salt_text,
            expected_key_text,
        ) = stored_hash.split("$")
        iterations = int(iterations_text)
        salt = _decode(salt_text)
        expected_key = _decode(expected_key_text)
    except (ValueError, binascii.Error):
        # A malformed stored value is never a valid password match.
        return False

    if (
        scheme != _HASH_SCHEME
        or version != _HASH_VERSION
        or algorithm != _ALGORITHM
        or not 1 <= iterations <= _MAX_ITERATIONS
        or not salt
        or len(expected_key) != _DERIVED_KEY_BYTES
    ):
        return False

    actual_key = hashlib.pbkdf2_hmac(
        algorithm,
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=_DERIVED_KEY_BYTES,
    )
    # compare_digest avoids returning early at the first differing byte, which
    # prevents the comparison itself from revealing partial match information.
    return hmac.compare_digest(actual_key, expected_key)


def _encode(value: bytes) -> str:
    """Encode binary values into text that can be stored in a VARCHAR column."""
    return base64.urlsafe_b64encode(value).decode("ascii")


def _decode(value: str) -> bytes:
    """Decode the text representation and reject invalid base64 input."""
    return base64.b64decode(value.encode("ascii"), altchars=b"-_", validate=True)
