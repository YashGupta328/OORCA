-- Initial database schema placeholder.
-- Real migrations live in this directory, applied in order by the migration runner.

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;

-- See subsequent migration files for tables: raw_ais_messages, sar_scenes,
-- detections, vessel_positions, drift_particles, esi_zones, attribution_scores,
-- liability_reports.

COMMIT;