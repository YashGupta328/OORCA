"""Simulation schemas for Phase 1."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class SpillFrame(BaseModel):
    time_hours: int
    geojson: dict


class WindCurrentFrame(BaseModel):
    time_hours: int
    wind_u: list[list[float]] | None = None
    wind_v: list[list[float]] | None = None
    current_u: list[list[float]] | None = None
    current_v: list[list[float]] | None = None
    bounds: list[float] | None = None


class SimulationRunCreate(BaseModel):
    incident_id: str
    provider: Literal["mock", "opendrift"] = "mock"


class SimulationRunRead(BaseModel):
    simulation_run_id: str
    incident_id: str
    provider: str
    status: Literal["pending", "running", "completed", "failed"]
    started_at: datetime
    completed_at: datetime | None = None
    frames: list[SpillFrame] | None = None
    wind_current_data: list[WindCurrentFrame] | None = None
    error: str | None = None

    class Config:
        from_attributes = True


class SimulationStatus(BaseModel):
    simulation_run_id: str
    status: Literal["idle", "initializing", "loading_metocean", "simulating", "calculating_impact", "completed", "failed"]
    progress: int
    current_step: str | None = None
    frames_ready: int = 0
    total_frames: int = 0