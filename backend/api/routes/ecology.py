"""Ecology endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/detection/{detection_id}")
async def ecological_exposure(detection_id: int) -> dict:
    """ESI exposure for a detection footprint."""
    raise NotImplementedError


@router.get("/forecast/{forecast_id}")
async def ecological_exposure_forecast(forecast_id: int) -> dict:
    """ESI exposure for a forecast footprint."""
    raise NotImplementedError