import { Droplet, Wind, Waves, Sun, Cloud } from 'lucide-react';
import { formatNumber, formatArea, formatDuration } from '@/utils/formatting';
import type { SpillSummary } from '@/types';

interface SpillSummaryProps {
  data: SpillSummary | null;
  className?: string;
}

export function SpillSummary({ data, className = 'w-96 flex-shrink-0' }: SpillSummaryProps) {
  if (!data) {
    return (
      <div className={`${className} panel p-4`}>
        <p className="text-center text-dark-text-muted text-sm py-8">Run simulation to see spill summary</p>
      </div>
    );
  }

  const metrics = [
    { label: 'Total Spilled', value: `${formatNumber(data.total_spilled_tonnes)} tonnes`, icon: Droplet, color: 'text-orange-400' },
    { label: 'Slick Area', value: formatArea(data.estimated_slick_area_km2), icon: Wind, color: 'text-marine-400' },
    { label: 'Duration', value: formatDuration(data.simulation_duration_hours), icon: Waves, color: 'text-ocean-400' },
    { label: 'Weathering', value: `${data.weathering_percent.toFixed(1)}%`, icon: Cloud, color: 'text-gray-400' },
    { label: 'Evaporated', value: `${data.evaporation_percent.toFixed(1)}%`, icon: Sun, color: 'text-yellow-400' },
    { label: 'Dispersed', value: `${data.dispersion_percent.toFixed(1)}%`, icon: Waves, color: 'text-cyan-400' },
    { label: 'Remaining Surface Oil', value: `${formatNumber(data.remaining_surface_oil_tonnes)} tonnes`, icon: Droplet, color: 'text-red-400' },
  ];

  return (
    <div className={`${className} panel p-4 overflow-y-auto`}>
      <h3 className="text-sm font-semibold text-dark-text uppercase tracking-wider mb-4 flex items-center gap-2">
        <Droplet className="w-5 h-5 text-orange-400" />
        Spill Summary
      </h3>
      <div className="grid grid-cols-2 gap-3">
        {metrics.map((metric, i) => (
          <div key={i} className="card hover:bg-dark-panel-hover transition-colors">
            <div className="flex items-center gap-2 mb-1">
              <metric.icon className={`w-4 h-4 ${metric.color}`} />
              <span className="metric-label">{metric.label}</span>
            </div>
            <div className="metric-value font-mono">{metric.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}