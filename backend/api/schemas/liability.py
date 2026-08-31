"""Liability schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class LiabilityRequest(BaseModel):
    detection_id: int | None = None
    release_time: datetime | None = None
    release_lat: float | None = None
    release_lon: float | None = None
    volume_m3: float | None = None
    iterations: int = 1000


class ComponentEstimate(BaseModel):
    name: str
    p05: float
    p50: float
    p95: float


class LiabilityReport(BaseModel):
    id: int
    total: ComponentEstimate
    components: list[ComponentEstimate]
    sensitivity: list[dict]