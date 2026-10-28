import cv2
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

for i in range(1, 9):
    p = OUT_DIR / f"audit_end_ep{i}.png"
    if not p.exists():
        continue
    img = cv2.imread(str(p))
    # Crop the phone screen window: x=190..890, y=105..1815
    screen = img[105:1815, 190:890]
    out_crop = OUT_DIR / f"crop_end_ep{i}.png"
    cv2.imwrite(str(out_crop), screen)
    print(f"Saved crop_end_ep{i}.png ({screen.shape[1]}x{screen.shape[0]})")
