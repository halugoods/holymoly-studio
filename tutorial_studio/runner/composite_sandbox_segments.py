#!/usr/bin/env python3
"""
Composite Sandbox Screen Recordings into Centered Z Flip 3 Mockup
Features:
- Locked Centered Samsung Galaxy Z Flip 3 Vector Mockup (cx=540, cy=960)
- Zero Camera Zoom (stable, high-converting, clean)
- Cupertino Tactile Ripple & Haptic Glow at click coordinates
- Seamless 60 FPS Scrolling Blurred Studio Grid
"""

import math
import time
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
MASK_PATH = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PATH = OUT_DIR / "zflip3_frame.png"

# Load pre-baked frame & mask
mask_img = cv2.imread(str(MASK_PATH), cv2.IMREAD_GRAYSCALE)
MASK_BASE = mask_img.astype(np.float32) / 255.0

frame_rgba = cv2.imread(str(FRAME_PATH), cv2.IMREAD_UNCHANGED)
FRAME_BGR = frame_rgba[:, :, :3]
FRAME_ALPHA = frame_rgba[:, :, 3].astype(np.float32) / 255.0

CANVAS_W, CANVAS_H = 1080, 1920
SCREEN_W, SCREEN_H = 700, 1710
SX, SY = 190, 105

# Warm Amber accent for NUSA Kelontong
ACCENT_BGR = (22, 115, 249)

# Bake background strip
def bake_background():
    grid_size = 60
    strip_h = CANVAS_H + grid_size
    bg = Image.new("RGB", (CANVAS_W, strip_h), (14, 16, 22))
    draw = ImageDraw.Draw(bg)

    line_color = (42, 50, 65)
    for x in range(0, CANVAS_W + grid_size, grid_size):
        draw.line([(x, 0), (x, strip_h)], fill=line_color, width=1)
    for y in range(0, strip_h + grid_size, grid_size):
        draw.line([(0, y), (CANVAS_W, y)], fill=line_color, width=1)

    bg = bg.filter(ImageFilter.GaussianBlur(radius=2.2))

    glow = Image.new("RGBA", (CANVAS_W, strip_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse(
        [CANVAS_W//2 - 420, strip_h//2 - 620, CANVAS_W//2 + 420, strip_h//2 + 620],
        fill=(38, 48, 64, 45)
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=75))
    bg.paste(glow, (0, 0), glow)

    return cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR), grid_size

BG_STRIP, GRID_SIZE = bake_background()

def composite_segment(input_mp4, events_json, target_duration_sec, output_mp4):
    print(f"\n[Compositor] Processing {input_mp4.name} -> {output_mp4.name} (target: {target_duration_sec}s @ 60 FPS)...")
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Gagal membuka: {input_mp4}")

    src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_src_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(events_json, "r") as f:
        events = json.load(f)

    tap_events = [ev for ev in events if ev.get("action") == "tap"]

    total_target_frames = int(target_duration_sec * 60.0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_mp4), fourcc, 60.0, (CANVAS_W, CANVAS_H))

    last_frame = None
    t0 = time.time()
    for frame_idx in range(total_target_frames):
        t_sec = frame_idx / 60.0
        
        # Read next frame sequentially (blazing fast, zero keyframe seek)
        ret, frame = cap.read()
        if ret:
            last_frame = frame
        elif last_frame is not None:
            frame = last_frame
        else:
            break

        # 1. Background grid scroll
        offset_y = int(frame_idx * 1.2) % GRID_SIZE
        bg = BG_STRIP[offset_y:offset_y + CANVAS_H, 0:CANVAS_W].copy()

        # 2. Scale screen frame to 700x1710
        screen_scaled = cv2.resize(frame, (SCREEN_W, SCREEN_H), interpolation=cv2.INTER_LINEAR)
        screen_masked = (screen_scaled.astype(np.float32) * MASK_BASE[:, :, np.newaxis]).astype(np.uint8)

        # 3. Draw Cupertino tactile ripple on screen at tap positions
        for tap in tap_events:
            dt = t_sec - tap["t_sec"]
            if 0.0 <= dt <= 0.40:
                p = dt / 0.40
                tx = int(tap.get("x_pct", 0.5) * SCREEN_W)
                ty = int(tap.get("y_pct", 0.5) * SCREEN_H)

                radius = int(14 + 70 * math.sqrt(p))
                alpha = max(0.0, (1.0 - p) * 0.90)

                overlay = screen_masked.copy()
                thickness = max(1, int(4 * (1.0 - p)))
                cv2.circle(overlay, (tx, ty), radius, ACCENT_BGR, thickness, cv2.LINE_AA)
                
                # Soft center pulse
                if p < 0.25:
                    cv2.circle(overlay, (tx, ty), int(10 * (1.0 - p * 4)), (255, 255, 255), -1, cv2.LINE_AA)

                screen_masked = cv2.addWeighted(overlay, alpha, screen_masked, 1.0 - alpha, 0)

        # 4. Composite screen onto phone canvas
        phone_canvas = np.zeros((CANVAS_H, CANVAS_W, 4), dtype=np.uint8)
        screen_rgba = np.zeros((SCREEN_H, SCREEN_W, 4), dtype=np.uint8)
        screen_rgba[:, :, :3] = screen_masked
        screen_rgba[:, :, 3] = (MASK_BASE * 255).astype(np.uint8)
        phone_canvas[SY:SY+SCREEN_H, SX:SX+SCREEN_W] = screen_rgba

        # 5. Overlay Z Flip 3 vector frame (bezels, punch-hole, shadow)
        f_bgr = FRAME_BGR
        f_alpha = FRAME_ALPHA[:, :, np.newaxis]
        p_bgr = phone_canvas[:, :, :3].astype(np.float32)
        p_a = (phone_canvas[:, :, 3] / 255.0)[:, :, np.newaxis]

        out_bgr = f_bgr.astype(np.float32) * f_alpha + p_bgr * (1.0 - f_alpha)
        out_alpha = np.clip(f_alpha + p_a * (1.0 - f_alpha), 0.0, 1.0)

        # 6. Composite phone over background grid
        final_frame = (out_bgr * out_alpha + bg.astype(np.float32) * (1.0 - out_alpha)).astype(np.uint8)
        writer.write(final_frame)

    cap.release()
    writer.release()
    elapsed = time.time() - t0
    fps = total_target_frames / elapsed
    print(f"[Compositor] Finished in {elapsed:.1f}s ({fps:.1f} FPS) -> {output_mp4.name}")

def main():
    # Segment 1: 15.0s
    composite_segment(
        input_mp4=OUT_DIR / "seg1_kelontong_raw.mp4",
        events_json=OUT_DIR / "seg1_events.json",
        target_duration_sec=15.0,
        output_mp4=OUT_DIR / "seg1_mockup_15s.mp4"
    )

    # Segment 2: 12.0s
    composite_segment(
        input_mp4=OUT_DIR / "seg2_kelontong_raw.mp4",
        events_json=OUT_DIR / "seg2_events.json",
        target_duration_sec=12.0,
        output_mp4=OUT_DIR / "seg2_mockup_12s.mp4"
    )

    # Segment 3: 12.0s
    composite_segment(
        input_mp4=OUT_DIR / "seg3_kelontong_raw.mp4",
        events_json=OUT_DIR / "seg3_events.json",
        target_duration_sec=12.0,
        output_mp4=OUT_DIR / "seg3_mockup_12s.mp4"
    )

    print("\n[Compositor] ALL 3 MOCKUP SEGMENTS COMPOSITED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
