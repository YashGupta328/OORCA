# System Architecture

OORCA is built as a layered system that ingests heterogeneous ocean observation and vessel tracking data, processes them through a chain of analytics engines, and exposes results through a REST API and web dashboard.

## Layers

1. **Data sources** — Sentinel-1 SAR, AIS, metocean reanalysis/forecast, ESI sensitivity rasters.
2. **Ingestion layer** — `scripts/ingest_*` and worker jobs push raw data into object storage and the PostGIS database.
3. **Analytics engines** (`engine/`) — domain logic: SAR detection, AIS cleaning, drift simulation, attribution, ecology, liability.
4. **Service layer** (`backend/services/`) — orchestrates engines and persists results.
5. **API layer** (`backend/api/`) — FastAPI surface for queries, investigations and report generation.
6. **Workers** (`backend/workers/`) — Celery tasks for asynchronous, long-running pipelines.
7. **Frontend** (`frontend/`) — operator dashboard, map visualisations, investigation workflow, liability reports.

## Cross-cutting

- **Configuration** — environment-specific YAML under `config/` loaded via `backend/core/config.py`.
- **Security** — JWT auth, role-based access, secret handling in `backend/core/security.py`.
- **Observability** — structured logging (`backend/core/logging.py`), metrics, traces.

See `data-flow.md`, `database-architecture.md` and `security-model.md` for details.