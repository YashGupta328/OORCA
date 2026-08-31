"""Object storage (S3 / MinIO) client built on boto3.

Credentials are loaded from .env via the application settings; nothing is
hard-coded in this module.
"""

from __future__ import annotations

import logging

import boto3
from botocore.client import Config

from backend.core.security import mask
from backend.core.settings import get_settings

log = logging.getLogger(__name__)


def get_client():
    s = get_settings().storage
    if not s.access_key or not s.secret_key:
        raise RuntimeError("S3 credentials missing: set S3_ACCESS_KEY and S3_SECRET_KEY in .env")
    log.debug("S3 endpoint=%s key=%s", s.endpoint, mask(s.access_key))
    return boto3.client(
        "s3",
        endpoint_url=s.endpoint,
        aws_access_key_id=s.access_key,
        aws_secret_access_key=s.secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def download(bucket: str, key: str, dest_path: str) -> str:
    client = get_client()
    client.download_file(bucket, key, dest_path)
    return dest_path


def upload(bucket: str, key: str, src_path: str) -> str:
    client = get_client()
    client.upload_file(src_path, bucket, key)
    return f"s3://{bucket}/{key}"