"""Weathering model for oil spill simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class WeatheringRates:
    """Weathering rates for a specific oil type."""
    evaporation_rate_per_hour: float
    dispersion_rate_per_hour: float
    emulsification_rate_per_hour: float
    biodegradation_rate_per_hour: float = 0.001


class WeatheringModel:
    """Model for oil weathering processes."""

    def __init__(self, oil_type: str = "crude_oil") -> None:
        self.oil_type = oil_type
        self.rates = self._get_default_rates(oil_type)

    def _get_default_rates(self, oil_type: str) -> WeatheringRates:
        """Get default weathering rates for oil type."""
        rates = {
            "crude_oil": WeatheringRates(0.02, 0.008, 0.015),
            "diesel": WeatheringRates(0.05, 0.025, 0.005),
            "heavy_fuel_oil": WeatheringRates(0.003, 0.001, 0.02),
            "gasoline": WeatheringRates(0.15, 0.01, 0.001),
            "jet_fuel": WeatheringRates(0.08, 0.015, 0.002),
        }
        return rates.get(oil_type, rates["crude_oil"])

    def step(self, particles: Any, dt_hours: float, water_temp_c: float = 28.0) -> dict[str, float]:
        """Apply weathering for one time step.

        Args:
            particles: ParticleArray instance
            dt_hours: Time step in hours
            water_temp_c: Water temperature in Celsius

        Returns:
            Dictionary with mass balance changes
        """
        active = particles.get_active_particles()
        if len(active) == 0:
            return {"evaporated_kg": 0, "dispersed_kg": 0, "emulsified_kg": 0}

        # Temperature correction for evaporation (Arrhenius-like)
        temp_factor = np.exp(0.07 * (water_temp_c - 15.0))

        # Evaporation
        evap_rate = self.rates.evaporation_rate_per_hour * temp_factor
        evap_mass = particles.mass_kg[active] * evap_rate * dt_hours
        evap_mass = np.minimum(evap_mass, particles.mass_kg[active] * 0.5)  # Max 50% per step

        # Dispersion
        disp_rate = self.rates.dispersion_rate_per_hour
        disp_mass = particles.mass_kg[active] * disp_rate * dt_hours

        # Emulsification (increases volume, decreases evaporation)
        emuls_rate = self.rates.emulsification_rate_per_hour
        emuls_mass = particles.mass_kg[active] * emuls_rate * dt_hours

        # Apply mass loss
        total_loss = evap_mass + disp_mass
        particles.mass_kg[active] -= total_loss

        # Mark particles for removal if mass too low
        min_mass = 0.001  # kg
        depleted = active[particles.mass_kg[active] < min_mass]
        particles.status[depleted] = 1  # evaporated/dispersed

        return {
            "evaporated_kg": float(np.sum(evap_mass)),
            "dispersed_kg": float(np.sum(disp_mass)),
            "emulsified_kg": float(np.sum(emuls_mass)),
            "active_particles": int(np.sum(particles.status == 0)),
        }

    def get_mass_balance(self, particles: Any) -> dict[str, float]:
        """Get current mass balance."""
        active = particles.get_active_particles()
        evaporated = particles.status == 1
        dispersed = particles.status == 2
        beached = particles.status == 3

        return {
            "surface_kg": float(np.sum(particles.mass_kg[active])),
            "evaporated_kg": float(np.sum(particles.mass_kg[evaporated])),
            "dispersed_kg": float(np.sum(particles.mass_kg[dispersed])),
            "beached_kg": float(np.sum(particles.mass_kg[beached])),
            "total_initial_kg": float(np.sum(particles.mass_kg)),
        }