-- Helper SQL functions.
-- Example: aggregate spill footprint area by ESI class.

CREATE OR REPLACE FUNCTION geo.footprint_area_km2(geom geometry)
RETURNS double precision AS $$
    SELECT ST_Area(geography(geom)) / 1e6;
$$ LANGUAGE SQL IMMUTABLE;