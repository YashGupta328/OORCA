/** Ecology/ESI types for Phase 1 */

export interface ESIResource {
  id: string;
  resource_type: string;
  resource_name: string;
  sensitivity_score: number;
  geometry: GeoJSON.Geometry;
  metadata?: Record<string, any>;
}