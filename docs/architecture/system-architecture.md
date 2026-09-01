# System Architecture (Phase 1)

OORCA Phase 1 is an **Oil Spill Simulator & Ecological Impact Analysis System** with a clean separation between frontend, backend, and analytical engines.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACE                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  React + TypeScript + Vite + Tailwind CSS + MapLibre GL JS         │   │
│  │  ┌─────────┐  ┌──────────────┐  ┌─────────────────────────────┐  │   │
│  │  │ Input   │  │ Map View     │  │ Bottom Dashboard (4 panels) │  │   │
│  │  │ Panel   │  │ (Spill + ESI │  │ • Spill Summary             │  │   │
│  │  │         │  │  + Shoreline)│  │ • Danger Assessment         │  │   │
│  │  │         │  │ + Timeline   │  │ • Ecological Resources      │  │   │
│  │  └─────────┘  └──────────────┘  │ • Shoreline Impact          │  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬─────────────────────────────────────────┘
                              │ HTTPS / REST API
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND API (FastAPI)                             │
│  ┌─────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │ Incidents   │  │ Simulation       │  │ Damage Assessment            │  │
│  │ Router      │  │ Router           │  │ Router                       │  │
│  └──────┬──────┘  └────────┬─────────┘  └──────────────┬───────────────┘  │
│         │                  │                          │                  │
│         ▼                  ▼                          ▼                  │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    SERVICE LAYER                                 │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐  │   │
│  │  │ IncidentService│  │SimulationService│ │ DamageService    │  │   │
│  │  └────────────────┘  └───────┬────────┘  └────────┬─────────┘  │   │
│  │                              │                      │           │   │
│  └──────────────────────────────┼──────────────────────┼───────────┘   │
│                                 │                      │               │
└─────────────────────────────────┼──────────────────────┼───────────────┘
                                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ANALYTICAL ENGINES                                   │
│  ┌─────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │ Simulation Engine       │  │ Damage Engine                          │  │
│  │ ┌─────────────────────┐ │  │ ┌──────────────┐ ┌────────────────┐   │  │
│  │ │ SpillSimulationProvider (ABC)     │  │ ESI Loader      │ │ Hazard Scoring│ │  │
│  │ │  ┌───────────────┐  │  │  │ └──────────────┘ └────────────────┘   │  │
│  │ │  │ MockProvider  │  │  │  │ ┌──────────────┐ ┌────────────────┐   │  │
│  │ │  │ (GeoJSON)     │  │  │  │ │ Spatial      │ │ Sensitivity    │   │  │
│  │ │  └───────────────┘  │  │  │ │ Intersection │ │ Analysis       │   │  │
│  │ │  ┌───────────────┐  │  │  │ └──────────────┘ └────────────────┘   │  │
│  │ │  │ OpenDrift     │  │  │  │ ┌──────────────┐ ┌────────────────┐   │  │
│  │ │  │ Provider      │  │  │  │ │ Exposure     │ │ Shoreline      │   │  │
│  │ │  │ (Future)      │  │  │  │ │ Calculation  │ │ Impact         │   │  │
│  │ │  └───────────────┘  │  │  │ └──────────────┘ └────────────────┘   │  │
│  │ └─────────────────────┘  │  └────────────────────────────────────────┘  │
│  └─────────────────────────┘                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │                      │
                    ┌─────────────┴─────────────┐        │
                    ▼                           ▼        ▼
             ┌─────────────┐            ┌─────────────┐ ┌─────────┐
             │ PostgreSQL  │            │ Redis       │ │ MinIO   │
             │ + PostGIS   │            │ (Queue/Cache)│ │ (S3)    │
             └─────────────┘            └─────────────┘ └─────────┘
```

## Data Flow

### 1. Incident Creation → Simulation
```
User Input (Location, Spill, Vessel)
        │
        ▼
POST /api/incidents → IncidentService.create_incident()
        │
        ▼
POST /api/incidents/{id}/simulate → IncidentService.run_simulation()
        │
        ▼
POST /api/simulation/run → SimulationService.run_simulation()
        │
        ▼
SpillSimulationProvider.run_simulation(SimulationParams)
        │
        ├── MockProvider: Load pre-generated GeoJSON frames
        └── OpenDriftProvider: Run OpenDrift physics (future)
        │
        ▼
SimulationResult → Store frames in DB → Return simulation_run_id
```

### 2. Simulation Progress Polling
```
Frontend: GET /api/simulation/runs/{id}/status (every 1s)
        │
        ▼
SimulationService.get_status() → SimulationStatus
        │
        ▼
Frontend updates progress bar & step indicators
```

### 3. Frame Loading & Map Rendering
```
Frontend: GET /api/simulation/runs/{id}/frames/{index}
        │
        ▼
SimulationService.get_frame() → SpillFrame (GeoJSON)
        │
        ▼
MapLibre GL: Update 'spill' source → Re-render concentration polygons
        │
        ▼
Timeline slider → frame index → Map updates
```

### 4. Damage Assessment
```
POST /api/damage/assess → DamageService.assess_damage()
        │
        ▼
Load ESI features (from DB or GeoJSON)
        │
        ▼
Spatial Intersection (Shapely/PostGIS)
        │
        ▼
Exposure Calculation (Area × Concentration)
        │
        ▼
Sensitivity Weighting (ESI Score × Resource Type Multiplier)
        │
        ▼
Hazard Zone Classification
        │
        ▼
Hazard Score (0-100) + Component Scores
        │
        ▼
DamageAssessment → Store in DB → Return to Frontend
```

## Component Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Frontend** | User interaction, map visualization, state management, API communication |
| **API Routes** | HTTP handling, validation, serialization, error responses |
| **Services** | Business logic, orchestration, data transformation |
| **Simulation Provider** | Abstract interface for spill modeling (Mock, OpenDrift) |
| **Damage Engine** | Pure spatial analysis functions (testable, no I/O) |
| **Database** | Persistence of incidents, simulations, assessments, ESI features |

## Extension Points for Future Phases

| Phase | Extension Point | Location |
|-------|-----------------|----------|
| 2 | AIS Ingestion | `engine/ais/`, `backend/workers/ais_worker.py` |
| 2 | SAR Detection | `engine/sar/`, `backend/workers/sar_worker.py` |
| 2 | Vessel Attribution | `engine/attribution/`, `backend/services/attribution_service.py` |
| 2 | OpenDrift Integration | `engine/simulation/opendrift_runner.py` |
| 2 | Satellite Catalog | `engine/satellite/`, `backend/api/routes/satellite.py` |
| 3 | NRDA Modeling | `engine/liability/`, `backend/services/liability_service.py` |
| 3 | Monte Carlo Uncertainty | `engine/liability/monte_carlo.py` |

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend API | FastAPI, Pydantic, SQLAlchemy, GeoAlchemy2 |
| Simulation | Abstract provider pattern, OpenDrift-ready |
| Damage Engine | Shapely, GeoPandas, PyProj, NumPy |
| Database | PostgreSQL 16 + PostGIS 3.4 |
| Queue/Cache | Redis 7 |
| Object Storage | MinIO (S3-compatible) |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Map | MapLibre GL JS 4.7 |
| Charts | Recharts |
| Icons | Lucide React |

## Security

- JWT-based authentication (configured, not yet enforced)
- Role-based access control (viewer/analyst/admin)
- Secrets via `.env` (gitignored)
- CORS restricted to configured origins
- Input validation via Pydantic schemas

## Observability

- Structured logging (JSON-ready)
- Health endpoint: `GET /health`
- Simulation status polling for progress tracking
- Error tracking via Sentry (configured, optional)