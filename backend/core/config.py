"""Application settings loaded from environment + YAML config."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel


def _config_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "config"


@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    env = os.getenv("APP_ENV", "development")
    config_path = _config_dir() / f"{env}.yaml"
    data: dict = {}
    if config_path.exists():
        data = yaml.safe_load(config_path.read_text()) or {}
    return Settings(env=env, raw=data)


class Settings(BaseModel):
    env: str = "development"
    raw: dict = {}