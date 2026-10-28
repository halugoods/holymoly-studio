import urllib.request
import json
import time
import os

TOKEN_FILE = os.path.expanduser(r'~/.flow-mcp/token')
BASE_URL = 'http://127.0.0.1:8787'

def _get_token():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f'Token file not found at {TOKEN_FILE}')
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def call_api(endpoint: str, payload: dict, timeout: int = 60) -> dict:
    token = _get_token()
    url = f'{BASE_URL}/api/{endpoint}'
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            'Content-Type': 'application/json',
            'x-flow-token': token
        }
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def generate(project: str, scenes: list) -> dict:
    return call_api('generate', {'project': project, 'scenes': scenes})

def wait(job_ids: list = None, timeout_seconds: int = 40) -> dict:
    payload = {'timeout_seconds': timeout_seconds}
    if job_ids:
        payload['job_ids'] = job_ids
    return call_api('wait', payload, timeout=timeout_seconds + 10)

def status(detailed: bool = False) -> dict:
    return call_api('status', {'detailed': detailed}, timeout=45)

def wait_until_complete(job_ids: list, max_rounds: int = 30) -> list:
    print(f"Waiting for jobs {job_ids}...")
    for round_idx in range(max_rounds):
        res = wait(job_ids=job_ids, timeout_seconds=40)
        jobs = res.get('jobs', [])
        pacing = res.get('pacing')
        finished = res.get('finished', False)
        
        for j in jobs:
            print(f"  [Round {round_idx+1}] Job {j.get('id')} ({j.get('scene')}): {j.get('status')} {j.get('progress', '')}")
            if j.get('status') == 'failed':
                print(f"    Error: {j.get('error')}")
                
        if pacing:
            print(f"  Flow pacing: {pacing}")
            
        if finished:
            print("All jobs finished!")
            return jobs
            
        time.sleep(2)
        
    raise TimeoutError("Jobs did not finish within allocated rounds.")

if __name__ == '__main__':
    st = status(detailed=False)
    print("Flow Client initialized. Status:", st)
