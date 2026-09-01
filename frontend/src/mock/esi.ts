/** Mock ESI data for development */

export const mockESIResources = [
  {
    id: 'esi-mangrove-001',
    resource_type: 'mangrove',
    resource_name: 'Thane Creek Mangroves',
    sensitivity_score: 95,
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [72.95, 19.15],
        [73.05, 19.15],
        [73.05, 19.25],
        [72.95, 19.25],
        [72.95, 19.15],
      ]],
    },
    metadata: {
      area_km2: 12.5,
      dominant_species: 'Avicennia marina',
      conservation_status: 'Protected',
    },
  },
  {
    id: 'esi-fish-001',
    resource_type: 'fish_habitat',
    resource_name: 'Mumbai Offshore Fisheries Zone',
    sensitivity_score: 75,
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [72.70, 18.80],
        [73.00, 18.80],
        [73.00, 19.20],
        [72.70, 19.20],
        [72.70, 18.80],
      ]],
    },
    metadata: {
      area_km2: 185.4,
      key_species: ['Bombay duck', 'Pomfret', 'Mackerel', 'Shrimp'],
      fishing_intensity: 'High',
    },
  },
];