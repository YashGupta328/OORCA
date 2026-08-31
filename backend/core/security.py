"""Security helpers: JWT, password hashing, role checks."""

from __future__ import annotations

import os


def jwt_secret() -> str:
    secret = os.getenv("SECRET_KEY")
    if not secret:
        raise RuntimeError("SECRET_KEY is not configured")
    return secret


def require_role(user_role: str, required: str) -> bool:
    """Minimal role hierarchy check; replace with a full RBAC implementation."""
    levels = {"viewer": 1, "analyst": 2, "admin": 3}
    return levels.get(user_role, 0) >= levels.get(required, 99)