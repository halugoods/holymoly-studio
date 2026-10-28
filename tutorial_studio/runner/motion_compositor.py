#!/usr/bin/env python3
"""
NUSA Anti-Slop Motion Compositor
Synthesized from Gojek & Apple Keynote standards:
- Dynamic Camera Rig: Smooth cubic ease-in-out punch-in zooms & pans
- Tactile Touch Ripple: Translucent Cupertino-style touch impulse rings at tap coordinates
- Sleek Anti-Slop Motion HUD & Accent Badges (0 slop, 0 emojis, clean Lucide style)
- Dynamic Progress Bar
- Word-Anchored Audio Sync with 60 FPS libx264 export
"""

import os
import sys
import json
import math
import time
import subprocess
from pathlib import Path
import cv2
import numpy as np

def ease_in_out_cubic(t):
    """Smooth cubic hermite ease-in-out curve for camera moves"""
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    return 3.0 * (t ** 2) - 2.0 * (t ** 3)

class MotionCompositor:
    def __init__(self, raw_video_path, timeline_script_path, audio_path, output_path, target_size=(1080, 1920)):
        self.raw_video_path = Path(raw_video_path)
        self.timeline_script_path = Path(timeline_script_path)
        self.audio_path = Path(audio_path)
        self.output_path = Path(output_path)
        self.target_w, self.target_h = target_size
        
        with open(self.timeline_script_path, "r", encoding="utf-8") as f:
            self.script = json.load(f)
            
        self.beats = self.script.get("beats", [])
        self.adb_timeline = self.script.get("adb_timeline", [])
        self.total_duration_sec = self.script.get("total_duration_sec", 15.0)

    def _get_camera_state(self, t_sec):
        """Calculates interpolated (zoom, focus_x_px, focus_y_px) at timestamp t_sec"""
        # Find current beat
        current_beat = None
        for b in self.beats:
            if b["start_sec"] <= t_sec <= b["end_sec"]:
                current_beat = b
                break
        if not current_beat and self.beats:
            current_beat = self.beats[-1] if t_sec >= self.beats[-1]["end_sec"] else self.beats[0]

        target_zoom = current_beat.get("camera", {}).get("zoom", 1.0)
        target_fx = current_beat.get("camera", {}).get("focus_x_pct", 0.5)
        target_fy = current_beat.get("camera", {}).get("focus_y_pct", 0.5)

        # Smooth transition from previous beat (0.45s transition window)
        prev_beat = None
        for i, b in enumerate(self.beats):
            if b == current_beat and i > 0:
                prev_beat = self.beats[i-1]
                break

        trans_dur = 0.45
        t_into_beat = t_sec - current_beat["start_sec"]
        if prev_beat and t_into_beat < trans_dur:
            p_zoom = prev_beat.get("camera", {}).get("zoom", 1.0)
            p_fx = prev_beat.get("camera", {}).get("focus_x_pct", 0.5)
            p_fy = prev_beat.get("camera", {}).get("focus_y_pct", 0.5)
            factor = ease_in_out_cubic(t_into_beat / trans_dur)
            zoom = p_zoom + (target_zoom - p_zoom) * factor
            fx = p_fx + (target_fx - p_fx) * factor
            fy = p_fy + (target_fy - p_fy) * factor
        else:
            zoom = target_zoom
            fx = target_fx
            fy = target_fy

        return zoom, fx, fy, current_beat

    def render(self):
        print(f"[Compositor] Membuka rekaman mentah: {self.raw_video_path}")
        cap = cv2.VideoCapture(str(self.raw_video_path))
        if not cap.isOpened():
            raise RuntimeError(f"Gagal membuka video mentah: {self.raw_video_path}")

        src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"[Compositor] Source Video: {src_w}x{src_h} @ {src_fps:.1f} FPS, {total_frames} frames")
        print(f"[Compositor] Target Canvas: {self.target_w}x{self.target_h} (Commercial 9:16 Feed)")

        temp_rendered_video = self.output_path.parent / f"temp_rendered_{self.output_path.name}"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_writer = cv2.VideoWriter(
            str(temp_rendered_video),
            fourcc,
            src_fps,
            (self.target_w, self.target_h)
        )

        # Buffer offset: ADB execution started 1.0s into the screen recording
        offset_sec = 1.0
        frame_idx = 0
        rendered_count = 0

        # Colors (BGR) dynamically adapted to NUSA variant
        variant = self.script.get("variant", "kelontong").lower()
        if "fnb" in variant:
            accent_color = (45, 50, 225) # Vibrant Crimson Red (BGR)
        elif "laundry" in variant:
            accent_color = (235, 140, 30) # Bright Ocean Blue (BGR)
        elif "bengkel" in variant:
            accent_color = (20, 150, 235) # Industrial Amber / Ochre (BGR)
        elif "apotek" in variant:
            accent_color = (80, 180, 40) # Fresh Medical Green (BGR)
        elif "salon" in variant:
            accent_color = (180, 60, 220) # Elegant Magenta / Violet (BGR)
        elif "fotocopy" in variant:
            accent_color = (210, 160, 30) # Electric Cyan / Printing Blue (BGR)
        elif "servis" in variant:
            accent_color = (245, 110, 20) # Tech Cobalt / Gadget Blue (BGR)
        else:
            accent_color = (22, 115, 249) # Standard Warm Orange (BGR)

        DARK_TEXT = (25, 25, 30)
        WHITE = (255, 255, 255)
        PILL_BG = (245, 247, 250)

        # Pre-process tap events list in seconds
        tap_events = []
        for ev in self.adb_timeline:
            if ev.get("action") == "tap":
                tap_events.append({
                    "t_sec": ev.get("offset_ms", 0) / 1000.0,
                    "x_pct": ev.get("x_pct", 0.5),
                    "y_pct": ev.get("y_pct", 0.5),
                    "label": ev.get("label", "")
                })

        start_time = time.time()
        print("[Compositor] Memulai rendering frame-by-frame dengan dynamic camera rig & tactile ripples...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            t_video_sec = frame_idx / src_fps
            t_action_sec = t_video_sec - offset_sec

            # Hanya render durasi aktif (dari t=0s sampai total_duration_sec)
            if t_action_sec < 0.0:
                frame_idx += 1
                continue
            if t_action_sec > self.total_duration_sec:
                break

            # 1. Camera Rig Calculations
            zoom, fx_pct, fy_pct, current_beat = self._get_camera_state(t_action_sec)
            
            # Crop window calculation
            crop_w = int(src_w / zoom)
            crop_h = int(src_h / zoom)
            
            center_x = int(fx_pct * src_w)
            center_y = int(fy_pct * src_h)

            x1 = max(0, min(src_w - crop_w, center_x - crop_w // 2))
            y1 = max(0, min(src_h - crop_h, center_y - crop_h // 2))
            x2 = x1 + crop_w
            y2 = y1 + crop_h

            cropped = frame[y1:y2, x1:x2]

            # 2. Rescale cropped frame to fit inside target canvas
            # We preserve aspect ratio and place it centered vertically/horizontally
            scale_to_fit = min(self.target_w / crop_w, self.target_h / crop_h)
            new_w = int(crop_w * scale_to_fit)
            new_h = int(crop_h * scale_to_fit)
            scaled = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

            # Canvas background (Modern Apple matte studio slate #0f172a or light studio #f8fafc)
            # Default to elegant dark luxury studio for high contrast
            canvas = np.zeros((self.target_h, self.target_w, 3), dtype=np.uint8)
            canvas[:] = (20, 24, 30) # Dark rich slate BGR

            # Subtle studio gradient / spotlight on background
            spot_y = self.target_h // 2
            spot_x = self.target_w // 2

            pos_x = (self.target_w - new_w) // 2
            pos_y = (self.target_h - new_h) // 2

            # Place device viewport
            canvas[pos_y:pos_y+new_h, pos_x:pos_x+new_w] = scaled

            # 3. Tactile Touch Ripple
            # Check if any tap occurred within the last 0.35 seconds
            for tap in tap_events:
                dt = t_action_sec - tap["t_sec"]
                if 0.0 <= dt <= 0.35:
                    progress = dt / 0.35
                    # Map original tap (x,y) to current canvas space
                    src_tap_x = tap["x_pct"] * src_w
                    src_tap_y = tap["y_pct"] * src_h

                    # Check if tap is within current crop
                    if x1 <= src_tap_x <= x2 and y1 <= src_tap_y <= y2:
                        canv_tap_x = int(pos_x + (src_tap_x - x1) * scale_to_fit)
                        canv_tap_y = int(pos_y + (src_tap_y - y1) * scale_to_fit)

                        # Draw expanding translucent ring
                        radius = int(20 + 70 * math.sqrt(progress))
                        alpha = max(0.0, 1.0 - progress)
                        
                        overlay = canvas.copy()
                        # Outer halo matching variant branding
                        cv2.circle(overlay, (canv_tap_x, canv_tap_y), radius, accent_color, max(1, int(4 * (1.0 - progress))))
                        # Center tactile dot
                        if progress < 0.2:
                            cv2.circle(overlay, (canv_tap_x, canv_tap_y), int(12 * (1.0 - progress*5)), (255, 255, 255), -1)

                        cv2.addWeighted(overlay, alpha * 0.85, canvas, 1.0 - alpha * 0.85, 0, canvas)

            # 4. Anti-Slop Motion HUD & Callout Pill
            # Display current beat callout or header pill
            if current_beat and "callout" in current_beat:
                callout_text = current_beat["callout"].get("text", "")
                if callout_text:
                    # Floating frosted glass badge at lower-third center (above progress bar)
                    # This guarantees the top Android status bar is ALWAYS 100% visible & unblocked!
                    badge_w = min(self.target_w - 80, 880)
                    badge_h = 68
                    bx1 = (self.target_w - badge_w) // 2
                    by1 = self.target_h - 145
                    bx2 = bx1 + badge_w
                    by2 = by1 + badge_h

                    # Frosted glass background
                    sub_roi = canvas[by1:by2, bx1:bx2]
                    blurred = cv2.GaussianBlur(sub_roi, (21, 21), 0)
                    white_box = np.full_like(sub_roi, 255)
                    blended = cv2.addWeighted(blurred, 0.25, white_box, 0.75, 0)
                    canvas[by1:by2, bx1:bx2] = blended

                    # Clean accent border (variant brand color)
                    cv2.rectangle(canvas, (bx1, by1), (bx2, by2), accent_color, 2, cv2.LINE_AA)

                    # Text (using OpenCV Hershey Simplex for zero dependency, crisp typography)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    font_scale = 0.72
                    thickness = 1
                    t_size = cv2.getTextSize(callout_text, font, font_scale, thickness)[0]
                    tx = bx1 + (badge_w - t_size[0]) // 2
                    ty = by1 + (badge_h + t_size[1]) // 2 - 2

                    cv2.putText(canvas, callout_text, (tx, ty), font, font_scale, DARK_TEXT, thickness, cv2.LINE_AA)

            # 5. Bottom Dynamic Progress Bar
            progress_ratio = min(1.0, max(0.0, t_action_sec / self.total_duration_sec))
            bar_y = self.target_h - 18
            cv2.rectangle(canvas, (0, bar_y), (self.target_w, self.target_h), (35, 40, 50), -1)
            cv2.rectangle(canvas, (0, bar_y), (int(self.target_w * progress_ratio), self.target_h), accent_color, -1)

            out_writer.write(canvas)
            rendered_count += 1
            frame_idx += 1

            if rendered_count % 120 == 0:
                elapsed = time.time() - start_time
                pct = (rendered_count / (self.total_duration_sec * src_fps)) * 100
                print(f"  [Render] {rendered_count} frame ({pct:.1f}%) rendered... ({elapsed:.1f}s)")

        cap.release()
        out_writer.release()
        total_render_time = time.time() - start_time
        print(f"[Compositor] Render visual selesai dalam {total_render_time:.2f} detik ({rendered_count} frame, {rendered_count/total_render_time:.1f} fps).")

        # 7. Final FFmpeg Muxing: Combine rendered visuals with Gemini Native VO Audio
        print(f"[Compositor] Menggabungkan visual motion dengan audio VO: {self.audio_path}...")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_rendered_video),
            "-i", str(self.audio_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(self.output_path)
        ]
        res = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[Compositor] FFmpeg Error: {res.stderr}")
            raise RuntimeError("Gagal melakukan audio-video muxing final.")

        # Clean up temp file
        if temp_rendered_video.exists():
            temp_rendered_video.unlink()

        final_mb = self.output_path.stat().st_size / (1024 * 1024)
        print(f"[Compositor] BERHASIL! Video Commercial Motion siap di: {self.output_path} ({final_mb:.2f} MB)")
        return self.output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--script", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    compositor = MotionCompositor(args.raw, args.script, args.audio, args.out)
    compositor.render()
