#!/usr/bin/env python3
"""
Record Real Chrome Desktop Web Session for Beat 3 (18.0s @ 60 FPS)
Using Playwright native video recorder
"""

import os
import sys
import time
import glob
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
VIDEO_DIR = OUT_DIR / "web_video"
FINAL_DESKTOP_MP4 = OUT_DIR / "real_desktop_beat3_18s.mp4"

def record_chrome():
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    for f in VIDEO_DIR.glob("*"):
        try: f.unlink()
        except: pass
        
    print("[Playwright] Launching Real Chromium for Desktop Session...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="msedge")
        context = browser.new_context(
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1280, "height": 720},
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # 1. Open Portal File
        print("  [Action] Opening Portal File...")
        page.goto("http://127.0.0.1:8080/portal-file", wait_until="networkidle")
        page.wait_for_selector(".order-card", timeout=10000)
        
        # Start continuous DOM ticker to ensure 60fps recording without frame drops
        page.evaluate("""() => {
            const ticker = document.createElement('div');
            ticker.id = 'render_ticker';
            ticker.style.position = 'fixed';
            ticker.style.bottom = '0';
            ticker.style.right = '0';
            ticker.style.width = '1px';
            ticker.style.height = '1px';
            ticker.style.opacity = '0.01';
            document.body.appendChild(ticker);
            let count = 0;
            function loop() {
                count++;
                ticker.innerText = count;
                requestAnimationFrame(loop);
            }
            requestAnimationFrame(loop);
        }""")
        
        # Helper for smooth ease-in-out cursor interpolation
        def smooth_mouse(x1, y1, x2, y2, duration, steps=30):
            interval = duration / steps
            for i in range(1, steps + 1):
                t = i / steps
                ease = 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
                cx = x1 + (x2 - x1) * ease
                cy = y1 + (y2 - y1) * ease
                page.mouse.move(cx, cy)
                page.wait_for_timeout(interval * 1000)
                
        # 0.0s - 3.5s: Initial overview of Portal Antrean File
        print("  [0.0s - 3.5s] Overview & Server status...")
        page.mouse.move(950, 45)
        page.wait_for_timeout(3500)
        
        # 3.5s - 8.0s: Gliding down to inspect queue and Budi Santoso skripsi
        print("  [3.5s - 8.0s] Gliding down to queue cards...")
        smooth_mouse(950, 45, 450, 260, duration=2.5, steps=50)
        smooth_mouse(450, 260, 280, 480, duration=2.0, steps=40)
        
        # 8.0s - 10.5s: Hovering over 'Unduh ke PC' button
        print("  [8.0s - 10.5s] Hovering Unduh ke PC...")
        btn = page.locator("a.btn-file-dl").first
        box = btn.bounding_box()
        target_x = box["x"] + box["width"] / 2 if box else 200
        target_y = box["y"] + box["height"] / 2 if box else 550
        smooth_mouse(280, 480, target_x, target_y, duration=1.5, steps=30)
        page.wait_for_timeout(1000)
        
        # 10.5s - 14.5s: Click download & show authentic toast
        print("  [10.5s - 14.5s] Clicking Unduh ke PC & notification...")
        btn.click()
        page.evaluate("""() => {
            const toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.bottom = '28px';
            toast.style.left = '50%';
            toast.style.transform = 'translateX(-50%)';
            toast.style.background = 'rgba(15, 23, 42, 0.95)';
            toast.style.border = '1px solid #38bdf8';
            toast.style.boxShadow = '0 10px 30px rgba(56, 189, 248, 0.3)';
            toast.style.color = '#ffffff';
            toast.style.padding = '12px 24px';
            toast.style.borderRadius = '14px';
            toast.style.fontSize = '14px';
            toast.style.fontWeight = '700';
            toast.style.display = 'flex';
            toast.style.alignItems = 'center';
            toast.style.gap = '10px';
            toast.style.zIndex = '99999';
            toast.innerHTML = '<span>📥</span> <span>Tersimpan di PC: <b>Skripsi_Budi_Santoso_Bab_1-5.pdf</b> (Siap Cetak)</span>';
            document.body.appendChild(toast);
        }""")
        page.wait_for_timeout(4000)
        
        # 14.5s - 18.5s: Gentle idle drift while holding view
        print("  [14.5s - 18.5s] Gentle hold & inspection...")
        smooth_mouse(target_x, target_y, target_x + 80, target_y - 40, duration=2.0, steps=40)
        page.wait_for_timeout(2000)
        
        page.close()
        context.close()
        browser.close()
        
    recorded_files = list(VIDEO_DIR.glob("*.webm"))
    if not recorded_files:
        raise RuntimeError("No recorded video found in web_video")
        
    src_webm = max(recorded_files, key=lambda f: f.stat().st_size)
    print(f"[FFmpeg] Converting {src_webm.name} ({src_webm.stat().st_size} bytes) to 18.0s MP4: {FINAL_DESKTOP_MP4.name}...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(src_webm),
        "-vf", "scale=1280:720,fps=60",
        "-t", "18.000",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(FINAL_DESKTOP_MP4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[FFmpeg Error]:", res.stderr)
        raise RuntimeError("Conversion failed")
        
    print(f"[Success] Real Desktop MP4 created: {FINAL_DESKTOP_MP4.name} ({FINAL_DESKTOP_MP4.stat().st_size} bytes)")

if __name__ == "__main__":
    record_chrome()
