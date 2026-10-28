#!/usr/bin/env python3
"""
Composite PC Web Portal onto Flow MCP Tripod Locked Video (scene-06.mp4)
- 100% Locked-off camera on tripod (0.000px drift)
- Active background motion in print shop
- Monitor width: 938px in 1080x1920 canvas (occupies 87% of frame width!)
- Animated Chrome Web Portal with cursor, click, download feedback, and PDF preview
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
FLOW_VIDEO = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-06.mp4")
PORTAL_PNG = OUT_DIR / "pc_portal_screen.png"
OUTPUT_MP4 = OUT_DIR / "pc_tripod_video_composite.mp4"

FPS = 30
DUR_SEC = 21.0
TOTAL_FRAMES = int(FPS * DUR_SEC)

# 1. Scale quad corners to 1080x1920
scale_x = 1080.0 / 720.0 # 1.5
scale_y = 1920.0 / 1280.0 # 1.5

tl = [48.0 * scale_x, 478.0 * scale_y]
tr = [673.0 * scale_x, 476.0 * scale_y]
br = [669.0 * scale_x, 833.0 * scale_y]
bl = [53.0 * scale_x, 832.0 * scale_y]

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

# 2. Load base web portal screenshot
web_base = cv2.imread(str(PORTAL_PNG))
if web_base is None or web_base.shape[:2] != (web_h, web_w):
    web_base = cv2.resize(web_base, (web_w, web_h)) if web_base is not None else np.zeros((web_h, web_w, 3), dtype=np.uint8)

# 3. Open background video
cap = cv2.VideoCapture(str(FLOW_VIDEO))
bg_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"[PC Tripod Video] Rendering {TOTAL_FRAMES} frames ({DUR_SEC}s @ {FPS}fps)...")
print(f"  Monitor bounds on 1080x1920: width={tr[0]-tl[0]:.1f}px, height={bl[1]-tl[1]:.1f}px")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(str(OUTPUT_MP4), fourcc, FPS, (1080, 1920))

for f in range(TOTAL_FRAMES):
    t = f / FPS # seconds
    
    # Read background frame (looping)
    bg_idx = f % bg_frame_count
    cap.set(cv2.CAP_PROP_POS_FRAMES, bg_idx)
    ret, bg_frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, bg_frame = cap.read()
        
    bg_1080 = cv2.resize(bg_frame, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    bg_masked = cv2.bitwise_and(bg_1080, bg_1080, mask=quad_mask_inv)
    
    # Create animated web frame
    cur_web = web_base.copy()
    
    # Cursor animation
    btn_x, btn_y = 440, 360
    
    if t < 1.5:
        cx, cy = 120, 620
    elif t < 4.0:
        p = (t - 1.5) / 2.5
        cx = int(120 + p * (btn_x - 120))
        cy = int(620 + p * (btn_y - 620))
    elif t < 6.0:
        cx, cy = btn_x, btn_y
    elif t < 7.0:
        cx, cy = btn_x, btn_y
    else:
        cx, cy = btn_x + 90, btn_y + 40
        
    # Interactive feedback on web screen
    if t >= 6.0:
        # Golden border highlight on Skripsi card (#FFE04A)
        cv2.rectangle(cur_web, (80, 190), (600, 440), (74, 224, 255), 3)
        
        if t < 9.0:
            # Downloading state
            cv2.rectangle(cur_web, (btn_x - 70, btn_y - 22), (btn_x + 150, btn_y + 22), (50, 180, 50), -1)
            cv2.putText(cur_web, "Mengunduh 100%...", (btn_x - 60, btn_y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        else:
            # Ready state
            cv2.rectangle(cur_web, (btn_x - 80, btn_y - 22), (btn_x + 160, btn_y + 22), (34, 139, 34), -1)
            cv2.putText(cur_web, "SIAP CETAK (140 HAL)", (btn_x - 70, btn_y + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 255, 255), 2)
            
            # Preview box
            pbox_x, pbox_y = 660, 190
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 490, pbox_y + 370), (255, 255, 255), -1)
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 490, pbox_y + 370), (30, 41, 59), 3)
            # Header
            cv2.rectangle(cur_web, (pbox_x, pbox_y), (pbox_x + 490, pbox_y + 55), (220, 38, 38), -1)
            cv2.putText(cur_web, "PDF PREVIEW : SKRIPSI BUDI", (pbox_x + 20, pbox_y + 36), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            # Content lines
            cv2.putText(cur_web, "File: Budi_Santoso_Skripsi_Final.pdf", (pbox_x + 20, pbox_y + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
            cv2.putText(cur_web, "Jumlah: 140 Halaman Bolak-Balik", (pbox_x + 20, pbox_y + 145), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
            cv2.putText(cur_web, "Finishing: Hardcover Biru Tua Tinta Emas", (pbox_x + 20, pbox_y + 190), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (60, 60, 60), 1)
            cv2.putText(cur_web, "Jumlah Cetak: 3 Buku", (pbox_x + 20, pbox_y + 235), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (60, 60, 60), 1)
            cv2.putText(cur_web, "STATUS: ZERO VIRUS - SIAP PRINT!", (pbox_x + 20, pbox_y + 310), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (34, 139, 34), 2)

    # Draw arrow cursor
    pts_cursor = np.array([[cx, cy], [cx, cy + 24], [cx + 7, cy + 18], [cx + 15, cy + 28], [cx + 20, cy + 25], [cx + 12, cy + 16], [cx + 19, cy + 16]], dtype=np.int32)
    cv2.fillPoly(cur_web, [pts_cursor], (0, 0, 0))
    cv2.polylines(cur_web, [pts_cursor], True, (255, 255, 255), 1)
    
    # Warp web frame into monitor quad
    warped_web = cv2.warpPerspective(cur_web, warp_mat, (1080, 1920), flags=cv2.INTER_LANCZOS4)
    warped_web_masked = cv2.bitwise_and(warped_web, warped_web, mask=quad_mask)
    
    # Combine with background video
    composite_1080 = cv2.add(bg_masked, warped_web_masked)
    writer.write(composite_1080)

cap.release()
writer.release()
print(f"[PC Tripod Video] SUCCESS! Saved {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")
