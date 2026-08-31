"""AIS ingestion and processing service."""

from __future__ import annotations

from backend.core.settings import get_settings


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

        s = get_settings().attribution if hasattr(get_settings(), "attribution") else None
        hours = s.time_window_hours if s else time_window_hours  # type: ignore[attr-defined]
        return generate_candidates(detection, hours, buffer_km)