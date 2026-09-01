import { Wifi, WifiOff, Database, Server, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

interface StatusBarProps {
  error: string | null;
  isSimulating: boolean;
  isLoadingResults: boolean;
}

export function StatusBar({ error, isSimulating, isLoadingResults }: StatusBarProps) {
  const getApiStatus = () => {
    // In production, this would check actual API health
    return 'connected';
  };

  return (
    <footer className="h-10 px-4 border-t border-dark-border bg-dark-panel/80 backdrop-blur-sm flex items-center justify-between text-xs text-dark-text-muted">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 text-green-400">
          <Wifi className="w-3.5 h-3.5" />
          <span>API Connected</span>
        </div>
        <div className="flex items-center gap-1.5 text-ocean-400">
          <Database className="w-3.5 h-3.5" />
          <span>PostGIS Ready</span>
        </div>
        <div className="flex items-center gap-1.5 text-marine-400">
          <Server className="w-3.5 h-3.5" />
          <span>Mock Provider Active</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {error && (
          <div className="flex items-center gap-1.5 text-red-400 animate-pulse">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>{error}</span>
          </div>
        )}

        {(isSimulating || isLoadingResults) && (
          <div className="flex items-center gap-1.5 text-marine-400">
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span>{isSimulating ? 'Simulating...' : 'Calculating Impact...'}</span>
          </div>
        )}

        {!error && !isSimulating && !isLoadingResults && (
          <div className="flex items-center gap-1.5 text-emerald-400">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Ready</span>
          </div>
        )}

        <div className="text-dark-text-muted/50 font-mono">
          {new Date().toLocaleTimeString()}
        </div>
      </div>
    </footer>
  );
}