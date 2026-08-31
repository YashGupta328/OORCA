"""Liability worker tasks."""

from __future__ import annotations

from backend.workers.celery_app import app


@app.task(name="backend.workers.liability_worker.compute")
def compute(incident: dict, iterations: int = 1000) -> dict:
    from backend.services.liability_service import LiabilityService

    return LiabilityService().compute(incident, iterations=iterations)