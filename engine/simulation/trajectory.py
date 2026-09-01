"""Trajectory calculator for particle advection."""

from __future__ import annotations

from typing import Any

import numpy as np


def advect_particles(
    particles: Any,
    metocean: Any,
    dt_seconds: float,
    wind_drift_factor: float = 0.03,
) -> None:
    """Advect particles using wind and current.

    Implements simple Euler advection:
    dx/dt = current + wind_drift_factor * wind

    Args:
        particles: ParticleArray instance
        metocean: MetoceanForcing instance for current time step
        dt_seconds: Time step in seconds
        wind_drift_factor: Fraction of wind velocity applied to particles (typical 0.03)
    """
    active = particles.get_active_particles()
    if len(active) == 0:
        return

    # For simplicity, use uniform forcing (in reality, interpolate from grid)
    wind_u = float(np.mean(metocean.wind_u))
    wind_v = float(np.mean(metocean.wind_v))
    current_u = float(np.mean(metocean.current_u))
    current_v = float(np.mean(metocean.current_v))

    # Total velocity
    u = current_u + wind_drift_factor * wind_u
    v = current_v + wind_drift_factor * wind_v

    # Convert to degrees per second (approximate)
    # 1 degree latitude ~= 111 km
    # 1 degree longitude ~= 111 km * cos(lat)
    lat_rad = np.radians(particles.latitude[active])
    dlat = (v * dt_seconds) / 111000.0
    dlon = (u * dt_seconds) / (111000.0 * np.cos(lat_rad))

    particles.latitude[active] += dlat
    particles.longitude[active] += dlon


def add_stochastic_dispersion(
    particles: Any,
    dt_seconds: float,
    horizontal_diffusivity: float = 10.0,  # m2/s
) -> None:
    """Add random walk dispersion to particles.

    Args:
        particles: ParticleArray instance
        dt_seconds: Time step in seconds
        horizontal_diffusivity: Horizontal eddy diffusivity (m2/s)
    """
    active = particles.get_active_particles()
    if len(active) == 0:
        return

    n = len(active)
    # Random displacement from normal distribution
    # sigma = sqrt(2 * K * dt)
    sigma = np.sqrt(2.0 * horizontal_diffusivity * dt_seconds)

    # Convert to degrees
    lat_rad = np.radians(particles.latitude[active])
    dlat = np.random.normal(0, sigma / 111000.0, n)
    dlon = np.random.normal(0, sigma / (111000.0 * np.cos(lat_rad)), n)

    particles.latitude[active] += dlat
    particles.longitude[active] += dlon


def check_beaching(
    particles: Any,
    coastline_polygons: list[Any] | None = None,
) -> np.ndarray:
    """Check which particles have beached.

    Args:
        particles: ParticleArray instance
        coastline_polygons: List of shapely polygons representing coastline

    Returns:
        Boolean array indicating beached particles
    """
    if coastline_polygons is None:
        return np.zeros(len(particles.longitude), dtype=bool)

    from shapely.geometry import Point
    from shapely.prepared import prep

    # Prepare polygons for fast intersection testing
    prepared = [prep(poly) for poly in coastline_polygons]

    beached = np.zeros(len(particles.longitude), dtype=bool)
    active = particles.get_active_particles()

    for idx in active:
        point = Point(particles.longitude[idx], particles.latitude[idx])
        for p in prepared:
            if p.contains(point):
                beached[idx] = True
                break

    return beached