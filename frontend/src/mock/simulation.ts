/** Mock simulation data for development */

export const mockIncident = {
  incident_id: 'ORCA-20260901-A1B2C3',
  location: { latitude: 18.9076, longitude: 72.8177 },
  spill: {
    amount: 100,
    unit: 'tonnes',
    oil_type: 'crude_oil',
    start_time: '2026-09-01T10:00:00Z',
    duration_hours: 72,
  },
  vessel: {
    name: 'MV Oceanic Star',
    vessel_type: 'oil_tanker',
    imo: '9732548',
    length_m: 274,
    breadth_m: 48,
    draft_m: 16,
    heading_deg: 45,
  },
  created_at: '2026-09-01T10:05:00Z',
  status: 'completed' as const,
};

export const mockSimulationRun = {
  simulation_run_id: 'sim-ORCA-20260901-20260901100500',
  incident_id: 'ORCA-20260901-A1B2C3',
  provider: 'mock',
  status: 'completed' as const,
  started_at: '2026-09-01T10:05:00Z',
  completed_at: '2026-09-01T10:05:15Z',
  frames: [] as any[],
  wind_current_data: [] as any[],
};

export const mockDamageAssessment = {
  assessment_id: 'damage-A1B2C3D4E5F6',
  incident_id: 'ORCA-20260901-A1B2C3',
  simulation_run_id: 'sim-ORCA-20260901-20260901100500',
  spill_summary: {
    total_spilled_tonnes: 100,
    estimated_slick_area_km2: 45.8,
    simulation_duration_hours: 72,
    weathering_percent: 25,
    evaporation_percent: 15,
    dispersion_percent: 10,
    remaining_surface_oil_tonnes: 75,
  },
  danger_assessment: {
    overall_risk: 'HIGH',
    environmental_risk: 'HIGH',
    shoreline_risk: 'MEDIUM',
    human_exposure_risk: 'MEDIUM',
    cleanup_difficulty: 'HIGH',
    hazard_score: 68.5,
  },
  ecological_resources: [
    {
      resource_id: 'esi-mangrove-001',
      resource_type: 'mangrove',
      resource_name: 'Thane Creek Mangroves',
      sensitivity_score: 95,
      geometry: { type: 'Polygon', coordinates: [] },
      affected_area_km2: 2.3,
      risk_level: 'HIGH',
    },
    {
      resource_id: 'esi-fish-001',
      resource_type: 'fish_habitat',
      resource_name: 'Mumbai Offshore Fisheries Zone',
      sensitivity_score: 75,
      geometry: { type: 'Polygon', coordinates: [] },
      affected_area_km2: 15.5,
      risk_level: 'MEDIUM',
    },
    {
      resource_id: 'esi-seagrass-001',
      resource_type: 'seagrass',
      resource_name: 'Malvan Seagrass Meadows',
      sensitivity_score: 85,
      geometry: { type: 'Polygon', coordinates: [] },
      affected_area_km2: 0.8,
      risk_level: 'LOW',
    },
  ],
  shoreline_impact: [
    {
      location: 'Alibaug Coast',
      arrival_time_hours: [36, 48],
      impact_level: 'HIGH',
      distance_km: 12.5,
      coordinates: [72.87, 18.64],
    },
    {
      location: 'Revdanda Beach',
      arrival_time_hours: [48, 60],
      impact_level: 'MEDIUM',
      distance_km: 18.2,
      coordinates: [72.92, 18.54],
    },
    {
      location: 'Murud Beach',
      arrival_time_hours: [60, 72],
      impact_level: 'MEDIUM',
      distance_km: 25.1,
      coordinates: [72.97, 18.42],
    },
    {
      location: 'Kihim Beach',
      arrival_time_hours: [72, 84],
      impact_level: 'LOW',
      distance_km: 30.8,
      coordinates: [72.83, 18.78],
    },
  ],
  calculated_at: '2026-09-01T10:06:00Z',
};