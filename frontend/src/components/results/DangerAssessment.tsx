import { AlertTriangle, Shield, TreePine, Waves, Users, Wrench } from 'lucide-react';
import { formatRiskLevel } from '@/utils/formatting';
import type { DangerAssessment } from '@/types';

interface DangerAssessmentProps {
  data: DangerAssessment | null;
  className?: string;
}

export function DangerAssessment({ data, className = 'w-96 flex-shrink-0' }: DangerAssessmentProps) {
  if (!data) {
    return (
      <div className={`${className} panel p-4`}>
        <p className="text-center text-dark-text-muted text-sm py-8">Run simulation to see danger assessment</p>
      </div>
    );
  }

  const risks = [
    { label: 'Overall Risk', value: data.overall_risk, icon: AlertTriangle },
    { label: 'Environmental Risk', value: data.environmental_risk, icon: TreePine },
    { label: 'Shoreline Risk', value: data.shoreline_risk, icon: Waves },
    { label: 'Human Exposure', value: data.human_exposure_risk, icon: Users },
    { label: 'Cleanup Difficulty', value: data.cleanup_difficulty, icon: Wrench },
  ];

  return (
    <div className={`${className} panel p-4 overflow-y-auto`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-dark-text uppercase tracking-wider flex items-center gap-2">
          <Shield className="w-5 h-5 text-red-400" />
          Danger Assessment
        </h3>
        <div className="text-right">
          <div className="text-3xl font-bold font-mono text-red-400">{data.hazard_score.toFixed(1)}</div>
          <div className="text-xs text-dark-text-muted">Hazard Score (0-100)</div>
        </div>
      </div>
      <div className="space-y-3">
        {risks.map((risk, i) => {
          const { label, value, icon: Icon } = risk;
          const { label: riskLabel, class: riskClass } = formatRiskLevel(value);
          return (
            <div key={i} className="card hover:bg-dark-panel-hover transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Icon className="w-4 h-4 text-dark-text-muted" />
                  <span className="text-sm text-dark-text-muted">{label}</span>
                </div>
                <span className={`font-medium text-sm ${riskClass}`}>{riskLabel}</span>
              </div>
            </div>
          );
        })}
      </div>
      <p className="text-xs text-dark-text-muted/50 mt-4 text-center">
        <em>Baseline Ecological Hazard Score — Not a legally valid damage assessment</em>
      </p>
    </div>
  );
}