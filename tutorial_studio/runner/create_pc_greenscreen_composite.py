#!/usr/bin/env python3
"""
Composite PC Web Portal onto Flow MCP Green Screen Monitor (scene-03-v2.jpeg)
Features:
- Renders high-res 16:9 Chrome browser showing http://192.168.1.13:8080/portal-file
- Animated cursor hovering & clicking 'Unduh ke PC' on Skripsi Budi Santoso
- Golden highlighter sweep (#FFE04A) + download progress & PDF ready badge
- Quad-warps web frames onto green screen monitor of scene-03-v2.jpeg
- Dynamic camera push (1.0x wide shop shot -> 2.2x zoom into monitor)
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
FLOW_IMG = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-03-v2.jpeg")
PORTAL_PNG = OUT_DIR / "pc_portal_screen.png"
OUTPUT_MP4 = OUT_DIR / "pc_greenscreen_composite.mp4"

FPS = 30
DUR_SEC = 21.0
TOTAL_FRAMES = int(FPS * DUR_SEC)

# 1. Load background image and scale to 1080x1920
bg_orig = cv2.imread(str(FLOW_IMG))
bg_1080 = cv2.resize(bg_orig, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)

# 2. Quad corners on 1080x1920
scale_x = 1080.0 / 768.0
scale_y = 1920.0 / 1376.0

tl = [193 * scale_x, 671 * scale_y]
bl = [196 * scale_x, 889 * scale_y]
br = [581 * scale_x, 886 * scale_y]
tr = [582 * scale_x, 670 * scale_y]

dst_pts = np.array([tl, tr, br, bl], dtype=np.float32)

# Source web screen size (1280x720)
web_w, web_h = 1280, 720
src_pts = np.array([
    [0, 0],
    [web_w, 0],
    [web_w, web_h],
    [0, web_h]
], dtype=np.float32)

warp_mat = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Mask for the quad
quad_mask = np.zeros((1920, 1080), dtype=np.uint8)
cv2.fillConvexPoly(quad_mask, dst_pts.astype(np.int32), 255)
quad_mask_inv = cv2.bitwise_not(quad_mask)
bg_masked = cv2.bitwise_and(bg_1080, bg_1080, mask=quad_mask_inv)

# 3. Load base web portal screenshot
web_base = cv2.imread(str(PORTAL_PNG))
if web_base is None or web_base.shape[:2] != (web_h, web_w):
    web_base = cv2.resize(web_base, (web_w, web_h)) if web_base is not None else np.zeros((web_h, web_w, 3), dtype=np.uint8)

print(f"[PC Greenscreen] Generating {TOTAL_FRAMES} frames ({DUR_SEC}s @ {FPS}fps)...")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(str(OUTPUT_MP4), fourcc, FPS, (1080, 1920))

for f in range(TOTAL_FRAMES):
    t = f / FPS # seconds
    
    # Create animated web frame
    cur_web = web_base.copy()
    
    # Cursor animation (enters at t=2.0s, hovers at t=4.0s, clicks at t=6.5s)
    # Unduh button for card 1 is around x=420, y=360
    btn_x, btn_y = 440, 360
    
    if t < 2.0:
        cx, cy = 100, 600
        clicking = False
    elif t < 4.5:
        # Move cursor to button
        p = (t - 2.0) / 2.5
        cx = int(100 + p * (btn_x - 100))
        cy = int(600 + p * (btn_y - 600))
        clicking = False
    elif t < 6.5:
        cx, cy = btn_x, btn_y
        clicking = False
    elif t < 7.5:
        # Click action
        cx, cy = btn_x, btn_y
        clicking = True
    else:
        # After click: move cursor slightly aside
        cx, cy = btn_x + 80, btn_y + 40
        clicking = False
    
    # Button highlight & download feedback after t >= 6.5s
    if t >= 6.5:
        # Highlight card with subtle yellow glow
        cv2.rectangle(cur_web, (80, 190), (600, 440), (74, 224, 255), 3) # #FFE04A in BGR
        
        # Draw "Mengunduh..." or "✅ Berkas Siap Cetak (Budi_Santoso_Skripsi.pdf)" badge
        if t < 9.5:
            cv2.rectangle(cur_web, (btn_x - 60, btn_y - 20), (btn_x + 140, btn_y + 20), (50, 180, 50), -1)
            cv2.putText(cur_web, "Mengunduh 100%...", (btn_x - 50, btn_y + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.rectangle(cur_web, (btn_x - 70, btn_y - 20), (btn_x + 150, btn_y + 20), (34, 139, 34), -1)
            cv2.putText(cur_web, "SIAP DICETAK (140 HAL)", (btn_x - 60, btn_y + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            
            # Show floating PDF preview document box
            pbox_x, pbox_y = 660, 200
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 480, pbox_y + 360), (255, 255, 255), -1)
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 480, pbox_y + 360), (30, 41, 59), 3)
            # Header
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 480, pbox_y + 50), (220, 38, 38), -1)
            cv2.putText(cur_web, "PDF PREVIEW : SKRIPSI BUDI SANTOSO", (pbox_x + 20, pbox_y + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            # Content lines
            cv2.putText(cur_web, "Judul: ANALISIS SISTEM INFORMASI KASIR", (pbox_x + 20, pbox_y + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
            cv2.putText(cur_web, "Total Halaman: 140 Lembar (Bolak-Balik)", (pbox_x + 20, pbox_y + 130), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
            cv2.putText(cur_web, "Finishing: Jilid Hardcover Tinta Emas (3 Rangkap)", (pbox_x + 20, pbox_y + 170), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (50, 50, 50), 1)
            cv2.putText(cur_web, "Status: ZERO VIRUS - SIAP PRINT", (pbox_x + 20, pbox_y + 240), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (34, 139, 34), 2)
    
    # Draw arrow cursor
    pts_cursor = np.array([[cx, cy], [cx, cy + 22], [cx + 6, cy + 17], [cx + 14, cy + 26], [cx + 18, cy + 24], [cx + 10, cy + 15], [cx + 17, cy + 15]], dtype=np.int32)
    cv2.fillPoly(cur_web, [pts_cursor], (0, 0, 0))
    cv2.polylines(cur_web, [pts_cursor], True, (255, 255, 255), 1)
    
    # Warp web frame into monitor quad
    warped_web = cv2.warpPerspective(cur_web, warp_mat, (1080, 1920), flags=cv2.INTER_LANCZOS4)
    warped_web_masked = cv2.bitwise_and(warped_web, warped_web, mask=quad_mask)
    
    # Combine with background
    composite_1080 = cv2.add(bg_masked, warped_web_masked)
    
    # Dynamic camera zoom:
    # 0s to 3s: zoom = 1.0 (wide counter)
    # 3s to 8s: zoom smoothly ramps from 1.0 -> 2.1 into monitor center
    # 8s to 21s: zoom = 2.1 (close-up on monitor actions)
    center_x = (tl[0] + tr[0]) / 2.0
    center_y = (tl[1] + bl[1]) / 2.0
    
    if t < 3.0:
        zoom = 1.0
    elif t < 8.0:
        p = (t - 3.0) / 5.0
        # Smooth ease in-out
        p_smooth = p * p * (3 - 2 * p)
        zoom = 1.0 + p_smooth * 1.15 # 1.0 -> 2.15
    else:
        zoom = 2.15
    
    if zoom > 1.001:
        crop_w = int(1080 / zoom)
        crop_h = int(1920 / zoom)
        
        # Center crop around monitor
        x1 = int(center_x - crop_w / 2)
        y1 = int(center_y - crop_h / 2)
        
        # Boundary clamp
        x1 = max(0, min(1080 - crop_w, x1))
        y1 = max(0, min(1920 - crop_h, y1))
        
        cropped = composite_1080[y1:y1+crop_h, x1:x1+crop_w]
        frame_final = cv2.resize(cropped, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    else:
        frame_final = composite_1080
        
    writer.write(frame_final)

writer.release()
print(f"[PC Greenscreen] SUCCESS! Saved to: {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")
