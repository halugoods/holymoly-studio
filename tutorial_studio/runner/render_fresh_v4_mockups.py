#!/usr/bin/env python3
"""
Render Centered Samsung Galaxy Z Flip 3 Vector Mockups for Mobile Beats 2 & 5 (V4)
- Beat 2: mobile_beat2_15.0s.mp4 -> mockup_beat2_15.0s.mp4 (15.000s @ 60 FPS)
- Beat 5: mobile_beat5_15.0s.mp4 -> mockup_beat5_15.0s.mp4 (15.000s @ 60 FPS)
"""

import sys
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
V4_DIR = OUT_DIR / "fresh_v4"
GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"

def render_mockup(raw_mp4, out_mp4, duration):
    print(f"[Mockup Engine V4] Rendering {raw_mp4.name} -> {out_mp4.name} ({duration:.3f}s @ 60 FPS)...")
    filter_complex = (
        "[1:v]fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
        "[scaled_screen][2:v]alphamerge[masked_screen];"
        "[0:v][masked_screen]overlay=x=190:y=105:shortest=1[bg_screen];"
        "[bg_screen][3:v]overlay=x=0:y=0:shortest=1[final_v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(GRID_MP4),
        "-i", str(raw_mp4),
        "-loop", "1", "-i", str(MASK_PNG),
        "-loop", "1", "-i", str(FRAME_PNG),
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-t", f"{duration:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Mockup Success] Saved {out_mp4.name} ({out_mp4.stat().st_size} bytes)")

if __name__ == "__main__":
    beat2_raw = V4_DIR / "mobile_beat2_15.0s.mp4"
    beat2_out = V4_DIR / "mockup_beat2_15.0s.mp4"
    render_mockup(beat2_raw, beat2_out, 15.000)

    beat5_raw = V4_DIR / "mobile_beat5_15.0s.mp4"
    beat5_out = V4_DIR / "mockup_beat5_15.0s.mp4"
    render_mockup(beat5_raw, beat5_out, 15.000)
