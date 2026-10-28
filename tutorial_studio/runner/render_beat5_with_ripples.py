#!/usr/bin/env python3
"""
Render Beat 5 Mockup with Tactile Touch Tap Ripples (V7 Master)
- Centered Samsung Galaxy Z Flip 3 vector mockup on scrolling grid.
- Duration: 16.000s @ 60 FPS (960 frames).
- Taps:
  1. t = 0.80s - 1.25s: Tap 'Bayar di Kasir' at (767, 952)
  2. t = 3.60s - 4.05s: Tap 'Tambah Print Warna A4' at (795, 739)
  3. t = 6.20s - 6.65s: Tap 'Bayar' bottom bar at (883, 2475)
  4. t = 8.70s - 9.15s: Tap 'Pembayaran Tunai' at (540, 2590)
  5. t >= 11.0s: Digital receipt held till 16.0s.
"""

import os
import sys
import time
import subprocess
import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
V4_DIR = OUT_DIR / "fresh_v4"

GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"
BEAT5_RAW = V4_DIR / "mobile_beat5_15.0s.mp4"

OUTPUT_MP4 = V4_DIR / "mockup_beat5_16.0s.mp4"
TEMP_RAW_MP4 = V4_DIR / "temp_mockup_beat5_raw.mp4"

FPS = 60
DUR = 16.000
TOTAL_FRAMES = int(FPS * DUR) # 960 frames
W, H = 1080, 1920

mask_rgba = cv2.imread(str(MASK_PNG), cv2.IMREAD_UNCHANGED)
frame_rgba = cv2.imread(str(FRAME_PNG), cv2.IMREAD_UNCHANGED)
f_alpha = (frame_rgba[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
f_bgr = frame_rgba[:, :, :3]

def draw_touch_ripple(frame_bgr, cx, cy, progress, max_radius=85, color=(56, 189, 248)):
    if progress < 0.0 or progress > 1.0:
        return
    h, w = frame_bgr.shape[:2]
    r = int(max_radius * (1.0 - (1.0 - progress) ** 2))
    alpha = (1.0 - progress) * 0.88
    x1, y1 = max(0, cx - r - 8), max(0, cy - r - 8)
    x2, y2 = min(w, cx + r + 8), min(h, cy + r + 8)
    if x2 <= x1 or y2 <= y1:
        return
    patch = frame_bgr[y1:y2, x1:x2].copy()
    overlay = patch.copy()
    local_cx, local_cy = cx - x1, cy - y1
    inner_r = max(4, int(r * 0.35))
    cv2.circle(overlay, (local_cx, local_cy), inner_r, (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(overlay, (local_cx, local_cy), r, color, 4, cv2.LINE_AA)
    if r > 8:
        cv2.circle(overlay, (local_cx, local_cy), max(1, r - 6), color, 2, cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, patch, 1.0 - alpha, 0, patch)
    frame_bgr[y1:y2, x1:x2] = patch

def build_phone_mockup_rgba(mobile_bgr):
    screen_scaled = cv2.resize(mobile_bgr, (700, 1710), interpolation=cv2.INTER_LANCZOS4)
    alpha = mask_rgba[:, :, 3]
    screen_rgba = cv2.cvtColor(screen_scaled, cv2.COLOR_BGR2BGRA)
    screen_rgba[:, :, 3] = alpha
    
    phone_comp = np.zeros((1920, 1080, 4), dtype=np.uint8)
    phone_comp[105:105+1710, 190:190+700] = screen_rgba
    
    bgr_part = phone_comp[:, :, :3]
    blended_bgr = (f_bgr * f_alpha + bgr_part * (1.0 - f_alpha)).astype(np.uint8)
    phone_comp[:, :, :3] = blended_bgr
    phone_comp[:, :, 3] = np.maximum(frame_rgba[:, :, 3], phone_comp[:, :, 3])
    return phone_comp

def render():
    print(f"[Beat 5 Engine V7] Rendering {TOTAL_FRAMES} frames ({DUR}s @ {FPS}fps)...")
    cap_grid = cv2.VideoCapture(str(GRID_MP4))
    cap_mob = cv2.VideoCapture(str(BEAT5_RAW))
    mob_total = int(cap_mob.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(TEMP_RAW_MP4), fourcc, FPS, (W, H))
    
    t0 = time.time()
    last_frame = None
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        
        # 1. Background grid
        ret_g, grid_frame = cap_grid.read()
        if not ret_g:
            cap_grid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_g, grid_frame = cap_grid.read()
        canvas = grid_frame.copy()
        
        # 2. Read mobile screen
        ret_m, mob_frame = cap_mob.read()
        if ret_m:
            last_frame = mob_frame.copy()
        else:
            mob_frame = last_frame.copy() if last_frame is not None else np.zeros((2640, 1080, 3), dtype=np.uint8)
            
        # Draw ripples on mob_frame
        # Tap 1: Bayar di Kasir at (767, 952)
        if 0.80 <= t <= 1.25:
            p_rip = (t - 0.80) / 0.45
            draw_touch_ripple(mob_frame, 767, 952, p_rip, max_radius=85, color=(56, 189, 248))
        # Tap 2: Tambah Print Warna A4 at (795, 739)
        elif 3.60 <= t <= 4.05:
            p_rip = (t - 3.60) / 0.45
            draw_touch_ripple(mob_frame, 795, 739, p_rip, max_radius=85, color=(56, 189, 248))
        # Tap 3: Bayar bottom bar at (883, 2475)
        elif 6.20 <= t <= 6.65:
            p_rip = (t - 6.20) / 0.45
            draw_touch_ripple(mob_frame, 883, 2475, p_rip, max_radius=85, color=(56, 189, 248))
        # Tap 4: Pembayaran Tunai at (540, 2590)
        elif 8.70 <= t <= 9.15:
            p_rip = (t - 8.70) / 0.45
            draw_touch_ripple(mob_frame, 540, 2590, p_rip, max_radius=85, color=(56, 189, 248))
            
        mockup_rgba = build_phone_mockup_rgba(mob_frame)
        
        # Alpha blend mockup onto canvas (centered scale 1.0, cx 540, cy 960)
        alpha = (mockup_rgba[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
        canvas = (mockup_rgba[:, :, :3] * alpha + canvas * (1.0 - alpha)).astype(np.uint8)
        
        writer.write(canvas)
        
        if frame_idx % 150 == 0:
            elapsed = time.time() - t0
            fps_proc = (frame_idx + 1) / max(0.1, elapsed)
            print(f"  Frame {frame_idx}/{TOTAL_FRAMES} ({t:.2f}s) - {fps_proc:.1f} fps")
            
    cap_grid.release()
    cap_mob.release()
    writer.release()
    
    print("[Beat 5 Engine] Re-encoding with libx264...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(TEMP_RAW_MP4),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(OUTPUT_MP4)
    ]
    subprocess.run(cmd, check=True)
    if TEMP_RAW_MP4.exists():
        TEMP_RAW_MP4.unlink()
    print(f"[Beat 5 Success] Saved {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")

if __name__ == "__main__":
    render()
