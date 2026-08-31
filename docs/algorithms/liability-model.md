# Liability Model

Probabilistic estimate of total damages and compensation.

## Components

| Module                                | Purpose                                                   |
|---------------------------------------|-----------------------------------------------------------|
| `engine/liability/volume.py`          | Estimate spilled volume (area × thickness, weather-corrected). |
| `engine/liability/cleanup.py`         | Response and clean-up costs.                              |
| `engine/liability/restoration.py`     | Habitat restoration costs (NRD-type).                     |
| `engine/liability/fisheries.py`       | Lost revenue to commercial fisheries.                     |
| `engine/liability/tourism.py`         | Lost revenue to coastal tourism.                          |
| `engine/liability/ecological.py`      | Non-use / passive-use ecological value.                   |
| `engine/liability/discounting.py`     | Discounting for time-distributed losses.                  |
| `engine/liability/monte_carlo.py`     | Joint Monte Carlo simulation over uncertain inputs.       |
| `engine/liability/calculator.py`      | Orchestrates components and produces final report.         |

## Outputs

- Total damages (point estimate + 5/50/95 percentiles).
- Per-component breakdown.
- Sensitivity tornado.