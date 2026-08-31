# Data Flow

End-to-end data flow for a single oil spill investigation.

```
Sentinel-1 SAR  ──┐
                  │
AIS messages  ────┼──►  ingestion (workers) ──► object storage + PostGIS
                  │                                  │
Metocean  ────────┤                                  ▼
                  │                          engine/sar, engine/ais
ESI rasters ──────┘                                  │
                                                     ▼
                                            detections + vessel tracks
                                                     │
                                                     ▼
                                          engine/drift (hindcast)
                                                     │
                                                     ▼
                                       engine/attribution (candidate ranking)
                                                     │
                                                     ▼
                                     engine/ecology (ESI intersection)
                                                     │
                                                     ▼
                                     engine/liability (Monte Carlo damages)
                                                     │
                                                     ▼
                                     backend/api  ──►  frontend dashboards
```

Each stage is independently triggerable through the worker queue, enabling partial replays and what-if analysis.