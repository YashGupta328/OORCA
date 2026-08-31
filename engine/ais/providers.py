"""AIS provider clients.

Each provider is optional; the service only requires credentials for the
providers you intend to use. Credentials are read from .env (see AISSettings).
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from backend.core.security import mask
from backend.core.settings import get_settings

log = logging.getLogger(__name__)


def _check(provider: str, key: str | None) -> str:
    if not key:
        raise RuntimeError(
            f"{provider} credentials missing: set the matching API key in .env"
        )
    return key


def fetch_marinetraffic(bbox: tuple[float, float, float, float], since: str) -> list[dict[str, Any]]:
    key = _check("MarineTraffic", get_settings().ais.marinetraffic_api_key)
    log.debug("MarineTraffic bbox=%s key=%s", bbox, mask(key))
    raise NotImplementedError


def fetch_ais_hub(mmsi: int, since: str) -> list[dict[str, Any]]:
    key = _check("AIS Hub", get_settings().ais.hub_api_key)
    log.debug("AIS Hub mmsi=%s key=%s", mmsi, mask(key))
    raise NotImplementedError


def fetch_vesselfinder(mmsi: int) -> dict[str, Any]:
    key = _check("VesselFinder", get_settings().ais.vesselfinder_api_key)
    log.debug("VesselFinder mmsi=%s key=%s", mmsi, mask(key))
    raise NotImplementedError


def fetch_aisstream_stream() -> Any:
    """Connect to the AISStream websocket. Returns a context manager."""
    key = _check("AISStream", get_settings().ais.aisstream_api_key)
    log.debug("AISStream key=%s", mask(key))
    raise NotImplementedError