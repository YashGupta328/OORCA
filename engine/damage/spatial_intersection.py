"""Spatial intersection calculations for spill footprint and ESI features."""

from __future__ import annotations

from typing import Any

from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import transform
import pyproj


def calculate_intersections(
    spill_geojson: dict[str, Any],
    esi_features: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Calculate intersections between spill footprint and ESI features.

    Args:
        spill_geojson: GeoJSON FeatureCollection of spill concentration polygons
        esi_features: List of ESI feature dictionaries with geometry

    Returns:
        List of intersection results with area calculations
    """
    intersections = []

    # Extract spill polygons by concentration level
    spill_polygons = []
    for feature in spill_geojson.get("features", []):
        geom = feature.get("geometry")
        props = feature.get("properties", {})
        if geom and geom["type"] in ("Polygon", "MultiPolygon"):
            concentration = props.get("concentration", "UNKNOWN")
            try:
                poly = shape(geom)
                if poly.is_valid and not poly.is_empty:
                    spill_polygons.append((poly, concentration))
            except Exception:
                continue

    if not spill_polygons:
        return intersections

    # Create union of all spill polygons for intersection testing
    from shapely.ops import unary_union
    spill_union = unary_union([p[0] for p in spill_polygons])

    # Project to a local CRS for accurate area calculations (UTM Zone 43N for Mumbai)
    project = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True).transform
    spill_union_proj = transform(project, spill_union)

    for esi in esi_features:
        esi_geom = esi.get("geometry")
        if not esi_geom or esi_geom["type"] not in ("Polygon", "MultiPolygon"):
            continue

        try:
            esi_poly = shape(esi_geom)
            if not esi_poly.is_valid or esi_poly.is_empty:
                continue

            # Check intersection
            if not spill_union.intersects(esi_poly):
                continue

            intersection = spill_union.intersection(esi_poly)
            if intersection.is_empty:
                continue

            # Calculate area in km2 using projected coordinates
            esi_poly_proj = transform(project, esi_poly)
            intersection_proj = transform(project, intersection)

            intersection_area_km2 = intersection_proj.area / 1_000_000
            esi_area_km2 = esi_poly_proj.area / 1_000_000

            if intersection_area_km2 < 0.001:  # Skip negligible intersections
                continue

            # Calculate percentage of ESI feature affected
            affected_percentage = (intersection_area_km2 / esi_area_km2 * 100) if esi_area_km2 > 0 else 0

            # Determine concentration level in intersection
            concentrations = set()
            for poly, conc in spill_polygons:
                if poly.intersects(esi_poly):
                    concentrations.add(conc)

            intersections.append({
                "resource_id": esi["id"],
                "resource_type": esi["resource_type"],
                "resource_name": esi["resource_name"],
                "sensitivity_score": esi["sensitivity_score"],
                "intersection_geometry": intersection.__geo_interface__,
                "area_km2": round(intersection_area_km2, 3),
                "esi_area_km2": round(esi_area_km2, 3),
                "affected_percentage": round(affected_percentage, 1),
                "concentrations_present": list(concentrations),
                "max_concentration": max(concentrations, key=_concentration_rank) if concentrations else "LOW",
            })

        except Exception:
            continue

    return intersections


def _concentration_rank(conc: str) -> int:
    """Rank concentration levels for sorting."""
    ranks = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY_HIGH": 4}
    return ranks.get(conc, 0)