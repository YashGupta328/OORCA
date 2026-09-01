/** Damage API service */

import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

export const damageApi = {
  async assessDamage(simulationRunId: string): Promise<any> {
    const response = await api.post('/damage/assess', null, { params: { simulation_run_id: simulationRunId } });
    return response.data;
  },

  async getAssessment(assessmentId: string): Promise<any> {
    const response = await api.get(`/damage/assessments/${assessmentId}`);
    return response.data;
  },
};

export default damageApi;