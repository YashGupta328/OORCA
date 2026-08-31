"""Attribution service: ranks candidate vessels for a detection."""

from __future__ import annotations


class AttributionService:
    def attribute(self, detection: dict, candidates: list[dict], weights: dict) -> list[dict]:
        from engine.attribution.temporal_score import temporal_score
        from engine.attribution.spatial_score import spatial_score
        from engine.attribution.drift_score import drift_score
        from engine.attribution.vessel_score import vessel_score
        from engine.attribution.ranking import rank

        scored = []
        for c in candidates:
            scored.append({
                "candidate": c,
                "temporal": temporal_score(detection, c),
                "spatial": spatial_score(detection, c),
                "drift": drift_score(detection, c),
                "vessel": vessel_score(c),
            })
        return rank(scored, weights)