#!/usr/bin/env python3
"""
Holymoly Studio - Indonesia History 60s Master Video Producer
(by Halu Goods Indonesia)

Assembles:
- 12 0-Credit Papercraft Diorama Keyframes (Nano Banana 2.1 / Imagen 3)
- Gemini Native Audio Voiceover (Charon / 24kHz Studio Master)
- Seamless Dual-Keyframe Ken Burns Camera Rig & Filmic Cross-Dissolve
- Minimalist Chapter Badges & High-Contrast Kinetic Subtitles
- Deep Atmospheric Cinematic Ambient Drone Score

Output: 1080x1920 (9:16 Vertical) ~72s Master Documentary Video
"""

import math
import os
import subprocess
import sys
import wave
from pathlib import Path

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FLOW_OUT = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60s")
AUDIO_DIR = FLOW_OUT / "gemini_audio"
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MASTER_MP4 = OUT_DIR / "sejarah_jepang_indonesia_60s.mp4"
CONCAT_LIST_PATH = OUT_DIR / "history_scenes_concat.txt"
BG_DRONE_PATH = OUT_DIR / "cinematic_drone.wav"

FONT_INTER = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/assets/fonts/Inter.ttf")
FONT_TITLE = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/assets/fonts/Bebas Neue.ttf")

WIDTH, HEIGHT = 1080, 1920
FPS = 30


# 1. Synthesize Ambient Cinematic Drone (Deep 55Hz + Warm 110Hz Fifth + Swell)
def generate_ambient_drone(duration: float, out_path: Path):
    sr = 24000
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # Low Cello Drone (A1 55Hz + E2 82.5Hz + A2 110Hz)
    drone = 0.35 * np.sin(2 * np.pi * 55 * t)
    drone += 0.20 * np.sin(2 * np.pi * 82.5 * t)
    drone += 0.12 * np.sin(2 * np.pi * 110 * t)
    # Subtle harmonic movement
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t)
    drone = drone * (0.8 + 0.2 * lfo)
    # Master gain
    drone = drone * 0.22
    # Convert to 16-bit PCM
    audio_int16 = (np.clip(drone, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())
    print(f"[Ambient Score] Synthesized {duration:.1f}s atmospheric drone -> {out_path.name}")


generate_ambient_drone(85.0, BG_DRONE_PATH)


def get_audio_duration(p: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


# Fonts
def load_font(font_path: Path, size: int):
    try:
        return ImageFont.truetype(str(font_path), size)
    except Exception:
        return ImageFont.load_default()

font_chap_num = load_font(FONT_TITLE, 36)
font_chap_title = load_font(FONT_TITLE, 52)
font_sub = load_font(FONT_INTER, 34)
font_sub_bold = load_font(FONT_INTER, 34)

# Scene Configurations
SCENES_CONFIG = [
    {
        "num": 1,
        "open_img": FLOW_OUT / "scene-01.jpeg",
        "close_img": FLOW_OUT / "scene-02.jpeg",
        "audio": AUDIO_DIR / "scene_01.wav",
        "badge": "01 / 06 · MARET 1942",
        "title": "ARMADA LAUT JEPANG MENDARAT DI JAWA",
        "caption_line1": "Maret 1942. Di tengah runtuhnya Hindia Belanda,",
        "caption_line2": "Armada Jepang mendarat membawa propaganda Saudara Tua.",
    },
    {
        "num": 2,
        "open_img": FLOW_OUT / "scene-03.jpeg",
        "close_img": FLOW_OUT / "scene-04.jpeg",
        "audio": AUDIO_DIR / "scene_02.wav",
        "badge": "02 / 06 · 1942-1943",
        "title": "PROPAGANDA GERAKAN TIGA A & REALITA",
        "caption_line1": "Slogan Tiga A bergema: Cahaya, Pelindung, Pemimpin Asia.",
        "caption_line2": "Namun janji manis segera berganti duka dan penderitaan.",
    },
    {
        "num": 3,
        "open_img": FLOW_OUT / "scene-05.jpeg",
        "close_img": FLOW_OUT / "scene-06.jpeg",
        "audio": AUDIO_DIR / "scene_03.wav",
        "badge": "03 / 06 · 1943-1944",
        "title": "KERJA PAKSA ROMUSHA DI BELANTARA",
        "caption_line1": "Romusha. Beras disita, jutaan rakyat dipaksa memeras keringat",
        "caption_line2": "Membangun jalur rel maut menembus rimba tanpa belas kasihan.",
    },
    {
        "num": 4,
        "open_img": FLOW_OUT / "scene-07.jpeg",
        "close_img": FLOW_OUT / "scene-08.jpeg",
        "audio": AUDIO_DIR / "scene_04.wav",
        "badge": "04 / 06 · 1943-1945",
        "title": "BARISAN MILITER PETA & SUPRIYADI",
        "caption_line1": "Dari tekanan lahirlah perlawanan. Pemuda dilatih dalam PETA,",
        "caption_line2": "Yang justru menjadi bara api kebangkitan tentara nasional.",
    },
    {
        "num": 5,
        "open_img": FLOW_OUT / "scene-09.jpeg",
        "close_img": FLOW_OUT / "scene-10.jpeg",
        "audio": AUDIO_DIR / "scene_05.wav",
        "badge": "05 / 06 · AGUSTUS 1945",
        "title": "JATUHNYA BOM ATOM & RENGASDENGKLOK",
        "caption_line1": "Agustus 1945. Bom atom meluluhlantakkan Hiroshima & Nagasaki.",
        "caption_line2": "Pemuda bergerak cepat mendesak Bung Karno di Rengasdengklok.",
    },
    {
        "num": 6,
        "open_img": FLOW_OUT / "scene-11.jpeg",
        "close_img": FLOW_OUT / "scene-12.jpeg",
        "audio": AUDIO_DIR / "scene_06.wav",
        "badge": "06 / 06 · 17 AGUSTUS 1945",
        "title": "FAJAR KEMERDEKAAN INDONESIA MERDEKA",
        "caption_line1": "17 Agustus 1945. Di Pegangsaan Timur, Proklamasi berkumandang.",
        "caption_line2": "Dari tiga setengah tahun derita, lahirlah Indonesia Merdeka!",
    },
]


def render_scene(cfg: dict, drone_audio_offset: float) -> tuple[Path, float]:
    scene_num = cfg["num"]
    print(f"\n[Scene {scene_num}] Preparing video render...")

    audio_dur = get_audio_duration(cfg["audio"])
    # Pad 0.3s for smooth transition
    scene_dur = audio_dur + 0.3
    total_frames = int(scene_dur * FPS)

    open_img = Image.open(cfg["open_img"]).convert("RGBA")
    close_img = Image.open(cfg["close_img"]).convert("RGBA")

    # Resize images to cover canvas + 10% margins for Ken Burns zooming
    canvas_w, canvas_h = WIDTH, HEIGHT
    margin_w = int(canvas_w * 1.15)
    margin_h = int(canvas_h * 1.15)

    open_scaled = open_img.resize((margin_w, margin_h), Image.Resampling.LANCZOS)
    close_scaled = close_img.resize((margin_w, margin_h), Image.Resampling.LANCZOS)

    out_scene_mp4 = OUT_DIR / f"scene_{scene_num:02d}.mp4"

    # FFmpeg command: rawvideo from stdin + Gemini audio + Drone ambient audio
    # Audio filter: Mix Gemini narration (0dB) + Drone ambient (-17dB)
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgba", "-r", str(FPS),
        "-i", "-",  # Video frames from stdin
        "-i", str(cfg["audio"]),  # Gemini Narration
        "-ss", str(drone_audio_offset), "-i", str(BG_DRONE_PATH),  # Ambient Drone
        "-filter_complex",
        "[1:a]volume=1.0[voice]; [2:a]volume=0.20[drone]; [voice][drone]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "veryfast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_scene_mp4),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    # Crossfade range: 44% to 56% of total duration
    fade_start = int(total_frames * 0.44)
    fade_end = int(total_frames * 0.56)

    for f in range(total_frames):
        p = f / total_frames  # 0.0 to 1.0

        # === 1. Dual-Keyframe Ken Burns Motion ===
        if f < fade_start:
            # Only open image
            zoom = 1.00 + 0.08 * (f / fade_start)
            pan_y = int(12 * (f / fade_start))
            crop_w = int(canvas_w / zoom)
            crop_h = int(canvas_h / zoom)
            left = (margin_w - crop_w) // 2
            top = (margin_h - crop_h) // 2 + pan_y
            frame_bg = open_scaled.crop((left, top, left + crop_w, top + crop_h)).resize((canvas_w, canvas_h), Image.Resampling.BILINEAR)

        elif f > fade_end:
            # Only close image
            rel_p = (f - fade_end) / (total_frames - fade_end)
            zoom = 1.07 - 0.05 * rel_p
            pan_y = int(15 * rel_p)
            crop_w = int(canvas_w / zoom)
            crop_h = int(canvas_h / zoom)
            left = (margin_w - crop_w) // 2
            top = (margin_h - crop_h) // 2 - pan_y
            frame_bg = close_scaled.crop((left, top, left + crop_w, top + crop_h)).resize((canvas_w, canvas_h), Image.Resampling.BILINEAR)

        else:
            # Crossfade blend between open and close
            alpha_t = (f - fade_start) / (fade_end - fade_start)
            # Smooth sine easing
            blend_w = 0.5 - 0.5 * math.cos(alpha_t * math.pi)

            # Crop open
            crop_w1 = int(canvas_w / 1.06)
            crop_h1 = int(canvas_h / 1.06)
            f1 = open_scaled.crop(((margin_w - crop_w1)//2, (margin_h - crop_h1)//2, (margin_w - crop_w1)//2 + crop_w1, (margin_h - crop_h1)//2 + crop_h1)).resize((canvas_w, canvas_h), Image.Resampling.BILINEAR)

            # Crop close
            crop_w2 = int(canvas_w / 1.07)
            crop_h2 = int(canvas_h / 1.07)
            f2 = close_scaled.crop(((margin_w - crop_w2)//2, (margin_h - crop_h2)//2, (margin_w - crop_w2)//2 + crop_w2, (margin_h - crop_h2)//2 + crop_h2)).resize((canvas_w, canvas_h), Image.Resampling.BILINEAR)

            frame_bg = Image.blend(f1, f2, blend_w)

        # Pure high-definition frame without artificial vignette box
        frame = frame_bg.copy()
        draw = ImageDraw.Draw(frame)

        # === 2. Minimalist Chapter Watermark (Top Left / Center) ===
        # Badge Pill
        badge_text = cfg["badge"]
        draw.rounded_rectangle([(70, 90), (390, 142)], radius=26, fill=(15, 23, 42, 210), outline=(234, 179, 8, 180), width=1)
        draw.text((230, 116), badge_text, fill=(254, 240, 138), font=font_chap_num, anchor="mm")

        # Chapter Title banner
        title_text = cfg["title"]
        draw.rounded_rectangle([(70, 158), (940, 222)], radius=20, fill=(15, 23, 42, 180))
        draw.text((90, 190), title_text, fill=(255, 255, 255), font=font_chap_title, anchor="lm")

        # === 3. Kinetic Subtitles (Bottom Center) ===
        sub1 = cfg["caption_line1"]
        sub2 = cfg["caption_line2"]

        # Background pill for subtitle
        bbox1 = draw.textbbox((540, 1720), sub1, font=font_sub, anchor="mm")
        bbox2 = draw.textbbox((540, 1775), sub2, font=font_sub, anchor="mm")
        min_x = min(bbox1[0], bbox2[0]) - 32
        max_x = max(bbox1[2], bbox2[2]) + 32
        min_y = bbox1[1] - 18
        max_y = bbox2[3] + 20

        draw.rounded_rectangle([(min_x, min_y), (max_x, max_y)], radius=24, fill=(10, 15, 26, 220), outline=(255, 255, 255, 40), width=1)

        # Line 1 (White crisp text)
        draw.text((540, 1720), sub1, fill=(255, 255, 255), font=font_sub, anchor="mm")
        # Line 2 (Warm Golden Glow for impactful storytelling)
        draw.text((540, 1775), sub2, fill=(253, 224, 71), font=font_sub, anchor="mm")

        # Push to ffmpeg rawvideo stream
        proc.stdin.write(frame.tobytes())

        if (f + 1) % 100 == 0 or f == total_frames - 1:
            print(f"  Frame {f + 1}/{total_frames} ({((f + 1) / total_frames) * 100:.1f}%)")

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed on scene {scene_num} with returncode {proc.returncode}")

    print(f"[Scene {scene_num}] SUCCESS -> {out_scene_mp4.name} ({scene_dur:.2f}s)")
    return out_scene_mp4, scene_dur


# Run all 6 scenes
rendered_scenes = []
drone_offset = 0.0

for cfg in SCENES_CONFIG:
    mp4_path, dur = render_scene(cfg, drone_offset)
    rendered_scenes.append(mp4_path)
    drone_offset += dur

# 2. Concat all 6 scenes into FINAL MASTER MP4
print("\n[Holymoly Studio] Stitching 6 scenes into Master 60s Film...")
with open(CONCAT_LIST_PATH, "w", encoding="utf-8") as f:
    for s in rendered_scenes:
        f.write(f"file '{s.resolve().as_posix()}'\n")

concat_cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(CONCAT_LIST_PATH),
    "-c", "copy",
    str(FINAL_MASTER_MP4)
]
subprocess.run(concat_cmd, check=True)

print(f"\n=======================================================")
print(f"🎬 MASTER 60s HISTORICAL FILM PRODUCED SUCCESSFULLY!")
print(f"Location: {FINAL_MASTER_MP4}")
print(f"Size: {FINAL_MASTER_MP4.stat().st_size / (1024 * 1024):.2f} MB")
print(f"=======================================================")
