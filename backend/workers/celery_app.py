"""Celery app for the OORCA worker stack."""

from __future__ import annotations

from backend.workers import celery_app

app = celery_app