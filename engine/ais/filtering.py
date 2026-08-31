"""Apply domain filters (port, loitering, course/speed sanity)."""

from __future__ import annotations


def apply_filters(trajectories: dict[int, list[dict]]) -> int:
    """Return count of trajectories retained after filtering."""
    raise NotImplementedError