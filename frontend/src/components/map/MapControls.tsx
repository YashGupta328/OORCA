import { ZoomIn, ZoomOut, Compass, RotateCcw, Layers, Navigation } from 'lucide-react';

interface MapControlsProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetNorth: () => void;
  onResetView: () => void;
}

export function MapControls({ onZoomIn, onZoomOut, onResetNorth, onResetView }: MapControlsProps) {
  return (
    <div className="absolute top-16 right-4 z-10 flex flex-col gap-1">
      <button onClick={onZoomIn} className="btn-secondary p-2 rounded-lg" title="Zoom In">
        <ZoomIn className="w-5 h-5" />
      </button>
      <button onClick={onZoomOut} className="btn-secondary p-2 rounded-lg" title="Zoom Out">
        <ZoomOut className="w-5 h-5" />
      </button>
      <button onClick={onResetNorth} className="btn-secondary p-2 rounded-lg" title="Reset North">
        <Compass className="w-5 h-5" />
      </button>
      <button onClick={onResetView} className="btn-secondary p-2 rounded-lg" title="Reset View">
        <RotateCcw className="w-5 h-5" />
      </button>
      <button className="btn-secondary p-2 rounded-lg" title="Layers">
        <Layers className="w-5 h-5" />
      </button>
    </div>
  );
}