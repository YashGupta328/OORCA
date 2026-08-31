"""Hindcast worker tasks."""

from __future__ import annotations

from backend.workers.celery_app import app


@app.task(name="backend.workers.hindcast_worker.run")
def run_hindcast(detection: dict, hours: int = 48) -> dict:
    from backend.services.drift_service import DriftService

    return DriftService().hindcast(detection, hours)