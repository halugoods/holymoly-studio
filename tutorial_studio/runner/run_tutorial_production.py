#!/usr/bin/env python3
"""
NUSA Kasir Autonomous Tutorial Video Production Runner
Executes pre-calibrated ADB touch sequence at hardware speed without LLM thinking pauses,
records screen at 60 FPS, and muxes high-fidelity audio with word-anchored sync.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

# Add runner dir to path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(CURRENT_DIR))

from adb_recorder import AdbTutorialRecorder
from motion_compositor import MotionCompositor

def run_production(script_path, output_dir=None):
    script_file = Path(script_path)
    if not script_file.exists():
        raise FileNotFoundError(f"Script file not found: {script_file}")

    with open(script_file, "r", encoding="utf-8") as f:
        script = json.load(f)

    if output_dir is None:
        out_dir = PROJECT_ROOT / "output"
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"  NUSA AUTONOMOUS TUTORIAL PRODUCTION: {script.get('title', 'Tutorial')}")
    print(f"  Variant: {script.get('variant', 'unknown')}")
    print(f"  Total Duration: {script.get('total_duration_sec', 15)} seconds")
    print(f"  ADB Events: {len(script.get('adb_timeline', []))} actions")
    print("=" * 60)

    # 1. Initialize recorder & preserve natural status bar (per user instruction)
    recorder = AdbTutorialRecorder()
    print("[Production] Menyiapkan environment (status bar natural dipertahankan)...")
    recorder._run_adb(["shell", "settings", "put", "global", "policy_control", "null"], check=False)

    variant = script.get("variant")
    if variant:
        print(f"[Production] Meluncurkan aplikasi NUSA varian '{variant}' fresh...")
        recorder._run_adb([
            "shell", "am", "start", "-S",
            "-n", "com.nusa.dev/com.example.nusa_kasir.MainActivity",
            "--es", "variant", variant,
            "--ez", "pro", "true",
            "--ez", "onboarding", "false"
        ], check=False)
        time.sleep(3.5)

    # 2. Record & execute timeline
    raw_video_path = out_dir / "raw_screenrecord.mp4"
    events = script.get("adb_timeline", [])
    duration = script.get("total_duration_sec", 16.5)

    print(f"\n[Production] Memulai eksekusi timeline (Headless Mode, Zero-LLM Delay)...")
    success = recorder.execute_timeline(
        events=events,
        total_duration_sec=duration,
        output_path=str(raw_video_path),
        remote_temp_path="/sdcard/nusa_tutorial_raw.mp4"
    )

    if not success or not raw_video_path.exists():
        raise RuntimeError("Gagal merekam layar atau mengunduh video mentah.")

    print(f"\n[Production] Rekaman mentah berhasil disimpan: {raw_video_path} ({raw_video_path.stat().st_size / (1024*1024):.2f} MB)")

    # 3. Audio Muxing & Word-Anchored Synchronization
    audio_track = script.get("audio_track")
    if not audio_track or not Path(audio_track).exists():
        print("[Production] Audio track tidak ditemukan, menggunakan pilot_kelontong_vo.wav default...")
        audio_track = str(out_dir / "pilot_kelontong_vo.wav")

    final_synced_path = out_dir / f"{script_file.stem}_synced.mp4"
    print(f"\n[Production] Melakukan audio-video muxing presisi milidetik ke: {final_synced_path}...")

    # Video memiliki jeda 1.0s di awal untuk buffer encoder Android
    # Kita potong 1.0s di awal video (-ss 1.0) agar aksi t=0 pas dengan awal narasi suara audio!
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-ss", "1.0",
        "-i", str(raw_video_path),
        "-i", str(audio_track),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_synced_path)
    ]

    res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[Production] FFmpeg error: {res.stderr}")
        raise RuntimeError("Gagal memproses video final dengan ffmpeg.")

    print(f"[Production] SUKSES! Video standard siap: {final_synced_path}")
    print(f"             Ukuran: {final_synced_path.stat().st_size / (1024*1024):.2f} MB")

    # 4. Anti-Slop Motion Compositor (Camera Rig, Punch-in Zoom, Tactile Ripple, Callout Badges)
    # First normalize Android VFR recording to true constant 60 FPS for buttery smooth camera interpolation
    raw_60fps_path = out_dir / f"raw_60fps_{raw_video_path.name}"
    print(f"\n[Production] Menormalisasi video mentah ke Constant 60 FPS untuk motion camera rig...")
    norm_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video_path),
        "-filter:v", "fps=fps=60",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        str(raw_60fps_path)
    ]
    subprocess.run(norm_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    commercial_motion_path = out_dir / f"{script_file.stem}_motion_commercial.mp4"
    print(f"\n[Production] Meluncurkan Anti-Slop Motion Compositor ke: {commercial_motion_path}...")
    try:
        compositor = MotionCompositor(
            raw_video_path=raw_60fps_path if raw_60fps_path.exists() else raw_video_path,
            timeline_script_path=script_file,
            audio_path=audio_track,
            output_path=commercial_motion_path,
            target_size=(1080, 1920)
        )
        compositor.render()
        print(f"[Production] MASTERPIECE READY! Video Commercial Motion: {commercial_motion_path}")
    except Exception as e:
        print(f"[Production] Warning: Motion compositor error: {e}")

    return final_synced_path

if __name__ == "__main__":
    script_path = CURRENT_DIR.parent / "scripts" / "pilot_kelontong_qris_20s.json"
    if len(sys.argv) > 1:
        script_path = Path(sys.argv[1])
    run_production(script_path)
