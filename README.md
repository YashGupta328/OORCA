# OORCA — Phase 1: Oil Spill Simulator & Ecological Impact Analysis

OORCA (Ocean Oil Reconnaissance, Correlation & Attribution) is a marine environmental intelligence platform. This repository contains the **Phase 1** implementation: an **Oil Spill Simulator with Ecological Impact Analysis**.

## Phase 1 Capabilities

- **Oil Spill Simulation** — Forward trajectory modeling with wind/current forcing
- **Interactive Map Visualization** — MapLibre GL JS with concentration fields, particle trajectories, vessel position
- **Timeline Animation** — Play through spill evolution at 0, 12, 24, 36, 48, 60, 72 hours
- **Ecological Sensitivity Index (ESI) Analysis** — Spatial intersection of spill footprint with mangroves, coral reefs, seagrass, fish habitats, turtle nesting beaches, dolphin sanctuaries, protected areas
- **Hazard Scoring** — Baseline Ecological Hazard Score (0-100) with component breakdown
- **Shoreline Impact Prediction** — Arrival time and impact level for coastal locations
- **Satellite Evidence Request** — Placeholder for Phase 2 integration (Copernicus, BHOONIDHI)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + TS)                    │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Input Panel │  │   Map View   │  │  Bottom Dashboard    │  │
│  │  Location   │  │  MapLibre GL │  │  Spill Summary       │  │
│  │  Spill      │  │  Layers      │  │  Danger Assessment   │  │
│  │  Vessel     │  │  Timeline    │  │  Eco Resources       │  │
│  └─────────────┘  └──────────────┘  │  Shoreline Impact    │  │
│                                     └──────────────────────┘  │
└─────────────────────────┬─────────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼─────────────────────────────────────┐
│                      BACKEND (FastAPI)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Incidents   │  │ Simulation   │  │ Damage Assessment    │  │
│  │   API       │  │   Service    │  │   Service            │  │
│  └─────────────┘  └──────────────┘  └──────────────────────┘  │
│         │                │                     │               │
│         ▼                ▼                     ▼               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              SIMULATION PROVIDER ABSTRACTION             │  │
│  │  ┌─────────────────┐    ┌────────────────────────────┐  │  │
│  │  │ Mock Provider   │    │ OpenDrift Provider (Phase 2)│  │  │
│  │  │ (GeoJSON frames)│    │ (Real physics)             │  │  │
│  │  └─────────────────┘    └────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                          │                     │               │
└──────────────────────────┼─────────────────────┼───────────────┘
                           │                     │
                    ┌──────▼──────┐       ┌──────▼──────┐
                    │  PostgreSQL │       │   Redis     │
                    │  + PostGIS  │       │   (Queue)   │
                    └─────────────┘       └─────────────┘
```

## Quickstart

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)

### Start with Docker

```bash
# Clone
git clone https://github.com/YashGupta328/OORCA.git
cd OORCA

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker compose up -d

# Run database migrations
docker compose exec api python -m alembic upgrade head

# Seed ESI data
docker compose exec postgres psql -U oorca -d oorca -f /app/database/seeds/phase1_esi_data.sql
```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Development Setup

**Backend:**
```bash
cd OORCA
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Start PostgreSQL + Redis (via Docker or locally)
uvicorn backend.api.main:app --reload
```

**Frontend:**
```bash
cd OORCA/frontend
npm install
npm run dev
```

## API Endpoints

### Incidents
- `POST /api/incidents` — Create new incident
- `GET /api/incidents` — List incidents
- `GET /api/incidents/{id}` — Get incident
- `POST /api/incidents/{id}/simulate` — Start simulation
- `POST /api/incidents/{id}/damage` — Calculate damage
- `POST /api/incidents/{id}/satellite-evidence` — Request satellite imagery

### Simulation
- `POST /api/simulation/run` — Run simulation
- `GET /api/simulation/runs/{id}` — Get simulation run
- `GET /api/simulation/runs/{id}/status` — Get real-time status
- `GET /api/simulation/runs/{id}/frames/{index}` — Get frame GeoJSON
- `GET /api/simulation/runs/{id}/wind-current/{index}` — Get wind/current data

### Damage
- `POST /api/damage/assess` — Assess damage for simulation run
- `GET /api/damage/assessments/{id}` — Get damage assessment

## Simulation Provider Abstraction

The simulation engine uses a provider pattern for extensibility:

```python
from backend.services.simulation_service import SpillSimulationProvider, get_simulation_provider

# Use mock provider (default)
provider = get_simulation_provider("mock")
result = await provider.run_simulation(params)

# Future: OpenDrift provider
# provider = get_simulation_provider("opendrift")
```

### Mock Provider

The mock provider returns pre-generated GeoJSON frames from `data/simulation_frames/`:
- `0h.geojson`, `12h.geojson`, `24h.geojson`, `36h.geojson`, `48h.geojson`, `60h.geojson`, `72h.geojson`

Each frame contains:
- Concentration polygons (LOW, MEDIUM, HIGH, VERY_HIGH)
- Release point marker
- Vessel position

### OpenDrift Provider (Future)

The `engine/simulation/` module contains interfaces for OpenDrift integration:
- `opendrift_runner.py` — OpenDrift model runner
- `spill_model.py` — Oil type properties and weathering
- `particles.py` — Particle array management
- `metocean.py` — Wind/current forcing (CMEMS, ERA5, GFS)
- `weathering.py` — Evaporation, dispersion, emulsification
- `trajectory.py` — Particle advection
- `output.py` — GeoJSON frame generation

## Damage Engine

The damage engine computes ecological impact:

```
Predicted Slick (GeoJSON)
        ↓
ESI Spatial Intersection (PostGIS / Shapely)
        ↓
Exposure = Area × Concentration Weight
        ↓
Sensitivity = Exposure × ESI Score × Resource Type Multiplier
        ↓
Hazard Zones (grouped by severity)
        ↓
Baseline Ecological Hazard Score (0-100)
```

### Risk Levels
- **LOW** (0-25)
- **MEDIUM** (25-50)
- **HIGH** (50-75)
- **VERY_HIGH** (75-100)

> **Important**: The hazard score is a *Baseline Ecological Hazard Score* for screening purposes only. It is NOT a legally valid environmental damage or financial liability calculation.

## ESI Data

Mock ESI data for the Mumbai/Arabian Sea region is included:
- **Mangroves**: Thane Creek, Vasai Creek
- **Coral Reefs**: Angria Bank
- **Seagrass**: Malvan Meadows
- **Fish Habitats**: Mumbai Offshore, Alibaug Coastal
- **Sea Turtles**: Velas Nesting Beach
- **Dolphins**: Sindhudurg Sanctuary
- **Protected Areas**: Sanjay Gandhi NP, Mahim Creek
- **Saltmarshes**: Uran

Data is stored as GeoJSON in `data/esi_features.geojson` and as PostGIS in `database/seeds/phase1_esi_data.sql`.

## Configuration

Key environment variables (see `.env.example`):

```bash
# Database
DATABASE_URL=postgresql://oorca:oorca@localhost:5432/oorca

# Simulation
OPENDRIFT_OFFLINE_MODE=true  # Use mock when OpenDrift unavailable

# Frontend
CORS_ALLOW_ORIGINS=http://localhost:3000
```

## Testing

```bash
# Backend tests
pytest tests/ -v

# Frontend tests
cd frontend && npm test
```

## Project Structure

```
OORCA/
├── backend/
│   ├── api/           # FastAPI routes & schemas
│   ├── core/          # Config, security, settings
│   ├── services/      # Business logic (incident, simulation, damage)
│   └── workers/       # Celery workers (future)
├── engine/
│   ├── damage/        # ESI, exposure, sensitivity, hazard, scoring
│   ├── simulation/    # OpenDrift interfaces, models, output
│   └── sar/ais/...    # Phase 2+ modules (stubs)
├── frontend/
│   ├── src/
│   │   ├── app/           # App, routing
│   │   ├── components/    # UI components
│   │   ├── services/      # API clients
│   │   ├── mock/          # Development mock data
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Helpers
│   └── ...
├── database/
│   ├── migrations/    # SQL migrations
│   └── seeds/         # Reference data
├── data/
│   ├── esi_features.geojson
│   └── simulation_frames/
└── docs/
    └── architecture/
```

## Roadmap

| Phase | Focus |
|-------|-------|
| **1** | Oil Spill Simulator + Ecological Impact (THIS RELEASE) |
| 2 | AIS Ingestion, Vessel Attribution, SAR Detection |
| 3 | NRDA Injury Modeling, Financial Liability, Monte Carlo |

## License

MIT License — see [LICENSE](LICENSE)