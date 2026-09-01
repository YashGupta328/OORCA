interface MapPopupProps {
  coordinates?: [number, number];
  title: string;
  children: React.ReactNode;
  onClose: () => void;
}

export function MapPopup({ coordinates, title, children, onClose }: MapPopupProps) {
  return (
    <div className="panel p-3 min-w-[250px] max-w-[350px] animate-in">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-dark-text">{title}</h3>
        <button onClick={onClose} className="text-dark-text-muted hover:text-dark-text p-1">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      {coordinates && (
        <p className="text-xs text-dark-text-muted font-mono mb-2">
          {coordinates[1].toFixed(4)}°N, {coordinates[0].toFixed(4)}°E
        </p>
      )}
      <div>{children}</div>
    </div>
  );
}