import cv2
from pathlib import Path

out_dir = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")
for lbl in ["02s", "07s", "11s", "15s", "19s"]:
    p = out_dir / f"f_ep3_{lbl}.png"
    img = cv2.imread(str(p))
    if img is not None:
        # Check top 120 pixels (status bar region)
        top_slice = img[0:120, :]
        mean_bgr = top_slice.mean(axis=(0, 1))
        # Check bottom badge region (1750 to 1860)
        badge_slice = img[1750:1860, :]
        mean_badge = badge_slice.mean(axis=(0, 1))
        print(f"[{lbl}] {img.shape[1]}x{img.shape[0]} | Top slice mean BGR: {mean_bgr.astype(int)} | Badge mean BGR: {mean_badge.astype(int)}")
