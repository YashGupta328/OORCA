# AIS Attribution

Given a spill detection, rank candidate source vessels using four signals.

## Candidate Generation (`engine/attribution/candidate_generation.py`)

- Pull AIS positions in a temporal window around the detection (default ±6 h).
- Apply spatial filter to a buffer around the detection polygon (default 50 km).
- Keep vessels with valid MMSI, type and recent positions.

## Scoring

Each candidate is evaluated on four axes and combined into a composite score.

| Signal   | File                                      | Description                                            |
|----------|-------------------------------------------|--------------------------------------------------------|
| Temporal | `engine/attribution/temporal_score.py`    | Closeness of last contact to spill time.                |
| Spatial  | `engine/attribution/spatial_score.py`     | Distance from last position to detection centroid.     |
| Drift    | `engine/attribution/drift_score.py`       | Likelihood that drift could connect vessel to spill.    |
| Vessel   | `engine/attribution/vessel_score.py`      | Prior (tanker, size, history, sanctions).              |

## Ranking (`engine/attribution/ranking.py`)

Weights are configurable per investigation. Output: ordered list with per-signal and composite scores plus confidence intervals from a lightweight ensemble.