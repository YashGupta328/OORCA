"""Joint Monte Carlo simulation over uncertain liability inputs."""

from __future__ import annotations


def simulate(samples: dict, iterations: int) -> dict:
    """Run Monte Carlo and return percentile summaries per component."""
    raise NotImplementedError