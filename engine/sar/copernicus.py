"""Copernicus / Sentinel-1 SAR ingestion.

Authentication uses credentials from the local .env file (Copernicus Dataspace
or legacy Copernicus Open Access Hub). The module never logs the raw password.
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.core.security import mask
from backend.core.settings import get_settings

log = logging.getLogger(__name__)


def authenticate() -> tuple[str, str]:
    """Return (username, password) from settings. Raise if missing."""
    s = get_settings().copernicus
    if not s.has_credentials():
        raise RuntimeError(
            "Copernicus credentials missing: set COPERNICUS_USERNAME and COPERNICUS_PASSWORD in .env"
        )
    log.info("Copernicus auth ready for user=%s", mask(s.username))
    return s.username, s.password  # type: ignore[return-value]


def fetch_token() -> str:
    """Fetch an OAuth2 access token from CDSE using client-credentials flow."""
    import httpx

    s = get_settings().copernicus
    if not s.has_credentials():
        raise RuntimeError("Copernicus credentials missing in .env")
    resp = httpx.post(
        s.token_url,
        data={
            "grant_type": "password",
            "username": s.username,
            "password": s.password,
            "client_id": "cdse-public",
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def download_scene(scene_id: str, out_dir: Path) -> Path:
    """Download a Sentinel-1 scene using the CDSE API. Returns the local path."""
    raise NotImplementedError