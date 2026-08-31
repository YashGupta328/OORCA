"""Vessel schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class VesselBase(BaseModel):
    mmsi: int
    imo: int | None = None
    name: str | None = None
    vessel_type: str | None = None
    length_m: float | None = None
    beam_m: float | None = None
    flag: str | None = None


class VesselRead(VesselBase):
    class Config:
        from_attributes = True


class Position(BaseModel):
    mmsi: int
    ts: datetime
    lat: float
    lon: float
    sog: float | None = None
    cog: float | None = None
    heading: float | None = None
    nav_status: str | None = None


class Track(BaseModel):
    mmsi: int
    positions: list[Position]