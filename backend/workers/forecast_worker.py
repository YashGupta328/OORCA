"""Forecast worker tasks."""

from __future__ import annotations

from backend.workers.celery_app import app


@app.task(name="backend.workers.forecast_worker.run")
def run_forecast(release: dict, hours: int = 72) -> dict:
    from backend.services.drift_service import DriftService

    return DriftService().forecast(release, hours)