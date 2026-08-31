# Secret Management

All secrets, API keys and credentials live in the local `.env` file at the
repository root. This file is **never committed** — it is listed in
`.gitignore`.

## Loading order

`backend/core/settings.py` loads `.env` once at import time via
`python-dotenv`. Settings are exposed through `get_settings()` and accessed
as typed Pydantic models (no raw `os.environ` reads elsewhere).

```
.env  →  backend.core.settings.Settings  →  backend.core.security  →  engines / services
```

## Generation

Generate strong placeholders before first run:

```bash
python scripts/generate_secrets.py --write
```

The script writes random 32-byte hex values for every `CHANGE_ME_*` placeholder.

## Rules

1. **Never commit `.env`.** CI must run with secrets injected by the runner.
2. **Never log secrets.** Use `backend.core.security.mask()` for diagnostics.
3. **Rotate immediately** if a value leaks. The old value stays in git history.
4. **Production** uses secret manager (Vault / AWS SM / GCP SM) and injects
   into the process env; `.env` is only used for local development.
5. **Database SSL** is enforced in production via `DATABASE_SSL_MODE=require`.

## Mapping of provider → env var

| Provider            | Env vars                                           |
|---------------------|----------------------------------------------------|
| Database            | `DATABASE_URL`, `DATABASE_SSL_MODE`                |
| Redis               | `REDIS_URL`, `REDIS_PASSWORD`                      |
| Object storage      | `S3_ACCESS_KEY`, `S3_SECRET_KEY`                   |
| Auth                | `JWT_SECRET`, `SECRET_KEY`                         |
| Copernicus (CDSE)   | `COPERNICUS_USERNAME`, `COPERNICUS_PASSWORD`       |
| MarineTraffic       | `MARINETRAFFIC_API_KEY`                            |
| AIS Hub             | `AIS_HUB_API_KEY`                                  |
| VesselFinder        | `VESSELFINDER_API_KEY`                             |
| Unistratis          | `UNISTRATIS_API_KEY`                               |
| SpaceOffshore       | `SPACEOFFSHORE_API_KEY`                            |
| AISStream           | `AISSTREAM_API_KEY`                                |
| ECMWF               | `ECMWF_API_KEY`                                    |
| CMEMS               | `CMEMS_USERNAME`, `CMEMS_PASSWORD`                 |
| NOAA NCEP           | `NOAA_NCEP_API_KEY`                                |
| OpenWeather         | `OPENWEATHER_API_KEY`                              |
| SendGrid            | `SENDGRID_API_KEY`                                 |
| Slack               | `SLACK_WEBHOOK_URL`                                |
| PagerDuty           | `PAGERDUTY_INTEGRATION_KEY`                        |
| Twilio              | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`          |
| Sentry              | `SENTRY_DSN`                                       |
| OTLP                | `OTEL_EXPORTER_OTLP_ENDPOINT`                      |
| MLflow              | `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD` |
| Hugging Face        | `HUGGINGFACE_TOKEN`                                |