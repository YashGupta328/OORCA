"""Drift service: hindcast and forecast orchestration."""

from __future__ import annotations


class DriftService:
    def hindcast(self, detection: dict, hours: int) -> dict:
        from engine.drift.hindcast import run_hindcast
        return run_hindcast(detection, hours)

    def forecast(self, release: dict, hours: int) -> dict:
        from engine.drift.forecast import run_forecast
        return run_forecast(release, hours)