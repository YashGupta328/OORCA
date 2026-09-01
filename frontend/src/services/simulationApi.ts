/** Simulation API service */

import axios from 'axios';
import type { Incident, IncidentCreate, SimulationRun, SimulationStatus, SpillFrame } from '@/types';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

export const simulationApi = {
  async createIncident(incident: IncidentCreate): Promise<Incident> {
    const response = await api.post('/incidents', incident);
    return response.data;
  },

  async listIncidents(limit = 50, offset = 0): Promise<Incident[]> {
    const response = await api.get('/incidents', { params: { limit, offset } });
    return response.data;
  },

  async getIncident(incidentId: string): Promise<Incident> {
    const response = await api.get(`/incidents/${incidentId}`);
    return response.data;
  },

  async runSimulation(incidentId: string, provider: 'mock' | 'opendrift' = 'mock'): Promise<{ simulation_run_id: string; status: string }> {
    const response = await api.post('/simulation/run', { incident_id: incidentId, provider });
    return response.data;
  },

  async getSimulationRun(simulationRunId: string): Promise<SimulationRun> {
    const response = await api.get(`/simulation/runs/${simulationRunId}`);
    return response.data;
  },

  async getSimulationStatus(simulationRunId: string): Promise<SimulationStatus> {
    const response = await api.get(`/simulation/runs/${simulationRunId}/status`);
    return response.data;
  },

  async getFrame(simulationRunId: string, frameIndex: number): Promise<SpillFrame> {
    const response = await api.get(`/simulation/runs/${simulationRunId}/frames/${frameIndex}`);
    return response.data;
  },

  async getWindCurrentFrame(simulationRunId: string, frameIndex: number): Promise<any> {
    const response = await api.get(`/simulation/runs/${simulationRunId}/wind-current/${frameIndex}`);
    return response.data;
  },

  async assessDamage(simulationRunId: string): Promise<any> {
    const response = await api.post('/damage/assess', null, { params: { simulation_run_id: simulationRunId } });
    return response.data;
  },

  async getDamageAssessment(assessmentId: string): Promise<any> {
    const response = await api.get(`/damage/assessments/${assessmentId}`);
    return response.data;
  },

  async requestSatelliteEvidence(incidentId: string, provider: string = 'copernicus'): Promise<any> {
    const response = await api.post(`/incidents/${incidentId}/satellite-evidence`, null, { params: { provider } });
    return response.data;
  },
};

export default simulationApi;