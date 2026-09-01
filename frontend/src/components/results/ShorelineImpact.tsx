import { MapPin, Clock, AlertTriangle, Waves } from 'lucide-react';
import { formatRiskLevel, formatDuration } from '@/utils/formatting';
import type { ShorelineImpact } from '@/types';

interface ShorelineImpactProps {
  impacts: ShorelineImpact[];
  className?: string;
}

export function ShorelineImpact({ impacts, className = 'w-96 flex-shrink-0' }: ShorelineImpactProps) {
  if (impacts.length === 0) {
    return (
      <div className={`${className} panel p-4`}>
        <p className="text-center text-dark-text-muted text-sm py-8">Run simulation to see shoreline impact</p>
      </div>
    );
  }

  // Sort by arrival time
  const sorted = [...impacts].sort((a, b) => {
    const aTime = a.arrival_time_hours?.[0] || 999;
    const bTime = b.arrival_time_hours?.[0] || 999;
    return aTime - bTime;
  });

  return (
    <div className={`${className} panel p-4 overflow-y-auto`}>
      <h3 className="text-sm font-semibold text-dark-text uppercase tracking-wider mb-4 flex items-center gap-2">
        <Waves className="w-5 h-5 text-blue-400" />
        Shoreline Impact
      </h3>
      <div className="space-y-2">
        {sorted.map((impact, i) => {
          const { label: riskLabel, class: riskClass } = formatRiskLevel(impact.impact_level);
          const arrival = impact.arrival_time_hours 
            ? `${impact.arrival_time_hours[0]}-${impact.arrival_time_hours[1]}h`
            : 'Unknown';
          const distance = impact.distance_km ? `${impact.distance_km.toFixed(1)} km` : 'Unknown';

          return (
            <div key={i} className="card hover:bg-dark-panel-hover transition-colors group">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 min-w-0">
                  <MapPin className="w-5 h-5 text-red-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-dark-text truncate">{impact.location}</p>
                    <p className="text-xs text-dark-text-muted truncate">{distance} from spill origin</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-right">
                  <div className="hidden sm:block text-xs text-dark-text-muted">
                    <Clock className="w-3 h-3 inline mr-1" />
                    {arrival}
                  </div>
                  <span className={`font-medium text-sm ${riskClass} whitespace-nowrap`}>{riskLabel}</span>
                </div>
              </div>
              <div className="mt-1 flex items-center gap-2 text-xs text-dark-text-muted">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: riskClass.includes('red') ? '#ef4444' : riskClass.includes('orange') ? '#f97316' : riskClass.includes('yellow') ? '#eab308' : '#22c55e' }} />
                <span>Arrival: {arrival}</span>
                {impact.distance_km && <span>• Distance: {distance}</span>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}