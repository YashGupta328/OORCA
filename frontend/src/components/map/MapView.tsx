import { useEffect, useRef, useState, useCallback } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import type { SpillFrame, DamageAssessment, Incident } from '@/types';
import { getConcentrationColor, getConcentrationOpacity, getFrameAtTime } from '@/utils/geojson';

interface MapViewProps {
  frames: SpillFrame[];
  currentFrameIndex: number;
  damageAssessment: DamageAssessment | null;
  incident: Incident | null;
  onMapReady: (ready: boolean) => void;
}

const INITIAL_VIEW = {
  center: [72.8177, 18.9076] as [number, number],
  zoom: 9,
  pitch: 0,
  bearing: 0,
};

const LAYER_IDS = {
  spill: 'spill-concentration',
  spillOutline: 'spill-outline',
  releasePoint: 'release-point',
  vessel: 'vessel-position',
  wind: 'wind-vectors',
  current: 'current-vectors',
  esi: 'esi-features',
  shoreline: 'shoreline-impact',
};

export function MapView({ frames, currentFrameIndex, damageAssessment, incident, onMapReady }: MapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [layersVisible, setLayersVisible] = useState({
    spill: true,
    spillOutline: true,
    releasePoint: true,
    vessel: true,
    wind: false,
    current: false,
    esi: true,
    shoreline: true,
  });

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors',
          },
        },
        layers: [
          {
            id: 'background',
            type: 'background',
            paint: { 'background-color': '#081830' },
          },
          {
            id: 'osm',
            type: 'raster',
            source: 'osm',
            paint: { 'raster-opacity': 0.4, 'raster-fade-duration': 0 },
          },
        ],
      },
      center: incident ? [incident.location.longitude, incident.location.latitude] : INITIAL_VIEW.center,
      zoom: INITIAL_VIEW.zoom,
      pitch: INITIAL_VIEW.pitch,
      bearing: INITIAL_VIEW.bearing,
      preserveDrawingBuffer: true,
    });

    map.current.on('load', () => {
      setMapLoaded(true);
      onMapReady(true);
      addMapLayers();
    });

    return () => {
      map.current?.remove();
      map.current = null;
      setMapLoaded(false);
      onMapReady(false);
    };
  }, [incident]);

  const addMapLayers = useCallback(() => {
    if (!map.current || !mapLoaded) return;

    const m = map.current;

    // ESI layer (static)
    if (damageAssessment?.ecological_resources) {
      const esiFeatures = damageAssessment.ecological_resources.map(r => ({
        type: 'Feature' as const,
        properties: {
          resource_id: r.resource_id,
          resource_type: r.resource_type,
          resource_name: r.resource_name,
          sensitivity_score: r.sensitivity_score,
          risk_level: r.risk_level,
        },
        geometry: r.geometry,
      }));

      if (!m.getSource('esi')) {
        m.addSource('esi', { type: 'geojson', data: { type: 'FeatureCollection', features: esiFeatures } });
        m.addLayer({
          id: LAYER_IDS.esi,
          type: 'fill',
          source: 'esi',
          paint: {
            'fill-color': [
              'match',
              ['get', 'resource_type'],
              'mangrove', '#006400',
              'coral_reef', '#ff6b6b',
              'seagrass', '#2e8b57',
              'fish_habitat', '#4682b4',
              'sea_turtle_habitat', '#ff8c00',
              'dolphin_habitat', '#00bfff',
              'protected_area', '#800080',
              'saltmarsh', '#8fbc8f',
              '#666666',
            ],
            'fill-opacity': 0.3,
            'fill-outline-color': '#ffffff',
          },
        });
      }
    }

    // Shoreline impact layer
    if (damageAssessment?.shoreline_impact) {
      const shoreFeatures = damageAssessment.shoreline_impact.map(s => ({
        type: 'Feature' as const,
        properties: {
          location: s.location,
          arrival_time: s.arrival_time_hours ? `${s.arrival_time_hours[0]}-${s.arrival_time_hours[1]}h` : 'Unknown',
          impact_level: s.impact_level,
          distance_km: s.distance_km,
        },
        geometry: {
          type: 'Point',
          coordinates: s.coordinates || [0, 0],
        },
      }));

      if (!m.getSource('shoreline')) {
        m.addSource('shoreline', { type: 'geojson', data: { type: 'FeatureCollection', features: shoreFeatures } });
        m.addLayer({
          id: LAYER_IDS.shoreline,
          type: 'circle',
          source: 'shoreline',
          paint: {
            'circle-radius': 10,
            'circle-color': [
              'match',
              ['get', 'impact_level'],
              'VERY_HIGH', '#8b0000',
              'HIGH', '#ff0000',
              'MEDIUM', '#ffa500',
              'LOW', '#ffff00',
              '#666666',
            ],
            'circle-stroke-width': 2,
            'circle-stroke-color': '#ffffff',
            'circle-opacity': 0.8,
          },
        });
      }
    }

    // Initial spill layers (empty, will be updated)
    if (!m.getSource('spill')) {
      m.addSource('spill', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
      m.addSource('releasePoint', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
      m.addSource('vessel', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });

      // Spill concentration fill
      m.addLayer({
        id: LAYER_IDS.spill,
        type: 'fill',
        source: 'spill',
        paint: {
          'fill-color': [
            'match',
            ['get', 'concentration'],
            'VERY_HIGH', '#8b0000',
            'HIGH', '#ff0000',
            'MEDIUM', '#ffa500',
            'LOW', '#ffff00',
            '#ffff00',
          ],
          'fill-opacity': [
            'match',
            ['get', 'concentration'],
            'VERY_HIGH', 0.8,
            'HIGH', 0.7,
            'MEDIUM', 0.6,
            'LOW', 0.5,
            0.5,
          ],
        },
        filter: ['!=', ['get', 'type'], 'release_point'],
      });

      // Spill outline
      m.addLayer({
        id: LAYER_IDS.spillOutline,
        type: 'line',
        source: 'spill',
        paint: {
          'line-color': [
            'match',
            ['get', 'concentration'],
            'VERY_HIGH', '#8b0000',
            'HIGH', '#ff0000',
            'MEDIUM', '#ffa500',
            'LOW', '#ffff00',
            '#ffff00',
          ],
          'line-width': 2,
          'line-opacity': 0.8,
        },
        filter: ['!=', ['get', 'type'], 'release_point'],
      });

      // Release point
      m.addLayer({
        id: LAYER_IDS.releasePoint,
        type: 'circle',
        source: 'releasePoint',
        paint: {
          'circle-radius': 12,
          'circle-color': '#ffffff',
          'circle-stroke-width': 3,
          'circle-stroke-color': '#ff0000',
          'circle-opacity': 0.9,
        },
      });

      // Vessel
      m.addLayer({
        id: LAYER_IDS.vessel,
        type: 'symbol',
        source: 'vessel',
        layout: {
          'icon-image': 'marker-15',
          'icon-size': 1.2,
          'icon-allow-overlap': true,
          'text-field': ['get', 'name'],
          'text-font': ['Open Sans Semibold'],
          'text-size': 12,
          'text-offset': [0, 1.5],
          'text-anchor': 'top',
        },
        paint: {
          'text-color': '#ffffff',
          'text-halo-color': '#0a1628',
          'text-halo-width': 2,
        },
      });
    }
  }, [damageAssessment, mapLoaded]);

  // Update spill frame
  useEffect(() => {
    if (!map.current || !mapLoaded || frames.length === 0) return;

    const frame = frames[currentFrameIndex];
    if (!frame) return;

    const m = map.current;

    // Update spill source
    const spillSource = m.getSource('spill');
    if (spillSource && frame.geojson) {
      spillSource.setData(frame.geojson);
    }

    // Update release point
    const releaseSource = m.getSource('releasePoint');
    const releaseFeature = frame.geojson.features.find(f => f.properties?.type === 'release_point');
    if (releaseSource && releaseFeature) {
      releaseSource.setData({ type: 'FeatureCollection', features: [releaseFeature] });
    }

    // Update vessel
    const vesselSource = m.getSource('vessel');
    const vesselFeature = frame.geojson.features.find(f => f.properties?.type === 'vessel');
    if (vesselSource && vesselFeature) {
      vesselSource.setData({ type: 'FeatureCollection', features: [vesselFeature] });
    }

    // Fit bounds to spill on first frame
    if (currentFrameIndex === 0) {
      const bounds = calculateBounds(frame.geojson);
      if (bounds) {
        m.fitBounds(bounds, { padding: 50, duration: 1000 });
      }
    }
  }, [currentFrameIndex, frames, mapLoaded]);

  const calculateBounds = (geojson: any): maplibregl.LngLatBoundsLike | null => {
    let minLon = Infinity, minLat = Infinity, maxLon = -Infinity, maxLat = -Infinity;
    let hasCoords = false;

    for (const feature of geojson.features) {
      const coords = feature.geometry?.coordinates;
      if (!coords) continue;
      hasCoords = true;
      if (feature.geometry.type === 'Point') {
        minLon = Math.min(minLon, coords[0]);
        maxLon = Math.max(maxLon, coords[0]);
        minLat = Math.min(minLat, coords[1]);
        maxLat = Math.max(maxLat, coords[1]);
      } else if (feature.geometry.type === 'Polygon') {
        for (const ring of coords) {
          for (const [lon, lat] of ring) {
            minLon = Math.min(minLon, lon);
            maxLon = Math.max(maxLon, lon);
            minLat = Math.min(minLat, lat);
            maxLat = Math.max(maxLat, lat);
          }
        }
      }
    }

    if (!hasCoords) return null;
    return [[minLon, minLat], [maxLon, maxLat]] as maplibregl.LngLatBoundsLike;
  };

  // Toggle layer visibility
  const toggleLayer = (layerId: keyof typeof layersVisible) => {
    if (!map.current || !mapLoaded) return;
    const newVisible = !layersVisible[layerId];
    setLayersVisible(prev => ({ ...prev, [layerId]: newVisible }));
    map.current.setLayoutProperty(LAYER_IDS[layerId], 'visibility', newVisible ? 'visible' : 'none');
  };

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      
      {/* Map Controls Overlay */}
      <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
        <div className="panel p-2 space-y-1 min-w-[200px]">
          <p className="text-xs font-semibold text-dark-text-muted uppercase tracking-wider px-2">Layers</p>
          {[
            { id: 'spill', label: 'Oil Concentration', color: 'bg-gradient-to-r from-yellow-400 to-red-600' },
            { id: 'spillOutline', label: 'Slick Outline', color: 'bg-gray-500' },
            { id: 'releasePoint', label: 'Release Point', color: 'bg-red-500' },
            { id: 'vessel', label: 'Vessel Position', color: 'bg-ocean-400' },
            { id: 'esi', label: 'ESI Resources', color: 'bg-green-600' },
            { id: 'shoreline', label: 'Shoreline Impact', color: 'bg-orange-500' },
            { id: 'wind', label: 'Wind Vectors', color: 'bg-blue-400' },
            { id: 'current', label: 'Current Vectors', color: 'bg-cyan-400' },
          ].map(layer => (
            <label key={layer.id} className="flex items-center gap-2 px-2 py-1 hover:bg-dark-panel-hover rounded cursor-pointer">
              <input
                type="checkbox"
                checked={layersVisible[layer.id as keyof typeof layersVisible]}
                onChange={() => toggleLayer(layer.id as keyof typeof layersVisible)}
                className="w-4 h-4 accent-marine-500"
              />
              <span className="w-3 h-3 rounded {layer.color}" />
              <span className="text-sm text-dark-text">{layer.label}</span>
            </label>
          ))}
        </div>

        {/* Legend */}
        <div className="panel p-2 min-w-[160px]">
          <p className="text-xs font-semibold text-dark-text-muted uppercase tracking-wider mb-2">Concentration</p>
          <div className="space-y-1">
            {[
              { label: 'Very High', color: '#8b0000' },
              { label: 'High', color: '#ff0000' },
              { label: 'Medium', color: '#ffa500' },
              { label: 'Low', color: '#ffff00' },
            ].map(item => (
              <div key={item.label} className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: item.color, opacity: 0.7 }} />
                <span className="text-xs text-dark-text">{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Coordinates display */}
      <div className="absolute bottom-4 left-4 z-10 panel px-3 py-1.5">
        <p className="text-xs font-mono text-dark-text">
          {map.current ? `${map.current.getCenter().lng.toFixed(4)}, ${map.current.getCenter().lat.toFixed(4)} | Zoom: ${map.current.getZoom().toFixed(1)}` : 'Loading...'}
        </p>
      </div>
    </div>
  );
}