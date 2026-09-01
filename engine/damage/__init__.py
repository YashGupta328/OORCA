"""Damage engine package for Phase 1."""

from engine.damage.esi_loader import load_esi_features, ESIResource
from engine.damage.spatial_intersection import calculate_intersections
from engine.damage.exposure import calculate_exposure
from engine.damage.sensitivity import calculate_sensitivity
from engine.damage.hazard_zone import calculate_hazard_zones
from engine.damage.scoring import calculate_hazard_score

__all__ = [
    "load_esi_features",
    "ESIResource",
    "calculate_intersections",
    "calculate_exposure",
    "calculate_sensitivity",
    "calculate_hazard_zones",
    "calculate_hazard_score",
]