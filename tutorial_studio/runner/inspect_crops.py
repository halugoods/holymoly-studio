import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

for i in range(1, 9):
    p = OUT_DIR / f"crop_end_ep{i}.png"
    if not p.exists():
        continue
    img = cv2.imread(str(p))
    h, w, _ = img.shape
    
    # Check bottom region: (h - 400) to h
    bottom_slice = img[h - 400:h, :]
    
    # Check if there is a green button (Share WA) or blue button (Cetak Printer) or text
    # Let's check mean color of bottom 300px
    b_mean = bottom_slice.mean(axis=(0, 1))
    
    # Check center for receipt dialog: receipt has a distinctive dark modal background (overlay)
    # around the edges, e.g. at (100, 100)
    corner_color = img[50:150, 50:150].mean(axis=(0, 1))
    center_color = img[700:1000, 200:500].mean(axis=(0, 1))
    
    print(f"EP{i}: Corner BGR={corner_color.astype(int)}, Center BGR={center_color.astype(int)}, Bottom BGR={b_mean.astype(int)}")
