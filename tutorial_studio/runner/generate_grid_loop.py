#!/usr/bin/env python3
"""
Generate a 2-second (120 frames @ 60 FPS) seamlessly looping video of the vertical scrolling blurred grid.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

def generate_grid_loop():
    w, h = 1080, 1920
    fps = 60
    duration_sec = 2.0
    total_frames = int(fps * duration_sec) # 120 frames
    grid_size = 60
    speed_px_per_frame = 2 # 2 px per frame -> exactly 240 px in 120 frames, which is 4 full grid cycles (240 % 60 == 0) -> SEAMLESS!

    strip_h = h + grid_size
    # Base background
    bg = Image.new("RGB", (w, strip_h), (14, 16, 22))
    draw = ImageDraw.Draw(bg)

    line_color = (42, 50, 65)
    for x in range(0, w + grid_size, grid_size):
        draw.line([(x, 0), (x, strip_h)], fill=line_color, width=1)
    for y in range(0, strip_h + grid_size, grid_size):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)

    # Soft Gaussian blur on grid
    bg = bg.filter(ImageFilter.GaussianBlur(radius=2.2))

    # Center spotlight / radial gradient
    glow = Image.new("RGBA", (w, strip_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([w//2 - 420, strip_h//2 - 620, w//2 + 420, strip_h//2 + 620], fill=(36, 46, 62, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=80))
    bg.paste(glow, (0, 0), glow)

    bg_np = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR)

    out_mp4 = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/grid_loop_60fps.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(out_mp4), fourcc, fps, (w, h))

    print(f"[GridLoop] Rendering {total_frames} frames of seamless scrolling blurred grid...")
    for f in range(total_frames):
        y_off = int((f * speed_px_per_frame) % grid_size)
        frame = bg_np[y_off:y_off + h, 0:w]
        out.write(frame)

    out.release()
    print(f"[GridLoop] Saved seamless grid loop to: {out_mp4} ({out_mp4.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    generate_grid_loop()
