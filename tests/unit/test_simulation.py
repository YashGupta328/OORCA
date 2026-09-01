"""Unit tests for simulation input validation."""

from __future__ import annotations

import pytest
from datetime import datetime, timedelta

from backend.api.schemas.incident import (
    IncidentCreate,
    Location,
    SpillDetails,
    VesselDetails,
)


class TestLocationValidation:
    """Tests for Location coordinate validation."""

    def test_valid_coordinates(self):
        loc = Location(latitude=18.9076, longitude=72.8177)
        assert loc.latitude == 18.9076
        assert loc.longitude == 72.8177

    def test_latitude_boundary_values(self):
        Location(latitude=90, longitude=0)
        Location(latitude=-90, longitude=0)
        Location(latitude=0, longitude=0)

    def test_longitude_boundary_values(self):
        Location(latitude=0, longitude=180)
        Location(latitude=0, longitude=-180)

    def test_invalid_latitude_too_high(self):
        with pytest.raises(ValueError):
            Location(latitude=91, longitude=0)

    def test_invalid_latitude_too_low(self):
        with pytest.raises(ValueError):
            Location(latitude=-91, longitude=0)

    def test_invalid_longitude_too_high(self):
        with pytest.raises(ValueError):
            Location(latitude=0, longitude=181)

    def test_invalid_longitude_too_low(self):
        with pytest.raises(ValueError):
            Location(latitude=0, longitude=-181)


class TestSpillDetailsValidation:
    """Tests for SpillDetails validation."""

    def test_valid_spill_details(self):
        spill = SpillDetails(
            amount=100,
            unit="tonnes",
            oil_type="crude_oil",
            start_time=datetime.utcnow(),
            duration_hours=72,
        )
        assert spill.amount == 100
        assert spill.unit == "tonnes"
        assert spill.oil_type == "crude_oil"
        assert spill.duration_hours == 72

    def test_valid_units(self):
        for unit in ["tonnes", "barrels", "liters", "gallons"]:
            spill = SpillDetails(
                amount=100,
                unit=unit,
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=24,
            )
            assert spill.unit == unit

    def test_valid_oil_types(self):
        for oil_type in ["crude_oil", "diesel", "heavy_fuel_oil", "gasoline", "jet_fuel"]:
            spill = SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type=oil_type,
                start_time=datetime.utcnow(),
                duration_hours=24,
            )
            assert spill.oil_type == oil_type

    def test_invalid_amount_zero(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=0,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=24,
            )

    def test_invalid_amount_negative(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=-10,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=24,
            )

    def test_invalid_unit(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=100,
                unit="invalid_unit",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=24,
            )

    def test_invalid_oil_type(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="invalid_oil",
                start_time=datetime.utcnow(),
                duration_hours=24,
            )

    def test_invalid_duration_zero(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=0,
            )

    def test_invalid_duration_negative(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=-1,
            )

    def test_invalid_duration_too_long(self):
        with pytest.raises(ValueError):
            SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=169,  # max is 168 (1 week)
            )


class TestVesselDetailsValidation:
    """Tests for VesselDetails validation."""

    def test_valid_vessel_details(self):
        vessel = VesselDetails(
            name="MV Oceanic Star",
            vessel_type="oil_tanker",
            imo="9732548",
            length_m=274,
            breadth_m=48,
            draft_m=16,
            heading_deg=45,
        )
        assert vessel.name == "MV Oceanic Star"
        assert vessel.vessel_type == "oil_tanker"
        assert vessel.imo == "9732548"
        assert vessel.length_m == 274

    def test_optional_fields_can_be_none(self):
        vessel = VesselDetails()
        assert vessel.name is None
        assert vessel.vessel_type is None
        assert vessel.imo is None

    def test_valid_vessel_types(self):
        for vtype in ["oil_tanker", "cargo", "fishing", "passenger", "other"]:
            vessel = VesselDetails(vessel_type=vtype)
            assert vessel.vessel_type == vtype

    def test_invalid_vessel_type(self):
        with pytest.raises(ValueError):
            VesselDetails(vessel_type="invalid_type")

    def test_invalid_length_zero(self):
        with pytest.raises(ValueError):
            VesselDetails(length_m=0)

    def test_invalid_breadth_negative(self):
        with pytest.raises(ValueError):
            VesselDetails(breadth_m=-10)

    def test_invalid_heading_too_high(self):
        with pytest.raises(ValueError):
            VesselDetails(heading_deg=360)

    def test_invalid_heading_negative(self):
        with pytest.raises(ValueError):
            VesselDetails(heading_deg=-1)

    def test_heading_boundary_values(self):
        VesselDetails(heading_deg=0)
        VesselDetails(heading_deg=359)


class TestIncidentCreateValidation:
    """Tests for complete IncidentCreate validation."""

    def test_minimal_valid_incident(self):
        incident = IncidentCreate(
            location=Location(latitude=18.9076, longitude=72.8177),
            spill=SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=72,
            ),
        )
        assert incident.location.latitude == 18.9076
        assert incident.spill.amount == 100
        assert incident.vessel is None

    def test_incident_with_vessel(self):
        incident = IncidentCreate(
            location=Location(latitude=18.9076, longitude=72.8177),
            spill=SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=datetime.utcnow(),
                duration_hours=72,
            ),
            vessel=VesselDetails(
                name="MV Test",
                vessel_type="oil_tanker",
                imo="1234567",
            ),
        )
        assert incident.vessel is not None
        assert incident.vessel.name == "MV Test"

    def test_missing_location_raises(self):
        with pytest.raises(ValueError):
            IncidentCreate(
                spill=SpillDetails(
                    amount=100,
                    unit="tonnes",
                    oil_type="crude_oil",
                    start_time=datetime.utcnow(),
                    duration_hours=72,
                ),
            )

    def test_missing_spill_raises(self):
        with pytest.raises(ValueError):
            IncidentCreate(
                location=Location(latitude=18.9076, longitude=72.8177),
            )

    def test_future_start_time_accepted(self):
        future_time = datetime.utcnow() + timedelta(days=1)
        incident = IncidentCreate(
            location=Location(latitude=18.9076, longitude=72.8177),
            spill=SpillDetails(
                amount=100,
                unit="tonnes",
                oil_type="crude_oil",
                start_time=future_time,
                duration_hours=72,
            ),
        )
        assert incident.spill.start_time == future_time