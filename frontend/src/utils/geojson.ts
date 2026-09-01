/** GeoJSON utilities */

import type { Feature, FeatureCollection, Geometry, Polygon, MultiPolygon, Point } from 'geojson';

export function isPoint(geom: Geometry): geom is Point {
  return geom.type === 'Point';
}

export function isPolygon(geom: Geometry): geom is Polygon {
  return geom.type === 'Polygon';
}

export function isMultiPolygon(geom: Geometry): geom is MultiPolygon {
  return geom.type === 'MultiPolygon';
}

export function getPolygonArea(geom: Polygon | MultiPolygon): number {
  // Approximate area calculation in km2
  if (geom.type === 'Polygon') {
    return Math.abs(calculatePolygonArea(geom.coordinates[0])) * 111 * 111;
  }
  let total = 0;
  for (const poly of geom.coordinates) {
    total += Math.abs(calculatePolygonArea(poly[0])) * 111 * 111;
  }
  return total;
}

function calculatePolygonArea(coords: number[][]): number {
  let area = 0;
  for (let i = 0; i < coords.length - 1; i++) {
    area += coords[i][0] * coords[i + 1][1] - coords[i + 1][0] * coords[i][1];
  }
  return area / 2;
}

export function getConcentrationColor(concentration: string): string {
  const colors: Record<string, string> = {
    LOW: '#ffff00',
    MEDIUM: '#ffa500',
    HIGH: '#ff0000',
    VERY_HIGH: '#8b0000',
  };
  return colors[concentration] || '#ffff00';
}

export function getConcentrationOpacity(concentration: string): number {
  const opacities: Record<string, number> = {
    LOW: 0.5,
    MEDIUM: 0.6,
    HIGH: 0.7,
    VERY_HIGH: 0.8,
  };
  return opacities[concentration] || 0.5;
}

export function filterFeaturesByConcentration(
  geojson: FeatureCollection,
  concentrations: string[]
): FeatureCollection {
  return {
    ...geojson,
    features: geojson.features.filter(f => 
      concentrations.includes(f.properties?.concentration || '')
    ),
  };
}

export function getTimeFrames(geojson: FeatureCollection): number[] {
  const times = new Set<number>();
  for (const feature of geojson.features) {
    const t = feature.properties?.time_hours;
    if (typeof t === 'number') times.add(t);
  }
  return Array.from(times).sort((a, b) => a - b);
}

export function getFrameAtTime(geojson: FeatureCollection, timeHours: number): FeatureCollection {
  return {
    ...geojson,
    features: geojson.features.filter(f => f.properties?.time_hours === timeHours),
  };
}