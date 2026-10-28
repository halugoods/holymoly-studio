#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path

video = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744/nusa_kelontong_60s_flagship_clean.mp4")
art_dir = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

# 1. FFprobe metadata check
cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(video)]
res = subprocess.run(cmd, capture_output=True, text=True, check=True)
meta = json.loads(res.stdout)

dur = float(meta["format"]["duration"])
v_stream = next(s for s in meta["streams"] if s["codec_type"] == "video")
a_stream = next(s for s in meta["streams"] if s["codec_type"] == "audio")

print("=== 1. STREAM METADATA AUDIT ===")
print(f"Duration: {dur:.2f}s (exact: {dur})")
print(f"Video: {v_stream['width']}x{v_stream['height']} @ {v_stream.get('r_frame_rate')} fps, codec: {v_stream['codec_name']}")
print(f"Audio: {a_stream.get('sample_rate')} Hz, codec: {a_stream['codec_name']}, channels: {a_stream.get('channels')}")

# 2. Extract Audit Frames
timestamps = [
    (2.5, "final_audit_beat1_warung_desk.png"),
    (6.5, "final_audit_beat1_warung_face.png"),
    (16.0, "final_audit_beat2_mockup_pos.png"),
    (27.0, "final_audit_beat3_customer_scan.png"),
    (36.0, "final_audit_beat4_mockup_struk.png"),
    (45.0, "final_audit_beat5_printer.png"),
    (54.0, "final_audit_beat6_mockup_laporan.png")
]

print("\n=== 2. AUDIT FRAME EXTRACTION ===")
for t, name in timestamps:
    out = art_dir / name
    cmd = ["ffmpeg", "-y", "-ss", str(t), "-i", str(video), "-vframes", "1", "-q:v", "2", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Extracted {name} at {t}s ({out.stat().st_size} bytes)")

# 3. Audio Continuity Check
print("\n=== 3. AUDIO CONTINUITY AUDIT ===")
cmd = ["ffmpeg", "-y", "-i", str(video), "-f", "s16le", "-ac", "1", "-ar", "24000", "-"]
res = subprocess.run(cmd, capture_output=True, check=True)
raw = res.stdout
import numpy as np
samples = np.frombuffer(raw, dtype=np.int16)
sr = 24000
win = int(sr * 0.05)
hop = int(sr * 0.02)
rms = np.array([np.sqrt(np.mean(samples[i:i+win].astype(float)**2)) for i in range(0, len(samples)-win, hop)])
times = np.arange(len(rms)) * hop / sr

is_silent = rms < 300
long_silences = []
in_silence = False
sil_start = 0

for idx, sil in enumerate(is_silent):
    t = times[idx]
    if t < 0.5 or t > 56.5:
        continue
    if sil and not in_silence:
        in_silence = True
        sil_start = t
    elif not sil and in_silence:
        in_silence = False
        if t - sil_start > 1.0:
            long_silences.append((sil_start, t, t - sil_start))

print(f"Total Audio Samples: {len(samples)} ({len(samples)/sr:.2f}s)")
print(f"Silences > 1.0s in active zone (0.5s - 56.5s): {len(long_silences)}")
if len(long_silences) == 0:
    print("AUDIO STATUS: PASSED - Continuous, seamless natural speech flow!")
else:
    for s, e, d in long_silences:
        print(f"  WARNING Silence at {s:.2f}s - {e:.2f}s ({d:.2f}s)")
