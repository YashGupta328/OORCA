"""Simulation endpoints for Phase 1."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.schemas.simulation import SimulationRunCreate, SimulationRunRead, SimulationStatus
from backend.services.simulation_service import SimulationService

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


def get_simulation_service() -> SimulationService:
    return SimulationService()


@router.post("/run", response_model=SimulationRunRead, status_code=status.HTTP_201_CREATED)
async def run_simulation(
    request: SimulationRunCreate,
    service: SimulationService = Depends(get_simulation_service),
) -> SimulationRunRead:
    """Start a new simulation run."""
    return await service.run_simulation(request.incident_id, request.provider)


@router.get("/runs/{simulation_run_id}", response_model=SimulationRunRead)
async def get_simulation_run(
    simulation_run_id: str,
    service: SimulationService = Depends(get_simulation_service),
) -> SimulationRunRead:
    """Get simulation run details."""
    run = await service.get_simulation_run(simulation_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Simulation run not found")
    return run


@router.get("/runs/{simulation_run_id}/status", response_model=SimulationStatus)
async def get_simulation_status(
    simulation_run_id: str,
    service: SimulationService = Depends(get_simulation_service),
) -> SimulationStatus:
    """Get real-time simulation status."""
    return await service.get_status(simulation_run_id)


@router.get("/runs/{simulation_run_id}/frames/{frame_index}")
async def get_frame(
    simulation_run_id: str,
    frame_index: int,
    service: SimulationService = Depends(get_simulation_service),
) -> dict:
    """Get a specific simulation frame by index."""
    frame = await service.get_frame(simulation_run_id, frame_index)
    if not frame:
        raise HTTPException(status_code=404, detail="Frame not found")
    return frame


@router.get("/runs/{simulation_run_id}/wind-current/{frame_index}")
async def get_wind_current_frame(
    simulation_run_id: str,
    frame_index: int,
    service: SimulationService = Depends(get_simulation_service),
) -> dict:
    """Get wind/current data for a specific frame."""
    data = await service.get_wind_current_frame(simulation_run_id, frame_index)
    if not data:
        raise HTTPException(status_code=404, detail="Wind/current data not found")
    return data