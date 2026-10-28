#!/usr/bin/env python3
"""
Holymoly Studio - GAGE SuperApp 15s Master Video Producer
(by Halu Goods Indonesia)

Combines:
1. Headless Flutter UI captures (gage_real_home_screen.png & gage_service_grid_perfect.png)
2. Smart Chroma Key 3D Courier Scooter (scene-01_clean_alpha.png)
3. Neural Indonesian Voiceover (id-ID-ArdiNeural)
4. Smooth Apple/Gojek-grade kinetic motion composited via FFmpeg
"""

import math
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from holymoly_studio.engine.tts import synthesize

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output")
TEMP_DIR = OUT_DIR / "temp_frames"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_PATH = OUT_DIR / "gage_narration.mp3"
FINAL_VIDEO_PATH = OUT_DIR / "gage_promo_15s.mp4"

# 1. Synthesize Narration
narration = (
    "Mau kulineran, belanja sembako, atau kirim paket di Pracimantoro? "
    "Sekarang serba praktis lewat GAGE. "
    "Sekali klik, driver langsung meluncur!"
)
print("[Holymoly Studio] Synthesizing Indonesian Voiceover...")
synthesize(text=narration, output_path=AUDIO_PATH, voice="id-ID-ArdiNeural", rate="+3%")

# Measure audio duration
def get_duration(audio_file: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

audio_duration = get_duration(AUDIO_PATH)
total_duration = max(audio_duration + 1.5, 12.0)
print(f"[Holymoly Studio] Audio duration: {audio_duration:.2f}s | Target video duration: {total_duration:.2f}s")

# Assets
BRAIN_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")
ASSETS_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/assets")

home_img_path = BRAIN_DIR / "gage_real_home_screen.png"
grid_img_path = BRAIN_DIR / "gage_service_grid_perfect.png"
scooter_img_path = BRAIN_DIR / "scene-01_clean_alpha.png"

img_home = Image.open(home_img_path).convert("RGBA")
img_grid = Image.open(grid_img_path).convert("RGBA")
img_scooter = Image.open(scooter_img_path).convert("RGBA")

# Video Specs
WIDTH, HEIGHT = 1080, 1920
FPS = 30
TOTAL_FRAMES = int(total_duration * FPS)

FONT_PATH = ASSETS_DIR / "fonts/Inter.ttf"
if not FONT_PATH.exists():
    FONT_PATH = "arial.ttf"

def get_font(size: int):
    try:
        return ImageFont.truetype(str(FONT_PATH), size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font(52)
font_subtitle = get_font(34)
font_badge = get_font(26)
font_cta = get_font(42)

print(f"[Holymoly Studio] Rendering {TOTAL_FRAMES} high-res video frames (1080x1920 @ {FPS}fps)...")

# Scene boundaries (frames)
scene1_end = int(4.0 * FPS)
scene2_end = int(8.2 * FPS)
scene3_end = TOTAL_FRAMES

# Base background: Clean Apple iOS Inset style (soft off-white #F8FAFC)
def draw_gradient_background(draw, width, height):
    # Smooth vertical subtle gradient
    top_color = (248, 250, 252) # #F8FAFC
    bot_color = (237, 242, 247) # #EDF2F7
    for y in range(0, height, 4):
        t = y / height
        r = int(top_color[0] * (1 - t) + bot_color[0] * t)
        g = int(top_color[1] * (1 - t) + bot_color[1] * t)
        b = int(top_color[2] * (1 - t) + bot_color[2] * t)
        draw.rectangle([(0, y), (width, y + 4)], fill=(r, g, b, 255))

for f in range(TOTAL_FRAMES):
    frame = Image.new("RGBA", (WIDTH, HEIGHT), (248, 250, 252, 255))
    draw = ImageDraw.Draw(frame)
    draw_gradient_background(draw, WIDTH, HEIGHT)

    t = f / FPS

    if f < scene1_end:
        # === SCENE 1: Real App Walkthrough (0s to 4.0s) ===
        progress = f / scene1_end
        # Ease out cubic
        ease = 1 - math.pow(1 - progress, 3)

        # Header Badge
        badge_text = "GAGE PRACIMANTORO"
        draw.rounded_rectangle([(340, 110), (740, 160)], radius=25, fill=(229, 35, 32, 25))
        draw.text((540, 135), badge_text, fill=(229, 35, 32), font=font_badge, anchor="mm")

        draw.text((540, 215), "Semua Kebutuhan Warga", fill=(15, 23, 42), font=font_title, anchor="mm")
        draw.text((540, 280), "Dalam 1 Aplikasi SuperApp Lokal", fill=(100, 116, 139), font=font_subtitle, anchor="mm")

        # Phone mockup container with shadow
        phone_w = 780
        aspect = img_home.height / img_home.width
        phone_h = int(phone_w * aspect)
        phone_scaled = img_home.resize((phone_w, phone_h), Image.Resampling.LANCZOS)

        # Vertical scroll animation: start from top, scroll smoothly downward
        scroll_y = int(370 - ease * 480)
        phone_x = (WIDTH - phone_w) // 2

        # Card shadow
        draw.rounded_rectangle([(phone_x - 12, 360), (phone_x + phone_w + 12, 1720)], radius=44, fill=(0, 0, 0, 15))
        draw.rounded_rectangle([(phone_x - 6, 364), (phone_x + phone_w + 6, 1714)], radius=40, fill=(0, 0, 0, 25))

        # Clip inside phone viewport
        clip_rect = (phone_x, 370, phone_x + phone_w, 1710)
        viewport = Image.new("RGBA", (phone_w, 1340), (255, 255, 255, 255))
        viewport.paste(phone_scaled, (0, scroll_y - 370), phone_scaled)

        # Round viewport corners
        mask = Image.new("L", (phone_w, 1340), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (phone_w, 1340)], radius=36, fill=255)

        frame.paste(viewport, (phone_x, 370), mask)

    elif f < scene2_end:
        # === SCENE 2: 8 Clay Services Showcase (4.0s to 8.2s) ===
        progress = (f - scene1_end) / (scene2_end - scene1_end)
        ease = min(1.0, progress * 1.4)
        scale_in = 0.92 + 0.08 * math.sin(ease * math.pi / 2)

        # Header Badge
        draw.rounded_rectangle([(370, 150), (710, 200)], radius=25, fill=(22, 163, 74, 25))
        draw.text((540, 175), "8 LAYANAN ANDALAN", fill=(22, 163, 74), font=font_badge, anchor="mm")

        draw.text((540, 260), "Kuliner, Sembako & Paket", fill=(15, 23, 42), font=font_title, anchor="mm")
        draw.text((540, 325), "Pracimantoro, Eromoko, Giritontro & Giriwoyo", fill=(100, 116, 139), font=font_subtitle, anchor="mm")

        # Large Inset Card for the 8 Clay Icons
        card_w, card_h = 920, 680
        card_x = (WIDTH - card_w) // 2
        card_y = 520

        # Card shadow & border
        draw.rounded_rectangle([(card_x - 8, card_y + 12), (card_x + card_w + 8, card_y + card_h + 20)], radius=42, fill=(0, 0, 0, 12))
        draw.rounded_rectangle([(card_x - 4, card_y + 6), (card_x + card_w + 4, card_y + card_h + 10)], radius=38, fill=(0, 0, 0, 20))
        draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=36, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

        # Resize perfect service grid
        target_grid_w = int(820 * scale_in)
        grid_ratio = target_grid_w / img_grid.width
        target_grid_h = int(img_grid.height * grid_ratio)
        grid_scaled = img_grid.resize((target_grid_w, target_grid_h), Image.Resampling.LANCZOS)

        gx = (WIDTH - target_grid_w) // 2
        gy = card_y + (card_h - target_grid_h) // 2
        frame.paste(grid_scaled, (gx, gy), grid_scaled)

        # Highlight tag on bottom
        tag_y = 1320
        draw.rounded_rectangle([(240, tag_y), (840, tag_y + 80)], radius=24, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
        draw.text((540, tag_y + 40), "100% Produk & Driver Warga Lokal", fill=(30, 41, 59), font=font_subtitle, anchor="mm")

    else:
        # === SCENE 3: 3D Courier Scooter & Call To Action (8.2s to end) ===
        progress = (f - scene2_end) / (scene3_end - scene2_end)
        ease = min(1.0, progress * 1.2)

        # Top Badge
        draw.rounded_rectangle([(390, 160), (690, 210)], radius=25, fill=(229, 35, 32, 25))
        draw.text((540, 185), "CEPAT & TERPERCAYA", fill=(229, 35, 32), font=font_badge, anchor="mm")

        draw.text((540, 270), "Sekali Klik, Driver Meluncur!", fill=(15, 23, 42), font=font_title, anchor="mm")
        draw.text((540, 335), "Ongkir hemat, barang diantar sampai depan pintu", fill=(100, 116, 139), font=font_subtitle, anchor="mm")

        # 3D Scooter gliding from left-center with subtle organic vertical hover bounce
        bounce = math.sin(t * 5.0) * 16
        scooter_w = 720
        sc_ratio = scooter_w / img_scooter.width
        scooter_h = int(img_scooter.height * sc_ratio)
        scooter_scaled = img_scooter.resize((scooter_w, scooter_h), Image.Resampling.LANCZOS)

        # Dynamic entrance glide: from x=-150 to x=180
        sc_x = int(-150 + ease * 330)
        sc_y = int(580 + bounce)

        # Ground soft shadow under scooter
        shadow_w = int(scooter_w * 0.7)
        shadow_h = 36
        draw.ellipse([(sc_x + 90, sc_y + scooter_h - 40), (sc_x + 90 + shadow_w, sc_y + scooter_h - 40 + shadow_h)], fill=(0, 0, 0, 25))

        frame.paste(scooter_scaled, (sc_x, sc_y), scooter_scaled)

        # Red CTA Button
        cta_y = 1420
        cta_btn_x1, cta_btn_x2 = 220, 860
        cta_btn_y1, cta_btn_y2 = cta_y, cta_y + 110

        # CTA shadow
        draw.rounded_rectangle([(cta_btn_x1, cta_btn_y1 + 10), (cta_btn_x2, cta_btn_y2 + 10)], radius=32, fill=(229, 35, 32, 50))
        draw.rounded_rectangle([(cta_btn_x1, cta_btn_y1), (cta_btn_x2, cta_btn_y2)], radius=30, fill=(229, 35, 32, 255))
        draw.text((540, cta_y + 55), "Buka GAGE Sekarang", fill=(255, 255, 255), font=font_cta, anchor="mm")

        draw.text((540, 1580), "Tersedia untuk Android & Web App", fill=(148, 163, 184), font=font_subtitle, anchor="mm")

    # Bottom Subtitle / Captions (Synchronized with speech)
    if t < 4.2:
        caption = "Mau kulineran, belanja sembako, atau kirim paket di Pracimantoro?"
    elif t < 7.8:
        caption = "Sekarang serba praktis lewat GAGE."
    else:
        caption = "Sekali klik, driver langsung meluncur!"

    # Draw modern kinetic pill subtitle at y=1770
    cap_bbox = draw.textbbox((540, 1780), caption, font=font_subtitle, anchor="mm")
    pad_x, pad_y = 28, 14
    draw.rounded_rectangle([(cap_bbox[0] - pad_x, cap_bbox[1] - pad_y), (cap_bbox[2] + pad_x, cap_bbox[3] + pad_y)], radius=24, fill=(15, 23, 42, 230))
    draw.text((540, 1780), caption, fill=(255, 255, 255), font=font_subtitle, anchor="mm")

    # Save frame
    frame_path = TEMP_DIR / f"frame_{f:05d}.png"
    frame.convert("RGB").save(frame_path)

    if (f + 1) % 60 == 0 or f == TOTAL_FRAMES - 1:
        print(f"[Holymoly Studio] Rendered {f + 1}/{TOTAL_FRAMES} frames ({((f + 1) / TOTAL_FRAMES) * 100:.1f}%)")

print("[Holymoly Studio] Compiling MP4 with FFmpeg & Audio Mixing...")

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-r", str(FPS),
    "-i", str(TEMP_DIR / "frame_%05d.png"),
    "-i", str(AUDIO_PATH),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "fast",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(FINAL_VIDEO_PATH),
]

subprocess.run(ffmpeg_cmd, check=True)
print(f"[Holymoly Studio] MASTER VIDEO READY: {FINAL_VIDEO_PATH}")

# Cleanup temp frames
for f in TEMP_DIR.glob("*.png"):
    try:
        f.unlink()
    except Exception:
        pass
try:
    TEMP_DIR.rmdir()
except Exception:
    pass
