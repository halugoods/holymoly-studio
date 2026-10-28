import sys
import os
sys.path.insert(0, r'C:\Users\ertyui\ZCodeProject\holymoly_studio\engine')
import flow_api_client

scenes = [
    {
        "prompt": "First-person action cam chest mount POV of an Indonesian angler battling an aggressive giant snakehead fish on a murky tropical river in Kalimantan. The bent carbon fishing rod vibrates intensely under heavy tension. The angler's hands grip the reel firmly, pumping the rod upward and cranking the handle. 4 meters away in the river water, the massive monster fish thrashes violently on the surface with white foamy splashes and flying water droplets. Handheld action sports camera motion, authentic jungle riverbank background, realistic water turbulence.",
        "aspect_ratio": "9:16",
        "duration": 6,
        "resolution": "720p",
        "download_quality": "upscaled"
    }
]

print("Queueing Scene 2...")
res = flow_api_client.generate(project="pov_mancing_raw_v1", scenes=scenes)
print("Generate response:", res)

job_ids = [j['id'] for j in res.get('jobs', [])]
if job_ids:
    print(f"Waiting for jobs {job_ids}...")
    finished_jobs = flow_api_client.wait_until_complete(job_ids, max_rounds=25)
    print("Finished jobs:", finished_jobs)
