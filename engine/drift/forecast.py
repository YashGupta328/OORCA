"""Forward-in-time drift projection."""

from __future__ import annotations


def run_forecast(release: dict, hours: int) -> dict:
    """Run a forward forecast and return footprints and probability contours."""
    from engine.drift.opendrift_runner import run
    from engine.drift.particles import seed_particles

    particles = seed_particles(release)
    traj = run(None, particles, duration_hours=hours, direction="forward")
    footprints = _build_footprints(traj)
    contours = _build_contours(traj)
    return {"footprints": footprints, "contours": contours, "particles": traj}


def _build_footprints(traj: "object") -> list[dict]:
    raise NotImplementedError


def _build_contours(traj: "object") -> list[dict]:
    raise NotImplementedError