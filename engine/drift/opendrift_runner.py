"""OpenDrift wrapper for running drift simulations."""

from __future__ import annotations


def run(opendrift_model, particles: "object", duration_hours: int, direction: str = "forward") -> "object":
    """Run an OpenDrift simulation. `direction` is 'forward' or 'backward'."""
    raise NotImplementedError