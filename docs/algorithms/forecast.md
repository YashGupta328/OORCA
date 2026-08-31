# Forecast Drift

Projects the future trajectory and footprint of a known or hypothetical release.

## Process (`engine/drift/forecast.py`)

1. Seed particles at release time/location (current detection or scenario).
2. Drive OpenDrift with forecast metocean fields (GFS / ECMWF / CMEMS forecast).
3. Run forward for the requested horizon (1–7 days).
4. Build probability contours (10/50/90%) and time-stamped footprints.

## Use Cases

- Response planning (where will the spill be in 24 h?).
- Ecological impact scoping (which ESI zones are threatened?).
- Liability anticipation (clean-up cost window).