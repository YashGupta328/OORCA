"""Detection schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DetectionBase(BaseModel):
    observed_at: datetime
    geometry: dict = Field(..., description="GeoJSON geometry")
    area_km2: float
    confidence: float
    classifier_score: float | None = None
    scene_id: str | None = None


class DetectionCreate(DetectionBase):
    pass


class DetectionRead(DetectionBase):
    id: int

    class Config:
        from_attributes = True