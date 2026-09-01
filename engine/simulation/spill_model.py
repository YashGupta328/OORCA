"""Spill model definitions for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class OilType(str, Enum):
    """Oil types with their properties."""
    CRUDE_OIL = "crude_oil"
    DIESEL = "diesel"
    HEAVY_FUEL_OIL = "heavy_fuel_oil"
    GASOLINE = "gasoline"
    JET_FUEL = "jet_fuel"


OIL_PROPERTIES = {
    OilType.CRUDE_OIL: {
        "density_kg_m3": 950,
        "viscosity_cst": 500,
        "evaporation_rate": 0.25,
        "dispersion_rate": 0.10,
        "emulsification_rate": 0.30,
        "weathering_half_life_hours": 48,
    },
    OilType.DIESEL: {
        "density_kg_m3": 850,
        "viscosity_cst": 10,
        "evaporation_rate": 0.50,
        "dispersion_rate": 0.30,
        "emulsification_rate": 0.05,
        "weathering_half_life_hours": 12,
    },
    OilType.HEAVY_FUEL_OIL: {
        "density_kg_m3": 1000,
        "viscosity_cst": 50000,
        "evaporation_rate": 0.05,
        "dispersion_rate": 0.02,
        "emulsification_rate": 0.40,
        "weathering_half_life_hours": 120,
    },
    OilType.GASOLINE: {
        "density_kg_m3": 750,
        "viscosity_cst": 1,
        "evaporation_rate": 0.90,
        "dispersion_rate": 0.05,
        "emulsification_rate": 0.01,
        "weathering_half_life_hours": 2,
    },
    OilType.JET_FUEL: {
        "density_kg_m3": 800,
        "viscosity_cst": 2,
        "evaporation_rate": 0.70,
        "dispersion_rate": 0.15,
        "emulsification_rate": 0.02,
        "weathering_half_life_hours": 6,
    },
}


@dataclass
class SpillModel:
    """Spill model parameters."""
    oil_type: OilType = OilType.CRUDE_OIL
    amount_tonnes: float = 100.0
    latitude: float = 0.0
    longitude: float = 0.0
    release_time: datetime | None = None
    duration_hours: int = 72
    release_depth_m: float = 0.0  # 0 = surface release

    def get_properties(self) -> dict[str, Any]:
        """Get oil properties for this spill."""
        return OIL_PROPERTIES.get(self.oil_type, OIL_PROPERTIES[OilType.CRUDE_OIL])

    def get_initial_volume_m3(self) -> float:
        """Calculate initial volume in m3."""
        props = self.get_properties()
        return (self.amount_tonnes * 1000) / props["density_kg_m3"]

    def estimate_weathering(self, hours: int) -> dict[str, float]:
        """Estimate weathering after given hours (simplified exponential model)."""
        props = self.get_properties()
        half_life = props["weathering_half_life_hours"]
        if half_life <= 0:
            return {"evaporated": 0, "dispersed": 0, "remaining": 100}

        import math
        decay = math.exp(-math.log(2) * hours / half_life)
        remaining = decay * 100
        evaporated = props["evaporation_rate"] * (100 - remaining)
        dispersed = props["dispersion_rate"] * (100 - remaining)
        emulsified = props["emulsification_rate"] * (100 - remaining)

        return {
            "evaporated": round(min(evaporated, 100), 1),
            "dispersed": round(min(dispersed, 100), 1),
            "emulsified": round(min(emulsified, 100), 1),
            "remaining": round(max(remaining - evaporated - dispersed - emulsified, 0), 1),
        }