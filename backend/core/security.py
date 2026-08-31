"""Security helpers: JWT, password hashing, role checks, secret masking."""

from __future__ import annotations

import os

from backend.core.settings import get_settings


def jwt_secret() -> str:
    """Return the configured JWT signing secret, or raise if missing."""
    secret = get_settings().jwt.secret or os.getenv("JWT_SECRET")
    if not secret or len(secret) < 32:
        raise RuntimeError("JWT_SECRET is missing or shorter than 32 characters")
    return secret


def app_secret() -> str:
    secret = get_settings().secret_key or os.getenv("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not configured")
    return secret


def require_role(user_role: str, required: str) -> bool:
    """Minimal role hierarchy check; replace with a full RBAC implementation."""
    levels = {"viewer": 1, "analyst": 2, "admin": 3}
    return levels.get(user_role, 0) >= levels.get(required, 99)


def mask(value: str | None, keep: int = 4) -> str:
    """Return a masked representation of a secret suitable for logging."""
    if not value:
        return "<empty>"
    if len(value) <= keep * 2:
        return "*" * len(value)
    return f"{value[:keep]}{'*' * (len(value) - keep * 2)}{value[-keep:]}"


__all__ = ["jwt_secret", "app_secret", "require_role", "mask"]