"""AIS ingestion and processing service."""

from __future__ import annotations


class AisService:
    """Coordinates ingestion, cleaning, interpolation and filtering of AIS messages."""

    def ingest(self, source: str) -> int:
        from engine.ais.ingestion import ingest
        from engine.ais.cleaning import clean
        from engine.ais.interpolation import interpolate
        from engine.ais.trajectory import build_trajectories
        from engine.ais.filtering import apply_filters

        raw = ingest(source)
        cleaned = clean(raw)
        interpolated = interpolate(cleaned)
        trajectories = build_trajectories(interpolated)
        return apply_filters(trajectories)

    def find_candidates(self, detection: dict, time_window_hours: int, buffer_km: float) -> list[dict]:
        from engine.attribution.candidate_generation import generate_candidates
        return generate_candidates(detection, time_window_hours, buffer_km)