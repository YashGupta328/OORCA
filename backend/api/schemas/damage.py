"""Damage assessment schemas for Phase 1."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SpillSummary(BaseModel):
    total_spilled_tonnes: float = Field(..., ge=0)
    estimated_slick_area_km2: float = Field(..., ge=0)
    simulation_duration_hours: int = Field(..., ge=0)
    weathering_percent: float = Field(..., ge=0, le=100)
    evaporation_percent: float = Field(..., ge=0, le=100)
    dispersion_percent: float = Field(..., ge=0, le=100)
    remaining_surface_oil_tonnes: float = Field(..., ge=0)


class DangerAssessment(BaseModel):
    overall_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    environmental_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    shoreline_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    human_exposure_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    cleanup_difficulty: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    hazard_score: float = Field(..., ge=0, le=100)


class ESIResource(BaseModel):
    resource_id: str
    resource_type: str
    resource_name: str
    sensitivity_score: float
    geometry: dict
    affected_area_km2: float | None = None
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"] | None = None
    intersection_geometry: dict | None = None


class ShorelineImpact(BaseModel):
    location: str
    arrival_time_hours: tuple[int, int] | None = None
    impact_level: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    distance_km: float | None = None
    coordinates: list[float] | None = None


class DamageAssessmentCreate(BaseModel):
    simulation_run_id: str


class DamageAssessmentRead(BaseModel):
    assessment_id: str
    incident_id: str
    simulation_run_id: str
    spill_summary: SpillSummary
    danger_assessment: DangerAssessment
    ecological_resources: list[ESIResource]
    shoreline_impact: list[ShorelineImpact]
    calculated_at: datetime

    class Config:
        from_attributes = True