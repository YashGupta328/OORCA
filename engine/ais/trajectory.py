"""Build per-vessel trajectories."""

from __future__ import annotations


def build_trajectories(messages: list[dict]) -> dict[int, list[dict]]:
    """Return mapping mmsi -> ordered list of positions."""
    raise NotImplementedError