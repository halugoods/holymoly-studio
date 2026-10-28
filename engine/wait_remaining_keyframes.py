#!/usr/bin/env python3
"""
Wait for remaining Flow keyframe jobs to complete, then update storyboard records.
"""

import sys
import json
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from holymoly_studio.engine import flow_client

PROJECT_NAME = "IndonesiaHistory60s"
assets_dir = Path("c:/Users/ertyui/ZCodeProject/holymoly_studio/assets")
json_path = assets_dir / f"{PROJECT_NAME}_storyboard.json"

if not json_path.exists():
    raise RuntimeError(f"Storyboard JSON not found: {json_path}")

storyboard_data = json.loads(json_path.read_text(encoding="utf-8"))
job_ids = [r["job_id"] for r in storyboard_data]

print(f"Tracking {len(job_ids)} jobs for project '{PROJECT_NAME}'...")

start_time = time.time()
while True:
    wait_res = flow_client.request_api("wait", {
        "job_ids": job_ids,
        "timeout_seconds": 35,
    })
    
    current_jobs = wait_res.get("jobs", [])
    job_map = {j["id"]: j for j in current_jobs}
    
    done_count = sum(1 for j in current_jobs if j.get("status") == "done")
    failed_count = sum(1 for j in current_jobs if j.get("status") == "failed")
    running_count = len(job_ids) - done_count - failed_count
    
    elapsed = int(time.time() - start_time)
    print(f"[Wait +{elapsed}s] Done: {done_count}/12 | In-Progress: {running_count} | Failed: {failed_count}")

    if done_count + failed_count == len(job_ids):
        print("All jobs finished!")
        break

    time.sleep(2)

# Update storyboard JSON with final results
print("\nUpdating storyboard metadata and files...")
for r in storyboard_data:
    jid = r["job_id"]
    job_info = job_map.get(jid, {})
    status = job_info.get("status", r.get("status"))
    r["status"] = status
    files = job_info.get("files", [])
    if files:
        r["file_path"] = files[0]
        fp = Path(files[0])
        if fp.exists():
            r["file_exists"] = True
            r["file_size_kb"] = round(fp.stat().st_size / 1024, 1)

json_path.write_text(json.dumps(storyboard_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated {json_path}")

# Rebuild Markdown
md_lines = [
    f"# Storyboard 60 Detik: Sejarah Penjajahan Jepang di Indonesia (1942-1945)",
    f"**Project**: `{PROJECT_NAME}` | **Style**: Paper-Cut / Origami Diorama | **Aspect Ratio**: 9:16 (Vertical)\n",
    f"Pipeline ini mengimplementasikan **Mode A (Pakem Template Harness)** dari Holymoly Studio, menggunakan **0 Credits (GRATIS)** via Google Flow Image Generator untuk memetakan Opening dan Closing Keyframe di setiap scene sebelum proses video interpolation.\n",
    "| No | Scene | Frame | Status | File Path | Ukuran | Narasi Suara (TTS) |",
    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
]

for r in storyboard_data:
    status_icon = "✅" if r["file_exists"] else "❌"
    md_lines.append(
        f"| {r['index']:02d} | Scene {r['scene_num']} | **{r['frame_type'].capitalize()}**: {r['label']} | "
        f"{status_icon} `{r['status']}` | `{r['file_path']}` | {r['file_size_kb']} KB | \"{r['narration']}\" |"
    )

md_lines.append("\n## Detail Visual Prompts & Keyframes\n")
for r in storyboard_data:
    md_lines.append(f"### Frame {r['index']:02d}: {r['label']}")
    md_lines.append(f"- **Scene**: {r['scene_title']}")
    md_lines.append(f"- **Tipe**: `{r['frame_type'].upper()}` Frame (Durasi total scene: 10s)")
    md_lines.append(f"- **File Lokasi**: `{r['file_path']}` ({r['file_size_kb']} KB)")
    md_lines.append(f"- **Narasi Pengiring**: *\"{r['narration']}\"*")
    md_lines.append(f"- **English Prompt**: \n  > {r['prompt']}\n")

md_path = assets_dir / f"{PROJECT_NAME}_STORYBOARD.md"
md_path.write_text("\n".join(md_lines), encoding="utf-8")
print(f"Updated {md_path}")
print("ALL DONE!")
