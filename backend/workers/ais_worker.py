"""AIS worker tasks."""

from __future__ import annotations

from backend.workers.celery_app import app


@app.task(name="backend.workers.ais_worker.ingest")
def ingest(source: str) -> int:
    from backend.services.ais_service import AisService

    return AisService().ingest(source)