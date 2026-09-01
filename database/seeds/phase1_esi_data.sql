-- Phase 1 Reference Data Seed
-- ESI features for Mumbai/Arabian Sea region

BEGIN;

-- Clear existing data
DELETE FROM esi_features;

-- Insert ESI features
INSERT INTO esi_features (esi_id, resource_type, resource_name, sensitivity_score, geometry, metadata) VALUES
(
    'esi-mangrove-001',
    'mangrove',
    'Thane Creek Mangroves',
    95,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.95 19.15, 73.05 19.15, 73.05 19.25, 72.95 19.25, 72.95 19.15))'), 4326),
    '{"area_km2": 12.5, "dominant_species": "Avicennia marina", "conservation_status": "Protected"}'::jsonb
),
(
    'esi-mangrove-002',
    'mangrove',
    'Vasai Creek Mangroves',
    90,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.80 19.30, 72.90 19.30, 72.90 19.40, 72.80 19.40, 72.80 19.30))'), 4326),
    '{"area_km2": 8.3, "dominant_species": "Rhizophora mucronata", "conservation_status": "Reserved Forest"}'::jsonb
),
(
    'esi-coral-001',
    'coral_reef',
    'Angria Bank Coral Reef',
    98,
    ST_SetSRID(ST_GeomFromText('POLYGON((73.10 16.80, 73.30 16.80, 73.30 17.00, 73.10 17.00, 73.10 16.80))'), 4326),
    '{"area_km2": 45.2, "depth_range_m": "10-25", "conservation_status": "Marine Protected Area"}'::jsonb
),
(
    'esi-seagrass-001',
    'seagrass',
    'Malvan Seagrass Meadows',
    85,
    ST_SetSRID(ST_GeomFromText('POLYGON((73.40 16.10, 73.55 16.10, 73.55 16.25, 73.40 16.25, 73.40 16.10))'), 4326),
    '{"area_km2": 22.7, "dominant_species": "Halophila ovalis", "conservation_status": "Ecologically Sensitive Area"}'::jsonb
),
(
    'esi-fish-001',
    'fish_habitat',
    'Mumbai Offshore Fisheries Zone',
    75,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.70 18.80, 73.00 18.80, 73.00 19.20, 72.70 19.20, 72.70 18.80))'), 4326),
    '{"area_km2": 185.4, "key_species": ["Bombay duck", "Pomfret", "Mackerel", "Shrimp"], "fishing_intensity": "High"}'::jsonb
),
(
    'esi-fish-002',
    'fish_habitat',
    'Alibaug Coastal Fisheries',
    70,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.85 18.50, 73.00 18.50, 73.00 18.80, 72.85 18.80, 72.85 18.50))'), 4326),
    '{"area_km2": 92.1, "key_species": ["Sardine", "Anchovy", "Crab"], "fishing_intensity": "Medium"}'::jsonb
),
(
    'esi-turtle-001',
    'sea_turtle_habitat',
    'Velas Turtle Nesting Beach',
    92,
    ST_SetSRID(ST_GeomFromText('POLYGON((73.05 17.85, 73.10 17.85, 73.10 17.95, 73.05 17.95, 73.05 17.85))'), 4326),
    '{"area_km2": 2.1, "species": "Olive Ridley", "nesting_season": "Nov-Mar", "conservation_status": "Critically Important"}'::jsonb
),
(
    'esi-dolphin-001',
    'dolphin_habitat',
    'Sindhudurg Dolphin Sanctuary',
    88,
    ST_SetSRID(ST_GeomFromText('POLYGON((73.30 15.90, 73.50 15.90, 73.50 16.10, 73.30 16.10, 73.30 15.90))'), 4326),
    '{"area_km2": 58.3, "species": "Indian Ocean Humpback Dolphin", "conservation_status": "Sanctuary"}'::jsonb
),
(
    'esi-protected-001',
    'protected_area',
    'Sanjay Gandhi National Park (Coastal Zone)',
    80,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.85 19.15, 72.95 19.15, 72.95 19.25, 72.85 19.25, 72.85 19.15))'), 4326),
    '{"area_km2": 15.6, "designation": "National Park", "iucn_category": "II"}'::jsonb
),
(
    'esi-protected-002',
    'protected_area',
    'Mahim Creek Bird Sanctuary',
    82,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.83 19.03, 72.87 19.03, 72.87 19.07, 72.83 19.07, 72.83 19.03))'), 4326),
    '{"area_km2": 1.8, "key_species": ["Flamingo", "Heron", "Sandpiper"], "designation": "Bird Sanctuary"}'::jsonb
),
(
    'esi-saltmarsh-001',
    'saltmarsh',
    'Uran Saltmarshes',
    78,
    ST_SetSRID(ST_GeomFromText('POLYGON((72.92 18.95, 73.00 18.95, 73.00 19.05, 72.92 19.05, 72.92 18.95))'), 4326),
    '{"area_km2": 6.4, "dominant_species": "Suaeda fruticosa", "conservation_status": "Wetland"}'::jsonb
);

COMMIT;