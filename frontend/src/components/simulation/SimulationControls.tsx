import { RotateCcw, Play, Pause, StopCircle, Info } from 'lucide-react';

interface SimulationControlsProps {
  isSimulating: boolean;
  onReset: () => void;
  disabled: boolean;
}

export function SimulationControls({ isSimulating, onReset, disabled }: SimulationControlsProps) {
  return (
    <div className="p-4 space-y-3 border-t border-dark-border animate-in">
      <div className="flex items-center gap-2">
        <Info className="w-5 h-5 text-marine-400" />
        <h2 className="text-sm font-semibold text-dark-text uppercase tracking-wider">Controls</h2>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <button
          type="button"
          className="btn-secondary py-2 flex items-center justify-center gap-2"
          disabled={disabled || isSimulating}
        >
          <Play className="w-4 h-4" />
          Start
        </button>
        <button
          type="button"
          className="btn-danger py-2 flex items-center justify-center gap-2"
          disabled={disabled || !isSimulating}
        >
          <StopCircle className="w-4 h-4" />
          Stop
        </button>
      </div>
      <button
        type="button"
        onClick={onReset}
        className="w-full btn-secondary py-2 flex items-center justify-center gap-2"
        disabled={disabled}
      >
        <RotateCcw className="w-4 h-4" />
        Reset Simulation
      </button>
    </div>
  );
}