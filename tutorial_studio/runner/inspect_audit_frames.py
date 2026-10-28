import cv2
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

for i in range(1, 9):
    p = OUT_DIR / f"audit_end_ep{i}.png"
    if not p.exists():
        continue
    img = cv2.imread(str(p))
    # Phone screen area inside 1080x1920 canvas:
    # x=190, y=105, w=700, h=1710
    screen = img[105:105+1710, 190:190+700]
    out_crop = OUT_DIR / f"crop_end_ep{i}.png"
    cv2.imwrite(str(out_crop), screen)
    print(f"EP{i} crop saved to {out_crop.name}, size: {screen.shape}")
