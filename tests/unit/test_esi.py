"""Unit tests for ESI spatial intersection and damage calculations."""

from __future__ import annotations

from shapely.geometry import Polygon, shape

from engine.damage.esi_loader import load_esi_features, ESIResource
from engine.damage.spatial_intersection import calculate_intersections
from engine.damage.exposure import calculate_exposure
from engine.damage.sensitivity import calculate_sensitivity
from engine.damage.hazard_zone import calculate_hazard_zones
from engine.damage.scoring import calculate_hazard_score, calculate_component_scores


class TestESILoader:
    """Tests for ESI feature loading."""

    def test_load_esi_features_returns_list(self):
        features = load_esi_features()
        assert isinstance(features, list)
        assert len(features) > 0

    def test_esi_features_have_required_fields(self):
        features = load_esi_features()
        for feature in features:
            assert "id" in feature
            assert "resource_type" in feature
            assert "resource_name" in feature
            assert "sensitivity_score" in feature
            assert "geometry" in feature

    def test_esi_sensitivity_scores_in_range(self):
        features = load_esi_features()
        for feature in features:
            score = feature["sensitivity_score"]
            assert 0 <= score <= 100, f"Invalid sensitivity score: {score}"

    def test_esi_resource_types_known(self):
        features = load_esi_features()
        known_types = {
            "mangrove", "coral_reef", "seagrass", "fish_habitat",
            "sea_turtle_habitat", "dolphin_habitat", "protected_area",
            "saltmarsh",
        }
        for feature in features:
            assert feature["resource_type"] in known_types

    def test_esi_resource_wrapper(self):
        features = load_esi_features()
        resource = ESIResource(features[0])
        assert resource.id == features[0]["id"]
        assert resource.resource_type == features[0]["resource_type"]
        assert resource.sensitivity_score == features[0]["sensitivity_score"]
        assert resource.geometry == features[0]["geometry"]


class TestSpatialIntersection:
    """Tests for spatial intersection calculations."""

    def test_intersection_with_overlapping_polygons(self):
        # Create a simple spill polygon
        spill_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"concentration": "HIGH"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [72.9, 19.1],
                            [73.0, 19.1],
                            [73.0, 19.2],
                            [72.9, 19.2],
                            [72.9, 19.1],
                        ]],
                    },
                },
            ],
        }

        esi_features = [{
            "id": "test-mangrove",
            "resource_type": "mangrove",
            "resource_name": "Test Mangrove",
            "sensitivity_score": 90,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [72.95, 19.15],
                    [73.05, 19.15],
                    [73.05, 19.25],
                    [72.95, 19.25],
                    [72.95, 19.15],
                ]],
            },
        }]

        intersections = calculate_intersections(spill_geojson, esi_features)
        assert len(intersections) == 1
        inter = intersections[0]
        assert inter["resource_id"] == "test-mangrove"
        assert inter["area_km2"] > 0
        assert inter["affected_percentage"] > 0

    def test_no_intersection_when_disjoint(self):
        spill_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"concentration": "HIGH"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [70.0, 10.0],
                            [71.0, 10.0],
                            [71.0, 11.0],
                            [70.0, 11.0],
                            [70.0, 10.0],
                        ]],
                    },
                },
            ],
        }

        esi_features = [{
            "id": "test-mangrove",
            "resource_type": "mangrove",
            "resource_name": "Test Mangrove",
            "sensitivity_score": 90,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [72.95, 19.15],
                    [73.05, 19.15],
                    [73.05, 19.25],
                    [72.95, 19.25],
                    [72.95, 19.15],
                ]],
            },
        }]

        intersections = calculate_intersections(spill_geojson, esi_features)
        assert len(intersections) == 0

    def test_intersection_with_multiple_concentrations(self):
        spill_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"concentration": "VERY_HIGH"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [72.9, 19.1],
                            [72.95, 19.1],
                            [72.95, 19.15],
                            [72.9, 19.15],
                            [72.9, 19.1],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"concentration": "HIGH"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [72.95, 19.1],
                            [73.0, 19.1],
                            [73.0, 19.15],
                            [72.95, 19.15],
                            [72.95, 19.1],
                        ]],
                    },
                },
                {
                    "type": "Feature",
                    "properties": {"concentration": "MEDIUM"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [72.9, 19.15],
                            [73.0, 19.15],
                            [73.0, 19.2],
                            [72.9, 19.2],
                            [72.9, 19.15],
                        ]],
                    },
                },
            ],
        }

        esi_features = [{
            "id": "test-fish",
            "resource_type": "fish_habitat",
            "resource_name": "Test Fisheries",
            "sensitivity_score": 75,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [72.9, 19.1],
                    [73.0, 19.1],
                    [73.0, 19.2],
                    [72.9, 19.2],
                    [72.9, 19.1],
                ]],
            },
        }]

        intersections = calculate_intersections(spill_geojson, esi_features)
        assert len(intersections) == 1
        inter = intersections[0]
        assert "VERY_HIGH" in inter["concentrations_present"]
        assert "HIGH" in inter["concentrations_present"]
        assert "MEDIUM" in inter["concentrations_present"]
        assert inter["max_concentration"] == "VERY_HIGH"


class TestExposureCalculation:
    """Tests for exposure calculation."""

    def test_exposure_zero_for_no_intersections(self):
        exposure = calculate_exposure([])
        assert exposure == []

    def test_exposure_increases_with_area(self):
        intersections = [
            {
                "resource_id": "test-1",
                "resource_type": "mangrove",
                "resource_name": "Test Mangrove 1",
                "area_km2": 1.0,
                "max_concentration": "HIGH",
                "concentrations_present": ["HIGH"],
                "affected_percentage": 50,
            },
            {
                "resource_id": "test-2",
                "resource_type": "mangrove",
                "resource_name": "Test Mangrove 2",
                "area_km2": 5.0,
                "max_concentration": "HIGH",
                "concentrations_present": ["HIGH"],
                "affected_percentage": 50,
            },
        ]
        exposure = calculate_exposure(intersections)
        assert len(exposure) == 2
        # Larger area should produce higher exposure
        assert exposure[1]["exposure_score"] > exposure[0]["exposure_score"]

    def test_exposure_increases_with_concentration(self):
        intersections = [
            {
                "resource_id": "test-low",
                "resource_type": "mangrove",
                "resource_name": "Test Low",
                "area_km2": 1.0,
                "max_concentration": "LOW",
                "concentrations_present": ["LOW"],
                "affected_percentage": 50,
            },
            {
                "resource_id": "test-high",
                "resource_type": "mangrove",
                "resource_name": "Test High",
                "area_km2": 1.0,
                "max_concentration": "HIGH",
                "concentrations_present": ["HIGH"],
                "affected_percentage": 50,
            },
        ]
        exposure = calculate_exposure(intersections)
        # Higher concentration should produce higher exposure
        high_exp = next(e for e in exposure if e["resource_id"] == "test-high")
        low_exp = next(e for e in exposure if e["resource_id"] == "test-low")
        assert high_exp["exposure_score"] > low_exp["exposure_score"]


class TestSensitivityCalculation:
    """Tests for sensitivity calculation."""

    def test_sensitivity_zero_for_no_exposure(self):
        sensitivity = calculate_sensitivity([], [])
        assert sensitivity == []

    def test_sensitivity_scales_with_esi_score(self):
        exposure_results = [
            {
                "resource_id": "test-low-sens",
                "resource_type": "mangrove",
                "resource_name": "Low Sensitivity",
                "exposure_score": 1.0,
                "area_km2": 1.0,
                "affected_percentage": 50,
                "max_concentration": "HIGH",
                "concentration_weight": 0.75,
            },
            {
                "resource_id": "test-high-sens",
                "resource_type": "mangrove",
                "resource_name": "High Sensitivity",
                "exposure_score": 1.0,
                "area_km2": 1.0,
                "affected_percentage": 50,
                "max_concentration": "HIGH",
                "concentration_weight": 0.75,
            },
        ]
        esi_features = [
            {"id": "test-low-sens", "sensitivity_score": 50, "resource_type": "mangrove"},
            {"id": "test-high-sens", "sensitivity_score": 95, "resource_type": "mangrove"},
        ]
        sensitivity = calculate_sensitivity(exposure_results, esi_features)
        high_sens = next(s for s in sensitivity if s["resource_id"] == "test-high-sens")
        low_sens = next(s for s in sensitivity if s["resource_id"] == "test-low-sens")
        assert high_sens["sensitivity_score"] > low_sens["sensitivity_score"]


class TestHazardZones:
    """Tests for hazard zone calculation."""

    def test_hazard_zones_empty_for_no_sensitivity(self):
        zones = calculate_hazard_zones([])
        assert zones == []

    def test_hazard_zones_classified_correctly(self):
        sensitivity_results = [
            {
                "resource_id": "test-very-high",
                "resource_type": "coral_reef",
                "resource_name": "Very High Risk",
                "sensitivity_score": 5.0,
                "area_km2": 10.0,
                "affected_percentage": 80,
                "max_concentration": "VERY_HIGH",
            },
            {
                "resource_id": "test-high",
                "resource_type": "mangrove",
                "resource_name": "High Risk",
                "sensitivity_score": 1.5,
                "area_km2": 5.0,
                "affected_percentage": 50,
                "max_concentration": "HIGH",
            },
            {
                "resource_id": "test-medium",
                "resource_type": "seagrass",
                "resource_name": "Medium Risk",
                "sensitivity_score": 0.7,
                "area_km2": 2.0,
                "affected_percentage": 30,
                "max_concentration": "MEDIUM",
            },
            {
                "resource_id": "test-low",
                "resource_type": "saltmarsh",
                "resource_name": "Low Risk",
                "sensitivity_score": 0.2,
                "area_km2": 1.0,
                "affected_percentage": 10,
                "max_concentration": "LOW",
            },
        ]
        zones = calculate_hazard_zones(sensitivity_results)
        assert len(zones) == 4
        # Check classifications
        very_high = next(z for z in zones if z["resource_id"] == "test-very-high")
        high = next(z for z in zones if z["resource_id"] == "test-high")
        medium = next(z for z in zones if z["resource_id"] == "test-medium")
        low = next(z for z in zones if z["resource_id"] == "test-low")
        assert very_high["hazard_level"] == "VERY_HIGH"
        assert high["hazard_level"] == "HIGH"
        assert medium["hazard_level"] == "MEDIUM"
        assert low["hazard_level"] == "LOW"


class TestHazardScoring:
    """Tests for overall hazard score calculation."""

    def test_hazard_score_zero_for_no_zones(self):
        score = calculate_hazard_score([])
        assert score == 0.0

    def test_hazard_score_in_range(self):
        zones = [
            {
                "resource_id": "test-1",
                "resource_type": "mangrove",
                "hazard_level": "HIGH",
                "hazard_score": 2.0,
                "area_km2": 5.0,
                "max_concentration": "HIGH",
            },
            {
                "resource_id": "test-2",
                "resource_type": "coral_reef",
                "hazard_level": "VERY_HIGH",
                "hazard_score": 4.0,
                "area_km2": 10.0,
                "max_concentration": "VERY_HIGH",
            },
        ]
        score = calculate_hazard_score(zones)
        assert 0 <= score <= 100

    def test_hazard_score_higher_for_more_severe_zones(self):
        # Fewer but more severe zones
        zones_severe = [
            {
                "resource_id": "test-1",
                "resource_type": "coral_reef",
                "hazard_level": "VERY_HIGH",
                "hazard_score": 5.0,
                "area_km2": 20.0,
                "max_concentration": "VERY_HIGH",
            },
        ]
        # More but less severe zones
        zones_mild = [
            {
                "resource_id": "test-2",
                "resource_type": "saltmarsh",
                "hazard_level": "LOW",
                "hazard_score": 0.5,
                "area_km2": 5.0,
                "max_concentration": "LOW",
            },
        ]
        score_severe = calculate_hazard_score(zones_severe)
        score_mild = calculate_hazard_score(zones_mild)
        assert score_severe > score_mild

    def test_component_scores(self):
        zones = [
            {
                "resource_id": "test-1",
                "resource_type": "mangrove",
                "hazard_level": "HIGH",
                "hazard_score": 2.0,
                "area_km2": 5.0,
                "max_concentration": "HIGH",
            },
            {
                "resource_id": "test-2",
                "resource_type": "coral_reef",
                "hazard_level": "VERY_HIGH",
                "hazard_score": 4.0,
                "area_km2": 10.0,
                "max_concentration": "VERY_HIGH",
            },
            {
                "resource_id": "test-3",
                "resource_type": "fish_habitat",
                "hazard_level": "MEDIUM",
                "hazard_score": 1.0,
                "area_km2": 15.0,
                "max_concentration": "MEDIUM",
            },
        ]
        components = calculate_component_scores(zones)
        assert "environmental_risk" in components
        assert "shoreline_risk" in components
        assert "human_exposure_risk" in components
        assert "cleanup_difficulty" in components
        for key, value in components.items():
            assert 0 <= value <= 100

    def test_score_to_risk_level(self):
        from engine.damage.scoring import score_to_risk_level
        assert score_to_risk_level(80) == "VERY_HIGH"
        assert score_to_risk_level(60) == "HIGH"
        assert score_to_risk_level(30) == "MEDIUM"
        assert score_to_risk_level(10) == "LOW"


class TestFullDamagePipeline:
    """Integration tests for the complete damage calculation pipeline."""

    def test_full_pipeline_with_mock_data(self):
        # Create a realistic spill scenario
        spill_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"concentration": "HIGH"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [72.7, 18.8],
                            [73.0, 18.8],
                            [73.0, 19.2],
                            [72.7, 19.2],
                            [72.7, 18.8],
                        ]],
                    },
                },
            ],
        }

        esi_features = load_esi_features()

        # Run full pipeline
        intersections = calculate_intersections(spill_geojson, esi_features)
        assert len(intersections) > 0

        exposure = calculate_exposure(intersections)
        assert len(exposure) == len(intersections)

        sensitivity = calculate_sensitivity(exposure, esi_features)
        assert len(sensitivity) == len(exposure)

        hazard_zones = calculate_hazard_zones(sensitivity)
        assert len(hazard_zones) == len(sensitivity)

        hazard_score = calculate_hazard_score(hazard_zones)
        assert 0 <= hazard_score <= 100

        components = calculate_component_scores(hazard_zones)
        assert all(0 <= v <= 100 for v in components.values())