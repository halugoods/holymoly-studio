#!/usr/bin/env python3
"""
High-Performance Pre-rendered Vector Mockup Engine for Samsung Galaxy Z Flip 3
Uses pre-baked alpha assets:
1. Seamless scrolling blurred grid background strip
2. Precision Z Flip 3 vector chassis & drop shadow with transparent screen cutout
3. Ultra-fast NumPy/OpenCV compositing (>100 FPS)
"""

import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

class FastZFlip3MockupCompositor:
    def __init__(self, canvas_w=1080, canvas_h=1920, scale=1.0, grid_size=60):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.scale = scale
        self.grid_size = grid_size
        
        # Dimensions
        self.screen_w = int(700 * scale)
        self.screen_h = int(1710 * scale)
        self.bezel = int(15 * scale)
        self.phone_w = self.screen_w + 2 * self.bezel
        self.phone_h = self.screen_h + 2 * self.bezel
        
        self.screen_x = (canvas_w - self.screen_w) // 2
        self.screen_y = (canvas_h - self.screen_h) // 2
        
        self.phone_x = (canvas_w - self.phone_w) // 2
        self.phone_y = (canvas_h - self.phone_h) // 2

        print(f"[MockupEngine] Initializing pre-baked assets: Screen {self.screen_w}x{self.screen_h}, Phone {self.phone_w}x{self.phone_h}...")
        self._bake_background_strip()
        self._bake_phone_overlay()

    def _bake_background_strip(self):
        """Bakes a seamless vertical strip for instantaneous scrolling via slice"""
        strip_h = self.canvas_h + self.grid_size
        bg = Image.new("RGB", (self.canvas_w, strip_h), (14, 16, 22))
        draw = ImageDraw.Draw(bg)

        # Draw grid
        line_color = (42, 50, 65)
        for x in range(0, self.canvas_w + self.grid_size, self.grid_size):
            draw.line([(x, 0), (x, strip_h)], fill=line_color, width=1)
        for y in range(0, strip_h + self.grid_size, self.grid_size):
            draw.line([(0, y), (self.canvas_w, y)], fill=line_color, width=1)

        # Soft depth-of-field blur
        bg = bg.filter(ImageFilter.GaussianBlur(radius=2.2))

        # Center spotlight
        glow = Image.new("RGBA", (self.canvas_w, strip_h), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow)
        g_draw.ellipse(
            [self.canvas_w//2 - 420, strip_h//2 - 620, self.canvas_w//2 + 420, strip_h//2 + 620],
            fill=(38, 48, 64, 45)
        )
        glow = glow.filter(ImageFilter.GaussianBlur(radius=75))
        bg.paste(glow, (0, 0), glow)

        self.bg_strip_bgr = cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR)

    def _bake_phone_overlay(self):
        """
        Bakes:
        1. Full canvas drop shadow (BGR + Alpha)
        2. Phone bezel overlay with transparent screen window (BGR + Alpha)
        3. Screen corner mask for clipping the video frame
        """
        corner_outer = int(46 * self.scale)
        corner_inner = int(32 * self.scale)

        # 1. Screen corner clipping mask
        mask = Image.new("L", (self.screen_w, self.screen_h), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, self.screen_w, self.screen_h], radius=corner_inner, fill=255)
        self.screen_mask = np.array(mask).astype(np.float32) / 255.0 # (H, W) in [0, 1]
        self.screen_mask_3c = np.stack([self.screen_mask]*3, axis=-1)

        # 2. Phone overlay image (1080x1920 RGBA)
        overlay = Image.new("RGBA", (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Drop shadow
        s_mask = Image.new("RGBA", (self.canvas_w, self.canvas_h), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(s_mask)
        s_draw.rounded_rectangle(
            [self.phone_x, self.phone_y, self.phone_x + self.phone_w, self.phone_y + self.phone_h],
            radius=corner_outer,
            fill=(0, 0, 0, 160)
        )
        s_blurred = s_mask.filter(ImageFilter.GaussianBlur(radius=24))
        overlay.paste(s_blurred, (0, 6), s_blurred)

        # Outer chassis (Metallic Armor Aluminum)
        draw.rounded_rectangle(
            [self.phone_x, self.phone_y, self.phone_x + self.phone_w, self.phone_y + self.phone_h],
            radius=corner_outer,
            fill=(36, 40, 46),
            outline=(75, 82, 94),
            width=2
        )

        # Inner bezel (Matte black rubber cushion)
        draw.rounded_rectangle(
            [self.phone_x + 2, self.phone_y + 2, self.phone_x + self.phone_w - 2, self.phone_y + self.phone_h - 2],
            radius=corner_outer - 2,
            fill=(14, 16, 20)
        )

        # Side keys
        # Volume
        draw.rounded_rectangle(
            [self.phone_x + self.phone_w, self.phone_y + 280, self.phone_x + self.phone_w + 3, self.phone_y + 420],
            radius=2, fill=(65, 70, 80)
        )
        # Power
        draw.rounded_rectangle(
            [self.phone_x + self.phone_w, self.phone_y + 460, self.phone_x + self.phone_w + 3, self.phone_y + 560],
            radius=2, fill=(65, 70, 80)
        )

        # Hinge caps
        h_cy = self.phone_y + self.phone_h // 2
        draw.rectangle([self.phone_x - 1, h_cy - 12, self.phone_x + 4, h_cy + 12], fill=(48, 52, 60))
        draw.rectangle([self.phone_x + self.phone_w - 4, h_cy - 12, self.phone_x + self.phone_w + 1, h_cy + 12], fill=(48, 52, 60))

        # Clear screen window to 100% transparent
        screen_cutout = Image.new("RGBA", (self.screen_w, self.screen_h), (0, 0, 0, 0))
        overlay.paste(screen_cutout, (self.screen_x, self.screen_y), mask)

        # Camera punch-hole (Infinity-O)
        cam_cx = self.screen_x + self.screen_w // 2
        cam_cy = self.screen_y + 26
        draw.ellipse([cam_cx - 9, cam_cy - 9, cam_cx + 9, cam_cy + 9], fill=(10, 10, 12))
        draw.ellipse([cam_cx - 4, cam_cy - 4, cam_cx + 4, cam_cy + 4], fill=(22, 32, 48))
        draw.ellipse([cam_cx - 2, cam_cy - 2, cam_cx, cam_cy], fill=(65, 85, 120))

        # Speaker slit in top bezel
        spk_x = self.phone_x + (self.phone_w - 48) // 2
        spk_y = self.phone_y + 6
        draw.rounded_rectangle([spk_x, spk_y, spk_x + 48, spk_y + 3], radius=1, fill=(24, 26, 30))

        overlay_np = np.array(overlay)
        # Split BGR and Alpha
        self.overlay_bgr = cv2.cvtColor(overlay_np, cv2.COLOR_RGBA2BGR)
        self.overlay_alpha = (overlay_np[:, :, 3].astype(np.float32) / 255.0)[:, :, np.newaxis]
        self.overlay_inv_alpha = 1.0 - self.overlay_alpha

    def render_frame(self, raw_frame, frame_idx):
        """
        Ultra-fast single frame compositor in pure NumPy / OpenCV
        """
        # 1. Background fast slice
        y_off = int((frame_idx * 1.8) % self.grid_size)
        bg = self.bg_strip_bgr[y_off:y_off + self.canvas_h, 0:self.canvas_w].copy()

        # 2. Resize raw screen recording frame to fit inside inner screen window
        resized_screen = cv2.resize(raw_frame, (self.screen_w, self.screen_h), interpolation=cv2.INTER_AREA)

        # 3. Apply rounded corners to screen and place onto background
        bg_screen_roi = bg[self.screen_y:self.screen_y + self.screen_h, self.screen_x:self.screen_x + self.screen_w]
        blended_screen = (resized_screen * self.screen_mask_3c + bg_screen_roi * (1.0 - self.screen_mask_3c)).astype(np.uint8)
        bg[self.screen_y:self.screen_y + self.screen_h, self.screen_x:self.screen_x + self.screen_w] = blended_screen

        # 4. Composite phone chassis, bezel, camera punch hole, and drop shadow over the canvas
        out = (self.overlay_bgr * self.overlay_alpha + bg * self.overlay_inv_alpha).astype(np.uint8)
        return out

def benchmark():
    compositor = FastZFlip3MockupCompositor()
    dummy_frame = np.zeros((2640, 1080, 3), dtype=np.uint8)
    # Fill with some colors
    dummy_frame[200:800, :] = (200, 120, 50)
    dummy_frame[800:1500, :] = (40, 180, 220)

    # Warm up
    compositor.render_frame(dummy_frame, 0)

    # Benchmark 100 frames
    t0 = time.perf_counter()
    N = 100
    for i in range(N):
        compositor.render_frame(dummy_frame, i)
    t1 = time.perf_counter()
    fps = N / (t1 - t0)
    print(f"[Benchmark] Rendered {N} frames in {t1 - t0:.3f}s -> {fps:.1f} FPS!")

    # Save 1 test frame
    res = compositor.render_frame(dummy_frame, 45)
    cv2.imwrite("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fast_mockup_test.png", res)
    print("Saved fast_mockup_test.png")

if __name__ == "__main__":
    benchmark()
