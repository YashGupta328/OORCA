import { Loader2, CheckCircle, AlertCircle, Clock, Database, Wind, Waves } from 'lucide-react';
import type { SimulationStatus } from '@/types';

interface SimulationStatusProps {
  status: SimulationStatus | null;
  isSimulating: boolean;
}

const STEPS = [
  { key: 'initializing', label: 'Initializing', icon: Loader2 },
  { key: 'loading_metocean', label: 'Loading MetOcean', icon: Wind },
  { key: 'simulating', label: 'Running Simulation', icon: Waves },
  { key: 'calculating_impact', label: 'Calculating Impact', icon: Database },
  { key: 'completed', label: 'Completed', icon: CheckCircle },
];

export function SimulationStatus({ status, isSimulating }: SimulationStatusProps) {
  if (!isSimulating && !status) return null;

  const currentStepIndex = status ? STEPS.findIndex(s => s.key === status.status) : 0;
  const progress = status?.progress || (isSimulating ? 10 : 0);

  return (
    <div className="p-4 space-y-3 border-t border-dark-border animate-in">
      <div className="flex items-center gap-2">
        <Database className="w-5 h-5 text-ocean-400" />
        <h2 className="text-sm font-semibold text-dark-text uppercase tracking-wider">Simulation Status</h2>
      </div>
      
      {/* Progress Bar */}
      <div className="space-y-1">
        <div className="flex justify-between text-xs">
          <span className="text-dark-text-muted">Progress</span>
          <span className="font-mono text-marine-400">{progress}%</span>
        </div>
        <div className="h-2 bg-dark-bg rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-marine-500 to-ocean-500 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="space-y-2">
        {STEPS.map((step, index) => {
          const isActive = index === currentStepIndex;
          const isCompleted = index < currentStepIndex;
          const Icon = step.icon;
          
          return (
            <div className={`flex items-center gap-3 transition-all duration-300 ${isActive ? 'animate-pulse' : ''}`}>
              <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
                isCompleted ? 'bg-emerald-500 text-white' :
                isActive ? 'bg-marine-500 text-white animate-spin' :
                'bg-dark-bg border border-dark-border text-dark-text-muted'
              }`}>
                {isCompleted ? (
                  <CheckCircle className="w-4 h-4" />
                ) : (
                  <Icon className="w-4 h-4" />
                )}
              </div>
              <span className={`text-sm font-medium ${
                isCompleted ? 'text-emerald-400' :
                isActive ? 'text-marine-400' :
                'text-dark-text-muted'
              }`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {status?.current_step && (
        <div className="pt-2 border-t border-dark-border">
          <p className="text-xs text-dark-text-muted font-mono">{status.current_step}</p>
        </div>
      )}

      {status?.error && (
        <div className="flex items-center gap-2 text-red-400 bg-red-500/10 p-2 rounded-md">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span className="text-sm">{status.error}</span>
        </div>
      )}
    </div>
  );
}