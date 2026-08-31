"""Liability service."""

from __future__ import annotations


class LiabilityService:
    def compute(self, incident: dict, iterations: int = 1000) -> dict:
        from engine.liability.calculator import calculate

        return calculate(incident, iterations=iterations)