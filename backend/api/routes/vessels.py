"""Vessel endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def list_vessels(
    bbox: str | None = Query(None),
    since: str | None = Query(None),
    mmsi: int | None = Query(None),
    limit: int = Query(500, ge=1, le=5000),
) -> dict:
    """List vessels / vessel positions."""
    raise NotImplementedError


@router.get("/{mmsi}/track")
async def get_vessel_track(mmsi: int, since: str | None = None, until: str | None = None) -> dict:
    """Return the reconstructed track for a vessel."""
    raise NotImplementedError


@router.get("/{mmsi}")
async def get_vessel(mmsi: int) -> dict:
    """Return vessel metadata."""
    raise NotImplementedError