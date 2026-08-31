"""Centralised application settings loaded from .env.

All secrets and external service credentials are read from environment variables
populated by the .env file (see .env.example for the schema). This module is the
single point of access — never read os.environ directly elsewhere.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env from the project root if it exists.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_PROJECT_ROOT / ".env", override=False)
load_dotenv(_PROJECT_ROOT / ".env.example", override=False)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DATABASE_", extra="ignore")

    url: str = "postgresql://oorca:oorca@localhost:5432/oorca"
    pool_size: int = 10
    ssl_mode: str | None = None
    sslrootcert: str | None = None


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")

    url: str = "redis://localhost:6379/0"
    password: str | None = None


class ObjectStorageSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="S3_", extra="ignore")

    endpoint: str = "http://localhost:9000"
    access_key: str = ""
    secret_key: str = ""
    bucket_raw: str = "oorca-raw"
    bucket_processed: str = "oorca-processed"
    sse_kms_key_id: str | None = None


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JWT_", extra="ignore")

    secret: str = Field(default="", min_length=32)
    algorithm: Literal["HS256", "HS384", "HS512", "RS256"] = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7


class CopernicusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="COPERNICUS_", extra="ignore")

    username: str | None = None
    password: str | None = None
    cdse_s3_key: str | None = None
    cdse_s3_secret: str | None = None
    cdse_endpoint: str = "https://dataspace.dataspace.copernicus.eu"
    token_url: str = (
        "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    )

    def has_credentials(self) -> bool:
        return bool(self.username and self.password)


class AISSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AIS", extra="ignore")

    hub_api_key: str | None = None
    marinetraffic_api_key: str | None = None
    unistratis_api_key: str | None = None
    vesselfinder_api_key: str | None = None
    spaceoffshore_api_key: str | None = None
    aisstream_api_key: str | None = None

    def available_providers(self) -> list[str]:
        return [p for p, k in {
            "ais_hub": self.hub_api_key,
            "marinetraffic": self.marinetraffic_api_key,
            "unistratis": self.unistratis_api_key,
            "vesselfinder": self.vesselfinder_api_key,
            "spaceoffshore": self.spaceoffshore_api_key,
            "aisstream": self.aisstream_api_key,
        }.items() if k]


class MetoceanSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ecmwf_api_key: str | None = None
    ecmwf_api_url: str = "https://api.ecmwf.int/v1"
    cmems_username: str | None = None
    cmems_password: str | None = None
    noaa_ncep_api_key: str | None = None
    openweather_api_key: str | None = None


class ESISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="NOAA_ESI_", extra="ignore")

    api_key: str | None = None


class ExternalServicesSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    sendgrid_api_key: str | None = None
    slack_webhook_url: str | None = None
    pagerduty_integration_key: str | None = None
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    sentry_dsn: str | None = None
    otel_exporter_otlp_endpoint: str | None = None
    otel_exporter_otlp_headers: str | None = None


class ModelRegistrySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_tracking_username: str | None = None
    mlflow_tracking_password: str | None = None
    huggingface_token: str | None = None
    model_registry_url: str | None = None


class FeatureFlags(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ENABLE_", extra="ignore")

    forecast: bool = True
    hindcast: bool = True
    liability_mc: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_name: str = "OORCA"
    log_level: str = "INFO"
    secret_key: str = ""

    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    storage: ObjectStorageSettings = ObjectStorageSettings()
    jwt: JWTSettings = JWTSettings()
    copernicus: CopernicusSettings = CopernicusSettings()
    ais: AISSettings = AISSettings()
    metocean: MetoceanSettings = MetoceanSettings()
    esi: ESISettings = ESISettings()
    external: ExternalServicesSettings = ExternalServicesSettings()
    model_registry: ModelRegistrySettings = ModelRegistrySettings()
    features: FeatureFlags = FeatureFlags()

    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    cors_allow_origins: list[str] = ["http://localhost:3000"]
    trusted_proxies: list[str] = ["127.0.0.1"]

    liability_mc_default_iterations: int = 1000
    opendrift_offline_mode: bool = False
    opendrift_cache_dir: str = "/var/cache/opendrift"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


__all__ = [
    "Settings",
    "get_settings",
    "DatabaseSettings",
    "RedisSettings",
    "ObjectStorageSettings",
    "JWTSettings",
    "CopernicusSettings",
    "AISSettings",
    "MetoceanSettings",
    "ESISettings",
    "ExternalServicesSettings",
    "ModelRegistrySettings",
    "FeatureFlags",
]