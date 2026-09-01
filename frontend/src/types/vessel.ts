/** Vessel types for Phase 1 */

export interface VesselDetails {
  name?: string;
  vessel_type?: 'oil_tanker' | 'cargo' | 'fishing' | 'passenger' | 'other';
  imo?: string;
  length_m?: number;
  breadth_m?: number;
  draft_m?: number;
  heading_deg?: number;
}