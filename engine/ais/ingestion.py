"""AIS message ingestion from various sources."""

from __future__ import annotations


def ingest(source: str) -> list[dict]:
    """Read AIS messages from `source` (file path, API, stream)."""
    raise NotImplementedError