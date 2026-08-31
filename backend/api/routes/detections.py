"""Detection endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def list_detections(
    bbox: str | None = Query(None, description="minLon,minLat,maxLon,maxLat"),
    since: str | None = Query(None, description="ISO timestamp"),
    limit: int = Query(100, ge=1, le=1000),
) -> dict:
    """List SAR oil spill detections."""
    raise NotImplementedError


@router.get("/{detection_id}")
async def get_detection(detection_id: int) -> dict:
    """Fetch one detection by id."""
    raise NotImplementedError


@router.post("/")
async def create_detection(payload: dict) -> dict:
    """Manually register a detection (analyst override)."""
    raise NotImplementedError