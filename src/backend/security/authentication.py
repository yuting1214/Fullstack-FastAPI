import hashlib
import secrets

from src.backend.core.config import global_settings


def _digest(value: str) -> bytes:
    return hashlib.sha256(value.encode("utf-8")).digest()


def authenticate_user(username: str, password: str) -> bool:
    # Compare SHA-256 digests in constant time: prevents timing-based
    # probing and, since digests are fixed-length, leaks nothing about
    # credential length either.
    username_ok = secrets.compare_digest(_digest(username), _digest(global_settings.USER_NAME))
    password_ok = secrets.compare_digest(_digest(password), _digest(global_settings.PASSWORD))
    return username_ok and password_ok
