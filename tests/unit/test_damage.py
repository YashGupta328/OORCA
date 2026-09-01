"""Unit tests for damage assessment API schemas and service."""

from __future__ import annotations

import pytest
from datetime import datetime

from backend.api.schemas.damage import (
    DamageAssessmentRead,
    DangerAssessment,
    ESIResource,
    ShorelineImpact,
    SpillSummary,
)


class TestSpillSummarySchema:
    """Tests for SpillSummary schema validation."""

    def test_valid_spill_summary(self):
        summary = SpillSummary(
            total_spilled_tonnes=100.0,
            estimated_slick_area_km2=45.8,
            simulation_duration_hours=72,
            weathering_percent=25.0,
            evaporation_percent=15.0,
            dispersion_percent=10.0,
            remaining_surface_oil_tonnes=75.0,
        )
        assert summary.total_spilled_tonnes == 100.0
        assert summary.estimated_slick_area_km2 == 45.8

    def test_spill_summary_negative_values_rejected(self):
        with pytest.raises(ValueError):
            SpillSummary(
                total_spilled_tonnes=-10.0,
                estimated_slick_area_km2=45.8,
                simulation_duration_hours=72,
                weathering_percent=25.0,
                evaporation_percent=15.0,
                dispersion_percent=10.0,
                remaining_surface_oil_tonnes=75.0,
            )


class TestDangerAssessmentSchema:
    """Tests for DangerAssessment schema validation."""

    def test_valid_danger_assessment(self):
        assessment = DangerAssessment(
            overall_risk="HIGH",
            environmental_risk="HIGH",
            shoreline_risk="MEDIUM",
            human_exposure_risk="MEDIUM",
            cleanup_difficulty="HIGH",
            hazard_score=68.5,
        )
        assert assessment.overall_risk == "HIGH"
        assert assessment.hazard_score == 68.5

    def test_invalid_risk_level_rejected(self):
        with pytest.raises(ValueError):
            DangerAssessment(
                overall_risk="INVALID",
                environmental_risk="HIGH",
                shoreline_risk="MEDIUM",
                human_exposure_risk="MEDIUM",
                cleanup_difficulty="HIGH",
                hazard_score=50.0,
            )

    def test_hazard_score_bounds(self):
        # Valid bounds
        DangerAssessment(
            overall_risk="LOW",
            environmental_risk="LOW",
            shoreline_risk="LOW",
            human_exposure_risk="LOW",
            cleanup_difficulty="LOW",
            hazard_score=0.0,
        )
        DangerAssessment(
            overall_risk="VERY_HIGH",
            environmental_risk="VERY_HIGH",
            shoreline_risk="VERY_HIGH",
            human_exposure_risk="VERY_HIGH",
            cleanup_difficulty="VERY_HIGH",
            hazard_score=100.0,
        )

        # Out of bounds
        with pytest.raises(ValueError):
            DangerAssessment(
                overall_risk="HIGH",
                environmental_risk="HIGH",
                shoreline_risk="HIGH",
                human_exposure_risk="HIGH",
                cleanup_difficulty="HIGH",
                hazard_score=-1.0,
            )
        with pytest.raises(ValueError):
            DangerAssessment(
                overall_risk="HIGH",
                environmental_risk="HIGH",
                shoreline_risk="HIGH",
                human_exposure_risk="HIGH",
                cleanup_difficulty="HIGH",
                hazard_score=101.0,
            )


class TestESIResourceSchema:
    """Tests for ESIResource schema validation."""

    def test_valid_esi_resource(self):
        resource = ESIResource(
            resource_id="esi-mangrove-001",
            resource_type="mangrove",
            resource_name="Thane Creek Mangroves",
            sensitivity_score=95,
            geometry={"type": "Polygon", "coordinates": [[[72.95, 19.15], [73.05, 19.15], [73.05, 19.25], [72.95, 19.25], [72.95, 19.15]]]},
            affected_area_km2=2.3,
            risk_level="HIGH",
        )
        assert resource.resource_id == "esi-mangrove-001"
        assert resource.affected_area_km2 == 2.3
        assert resource.risk_level == "HIGH"

    def test_optional_fields_can_be_none(self):
        resource = ESIResource(
            resource_id="esi-test",
            resource_type="mangrove",
            resource_name="Test",
            sensitivity_score=90,
            geometry={"type": "Point", "coordinates": [72.8, 19.0]},
        )
        assert resource.affected_area_km2 is None
        assert resource.risk_level is None


class TestShorelineImpactSchema:
    """Tests for ShorelineImpact schema validation."""

    def test_valid_shoreline_impact(self):
        impact = ShorelineImpact(
            location="Alibaug Coast",
            arrival_time_hours=(36, 48),
            impact_level="HIGH",
            distance_km=12.5,
            coordinates=[72.87, 18.64],
        )
        assert impact.location == "Alibaug Coast"
        assert impact.arrival_time_hours == (36, 48)
        assert impact.impact_level == "HIGH"

    def test_optional_fields(self):
        impact = ShorelineImpact(
            location="Test Beach",
            impact_level="LOW",
        )
        assert impact.arrival_time_hours is None
        assert impact.distance_km is None
        assert impact.coordinates is None


class TestDamageAssessmentReadSchema:
    """Tests for DamageAssessmentRead schema."""

    def test_valid_damage_assessment_read(self):
        assessment = DamageAssessmentRead(
            assessment_id="damage-test123",
            incident_id="ORCA-20260901-ABC123",
            simulation_run_id="sim-test456",
            spill_summary=SpillSummary(
                total_spilled_tonnes=100.0,
                estimated_slick_area_km2=45.8,
                simulation_duration_hours=72,
                weathering_percent=25.0,
                evaporation_percent=15.0,
                dispersion_percent=10.0,
                remaining_surface_oil_tonnes=75.0,
            ),
            danger_assessment=DangerAssessment(
                overall_risk="HIGH",
                environmental_risk="HIGH",
                shoreline_risk="MEDIUM",
                human_exposure_risk="MEDIUM",
                cleanup_difficulty="HIGH",
                hazard_score=68.5,
            ),
            ecological_resources=[
                ESIResource(
                    resource_id="esi-mangrove-001",
                    resource_type="mangrove",
                    resource_name="Thane Creek Mangroves",
                    sensitivity_score=95,
                    geometry={"type": "Polygon", "coordinates": [[[72.95, 19.15], [73.05, 19.15], [73.05, 19.25], [72.95, 19.25], [72.95, 19.15]]]},
                    affected_area_km2=2.3,
                    risk_level="HIGH",
                ),
            ],
            shoreline_impact=[
                ShorelineImpact(
                    location="Alibaug Coast",
                    arrival_time_hours=(36, 48),
                    impact_level="HIGH",
                    distance_km=12.5,
                    coordinates=[72.87, 18.64],
                ),
            ],
            calculated_at=datetime.utcnow(),
        )
        assert assessment.assessment_id == "damage-test123"
        assert len(assessment.ecological_resources) == 1
        assert len(assessment.shoreline_impact) == 1


class TestDamageService:
    """Tests for DamageService (requires mock data)."""

    @pytest.mark.asyncio
    async def test_assess_damage_returns_assessment(self):
        from backend.services.damage_service import DamageService

        service = DamageService()
        # Use a known simulation run ID from mock data
        result = await service.assess_damage("sim-test-run-id")

        # Service returns mock data regardless of input
        assert result is not None
        assert result.assessment_id.startswith("damage-")
        assert result.incident_id is not None
        assert result.simulation_run_id == "sim-test-run-id"
        assert isinstance(result.spill_summary, SpillSummary)
        assert isinstance(result.danger_assessment, DangerAssessment)
        assert isinstance(result.ecological_resources, list)
        assert isinstance(result.shoreline_impact, list)
        assert isinstance(result.calculated_at, datetime)

    def test_spill_summary_values(self):
        from backend.services.damage_service import DamageService

        service = DamageService()
        import asyncio
        result = asyncio.run(service.assess_damage("sim-test"))

        summary = result.spill_summary
        assert summary.total_spilled_tonnes > 0
        assert summary.estimated_slick_area_km2 >= 0
        assert summary.simulation_duration_hours > 0
        assert 0 <= summary.weathering_percent <= 100
        assert 0 <= summary.evaporation_percent <= 100
        assert 0 <= summary.dispersion_percent <= 100
        assert summary.remaining_surface_oil_tonnes >= 0

    def test_danger_assessment_values(self):
        from backend.services.damage_service import DamageService

        service = DamageService()
        import asyncio
        result = asyncio.run(service.assess_damage("sim-test"))

        danger = result.danger_assessment
        valid_risks = {"LOW", "MEDIUM", "HIGH", "VERY_HIGH"}
        assert danger.overall_risk in valid_risks
        assert danger.environmental_risk in valid_risks
        assert danger.shoreline_risk in valid_risks
        assert danger.human_exposure_risk in valid_risks
        assert danger.cleanup_difficulty in valid_risks
        assert 0 <= danger.hazard_score <= 100

    def test_ecological_resources_structure(self):
        from backend.services.damage_service import DamageService

        service = DamageService()
        import asyncio
        result = asyncio.run(service.assess_damage("sim-test"))

        for resource in result.ecological_resources:
            assert resource.resource_id is not None
            assert resource.resource_type is not None
            assert resource.resource_name is not None
            assert resource.sensitivity_score >= 0
            if resource.affected_area_km2 is not None:
                assert resource.affected_area_km2 >= 0
            if resource.risk_level is not None:
                assert resource.risk_level in {"LOW", "MEDIUM", "HIGH", "VERY_HIGH"}

    def test_shoreline_impact_structure(self):
        from backend.services.damage_service import DamageService

        service = DamageService()
        import asyncio
        result = asyncio.run(service.assess_damage("sim-test"))

        for impact in result.shoreline_impact:
            assert impact.location is not None
            assert impact.impact_level in {"LOW", "MEDIUM", "HIGH", "VERY_HIGH"}
            if impact.arrival_time_hours is not None:
                assert len(impact.arrival_time_hours) == 2
                assert impact.arrival_time_hours[0] <= impact.arrival_time_hours[1]
            if impact.distance_km is not None:
                assert impact.distance_km >= 0