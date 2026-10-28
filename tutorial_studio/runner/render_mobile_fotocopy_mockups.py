#!/usr/bin/env python3
"""
Render Centered Samsung Galaxy Z Flip 3 Vector Mockups for Mobile Segments
Rule 11 Compliant
"""

import os
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"

SEGMENTS = [
    {
        "input": OUT_DIR / "seg1_mobile_portal_pc.mp4",
        "output": OUT_DIR / "mockup_seg1_mobile_portal_pc.mp4",
        "dur": 14.5
    },
    {
        "input": OUT_DIR / "seg2_mobile_kasir_struk.mp4",
        "output": OUT_DIR / "mockup_seg2_mobile_kasir_struk.mp4",
        "dur": 15.0
    }
]

filter_complex = (
    "[1:v]fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
    "[scaled_screen][2:v]alphamerge[masked_screen];"
    "[0:v][masked_screen]overlay=x=190:y=105:shortest=1[bg_screen];"
    "[bg_screen][3:v]overlay=x=0:y=0:shortest=1[final_v]"
)

for seg in SEGMENTS:
    inp = seg["input"]
    out = seg["output"]
    dur = seg["dur"]
    print(f"[Render Mockup] {inp.name} -> {out.name} ({dur}s)...")
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(GRID_MP4),
        "-i", str(inp),
        "-loop", "1", "-i", str(MASK_PNG),
        "-loop", "1", "-i", str(FRAME_PNG),
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-t", f"{dur:.2f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Error]:", res.stderr)
        raise RuntimeError(f"Failed to render mockup for {inp.name}")
    print(f"[Success] {out.name} ({out.stat().st_size} bytes)")

print("[Render Mockup] All mobile mockups rendered successfully!")
