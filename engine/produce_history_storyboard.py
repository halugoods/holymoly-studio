#!/usr/bin/env python3
"""
Holymoly Studio - Indonesia History 60s Storyboard Keyframe Production
Produces 12 Storyboard Keyframes (0 Credits / Free) via Flow MCP Studio
"""

import sys
import os
import json
import time
from pathlib import Path

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding="utf-8")

# Ensure ZCodeProject is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from holymoly_studio.engine import flow_client

PROJECT_NAME = "IndonesiaHistory60s"
ASPECT_RATIO = "9:16"
STYLE_SUFFIX = (
    "layered papercraft origami stop-motion, handcrafted paper cut textures, "
    "cinematic warm lighting, detailed historical diorama, vertical 9:16, centered composition, high quality."
)

SCENES = [
    {
        "scene_num": 1,
        "title": "Scene 1: Kedatangan Armada Jepang di Jawa (Maret 1942)",
        "narration": "Maret 1942. Di tengah runtuhnya Hindia Belanda, tentara Jepang mendarat di Jawa membawa propaganda Saudara Tua.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 1 Opening: Armada Laut Jepang Mendarat",
                "prompt": (
                    f"Japanese navy fleet of warships approaching the shores of Java island in 1942, "
                    f"paper-cut waves, dramatic sunrise on tropical sea, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 1 Closing: Sambutan Rakyat Batavia",
                "prompt": (
                    f"Crowds of Indonesian civilians in colonial Batavia waving small Hinomaru paper flags "
                    f"with hopeful yet cautious facial expressions, colonial street buildings made of cut paper, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
    {
        "scene_num": 2,
        "title": "Scene 2: Propaganda Gerakan Tiga A (1942-1943)",
        "narration": "Slogan Tiga A bergema di mana-mana. Jepang Cahaya Asia, Pelindung Asia, Pemimpin Asia. Tapi harapan rakyat perlahan memudar.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 2 Opening: Baliho Propaganda Tiga A",
                "prompt": (
                    f"Large wooden billboard in colonial town with Gerakan 3A propaganda slogans "
                    f"'Jepang Cahaya Asia, Jepang Pelindung Asia, Jepang Pemimpin Asia', "
                    f"Japanese soldier standing guard, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 2 Closing: Poster Terkoyak & Sawah Kering",
                "prompt": (
                    f"Torn paper propaganda poster peeling away from wooden post revealing barren drought-stricken "
                    f"empty rice fields behind it, melancholic evening shadows, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
    {
        "scene_num": 3,
        "title": "Scene 3: Romusha & Jalur Kereta Maut (1943-1944)",
        "narration": "Beras disita, romusha dikerahkan paksa menembus hutan rimba membangun jalur rel maut demi mesin perang Pasifik.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 3 Opening: Kerja Paksa Romusha di Rimba",
                "prompt": (
                    f"Indonesian forced laborers (Romusha) carving a railway track through dense tropical jungle "
                    f"with picks and shovels, layered paper trees and misty mountains, dramatic rim lighting, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 3 Closing: Penderitaan di Bawah Hujan Lebat",
                "prompt": (
                    f"Exhausted Romusha workers resting beside newly laid iron railroad tracks under torrential tropical rain, "
                    f"paper rain drops streaks, moody atmospheric lighting, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
    {
        "scene_num": 4,
        "title": "Scene 4: Kobaran Api & Pembentukan PETA (1943-1945)",
        "narration": "Dari tekanan lahirlah perlawanan. Pemuda dilatih militer dalam PETA, yang justru menjadi cikal bakal bara api tentara nasional.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 4 Opening: Pelatihan Militer Pemuda PETA",
                "prompt": (
                    f"Young Indonesian youth in PETA military uniforms with peci caps training with wooden rifles "
                    f"on a grassy field, disciplined formation, crisp morning sun, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 4 Closing: Sorot Mata Berani Supriyadi",
                "prompt": (
                    f"Close-up of young officer Supriyadi looking resolute and determined at night under paper-cut full moon, "
                    f"shadows of rebellion, heroic expression, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
    {
        "scene_num": 5,
        "title": "Scene 5: Jatuhnya Bom Atom & Rengasdengklok (Agustus 1945)",
        "narration": "Agustus 1945. Hiroshima dan Nagasaki luluh lantak. Para pemuda bertindak cepat mendesak Bung Karno di Rengasdengklok.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 5 Opening: Surat Kabar Menyerahnya Jepang",
                "prompt": (
                    f"Vintage paper newspaper headline announcing Japan's unconditional surrender after atomic bomb, "
                    f"glowing kerosene lamp on paper desk, dramatic chiaroscuro shadows, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 5 Closing: Perumusan di Rumah Rengasdengklok",
                "prompt": (
                    f"Soekarno, Mohammad Hatta, and youth leaders in a rustic wooden house in Rengasdengklok "
                    f"intensely drafting proclamation papers around a wooden table, warm lantern glow, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
    {
        "scene_num": 6,
        "title": "Scene 6: Fajar Kemerdekaan 17 Agustus 1945",
        "narration": "17 Agustus 1945. Di Pegangsaan Timur, teks proklamasi dibacakan. Dari tiga setengah tahun derita, lahirlah Indonesia Merdeka.",
        "duration_sec": 10,
        "frames": [
            {
                "frame_type": "opening",
                "label": "Scene 6 Opening: Pembacaan Teks Proklamasi",
                "prompt": (
                    f"Soekarno speaking into a vintage standing microphone on front porch of Pegangsaan Timur 56 Jakarta, "
                    f"Hatta standing beside him, crowds of paper silhouettes listening in reverence, {STYLE_SUFFIX}"
                ),
            },
            {
                "frame_type": "closing",
                "label": "Scene 6 Closing: Kibaran Sang Saka Merah Putih",
                "prompt": (
                    f"The iconic red and white Merah Putih flag rising proudly on tall bamboo flagpole "
                    f"against vibrant clear blue paper-cut sky and white origami clouds, triumphant golden sunrise, {STYLE_SUFFIX}"
                ),
            },
        ],
    },
]


def run():
    print("=" * 60)
    print(f"🎬 HOLYMOLY STUDIO: {PROJECT_NAME}")
    print("Mode: Storyboard Keyframe Production (0 Credits / Free)")
    print(f"Total Scenes: {len(SCENES)} (12 Keyframes Total, 9:16 Vertical)")
    print("=" * 60)

    # 1. Check status
    print("\n[Step 1] Verifying Flow MCP Studio Daemon...")
    status = flow_client.check_status()
    flow_info = status.get("flow", {})
    print(f"  SignedIn: {flow_info.get('signedIn')}")
    print(f"  Plan: {flow_info.get('plan')}")
    print(f"  Remaining Credits: {flow_info.get('credits_remaining')}")
    print(f"  Active Composer: {flow_info.get('composer')}")

    if not flow_info.get("signedIn"):
        raise RuntimeError("Flow MCP is not signed in!")

    # 2. Prepare payload
    print("\n[Step 2] Queuing 12 Keyframe Generation Jobs...")
    scenes_payload = []
    frame_meta = []
    for sc in SCENES:
        for fr in sc["frames"]:
            scenes_payload.append({
                "prompt": fr["prompt"],
                "type": "image",
                "aspect_ratio": ASPECT_RATIO,
                "max_credits": 0,
            })
            frame_meta.append({
                "scene_num": sc["scene_num"],
                "scene_title": sc["title"],
                "narration": sc["narration"],
                "frame_type": fr["frame_type"],
                "label": fr["label"],
                "prompt": fr["prompt"],
            })

    gen_res = flow_client.request_api("generate", {
        "project": PROJECT_NAME,
        "scenes": scenes_payload,
    })

    jobs = gen_res.get("jobs", [])
    job_ids = [j["id"] for j in jobs]
    print(f"Successfully queued {len(job_ids)} jobs:")
    for idx, (jid, meta) in enumerate(zip(job_ids, frame_meta)):
        print(f"  [{idx+1:02d}/12] Job ID: {jid} -> {meta['label']}")

    # 3. Wait for all jobs to complete
    print("\n[Step 3] Waiting for Flow to render and download all keyframes...")
    timeout_total = 900  # 15 minutes max
    start_time = time.time()
    last_report_time = 0

    while time.time() - start_time < timeout_total:
        wait_res = flow_client.request_api("wait", {
            "job_ids": job_ids,
            "timeout_seconds": 35,
        })
        
        current_jobs = wait_res.get("jobs", [])
        job_map = {j["id"]: j for j in current_jobs}
        
        done_count = sum(1 for j in current_jobs if j.get("status") == "done")
        failed_count = sum(1 for j in current_jobs if j.get("status") == "failed")
        running_count = len(job_ids) - done_count - failed_count

        now = time.time()
        if now - last_report_time > 10 or done_count == len(job_ids):
            elapsed = int(now - start_time)
            print(f"  [Progress +{elapsed}s] Done: {done_count}/12 | In-Progress: {running_count} | Failed: {failed_count}")
            last_report_time = now

        if done_count == len(job_ids):
            print("\n🎉 ALL 12 KEYFRAMES SUCCESSFULLY GENERATED & DOWNLOADED!")
            break

        if failed_count > 0 and running_count == 0:
            print(f"\n⚠️ Some jobs failed: {failed_count} failed out of {len(job_ids)}")
            break

        time.sleep(2)

    # 4. Compile Storyboard Report
    print("\n[Step 4] Compiling Storyboard Artifact & Asset Index...")
    final_wait = flow_client.request_api("wait", {"job_ids": job_ids, "timeout_seconds": 5})
    completed_jobs = {j["id"]: j for j in final_wait.get("jobs", [])}

    output_dir = Path("C:/Users/ertyui/flow-mcp-out") / PROJECT_NAME
    results_list = []

    for idx, (jid, meta) in enumerate(zip(job_ids, frame_meta)):
        job_info = completed_jobs.get(jid, {})
        files = job_info.get("files", [])
        file_path = files[0] if files else None
        
        file_exists = False
        file_size_kb = 0
        if file_path:
            fp = Path(file_path)
            if fp.exists():
                file_exists = True
                file_size_kb = round(fp.stat().st_size / 1024, 1)

        record = {
            "index": idx + 1,
            "scene_num": meta["scene_num"],
            "scene_title": meta["scene_title"],
            "narration": meta["narration"],
            "frame_type": meta["frame_type"],
            "label": meta["label"],
            "prompt": meta["prompt"],
            "job_id": jid,
            "status": job_info.get("status", "unknown"),
            "file_path": str(file_path) if file_path else None,
            "file_exists": file_exists,
            "file_size_kb": file_size_kb,
        }
        results_list.append(record)

    # Save JSON summary
    assets_dir = Path("c:/Users/ertyui/ZCodeProject/holymoly_studio/assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    json_path = assets_dir / f"{PROJECT_NAME}_storyboard.json"
    json_path.write_text(json.dumps(results_list, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved storyboard metadata JSON: {json_path}")

    # Generate Markdown Storyboard Document
    md_lines = [
        f"# Storyboard 60 Detik: Sejarah Penjajahan Jepang di Indonesia (1942-1945)",
        f"**Project**: `{PROJECT_NAME}` | **Style**: Paper-Cut / Origami Diorama | **Aspect Ratio**: 9:16 (Vertical)\n",
        f"Pipeline ini mengimplementasikan **Mode A (Pakem Template Harness)** dari Holymoly Studio, menggunakan **0 Credits (GRATIS)** via Google Flow Image Generator untuk memetakan Opening dan Closing Keyframe di setiap scene sebelum proses video interpolation.\n",
        "| No | Scene | Frame | Status | File Path | Ukuran | Narasi Suara (TTS) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in results_list:
        status_icon = "✅" if r["file_exists"] else "❌"
        md_lines.append(
            f"| {r['index']:02d} | Scene {r['scene_num']} | **{r['frame_type'].capitalize()}**: {r['label']} | "
            f"{status_icon} `{r['status']}` | `{r['file_path']}` | {r['file_size_kb']} KB | \"{r['narration']}\" |"
        )

    md_lines.append("\n## Detail Visual Prompts & Keyframes\n")
    for r in results_list:
        md_lines.append(f"### Frame {r['index']:02d}: {r['label']}")
        md_lines.append(f"- **Scene**: {r['scene_title']}")
        md_lines.append(f"- **Tipe**: `{r['frame_type'].upper()}` Frame (Durasi total scene: 10s)")
        md_lines.append(f"- **File Lokasi**: `{r['file_path']}` ({r['file_size_kb']} KB)")
        md_lines.append(f"- **Narasi Pengiring**: *\"{r['narration']}\"*")
        md_lines.append(f"- **English Prompt**: \n  > {r['prompt']}\n")

    md_path = assets_dir / f"{PROJECT_NAME}_STORYBOARD.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Saved storyboard visual document: {md_path}")

    print("\n✅ STORYBOARD KEYFRAME GENERATION COMPLETE!")
    return results_list


if __name__ == "__main__":
    run()
