"""Ingest AIS messages from configured providers."""

from __future__ import annotations

import logging
import sys

from backend.core.settings import get_settings

log = logging.getLogger(__name__)


def main() -> int:
    logging.basicConfig(level=get_settings().log_level)
    if len(sys.argv) < 2:
        print("usage: ingest_ais.py <source>", file=sys.stderr)
        return 2
    source = sys.argv[1]
    providers = get_settings().ais.available_providers()
    if not providers:
        log.error("No AIS providers configured in .env")
        return 1
    log.info("Ingesting AIS from %s using providers=%s", source, providers)
    raise NotImplementedError
    return 0


if __name__ == "__main__":
    raise SystemExit(main())