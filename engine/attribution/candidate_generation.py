"""Generate candidate vessels for a given detection."""

from __future__ import annotations


def generate_candidates(detection: dict, time_window_hours: int, buffer_km: float) -> list[dict]:
    """Return candidate vessels from the AIS archive."""
    raise NotImplementedError