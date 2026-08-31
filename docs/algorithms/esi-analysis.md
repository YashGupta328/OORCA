# ESI Analysis

Quantifies ecological sensitivity of areas exposed to oil.

## Stages

1. **Load** (`engine/ecology/esi_loader.py`) — read ESI rasters/polygons.
2. **Intersection** (`engine/ecology/spatial_intersection.py`) — overlay spill footprint(s) with ESI polygons.
3. **Exposure** (`engine/ecology/exposure.py`) — compute area exposed per ESI class, weighted by oiling probability.
4. **Sensitivity** (`engine/ecology/sensitivity.py`) — apply per-class sensitivity multipliers.
5. **Hazard zones** (`engine/ecology/hazard_zone.py`) — produce ranked hazard zones for response prioritisation.

## Outputs

Per-incident ecological exposure summary: total exposed area, breakdown by ESI class, top-N at-risk habitats.