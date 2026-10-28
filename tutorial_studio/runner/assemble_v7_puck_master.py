#!/usr/bin/env python3
"""
Master Video Assembly Script for NUSA Kasir Fotocopy V7 (Puck Clean VO + Full Interactivity)
- Total Duration: exactly 60.000s @ 60 FPS (1080x1920)
- Audio: Voice Puck Clean (Metropolitan Jakarta commercial TV accent, non-medhok, crisp 'pe-lang-gan' diction)
- Visual Interactivity:
  * Smart camera zoom to 'Unduh ke PC' button at (280, 450) with 1.45x zoom
  * Phone mockup scales proportionally (0.42 -> 0.609x) maintaining unified optical perspective
  * Balanced LAN status badge at exact midpoint cy = 872 (152px top, 152px bottom)
  * Animated mouse cursor gliding and clicking 'Unduh ke PC' with bounce & ripple
  * Animated touch tap ripples on mobile phone screen across Beats 2 and 5
- Rule 15 Pure Typography Subtitles (Zero box wrapper, Inter/Arial bold 52, White, multi-layer shadow, safe-zone)
- Keynote Clean Master (No Subtitles)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
V4_DIR = OUT_DIR / "fresh_v4"
ARTIFACT_DIR = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")

BROLL1 = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_fresh_v4/scene-01.mp4")
BEAT2_3_SEAMLESS = V4_DIR / "beat2_3_seamless_31s.mp4"
BROLL2 = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-02.mp4")
BEAT5_MOCKUP = V4_DIR / "mockup_beat5_16.0s.mp4"
VO_PUCK = V4_DIR / "fotocopy_pc_puck_60s_vo.wav"

def generate_subtitles_ass(ass_path):
    print(f"[ASS Subtitles] Generating Rule 15 pure typography subtitles at {ass_path}...")
    ass_content = """[Script Info]
Title: NUSA Kasir Fotocopy Commercial V7 Puck Clean
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,3.5,2.0,2,60,60,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:04.30,Default,,0,0,0,,Buka usaha fotocopy kok masih ribet\\Ncolok-cabut flashdisk pelanggan?
Dialogue: 0,0:00:04.50,0:00:07.20,Default,,0,0,0,,Awas, laptop toko rawan kena virus!
Dialogue: 0,0:00:08.40,0:00:11.00,Default,,0,0,0,,Solusinya, pakai NUSA Kasir Fotocopy!
Dialogue: 0,0:00:11.40,0:00:15.60,Default,,0,0,0,,Cukup buka menu Portal File dari HP tokomu,\\Nlalu klik Buka di PC.
Dialogue: 0,0:00:16.00,0:00:20.60,Default,,0,0,0,,Alamat server lokal langsung aktif tanpa kabel\\ndan tanpa install software apapun!
Dialogue: 0,0:00:22.70,0:00:25.00,Default,,0,0,0,,Sekarang buka Google Chrome di komputer tokomu.
Dialogue: 0,0:00:25.20,0:00:29.00,Default,,0,0,0,,Semua berkas antrean pelanggan\\nlangsung masuk otomatis di monitor PC!
Dialogue: 0,0:00:29.50,0:00:34.80,Default,,0,0,0,,Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi\\nlangsung tersimpan dan siap diprint.
Dialogue: 0,0:00:35.20,0:00:37.60,Default,,0,0,0,,Zero kabel data, zero colok flashdisk!
Dialogue: 0,0:00:39.60,0:00:43.30,Default,,0,0,0,,Hasil cetak langsung keluar dari mesin percetakanmu\\ndengan cepat dan aman.
Dialogue: 0,0:00:44.60,0:00:49.70,Default,,0,0,0,,Biaya print per lembar, cetak warna, sampai jasa jilid\\notomatis terhitung rapi di kasir!
Dialogue: 0,0:00:49.90,0:00:51.00,Default,,0,0,0,,Praktis banget kan?
Dialogue: 0,0:00:51.20,0:00:55.50,Default,,0,0,0,,NUSA Kasir Fotocopy, sekali beli aktif selamanya\\ntanpa biaya bulanan.
Dialogue: 0,0:00:55.70,0:00:56.90,Default,,0,0,0,,Download sekarang juga!
"""
    ass_path.write_text(ass_content, encoding='utf-8')
    print("[ASS Subtitles] Saved successfully.")

def assemble():
    std_beat1 = V4_DIR / "std_beat1_8.0s.mp4"
    std_beat4 = V4_DIR / "std_beat4_5.0s.mp4"

    # 1. Standardize Beat 1 (8.000s) if not already done
    if not std_beat1.exists():
        cmd1 = [
            "ffmpeg", "-y", "-i", str(BROLL1), "-t", "8.000",
            "-vf", "fps=60,scale=1080:1920:flags=lanczos,setsar=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-an",
            str(std_beat1)
        ]
        subprocess.run(cmd1, check=True)

    # 2. Standardize Beat 4 (5.000s)
    cmd4 = [
        "ffmpeg", "-y", "-i", str(BROLL2), "-t", "5.000",
        "-vf", "fps=60,scale=1080:1920:flags=lanczos,setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-an",
        str(std_beat4)
    ]
    subprocess.run(cmd4, check=True)

    # 3. Concatenate:
    # 0: std_beat1 (8.000s)
    # 1: beat2_3_seamless_31s (31.000s)
    # 2: std_beat4 (5.000s)
    # 3: mockup_beat5_16.0s (16.000s)
    # Total = 8.000 + 31.000 + 5.000 + 16.000 = 60.000s
    clean_master = V4_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    print(f"[Assembly] Concatenating 4 parts -> {clean_master.name}...")

    filter_concat = "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[v_clean]"

    cmd_clean = [
        "ffmpeg", "-y",
        "-i", str(std_beat1),
        "-i", str(BEAT2_3_SEAMLESS),
        "-i", str(std_beat4),
        "-i", str(BEAT5_MOCKUP),
        "-i", str(VO_PUCK),
        "-filter_complex", filter_concat,
        "-map", "[v_clean]",
        "-map", "4:a",
        "-t", "60.000",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(clean_master)
    ]
    subprocess.run(cmd_clean, check=True)
    print(f"[Assembly Success] Clean master saved ({clean_master.stat().st_size} bytes)")

    # 4. Create Subtitled Master
    ass_path = V4_DIR / "subtitles_v7_puck.ass"
    generate_subtitles_ass(ass_path)

    subtitled_master = V4_DIR / "nusa_fotocopy_pc_connect_master.mp4"
    print(f"[Subtitles] Burning subtitles onto master -> {subtitled_master.name}...")

    escaped_ass = str(ass_path).replace("\\", "/").replace(":", "\\:")
    cmd_sub = [
        "ffmpeg", "-y",
        "-i", str(clean_master),
        "-vf", f"subtitles='{escaped_ass}'",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        str(subtitled_master)
    ]
    subprocess.run(cmd_sub, check=True)
    print(f"[Master Success] Subtitled master saved ({subtitled_master.stat().st_size} bytes)")

    # 5. Copy Deliverables to Artifact Directory
    artifact_clean = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    artifact_master = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"

    shutil.copy2(clean_master, artifact_clean)
    shutil.copy2(subtitled_master, artifact_master)
    print(f"[Delivery] Copied clean master to {artifact_clean}")
    print(f"[Delivery] Copied subtitled master to {artifact_master}")

    # 6. Extract Audit Frames
    audit_points = [
        (4.0, "v7_audit_beat1_4s.png", "Beat 1: USB Flashdrive plugged into laptop"),
        (14.0, "v7_audit_beat2_14s.png", "Beat 2: NUSA Kasir Fotocopy Portal File & Touch Ripple"),
        (17.5, "v7_audit_workstation_17s.png", "Beat 3: Symmetrical LAN Workstation (cy=872, 152px margins)"),
        (21.5, "v7_audit_smart_zoom_click_21s.png", "Beat 3: Smart Zoom into 'Unduh ke PC' + Cursor Click Ripple"),
        (25.0, "v7_audit_toast_25s.png", "Beat 3: Skripsi PDF Download Toast in Macro View"),
        (34.0, "v7_audit_dual_view_34s.png", "Beat 3: Restored Wide Dual View (Zero Kabel Zero Flashdisk)"),
        (42.0, "v7_audit_beat4_42s.png", "Beat 4: Laser Printer continuous physical output"),
        (50.0, "v7_audit_beat5_pos_50s.png", "Beat 5: NUSA Kasir POS - Touch Tap Ripples & Kalkulasi"),
        (58.0, "v7_audit_beat5_outro_58s.png", "Beat 5: Outro Call to Action & Digital Struk")
    ]

    print("[Audit] Extracting key audit frames...")
    for t, fname, desc in audit_points:
        out_frame = ARTIFACT_DIR / fname
        cmd_frame = [
            "ffmpeg", "-y",
            "-ss", f"{t:.1f}",
            "-i", str(subtitled_master),
            "-vframes", "1",
            "-q:v", "2",
            str(out_frame)
        ]
        subprocess.run(cmd_frame, check=True)
        print(f"  [OK] Extracted {fname} at {t:.1f}s ({desc})")

if __name__ == "__main__":
    assemble()
