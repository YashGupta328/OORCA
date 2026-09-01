import uvicorn
import asyncio
import httpx
from backend.api.main import app

async def test():
    config = uvicorn.Config(app, host='127.0.0.1', port=8000, log_level='info')
    server = uvicorn.Server(config)

    async def run_server():
        await server.serve()

    server_task = asyncio.create_task(run_server())
    await asyncio.sleep(2)  # Wait for server to start

    async with httpx.AsyncClient() as client:
        try:
            # Test health
            response = await client.get('http://127.0.0.1:8000/health', timeout=5)
            print('Health:', response.json())

            # Create incident
            incident_data = {
                'location': {'latitude': 18.9076, 'longitude': 72.8177},
                'spill': {
                    'amount': 100,
                    'unit': 'tonnes',
                    'oil_type': 'crude_oil',
                    'start_time': '2026-09-01T10:00:00',
                    'duration_hours': 72
                },
                'vessel': {
                    'name': 'MV Oceanic Star',
                    'vessel_type': 'oil_tanker',
                    'imo': '9732548'
                }
            }
            response = await client.post('http://127.0.0.1:8000/api/incidents', json=incident_data, timeout=10)
            print('Create incident:', response.status_code, response.json())
            incident_id = response.json()['incident_id']

            # Start simulation
            response = await client.post(f'http://127.0.0.1:8000/api/incidents/{incident_id}/simulate', timeout=10)
            print('Start simulation:', response.status_code, response.json())
            sim_run_id = response.json()['simulation_run_id']

            # Poll simulation status
            for i in range(10):
                await asyncio.sleep(1)
                response = await client.get(f'http://127.0.0.1:8000/api/simulation/runs/{sim_run_id}/status', timeout=5)
                status = response.json()
                print('Status {}: {} - {}% - {}'.format(i, status['status'], status['progress'], status['current_step']))
                if status['status'] in ('completed', 'failed'):
                    break

            # Get simulation run
            response = await client.get('http://127.0.0.1:8000/api/simulation/runs/{}'.format(sim_run_id), timeout=5)
            print('Simulation run:', response.status_code, response.json())

            # Get frames
            response = await client.get('http://127.0.0.1:8000/api/simulation/runs/{}/frames/0'.format(sim_run_id), timeout=5)
            frame = response.json()
            print('Frame 0: time_hours={}, features={}'.format(frame['time_hours'], len(frame['geojson']['features'])))

            # Assess damage
            response = await client.post('http://127.0.0.1:8000/api/damage/assess?simulation_run_id={}'.format(sim_run_id), timeout=15)
            print('Damage assessment:', response.status_code)
            damage = response.json()
            print('  Hazard score: {}'.format(damage['danger_assessment']['hazard_score']))
            print('  Ecological resources: {}'.format(len(damage['ecological_resources'])))
            print('  Shoreline impacts: {}'.format(len(damage['shoreline_impact'])))

        except Exception as e:
            print('Error:', e)
            import traceback
            traceback.print_exc()
        finally:
            server.should_exit = True

    await server_task

asyncio.run(test())