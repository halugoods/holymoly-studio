#!/usr/bin/env python3
"""
Record Exact Mobile Screen Segments for NUSA Fotocopy Commercial (V3)
- Beat 2 (15.5s): Dashboard -> Tap Portal File -> Tap Buka di PC -> Hold URL Dialog
- Beat 5 (16.5s): Portal File -> Tap Bayar di Kasir -> Layanan -> Tambah -> Bayar -> Struk
"""

import os
import sys
import time
import subprocess
from pathlib import Path

DEVICE = "R5CR81GTJDD"
DISPLAY_ID = "4630947232161729154"
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def adb_cmd(cmd):
    return subprocess.run(f"adb -s {DEVICE} shell {cmd}", shell=True, capture_output=True, text=True)

def setup_for_beat2():
    print("[Mobile Setup] Resetting to clean Dashboard...")
    # Dismiss dialog if open
    adb_cmd("input tap 500 800")
    time.sleep(0.5)
    # Press back until dashboard
    for _ in range(3):
        res = subprocess.run(f"adb -s {DEVICE} shell dumpsys window | findstr /i mCurrentFocus", shell=True, capture_output=True, text=True)
        if "MainActivity" in res.stdout:
            # check if dashboard
            adb_cmd("input keyevent 4")
            time.sleep(0.5)
    adb_cmd("am start -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant fotocopy --ez pro true")
    time.sleep(1.0)

def record_beat_2():
    print("=" * 60)
    print("RECORDING BEAT 2: Dashboard -> Portal File -> Buka di PC (15.5s)")
    print("=" * 60)
    setup_for_beat2()
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_beat2_v3.mp4"
    local_mp4 = OUT_DIR / "mobile_beat2_v3.mp4"
    
    print("[ADB] Starting screen recording...")
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 16 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.2)
    
    # 0.0s - 3.5s: Dashboard overview ("Solusinya, pakai NUSA Kasir Fotocopy!")
    print("  1. Dashboard view...")
    time.sleep(2.5)
    
    # 3.5s - 6.5s: Tap Portal File (x=540, y=2110)
    print("  2. Tapping Portal File (x=540, y=2110)...")
    adb_cmd("input tap 540 2110")
    time.sleep(3.0)
    
    # 6.5s - 9.0s: Tap Buka di PC (x=907, y=496)
    print("  3. Tapping Buka di PC (x=907, y=496)...")
    adb_cmd("input tap 907 496")
    time.sleep(2.5)
    
    # 9.0s - 15.5s: Hold Buka di PC dialog
    print("  4. Holding Buka di PC dialog with server URL...")
    time.sleep(6.5)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb_cmd(f"rm {remote_mp4}")
    
    # Standardize to exact 15.50s @ 60 FPS
    final_mp4 = OUT_DIR / "mobile_beat2_15.5s.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(local_mp4),
        "-t", "15.500",
        "-vf", "fps=60",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(final_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Success] Saved {final_mp4.name} ({final_mp4.stat().st_size} bytes)")

def record_beat_5():
    print("=" * 60)
    print("RECORDING BEAT 5: Portal File -> Bayar di Kasir -> Checkout Struk (16.5s)")
    print("=" * 60)
    # Dismiss dialog
    adb_cmd("input tap 500 800")
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_beat5_v3.mp4"
    local_mp4 = OUT_DIR / "mobile_beat5_v3.mp4"
    
    print("[ADB] Starting screen recording...")
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 18 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.2)
    
    # 0.0s - 3.5s: Tap Bayar di Kasir on Hendra Wijaya (x=767, y=952)
    print("  1. Tapping Bayar di Kasir (x=767, y=952)...")
    adb_cmd("input tap 767 952")
    time.sleep(3.0)
    
    # 3.5s - 6.5s: Tap Layanan -> Tambah Print Warna A4 (x=795, y=739)
    print("  2. Tapping Tambah Print Warna A4 (x=795, y=739)...")
    adb_cmd("input tap 795 739")
    time.sleep(2.5)
    
    # 6.5s - 9.5s: Tap Bayar (x=883, y=2475)
    print("  3. Tapping Bayar (x=883, y=2475)...")
    adb_cmd("input tap 883 2475")
    time.sleep(3.0)
    
    # 9.5s - 12.0s: Tap Pembayaran Tunai (x=540, y=2590)
    print("  4. Tapping Pembayaran Tunai (x=540, y=2590)...")
    adb_cmd("input tap 540 2590")
    time.sleep(2.5)
    
    # 12.0s - 16.5s: Hold view of Struk and success screen
    print("  5. Holding Struk digital view...")
    time.sleep(4.5)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb_cmd(f"rm {remote_mp4}")
    
    # Standardize to exact 16.50s @ 60 FPS
    final_mp4 = OUT_DIR / "mobile_beat5_16.5s.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(local_mp4),
        "-t", "16.500",
        "-vf", "fps=60",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(final_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Success] Saved {final_mp4.name} ({final_mp4.stat().st_size} bytes)")

if __name__ == "__main__":
    record_beat_2()
    time.sleep(2.0)
    record_beat_5()
