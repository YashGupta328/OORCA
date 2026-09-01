"""Simulation output generation for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import numpy as np


@dataclass
class SpillFrame:
    """Single time step output frame."""
    time_hours: int
    time: datetime
    geojson: dict[str, Any]
    mass_balance: dict[str, float]
    wind_data: dict[str, Any] | None = None
    current_data: dict[str, Any] | None = None


@dataclass
class SimulationOutput:
    """Complete simulation output."""
    simulation_run_id: str
    incident_id: str
    frames: list[SpillFrame] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_frame(self, frame: SpillFrame) -> None:
        self.frames.append(frame)

    def get_frame(self, index: int) -> SpillFrame | None:
        if 0 <= index < len(self.frames):
            return self.frames[index]
        return None

    def get_final_frame(self) -> SpillFrame | None:
        return self.frames[-1] if self.frames else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_run_id": self.simulation_run_id,
            "incident_id": self.incident_id,
            "frames": [
                {
                    "time_hours": f.time_hours,
                    "time": f.time.isoformat(),
                    "geojson": f.geojson,
                    "mass_balance": f.mass_balance,
                    "wind_data": f.wind_data,
                    "current_data": f.current_data,
                }
                for f in self.frames
            ],
            "metadata": self.metadata,
        }


def create_concentration_grid(
    particles: Any,
    bounds: tuple[float, float, float, float] | None = None,
    grid_size: int = 100,
    concentration_levels: list[tuple[str, float]] = None,
) -> dict[str, Any]:
    """Create concentration grid from particle positions.

    Args:
        particles: ParticleArray instance
        bounds: (min_lon, min_lat, max_lon, max_lat) or None for particle bounds
        grid_size: Grid resolution
        concentration_levels: List of (level_name, threshold_mass_per_km2)

    Returns:
        GeoJSON FeatureCollection with concentration polygons
    """
    if concentration_levels is None:
        concentration_levels = [
            ("LOW", 100),
            ("MEDIUM", 500),
            ("HIGH", 2000),
            ("VERY_HIGH", 5000),
        ]

    active = particles.get_active_particles()
    if len(active) == 0:
        return {"type": "FeatureCollection", "features": []}

    if bounds is None:
        bounds = particles.get_bounds()

    min_lon, min_lat, max_lon, max_lat = bounds

    # Handle case where all particles are at same location
    if min_lon == max_lon or min_lat == max_lat:
        # Expand bounds by a small amount (~1km)
        min_lon -= 0.005
        max_lon += 0.005
        min_lat -= 0.005
        max_lat += 0.005

    # Create grid
    lon_edges = np.linspace(min_lon, max_lon, grid_size + 1)
    lat_edges = np.linspace(min_lat, max_lat, grid_size + 1)

    # Bin particles
    mass_grid = np.zeros((grid_size, grid_size), dtype=np.float64)
    lon_indices = np.digitize(particles.longitude[active], lon_edges) - 1
    lat_indices = np.digitize(particles.latitude[active], lat_edges) - 1

    # Clip to grid
    valid = (lon_indices >= 0) & (lon_indices < grid_size) & (lat_indices >= 0) & (lat_indices < grid_size)
    lon_indices = lon_indices[valid]
    lat_indices = lat_indices[valid]
    masses = particles.mass_kg[active][valid]

    np.add.at(mass_grid, (lat_indices, lon_indices), masses)

    # Convert to mass per km2 (approximate cell area)
    cell_area_km2 = ((max_lat - min_lat) / grid_size * 111) * ((max_lon - min_lon) / grid_size * 111 * np.cos(np.radians((min_lat + max_lat) / 2)))
    conc_grid = mass_grid / cell_area_km2 if cell_area_km2 > 0 else mass_grid

    # Generate contours for each concentration level
    features = []
    for level_name, threshold in concentration_levels:
        # Simple threshold-based polygons (in production, use marching squares)
        mask = conc_grid >= threshold
        if np.any(mask):
            # Create polygons for each contiguous region
            from scipy import ndimage
            labeled, num_features = ndimage.label(mask)
            for i in range(1, num_features + 1):
                region = labeled == i
                if np.sum(region) < 4:  # Skip tiny regions
                    continue
                # Get boundary coordinates
                coords = _get_polygon_coords(region, lon_edges, lat_edges)
                if coords:
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "concentration": level_name,
                            "threshold_kg_km2": threshold,
                        },
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords],
                        },
                    })

    # Add release point
    features.append({
        "type": "Feature",
        "properties": {"type": "release_point"},
        "geometry": {
            "type": "Point",
            "coordinates": [float(particles.longitude[0]), float(particles.latitude[0])],
        },
    })

    return {"type": "FeatureCollection", "features": features}


def _get_polygon_coords(
    mask: np.ndarray,
    lon_edges: np.ndarray,
    lat_edges: np.ndarray,
) -> list[list[float]] | None:
    """Extract polygon coordinates from binary mask using marching squares."""
    # Simplified: just return bounding box of mask
    # In production, use skimage.measure.find_contours or similar
    rows, cols = np.where(mask)
    if len(rows) == 0:
        return None

    min_row, max_row = rows.min(), rows.max()
    min_col, max_col = cols.min(), cols.max()

    # Create rectangle
    coords = [
        [float(lon_edges[min_col]), float(lat_edges[min_row])],
        [float(lon_edges[max_col + 1]), float(lat_edges[min_row])],
        [float(lon_edges[max_col + 1]), float(lat_edges[max_row + 1])],
        [float(lon_edges[min_col]), float(lat_edges[max_row + 1])],
        [float(lon_edges[min_col]), float(lat_edges[min_row])],
    ]
    return coords


def generate_wind_current_geojson(metocean: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    """Generate wind and current vector GeoJSON from metocean data."""
    # Simplified: return vector field at grid centers
    if metocean.lon_grid is None or metocean.lat_grid is None:
        return {}, {}

    wind_features = []
    current_features = []

    # Sample every 5th grid point
    step = 5
    for i in range(0, metocean.lon_grid.shape[0], step):
        for j in range(0, metocean.lon_grid.shape[1], step):
            lon = float(metocean.lon_grid[i, j])
            lat = float(metocean.lat_grid[i, j])
            wu = float(metocean.wind_u[i, j])
            wv = float(metocean.wind_v[i, j])
            cu = float(metocean.current_u[i, j])
            cv = float(metocean.current_v[i, j])

            wind_speed = np.hypot(wu, wv)
            wind_dir = np.degrees(np.arctan2(wu, wv))
            current_speed = np.hypot(cu, cv)
            current_dir = np.degrees(np.arctan2(cu, cv))

            wind_features.append({
                "type": "Feature",
                "properties": {
                    "speed_ms": round(wind_speed, 1),
                    "direction_deg": round(wind_dir, 0),
                },
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
            })

            current_features.append({
                "type": "Feature",
                "properties": {
                    "speed_ms": round(current_speed, 2),
                    "direction_deg": round(current_dir, 0),
                },
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
            })

    return (
        {"type": "FeatureCollection", "features": wind_features},
        {"type": "FeatureCollection", "features": current_features},
    )