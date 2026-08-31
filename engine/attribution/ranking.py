"""Composite ranking of attribution candidates."""

from __future__ import annotations


def rank(scored: list[dict], weights: dict) -> list[dict]:
    """Combine per-signal scores with `weights` and return ordered list."""
    raise NotImplementedError