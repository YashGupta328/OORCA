# Data Flow (Phase 1)

End-to-end data flow for the Oil Spill Simulator.

## 1. Incident Creation Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant IncidentService
    participant DB

    User->>Frontend: Fill form (Location, Spill, Vessel)
    Frontend->>API: POST /api/incidents
    API->>IncidentService: create_incident(IncidentCreate)
    IncidentService->>DB: INSERT incident
    DB-->>IncidentService: incident_id
    IncidentService-->>API: IncidentRead
    API-->>Frontend: 201 Created + Incident
    Frontend-->>User: Show incident created
```

**Data Structures:**
- Input: `IncidentCreate` (Location, SpillDetails, VesselDetails)
- Output: `IncidentRead` with generated `incident_id` (format: `ORCA-YYYYMMDD-XXXXXX`)

---

## 2. Simulation Execution Flow

```mermaid
sequenceDiagram
    participant Frontend
    participant API
    participant SimulationService
    participant Provider
    participant DB

    Frontend->>API: POST /api/incidents/{id}/simulate
    API->>SimulationService: run_simulation(incident_id, provider)
    SimulationService->>Provider: run_simulation(SimulationParams)
    
    alt Mock Provider
        Provider->>Provider: Load GeoJSON frames from disk
    else OpenDrift Provider (Future)
        Provider->>Provider: Initialize OpenDrift model
        Provider->>Provider: Fetch metocean forcing (CMEMS/ERA5)
        Provider->>Provider: Seed particles
        Provider->>Provider: Run advection + weathering
        Provider->>Provider: Generate concentration grids
    end
    
    Provider-->>SimulationService: SimulationResult (frames + metadata)
    SimulationService->>DB: INSERT simulation_run + frames
    SimulationService-->>API: simulation_run_id
    API-->>Frontend: {simulation_run_id, status: "started"}
    
    loop Poll every 1s
        Frontend->>API: GET /api/simulation/runs/{id}/status
        API->>SimulationService: get_status(simulation_run_id)
        SimulationService-->>API: SimulationStatus (progress, step)
        API-->>Frontend: status update
    end
```

**SimulationParams:**
```python
@dataclass
class SimulationParams:
    incident_id: str
    latitude: float
    longitude: float
    spill_amount: float
    spill_unit: str
    oil_type: str
    start_time: datetime
    duration_hours: int
    vessel_name: str | None
    vessel_type: str | None
    vessel_heading: float | None
```

**SimulationResult:**
```python
@dataclass
class SimulationResult:
    simulation_run_id: str
    frames: list[SimulationFrame]  # time_hours, geojson, wind_data, current_data
    completed_at: datetime
```

---

## 3. Frame Rendering Flow (Map)

```mermaid
sequenceDiagram
    participant Frontend
    participant API
    participant SimulationService
    participant MapLibre

    Frontend->>API: GET /api/simulation/runs/{id}/frames/{index}
    API->>SimulationService: get_frame(simulation_run_id, index)
    SimulationService->>DB: SELECT frame_geojson FROM simulation_frames
    DB-->>SimulationService: GeoJSON
    SimulationService-->>API: SpillFrame
    API-->>Frontend: {time_hours, geojson, mass_balance, ...}
    
    Frontend->>MapLibre: map.getSource('spill').setData(geojson)
    MapLibre->>MapLibre: Re-render concentration polygons
    MapLibre->>MapLibre: Update release point, vessel layers
```

**Frame GeoJSON Structure:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "concentration": "VERY_HIGH|HIGH|MEDIUM|LOW",
        "time_hours": 24,
        "color": "#8B0000",
        "opacity": 0.8
      },
      "geometry": { "type": "Polygon", "coordinates": [...] }
    },
    {
      "type": "Feature",
      "properties": { "type": "release_point", "time_hours": 24 },
      "geometry": { "type": "Point", "coordinates": [72.8177, 18.9076] }
    },
    {
      "type": "Feature",
      "properties": { "type": "vessel", "name": "MV Oceanic Star", "time_hours": 24 },
      "geometry": { "type": "Point", "coordinates": [72.8227, 18.9126] }
    }
  ]
}
```

---

## 4. Damage Assessment Flow

```mermaid
sequenceDiagram
    participant Frontend
    participant API
    participant DamageService
    participant ESI_Loader
    participant Spatial
    participant Exposure
    participant Sensitivity
    participant HazardZone
    participant Scoring
    participant DB

    Frontend->>API: POST /api/damage/assess (simulation_run_id)
    API->>DamageService: assess_damage(simulation_run_id)
    DamageService->>ESI_Loader: load_esi_features()
    ESI_Loader-->>DamageService: List[ESIFeature]
    
    DamageService->>Spatial: calculate_intersections(spill_geojson, esi_features)
    Spatial-->>DamageService: List[Intersection] (area_km2, affected_pct, concentrations)
    
    DamageService->>Exposure: calculate_exposure(intersections)
    Exposure-->>DamageService: List[ExposureResult] (exposure_score)
    
    DamageService->>Sensitivity: calculate_sensitivity(exposure, esi_features)
    Sensitivity-->>DamageService: List[SensitivityResult] (sensitivity_score)
    
    DamageService->>HazardZone: calculate_hazard_zones(sensitivity)
    HazardZone-->>DamageService: List[HazardZone] (hazard_level, hazard_score)
    
    DamageService->>Scoring: calculate_hazard_score(hazard_zones)
    Scoring-->>DamageService: hazard_score (0-100) + component_scores
    
    DamageService->>DB: INSERT damage_assessment + resources + shoreline
    DamageService-->>API: DamageAssessmentRead
    API-->>Frontend: Full damage assessment
```

**Key Transformations:**

| Stage | Input | Operation | Output |
|-------|-------|-----------|--------|
| Intersection | Spill polygons + ESI polygons | `ST_Intersection` (PostGIS) / Shapely | Affected area per resource |
| Exposure | Intersection + concentration | Area × Concentration Weight | Exposure score per resource |
| Sensitivity | Exposure + ESI metadata | × Sensitivity Score × Type Multiplier | Sensitivity score per resource |
| Hazard Zones | Sensitivity results | Threshold classification | Zones (LOW/MEDIUM/HIGH/VERY_HIGH) |
| Scoring | Hazard zones | Weighted sum normalized | Hazard Score 0-100 + components |

---

## 5. Dashboard Update Flow

```mermaid
sequenceDiagram
    participant Frontend
    participant API
    participant DamageService
    participant DB

    Frontend->>API: GET /api/damage/assessments/{id}
    API->>DamageService: get_assessment(assessment_id)
    DamageService->>DB: SELECT with JOINs
    DB-->>DamageService: Assessment + resources + shoreline
    DamageService-->>API: DamageAssessmentRead
    API-->>Frontend: Complete assessment
    
    Frontend->>Frontend: Update 4 panels:
    Note right of Frontend: SpillSummary<br/>DangerAssessment<br/>EcologicalResources<br/>ShorelineImpact
```

---

## 6. Satellite Evidence Request (Placeholder)

```mermaid
sequenceDiagram
    participant Frontend
    participant API
    participant IncidentService

    Frontend->>API: POST /api/incidents/{id}/satellite-evidence
    API->>IncidentService: request_satellite_evidence(incident_id, provider)
    IncidentService-->>API: {status: "requested", provider, message}
    API-->>Frontend: 200 OK + info
    
    Note over Frontend: UI shows "Satellite evidence requested.<br/>Integration coming in Phase 2."
```

---

## Data Stores

| Store | Purpose | Key Tables |
|-------|---------|------------|
| PostgreSQL + PostGIS | Primary persistence | `incidents`, `simulation_runs`, `simulation_frames`, `esi_features`, `damage_assessments`, `damage_ecological_resources`, `shoreline_impacts` |
| Redis | Queue (Celery), caching | Session, task queue, rate limiting |
| MinIO (S3) | Large objects | SAR scenes, model weights, raw data |
| File System (dev) | Mock data | `data/simulation_frames/*.geojson`, `data/esi_features.geojson` |

---

## Error Handling Flow

```
Any Service Method
        │
        ▼
Try/Except
        │
        ├── Success → Return typed result
        │
        └── Exception → Log error → Return None / Raise HTTPException
                            │
                            ▼
                    API catches → HTTPException(status, detail)
                            │
                            ▼
                    Frontend catches → Show toast/error banner
```