#!/usr/bin/env python3
"""
Clean up old legacy HolyMoly assets and scripts, moving them to archive_legacy.
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio")
ARCHIVE_DIR = BASE_DIR / "archive_legacy"

def main():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    (ARCHIVE_DIR / "assets").mkdir(parents=True, exist_ok=True)
    (ARCHIVE_DIR / "engine").mkdir(parents=True, exist_ok=True)
    
    # 1. Old assets
    assets_dir = BASE_DIR / "assets"
    for f in assets_dir.glob("IndonesiaHistory60s*"):
        dest = ARCHIVE_DIR / "assets" / f.name
        print(f"Archiving: {f} -> {dest}")
        shutil.move(str(f), str(dest))
        
    for f in assets_dir.glob("ui_captures/*"):
        dest = ARCHIVE_DIR / "assets" / f.name
        print(f"Archiving: {f} -> {dest}")
        shutil.move(str(f), str(dest))
        
    old_courier = assets_dir / "cutouts" / "scooter_courier.png"
    if old_courier.exists():
        shutil.move(str(old_courier), str(ARCHIVE_DIR / "assets" / old_courier.name))
        
    old_raw = assets_dir / "raw" / "scooter_courier_raw.jpeg"
    if old_raw.exists():
        shutil.move(str(old_raw), str(ARCHIVE_DIR / "assets" / old_raw.name))
        
    # 2. Old motion lab
    motion_lab = BASE_DIR / "motion_lab"
    if motion_lab.exists():
        dest_motion = ARCHIVE_DIR / "motion_lab"
        print(f"Archiving: {motion_lab} -> {dest_motion}")
        if dest_motion.exists():
            shutil.rmtree(str(dest_motion))
        shutil.move(str(motion_lab), str(dest_motion))
        
    # 3. Old engine scripts
    engine_dir = BASE_DIR / "engine"
    legacy_scripts = [
        "assemble_pov_mancing.py",
        "capture_shadcn_web.py",
        "generate_jepang_assets.py",
        "test_speech.py",
        "test_tts.py"
    ]
    for s in legacy_scripts:
        src = engine_dir / s
        if src.exists():
            dest = ARCHIVE_DIR / "engine" / s
            print(f"Archiving script: {src} -> {dest}")
            shutil.move(str(src), str(dest))
            
    # 4. Old holymoly_web (vite dist / etc)
    old_web = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_web")
    if old_web.exists():
        dest_web = ARCHIVE_DIR / "holymoly_web"
        print(f"Archiving web: {old_web} -> {dest_web}")
        if dest_web.exists():
            shutil.rmtree(str(dest_web))
        shutil.move(str(old_web), str(dest_web))
        
    print("[SUCCESS] Legacy files cleanly archived in archive_legacy/!")

if __name__ == "__main__":
    main()
