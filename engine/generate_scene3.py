import sys
import os
sys.path.insert(0, r'C:\Users\ertyui\ZCodeProject\holymoly_studio\engine')
import flow_api_client

scenes = [
    {
        "prompt": "First-person action cam chest mount POV of an Indonesian angler landing a massive wild giant snakehead predator fish (Toman Babon) beside a wooden boat on a tropical river. The gleaming yellow-green and black mottled monster fish thrashes violently beside the boat with wide open jaws and sharp teeth, splashing clear river water. The angler's gloved hand clamps a metal lip grip onto the fish's lower jaw and lifts the heavy monster fish out of the water. Triumphant action sports footage, bright morning sun reflecting on wet fish scales, authentic outdoor fishing realism.",
        "aspect_ratio": "9:16",
        "duration": 6,
        "resolution": "720p",
        "download_quality": "upscaled"
    }
]

print("Queueing Scene 3...")
res = flow_api_client.generate(project="pov_mancing_raw_v1", scenes=scenes)
print("Generate response:", res)

job_ids = [j['id'] for j in res.get('jobs', [])]
if job_ids:
    print(f"Waiting for jobs {job_ids}...")
    finished_jobs = flow_api_client.wait_until_complete(job_ids, max_rounds=25)
    print("Finished jobs:", finished_jobs)
