"""Liability endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/compute")
async def compute_liability(payload: dict) -> dict:
    """Run a liability Monte Carlo for an incident."""
    raise NotImplementedError


@router.get("/{report_id}")
async def get_report(report_id: int) -> dict:
    """Retrieve a liability report (summary + components + sensitivity)."""
    raise NotImplementedError