#!/usr/bin/env python3
"""
Record 3 Live Sandbox Screen Segments for NUSA Kelontong 60s Master Commercial
Uses Samsung Galaxy Z Flip3 display-id 4630947232161729154
"""

import sys
import time
import json
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEVICE_ID = "R5CR81GTJDD"
DISPLAY_ID = "4630947232161729154"

def adb(cmd):
    full_cmd = ["adb", "-s", DEVICE_ID] + cmd
    return subprocess.run(full_cmd, capture_output=True, text=True)

def record_and_automate(remote_mp4, local_mp4, duration_sec, events):
    """
    Starts background screenrecord on phone, executes timed tap events,
    waits for recording to finish, and pulls the MP4.
    """
    print(f"\n[Record] Starting screenrecord for {duration_sec}s -> {local_mp4.name}...")
    adb(["shell", f"rm -f {remote_mp4}"])
    
    # Start screenrecord process
    rec_cmd = [
        "adb", "-s", DEVICE_ID, "shell",
        f"screenrecord --display-id {DISPLAY_ID} --bit-rate 16000000 --time-limit {duration_sec} {remote_mp4}"
    ]
    rec_proc = subprocess.Popen(rec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Small buffer for encoder to start
    time.sleep(0.6)
    start_time = time.time()
    
    for ev in events:
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
    
    print(f"[Record] Pulling {remote_mp4} to {local_mp4}...")
    adb(["pull", remote_mp4, str(local_mp4)])
    adb(["shell", f"rm -f {remote_mp4}"])
    print(f"[Record] Saved: {local_mp4.name} ({local_mp4.stat().st_size} bytes)")

def main():
    print("[Master Sandbox 60s] Sanitizing device environment...")
    adb(["shell", "cmd notification set_zen_mode 1"])
    adb(["shell", "svc power stayon true"])

    # --- SEGMENT 1 (15.0s): POS Catalog & Add Items to Cart ---
    print("\n--- PREPARING SEGMENT 1: POS Catalog & Add to Cart ---")
    # Reset app to fresh Kelontong POS
    adb(["shell", "am force-stop com.nusa.dev"])
    time.sleep(1.0)
    adb(["shell", "am start -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant kelontong --ez pro true --ez onboarding false"])
    time.sleep(3.0)
    adb(["shell", "input tap 540 2476"]) # Enter Kasir
    time.sleep(2.0)

    events_seg1 = [
        {"t_sec": 1.8, "action": "tap", "x": 330, "y": 440, "label": "Tab Sembako", "x_pct": 330/1080, "y_pct": 440/2640},
        {"t_sec": 4.5, "action": "tap", "x": 270, "y": 1250, "label": "Tambah Beras Premium 5kg", "x_pct": 270/1080, "y_pct": 1250/2640},
        {"t_sec": 8.0, "action": "tap", "x": 735, "y": 1250, "label": "Tambah Minyak Goreng 2L", "x_pct": 735/1080, "y_pct": 1250/2640},
    ]

    record_and_automate(
        remote_mp4="/sdcard/seg1_kelontong.mp4",
        local_mp4=OUT_DIR / "seg1_kelontong_raw.mp4",
        duration_sec=15,
        events=events_seg1
    )
    with open(OUT_DIR / "seg1_events.json", "w") as f:
        json.dump(events_seg1, f, indent=2)

    # --- SEGMENT 2 (12.0s): Checkout, QRIS & Receipt ---
    print("\n--- PREPARING SEGMENT 2: Checkout, QRIS & Struk ---")
    events_seg2 = [
        {"t_sec": 1.2, "action": "tap", "x": 815, "y": 2476, "label": "Bayar ->", "x_pct": 815/1080, "y_pct": 2476/2640},
        {"t_sec": 3.2, "action": "tap", "x": 527, "y": 1960, "label": "Pilih QRIS", "x_pct": 527/1080, "y_pct": 1960/2640},
        {"t_sec": 5.8, "action": "swipe", "x1": 540, "y1": 2000, "x2": 540, "y2": 1200, "dur": 300, "label": "Scroll QRIS Card"},
        {"t_sec": 7.5, "action": "tap", "x": 540, "y": 2431, "label": "Cek Status Pembayaran (Lunas)", "x_pct": 540/1080, "y_pct": 2431/2640},
        {"t_sec": 9.8, "action": "tap", "x": 500, "y": 1870, "label": "Cetak Printer", "x_pct": 500/1080, "y_pct": 1870/2640},
    ]

    record_and_automate(
        remote_mp4="/sdcard/seg2_kelontong.mp4",
        local_mp4=OUT_DIR / "seg2_kelontong_raw.mp4",
        duration_sec=12,
        events=events_seg2
    )
    with open(OUT_DIR / "seg2_events.json", "w") as f:
        json.dump(events_seg2, f, indent=2)

    # --- SEGMENT 3 (12.0s): Laporan Penjualan & Outro ---
    print("\n--- PREPARING SEGMENT 3: Laporan Penjualan & Recap ---")
    events_seg3 = [
        {"t_sec": 1.0, "action": "tap", "x": 540, "y": 1630, "label": "Selesai & Tutup Struk", "x_pct": 540/1080, "y_pct": 1630/2640},
        {"t_sec": 2.5, "action": "key", "code": 4, "label": "Back ke Dashboard"},
        {"t_sec": 4.5, "action": "tap", "x": 500, "y": 1950, "label": "Buka Laporan", "x_pct": 500/1080, "y_pct": 1950/2640},
        {"t_sec": 7.5, "action": "swipe", "x1": 540, "y1": 1800, "x2": 540, "y2": 1400, "dur": 400, "label": "Inspect Grafik Omset"},
    ]

    record_and_automate(
        remote_mp4="/sdcard/seg3_kelontong.mp4",
        local_mp4=OUT_DIR / "seg3_kelontong_raw.mp4",
        duration_sec=12,
        events=events_seg3
    )
    with open(OUT_DIR / "seg3_events.json", "w") as f:
        json.dump(events_seg3, f, indent=2)

    print("\n[Master Sandbox 60s] ALL 3 SEGMENTS RECORDED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
