#!/usr/bin/env python3
"""
Record Real Chrome Desktop Web Session for Beat 3 (18.0s @ 60 FPS)
Interacts with live http://127.0.0.1:8080/portal-file using Playwright Chromium
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
TEMP_FRAMES = OUT_DIR / "chrome_frames"
TEMP_FRAMES.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUT_DIR / "real_chrome_portal_beat3.mp4"

def record_desktop():
    print("[Playwright] Launching Chrome Desktop for Portal File recording...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        # 16:9 widescreen viewport
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=2 # Retina 2x for ultra-crisp text
        )
        page = context.new_page()
        
        print("[Playwright] Navigating to http://127.0.0.1:8080/portal-file...")
        page.goto("http://127.0.0.1:8080/portal-file", wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        
        # We need 18.0s total duration
        # We capture snapshots or video
        # Let's see: Playwright can record video directly or save frames
        fps = 30
        total_frames = int(18.0 * fps)
        
        print(f"[Playwright] Capturing {total_frames} frames (18.0s @ {fps}fps)...")
        
        # Initial cursor position
        page.mouse.move(200, 600)
        
        for f in range(total_frames):
            t = f / fps
            
            # Smooth cursor movement to Budi Santoso download button
            # Button is inside first card: .order-card .btn-download
            if t < 3.0:
                # Browse top header & search
                page.mouse.move(400, 200)
            elif t < 7.0:
                # Move towards Budi Santoso card download button
                p_move = (t - 3.0) / 4.0
                cx = 400 + p_move * (450 - 400)
                cy = 200 + p_move * (365 - 200)
                page.mouse.move(cx, cy)
            elif t < 8.5:
                # Hover on button
                page.mouse.move(450, 365)
            elif t < 9.5:
                # Click
                if f == int(8.5 * fps):
                    print("  [Action] Clicking Unduh ke PC on Budi Santoso...")
                    try:
                        btn = page.locator(".btn-download").first
                        btn.click()
                    except Exception as e:
                        print("  [Click fallback]:", e)
                        page.mouse.click(450, 365)
            else:
                # Move slightly to reveal the downloaded status
                page.mouse.move(550, 380)
                
            frame_path = TEMP_FRAMES / f"frame_{f:04d}.png"
            page.screenshot(path=str(frame_path))
            
        browser.close()

    print("[Playwright] Assembling frames to MP4 with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "30",
        "-i", str(TEMP_FRAMES / "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-t", "18.000",
        str(OUT_MP4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[FFmpeg Error]:", res.stderr)
        raise RuntimeError("FFmpeg assembly failed")
        
    # Clean up temp frames
    for f in TEMP_FRAMES.glob("*.png"):
        f.unlink()
    TEMP_FRAMES.rmdir()
    
    print(f"[Success] Saved {OUT_MP4.name} ({OUT_MP4.stat().st_size} bytes, 18.0s)")

if __name__ == "__main__":
    record_desktop()
