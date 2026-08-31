# Hindcast Drift

Reconstructs the likely origin of a detected spill by running OpenDrift backwards in time.

## Process (`engine/drift/hindcast.py`)

1. Seed particles within the detection polygon at the detection timestamp.
2. Run `OpenDrift` (`engine/drift/opendrift_runner.py`) using metocean reanalysis winds and currents (ERA5 / CMEMS).
3. Advect backwards for a configurable window (default 48 h).
4. Aggregate particle endpoints to estimate the origin region.

## Weathering (`engine/drift/weathering.py`)

Tracks mass balance (evaporation, dispersion, emulsification) so that the effective spill volume at the detection time is recoverable.

## Outputs

- Origin probability heatmap (GeoJSON raster / vector).
- Most-likely release time and location.
- Estimated volume at sea at detection time.