#!/usr/bin/env python3
"""
Render Beat 3 Workstation Studio (17.30s @ 60 FPS)
Canvas: 1080x1920
"""

import sys
import subprocess
import cv2
import numpy as np
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fresh_v4")
SRC_DESKTOP_MP4 = OUT_DIR / "real_desktop_beat3_17.3s.mp4"
BEAT2_RAW_MP4 = OUT_DIR / "mobile_beat2_15.0s.mp4"
TEMP_MP4 = OUT_DIR / "temp_workstation_17.3s.mp4"
OUTPUT_MP4 = OUT_DIR / "workstation_beat3_17.3s.mp4"

FPS = 60
DUR = 17.300
TOTAL_FRAMES = int(FPS * DUR) # 1038 frames
W, H = 1080, 1920

def create_window_header(win_w, head_h):
    header = np.full((head_h, win_w, 3), (30, 41, 59), dtype=np.uint8) # #1e293b
    cv2.circle(header, (26, head_h // 2), 6, (68, 68, 239), -1, cv2.LINE_AA)  # Red
    cv2.circle(header, (46, head_h // 2), 6, (11, 158, 245), -1, cv2.LINE_AA) # Yellow
    cv2.circle(header, (66, head_h // 2), 6, (94, 197, 34), -1, cv2.LINE_AA)  # Green
    
    pill_w, pill_h = 460, 24
    pill_x1 = (win_w - pill_w) // 2
    pill_y1 = (head_h - pill_h) // 2
    cv2.rectangle(header, (pill_x1, pill_y1), (pill_x1 + pill_w, pill_y1 + pill_h), (15, 23, 42), -1)
    cv2.rectangle(header, (pill_x1, pill_y1), (pill_x1 + pill_w, pill_y1 + pill_h), (71, 85, 105), 1, cv2.LINE_AA)
    
    cv2.putText(header, "http://192.168.1.13:8080/portal-file", (pill_x1 + 35, pill_y1 + 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (148, 163, 184), 1, cv2.LINE_AA)
    cv2.circle(header, (pill_x1 + 18, head_h // 2), 4, (94, 197, 34), -1, cv2.LINE_AA)
    return header

def render_workstation():
    print(f"[Workstation V4] Opening {SRC_DESKTOP_MP4.name}...")
    cap_web = cv2.VideoCapture(str(SRC_DESKTOP_MP4))
    
    cap_mob = cv2.VideoCapture(str(BEAT2_RAW_MP4))
    cap_mob.set(cv2.CAP_PROP_POS_FRAMES, 720) # at 12s of beat 2 (dialog is open)
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
    writer = cv2.VideoWriter(str(TEMP_MP4), fourcc, FPS, (W, H))
    
    base_win_x = (W - win_w) // 2 # 50
    base_win_y = 280
    
    mob_x = (W - 320) // 2 # 380
    mob_y = 1020
    
    target_focus_x = base_win_x + 360
    target_focus_y = base_win_y + head_h + 200
    
    print(f"[Workstation V4] Processing {TOTAL_FRAMES} frames ({DUR}s @ {FPS}fps)...")
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        ret, web_raw = cap_web.read()
        if not ret:
            break
            
        canvas = np.full((H, W, 3), (32, 17, 11), dtype=np.uint8)
        cv2.circle(canvas, (540, 600), 750, (48, 28, 18), -1)
        canvas = cv2.GaussianBlur(canvas, (101, 101), 0)
        
        web_resized = cv2.resize(web_raw, (win_w, web_h), interpolation=cv2.INTER_LANCZOS4)
        window_img = np.vstack([win_header, web_resized])
        
        cv2.rectangle(canvas, (base_win_x - 4, base_win_y + 10), (base_win_x + win_w + 4, base_win_y + total_win_h + 24), (0, 0, 0), -1)
        canvas = cv2.GaussianBlur(canvas, (25, 25), 0)
        
        canvas[base_win_y:base_win_y + total_win_h, base_win_x:base_win_x + win_w] = window_img
        cv2.rectangle(canvas, (base_win_x, base_win_y), (base_win_x + win_w, base_win_y + total_win_h), (56, 189, 248), 1, cv2.LINE_AA)
        
        # Companion LAN Badge
        badge_w, badge_h = 480, 42
        bx1 = (W - badge_w) // 2
        by1 = 940
        cv2.rectangle(canvas, (bx1, by1), (bx1 + badge_w, by1 + badge_h), (30, 41, 59), -1)
        cv2.rectangle(canvas, (bx1, by1), (bx1 + badge_w, by1 + badge_h), (34, 197, 94), 1, cv2.LINE_AA)
        cv2.putText(canvas, "TERHUBUNG LOCAL LAN - HP KASIR", (bx1 + 45, by1 + 27),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, (241, 245, 249), 2, cv2.LINE_AA)
        cv2.circle(canvas, (bx1 + 24, by1 + 21), 6, (34, 197, 94), -1, cv2.LINE_AA)
        
        # Companion Mobile Frame
        mob_h_box = 460
        mob_crop = mob_scaled[0:mob_h_box, :]
        cv2.rectangle(canvas, (mob_x - 3, mob_y + 8), (mob_x + 320 + 3, mob_y + mob_h_box + 12), (0, 0, 0), -1)
        canvas[mob_y:mob_y + mob_h_box, mob_x:mob_x + 320] = mob_crop
        cv2.rectangle(canvas, (mob_x, mob_y), (mob_x + 320, mob_y + mob_h_box), (71, 85, 105), 1, cv2.LINE_AA)

        # Dynamic Zoom Punch-In at t=7.5s (VO: "Tinggal satu kali klik Unduh ke PC...")
        if t < 7.5:
            zoom = 1.0
        elif t < 8.7:
            p = (t - 7.5) / 1.2
            ease = 4 * p * p * p if p < 0.5 else 1 - pow(-2 * p + 2, 3) / 2
            zoom = 1.0 + ease * 0.40
        else:
            zoom = 1.40
            
        if zoom > 1.001:
            crop_w = int(W / zoom)
            crop_h = int(H / zoom)
            x1 = max(0, min(W - crop_w, int(target_focus_x - crop_w / 2)))
            y1 = max(0, min(H - crop_h, int(target_focus_y - crop_h / 2)))
            cropped = canvas[y1:y1 + crop_h, x1:x1 + crop_w]
            out_frame = cv2.resize(cropped, (W, H), interpolation=cv2.INTER_LANCZOS4)
        else:
            out_frame = canvas
            
        writer.write(out_frame)
            
    cap_web.release()
    writer.release()
    print(f"[Workstation V4] Raw MP4 written: {TEMP_MP4.name}")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(TEMP_MP4),
        "-vf", "fps=60",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(OUTPUT_MP4)
    ]
    subprocess.run(cmd, check=True)
    if TEMP_MP4.exists():
        TEMP_MP4.unlink()
    print(f"[Workstation Complete] Saved {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")

if __name__ == "__main__":
    render_workstation()
