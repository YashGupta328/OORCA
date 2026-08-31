"""SAR worker tasks."""

from __future__ import annotations

from backend.workers.celery_app import app


@app.task(name="backend.workers.sar_worker.run_detection")
def run_detection(scene_id: str) -> list[dict]:
    from backend.services.sar_service import SarService

    return SarService().detect_scene(scene_id)