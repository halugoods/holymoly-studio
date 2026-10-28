#!/usr/bin/env python3
"""
Render Seamless Beat 2 & Beat 3 (V7 Master)
- Continuous scrolling grid background.
- Beat 2 (t = 0.0s to 12.5s): Centered full-size Z Flip 3 mockup (scale 1.0, cy 960).
  * Tactile touch tap ripples at:
    - t = 5.60s (Portal File at x=540, y=2110)
    - t = 8.80s (Buka di PC at x=907, y=496)
- Transition (t = 12.5s to 14.2s):
  * Phone smoothly shrinks: scale 1.0 -> 0.42, cy 960 -> 1450 (full frame intact).
  * Web Chrome window zooms out dramatically from macro close-up (scale 3.20 -> 1.0, cy -320 -> 403).
  * Symmetrical LAN Glass Badge fades in at exact midpoint cy = 872 (152px top, 152px bottom).
- Beat 3 (t = 14.2s to 31.0s):
  * Wide dual view (t = 14.2s to 20.0s).
  * Smart Camera Punch-in Zoom (t = 20.0s to 26.8s):
    - Cam zoom 1.0 -> 1.45x focused on 'Unduh ke PC' button at (cam_focus_x=280, cam_focus_y=450).
    - Phone mockup scales up proportionally (0.42 -> 0.609x) tracking camera motion down.
    - Animated mouse cursor glides into button (t = 20.5s to 21.3s).
    - Mouse cursor clicks button at t = 21.4s with bounce scale and expanding emerald click ripple!
    - Desktop screen responds at t = 21.4s with download progress and success toast notification.
    - Cam zoom pulls back 1.45x -> 1.0x (t = 25.5s to 26.8s).
  * Wide dual view restored (t = 26.8s to 31.0s).
"""

import os
import sys
import time
import subprocess
import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
V4_DIR = OUT_DIR / "fresh_v4"

GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"
BEAT2_RAW = V4_DIR / "mobile_beat2_15.0s.mp4"
DESKTOP_RAW = V4_DIR / "real_desktop_beat3_17.3s.mp4"

OUTPUT_MP4 = V4_DIR / "beat2_3_seamless_31s.mp4"
TEMP_RAW_MP4 = V4_DIR / "temp_beat2_3_raw.mp4"

FPS = 60
DUR = 31.000
TOTAL_FRAMES = int(FPS * DUR) # 1860 frames
W, H = 1080, 1920

# Load mask & frame
mask_rgba = cv2.imread(str(MASK_PNG), cv2.IMREAD_UNCHANGED)
frame_rgba = cv2.imread(str(FRAME_PNG), cv2.IMREAD_UNCHANGED)
f_alpha = (frame_rgba[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
f_bgr = frame_rgba[:, :, :3]

def draw_touch_ripple(frame_bgr, cx, cy, progress, max_radius=80, color=(56, 189, 248)):
    """Draw anti-aliased tactile touch ripple on a BGR image."""
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

def create_cursor_rgba(size=36):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    pts = [(0, 0), (0, int(size * 0.72)), (int(size * 0.17), int(size * 0.58)),
           (int(size * 0.33), int(size * 0.92)), (int(size * 0.47), int(size * 0.86)),
           (int(size * 0.31), int(size * 0.53)), (int(size * 0.53), int(size * 0.53))]
    draw.polygon(pts, fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=2)
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)

cursor_base_rgba = create_cursor_rgba(size=38)

def render_glass_badge(w=500, h=46, pulse_phase=0.0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    r = h // 2
    # Outer capsule with soft emerald-cyan double border
    draw.rounded_rectangle([2, 2, w-3, h-3], radius=r, fill=(11, 23, 48, 240), outline=(16, 185, 129, 255), width=2)
    draw.rounded_rectangle([4, 4, w-5, h-5], radius=r-2, outline=(56, 189, 248, 70), width=1)
    # Glass shine top
    draw.rounded_rectangle([14, 4, w-15, 13], radius=4, fill=(255, 255, 255, 35))
    
    # Glowing pulsing LED
    led_cx, led_cy = 30, h // 2
    ripple_r = 9 + int(5 * np.sin(pulse_phase))
    ripple_alpha = int(140 - 80 * np.sin(pulse_phase))
    draw.ellipse([led_cx - ripple_r, led_cy - ripple_r, led_cx + ripple_r, led_cy + ripple_r],
                 outline=(16, 185, 129, max(20, ripple_alpha)), width=1)
    draw.ellipse([led_cx - 5, led_cy - 5, led_cx + 5, led_cy + 5], fill=(34, 197, 94, 255))
    draw.ellipse([led_cx - 2, led_cy - 2, led_cx + 2, led_cy + 2], fill=(255, 255, 255, 240))
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 17)
    except:
        font = ImageFont.load_default()
        
    draw.text((52, led_cy - 9), "TERHUBUNG LOCAL LAN • HP KASIR", fill=(255, 255, 255, 255), font=font)
    
    # Mini wifi symbol on the right
    wx, wy = w - 36, led_cy
    draw.arc([wx - 10, wy - 8, wx + 10, wy + 8], 200, 340, fill=(16, 185, 129, 255), width=2)
    draw.arc([wx - 6, wy - 4, wx + 6, wy + 4], 200, 340, fill=(16, 185, 129, 255), width=2)
    draw.ellipse([wx - 2, wy + 3, wx + 2, wy + 7], fill=(16, 185, 129, 255))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)

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

def build_web_window_rgba(desktop_bgr, win_w=980, head_h=36):
    web_h = int(win_w * 720 / 1280)
    web_resized = cv2.resize(desktop_bgr, (win_w, web_h), interpolation=cv2.INTER_LANCZOS4)
    header = create_window_header(win_w, head_h)
    stacked = np.vstack([header, web_resized])
    
    total_h = head_h + web_h
    win_rgba = np.zeros((total_h + 4, win_w + 4, 4), dtype=np.uint8)
    win_rgba[2:total_h+2, 2:win_w+2, :3] = stacked
    win_rgba[2:total_h+2, 2:win_w+2, 3] = 255
    cv2.rectangle(win_rgba, (1, 1), (win_w + 2, total_h + 2), (56, 189, 248, 255), 2, cv2.LINE_AA)
    return win_rgba

def overlay_fast(canvas_bgr, overlay_rgba, cx, cy, scale):
    if scale <= 0: return
    orig_h, orig_w = overlay_rgba.shape[:2]
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    if new_w <= 0 or new_h <= 0: return
    
    resized = cv2.resize(overlay_rgba, (new_w, new_h),
                         interpolation=cv2.INTER_AREA if scale < 0.9 else cv2.INTER_LANCZOS4)
    
    x1 = cx - new_w // 2
    y1 = cy - new_h // 2
    x2 = x1 + new_w
    y2 = y1 + new_h
    
    cx1, cy1 = max(0, x1), max(0, y1)
    cx2, cy2 = min(W, x2), min(H, y2)
    
    if cx1 >= cx2 or cy1 >= cy2: return
    
    ox1, oy1 = cx1 - x1, cy1 - y1
    ox2, oy2 = ox1 + (cx2 - cx1), oy1 + (cy2 - cy1)
    
    part_over = resized[oy1:oy2, ox1:ox2]
    alpha = (part_over[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
    
    canvas_bgr[cy1:cy2, cx1:cx2] = (
        part_over[:, :, :3] * alpha + canvas_bgr[cy1:cy2, cx1:cx2] * (1.0 - alpha)
    ).astype(np.uint8)

def render():
    print(f"[Seamless Engine V7] Rendering {TOTAL_FRAMES} frames ({DUR}s @ {FPS}fps)...")
    
    cap_grid = cv2.VideoCapture(str(GRID_MP4))
    cap_mob = cv2.VideoCapture(str(BEAT2_RAW))
    mob_total = int(cap_mob.get(cv2.CAP_PROP_FRAME_COUNT))
    cap_desk = cv2.VideoCapture(str(DESKTOP_RAW))
    desk_total = int(cap_desk.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(TEMP_RAW_MP4), fourcc, FPS, (W, H))
    
    # Pre-cache last mobile frame for hold
    cap_mob.set(cv2.CAP_PROP_POS_FRAMES, min(750, mob_total - 1))
    _, last_mob_frame = cap_mob.read()
    last_phone_rgba = build_phone_mockup_rgba(last_mob_frame)
    cap_mob.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    t_trans_start = 12.50
    t_trans_end = 14.20
    trans_duration = t_trans_end - t_trans_start
    
    # Smart Camera punch-in zoom parameters focusing on 'Unduh ke PC' button
    t_zoom_in_start = 20.00
    t_zoom_in_end = 21.20
    t_zoom_out_start = 25.50
    t_zoom_out_end = 26.80
    cam_focus_x = 280
    cam_focus_y = 450
    max_cam_zoom = 1.45
    
    t0 = time.time()
    current_phone_rgba = last_phone_rgba
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        
        # 1. Background grid loop
        ret_g, grid_frame = cap_grid.read()
        if not ret_g:
            cap_grid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_g, grid_frame = cap_grid.read()
        canvas = grid_frame.copy()
        
        # 2. Mobile screen source with touch tap ripples in Beat 2
        if t < 12.50:
            ret_m, mob_frame = cap_mob.read()
            if ret_m:
                mob_copy = mob_frame.copy()
                # Touch Tap Ripple 1: Tap 'Portal File' at (540, 2110) from t = 5.50s to 5.95s
                if 5.50 <= t <= 5.95:
                    p_rip1 = (t - 5.50) / 0.45
                    draw_touch_ripple(mob_copy, 540, 2110, p_rip1, max_radius=85, color=(56, 189, 248))
                # Touch Tap Ripple 2: Tap 'Buka di PC' at (907, 496) from t = 8.65s to 9.10s
                elif 8.65 <= t <= 9.10:
                    p_rip2 = (t - 8.65) / 0.45
                    draw_touch_ripple(mob_copy, 907, 496, p_rip2, max_radius=80, color=(56, 189, 248))
                current_phone_rgba = build_phone_mockup_rgba(mob_copy)
        else:
            current_phone_rgba = last_phone_rgba
            
        # 3. Base layout calculation
        if t < t_trans_start:
            # Beat 2 Full Centered Mockup
            base_phone_scale = 1.0
            base_phone_cx = 540
            base_phone_cy = 960
            web_visible = False
            badge_alpha = 0.0
            base_web_scale = 1.0
            base_web_cx = 540
            base_web_cy = 403
        elif t < t_trans_end:
            # Transition Phase: Phone shrinks down, Web zooms out from 3.20x macro close-up!
            p = (t - t_trans_start) / trans_duration
            p_smooth = p * p * (3.0 - 2.0 * p)
            
            # Phone shrinks and moves down
            base_phone_scale = 1.0 - (1.0 - 0.42) * p_smooth
            base_phone_cx = 540
            base_phone_cy = int(960 + (1450 - 960) * p_smooth)
            
            # Web starts at 3.20x macro zoom-in and smoothly zooms out to 1.0x!
            base_web_scale = 3.20 - (3.20 - 1.0) * p_smooth
            base_web_cx = 540
            base_web_cy = int(-320 + (403 - (-320)) * p_smooth)
            web_visible = True
            badge_alpha = max(0.0, (p - 0.4) / 0.6)
        else:
            # Beat 3 Settled Base Layout
            base_phone_scale = 0.42
            base_phone_cx = 540
            base_phone_cy = 1450
            
            base_web_scale = 1.0
            base_web_cx = 540
            base_web_cy = 403
            web_visible = True
            badge_alpha = 1.0
            
        # 4. Calculate Camera Punch-in Zoom factor during Beat 3 download action
        if t < t_zoom_in_start:
            cam_zoom = 1.0
        elif t < t_zoom_in_end:
            pz = (t - t_zoom_in_start) / (t_zoom_in_end - t_zoom_in_start)
            pz_smooth = pz * pz * (3.0 - 2.0 * pz)
            cam_zoom = 1.0 + (max_cam_zoom - 1.0) * pz_smooth
        elif t < t_zoom_out_start:
            cam_zoom = max_cam_zoom
        elif t < t_zoom_out_end:
            pz = (t - t_zoom_out_start) / (t_zoom_out_end - t_zoom_out_start)
            pz_smooth = pz * pz * (3.0 - 2.0 * pz)
            cam_zoom = max_cam_zoom - (max_cam_zoom - 1.0) * pz_smooth
        else:
            cam_zoom = 1.0
            
        # Apply smart camera zoom to Web Window
        final_web_scale = base_web_scale * cam_zoom
        final_web_cx = int(cam_focus_x + (base_web_cx - cam_focus_x) * cam_zoom)
        final_web_cy = int(cam_focus_y + (base_web_cy - cam_focus_y) * cam_zoom)
        
        # Apply camera zoom to Phone Mockup (User rule: 'jgn lupa logika yg hp jg ikut zoom ya')
        final_phone_scale = base_phone_scale * cam_zoom
        final_phone_cx = int(cam_focus_x + (base_phone_cx - cam_focus_x) * cam_zoom)
        final_phone_cy = int(cam_focus_y + (base_phone_cy - cam_focus_y) * cam_zoom)
        
        # Apply camera zoom to Badge (exact midpoint cy = 872)
        final_badge_scale = 1.0 * cam_zoom
        final_badge_cx = int(cam_focus_x + (540 - cam_focus_x) * cam_zoom)
        final_badge_cy = int(cam_focus_y + (872 - cam_focus_y) * cam_zoom)
        
        # 5. Draw Web Window with synchronized action playback
        if web_visible:
            # Paced desktop playback:
            # - t < 21.40s: Desktop shows queue before click (progress 0.0s to 4.90s)
            # - t >= 21.40s: Desktop triggers click at 5.00s and plays continuous download + toast
            if t < 21.40:
                dt = (t - 12.50) / (21.40 - 12.50) * 4.90
            else:
                dt = 5.00 + (t - 21.40)
            desk_frame_idx = min(desk_total - 1, int(dt * FPS))
            cap_desk.set(cv2.CAP_PROP_POS_FRAMES, desk_frame_idx)
            ret_d, desk_frame = cap_desk.read()
            if not ret_d:
                cap_desk.set(cv2.CAP_PROP_POS_FRAMES, desk_total - 1)
                ret_d, desk_frame = cap_desk.read()
            web_rgba = build_web_window_rgba(desk_frame)
            overlay_fast(canvas, web_rgba, cx=final_web_cx, cy=final_web_cy, scale=final_web_scale)
            
        # 6. Draw LAN Connection Badge & Energy Beam (Midpoint 872, 152px margins)
        if badge_alpha > 0.01:
            pulse_phase = t * 6.0
            badge_rgba = render_glass_badge(w=500, h=46, pulse_phase=pulse_phase)
            
            # Symmetrical luminous beam lines between Web, Badge, and Phone
            beam_top_start = int(final_web_cy + (587 * final_web_scale) / 2) + 8
            beam_top_end = int(final_badge_cy - (46 * final_badge_scale) / 2) - 8
            
            beam_bot_start = int(final_badge_cy + (46 * final_badge_scale) / 2) + 8
            beam_bot_end = int(final_phone_cy - (1920 * final_phone_scale) / 2) - 8
            
            badge_cx = final_badge_cx
            if beam_top_end > beam_top_start + 10:
                cv2.line(canvas, (badge_cx, beam_top_start), (badge_cx, beam_top_end), (16, 185, 129), 2, cv2.LINE_AA)
                # Traveling packet 1
                travel1 = int((t * 280) % max(1, (beam_top_end - beam_top_start)))
                py1 = beam_top_end - travel1
                cv2.circle(canvas, (badge_cx, py1), 3, (34, 255, 120), -1, cv2.LINE_AA)
                cv2.circle(canvas, (badge_cx, py1), 7, (16, 185, 129), 1, cv2.LINE_AA)
                
            if beam_bot_end > beam_bot_start + 10:
                cv2.line(canvas, (badge_cx, beam_bot_start), (badge_cx, beam_bot_end), (16, 185, 129), 2, cv2.LINE_AA)
                # Traveling packet 2
                travel2 = int((t * 280 + 100) % max(1, (beam_bot_end - beam_bot_start)))
                py2 = beam_bot_end - travel2
                cv2.circle(canvas, (badge_cx, py2), 3, (34, 255, 120), -1, cv2.LINE_AA)
                cv2.circle(canvas, (badge_cx, py2), 7, (16, 185, 129), 1, cv2.LINE_AA)
            
            # Overlay glass badge with alpha fade-in
            overlay_fast(canvas, badge_rgba, cx=final_badge_cx, cy=final_badge_cy, scale=final_badge_scale * badge_alpha)
            
        # 7. Draw Phone Mockup
        overlay_fast(canvas, current_phone_rgba, cx=final_phone_cx, cy=final_phone_cy, scale=final_phone_scale)
        
        # 8. Animated Mouse Cursor & Button Click on PC during Beat 3 Smart Zoom
        # Target button center under current cam_zoom
        btn_curr_x = int(cam_focus_x + (192 - cam_focus_x) * cam_zoom)
        btn_curr_y = int(cam_focus_y + (460 - cam_focus_y) * cam_zoom)
        
        if 20.40 <= t <= 24.80:
            if t < 21.30:
                # Gliding smoothly to button
                p_cur = (t - 20.40) / 0.90
                p_cur_smooth = p_cur * p_cur * (3.0 - 2.0 * p_cur)
                cur_x = int(380 + (btn_curr_x - 380) * p_cur_smooth)
                cur_y = int(600 + (btn_curr_y - 600) * p_cur_smooth)
                cur_scale = 1.0
            elif t <= 21.80:
                # Clicking button with bounce & expanding emerald shockwave
                p_click = (t - 21.30) / 0.50
                cur_x = btn_curr_x
                cur_y = btn_curr_y
                cur_scale = 1.0 - 0.18 * np.sin(p_click * np.pi)
                draw_touch_ripple(canvas, btn_curr_x, btn_curr_y, p_click, max_radius=48, color=(34, 197, 94))
            else:
                # Hovering gently near button
                cur_x = btn_curr_x + 10
                cur_y = btn_curr_y + 12
                cur_scale = 1.0
                
            # Draw cursor (hotspot offset +8, +10)
            overlay_fast(canvas, cursor_base_rgba, cx=cur_x + 10, cy=cur_y + 12, scale=cur_scale)
        
        writer.write(canvas)
        
        if frame_idx % 150 == 0:
            elapsed = time.time() - t0
            fps_proc = (frame_idx + 1) / max(0.1, elapsed)
            print(f"  Frame {frame_idx}/{TOTAL_FRAMES} ({t:.2f}s) - {fps_proc:.1f} fps")
            
    cap_grid.release()
    cap_mob.release()
    cap_desk.release()
    writer.release()
    
    print(f"[Seamless Engine] Finished raw render. Re-encoding with libx264...")
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
        
    print(f"[Seamless Success] Saved {OUTPUT_MP4.name} ({OUTPUT_MP4.stat().st_size} bytes)")

if __name__ == "__main__":
    render()
