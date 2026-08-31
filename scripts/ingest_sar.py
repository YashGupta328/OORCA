"""Ingest Sentinel-1 SAR scenes from Copernicus (CDSE)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from backend.core.settings import get_settings
from engine.sar.copernicus import authenticate, download_scene

log = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=get_settings().log_level)
    if len(sys.argv) < 3:
        print("usage: ingest_sar.py <scene_id> <out_dir>", file=sys.stderr)
        return 2
    scene_id, out_dir = sys.argv[1], Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    authenticate()
    path = download_scene(scene_id, out_dir)
    log.info("Downloaded %s -> %s", scene_id, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())