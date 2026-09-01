"""Particle array for spill simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class ParticleArray:
    """Container for oil spill particles."""
    longitude: np.ndarray  # shape: (n_particles,)
    latitude: np.ndarray   # shape: (n_particles,)
    mass_kg: np.ndarray    # shape: (n_particles,)
    age_hours: np.ndarray  # shape: (n_particles,)
    status: np.ndarray     # shape: (n_particles,) - 0=active, 1=evaporated, 2=dispersed, 3=beached

    @classmethod
    def create_initial(cls, n_particles: int, longitude: float, latitude: float, total_mass_kg: float) -> "ParticleArray":
        """Create initial particle array at release point."""
        return cls(
            longitude=np.full(n_particles, longitude, dtype=np.float64),
            latitude=np.full(n_particles, latitude, dtype=np.float64),
            mass_kg=np.full(n_particles, total_mass_kg / n_particles, dtype=np.float64),
            age_hours=np.zeros(n_particles, dtype=np.float64),
            status=np.zeros(n_particles, dtype=np.int8),
        )

    def get_active_particles(self) -> np.ndarray:
        """Get indices of active particles."""
        return np.where(self.status == 0)[0]

    def get_active_count(self) -> int:
        """Get count of active particles."""
        return int(np.sum(self.status == 0))

    def to_geojson(self) -> dict[str, Any]:
        """Convert active particles to GeoJSON Point features."""
        active = self.get_active_particles()
        features = []
        for idx in active:
            features.append({
                "type": "Feature",
                "properties": {
                    "mass_kg": float(self.mass_kg[idx]),
                    "age_hours": float(self.age_hours[idx]),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(self.longitude[idx]), float(self.latitude[idx])],
                },
            })
        return {
            "type": "FeatureCollection",
            "features": features,
        }

    def get_bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box of active particles (min_lon, min_lat, max_lon, max_lat)."""
        active = self.get_active_particles()
        if len(active) == 0:
            return (0, 0, 0, 0)
        return (
            float(np.min(self.longitude[active])),
            float(np.min(self.latitude[active])),
            float(np.max(self.longitude[active])),
            float(np.max(self.latitude[active])),
        )