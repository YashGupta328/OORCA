"""Workers package marker."""

from __future__ import annotations

from celery import Celery

celery_app = Celery("oorca", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
celery_app.conf.task_routes = {
    "backend.workers.sar_worker.*": {"queue": "sar"},
    "backend.workers.ais_worker.*": {"queue": "ais"},
    "backend.workers.hindcast_worker.*": {"queue": "hindcast"},
    "backend.workers.forecast_worker.*": {"queue": "forecast"},
    "backend.workers.liability_worker.*": {"queue": "liability"},
}

__all__ = ["celery_app"]