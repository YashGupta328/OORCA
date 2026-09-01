"""Metocean forcing data for spill simulation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import numpy as np


@dataclass
class MetoceanForcing:
    """Metocean forcing data for a time step."""
    time: datetime
    wind_u: np.ndarray  # Eastward wind component (m/s)
    wind_v: np.ndarray  # Northward wind component (m/s)
    current_u: np.ndarray  # Eastward current component (m/s)
    current_v: np.ndarray  # Northward current component (m/s)
    wave_height: np.ndarray | None = None  # Significant wave height (m)
    wave_period: np.ndarray | None = None  # Peak wave period (s)
    wave_direction: np.ndarray | None = None  # Wave direction (degrees)
    lon_grid: np.ndarray | None = None  # Longitude grid
    lat_grid: np.ndarray | None = None  # Latitude grid


def create_mock_metocean(
    latitude: float,
    longitude: float,
    start_time: datetime,
    duration_hours: int,
    time_step_hours: int = 1,
    grid_size: int = 50,
) -> list[MetoceanForcing]:
    """Create mock metocean forcing data for testing.

    In production, this would fetch from Copernicus/CMEMS/ERA5/GFS.
    """
    forcings = []
    for i in range(duration_hours + 1):
        t = start_time + timedelta(hours=i * time_step_hours)

        # Create a simple grid around the release point
        if forcings:
            # Reuse grids from first step
            lon_grid = forcings[0].lon_grid
            lat_grid = forcings[0].lat_grid
        else:
            lon_grid = np.linspace(longitude - 0.5, longitude + 0.5, grid_size)
            lat_grid = np.linspace(latitude - 0.5, latitude + 0.5, grid_size)
            lon_grid, lat_grid = np.meshgrid(lon_grid, lat_grid)

        # Mock wind: steady SW wind (225 deg) at 5-8 m/s
        wind_speed = 5.0 + 0.5 * np.sin(i * 0.2)
        wind_dir = 225  # degrees, from SW
        wind_u = -wind_speed * np.sin(np.radians(wind_dir)) * np.ones_like(lon_grid)
        wind_v = -wind_speed * np.cos(np.radians(wind_dir)) * np.ones_like(lon_grid)

        # Mock current: steady NE current (45 deg) at 0.3-0.5 m/s
        current_speed = 0.3 + 0.1 * np.sin(i * 0.1)
        current_dir = 45  # degrees, toward NE
        current_u = current_speed * np.sin(np.radians(current_dir)) * np.ones_like(lon_grid)
        current_v = current_speed * np.cos(np.radians(current_dir)) * np.ones_like(lon_grid)

        # Mock waves
        wave_height = 1.5 * np.ones_like(lon_grid)
        wave_period = 6.0 * np.ones_like(lon_grid)
        wave_direction = 225 * np.ones_like(lon_grid)

        forcings.append(MetoceanForcing(
            time=t,
            wind_u=wind_u,
            wind_v=wind_v,
            current_u=current_u,
            current_v=current_v,
            wave_height=wave_height,
            wave_period=wave_period,
            wave_direction=wave_direction,
            lon_grid=lon_grid,
            lat_grid=lat_grid,
        ))

    return forcings


def load_metocean_from_copernicus(
    latitude: float,
    longitude: float,
    start_time: datetime,
    duration_hours: int,
) -> list[MetoceanForcing]:
    """Load metocean data from Copernicus Marine Service.

    TODO: Implement actual CMEMS data fetching.
    """
    raise NotImplementedError("Copernicus metocean integration not yet implemented")


def load_metocean_from_era5(
    latitude: float,
    longitude: float,
    start_time: datetime,
    duration_hours: int,
) -> list[MetoceanForcing]:
    """Load metocean data from ERA5 reanalysis.

    TODO: Implement actual ERA5 data fetching.
    """
    raise NotImplementedError("ERA5 metocean integration not yet implemented")