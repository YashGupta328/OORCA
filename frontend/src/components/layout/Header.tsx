import { X, RotateCcw, AlertTriangle } from 'lucide-react';
import { useState } from 'react';

interface HeaderProps {
  onReset: () => void;
}

export function Header({ onReset }: HeaderProps) {
  const [showConfirm, setShowConfirm] = useState(false);

  const handleReset = () => {
    if (showConfirm) {
      onReset();
      setShowConfirm(false);
    } else {
      setShowConfirm(true);
      setTimeout(() => setShowConfirm(false), 3000);
    }
  };

  return (
    <header className="h-14 px-4 border-b border-dark-border bg-dark-panel/80 backdrop-blur-sm flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-marine-500 to-ocean-500 flex items-center justify-center">
          <svg width="20" height="20" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 6 L16 14 M11 11 L16 16 L21 11" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="16" cy="22" r="5" stroke="white" stroke-width="2"/>
            <path d="M14 22 L16 24 L18 22" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div>
          <h1 className="text-lg font-semibold text-dark-text">OORCA</h1>
          <p className="text-xs text-dark-text-muted">Oil Spill Simulator</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={handleReset}
          className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 flex items-center gap-1.5 ${
            showConfirm 
              ? 'bg-red-600 text-white hover:bg-red-500' 
              : 'bg-dark-panel-hover text-dark-text-muted hover:text-dark-text hover:bg-dark-border border border-dark-border'
          }`}
          title="Reset Simulation"
        >
          <RotateCcw className="w-4 h-4" />
          {showConfirm ? (
            <>Confirm Reset <AlertTriangle className="w-3.5 h-3.5 animate-pulse" /></>
          ) : (
            'Reset'
          )}
        </button>
      </div>
    </header>
  );
}