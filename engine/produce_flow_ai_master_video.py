#!/usr/bin/env python3
"""
Holymoly Studio - Indonesia History 60s Flow AI Master Video Producer
(by Halu Goods Indonesia)

Assembles:
- 6 Real Google Flow AI Generated Videos (Omni 1.1 Flash Start->End Keyframe Interpolation)
- Gemini Studio Master Narration + Ambient Drone Score
- Chapter Badges & Kinetic Subtitles (1080x1920 Vertical 9:16)
"""

import os
import subprocess
import sys
from pathlib import Path

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFont

FLOW_VID_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60sVideo")
AUDIO_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60s/gemini_audio")
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output_flow_ai")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MASTER_MP4 = OUT_DIR / "sejarah_jepang_flow_ai_60s.mp4"
CONCAT_LIST_PATH = OUT_DIR / "flow_scenes_concat.txt"
BG_DRONE_PATH = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output/cinematic_drone.wav")

FONT_INTER = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/assets/fonts/Inter.ttf")
FONT_TITLE = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/assets/fonts/Bebas Neue.ttf")

WIDTH, HEIGHT = 1080, 1920

SCENES_CONFIG = [
    {
        "num": 1,
        "video": FLOW_VID_DIR / "scene-07.mp4",
        "audio": AUDIO_DIR / "scene_01.wav",
        "badge": "01 / 06 · MARET 1942",
        "title": "ARMADA LAUT JEPANG MENDARAT DI JAWA",
        "caption_line1": "Maret 1942. Di tengah runtuhnya Hindia Belanda,",
        "caption_line2": "Armada Jepang mendarat membawa propaganda Saudara Tua.",
    },
    {
        "num": 2,
        "video": FLOW_VID_DIR / "scene-08.mp4",
        "audio": AUDIO_DIR / "scene_02.wav",
        "badge": "02 / 06 · 1942-1943",
        "title": "PROPAGANDA GERAKAN TIGA A & REALITA",
        "caption_line1": "Slogan Tiga A bergema: Cahaya, Pelindung, Pemimpin Asia.",
        "caption_line2": "Namun janji manis segera berganti duka dan penderitaan.",
    },
    {
        "num": 3,
        "video": FLOW_VID_DIR / "scene-09.mp4",
        "audio": AUDIO_DIR / "scene_03.wav",
        "badge": "03 / 06 · 1943-1944",
        "title": "KERJA PAKSA ROMUSHA DI BELANTARA",
        "caption_line1": "Romusha. Beras disita, jutaan rakyat dipaksa memeras keringat",
        "caption_line2": "Membangun jalur rel maut menembus rimba tanpa belas kasihan.",
    },
    {
        "num": 4,
        "video": FLOW_VID_DIR / "scene-10.mp4",
        "audio": AUDIO_DIR / "scene_04.wav",
        "badge": "04 / 06 · 1943-1945",
        "title": "BARISAN MILITER PETA & SUPRIYADI",
        "caption_line1": "Dari tekanan lahirlah perlawanan. Pemuda dilatih dalam PETA,",
        "caption_line2": "Yang justru menjadi bara api kebangkitan tentara nasional.",
    },
    {
        "num": 5,
        "video": FLOW_VID_DIR / "scene-13.mp4",
        "audio": AUDIO_DIR / "scene_05.wav",
        "badge": "05 / 06 · AGUSTUS 1945",
        "title": "KABAR MENYERAHNYA JEPANG & RENGASDENGKLOK",
        "caption_line1": "Agustus 1945. Kabar kekalahan Jepang merebak cepat.",
        "caption_line2": "Pemuda bergerak cepat mendesak Bung Karno di Rengasdengklok.",
    },
    {
        "num": 6,
        "video": FLOW_VID_DIR / "scene-12.mp4",
        "audio": AUDIO_DIR / "scene_06.wav",
        "badge": "06 / 06 · 17 AGUSTUS 1945",
        "title": "FAJAR KEMERDEKAAN INDONESIA MERDEKA",
        "caption_line1": "17 Agustus 1945. Di Pegangsaan Timur, Proklamasi berkumandang.",
        "caption_line2": "Dari tiga setengah tahun derita, lahirlah Indonesia Merdeka!",
    },
]

def get_duration(p: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(p)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

# Create transparent overlay PNG with badges and subtitles for each scene
def create_overlay_png(cfg: dict, out_png: Path):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_badge = ImageFont.truetype(str(FONT_TITLE), 36)
    font_title = ImageFont.truetype(str(FONT_TITLE), 52)
    font_sub = ImageFont.truetype(str(FONT_INTER), 34)

    # 1. Badge Pill
    draw.rounded_rectangle([(70, 90), (390, 142)], radius=26, fill=(15, 23, 42, 210), outline=(234, 179, 8, 180), width=1)
    draw.text((230, 116), cfg["badge"], fill=(254, 240, 138), font=font_badge, anchor="mm")

    # 2. Title Banner
    draw.rounded_rectangle([(70, 158), (940, 222)], radius=20, fill=(15, 23, 42, 180))
    draw.text((90, 190), cfg["title"], fill=(255, 255, 255), font=font_title, anchor="lm")

    # 3. Subtitle Pill
    sub1 = cfg["caption_line1"]
    sub2 = cfg["caption_line2"]
    bbox1 = draw.textbbox((540, 1720), sub1, font=font_sub, anchor="mm")
    bbox2 = draw.textbbox((540, 1775), sub2, font=font_sub, anchor="mm")
    min_x = min(bbox1[0], bbox2[0]) - 32
    max_x = max(bbox1[2], bbox2[2]) + 32
    min_y = bbox1[1] - 18
    max_y = bbox2[3] + 20

    draw.rounded_rectangle([(min_x, min_y), (max_x, max_y)], radius=24, fill=(10, 15, 26, 220), outline=(255, 255, 255, 40), width=1)
    draw.text((540, 1720), sub1, fill=(255, 255, 255), font=font_sub, anchor="mm")
    draw.text((540, 1775), sub2, fill=(253, 224, 71), font=font_sub, anchor="mm")

    img.save(out_png)

def process_scene(cfg: dict, drone_offset: float) -> tuple[Path, float]:
    scene_num = cfg["num"]
    print(f"\n[Scene {scene_num}] Processing Flow AI Video -> {cfg['video'].name}...")

    audio_dur = get_duration(cfg["audio"])
    target_dur = audio_dur + 0.3  # slight buffer for smooth transition
    flow_vid_dur = get_duration(cfg["video"])
    speed_factor = target_dur / flow_vid_dur

    overlay_png = OUT_DIR / f"overlay_scene_{scene_num:02d}.png"
    create_overlay_png(cfg, overlay_png)

    out_mp4 = OUT_DIR / f"flow_scene_{scene_num:02d}.mp4"

    # Filter:
    # 1. Scale Flow video to 1080x1920 with high-quality lanczos
    # 2. Retime video frames with setpts=speed_factor*PTS
    # 3. Overlay subtitles & badge PNG
    # 4. Mix narration (0dB) + ambient drone (-17dB)
    filter_complex = (
        f"[0:v]scale={WIDTH}:{HEIGHT}:flags=lanczos,setpts={speed_factor:.4f}*PTS[bg]; "
        f"[bg][1:v]overlay=0:0[vout]; "
        f"[2:a]volume=1.0[voice]; "
        f"[3:a]volume=0.20[drone]; "
        f"[voice][drone]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(cfg["video"]),
        "-loop", "1", "-i", str(overlay_png),
        "-i", str(cfg["audio"]),
        "-ss", str(drone_offset), "-i", str(BG_DRONE_PATH),
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{target_dur:.2f}",
        str(out_mp4)
    ]

    subprocess.run(cmd, check=True)
    print(f"[Scene {scene_num}] SUCCESS -> {out_mp4.name} ({target_dur:.2f}s)")
    return out_mp4, target_dur

rendered_clips = []
drone_offset = 0.0

for cfg in SCENES_CONFIG:
    clip_path, dur = process_scene(cfg, drone_offset)
    rendered_clips.append(clip_path)
    drone_offset += dur

# Concat into master video
print("\n[Holymoly Studio] Assembling 6 Flow AI scenes into Master Film...")
with open(CONCAT_LIST_PATH, "w", encoding="utf-8") as f:
    for c in rendered_clips:
        f.write(f"file '{c.resolve().as_posix()}'\n")

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
print(f"🎬 MASTER GOOGLE FLOW AI VIDEO FILM PRODUCED SUCCESSFULLY!")
print(f"Location: {FINAL_MASTER_MP4}")
print(f"Size: {FINAL_MASTER_MP4.stat().st_size / (1024 * 1024):.2f} MB")
print(f"=======================================================")
