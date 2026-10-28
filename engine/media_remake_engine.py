#!/usr/bin/env python3
"""
Holymoly Studio - Social Media Downloader & Vision REA Remake Engine
Downloads media from YouTube, Shorts, Instagram Reels, TikTok via yt-dlp,
extracts keyframes via FFmpeg, analyzes visual style, and formulates
interactive remake options for the project workspace.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import yt_dlp

BASE_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio")
DOWNLOADS_DIR = BASE_DIR / "downloads"

def ensure_downloads_dir() -> Path:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return DOWNLOADS_DIR

def download_social_media(url: str, dest_dir: Path = None) -> dict:
    """Download video or image from social media URL using yt-dlp."""
    if dest_dir is None:
        dest_dir = ensure_downloads_dir()
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(datetime.now().timestamp())
    ydl_opts = {
        'outtmpl': str(dest_dir / f"media_{timestamp}_%(id)s.%(ext)s"),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            
            # If merged format had a different extension (e.g. mkv -> mp4)
            if not Path(downloaded_file).exists():
                stem = Path(downloaded_file).stem
                candidates = list(dest_dir.glob(f"{stem}*"))
                if candidates:
                    downloaded_file = str(candidates[0])

            return {
                "success": True,
                "title": info.get("title", "Social Video"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
                "view_count": info.get("view_count", 0),
                "thumbnail": info.get("thumbnail"),
                "webpage_url": info.get("webpage_url", url),
                "file_path": downloaded_file,
                "file_name": Path(downloaded_file).name,
                "downloaded_at": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def extract_keyframes(video_path: Path, output_dir: Path, fps: float = 1.0) -> list:
    """Extract keyframe images using ffmpeg at given fps."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_pattern = output_dir / "frame_%04d.jpg"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        str(out_pattern)
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    frames = sorted(list(output_dir.glob("frame_*.jpg")))
    return [str(f) for f in frames]

def analyze_visual_pacing(keyframes: list, duration: float) -> dict:
    """Estimates visual pacing and scene changes from keyframes."""
    num_frames = len(keyframes)
    cuts_per_sec = (num_frames / max(duration, 1.0)) if duration > 0 else 1.0
    
    pacing_tag = "Fast" if cuts_per_sec > 1.2 else ("Medium" if cuts_per_sec > 0.5 else "Slow")
    
    return {
        "total_frames": num_frames,
        "duration_seconds": duration,
        "estimated_pacing": pacing_tag,
        "recommended_style": "Fast Editorial Montage" if pacing_tag == "Fast" else "Centered Vector Mockup Z Flip 3"
    }

def generate_remake_card(meta: dict, pacing: dict) -> dict:
    """Generate interactive choice options for the user to remake the downloaded video."""
    title = meta.get("title", "Video Referensi")
    duration = meta.get("duration", 15)
    
    return {
        "card_type": "onboarding_question",
        "question_data": {
            "index": 1,
            "key": "remake_style",
            "title": "Pilih Gaya Remake Video",
            "question": f"Video referensi **'{title}'** ({duration}s) berhasil dianalisis!\n\nGaya remake mana yang ingin diterapkan untuk konten tokomu?",
            "options": [
                {
                    "key": "A",
                    "label": "Adaptasi ke Mockup HP Z Flip 3 (9:16)",
                    "desc": "Tampilan centered phone mockup Samsung Galaxy Z Flip 3, infinite blurred grid, zero crop."
                },
                {
                    "key": "B",
                    "label": "Hybrid B-Roll Sinematik + POS (60 Detik)",
                    "desc": "Suasana toko riil sinematik bergantian dengan alur kasir POS & struk termal."
                },
                {
                    "key": "C",
                    "label": "Vox Investigative Documentary (9:16)",
                    "desc": "Tempo investigatif, foto toko 100% fresh, quad-warp UI pada layar HP aktor, word-anchored sync."
                },
                {
                    "key": "D",
                    "label": "Fast Editorial Montage (0.8s Cut)",
                    "desc": "Transisi cepat, 3x3 reveal, 2-frame strobe, yellow highlighter sweep, 26 transient SFX."
                }
            ]
        }
    }

if __name__ == "__main__":
    print("[OK] Media Remake Engine initialized.")
