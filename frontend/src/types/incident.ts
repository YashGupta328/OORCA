/** Incident and simulation types for Phase 1 */

export interface Location {
  latitude: number;
  longitude: number;
}

export interface SpillDetails {
  amount: number;
  unit: 'tonnes' | 'barrels' | 'liters' | 'gallons';
  oil_type: 'crude_oil' | 'diesel' | 'heavy_fuel_oil' | 'gasoline' | 'jet_fuel';
  start_time: string;
  duration_hours: number;
}

export interface VesselDetails {
  name?: string;
  vessel_type?: 'oil_tanker' | 'cargo' | 'fishing' | 'passenger' | 'other';
  imo?: string;
  length_m?: number;
  breadth_m?: number;
  draft_m?: number;
  heading_deg?: number;
}

export interface IncidentCreate {
  location: Location;
  spill: SpillDetails;
  vessel?: VesselDetails;
}

export interface Incident extends IncidentCreate {
  incident_id: string;
  created_at: string;
  status: 'created' | 'simulating' | 'completed' | 'failed';
}

export interface SimulationRunCreate {
  incident_id: string;
  provider: 'mock' | 'opendrift';
}

export interface SimulationRun {
  simulation_run_id: string;
  incident_id: string;
  provider: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  frames?: SpillFrame[];
  wind_current_data?: WindCurrentFrame[];
  error?: string;
}

export interface SpillFrame {
  time_hours: number;
  geojson: GeoJSON.FeatureCollection;
}

export interface WindCurrentFrame {
  time_hours: number;
  wind_u?: number[][];
  wind_v?: number[][];
  current_u?: number[][];
  current_v?: number[][];
  bounds?: number[];
}

export interface SimulationStatus {
  simulation_run_id: string;
  status: 'idle' | 'initializing' | 'loading_metocean' | 'simulating' | 'calculating_impact' | 'completed' | 'failed';
  progress: number;
  current_step?: string;
  frames_ready: number;
  total_frames: number;
}