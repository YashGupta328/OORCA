"""Sensitivity calculation for ESI features."""

from __future__ import annotations

from typing import Any


RESOURCE_TYPE_MULTIPLIERS = {
    "mangrove": 1.3,
    "coral_reef": 1.5,
    "seagrass": 1.2,
    "fish_habitat": 1.0,
    "sea_turtle_habitat": 1.4,
    "dolphin_habitat": 1.3,
    "protected_area": 1.2,
    "saltmarsh": 1.1,
    "mudflat": 1.0,
    "sandy_beach": 0.8,
    "rocky_shore": 0.9,
}


def calculate_sensitivity(
    exposure_results: list[dict[str, Any]],
    esi_features: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Calculate sensitivity-weighted impact for each exposed resource.

    Sensitivity = Exposure × Resource Sensitivity Score × Resource Type Multiplier

    Args:
        exposure_results: List of exposure results
        esi_features: Original ESI features for metadata

    Returns:
        List of sensitivity results
    """
    # Create lookup for ESI features
    esi_lookup = {f["id"]: f for f in esi_features}

    sensitivity_results = []

    for exp in exposure_results:
        resource_id = exp["resource_id"]
        esi = esi_lookup.get(resource_id)

        if not esi:
            continue

        base_sensitivity = esi.get("sensitivity_score", 50)  # 0-100 scale
        resource_type = esi.get("resource_type", "unknown")
        type_multiplier = RESOURCE_TYPE_MULTIPLIERS.get(resource_type, 1.0)

        # Normalized sensitivity (0-1)
        norm_sensitivity = base_sensitivity / 100.0

        # Combined sensitivity score
        sensitivity_score = exp["exposure_score"] * norm_sensitivity * type_multiplier

        sensitivity_results.append({
            "resource_id": resource_id,
            "resource_type": resource_type,
            "resource_name": exp["resource_name"],
            "sensitivity_score": round(sensitivity_score, 3),
            "base_sensitivity": base_sensitivity,
            "type_multiplier": type_multiplier,
            "exposure_score": exp["exposure_score"],
            "area_km2": exp["area_km2"],
            "affected_percentage": exp["affected_percentage"],
            "max_concentration": exp["max_concentration"],
        })

    return sensitivity_results