import cv2
from pathlib import Path

out_dir = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")
for lbl in ["02s", "06s", "10s", "16s", "23s"]:
    p = out_dir / f"f_ep5_{lbl}.png"
    img = cv2.imread(str(p))
    if img is not None:
        top_slice = img[0:120, :]
        mean_bgr = top_slice.mean(axis=(0, 1))
        badge_slice = img[1750:1860, :]
        mean_badge = badge_slice.mean(axis=(0, 1))
        print(f"[{lbl}] {img.shape[1]}x{img.shape[0]} | Top slice mean BGR: {mean_bgr.astype(int)} | Badge mean BGR: {mean_badge.astype(int)}")
