-- Database views.

-- Recent detections enriched with scene metadata.
CREATE OR REPLACE VIEW analytics.v_recent_detections AS
SELECT d.id, d.observed_at, d.area_km2, d.confidence,
       s.scene_id, s.platform
FROM geo.detections d
JOIN raw.sar_scenes s ON s.id = d.scene_id
ORDER BY d.observed_at DESC;