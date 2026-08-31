# Database Architecture

PostgreSQL 16 with PostGIS 3.4 is the system of record.

## Schemas

- `raw` — unprocessed ingested payloads (AIS messages, SAR scene metadata).
- `staging` — normalised but non-spatial tables.
- `geo` — spatial tables (`detections`, `vessel_positions`, `drift_particles`, `esi_zones`) with geometry/geometry columns.
- `analytics` — derived tables (attribution scores, liability estimates, exposure scores).
- `audit` — append-only operational audit log.

## Conventions

- All spatial tables use SRID 4326 unless noted.
- Timestamps are stored as `timestamptz` in UTC.
- Partitioning on time-series tables by month.
- Row-Level Security (RLS) on investigation-scoped tables.

## Migrations

SQL migrations live in `database/migrations/` and are applied by Alembic or a lightweight runner. Helper functions (e.g. spill footprint aggregation) live in `database/functions/` and views in `database/views/`.