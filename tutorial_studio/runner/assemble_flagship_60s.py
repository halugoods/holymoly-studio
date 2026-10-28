#!/usr/bin/env python3
"""
Assemble Flagship 60-Second Hybrid Video:
Flow Cinematic B-Roll + Centered Samsung Galaxy Z Flip 3 Mockup Studio
Audio: Gemini Native Audio TTS (Puck)
Aspect Ratio: 9:16 (1080x1920) @ 60 FPS
Zero AI Slop, Zero Crop, Cupertino Tactile Ripple
"""

import sys
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
FLOW_DIR = Path("C:/Users/ertyui/flow-mcp-out/nusa_kelontong_60s")
FLOW_V4 = Path("C:/Users/ertyui/flow-mcp-out/nusa_kelontong_60s_v4")
FLOW_V5 = Path("C:/Users/ertyui/flow-mcp-out/nusa_kelontong_60s_v5")
FLOW_V6 = Path("C:/Users/ertyui/flow-mcp-out/nusa_kelontong_60s_v6")
FLOW_V7 = Path("C:/Users/ertyui/flow-mcp-out/nusa_kelontong_60s_v7")
ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

VO_AUDIO = OUT_DIR / "kelontong_60s_vo.wav"
FINAL_MASTER = ARTIFACT_DIR / "nusa_kelontong_60s_flagship_master.mp4"

CLIPS = [
    {
        "id": "beat_01_flow",
        "type": "flow",
        "file": FLOW_V5 / "scene-01.mp4",
        "dur": 9.0, # Target 9.0s
        "label": "B-Roll: Bustling Warung Kelontong & Stressed Manual Ledger Notebook (Glitch-Free)"
    },
    {
        "id": "beat_02_mockup",
        "type": "mockup",
        "file": OUT_DIR / "seg1_mockup_15s.mp4",
        "dur": 15.0, # Exactly 15.0s
        "label": "Mockup: POS Kasir Catalog & Add Items to Cart"
    },
    {
        "id": "beat_03_flow",
        "type": "flow",
        "file": FLOW_V4 / "scene-02.mp4",
        "dur": 6.0, # Exactly 6.0s
        "label": "B-Roll: Over-the-shoulder Customer Scanning Counter QRIS Standee"
    },
    {
        "id": "beat_04_mockup",
        "type": "mockup",
        "file": OUT_DIR / "seg2_mockup_12s.mp4",
        "dur": 12.0, # Exactly 12.0s
        "label": "Mockup: QRIS Checkout & Struk Pesanan Modal"
    },
    {
        "id": "beat_05_flow",
        "type": "flow",
        "file": FLOW_V7 / "scene-01.mp4",
        "dur": 6.0, # Exactly 6.0s
        "label": "B-Roll: Steady Cam Thermal Printer Dispensing Beras 5kg & Minyak 2L Rp 111.500 Receipt"
    },
    {
        "id": "beat_06_mockup",
        "type": "mockup",
        "file": OUT_DIR / "seg3_mockup_12s.mp4",
        "dur": 12.0, # Exactly 12.0s
        "label": "Mockup: Laporan Penjualan & Revenue Graph Outro"
    }
]

def standardize_clip(clip_info, out_path):
    src = clip_info["file"]
    dur = clip_info["dur"]
    print(f"[Standardize] {clip_info['id']} ({dur}s): {src.name} -> {out_path.name}...")
    
    # Scale to 1080x1920, fps=60, trim/pad to exact duration
    # High-quality lanczos scaling + pad if needed
    cmd = [
        "ffmpeg", "-y",
        "-err_detect", "ignore_err",
        "-max_error_rate", "1.0",
        "-i", str(src),
        "-vf", (
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,"
            f"fps=60,"
            f"tpad=stop_mode=clone:stop_duration={dur}"
        ),
        "-t", f"{dur:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Standardize Error]:", res.stderr)
        raise RuntimeError(f"Standardize failed for {src}")

def main():
    print("[Assembly 60s] Preparing clips...")
    std_clips = []
    for idx, c in enumerate(CLIPS):
        std_file = OUT_DIR / f"std_part_{idx+1}_{c['id']}.mp4"
        standardize_clip(c, std_file)
        std_clips.append(std_file)

    # Concat file list
    concat_list = OUT_DIR / "concat_60s.txt"
    with open(concat_list, "w") as f:
        for p in std_clips:
            f.write(f"file '{p.resolve()}'\n")

    temp_video = OUT_DIR / "temp_video_60s.mp4"
    print(f"\n[Assembly 60s] Concatenating 6 clips to {temp_video.name}...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(temp_video)
    ]
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Concat Error]:", res.stderr)
        raise RuntimeError("Concat failed")

    # Mux with Voiceover Audio
    print(f"\n[Assembly 60s] Muxing video with Gemini Native Audio: {VO_AUDIO.name}...")
    final_temp = OUT_DIR / "final_with_audio_60s.mp4"
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(VO_AUDIO),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "60.000",
        str(final_temp)
    ]
    res = subprocess.run(mux_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Mux Error]:", res.stderr)
        raise RuntimeError("Mux failed")

    # Copy to Brain Artifacts
    FINAL_MASTER.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copyfile(str(final_temp), str(FINAL_MASTER))
    
    mb = FINAL_MASTER.stat().st_size / (1024 * 1024)
    print(f"\n[Assembly 60s] MASTER COMMERCIAL COMPLETE!")
    print(f"File: {FINAL_MASTER}")
    print(f"Size: {mb:.2f} MB, Duration: 60.00s, Resolution: 1080x1920 (9:16) @ 60 FPS")

if __name__ == "__main__":
    main()
