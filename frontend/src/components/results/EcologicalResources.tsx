import { TreePine, Waves, Fish, Bug, Shield, Leaf } from 'lucide-react';
import { formatRiskLevel, formatArea } from '@/utils/formatting';
import type { ESIResource } from '@/types';

interface EcologicalResourcesProps {
  resources: ESIResource[];
  className?: string;
}

const RESOURCE_ICONS: Record<string, any> = {
  mangrove: TreePine,
  coral_reef: Waves,
  seagrass: Leaf,
  fish_habitat: Fish,
  sea_turtle_habitat: Bug,
  dolphin_habitat: Bug,
  protected_area: Shield,
  saltmarsh: Leaf,
};

export function EcologicalResources({ resources, className = 'w-96 flex-shrink-0' }: EcologicalResourcesProps) {
  if (resources.length === 0) {
    return (
      <div className={`${className} panel p-4`}>
        <p className="text-center text-dark-text-muted text-sm py-8">Run simulation to see ecological resources at risk</p>
      </div>
    );
  }

  // Sort by risk level
  const riskOrder = { VERY_HIGH: 4, HIGH: 3, MEDIUM: 2, LOW: 1 };
  const sorted = [...resources].sort((a, b) => (riskOrder[b.risk_level || 'LOW'] || 0) - (riskOrder[a.risk_level || 'LOW'] || 0));

  return (
    <div className={`${className} panel p-4 overflow-y-auto`}>
      <h3 className="text-sm font-semibold text-dark-text uppercase tracking-wider mb-4 flex items-center gap-2">
        <TreePine className="w-5 h-5 text-green-400" />
        Ecological Resources at Risk
      </h3>
      <div className="space-y-2">
        {sorted.map((resource, i) => {
          const Icon = RESOURCE_ICONS[resource.resource_type] || Shield;
          const { label: riskLabel, class: riskClass } = formatRiskLevel(resource.risk_level || 'LOW');
          const presence = resource.affected_area_km2 ? `${formatArea(resource.affected_area_km2)} (${resource.sensitivity_score}% sens.)` : 'Present';

          return (
            <div key={i} className="card hover:bg-dark-panel-hover transition-colors group">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 min-w-0">
                  <Icon className="w-5 h-5 text-ocean-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-dark-text truncate">{resource.resource_name}</p>
                    <p className="text-xs text-dark-text-muted truncate capitalize">{resource.resource_type.replace('_', ' ')}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-right">
                  <div className="hidden sm:block text-xs text-dark-text-muted">
                    {presence}
                  </div>
                  <span className={`font-medium text-sm ${riskClass} whitespace-nowrap`}>{riskLabel}</span>
                </div>
              </div>
              <div className="mt-1 flex items-center gap-2 text-xs text-dark-text-muted">
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: riskClass.includes('red') ? '#ef4444' : riskClass.includes('orange') ? '#f97316' : riskClass.includes('yellow') ? '#eab308' : '#22c55e' }} />
                <span>Sensitivity: {resource.sensitivity_score}/100</span>
                {resource.affected_area_km2 && (
                  <>·</> <span>Affected: {formatArea(resource.affected_area_km2)}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}