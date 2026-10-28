#!/usr/bin/env python3
"""
Automated ADB Screen Recording for NUSA Kasir Fotocopy on Samsung Galaxy Z Flip 3
Records:
1. seg1_mobile_portal_pc.mp4: Dashboard -> Scroll -> Portal File -> Buka di PC Dialog
2. seg2_mobile_kasir_struk.mp4: Portal File -> Bayar di Kasir -> Checkout -> Struk Cetak
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

def adb(cmd):
    full_cmd = f"adb -s {DEVICE} shell \"{cmd}\""
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True)

def start_screenrecord(remote_path, duration_sec):
    cmd = [
        "adb", "-s", DEVICE, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --time-limit {duration_sec} --bit-rate 16M {remote_path}"
    ]
    proc = subprocess.Popen(cmd)
    return proc

def pull_and_clean(remote_path, local_path):
    print(f"[ADB] Pulling {remote_path} -> {local_path.name}...")
    subprocess.run(f"adb -s {DEVICE} pull {remote_path} \"{local_path}\"", shell=True, check=True)
    subprocess.run(f"adb -s {DEVICE} shell \"rm {remote_path}\"", shell=True, check=True)
    print(f"[ADB] Saved {local_path.name} ({local_path.stat().st_size} bytes)")

def record_segment_1():
    print("=" * 60)
    print("RECORDING SEGMENT 1: Portal File & Sambungkan ke PC")
    print("=" * 60)
    
    # Reset to dashboard
    adb("input keyevent 4")
    time.sleep(0.5)
    adb("input keyevent 4")
    time.sleep(1.0)
    
    remote_file = "/sdcard/seg1_portal_rec.mp4"
    local_file = OUT_DIR / "seg1_mobile_portal_pc.mp4"
    
    rec_proc = start_screenrecord(remote_file, 16)
    time.sleep(1.5)
    
    # 1. Scroll dashboard to reveal Portal File
    print("  -> Scrolling dashboard...")
    adb("input swipe 500 2000 500 1200 350")
    time.sleep(2.0)
    
    # 2. Tap Portal File
    print("  -> Tapping Portal File...")
    adb("input tap 875 2110")
    time.sleep(3.0)
    
    # 3. Tap Buka di PC
    print("  -> Tapping Buka di PC...")
    adb("input tap 900 495")
    time.sleep(4.0)
    
    # 4. Highlight dialog / wait
    print("  -> Holding Buka di PC dialog...")
    time.sleep(3.0)
    
    rec_proc.wait()
    pull_and_clean(remote_file, local_file)

def record_segment_2():
    print("=" * 60)
    print("RECORDING SEGMENT 2: Bayar di Kasir & Struk Cetak")
    print("=" * 60)
    
    # Dismiss dialog
    adb("input tap 500 800")
    time.sleep(1.5)
    
    remote_file = "/sdcard/seg2_kasir_rec.mp4"
    local_file = OUT_DIR / "seg2_mobile_kasir_struk.mp4"
    
    rec_proc = start_screenrecord(remote_file, 16)
    time.sleep(1.5)
    
    # 1. Tap Bayar di Kasir on Hendra Wijaya (#PRN-023)
    print("  -> Tapping Bayar di Kasir on Hendra Wijaya...")
    adb("input tap 760 950")
    time.sleep(3.0)
    
    # 2. Add an item or tap Bayar
    print("  -> Tapping Tambah Kertas HVS...")
    adb("input tap 280 1400")
    time.sleep(2.0)
    
    # 3. Tap floating Bayar / Keranjang at bottom
    print("  -> Tapping Bayar...")
    adb("input tap 850 2480")
    time.sleep(2.5)
    
    # 4. Tap Uang Pas / Confirm
    print("  -> Confirming Payment...")
    adb("input tap 500 2480")
    time.sleep(4.0)
    
    rec_proc.wait()
    pull_and_clean(remote_file, local_file)

if __name__ == "__main__":
    record_segment_1()
    time.sleep(2.0)
    record_segment_2()
    print("=" * 60)
    print("ALL MOBILE SCREEN RECORDINGS COMPLETE!")
    print("=" * 60)
