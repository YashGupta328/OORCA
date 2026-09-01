-- Phase 1 Database Schema
-- Core tables for Oil Spill Simulator

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Incidents table - core domain object
CREATE TABLE incidents (
    incident_id VARCHAR(50) PRIMARY KEY,
    location_lat DOUBLE PRECISION NOT NULL,
    location_lon DOUBLE PRECISION NOT NULL,
    location_geom GEOMETRY(POINT, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(location_lon, location_lat), 4326)) STORED,
    
    spill_amount DOUBLE PRECISION NOT NULL,
    spill_unit VARCHAR(20) NOT NULL DEFAULT 'tonnes',
    spill_oil_type VARCHAR(30) NOT NULL DEFAULT 'crude_oil',
    spill_start_time TIMESTAMPTZ NOT NULL,
    spill_duration_hours INTEGER NOT NULL,
    
    vessel_name VARCHAR(100),
    vessel_type VARCHAR(30),
    vessel_imo VARCHAR(20),
    vessel_length_m DOUBLE PRECISION,
    vessel_breadth_m DOUBLE PRECISION,
    vessel_draft_m DOUBLE PRECISION,
    vessel_heading_deg DOUBLE PRECISION,
    
    status VARCHAR(20) NOT NULL DEFAULT 'created',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
CREATE INDEX idx_incidents_location ON incidents USING GIST(location_geom);

-- Simulation runs table
CREATE TABLE simulation_runs (
    simulation_run_id VARCHAR(64) PRIMARY KEY,
    incident_id VARCHAR(50) NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
    provider VARCHAR(30) NOT NULL DEFAULT 'mock',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    error TEXT,
    
    -- Summary statistics
    total_frames INTEGER DEFAULT 0,
    slick_area_km2 DOUBLE PRECISION,
    weathering_percent DOUBLE PRECISION,
    evaporation_percent DOUBLE PRECISION,
    dispersion_percent DOUBLE PRECISION,
    remaining_oil_tonnes DOUBLE PRECISION
);

CREATE INDEX idx_simulation_runs_incident ON simulation_runs(incident_id);
CREATE INDEX idx_simulation_runs_status ON simulation_runs(status);

-- Simulation frames table (stores GeoJSON for each time step)
CREATE TABLE simulation_frames (
    id BIGSERIAL PRIMARY KEY,
    simulation_run_id VARCHAR(64) NOT NULL REFERENCES simulation_runs(simulation_run_id) ON DELETE CASCADE,
    time_hours INTEGER NOT NULL,
    frame_geojson JSONB NOT NULL,
    mass_balance JSONB,
    wind_data JSONB,
    current_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_simulation_frames_run_time ON simulation_frames(simulation_run_id, time_hours);

-- ESI features table (cached from GeoJSON)
CREATE TABLE esi_features (
    esi_id VARCHAR(50) PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_name VARCHAR(100) NOT NULL,
    sensitivity_score INTEGER NOT NULL CHECK (sensitivity_score >= 0 AND sensitivity_score <= 100),
    geometry GEOMETRY(GEOMETRY, 4326) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_esi_features_geom ON esi_features USING GIST(geometry);
CREATE INDEX idx_esi_features_type ON esi_features(resource_type);

-- Damage assessments table
CREATE TABLE damage_assessments (
    assessment_id VARCHAR(64) PRIMARY KEY,
    incident_id VARCHAR(50) NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
    simulation_run_id VARCHAR(64) NOT NULL REFERENCES simulation_runs(simulation_run_id) ON DELETE CASCADE,
    
    -- Spill summary
    total_spilled_tonnes DOUBLE PRECISION,
    estimated_slick_area_km2 DOUBLE PRECISION,
    simulation_duration_hours INTEGER,
    weathering_percent DOUBLE PRECISION,
    evaporation_percent DOUBLE PRECISION,
    dispersion_percent DOUBLE PRECISION,
    remaining_surface_oil_tonnes DOUBLE PRECISION,
    
    -- Danger assessment
    overall_risk VARCHAR(20),
    environmental_risk VARCHAR(20),
    shoreline_risk VARCHAR(20),
    human_exposure_risk VARCHAR(20),
    cleanup_difficulty VARCHAR(20),
    hazard_score DOUBLE PRECISION,
    
    calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_damage_assessments_incident ON damage_assessments(incident_id);
CREATE INDEX idx_damage_assessments_simulation ON damage_assessments(simulation_run_id);

-- Ecological resources affected (junction table for damage assessment)
CREATE TABLE damage_ecological_resources (
    id BIGSERIAL PRIMARY KEY,
    assessment_id VARCHAR(64) NOT NULL REFERENCES damage_assessments(assessment_id) ON DELETE CASCADE,
    esi_id VARCHAR(50) NOT NULL REFERENCES esi_features(esi_id),
    affected_area_km2 DOUBLE PRECISION,
    affected_percentage DOUBLE PRECISION,
    risk_level VARCHAR(20),
    intersection_geometry GEOMETRY(GEOMETRY, 4326),
    max_concentration VARCHAR(20)
);

CREATE INDEX idx_damage_eco_assessment ON damage_ecological_resources(assessment_id);
CREATE INDEX idx_damage_eco_esi ON damage_ecological_resources(esi_id);

-- Shoreline impacts
CREATE TABLE shoreline_impacts (
    id BIGSERIAL PRIMARY KEY,
    assessment_id VARCHAR(64) NOT NULL REFERENCES damage_assessments(assessment_id) ON DELETE CASCADE,
    location_name VARCHAR(100) NOT NULL,
    arrival_time_min_hours INTEGER,
    arrival_time_max_hours INTEGER,
    impact_level VARCHAR(20),
    distance_km DOUBLE PRECISION,
    coordinates GEOMETRY(POINT, 4326)
);

CREATE INDEX idx_shoreline_assessment ON shoreline_impacts(assessment_id);

-- Satellite evidence requests (placeholder for Phase 2)
CREATE TABLE satellite_evidence_requests (
    id BIGSERIAL PRIMARY KEY,
    incident_id VARCHAR(50) NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
    provider VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'requested',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fulfilled_at TIMESTAMPTZ,
    scene_ids TEXT[],
    metadata JSONB
);

CREATE INDEX idx_satellite_incident ON satellite_evidence_requests(incident_id);

COMMIT;