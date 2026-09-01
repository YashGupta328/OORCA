"""Hazard zone calculation for damage assessment."""

from __future__ import annotations

from typing import Any


def calculate_hazard_zones(sensitivity_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Calculate hazard zones from sensitivity results.

    Groups resources into hazard zones based on spatial proximity and impact severity.

    Args:
        sensitivity_results: List of sensitivity results

    Returns:
        List of hazard zones
    """
    if not sensitivity_results:
        return []

    # Sort by sensitivity score descending
    sorted_results = sorted(sensitivity_results, key=lambda x: x["sensitivity_score"], reverse=True)

    hazard_zones = []

    for i, result in enumerate(sorted_results):
        score = result["sensitivity_score"]

        # Classify hazard level
        if score >= 2.0:
            hazard_level = "VERY_HIGH"
        elif score >= 1.0:
            hazard_level = "HIGH"
        elif score >= 0.5:
            hazard_level = "MEDIUM"
        else:
            hazard_level = "LOW"

        hazard_zones.append({
            "zone_id": f"HZ-{i+1:03d}",
            "resource_id": result["resource_id"],
            "resource_type": result["resource_type"],
            "resource_name": result["resource_name"],
            "hazard_level": hazard_level,
            "hazard_score": round(score, 3),
            "area_km2": result["area_km2"],
            "affected_percentage": result["affected_percentage"],
            "max_concentration": result["max_concentration"],
        })

    return hazard_zones


def aggregate_hazard_zones(hazard_zones: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate hazard zones into summary statistics."""
    if not hazard_zones:
        return {
            "total_zones": 0,
            "total_affected_area_km2": 0,
            "by_hazard_level": {},
            "by_resource_type": {},
        }

    by_level = {}
    by_type = {}
    total_area = 0

    for zone in hazard_zones:
        level = zone["hazard_level"]
        rtype = zone["resource_type"]
        area = zone["area_km2"]

        by_level[level] = by_level.get(level, 0) + 1
        by_type[rtype] = by_type.get(rtype, 0) + 1
        total_area += area

    return {
        "total_zones": len(hazard_zones),
        "total_affected_area_km2": round(total_area, 3),
        "by_hazard_level": by_level,
        "by_resource_type": by_type,
    }