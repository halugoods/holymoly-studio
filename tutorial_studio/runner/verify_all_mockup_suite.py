import subprocess
from pathlib import Path

ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

VIDEOS = [
    ("ep1", "ep1_kelontong_qris_commercial.mp4"),
    ("ep2", "ep2_fnb_catalog_commercial.mp4"),
    ("ep3", "ep3_laundry_kiloan_commercial.mp4"),
    ("ep4", "ep4_bengkel_servis_commercial.mp4"),
    ("ep5", "ep5_apotek_farmasi_commercial.mp4"),
    ("ep6", "ep6_salon_treatment_commercial.mp4"),
    ("ep7", "ep7_fotocopy_cetak_commercial.mp4"),
    ("ep8", "ep8_servis_gadget_commercial.mp4"),
]

print("=== VERIFYING ALL 8 RE-RENDERED COMMERCIAL VIDEOS ===")
for ep_id, filename in VIDEOS:
    p = ARTIFACT_DIR / filename
    if not p.exists():
        print(f"[{ep_id}] MISSING: {filename}")
        continue
    
    # Check width, height, duration
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-of", "csv=s=x:p=0",
        str(p)
    ]
    res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True)
    size_mb = p.stat().st_size / (1024 * 1024)
    info = res.stdout.strip()
    print(f"[{ep_id}] {filename}: {size_mb:.2f} MB | Stream: {info}")

    # Extract sample frame at 4.0s
    frame_path = ARTIFACT_DIR / f"frame_v2_{ep_id}.png"
    cmd = ["ffmpeg", "-y", "-ss", "00:00:04.000", "-i", str(p), "-vframes", "1", str(frame_path)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"     Extracted frame -> {frame_path.name}")
