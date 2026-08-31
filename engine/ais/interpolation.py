"""Interpolate AIS positions to fill gaps."""

from __future__ import annotations


def interpolate(messages: list[dict]) -> list[dict]:
    """Return interpolated AIS positions (default linear)."""
    raise NotImplementedError