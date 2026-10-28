#!/usr/bin/env python3
"""
NUSA Kasir Flagship Vector Mockup Suite Renderer
Re-edits all 8 screen recordings:
- Canvas: 1080x1920 (9:16)
- Centered Samsung Galaxy Z Flip 3 Vector Mockup (100% uncropped screen, full status bar visible)
- Blurred vertical scrolling grid background
- Zero subtitles / zero callout badges
- Preserves original Gemini Native Audio TTS
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"

EPISODES = [
    {
        "id": "ep1",
        "variant": "kelontong",
        "title": "NUSA Kelontong - POS Kasir & QRIS ShopeePay",
        "input_mp4": OUT_DIR / "pilot_kelontong_qris_20s_synced.mp4",
        "output_filename": "ep1_kelontong_qris_commercial.mp4"
    },
    {
        "id": "ep2",
        "variant": "fnb",
        "title": "NUSA F&B - Katalog Menu Resto & Privacy Shield",
        "input_mp4": OUT_DIR / "fnb_catalog_24s_synced.mp4",
        "output_filename": "ep2_fnb_catalog_commercial.mp4"
    },
    {
        "id": "ep3",
        "variant": "laundry",
        "title": "NUSA Laundry - Timbang Kiloan & Struk WhatsApp",
        "input_mp4": OUT_DIR / "laundry_kiloan_21s_synced.mp4",
        "output_filename": "ep3_laundry_kiloan_commercial.mp4"
    },
    {
        "id": "ep4",
        "variant": "bengkel",
        "title": "NUSA Bengkel - Servis Berkala & Sparepart Motor/Mobil",
        "input_mp4": OUT_DIR / "bengkel_servis_21s_synced.mp4",
        "output_filename": "ep4_bengkel_servis_commercial.mp4"
    },
    {
        "id": "ep5",
        "variant": "apotek",
        "title": "NUSA Apotek - Obat Bebas, Vitamin & Struk Farmasi",
        "input_mp4": OUT_DIR / "apotek_farmasi_26s_synced.mp4",
        "output_filename": "ep5_apotek_farmasi_commercial.mp4"
    },
    {
        "id": "ep6",
        "variant": "salon",
        "title": "NUSA Salon - Treatment Rambut & Retail Perawatan",
        "input_mp4": OUT_DIR / "salon_treatment_19s_synced.mp4",
        "output_filename": "ep6_salon_treatment_commercial.mp4"
    },
    {
        "id": "ep7",
        "variant": "fotocopy",
        "title": "NUSA Fotocopy - Print Warna, Jilid & Percetakan",
        "input_mp4": OUT_DIR / "fotocopy_cetak_20s_synced.mp4",
        "output_filename": "ep7_fotocopy_cetak_commercial.mp4"
    },
    {
        "id": "ep8",
        "variant": "servis",
        "title": "NUSA Servis - Tanda Terima Servis Gadget & Garansi",
        "input_mp4": OUT_DIR / "servis_gadget_23s_synced.mp4",
        "output_filename": "ep8_servis_gadget_commercial.mp4"
    }
]

def render_episode(ep):
    input_file = ep["input_mp4"]
    if not input_file.exists():
        print(f"[Error] Input file not found: {input_file}")
        return False

    temp_out = OUT_DIR / f"mockup_{ep['output_filename']}"
    artifact_out = ARTIFACT_DIR / ep["output_filename"]

    print("=" * 60)
    print(f"[{ep['id'].upper()}] RENDERING: {ep['title']}")
    print(f"  Input: {input_file.name}")
    print(f"  Target: {ep['output_filename']}")
    print("=" * 60)

    filter_complex = (
        "[1:v]fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
        "[scaled_screen][2:v]alphamerge[masked_screen];"
        "[0:v][masked_screen]overlay=x=190:y=105:shortest=1[bg_screen];"
        "[bg_screen][3:v]overlay=x=0:y=0:shortest=1[final_v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(GRID_MP4),
        "-i", str(input_file),
        "-loop", "1", "-i", str(MASK_PNG),
        "-loop", "1", "-i", str(FRAME_PNG),
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-map", "1:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(temp_out)
    ]

    t0 = time.perf_counter()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    t1 = time.perf_counter()

    if res.returncode != 0:
        print(f"[FFmpeg Error on {ep['id']}]:", res.stderr)
        return False

    # Copy to artifact directory
    shutil.copyfile(str(temp_out), str(artifact_out))
    size_mb = artifact_out.stat().st_size / (1024 * 1024)
    print(f"[{ep['id'].upper()}] SUCCESS in {t1 - t0:.2f}s! Saved to: {artifact_out.name} ({size_mb:.2f} MB)")
    return True

def main():
    start_total = time.perf_counter()
    success_count = 0

    for ep in EPISODES:
        ok = render_episode(ep)
        if ok:
            success_count += 1

    end_total = time.perf_counter()
    print("\n" + "=" * 60)
    print(f"BATCH COMPLETE: {success_count}/{len(EPISODES)} episodes rendered successfully!")
    print(f"Total processing time: {end_total - start_total:.2f} seconds")
    print("=" * 60)

if __name__ == "__main__":
    main()
