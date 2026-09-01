"""Incident schemas for Phase 1."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class SpillDetails(BaseModel):
    amount: float = Field(..., gt=0)
    unit: Literal["tonnes", "barrels", "liters", "gallons"] = "tonnes"
    oil_type: Literal["crude_oil", "diesel", "heavy_fuel_oil", "gasoline", "jet_fuel"] = "crude_oil"
    start_time: datetime
    duration_hours: int = Field(..., gt=0, le=168)


class VesselDetails(BaseModel):
    name: str | None = None
    vessel_type: Literal["oil_tanker", "cargo", "fishing", "passenger", "other"] | None = None
    imo: str | None = None
    length_m: float | None = Field(None, gt=0)
    breadth_m: float | None = Field(None, gt=0)
    draft_m: float | None = Field(None, gt=0)
    heading_deg: float | None = Field(None, ge=0, lt=360)


class IncidentCreate(BaseModel):
    location: Location
    spill: SpillDetails
    vessel: VesselDetails | None = None


class IncidentRead(IncidentCreate):
    incident_id: str
    created_at: datetime
    status: Literal["created", "simulating", "completed", "failed"]

    class Config:
        from_attributes = True


class SimulationRequest(BaseModel):
    incident_id: str


class SimulationStatus(BaseModel):
    incident_id: str
    status: Literal["idle", "initializing", "loading_metocean", "simulating", "calculating_impact", "completed", "failed"]
    progress: int = 0
    current_step: str | None = None
    error: str | None = None


class SpillFrame(BaseModel):
    time_hours: int
    geojson: dict


class SimulationResult(BaseModel):
    incident_id: str
    simulation_run_id: str
    frames: list[SpillFrame]
    wind_data: list[dict] | None = None
    current_data: list[dict] | None = None
    completed_at: datetime


class DamageRequest(BaseModel):
    simulation_run_id: str


class ESIResource(BaseModel):
    resource_type: str
    resource_name: str
    sensitivity_score: float
    geometry: dict
    affected_area_km2: float | None = None
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"] | None = None


class ShorelineImpact(BaseModel):
    location: str
    arrival_time_hours: tuple[int, int] | None = None
    impact_level: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    distance_km: float | None = None


class SpillSummary(BaseModel):
    total_spilled_tonnes: float
    estimated_slick_area_km2: float
    simulation_duration_hours: int
    weathering_percent: float
    evaporation_percent: float
    dispersion_percent: float
    remaining_surface_oil_tonnes: float


class DangerAssessment(BaseModel):
    overall_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    environmental_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    shoreline_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    human_exposure_risk: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    cleanup_difficulty: Literal["LOW", "MEDIUM", "HIGH", "VERY_HIGH"]
    hazard_score: float = Field(..., ge=0, le=100)


class DamageResult(BaseModel):
    incident_id: str
    simulation_run_id: str
    spill_summary: SpillSummary
    danger_assessment: DangerAssessment
    ecological_resources: list[ESIResource]
    shoreline_impact: list[ShorelineImpact]
    calculated_at: datetime


class SatelliteEvidenceRequest(BaseModel):
    incident_id: str
    provider: Literal["copernicus", "bhoonidhi"] = "copernicus"