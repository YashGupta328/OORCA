/** Coordinate utilities */

export function formatCoordinate(coord: number, isLat: boolean = true): string {
  const direction = isLat 
    ? (coord >= 0 ? 'N' : 'S')
    : (coord >= 0 ? 'E' : 'W');
  const abs = Math.abs(coord);
  const degrees = Math.floor(abs);
  const minutes = (abs - degrees) * 60;
  return `${degrees}°${minutes.toFixed(2)}'${direction}`;
}

export function formatCoordinateDecimal(coord: number, precision: number = 4): string {
  return coord.toFixed(precision);
}

export function parseCoordinate(input: string): number | null {
  // Parse DMS or decimal format
  const dmsMatch = input.match(/(\d+)°?\s*(\d+(?:\.\d+)?)?\s*['′]?\s*(\d+(?:\.\d+)?)?\s*["″]?\s*([NSEW])?/i);
  if (dmsMatch) {
    const degrees = parseFloat(dmsMatch[1]);
    const minutes = parseFloat(dmsMatch[2] || '0');
    const seconds = parseFloat(dmsMatch[3] || '0');
    const direction = dmsMatch[4]?.toUpperCase();
    let decimal = degrees + minutes / 60 + seconds / 3600;
    if (direction === 'S' || direction === 'W') decimal = -decimal;
    return decimal;
  }
  const decimal = parseFloat(input);
  return isNaN(decimal) ? null : decimal;
}

export function haversineDistance(
  lat1: number, lon1: number,
  lat2: number, lon2: number
): number {
  const R = 6371; // Earth radius in km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function toRad(deg: number): number {
  return deg * Math.PI / 180;
}

export function boundingBoxFromPoints(points: [number, number][]): [number, number, number, number] {
  let minLon = Infinity, minLat = Infinity, maxLon = -Infinity, maxLat = -Infinity;
  for (const [lon, lat] of points) {
    minLon = Math.min(minLon, lon);
    maxLon = Math.max(maxLon, lon);
    minLat = Math.min(minLat, lat);
    maxLat = Math.max(maxLat, lat);
  }
  return [minLon, minLat, maxLon, maxLat];
}