#!/usr/bin/env python3
"""
Prepare device state and re-record Segment 3 with correct Laporan menu coordinates:
Laporan is at (540, 1995) on Dashboard (NOT Keuangan at 540, 2360!)
"""

import sys
import time
import json
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
DEVICE_ID = "R5CR81GTJDD"
DISPLAY_ID = "4630947232161729154"

def adb(cmd):
    full_cmd = ["adb", "-s", DEVICE_ID] + cmd
    return subprocess.run(full_cmd, capture_output=True, text=True)

def setup_struk_dialog():
    print("[Setup] Setting up Struk Pesanan dialog on device...")
    # Go to Kasir
    adb(["shell", "am start -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant kelontong --ez pro true --ez onboarding false"])
    time.sleep(1.5)
    # Tap Kasir
    adb(["shell", "input tap 540 2464"])
    time.sleep(1.5)
    # Tap Sembako
    adb(["shell", "input tap 350 470"])
    time.sleep(0.8)
    # Add items
    adb(["shell", "input tap 284 1245"])
    time.sleep(0.6)
    adb(["shell", "input tap 795 1245"])
    time.sleep(0.8)
    # Tap Bayar
    adb(["shell", "input tap 883 2475"])
    time.sleep(1.2)
    # Tap QRIS
    adb(["shell", "input tap 527 1960"])
    time.sleep(1.0)
    # Swipe up
    adb(["shell", "input swipe 540 2000 540 1200 300"])
    time.sleep(0.8)
    # Tap Cek Status
    adb(["shell", "input tap 540 2434"])
    time.sleep(1.5)
    # Tap Cetak Printer
    adb(["shell", "input tap 540 1842"])
    time.sleep(1.0)
    print("[Setup] Struk dialog is now ready on screen!")

def record_seg3():
    remote_mp4 = "/sdcard/seg3_kelontong.mp4"
    local_raw = OUT_DIR / "seg3_kelontong_raw.mp4"
    dur_sec = 12

    events_seg3 = [
        {"t_sec": 1.2, "action": "tap", "x": 540, "y": 1684, "label": "Selesai & Tutup Struk", "x_pct": 540/1080, "y_pct": 1684/2640},
        {"t_sec": 2.8, "action": "key", "code": 4, "label": "Back ke Dashboard"},
        {"t_sec": 4.5, "action": "tap", "x": 540, "y": 1995, "label": "Buka Laporan Penjualan", "x_pct": 540/1080, "y_pct": 1995/2640},
        {"t_sec": 7.5, "action": "swipe", "x1": 540, "y1": 1800, "x2": 540, "y2": 1300, "dur": 400, "label": "Inspect Grafik Omzet"},
    ]

    print(f"\n[Record Seg 3] Starting screenrecord for {dur_sec}s -> {local_raw.name}...")
    adb(["shell", f"rm -f {remote_mp4}"])
    
    rec_cmd = [
        "adb", "-s", DEVICE_ID, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --bit-rate 16000000 --time-limit {dur_sec} {remote_mp4}"
    ]
    rec_proc = subprocess.Popen(rec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(0.5)
    start_time = time.time()
    
    for ev in events_seg3:
        target_t = ev["t_sec"]
        now = time.time() - start_time
        wait_t = target_t - now
        if wait_t > 0:
            time.sleep(wait_t)
            
        action = ev["action"]
        if action == "tap":
            x, y = ev["x"], ev["y"]
            print(f"  [{time.time()-start_time:.2f}s] Tap ({x}, {y}) - {ev.get('label', '')}")
            adb(["shell", f"input tap {x} {y}"])
        elif action == "swipe":
            x1, y1, x2, y2, dur = ev["x1"], ev["y1"], ev["x2"], ev["y2"], ev.get("dur", 300)
            print(f"  [{time.time()-start_time:.2f}s] Swipe ({x1}, {y1}) -> ({x2}, {y2}) - {ev.get('label', '')}")
            adb(["shell", f"input swipe {x1} {y1} {x2} {y2} {dur}"])
        elif action == "key":
            code = ev["code"]
            print(f"  [{time.time()-start_time:.2f}s] Keyevent {code} - {ev.get('label', '')}")
            adb(["shell", f"input keyevent {code}"])

    rec_proc.wait()
    time.sleep(1.0)
    
    print(f"[Record Seg 3] Pulling {remote_mp4} to {local_raw}...")
    adb(["pull", remote_mp4, str(local_raw)])
    adb(["shell", f"rm -f {remote_mp4}"])
    
    with open(OUT_DIR / "seg3_events.json", "w") as f:
        json.dump(events_seg3, f, indent=2)
    print(f"[Record Seg 3] Saved: {local_raw.name} ({local_raw.stat().st_size} bytes)")

if __name__ == "__main__":
    setup_struk_dialog()
    time.sleep(1.0)
    record_seg3()
