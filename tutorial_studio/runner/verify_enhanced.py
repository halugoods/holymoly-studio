import subprocess
from pathlib import Path
import cv2

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")
vid = OUT_DIR / "ep1_kelontong_qris_enhanced_click_zoom.mp4"
print("Video exists:", vid.exists(), "Size:", vid.stat().st_size / (1024*1024), "MB")

timestamps = [
    ("00:00:01.000", "01s_intro"),
    ("00:00:02.550", "02s_click_beras"),
    ("00:00:04.250", "04s_click_minyak"),
    ("00:00:08.500", "08s_zoom_qris"),
    ("00:00:11.850", "11s_click_bayar"),
    ("00:00:14.200", "14s_receipt")
]

for ts, lbl in timestamps:
    out_f = OUT_DIR / f"enhanced_{lbl}.png"
    subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(vid), "-vframes", "1", str(out_f)], capture_output=True)
    img = cv2.imread(str(out_f))
    if img is not None:
        print(f"[{lbl}] {ts} -> shape: {img.shape}, center: {img[960, 540]}, top-left: {img[50, 50]}")
    else:
        print(f"[{lbl}] {ts} -> Failed to read")
