"""Convert segmentation probability map to polygon candidates."""

from __future__ import annotations


def detect_candidates(prob_map: "object") -> list[dict]:
    """Threshold and vectorise the probability map into candidate polygons."""
    raise NotImplementedError