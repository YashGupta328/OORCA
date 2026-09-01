/** Formatting utilities */

export function formatNumber(num: number, precision: number = 1): string {
  if (num >= 1e6) return (num / 1e6).toFixed(precision) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(precision) + 'K';
  return num.toFixed(precision);
}

export function formatArea(km2: number): string {
  if (km2 >= 1) return `${km2.toFixed(1)} km²`;
  return `${(km2 * 1e6).toFixed(0)} m²`;
}

export function formatDuration(hours: number): string {
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  const remainingHours = hours % 24;
  return remainingHours > 0 ? `${days}d ${remainingHours}h` : `${days}d`;
}

export function formatTimeHours(hours: number): string {
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  if (m === 0) return `${h}:00`;
  return `${h}:${m.toString().padStart(2, '0')}`;
}

export function formatRiskLevel(level: string): { label: string; class: string } {
  const levels: Record<string, { label: string; class: string }> = {
    LOW: { label: 'Low', class: 'text-green-400' },
    MEDIUM: { label: 'Medium', class: 'text-yellow-400' },
    HIGH: { label: 'High', class: 'text-orange-400' },
    VERY_HIGH: { label: 'Very High', class: 'text-red-400' },
  };
  return levels[level] || { label: level, class: 'text-gray-400' };
}

export function formatTimestamp(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function formatRelativeTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  const diff = Date.now() - d.getTime();
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (minutes > 0) return `${minutes}m ago`;
  return 'just now';
}