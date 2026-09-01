/** Damage assessment types for Phase 1 */

export interface SpillSummary {
  total_spilled_tonnes: number;
  estimated_slick_area_km2: number;
  simulation_duration_hours: number;
  weathering_percent: number;
  evaporation_percent: number;
  dispersion_percent: number;
  remaining_surface_oil_tonnes: number;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'VERY_HIGH';

export interface DangerAssessment {
  overall_risk: RiskLevel;
  environmental_risk: RiskLevel;
  shoreline_risk: RiskLevel;
  human_exposure_risk: RiskLevel;
  cleanup_difficulty: RiskLevel;
  hazard_score: number;
}

export interface ESIResource {
  resource_id: string;
  resource_type: string;
  resource_name: string;
  sensitivity_score: number;
  geometry: GeoJSON.Geometry;
  affected_area_km2?: number;
  risk_level?: RiskLevel;
  intersection_geometry?: GeoJSON.Geometry;
}

export interface ShorelineImpact {
  location: string;
  arrival_time_hours?: [number, number];
  impact_level: RiskLevel;
  distance_km?: number;
  coordinates?: [number, number];
}

export interface DamageAssessment {
  assessment_id: string;
  incident_id: string;
  simulation_run_id: string;
  spill_summary: SpillSummary;
  danger_assessment: DangerAssessment;
  ecological_resources: ESIResource[];
  shoreline_impact: ShorelineImpact[];
  calculated_at: string;
}