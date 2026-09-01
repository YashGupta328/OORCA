import { useState, useRef, useEffect } from 'react';
import { MapPin, Search, Ship, Droplet, Calendar, Clock, HelpCircle } from 'lucide-react';
import type { IncidentCreate, Location, SpillDetails, VesselDetails } from '@/types';

interface InputPanelProps {
  incident: IncidentCreate | null;
  onSubmit: (incident: IncidentCreate) => void;
  disabled: boolean;
}

export function InputPanel({ incident, onSubmit, disabled }: InputPanelProps) {
  const [location, setLocation] = useState<Location>(incident?.location || { latitude: 18.9076, longitude: 72.8177 });
  const [spill, setSpill] = useState<SpillDetails>(incident?.spill || {
    amount: 100,
    unit: 'tonnes',
    oil_type: 'crude_oil',
    start_time: new Date().toISOString().slice(0, 16),
    duration_hours: 72,
  });
  const [vessel, setVessel] = useState<VesselDetails>(incident?.vessel || {
    name: 'MV Oceanic Star',
    vessel_type: 'oil_tanker',
    imo: '9732548',
    length_m: 274,
    breadth_m: 48,
    draft_m: 16,
    heading_deg: 45,
  });
  const [showMapPicker, setShowMapPicker] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const mapPickerRef = useRef<HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (disabled) return;
    onSubmit({ location, spill, vessel });
  };

  // Click outside to close map picker
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (mapPickerRef.current && !mapPickerRef.current.contains(event.target as Node)) {
        setShowMapPicker(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <form onSubmit={handleSubmit} className="p-4 space-y-5 animate-in">
      {/* Location Section */}
      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <MapPin className="w-5 h-5 text-marine-400" />
          <h2 className="text-sm font-semibold text-dark-text uppercase tracking-wider">Location</h2>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="label">Latitude</label>
            <input
              type="number"
              step="0.0001"
              min="-90"
              max="90"
              className="input font-mono text-sm"
              value={location.latitude}
              onChange={e => setLocation(prev => ({ ...prev, latitude: parseFloat(e.target.value) }))}
              disabled={disabled}
            />
          </div>
          <div>
            <label className="label">Longitude</label>
            <input
              type="number"
              step="0.0001"
              min="-180"
              max="180"
              className="input font-mono text-sm"
              value={location.longitude}
              onChange={e => setLocation(prev => ({ ...prev, longitude: parseFloat(e.target.value) }))}
              disabled={disabled}
            />
          </div>
        </div>
        <div className="relative">
          <label className="label">Search Location</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dark-text-muted" />
            <input
              type="text"
              className="input pl-10"
              placeholder="Search: Mumbai, Alibaug, coordinates..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              onFocus={() => setShowMapPicker(true)}
              disabled={disabled}
            />
          </div>
          {showMapPicker && (
            <div className="absolute top-full left-0 right-0 mt-1 panel z-10" ref={mapPickerRef}>
              <p className="p-3 text-sm text-dark-text-muted text-center">Click on map to select location</p>
            </div>
          )}
        </div>
      </section>

      {/* Spill Details Section */}
      <section className="space-y-3 border-t border-dark-border pt-4">
        <div className="flex items-center gap-2">
          <Droplet className="w-5 h-5 text-orange-400" />
          <h2 className="text-sm font-semibold text-dark-text uppercase tracking-wider">Spill Details</h2>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="label">Amount</label>
            <input
              type="number"
              step="0.1"
              min="0.1"
              className="input font-mono text-sm"
              value={spill.amount}
              onChange={e => setSpill(prev => ({ ...prev, amount: parseFloat(e.target.value) }))}
              disabled={disabled}
            />
          </div>
          <div>
            <label className="label">Unit</label>
            <select className="select text-sm" value={spill.unit} onChange={e => setSpill(prev => ({ ...prev, unit: e.target.value as any }))} disabled={disabled}>
              <option value="tonnes">Tonnes</option>
              <option value="barrels">Barrels</option>
              <option value="liters">Liters</option>
              <option value="gallons">Gallons</option>
            </select>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="label">Oil Type</label>
            <select className="select text-sm" value={spill.oil_type} onChange={e => setSpill(prev => ({ ...prev, oil_type: e.target.value as any }))} disabled={disabled}>
              <option value="crude_oil">Crude Oil</option>
              <option value="diesel">Diesel</option>
              <option value="heavy_fuel_oil">Heavy Fuel Oil</option>
              <option value="gasoline">Gasoline</option>
              <option value="jet_fuel">Jet Fuel</option>
            </select>
          </div>
          <div>
            <label className="label">Start Time (UTC)</label>
            <input
              type="datetime-local"
              className="input font-mono text-sm"
              value={spill.start_time}
              onChange={e => setSpill(prev => ({ ...prev, start_time: e.target.value }))}
              disabled={disabled}
            />
          </div>
        </div>
        <div>
          <label className="label">Duration (hours)</label>
          <input
            type="number"
            min="1"
            max="168"
            className="input font-mono text-sm"
            value={spill.duration_hours}
            onChange={e => setSpill(prev => ({ ...prev, duration_hours: parseInt(e.target.value) }))}
            disabled={disabled}
          />
        </div>
      </section>

      {/* Vessel Details Section */}
      <section className="space-y-3 border-t border-dark-border pt-4">
        <div className="flex items-center gap-2">
          <Ship className="w-5 h-5 text-ocean-400" />
          <h2 className="text-sm font-semibold text-dark-text uppercase tracking-wider">Vessel Details (Optional)</h2>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="label">Vessel Name</label>
            <input
              type="text"
              className="input text-sm"
              value={vessel.name || ''}
              onChange={e => setVessel(prev => ({ ...prev, name: e.target.value }))}
              disabled={disabled}
            />
          </div>
          <div>
            <label className="label">IMO Number</label>
            <input
              type="text"
              className="input text-sm font-mono"
              value={vessel.imo || ''}
              onChange={e => setVessel(prev => ({ ...prev, imo: e.target.value }))}
              disabled={disabled}
              placeholder="9732548"
            />
          </div>
          <div>
            <label className="label">Vessel Type</label>
            <select className="select text-sm" value={vessel.vessel_type || ''} onChange={e => setVessel(prev => ({ ...prev, vessel_type: e.target.value as any || undefined }))} disabled={disabled}>
              <option value="">Select type</option>
              <option value="oil_tanker">Oil Tanker</option>
              <option value="cargo">Cargo</option>
              <option value="fishing">Fishing</option>
              <option value="passenger">Passenger</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label className="label">Heading (°)</label>
            <input
              type="number"
              min="0"
              max="359"
              step="1"
              className="input font-mono text-sm"
              value={vessel.heading_deg || ''}
              onChange={e => setVessel(prev => ({ ...prev, heading_deg: e.target.value ? parseInt(e.target.value) : undefined }))}
              disabled={disabled}
              placeholder="45"
            />
          </div>
        </div>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="label">Length (m)</label>
            <input
              type="number"
              step="0.1"
              min="0"
              className="input font-mono text-sm"
              value={vessel.length_m || ''}
              onChange={e => setVessel(prev => ({ ...prev, length_m: e.target.value ? parseFloat(e.target.value) : undefined }))}
              disabled={disabled}
            />
          </div>
          <div>
            <label className="label">Breadth (m)</label>
            <input
              type="number"
              step="0.1"
              min="0"
              className="input font-mono text-sm"
              value={vessel.breadth_m || ''}
              onChange={e => setVessel(prev => ({ ...prev, breadth_m: e.target.value ? parseFloat(e.target.value) : undefined }))}
              disabled={disabled}
            />
          </div>
          <div>
            <label className="label">Draft (m)</label>
            <input
              type="number"
              step="0.1"
              min="0"
              className="input font-mono text-sm"
              value={vessel.draft_m || ''}
              onChange={e => setVessel(prev => ({ ...prev, draft_m: e.target.value ? parseFloat(e.target.value) : undefined }))}
              disabled={disabled}
            />
          </div>
        </div>
      </section>

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full btn-primary py-3 text-lg font-semibold disabled:opacity-50"
        disabled={disabled}
      >
        Run Simulation
      </button>
    </form>
  );
}