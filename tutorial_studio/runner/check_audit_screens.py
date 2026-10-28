import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

# Screen area in mockup: x=190..890, y=105..1815
for i in range(1, 9):
    p = OUT_DIR / f"audit_end_ep{i}.png"
    if not p.exists():
        continue
    img = cv2.imread(str(p))
    screen = img[105:1815, 190:890]
    # Check middle area of screen (around y=900..1200) for white modal receipt
    mid_roi = screen[600:1200, 100:600]
    # In receipt dialog, background is white/light grey (Struk Pesanan)
    mean_val = mid_roi.mean()
    # Check if header has text "Struk Pesanan"
    print(f"[EP{i}] Screen center mean brightness: {mean_val:.1f}")
