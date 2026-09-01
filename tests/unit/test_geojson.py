"""Unit tests for GeoJSON generation and validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.damage.esi_loader import load_esi_features
from engine.simulation.output import create_concentration_grid
from engine.simulation.particles import ParticleArray


class TestGeoJSONStructure:
    """Tests for GeoJSON structure validity."""

    def test_esi_features_geojson_loads(self):
        features = load_esi_features()
        assert len(features) > 0
        for feature in features:
            assert "id" in feature
            assert "resource_type" in feature
            assert "resource_name" in feature
            assert "sensitivity_score" in feature
            assert "geometry" in feature
            assert feature["geometry"]["type"] in ("Polygon", "MultiPolygon")
            assert "coordinates" in feature["geometry"]

    def test_esi_features_have_valid_coordinates(self):
        features = load_esi_features()
        for feature in features:
            coords = feature["geometry"]["coordinates"]
            if feature["geometry"]["type"] == "Polygon":
                for ring in coords:
                    for coord in ring:
                        assert len(coord) == 2
                        assert -180 <= coord[0] <= 180
                        assert -90 <= coord[1] <= 90

    def test_simulation_frames_exist(self):
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        for t in [0, 12, 24, 36, 48, 60, 72]:
            frame_file = frames_dir / f"{t}h.geojson"
            assert frame_file.exists(), f"Missing frame file: {frame_file}"
            data = json.loads(frame_file.read_text())
            assert data["type"] == "FeatureCollection"
            assert "features" in data
            assert len(data["features"]) > 0


class TestSimulationFrameStructure:
    """Tests for simulation frame GeoJSON structure."""

    def test_frame_has_concentration_polygons(self):
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        frame_file = frames_dir / "24h.geojson"
        data = json.loads(frame_file.read_text())

        concentrations = set()
        for feature in data["features"]:
            props = feature.get("properties", {})
            if "concentration" in props:
                concentrations.add(props["concentration"])
            assert feature["geometry"]["type"] in ("Polygon", "Point")

        assert "VERY_HIGH" in concentrations or "HIGH" in concentrations
        assert "LOW" in concentrations

    def test_frame_has_release_point(self):
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        frame_file = frames_dir / "0h.geojson"
        data = json.loads(frame_file.read_text())

        release_points = [
            f for f in data["features"]
            if f.get("properties", {}).get("type") == "release_point"
        ]
        assert len(release_points) == 1
        assert release_points[0]["geometry"]["type"] == "Point"

    def test_frame_has_vessel_position(self):
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        frame_file = frames_dir / "24h.geojson"
        data = json.loads(frame_file.read_text())

        vessels = [
            f for f in data["features"]
            if f.get("properties", {}).get("type") == "vessel"
        ]
        assert len(vessels) >= 1
        assert vessels[0]["geometry"]["type"] == "Point"

    def test_concentration_levels_have_colors(self):
        frames_dir = Path(__file__).resolve().parents[2] / "data" / "simulation_frames"
        frame_file = frames_dir / "48h.geojson"
        data = json.loads(frame_file.read_text())

        for feature in data["features"]:
            props = feature.get("properties", {})
            if "concentration" in props:
                assert "color" in props
                assert props["color"].startswith("#")
                assert "opacity" in props
                assert 0 <= props["opacity"] <= 1


class TestParticleArrayGeoJSON:
    """Tests for particle array GeoJSON output."""

    def test_particle_array_to_geojson(self):
        particles = ParticleArray.create_initial(
            n_particles=10,
            longitude=72.8177,
            latitude=18.9076,
            total_mass_kg=100000,
        )
        geojson = particles.to_geojson()

        assert geojson["type"] == "FeatureCollection"
        assert len(geojson["features"]) == 10
        for feature in geojson["features"]:
            assert feature["geometry"]["type"] == "Point"
            coords = feature["geometry"]["coordinates"]
            assert coords[0] == pytest.approx(72.8177, rel=1e-10)
            assert coords[1] == pytest.approx(18.9076, rel=1e-10)
            assert "mass_kg" in feature["properties"]
            assert "age_hours" in feature["properties"]

    def test_particle_array_get_bounds(self):
        particles = ParticleArray.create_initial(
            n_particles=5,
            longitude=72.8177,
            latitude=18.9076,
            total_mass_kg=100000,
        )
        bounds = particles.get_bounds()
        assert bounds == (72.8177, 18.9076, 72.8177, 18.9076)


class TestConcentrationGridGeneration:
    """Tests for concentration grid generation from particles."""

    def test_create_concentration_grid_empty(self):
        particles = ParticleArray(
            longitude=[],
            latitude=[],
            mass_kg=[],
            age_hours=[],
            status=[],
        )
        grid = create_concentration_grid(particles, grid_size=10)
        assert grid["type"] == "FeatureCollection"
        assert len(grid["features"]) == 0

    def test_create_concentration_grid_with_particles(self):
        # Create particles spread over a small area to ensure proper binning
        import numpy as np
        n_particles = 100
        base_lon, base_lat = 72.8177, 18.9076
        lons = base_lon + np.random.normal(0, 0.001, n_particles)
        lats = base_lat + np.random.normal(0, 0.001, n_particles)
        masses = np.full(n_particles, 1000.0)  # 1000 kg each = 100,000 kg total
        ages = np.zeros(n_particles)
        status = np.zeros(n_particles, dtype=np.int8)

        particles = ParticleArray(
            longitude=lons,
            latitude=lats,
            mass_kg=masses,
            age_hours=ages,
            status=status,
        )
        grid = create_concentration_grid(particles, grid_size=20, bounds=(72.8, 18.9, 72.85, 18.95))

        assert grid["type"] == "FeatureCollection"
        assert len(grid["features"]) > 0

        # Check concentration levels present
        concentrations = {
            f["properties"]["concentration"]
            for f in grid["features"]
            if "concentration" in f["properties"]
        }
        assert len(concentrations) > 0

    def test_concentration_grid_has_release_point(self):
        particles = ParticleArray.create_initial(
            n_particles=50,
            longitude=72.8177,
            latitude=18.9076,
            total_mass_kg=50000,
        )
        grid = create_concentration_grid(particles, grid_size=20)

        release_points = [
            f for f in grid["features"]
            if f.get("properties", {}).get("type") == "release_point"
        ]
        assert len(release_points) == 1