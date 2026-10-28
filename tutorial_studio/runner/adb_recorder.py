#!/usr/bin/env python3
"""
ADB Headless Zero-Latency Screen Recorder & Action Runner
(Part of NUSA Autonomous Multi-Skill Tutorial Studio)

Prinsip:
1. Tidak ada LLM thinking loop saat merekam layar HP.
2. DND (Do Not Disturb) diaktifkan sebelum rekam dan dimatikan setelah selesai.
3. Menjalankan timeline aksi terkalibrasi milidetik berbasis persentase layar (%W, %H).
"""

import sys
import time
import json
import subprocess
from pathlib import Path

class AdbTutorialRecorder:
    def __init__(self, device_id=None):
        self.device_id = device_id
        self._detect_device()

    def _adb_cmd(self, args):
        cmd = ["adb"]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        return cmd

    def _run_adb(self, args, check=True):
        cmd = self._adb_cmd(args)
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check)

    def _detect_device(self):
        res = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, text=True)
        lines = [l.strip().split() for l in res.stdout.strip().splitlines()[1:] if l.strip()]
        devices = [l[0] for l in lines if len(l) >= 2 and l[1] == "device"]
        if not devices:
            raise RuntimeError("Tidak ada perangkat ADB yang terhubung!")
        if not self.device_id:
            self.device_id = devices[0]
        print(f"[ADB Recorder] Menggunakan perangkat: {self.device_id}")

    def get_screen_resolution(self):
        res = self._run_adb(["shell", "wm", "size"])
        # Format: Physical size: 1080x2640
        for part in res.stdout.split():
            if "x" in part:
                w, h = part.split("x")
                return int(w), int(h)
        return 1080, 2400

    def pre_flight(self):
        print("[ADB Recorder] Pre-flight: Mengaktifkan mode DND & mengunci layar...")
        # 1. Aktifkan Do Not Disturb (Zen mode = 1)
        self._run_adb(["shell", "cmd", "notification", "set_zen_mode", "1"], check=False)
        # 2. Bangunkan layar & set stay on
        self._run_adb(["shell", "input", "keyevent", "224"], check=False)
        self._run_adb(["shell", "svc", "power", "stayon", "true"], check=False)
        # 3. Kunci kecerahan
        self._run_adb(["shell", "settings", "put", "system", "screen_brightness", "200"], check=False)

    def post_flight(self):
        print("[ADB Recorder] Post-flight: Mengembalikan mode DND normal...")
        # Kembalikan DND ke normal (Zen mode = 0)
        self._run_adb(["shell", "cmd", "notification", "set_zen_mode", "0"], check=False)

    def get_main_display_id(self):
        try:
            res = self._run_adb(["shell", "dumpsys", "SurfaceFlinger", "--display-id"])
            for line in res.stdout.splitlines():
                if "HWC display 0" in line:
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0].lower() == "display":
                        return parts[1]
        except Exception as e:
            print(f"[ADB Recorder] Note on display detection: {e}")
        return None

    def execute_timeline(self, events, total_duration_sec, output_path, remote_temp_path="/sdcard/tutorial_raw.mp4"):
        w, h = self.get_screen_resolution()
        display_id = self.get_main_display_id()
        print(f"[ADB Recorder] Resolusi layar terdeteksi: {w}x{h}, Display ID: {display_id}")

        self.pre_flight()

        # Hitung durasi perekaman aman: 1.0s buffer awal + durasi aksi + 1.5s buffer akhir
        time_limit = int(total_duration_sec + 3)

        # Mulai screenrecord di background Android dengan --time-limit otomatis
        print(f"[ADB Recorder] Memulai perekaman layar ke {remote_temp_path} (limit: {time_limit}s)...")
        self._run_adb(["shell", "rm", "-f", remote_temp_path], check=False)
        record_cmd = ["shell", "screenrecord"]
        if display_id:
            record_cmd.extend(["--display-id", str(display_id)])
        record_cmd.extend([
            "--time-limit", str(time_limit),
            "--size", f"{w}x{h}",
            "--bit-rate", "16000000",
            remote_temp_path
        ])
        record_proc = subprocess.Popen(self._adb_cmd(record_cmd))

        # Beri jeda 1 detik untuk buffer startup encoder Android
        time.sleep(1.0)
        start_time = time.perf_counter()
        print(f"[ADB Recorder] Clock dimulai. Menjalankan {len(events)} aksi deterministik...")

        for ev in sorted(events, key=lambda x: x.get("offset_ms", 0)):
            target_time = ev.get("offset_ms", 0) / 1000.0
            now = time.perf_counter() - start_time
            wait_sec = target_time - now
            if wait_sec > 0:
                time.sleep(wait_sec)

            action = ev.get("action")
            if action == "tap":
                x = int(ev.get("x_pct", 0.5) * w)
                y = int(ev.get("y_pct", 0.5) * h)
                print(f"  [{time.perf_counter() - start_time:05.2f}s] TAP -> ({x}, {y}) [{ev.get('label', '')}]")
                self._run_adb(["shell", "input", "-d", "0", "tap", str(x), str(y)], check=False)

            elif action == "swipe":
                x1 = int(ev.get("x1_pct", 0.5) * w)
                y1 = int(ev.get("y1_pct", 0.8) * h)
                x2 = int(ev.get("x2_pct", 0.5) * w)
                y2 = int(ev.get("y2_pct", 0.2) * h)
                duration = ev.get("duration_ms", 300)
                print(f"  [{time.perf_counter() - start_time:05.2f}s] SWIPE -> ({x1},{y1}) to ({x2},{y2})")
                self._run_adb(["shell", "input", "-d", "0", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)], check=False)

            elif action == "text":
                val = ev.get("value", "")
                print(f"  [{time.perf_counter() - start_time:05.2f}s] TEXT -> '{val}'")
                self._run_adb(["shell", "input", "text", val], check=False)

            elif action == "key":
                code = ev.get("code", "66") # 66 = Enter
                print(f"  [{time.perf_counter() - start_time:05.2f}s] KEYEVENT -> {code}")
                self._run_adb(["shell", "input", "keyevent", str(code)], check=False)

            elif action == "idle" or action == "hold":
                print(f"  [{time.perf_counter() - start_time:05.2f}s] IDLE HOLD (B-Roll or Transition Slot)")

        # Tunggu sampai total durasi selesai
        remaining = total_duration_sec - (time.perf_counter() - start_time)
        if remaining > 0:
            time.sleep(remaining)

        print("[ADB Recorder] Menunggu finalisasi encoder MP4...")
        # Tunggu screenrecord menyelesaikan penulisan moov atom
        try:
            record_proc.wait(timeout=5)
        except Exception:
            self._run_adb(["shell", "pkill", "-INT", "screenrecord"], check=False)
            time.sleep(1.0)

        self.post_flight()

        # Beri jeda 0.5 detik sebelum pull
        time.sleep(0.5)

        # Pull file ke lokal
        dest_file = Path(output_path)
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        print(f"[ADB Recorder] Mengunduh hasil rekaman ke: {dest_file}...")
        self._run_adb(["pull", remote_temp_path, str(dest_file)])
        self._run_adb(["shell", "rm", "-f", remote_temp_path], check=False)

        if dest_file.exists() and dest_file.stat().st_size > 0:
            print(f"[ADB Recorder] Berhasil! Ukuran file: {dest_file.stat().st_size / (1024*1024):.2f} MB")
            return True
        else:
            print("[ADB Recorder] Gagal: File hasil rekaman kosong atau tidak ditemukan.")
            return False

if __name__ == "__main__":
    recorder = AdbTutorialRecorder()
    w, h = recorder.get_screen_resolution()
    print(f"Ready. Device resolution: {w}x{h}")
