"""ESI / ecological service."""

from __future__ import annotations


class EsiService:
    def exposure_for_detection(self, detection: dict) -> dict:
        from engine.ecology.esi_loader import load
        from engine.ecology.spatial_intersection import intersect
        from engine.ecology.exposure import compute_exposure
        from engine.ecology.sensitivity import apply_sensitivity
        from engine.ecology.hazard_zone import rank_hazards

        esi = load()
        overlap = intersect(detection, esi)
        exposure = compute_exposure(overlap)
        weighted = apply_sensitivity(exposure, esi)
        return rank_hazards(weighted)