#!/usr/bin/env python3
"""
Render Beat 3 Workstation Desktop Chrome with 1.40x Dynamic Punch-In (18.0s @ 60 FPS)
Canvas: 1080x1920
Features:
- Premium Dark Slate Studio Aesthetic
- Chrome Window Frame (1000x600 px) with realistic URL bar & controls
- Real Chrome Playwright Recording (real_desktop_beat3_18s.mp4)
- Companion LAN Connection Badge & Samsung Z Flip 3 screen
- Smooth Ease-in-out Camera Zoom (1.0x -> 1.40x) at t=8.0s to 9.0s focused on Skripsi download
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
SRC_DESKTOP_MP4 = OUT_DIR / "real_desktop_beat3_18s.mp4"
BEAT2_RAW_MP4 = OUT_DIR / "mobile_beat2_15.5s.mp4"
OUTPUT_MP4 = OUT_DIR / "rendered_beat3_workstation_18s.mp4"

FPS = 60
DUR = 18.0
TOTAL_FRAMES = int(FPS * DUR)
W, H = 1080, 1920

def create_window_header(win_w, head_h):
    header = np.full((head_h, win_w, 3), (30, 41, 59), dtype=np.uint8) # #1e293b (BGR)
    # 3 window dots: Red, Yellow, Green
    cv2.circle(header, (26, head_h // 2), 6, (68, 68, 239), -1, cv2.LINE_AA)  # Red (#ef4444)
    cv2.circle(header, (46, head_h // 2), 6, (11, 158, 245), -1, cv2.LINE_AA) # Yellow (#f59e0b)
    cv2.circle(header, (66, head_h // 2), 6, (94, 197, 34), -1, cv2.LINE_AA)  # Green (#22c55e)
    
    # URL Pill in center
    pill_w = 460
    pill_h = 24
    pill_x1 = (win_w - pill_w) // 2
    pill_y1 = (head_h - pill_h) // 2
    cv2.rectangle(header, (pill_x1, pill_y1), (pill_x1 + pill_w, pill_y1 + pill_h), (15, 23, 42), -1) # #0f172a
    cv2.rectangle(header, (pill_x1, pill_y1), (pill_x1 + pill_w, pill_y1 + pill_h), (71, 85, 105), 1, cv2.LINE_AA)
    
    # Text
    cv2.putText(header, "http://192.168.1.13:8080/portal-file", (pill_x1 + 35, pill_y1 + 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (148, 163, 184), 1, cv2.LINE_AA)
    cv2.circle(header, (pill_x1 + 18, head_h // 2), 4, (94, 197, 34), -1, cv2.LINE_AA) # green lock/status dot
    return header

def render_workstation():
    print(f"[Workstation Render] Opening {SRC_DESKTOP_MP4.name}...")
    cap_web = cv2.VideoCapture(str(SRC_DESKTOP_MP4))
    
    # Extract companion mobile frame showing connected server dialog
    cap_mob = cv2.VideoCapture(str(BEAT2_RAW_MP4))
    cap_mob.set(cv2.CAP_PROP_POS_FRAMES, 600) # at 10s of beat 2 (dialog is open)
    ret_m, mob_frame = cap_mob.read()
    cap_mob.release()
    if not ret_m:
        mob_frame = np.zeros((2640, 1080, 3), dtype=np.uint8)
        
    mob_scaled = cv2.resize(mob_frame, (320, 782), interpolation=cv2.INTER_AREA)

    win_w = 980
    web_h = int(win_w * 720 / 1280) # 551 px
    head_h = 36
    total_win_h = web_h + head_h
    win_header = create_window_header(win_w, head_h)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(OUTPUT_MP4), fourcc, FPS, (W, H))
    
    # Window placement in canvas
    base_win_x = (W - win_w) // 2 # 50
    base_win_y = 280
    
    # Mobile companion placement in canvas
    mob_x = (W - 320) // 2 # 380
    mob_y = 1020
    
    # Skripsi card center on canvas for punch zoom
    # Skripsi card is on top-left of web content: approx x=320, y=420 inside window
    target_focus_x = base_win_x + 360 # ~410
    target_focus_y = base_win_y + head_h + 200 # ~516
    
    print(f"[Workstation Render] Processing {TOTAL_FRAMES} frames (18.0s @ 60 FPS)...")
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        ret, web_raw = cap_web.read()
        if not ret:
            break
            
        # 1. Base Dark Canvas (#0b1120 with soft subtle gradient)
        canvas = np.full((H, W, 3), (32, 17, 11), dtype=np.uint8) # BGR for #0b1120
        # Add subtle top vignette
        cv2.circle(canvas, (540, 600), 750, (48, 28, 18), -1)
        canvas = cv2.GaussianBlur(canvas, (101, 101), 0)
        
        # 2. Draw Desktop Chrome Window
        web_resized = cv2.resize(web_raw, (win_w, web_h), interpolation=cv2.INTER_LANCZOS4)
        window_img = np.vstack([win_header, web_resized])
        
        # Shadow for desktop window
        cv2.rectangle(canvas, (base_win_x - 4, base_win_y + 10), (base_win_x + win_w + 4, base_win_y + total_win_h + 24), (0, 0, 0), -1)
        canvas = cv2.GaussianBlur(canvas, (25, 25), 0)
        
        # Paste Window
        canvas[base_win_y:base_win_y + total_win_h, base_win_x:base_win_x + win_w] = window_img
        # Window border
        cv2.rectangle(canvas, (base_win_x, base_win_y), (base_win_x + win_w, base_win_y + total_win_h), (56, 189, 248), 1, cv2.LINE_AA)
        
        # 3. Companion Mobile Card & Badge (Bottom half)
        # Badge: "🟢 TERHUBUNG LOCAL LAN • HP KASIR AKTIF"
        badge_w, badge_h = 480, 42
        bx1 = (W - badge_w) // 2
        by1 = 940
        cv2.rectangle(canvas, (bx1, by1), (bx1 + badge_w, by1 + badge_h), (30, 41, 59), -1)
        cv2.rectangle(canvas, (bx1, by1), (bx1 + badge_w, by1 + badge_h), (34, 197, 94), 1, cv2.LINE_AA)
        cv2.putText(canvas, "TERHUBUNG LOCAL LAN - HP KASIR", (bx1 + 45, by1 + 27),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, (241, 245, 249), 2, cv2.LINE_AA)
        cv2.circle(canvas, (bx1 + 24, by1 + 21), 6, (34, 197, 94), -1, cv2.LINE_AA) # pulsing green
        
        # Companion Mobile Frame
        mob_h_box = 460
        mob_crop = mob_scaled[0:mob_h_box, :]
        # Shadow
        cv2.rectangle(canvas, (mob_x - 3, mob_y + 8), (mob_x + 320 + 3, mob_y + mob_h_box + 12), (0, 0, 0), -1)
        # Paste
        canvas[mob_y:mob_y + mob_h_box, mob_x:mob_x + 320] = mob_crop
        cv2.rectangle(canvas, (mob_x, mob_y), (mob_x + 320, mob_y + mob_h_box), (71, 85, 105), 1, cv2.LINE_AA)

        # 4. Dynamic Zoom Punch-In (t = 8.0s to 18.0s)
        # At t=8.0s ("Tinggal satu kali klik Unduh ke PC..."), camera punches in 1.40x onto the Skripsi card & download toast!
        if t < 8.0:
            zoom = 1.0
        elif t < 9.2:
            p = (t - 8.0) / 1.2
            # smooth easeInOutCubic
            ease = 4 * p * p * p if p < 0.5 else 1 - pow(-2 * p + 2, 3) / 2
            zoom = 1.0 + ease * 0.40
        else:
            zoom = 1.40
            
        if zoom > 1.001:
            # Crop centered on target_focus
            crop_w = int(W / zoom)
            crop_h = int(H / zoom)
            x1 = max(0, min(W - crop_w, int(target_focus_x - crop_w / 2)))
            y1 = max(0, min(H - crop_h, int(target_focus_y - crop_h / 2)))
            cropped = canvas[y1:y1 + crop_h, x1:x1 + crop_w]
            out_frame = cv2.resize(cropped, (W, H), interpolation=cv2.INTER_LANCZOS4)
        else:
            out_frame = canvas
            
        writer.write(out_frame)
        if frame_idx % 180 == 0:
            print(f"  Frame {frame_idx}/{TOTAL_FRAMES} (t={t:.1f}s, zoom={zoom:.2f}x)...")
            
    cap_web.release()
    writer.release()
    print(f"[Workstation Success] Video written: {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")
    
    # Convert to standard H.264
    final_h264 = OUT_DIR / "workstation_beat3_18s.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", str(OUTPUT_MP4),
        "-vf", "fps=60",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(final_h264)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Workstation Complete] Standard H.264: {final_h264.name} ({final_h264.stat().st_size} bytes)")

if __name__ == "__main__":
    render_workstation()
