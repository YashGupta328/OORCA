"""Backward-in-time drift reconstruction."""

from __future__ import annotations


def run_hindcast(detection: dict, hours: int) -> dict:
    """Run a hindcast and return origin probability and release estimate."""
    from engine.drift.opendrift_runner import run
    from engine.drift.particles import seed_particles
    from engine.drift.weathering import apply_weathering

    particles = seed_particles(detection)
    traj = run(None, particles, duration_hours=hours, direction="backward")
    origin = _summarise_origin(traj)
    volume = apply_weathering(detection, traj)
    return {"origin": origin, "estimated_volume_m3": volume, "particles": traj}


def _summarise_origin(traj: "object") -> dict:
    raise NotImplementedError