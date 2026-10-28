#!/usr/bin/env python3
"""
Record Fresh V4 Mobile Beats from physical Samsung Galaxy Z Flip 3
- Beat 2: 15.000s @ 60 FPS (Dashboard -> Swipe -> Portal File -> Buka di PC Dialog)
- Beat 5: 15.000s @ 60 FPS (Portal File -> Bayar di Kasir -> Tambah -> Checkout -> Struk)
"""

import time
import subprocess
from pathlib import Path

DEVICE = "R5CR81GTJDD"
DISPLAY_ID = "4630947232161729154"
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fresh_v4")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def adb(cmd):
    return subprocess.run(f"adb -s {DEVICE} shell {cmd}", shell=True, capture_output=True, text=True)

def record_beat_2():
    print("=" * 60)
    print("RECORDING FRESH BEAT 2: Dashboard -> Portal File -> Buka di PC (15.0s)")
    print("=" * 60)
    # Dismiss any dialog
    adb("input tap 500 800")
    time.sleep(0.5)
    # Reset dashboard to top
    adb("input keyevent 4")
    time.sleep(0.5)
    adb("input swipe 500 600 500 2200 300")
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_v4_beat2.mp4"
    local_mp4 = OUT_DIR / "raw_beat2.mp4"
    
    print("[ADB] Starting screen recording...")
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 16 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.2)
    
    # 0.0s - 2.5s: Dashboard overview
    print("  1. Dashboard overview...")
    time.sleep(2.5)
    
    # 2.5s - 4.5s: Swipe down to reveal Portal File
    print("  2. Swiping to reveal Portal File...")
    adb("input swipe 500 2000 500 800 350")
    time.sleep(2.0)
    
    # 4.5s - 7.5s: Tap Portal File (540, 2110)
    print("  3. Tapping Portal File (x=540, y=2110)...")
    adb("input tap 540 2110")
    time.sleep(3.0)
    
    # 7.5s - 10.0s: Tap Buka di PC (907, 496)
    print("  4. Tapping Buka di PC (x=907, y=496)...")
    adb("input tap 907 496")
    time.sleep(2.5)
    
    # 10.0s - 15.0s: Hold Buka di PC dialog
    print("  5. Holding Buka di PC dialog...")
    time.sleep(5.0)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb(f"rm {remote_mp4}")
    
    # Standardize to exact 15.000s @ 60 FPS
    final_mp4 = OUT_DIR / "mobile_beat2_15.0s.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(local_mp4),
        "-vf", "fps=60,tpad=stop_mode=clone:stop_duration=5",
        "-t", "15.000",
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
    print("RECORDING FRESH BEAT 5: Portal File -> Bayar di Kasir -> Checkout Struk (15.0s)")
    print("=" * 60)
    # Dismiss dialog
    adb("input tap 500 800")
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_v4_beat5.mp4"
    local_mp4 = OUT_DIR / "raw_beat5.mp4"
    
    print("[ADB] Starting screen recording...")
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 16 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.2)
    
    # 0.0s - 3.0s: Tap Bayar di Kasir on Hendra Wijaya (x=767, y=952)
    print("  1. Tapping Bayar di Kasir (x=767, y=952)...")
    adb("input tap 767 952")
    time.sleep(3.0)
    
    # 3.0s - 6.0s: Tap Tambah on Print Warna Dokumen A4 (x=795, y=739)
    print("  2. Tapping Tambah Print Warna A4 (x=795, y=739)...")
    adb("input tap 795 739")
    time.sleep(2.5)
    
    # 6.0s - 8.5s: Tap Bayar (x=883, y=2475)
    print("  3. Tapping Bayar (x=883, y=2475)...")
    adb("input tap 883 2475")
    time.sleep(2.5)
    
    # 8.5s - 11.0s: Tap Pembayaran Tunai (x=540, y=2590)
    print("  4. Tapping Pembayaran Tunai (x=540, y=2590)...")
    adb("input tap 540 2590")
    time.sleep(2.5)
    
    # 11.0s - 15.0s: Hold Struk digital
    print("  5. Holding Struk digital view...")
    time.sleep(4.0)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb(f"rm {remote_mp4}")
    
    # Standardize to exact 15.000s @ 60 FPS
    final_mp4 = OUT_DIR / "mobile_beat5_15.0s.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(local_mp4),
        "-vf", "fps=60,tpad=stop_mode=clone:stop_duration=10",
        "-t", "15.000",
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
