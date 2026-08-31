"""Postprocess classified candidates."""

from __future__ import annotations


def postprocess(candidates: list[dict]) -> list[dict]:
    """Filter by minimum area, validate geometry, attach confidence."""
    raise NotImplementedError