"""Clean raw AIS messages: schema validation, deduplication, plausibility checks."""

from __future__ import annotations


def clean(messages: list[dict]) -> list[dict]:
    """Return cleaned AIS messages."""
    raise NotImplementedError