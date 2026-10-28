#!/usr/bin/env python3
"""
Record Exact Mobile Screen Segments for NUSA Fotocopy Commercial
- Beat 2 (14.5s): Dashboard -> Scroll -> Portal File -> Buka di PC Dialog
- Beat 6 (17.0s): Portal File -> Bayar di Kasir -> Layanan -> Tambah -> Checkout -> Struk
"""

import os
import sys
import time
import subprocess
from pathlib import Path

DEVICE = "R5CR81GTJDD"
DISPLAY_ID = "4630947232161729154"
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")

def adb_cmd(cmd):
    return subprocess.run(f"adb -s {DEVICE} shell {cmd}", shell=True, capture_output=True, text=True)

def ensure_dashboard():
    # If in sub-screen, tap top-left back button or back key until dashboard
    print("[Mobile Setup] Resetting to clean Dashboard...")
    adb_cmd("am start -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant fotocopy --ez pro true")
    time.sleep(1.0)
    # Check if back arrow exists, tap it
    adb_cmd("input tap 100 180")
    time.sleep(1.0)

def record_beat_2():
    print("=" * 60)
    print("RECORDING BEAT 2: Dashboard -> Portal File -> Buka di PC")
    print("=" * 60)
    ensure_dashboard()
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_beat2.mp4"
    local_mp4 = OUT_DIR / "mobile_beat2_portal_pc.mp4"
    
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 16 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.5)
    
    # 1. Smooth scroll to reveal Portal File
    print("  1. Scrolling to Portal File...")
    adb_cmd("input swipe 500 2000 500 1200 350")
    time.sleep(2.5)
    
    # 2. Tap Portal File (Col 2: x=540, y=2110)
    print("  2. Tapping Portal File (x=540, y=2110)...")
    adb_cmd("input tap 540 2110")
    time.sleep(3.5)
    
    # 3. Tap Buka di PC (x=907, y=496)
    print("  3. Tapping Buka di PC (x=907, y=496)...")
    adb_cmd("input tap 907 496")
    time.sleep(4.5)
    
    # Hold dialog
    print("  4. Holding Buka di PC dialog...")
    time.sleep(3.0)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb_cmd(f"rm {remote_mp4}")
    print(f"[Success] Saved {local_mp4.name} ({local_mp4.stat().st_size} bytes)")

def record_beat_6():
    print("=" * 60)
    print("RECORDING BEAT 6: Portal File -> Bayar di Kasir -> Checkout Struk")
    print("=" * 60)
    # Dismiss dialog
    adb_cmd("input tap 500 800")
    time.sleep(1.0)
    
    remote_mp4 = "/sdcard/rec_beat6.mp4"
    local_mp4 = OUT_DIR / "mobile_beat6_kasir_struk.mp4"
    
    proc = subprocess.Popen([
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 18 --bit-rate 16M {remote_mp4}"
    ])
    time.sleep(1.5)
    
    # 1. Tap Bayar di Kasir on Hendra Wijaya (#PRN-027) at x=767, y=952
    print("  1. Tapping Bayar di Kasir (x=767, y=952)...")
    adb_cmd("input tap 767 952")
    time.sleep(3.0)
    
    # 2. Tap Layanan tab at x=789, y=485
    print("  2. Tapping Layanan tab (x=789, y=485)...")
    adb_cmd("input tap 789 485")
    time.sleep(2.5)
    
    # 3. Tap Tambah Print Warna Dokumen A4 at x=795, y=1392
    print("  3. Tapping Tambah Print Warna A4 (x=795, y=1392)...")
    adb_cmd("input tap 795 1392")
    time.sleep(2.0)
    
    # 4. Tap Tambah Jilid Lakban at x=795, y=2245
    print("  4. Tapping Tambah Jilid Lakban (x=795, y=2245)...")
    adb_cmd("input tap 795 2245")
    time.sleep(2.5)
    
    # 5. Tap Bayar (bottom bar at x=850, y=2480)
    print("  5. Tapping Bayar (x=850, y=2480)...")
    adb_cmd("input tap 850 2480")
    time.sleep(3.0)
    
    proc.wait()
    subprocess.run(f"adb -s {DEVICE} pull {remote_mp4} \"{local_mp4}\"", shell=True, check=True)
    adb_cmd(f"rm {remote_mp4}")
    print(f"[Success] Saved {local_mp4.name} ({local_mp4.stat().st_size} bytes)")

if __name__ == "__main__":
    record_beat_2()
    time.sleep(2.0)
    record_beat_6()
    print("=" * 60)
    print("ALL MOBILE BEATS RECORDED SUCCESSFULLY!")
    print("=" * 60)
