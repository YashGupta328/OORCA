"""Forecast endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/run")
async def run_forecast(payload: dict) -> dict:
    """Trigger a drift forecast for a given release scenario."""
    raise NotImplementedError


@router.get("/{forecast_id}")
async def get_forecast(forecast_id: int) -> dict:
    """Retrieve forecast results (footprints, contours)."""
    raise NotImplementedError