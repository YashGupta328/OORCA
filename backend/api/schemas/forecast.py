"""Forecast schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ForecastRequest(BaseModel):
    release_time: datetime
    release_lat: float
    release_lon: float
    volume_m3: float | None = None
    horizon_hours: int = 72
    particle_count: int = 10000


class ForecastResult(BaseModel):
    id: int
    request: ForecastRequest
    footprints: list[dict]
    probability_contours: list[dict]