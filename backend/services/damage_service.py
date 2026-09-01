"""Damage assessment service for Phase 1."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from backend.api.schemas.damage import (
    DangerAssessment,
    DamageAssessmentRead,
    ESIResource,
    ShorelineImpact,
    SpillSummary,
)
from backend.services.simulation_service import get_simulation_provider
from engine.damage.esi_loader import load_esi_features
from engine.damage.spatial_intersection import calculate_intersections
from engine.damage.exposure import calculate_exposure
from engine.damage.sensitivity import calculate_sensitivity
from engine.damage.hazard_zone import calculate_hazard_zones
from engine.damage.scoring import calculate_hazard_score


class DamageService:
    """Damage assessment service."""

    def __init__(self) -> None:
        self._assessments: dict[str, DamageAssessmentRead] = {}

    async def assess_damage(self, simulation_run_id: str) -> DamageAssessmentRead | None:
        """Calculate damage assessment for a simulation run."""
        # In production, fetch simulation frames from database
        # For now, generate mock assessment based on simulation run ID

        # Load ESI features
        esi_features = load_esi_features()

        # Get the final simulation frame (max time)
        provider = get_simulation_provider("mock")
        # We'll generate mock data here
        final_frame_geojson = self._get_final_frame(simulation_run_id)

        # Calculate intersections
        intersections = calculate_intersections(final_frame_geojson, esi_features)

        # Calculate exposure
        exposure = calculate_exposure(intersections)

        # Calculate sensitivity
        sensitivity = calculate_sensitivity(exposure, esi_features)

        # Calculate hazard zones
        hazard_zones = calculate_hazard_zones(sensitivity)

        # Calculate overall hazard score
        hazard_score = calculate_hazard_score(hazard_zones)

        # Build spill summary
        spill_summary = SpillSummary(
            total_spilled_tonnes=100.0,
            estimated_slick_area_km2=sum(f.get("properties", {}).get("area_km2", 0) for f in final_frame_geojson.get("features", [])),
            simulation_duration_hours=72,
            weathering_percent=25.0,
            evaporation_percent=15.0,
            dispersion_percent=10.0,
            remaining_surface_oil_tonnes=75.0,
        )

        # Build danger assessment
        danger_assessment = DangerAssessment(
            overall_risk=self._score_to_risk(hazard_score),
            environmental_risk=self._score_to_risk(hazard_score * 1.1),
            shoreline_risk=self._score_to_risk(hazard_score * 0.9),
            human_exposure_risk="MEDIUM",
            cleanup_difficulty=self._score_to_risk(hazard_score * 1.2),
            hazard_score=round(hazard_score, 1),
        )

        # Build ecological resources
        ecological_resources = []
        for resource in esi_features:
            affected = next((i for i in intersections if i["resource_id"] == resource["id"]), None)
            if affected:
                ecological_resources.append(ESIResource(
                    resource_id=resource["id"],
                    resource_type=resource["resource_type"],
                    resource_name=resource["resource_name"],
                    sensitivity_score=resource["sensitivity_score"],
                    geometry=resource["geometry"],
                    affected_area_km2=affected.get("area_km2"),
                    risk_level=self._score_to_risk(affected.get("hazard_score", 0)),
                    intersection_geometry=affected.get("intersection_geometry"),
                ))

        # Build shoreline impact
        shoreline_impact = self._calculate_shoreline_impact(final_frame_geojson)

        assessment = DamageAssessmentRead(
            assessment_id=f"damage-{uuid4().hex[:12]}",
            incident_id=simulation_run_id.split("-")[1] if "-" in simulation_run_id else "unknown",
            simulation_run_id=simulation_run_id,
            spill_summary=spill_summary,
            danger_assessment=danger_assessment,
            ecological_resources=ecological_resources,
            shoreline_impact=shoreline_impact,
            calculated_at=datetime.utcnow(),
        )

        self._assessments[assessment.assessment_id] = assessment
        return assessment

    async def get_assessment(self, assessment_id: str) -> DamageAssessmentRead | None:
        return self._assessments.get(assessment_id)

    def _score_to_risk(self, score: float) -> str:
        if score >= 75:
            return "VERY_HIGH"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        return "LOW"

    def _get_final_frame(self, simulation_run_id: str) -> dict:
        """Get the final frame from a simulation run. Mock implementation."""
        # In production, fetch from database
        # For now, return a mock final frame
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"concentration": "HIGH", "area_km2": 15.5},
                    "geometry": {"type": "Polygon", "coordinates": [[[72.8, 18.9], [72.9, 18.9], [72.9, 19.0], [72.8, 19.0], [72.8, 18.9]]]},
                },
            ],
        }

    def _calculate_shoreline_impact(self, frame_geojson: dict) -> list[ShorelineImpact]:
        """Calculate mock shoreline impact."""
        return [
            ShorelineImpact(
                location="Alibaug Coast",
                arrival_time_hours=(36, 48),
                impact_level="HIGH",
                distance_km=12.5,
                coordinates=[72.87, 18.64],
            ),
            ShorelineImpact(
                location="Revdanda Beach",
                arrival_time_hours=(48, 60),
                impact_level="MEDIUM",
                distance_km=18.2,
                coordinates=[72.92, 18.54],
            ),
            ShorelineImpact(
                location="Murud Beach",
                arrival_time_hours=(60, 72),
                impact_level="MEDIUM",
                distance_km=25.1,
                coordinates=[72.97, 18.42],
            ),
            ShorelineImpact(
                location="Kihim Beach",
                arrival_time_hours=(72, 84),
                impact_level="LOW",
                distance_km=30.8,
                coordinates=[72.83, 18.78],
            ),
        ]