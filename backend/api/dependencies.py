"""Shared FastAPI dependencies (DB session, current user, settings)."""

from __future__ import annotations

from collections.abc import Generator

from backend.core.config import Settings, get_settings
from fastapi import Depends


def get_db() -> Generator:
    """Yield a database session. Replace with real session factory."""
    raise NotImplementedError


def get_settings_dep() -> Settings:
    return get_settings()


__all__ = ["Depends", "get_db", "get_settings_dep"]