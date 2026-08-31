# OORCA

**Ocean Oil Spill Response, Attribution & Compensation Analytics**

OORCA is an end-to-end platform for detecting marine oil spills from satellite SAR imagery, attributing them to likely source vessels using AIS data and ocean drift modeling, quantifying ecological and economic damages, and computing liability estimates.

---

## Capabilities

- **SAR Detection** — Automated oil spill detection from Sentinel-1 SAR imagery (preprocessing, segmentation, classification, postprocessing).
- **AIS Ingestion** — Vessel tracking data ingestion, cleaning, interpolation, trajectory reconstruction and filtering.
- **Drift Modeling** — Hindcast and forecast oil spill drift using OpenDrift with metocean forcing.
- **Attribution Engine** — Multi-signal candidate scoring (temporal, spatial, drift, vessel characteristics) to rank likely source vessels.
- **Ecology Analysis** — Intersection of spill footprints with ESI sensitivity maps to compute ecological exposure.
- **Liability Calculator** — Monte Carlo-based estimation of cleanup, restoration, fisheries, tourism and ecological damages.

---

## Repository Layout

```
oorca/
├── docs/            Architecture, algorithm and dataset documentation
├── config/          Environment-specific YAML configuration
├── data/            Raw, processed and sample data
├── models/          ML model weights and checkpoints
├── notebooks/       Jupyter exploration and demos
├── backend/         FastAPI service (api, services, workers, core)
├── engine/          Core analytics engines (sar, ais, attribution, drift, ecology, liability)
├── database/        SQL migrations, seeds, functions and views
├── tests/           Unit, integration and fixtures
├── frontend/        Web UI (React)
├── infrastructure/  Docker, Kubernetes, Terraform
└── scripts/         Operational scripts and pipeline runners
```

See `docs/architecture/system-architecture.md` for the full architecture overview.

---

## Quickstart

```bash
# Clone
git clone https://github.com/YashGupta328/OORCA.git
cd OORCA

# Configure environment
cp .env.example .env

# Bring up the stack
make up

# Run the API
make api
```

See `Makefile` for the full list of available targets.

---

## Documentation

- [Architecture](docs/architecture/system-architecture.md)
- [Algorithms](docs/algorithms/sar-detection.md)
- [Datasets](docs/datasets/sentinel1.md)

---

## License

See [LICENSE](LICENSE).