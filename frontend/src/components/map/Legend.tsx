interface LegendProps {
  concentrations?: Array<{ label: string; color: string }>;
  riskLevels?: Array<{ label: string; color: string }>;
}

export function Legend({ 
  concentrations = [
    { label: 'Very High', color: '#8b0000' },
    { label: 'High', color: '#ff0000' },
    { label: 'Medium', color: '#ffa500' },
    { label: 'Low', color: '#ffff00' },
  ],
  riskLevels = [
    { label: 'Very High', color: '#8b0000' },
    { label: 'High', color: '#ff0000' },
    { label: 'Medium', color: '#ffa500' },
    { label: 'Low', color: '#ffff00' },
  ]
}: LegendProps) {
  return (
    <div className="panel p-3 min-w-[180px]">
      <p className="text-xs font-semibold text-dark-text-muted uppercase tracking-wider mb-2">Concentration</p>
      <div className="space-y-2 mb-4">
        {concentrations.map(item => (
          <div key={item.label} className="flex items-center gap-2">
            <div className="w-5 h-5 rounded" style={{ backgroundColor: item.color, opacity: 0.7 }} />
            <span className="text-sm text-dark-text">{item.label}</span>
          </div>
        ))}
      </div>
      <div className="border-t border-dark-border pt-3">
        <p className="text-xs font-semibold text-dark-text-muted uppercase tracking-wider mb-2">Risk Level</p>
        <div className="space-y-2">
          {riskLevels.map(item => (
            <div key={item.label} className="flex items-center gap-2">
              <div className="w-5 h-5 rounded" style={{ backgroundColor: item.color, opacity: 0.7 }} />
              <span className="text-sm text-dark-text">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}