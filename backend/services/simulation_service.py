"""Simulation provider abstraction for Phase 1."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from backend.api.schemas.simulation import SimulationRunRead, SimulationStatus


@dataclass
class SimulationParams:
    incident_id: str
    latitude: float
    longitude: float
    spill_amount: float
    spill_unit: str
    oil_type: str
    start_time: datetime
    duration_hours: int
    vessel_name: str | None = None
    vessel_type: str | None = None
    vessel_heading: float | None = None


@dataclass
class SimulationFrame:
    time_hours: int
    geojson: dict[str, Any]
    wind_data: dict[str, Any] | None = None
    current_data: dict[str, Any] | None = None


@dataclass
class SimulationResult:
    simulation_run_id: str
    frames: list[SimulationFrame]
    completed_at: datetime


class SpillSimulationProvider(ABC):
    """Abstract base class for spill simulation providers."""

    @abstractmethod
    async def run_simulation(self, params: SimulationParams) -> SimulationResult:
        """Run a spill simulation and return the result."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name."""
        pass


class MockSpillSimulationProvider(SpillSimulationProvider):
    """Mock simulation provider that returns pre-generated frames."""

    def __init__(self) -> None:
        self._frames_cache: dict[str, list[SimulationFrame]] = {}

    def get_provider_name(self) -> str:
        return "mock"

    async def run_simulation(self, params: SimulationParams) -> SimulationResult:
        """Generate mock spill frames based on parameters."""
        import json
        from pathlib import Path

        # Try to load pre-generated frames from disk
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        frames: list[SimulationFrame] = []

        # Generate frames for each time step (0, 12, 24, 36, 48, 60, 72 hours)
        time_steps = list(range(0, params.duration_hours + 1, 12))
        if time_steps[-1] != params.duration_hours:
            time_steps.append(params.duration_hours)

        for t in time_steps:
            frame_file = frames_dir / f"{t}h.geojson"
            if frame_file.exists():
                geojson = json.loads(frame_file.read_text())
            else:
                # Generate synthetic frame if file doesn't exist
                geojson = self._generate_synthetic_frame(params, t)

            frames.append(SimulationFrame(
                time_hours=t,
                geojson=geojson,
                wind_data=self._generate_wind_data(t),
                current_data=self._generate_current_data(t),
            ))

        return SimulationResult(
            simulation_run_id=f"sim-{params.incident_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            frames=frames,
            completed_at=datetime.utcnow(),
        )

    def _generate_synthetic_frame(self, params: SimulationParams, time_hours: int) -> dict:
        """Generate a synthetic spill frame for testing."""
        import math

        # Simple expanding circle model for demonstration
        # In reality, this would come from OpenDrift
        base_radius_km = 0.5
        spread_rate_kmh = 2.5
        radius_km = base_radius_km + spread_rate_kmh * time_hours

        # Convert radius to degrees (approximate)
        lat_deg = radius_km / 111.0
        lon_deg = radius_km / (111.0 * math.cos(math.radians(params.latitude)))

        # Create concentric polygons for different concentration levels
        features = []
        concentration_levels = [
            ("VERY_HIGH", 0.2, "#8B0000"),
            ("HIGH", 0.4, "#FF0000"),
            ("MEDIUM", 0.6, "#FFA500"),
            ("LOW", 1.0, "#FFFF00"),
        ]

        for level, radius_mult, color in concentration_levels:
            r_lat = lat_deg * radius_mult
            r_lon = lon_deg * radius_mult
            coords = []
            for i in range(32):
                angle = 2 * math.pi * i / 32
                lat = params.latitude + r_lat * math.sin(angle)
                lon = params.longitude + r_lon * math.cos(angle)
                coords.append([lon, lat])
            coords.append(coords[0])  # Close polygon

            features.append({
                "type": "Feature",
                "properties": {
                    "concentration": level,
                    "time_hours": time_hours,
                    "color": color,
                    "opacity": 0.7 if level != "LOW" else 0.5,
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords],
                },
            })

        # Add release point
        features.append({
            "type": "Feature",
            "properties": {
                "type": "release_point",
                "time_hours": time_hours,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [params.longitude, params.latitude],
            },
        })

        # Add vessel position if provided
        if params.vessel_name:
            # Simple drift for vessel
            vessel_lat = params.latitude + 0.01 * time_hours
            vessel_lon = params.longitude + 0.01 * time_hours
            features.append({
                "type": "Feature",
                "properties": {
                    "type": "vessel",
                    "name": params.vessel_name,
                    "time_hours": time_hours,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [vessel_lon, vessel_lat],
                },
            })

        return {
            "type": "FeatureCollection",
            "features": features,
        }

    def _generate_wind_data(self, time_hours: int) -> dict:
        """Generate mock wind data."""
        return {
            "time_hours": time_hours,
            "speed_ms": 5.0 + (time_hours * 0.1),
            "direction_deg": 225,  # SW wind
            "u_component": -3.5,
            "v_component": -3.5,
        }

    def _generate_current_data(self, time_hours: int) -> dict:
        """Generate mock current data."""
        return {
            "time_hours": time_hours,
            "speed_ms": 0.5,
            "direction_deg": 45,  # NE current
            "u_component": 0.35,
            "v_component": 0.35,
        }


class OpenDriftSimulationProvider(SpillSimulationProvider):
    """OpenDrift simulation provider (to be implemented)."""

    def get_provider_name(self) -> str:
        return "opendrift"

    async def run_simulation(self, params: SimulationParams) -> SimulationResult:
        # TODO: Implement OpenDrift integration
        # This would use engine/simulation/opendrift_runner.py
        raise NotImplementedError("OpenDrift provider not yet implemented")


def get_simulation_provider(provider_name: str = "mock") -> SpillSimulationProvider:
    """Factory function to get simulation provider."""
    providers = {
        "mock": MockSpillSimulationProvider,
        "opendrift": OpenDriftSimulationProvider,
    }
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown simulation provider: {provider_name}")
    return provider_class()


class SimulationService:
    """Service layer for simulation management."""

    def __init__(self) -> None:
        self._statuses: dict[str, SimulationStatus] = {}

    async def run_simulation(self, incident_id: str, provider_name: str = "mock") -> SimulationRunRead:
        """Start a new simulation run."""
        from backend.api.schemas.incident import IncidentRead
        from backend.services.incident_service import get_incident, set_simulation_run

        # Get incident details
        incident = await get_incident(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")

        # Create simulation run record
        simulation_run_id = f"sim-{incident_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        # Initialize status
        self._statuses[simulation_run_id] = SimulationStatus(
            simulation_run_id=simulation_run_id,
            status="initializing",
            progress=0,
            current_step="Initializing simulation...",
            frames_ready=0,
            total_frames=7,  # 0, 12, 24, 36, 48, 60, 72
        )

        # Store run info in shared storage
        run_data = {
            "simulation_run_id": simulation_run_id,
            "incident_id": incident_id,
            "provider": provider_name,
            "status": "running",
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "frames": None,
            "wind_current_data": None,
            "error": None,
        }
        set_simulation_run(simulation_run_id, run_data)

        # Run simulation asynchronously
        import asyncio
        asyncio.create_task(self._run_simulation_async(simulation_run_id, incident, provider_name))

        return SimulationRunRead(
            simulation_run_id=simulation_run_id,
            incident_id=incident_id,
            provider=provider_name,
            status="running",
            started_at=datetime.utcnow(),
            completed_at=None,
            frames=None,
            wind_current_data=None,
            error=None,
        )

    async def _run_simulation_async(self, simulation_run_id: str, incident: IncidentRead, provider_name: str):
        """Run simulation in background."""
        from backend.services.incident_service import set_simulation_run, get_simulation_run

        try:
            # Update status
            self._statuses[simulation_run_id].status = "loading_metocean"
            self._statuses[simulation_run_id].progress = 10
            self._statuses[simulation_run_id].current_step = "Loading metocean data..."

            await asyncio.sleep(0.5)  # Simulate loading

            self._statuses[simulation_run_id].status = "simulating"
            self._statuses[simulation_run_id].progress = 30
            self._statuses[simulation_run_id].current_step = "Running spill simulation..."

            # Run simulation via provider
            provider = get_simulation_provider(provider_name)
            params = SimulationParams(
                incident_id=incident.incident_id,
                latitude=incident.location.latitude,
                longitude=incident.location.longitude,
                spill_amount=incident.spill.amount,
                spill_unit=incident.spill.unit,
                oil_type=incident.spill.oil_type,
                start_time=incident.spill.start_time,
                duration_hours=incident.spill.duration_hours,
                vessel_name=incident.vessel.name if incident.vessel else None,
                vessel_type=incident.vessel.vessel_type if incident.vessel else None,
                vessel_heading=incident.vessel.heading_deg if incident.vessel else None,
            )

            result = await provider.run_simulation(params)

            # Update frames progressively
            total_frames = len(result.frames)
            for i, frame in enumerate(result.frames):
                await asyncio.sleep(0.1)  # Simulate processing time
                self._statuses[simulation_run_id].progress = 30 + int(60 * (i + 1) / total_frames)
                self._statuses[simulation_run_id].current_step = "Processing frame {}/{} ({}h)".format(i+1, total_frames, frame.time_hours)
                self._statuses[simulation_run_id].frames_ready = i + 1

            # Update status to calculating impact
            self._statuses[simulation_run_id].status = "calculating_impact"
            self._statuses[simulation_run_id].progress = 90
            self._statuses[simulation_run_id].current_step = "Calculating ecological impact..."

            await asyncio.sleep(0.2)

            # Store results in shared storage
            run = get_simulation_run(simulation_run_id)
            if run:
                run.update({
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "frames": result.frames,
                    "wind_current_data": [
                        {"time_hours": f.time_hours, "wind_data": f.wind_data, "current_data": f.current_data}
                        for f in result.frames
                    ],
                })
                set_simulation_run(simulation_run_id, run)

            # Final status
            self._statuses[simulation_run_id].status = "completed"
            self._statuses[simulation_run_id].progress = 100
            self._statuses[simulation_run_id].current_step = "Completed"
            self._statuses[simulation_run_id].frames_ready = total_frames

        except Exception as e:
            run = get_simulation_run(simulation_run_id)
            if run:
                run.update({
                    "status": "failed",
                    "completed_at": datetime.utcnow(),
                    "error": str(e),
                })
                set_simulation_run(simulation_run_id, run)
            self._statuses[simulation_run_id].status = "failed"
            self._statuses[simulation_run_id].error = str(e)

    async def get_simulation_run(self, simulation_run_id: str) -> SimulationRunRead | None:
        """Get simulation run details."""
        from backend.services.incident_service import get_simulation_run
        run = get_simulation_run(simulation_run_id)
        if not run:
            return None
        return SimulationRunRead(**run)

    async def get_status(self, simulation_run_id: str) -> SimulationStatus:
        """Get real-time simulation status."""
        from backend.services.incident_service import get_simulation_status, set_simulation_status
        
        status = get_simulation_status(simulation_run_id)
        if status:
            return SimulationStatus(**status)
        # Initialize default status if not exists
        default = SimulationStatus(
            simulation_run_id=simulation_run_id,
            status="idle",
            progress=0,
            current_step=None,
            frames_ready=0,
            total_frames=0,
        )
        set_simulation_status(simulation_run_id, default.dict())
        return default

    async def get_frame(self, simulation_run_id: str, frame_index: int) -> dict | None:
        """Get a specific simulation frame by index."""
        from backend.services.incident_service import get_simulation_run
        run = get_simulation_run(simulation_run_id)
        if not run or not run.get("frames"):
            return None
        frames = run["frames"]
        if 0 <= frame_index < len(frames):
            return {
                "time_hours": frames[frame_index].time_hours,
                "geojson": frames[frame_index].geojson,
                "wind_data": frames[frame_index].wind_data,
                "current_data": frames[frame_index].current_data,
            }
        return None

    async def get_wind_current_frame(self, simulation_run_id: str, frame_index: int) -> dict | None:
        """Get wind/current data for a specific frame."""
        from backend.services.incident_service import get_simulation_run
        run = get_simulation_run(simulation_run_id)
        if not run or not run.get("wind_current_data"):
            return None
        data = run["wind_current_data"]
        if 0 <= frame_index < len(data):
            return data[frame_index]
        return None