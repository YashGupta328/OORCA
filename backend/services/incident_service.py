"""Incident service for Phase 1."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from backend.api.schemas.incident import IncidentCreate, IncidentRead


# Shared in-memory storage for Phase 1
_incidents: dict[str, IncidentRead] = {}
_simulation_runs: dict[str, dict] = {}
_simulation_statuses: dict[str, dict] = {}


class IncidentService:
    """In-memory incident storage for Phase 1. Replace with database in production."""

    def __init__(self) -> None:
        pass  # Using module-level shared storage

    async def create_incident(self, incident: IncidentCreate) -> IncidentRead:
        incident_id = f"ORCA-{datetime.utcnow().strftime('%Y%m%d')}-{uuid4().hex[:6].upper()}"
        now = datetime.utcnow()
        incident_read = IncidentRead(
            incident_id=incident_id,
            location=incident.location,
            spill=incident.spill,
            vessel=incident.vessel,
            created_at=now,
            status="created",
        )
        _incidents[incident_id] = incident_read
        return incident_read

    async def list_incidents(self, limit: int, offset: int) -> list[IncidentRead]:
        incidents = list(_incidents.values())
        incidents.sort(key=lambda x: x.created_at, reverse=True)
        return incidents[offset:offset + limit]

    async def get_incident(self, incident_id: str) -> IncidentRead | None:
        return _incidents.get(incident_id)

    async def run_simulation(self, incident_id: str) -> str | None:
        incident = _incidents.get(incident_id)
        if not incident:
            return None

        incident.status = "simulating"
        # Delegate to simulation service (will be called via API)
        # Return a simulation run ID
        sim_run_id = f"sim-{uuid4().hex[:12]}"
        _simulation_runs[sim_run_id] = {
            "incident_id": incident_id,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        return sim_run_id

    async def calculate_damage(self, incident_id: str) -> str | None:
        incident = _incidents.get(incident_id)
        if not incident:
            return None
        # Delegate to damage service
        assessment_id = f"damage-{uuid4().hex[:12]}"
        return assessment_id

    async def request_satellite_evidence(self, incident_id: str, provider: str) -> dict:
        return {
            "incident_id": incident_id,
            "provider": provider,
            "status": "requested",
            "message": "Satellite evidence request queued for {}. This feature will be implemented in Phase 2.".format(provider),
        }


# Shared access functions for other services
def get_incident(incident_id: str) -> IncidentRead | None:
    return _incidents.get(incident_id)

def get_simulation_run(sim_run_id: str) -> dict | None:
    return _simulation_runs.get(sim_run_id)

def set_simulation_run(sim_run_id: str, data: dict) -> None:
    _simulation_runs[sim_run_id] = data

def get_simulation_status(sim_run_id: str) -> dict | None:
    return _simulation_statuses.get(sim_run_id)

def set_simulation_status(sim_run_id: str, data: dict) -> None:
    _simulation_statuses[sim_run_id] = data