"""Ecology schemas."""

from __future__ import annotations

from pydantic import BaseModel


class ESIPolygon(BaseModel):
    esi_id: str
    ranking: int
    habitat: str | None = None
    geometry: dict


class ExposureReport(BaseModel):
    total_exposed_km2: float
    by_esi_class: dict[str, float]
    top_habitats: list[dict]
    hazard_zones: list[dict]