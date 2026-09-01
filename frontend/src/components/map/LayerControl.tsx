import { Eye, EyeOff } from 'lucide-react';

interface LayerControlProps {
  visibleLayers: Record<string, boolean>;
  onToggle: (layerId: string) => void;
}

export function LayerControl({ visibleLayers, onToggle }: LayerControlProps) {
  const layers = [
    { id: 'spill', label: 'Oil Concentration', icon: '🛢️' },
    { id: 'spillOutline', label: 'Slick Outline', icon: '📍' },
    { id: 'releasePoint', label: 'Release Point', icon: '🎯' },
    { id: 'vessel', label: 'Vessel Position', icon: '🚢' },
    { id: 'esi', label: 'ESI Resources', icon: '🌿' },
    { id: 'shoreline', label: 'Shoreline Impact', icon: '🏖️' },
    { id: 'wind', label: 'Wind Vectors', icon: '💨' },
    { id: 'current', label: 'Current Vectors', icon: '🌊' },
  ];

  return (
    <div className="panel p-2 space-y-1 min-w-[200px]">
      <p className="text-xs font-semibold text-dark-text-muted uppercase tracking-wider px-2">Map Layers</p>
      {layers.map(layer => (
        <label key={layer.id} className="flex items-center gap-2 px-2 py-1 hover:bg-dark-panel-hover rounded cursor-pointer">
          <input
            type="checkbox"
            checked={visibleLayers[layer.id]}
            onChange={() => onToggle(layer.id)}
            className="w-4 h-4 accent-marine-500"
          />
          <span className="text-sm text-dark-text">{layer.icon} {layer.label}</span>
        </label>
      ))}
    </div>
  );
}