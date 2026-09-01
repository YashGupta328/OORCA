"""Hazard scoring for Phase 1 damage assessment.

This implements the Baseline Ecological Hazard Score (0-100).
IMPORTANT: This is NOT a legally valid environmental damage or financial liability calculation.
"""

from __future__ import annotations

from typing import Any


def calculate_hazard_score(hazard_zones: list[dict[str, Any]]) -> float:
    """Calculate the overall Baseline Ecological Hazard Score (0-100).

    Score = Σ(Hazard Zone Score × Weight) normalized to 0-100

    Args:
        hazard_zones: List of hazard zones from hazard_zone calculation

    Returns:
        Hazard score 0-100
    """
    if not hazard_zones:
        return 0.0

    # Weights by hazard level
    level_weights = {
        "VERY_HIGH": 1.0,
        "HIGH": 0.7,
        "MEDIUM": 0.4,
        "LOW": 0.15,
    }

    # Resource type importance weights
    type_weights = {
        "coral_reef": 1.5,
        "mangrove": 1.3,
        "sea_turtle_habitat": 1.4,
        "dolphin_habitat": 1.3,
        "seagrass": 1.2,
        "protected_area": 1.2,
        "fish_habitat": 1.0,
        "saltmarsh": 1.1,
        "mudflat": 0.9,
        "sandy_beach": 0.7,
        "rocky_shore": 0.8,
    }

    total_weighted_score = 0.0
    max_possible_score = 0.0

    for zone in hazard_zones:
        hazard_score = zone.get("hazard_score", 0)
        level = zone.get("hazard_level", "LOW")
        rtype = zone.get("resource_type", "unknown")

        level_weight = level_weights.get(level, 0.15)
        type_weight = type_weights.get(rtype, 1.0)
        area_km2 = zone.get("area_km2", 0)

        # Zone contribution: hazard_score × level_weight × type_weight × area_factor
        area_factor = min(area_km2 / 10.0, 2.0)  # Cap area influence
        zone_contribution = hazard_score * level_weight * type_weight * (1 + area_factor)

        total_weighted_score += zone_contribution
        max_possible_score += 10.0 * level_weight * type_weight * 3.0  # Theoretical max per zone

    if max_possible_score == 0:
        return 0.0

    # Normalize to 0-100
    normalized_score = min((total_weighted_score / max_possible_score) * 100, 100.0)

    return round(normalized_score, 1)


def calculate_component_scores(hazard_zones: list[dict[str, Any]]) -> dict[str, float]:
    """Calculate component scores for the danger assessment.

    Returns:
        Dictionary with environmental_risk, shoreline_risk, human_exposure_risk, cleanup_difficulty
    """
    if not hazard_zones:
        return {
            "environmental_risk": 0.0,
            "shoreline_risk": 0.0,
            "human_exposure_risk": 0.0,
            "cleanup_difficulty": 0.0,
        }

    # Environmental risk: all ecological resources
    env_zones = [z for z in hazard_zones if z["resource_type"] in (
        "mangrove", "coral_reef", "seagrass", "fish_habitat",
        "sea_turtle_habitat", "dolphin_habitat", "saltmarsh",
    )]
    env_score = _score_zones(env_zones)

    # Shoreline risk: coastal habitats
    shore_zones = [z for z in hazard_zones if z["resource_type"] in (
        "mangrove", "saltmarsh", "sandy_beach", "rocky_shore", "mudflat",
    )]
    shore_score = _score_zones(shore_zones)

    # Human exposure: proximity to population, fisheries
    human_zones = [z for z in hazard_zones if z["resource_type"] in (
        "fish_habitat", "protected_area",
    )]
    human_score = _score_zones(human_zones) * 0.8  # Slightly lower weight

    # Cleanup difficulty: based on oil concentration and habitat complexity
    cleanup_zones = [z for z in hazard_zones if z["max_concentration"] in ("HIGH", "VERY_HIGH")]
    cleanup_score = _score_zones(cleanup_zones) * 1.2  # Higher weight for difficult cleanup

    return {
        "environmental_risk": round(min(env_score, 100), 1),
        "shoreline_risk": round(min(shore_score, 100), 1),
        "human_exposure_risk": round(min(human_score, 100), 1),
        "cleanup_difficulty": round(min(cleanup_score, 100), 1),
    }


def _score_zones(zones: list[dict[str, Any]]) -> float:
    """Helper to score a subset of zones."""
    if not zones:
        return 0.0
    scores = [z.get("hazard_score", 0) for z in zones]
    return sum(scores) / len(scores) * 10  # Scale to 0-100 range


def score_to_risk_level(score: float) -> str:
    """Convert numeric score to risk level."""
    if score >= 75:
        return "VERY_HIGH"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    return "LOW"