#!/usr/bin/env python3
"""
Safe & Validated ADB Screen Recording for NUSA Kasir Fotocopy
Guarantees zero launcher touch & verifies package focus at every step.
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

def ensure_nusa_focus():
    cmd = f"adb -s {DEVICE} shell dumpsys window | findstr /i mCurrentFocus"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if "com.nusa.dev" not in res.stdout:
        print("[Focus Guard] Restoring NUSA Kasir focus...")
        subprocess.run(
            f"adb -s {DEVICE} shell am start -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant fotocopy --ez pro true",
            shell=True
        )
        time.sleep(2.0)

def safe_tap(x, y, label=""):
    ensure_nusa_focus()
    print(f"  [Action] {label} -> tap({x}, {y})")
    subprocess.run(f"adb -s {DEVICE} shell input tap {x} {y}", shell=True)

def safe_swipe(x1, y1, x2, y2, dur=350, label=""):
    ensure_nusa_focus()
    print(f"  [Action] {label} -> swipe({x1}, {y1} -> {x2}, {y2})")
    subprocess.run(f"adb -s {DEVICE} shell input swipe {x1} {y1} {x2} {y2} {dur}", shell=True)

def main():
    print("=" * 60)
    print("SAFE RECORDING NUSA KASIR FOTOCOPY MOBILE FLOW")
    print("=" * 60)
    ensure_nusa_focus()
    
    remote_file = "/sdcard/nusa_fotocopy_flow.mp4"
    local_file = OUT_DIR / "nusa_fotocopy_flow_raw.mp4"
    
    # 28s recording
    rec_cmd = [
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit 28 --bit-rate 16M {remote_file}"
    ]
    print("[ADB] Starting screenrecord (28s)...")
    proc = subprocess.Popen(rec_cmd)
    time.sleep(1.5)
    
    # 1. Scroll dashboard down to show Portal File
    safe_swipe(500, 2000, 500, 1200, 350, "Scroll Dashboard to Portal File")
    time.sleep(2.5)
    
    # 2. Tap Portal File
    safe_tap(875, 2110, "Buka Menu Portal File")
    time.sleep(3.5)
    
    # 3. Tap Buka di PC
    safe_tap(900, 495, "Buka Dialog Sambungkan ke PC")
    time.sleep(4.5)
    
    # 4. Dismiss Dialog by tapping outside
    safe_tap(500, 800, "Tutup Dialog PC")
    time.sleep(2.5)
    
    # 5. Tap Bayar di Kasir on Hendra Wijaya (#PRN-023)
    safe_tap(760, 950, "Klik Bayar di Kasir")
    time.sleep(3.5)
    
    # 6. Tap Tambah
    safe_tap(280, 1400, "Tambah Layanan")
    time.sleep(2.5)
    
    # 7. Tap Bayar bottom bar
    safe_tap(850, 2480, "Klik Bayar Kasir")
    time.sleep(3.0)
    
    # Wait for recording process
    print("[ADB] Waiting for screenrecord to finish...")
    proc.wait()
    
    print(f"[ADB] Pulling {remote_file} -> {local_file.name}...")
    subprocess.run(f"adb -s {DEVICE} pull {remote_file} \"{local_file}\"", shell=True, check=True)
    subprocess.run(f"adb -s {DEVICE} shell rm {remote_file}", shell=True, check=True)
    size_mb = local_file.stat().st_size / (1024 * 1024)
    print(f"[ADB] SUCCESS! Saved {local_file.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
