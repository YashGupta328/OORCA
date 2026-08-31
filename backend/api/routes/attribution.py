"""Attribution endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/run")
async def run_attribution(payload: dict) -> dict:
    """Run attribution for a given detection."""
    raise NotImplementedError


@router.get("/{detection_id}")
async def get_attribution(detection_id: int) -> dict:
    """Return ranked candidate vessels for a detection."""
    raise NotImplementedError