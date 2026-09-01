import { useState, useEffect, useCallback, useRef } from 'react';
import { MapView } from '@/components/map/MapView';
import { InputPanel } from '@/components/simulation/InputPanel';
import { SimulationControls } from '@/components/simulation/SimulationControls';
import { Timeline } from '@/components/simulation/Timeline';
import { SimulationStatus } from '@/components/simulation/SimulationStatus';
import { SpillSummary } from '@/components/results/SpillSummary';
import { DangerAssessment } from '@/components/results/DangerAssessment';
import { EcologicalResources } from '@/components/results/EcologicalResources';
import { ShorelineImpact } from '@/components/results/ShorelineImpact';
import { Header } from '@/components/layout/Header';
import { StatusBar } from '@/components/layout/StatusBar';
import { simulationApi } from '@/services/simulationApi';
import { damageApi } from '@/services/damageApi';
import type { Incident, IncidentCreate, SimulationRun, SimulationStatus as SimStatus, SpillFrame, DamageAssessment } from '@/types';
import { mockIncident, mockSimulationRun, mockDamageAssessment } from '@/mock/simulation';

interface SimulatorState {
  // Input
  incident: IncidentCreate | null;
  // Simulation
  simulationRun: SimulationRun | null;
  simStatus: SimStatus | null;
  frames: SpillFrame[];
  currentFrameIndex: number;
  // Results
  damageAssessment: DamageAssessment | null;
  // UI state
  isSimulating: boolean;
  isLoadingResults: boolean;
  error: string | null;
  activeTab: 'summary' | 'danger' | 'ecology' | 'shoreline';
}

const INITIAL_STATE: SimulatorState = {
  incident: null,
  simulationRun: null,
  simStatus: null,
  frames: [],
  currentFrameIndex: 0,
  damageAssessment: null,
  isSimulating: false,
  isLoadingResults: false,
  error: null,
  activeTab: 'summary',
};

export function Simulator() {
  const [state, setState] = useState<SimulatorState>(INITIAL_STATE);
  const [mapReady, setMapReady] = useState(false);
  const statusPollInterval = useRef<number | null>(null);
  const framePollInterval = useRef<number | null>(null);

  // Poll simulation status
  const pollSimulationStatus = useCallback(async (simulationRunId: string) => {
    try {
      const status = await simulationApi.getSimulationStatus(simulationRunId);
      setState(prev => ({ ...prev, simStatus: status }));

      if (status.status === 'completed') {
        if (statusPollInterval.current) {
          window.clearInterval(statusPollInterval.current);
          statusPollInterval.current = null;
        }
        // Fetch frames
        const run = await simulationApi.getSimulationRun(simulationRunId);
        setState(prev => ({ ...prev, simulationRun: run, frames: run.frames || [], isSimulating: false }));
        // Auto-calculate damage
        await calculateDamage(simulationRunId);
      } else if (status.status === 'failed') {
        if (statusPollInterval.current) {
          window.clearInterval(statusPollInterval.current);
          statusPollInterval.current = null;
        }
        setState(prev => ({ 
          ...prev, 
          isSimulating: false, 
          error: status.current_step || 'Simulation failed' 
        }));
      }
    } catch (err) {
      console.error('Failed to poll simulation status:', err);
    }
  }, []);

  const calculateDamage = useCallback(async (simulationRunId: string) => {
    setState(prev => ({ ...prev, isLoadingResults: true, error: null }));
    try {
      const assessment = await damageApi.assessDamage(simulationRunId);
      setState(prev => ({ ...prev, damageAssessment: assessment, isLoadingResults: false }));
    } catch (err) {
      console.error('Failed to calculate damage:', err);
      setState(prev => ({ 
        ...prev, 
        isLoadingResults: false, 
        error: 'Failed to calculate damage assessment' 
      }));
    }
  }, []);

  const handleCreateIncident = useCallback(async (incident: IncidentCreate) => {
    setState(prev => ({ ...prev, error: null }));
    try {
      const created = await simulationApi.createIncident(incident);
      setState(prev => ({ ...prev, incident: created }));
      // Auto-start simulation
      const sim = await simulationApi.runSimulation(created.incident_id, 'mock');
      setState(prev => ({ ...prev, isSimulating: true }));
      // Start polling
      if (statusPollInterval.current) window.clearInterval(statusPollInterval.current);
      statusPollInterval.current = window.setInterval(() => pollSimulationStatus(sim.simulation_run_id), 1000);
      // Initial poll
      await pollSimulationStatus(sim.simulation_run_id);
    } catch (err) {
      console.error('Failed to create incident:', err);
      setState(prev => ({ ...prev, error: 'Failed to create incident' }));
    }
  }, [pollSimulationStatus]);

  const handleReset = useCallback(() => {
    if (statusPollInterval.current) window.clearInterval(statusPollInterval.current);
    if (framePollInterval.current) window.clearInterval(framePollInterval.current);
    setState(INITIAL_STATE);
  }, []);

  const handleFrameChange = useCallback((index: number) => {
    setState(prev => ({ ...prev, currentFrameIndex: index }));
  }, []);

  const handleTabChange = useCallback((tab: SimulatorState['activeTab']) => {
    setState(prev => ({ ...prev, activeTab: tab }));
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (statusPollInterval.current) window.clearInterval(statusPollInterval.current);
      if (framePollInterval.current) window.clearInterval(framePollInterval.current);
    };
  }, []);

  return (
    <div className="h-full w-full flex flex-col bg-dark-bg">
      <Header onReset={handleReset} />
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Input & Controls */}
        <div className="w-96 flex-shrink-0 flex flex-col border-r border-dark-border bg-dark-panel">
          <div className="flex-1 overflow-y-auto">
            <InputPanel 
              incident={state.incident}
              onSubmit={handleCreateIncident}
              disabled={state.isSimulating}
            />
            <SimulationControls 
              isSimulating={state.isSimulating}
              onReset={handleReset}
              disabled={!state.incident}
            />
            <SimulationStatus 
              status={state.simStatus}
              isSimulating={state.isSimulating}
            />
          </div>
          <div className="p-4 border-t border-dark-border">
            <Timeline
              frames={state.frames}
              currentIndex={state.currentFrameIndex}
              onFrameChange={handleFrameChange}
              disabled={state.frames.length === 0}
            />
          </div>
        </div>

        {/* Map View */}
        <div className="flex-1 relative min-w-0">
          <MapView
            frames={state.frames}
            currentFrameIndex={state.currentFrameIndex}
            damageAssessment={state.damageAssessment}
            incident={state.incident}
            onMapReady={setMapReady}
          />
        </div>
      </div>

      {/* Bottom Dashboard */}
      <div className="h-64 flex-shrink-0 border-t border-dark-border bg-dark-panel">
        <div className="h-full flex overflow-x-auto">
          <SpillSummary 
            data={state.damageAssessment?.spill_summary}
            className="w-96 flex-shrink-0"
          />
          <DangerAssessment 
            data={state.damageAssessment?.danger_assessment}
            className="w-96 flex-shrink-0"
          />
          <EcologicalResources 
            resources={state.damageAssessment?.ecological_resources || []}
            className="w-96 flex-shrink-0"
          />
          <ShorelineImpact 
            impacts={state.damageAssessment?.shoreline_impact || []}
            className="w-96 flex-shrink-0"
          />
        </div>
      </div>

      <StatusBar 
        error={state.error}
        isSimulating={state.isSimulating}
        isLoadingResults={state.isLoadingResults}
      />
    </div>
  );
}

export default Simulator;