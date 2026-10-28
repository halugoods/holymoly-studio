#!/usr/bin/env python3
import wave
import numpy as np
from pathlib import Path

vo_test_file = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/kelontong_60s_vo_test.wav")
out_file = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/kelontong_60s_vo.wav")

with wave.open(str(vo_test_file), "rb") as wf:
    sr = wf.getframerate()
    raw = wf.readframes(wf.getnframes())
    samples = np.frombuffer(raw, dtype=np.int16)

BEAT_ALIGNMENT = [
    {"id": "beat1_warung",  "src_slice": (0.05, 6.90),  "target_start": 0.8},
    {"id": "beat2_pos",     "src_slice": (7.05, 17.90), "target_start": 9.8},
    {"id": "beat3_scan",    "src_slice": (18.15, 22.60), "target_start": 24.5},
    {"id": "beat4_struk",   "src_slice": (22.80, 31.85), "target_start": 30.8},
    {"id": "beat5_printer", "src_slice": (32.10, 37.05), "target_start": 42.5},
    {"id": "beat6_laporan", "src_slice": (37.20, 44.97), "target_start": 48.8},
]

total_samples = int(60.0 * sr)
master_audio = np.zeros(total_samples, dtype=np.int16)

for b in BEAT_ALIGNMENT:
    s_sec, e_sec = b["src_slice"]
    src_sub = samples[int(s_sec * sr):int(e_sec * sr)]
    tgt_start_idx = int(b["target_start"] * sr)
    tgt_end_idx = tgt_start_idx + len(src_sub)
    master_audio[tgt_start_idx:tgt_end_idx] = src_sub
    actual_dur = len(src_sub) / sr
    end_time = tgt_end_idx / sr
    print(f"[{b['id']}] Placed at {b['target_start']:.2f}s - {end_time:.2f}s (duration: {actual_dur:.2f}s)")

with wave.open(str(out_file), "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(master_audio.tobytes())

print(f"Successfully assembled {out_file} (duration: {len(master_audio)/sr:.2f}s)")
