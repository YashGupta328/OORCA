"""Exposure calculation for ESI features intersected by oil spill."""

from __future__ import annotations

from typing import Any


CONCENTRATION_WEIGHTS = {
    "LOW": 0.25,
    "MEDIUM": 0.5,
    "HIGH": 0.75,
    "VERY_HIGH": 1.0,
}


def calculate_exposure(intersections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Calculate exposure score for each intersected ESI feature.

    Exposure = Affected Area × Concentration Weight × Duration Factor

    Args:
        intersections: List of intersection results from spatial_intersection

    Returns:
        List of exposure results with exposure scores
    """
    exposure_results = []

    for inter in intersections:
        area_km2 = inter.get("area_km2", 0)
        max_conc = inter.get("max_concentration", "LOW")
        concentrations = inter.get("concentrations_present", ["LOW"])

        # Weighted concentration based on all concentrations present
        conc_weight = sum(CONCENTRATION_WEIGHTS.get(c, 0.25) for c in concentrations) / len(concentrations)

        # Base exposure: area × concentration weight
        base_exposure = area_km2 * conc_weight

        # Duration factor (simplified - would come from simulation frames in production)
        duration_factor = 1.0  # Placeholder for time-integrated exposure

        exposure_score = base_exposure * duration_factor

        exposure_results.append({
            "resource_id": inter["resource_id"],
            "resource_type": inter["resource_type"],
            "resource_name": inter["resource_name"],
            "exposure_score": round(exposure_score, 3),
            "area_km2": inter["area_km2"],
            "affected_percentage": inter["affected_percentage"],
            "max_concentration": max_conc,
            "concentration_weight": round(conc_weight, 2),
        })

    return exposure_results