#!/usr/bin/env python3
"""
Holymoly Studio - Clean Master Video Producer (Zero Top Cards, Zero Hardcoded Captions)
Ready for Flow MCP Bold Pop Captions Burning
"""

import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

FLOW_VID_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60sVideo")
AUDIO_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60s/gemini_audio")
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output_clean")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_CLEAN_MP4 = OUT_DIR / "sejarah_jepang_flow_clean.mp4"
CONCAT_LIST_PATH = OUT_DIR / "clean_scenes_concat.txt"
BG_DRONE_PATH = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output/cinematic_drone.wav")

WIDTH, HEIGHT = 1080, 1920

SCENES_CONFIG = [
    {
        "num": 1,
        "video": FLOW_VID_DIR / "scene-07.mp4",
        "audio": AUDIO_DIR / "scene_01.wav",
    },
    {
        "num": 2,
        "video": FLOW_VID_DIR / "scene-08.mp4",
        "audio": AUDIO_DIR / "scene_02.wav",
    },
    {
        "num": 3,
        "video": FLOW_VID_DIR / "scene-09.mp4",
        "audio": AUDIO_DIR / "scene_03.wav",
    },
    {
        "num": 4,
        "video": FLOW_VID_DIR / "scene-10.mp4",
        "audio": AUDIO_DIR / "scene_04.wav",
    },
    {
        "num": 5,
        "video": FLOW_VID_DIR / "scene-13.mp4",
        "audio": AUDIO_DIR / "scene_05.wav",
    },
    {
        "num": 6,
        "video": FLOW_VID_DIR / "scene-12.mp4",
        "audio": AUDIO_DIR / "scene_06.wav",
    },
]

def get_duration(p: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def process_clean_scene(cfg: dict, drone_offset: float) -> tuple[Path, float]:
    scene_num = cfg["num"]
    print(f"\n[Scene {scene_num}] Processing Clean Flow AI Clip -> {cfg['video'].name}...")

    audio_dur = get_duration(cfg["audio"])
    target_dur = audio_dur + 0.3
    flow_vid_dur = get_duration(cfg["video"])
    speed_factor = target_dur / flow_vid_dur

    out_mp4 = OUT_DIR / f"clean_scene_{scene_num:02d}.mp4"

    filter_complex = (
        f"[0:v]scale={WIDTH}:{HEIGHT}:flags=lanczos,setpts={speed_factor:.4f}*PTS[vout]; "
        f"[1:a]volume=1.0[voice]; "
        f"[2:a]volume=0.20[drone]; "
        f"[voice][drone]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(cfg["video"]),
        "-i", str(cfg["audio"]),
        "-ss", str(drone_offset), "-i", str(BG_DRONE_PATH),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{target_dur:.2f}",
        str(out_mp4)
    ]

    subprocess.run(cmd, check=True)
    print(f"[Scene {scene_num}] SUCCESS -> {out_mp4.name} ({target_dur:.2f}s)")
    return out_mp4, target_dur

rendered_clips = []
drone_offset = 0.0

for cfg in SCENES_CONFIG:
    clip_path, dur = process_clean_scene(cfg, drone_offset)
    rendered_clips.append(clip_path)
    drone_offset += dur

print("\n[Holymoly Studio] Stitching 6 clean scenes into master video...")
with open(CONCAT_LIST_PATH, "w", encoding="utf-8") as f:
    for c in rendered_clips:
        f.write(f"file '{c.resolve().as_posix()}'\n")

concat_cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(CONCAT_LIST_PATH),
    "-c", "copy",
    str(FINAL_CLEAN_MP4)
]
subprocess.run(concat_cmd, check=True)

print(f"\n=======================================================")
print(f"🎬 CLEAN VIDEO PRODUCED (ZERO CARDS, ZERO SUBTITLES)!")
print(f"Location: {FINAL_CLEAN_MP4}")
print(f"Size: {FINAL_CLEAN_MP4.stat().st_size / (1024 * 1024):.2f} MB")
print(f"=======================================================")
