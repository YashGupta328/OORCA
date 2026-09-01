"""Incident endpoints for Phase 1."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from backend.api.schemas.incident import IncidentCreate, IncidentRead
from backend.services.incident_service import IncidentService

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


def get_incident_service() -> IncidentService:
    return IncidentService()


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentRead:
    """Create a new oil spill incident."""
    return await service.create_incident(incident)


@router.get("", response_model=list[IncidentRead])
async def list_incidents(
    limit: int = 50,
    offset: int = 0,
    service: IncidentService = Depends(get_incident_service),
) -> list[IncidentRead]:
    """List all incidents."""
    return await service.list_incidents(limit, offset)


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentRead:
    """Get incident by ID."""
    incident = await service.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("/{incident_id}/simulate", response_model=dict)
async def run_simulation(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> dict:
    """Trigger a simulation for an incident."""
    result = await service.run_simulation(incident_id)
    if not result:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"simulation_run_id": result, "status": "started"}


@router.post("/{incident_id}/damage", response_model=dict)
async def calculate_damage(
    incident_id: str,
    service: IncidentService = Depends(get_incident_service),
) -> dict:
    """Calculate damage assessment for an incident's latest simulation."""
    result = await service.calculate_damage(incident_id)
    if not result:
        raise HTTPException(status_code=404, detail="No completed simulation found")
    return {"assessment_id": result, "status": "calculated"}


@router.post("/{incident_id}/satellite-evidence", response_model=dict)
async def request_satellite_evidence(
    incident_id: str,
    provider: str = "copernicus",
    service: IncidentService = Depends(get_incident_service),
) -> dict:
    """Request satellite evidence for an incident (placeholder for future integration)."""
    return await service.request_satellite_evidence(incident_id, provider)