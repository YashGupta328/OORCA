"""Lightweight YAML config loader (non-secret application tuning)."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

from backend.core.settings import get_settings


def _config_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "config"


@lru_cache(maxsize=1)
def get_yaml_config() -> dict:
    env = os.getenv("APP_ENV", get_settings().app_env)
    config_path = _config_dir() / f"{env}.yaml"
    if not config_path.exists():
        return {}
    return yaml.safe_load(config_path.read_text()) or {}


__all__ = ["get_yaml_config", "get_settings"]