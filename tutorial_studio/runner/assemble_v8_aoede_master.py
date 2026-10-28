#!/usr/bin/env python3
"""
Master Video Assembly Script for NUSA Kasir Fotocopy V8 (Female Voice: Aoede)
- Total Duration: exactly 60.000s @ 60 FPS (1080x1920)
- Audio: Voice Aoede (Female, stylish, warm, professional broadcast talent from ep6 salon commercial)
- Video: V7 Visual Master
  * Centered Z Flip 3 Mockup with Touch Tap Ripples
  * Seamless descent of Chrome Web POS & macro pull-back
  * Symmetrical LAN Glass Badge at exact midpoint cy = 872 (152px top & bottom margins)
  * Smart Camera Zoom (1.45x) focusing on 'Unduh ke PC' button
  * Proportional Phone Mockup Zoom (0.42x -> 0.609x)
  * Animated Mouse Cursor gliding, clicking with bounce scale and expanding emerald ripple
  * Clean toast notification & continuous laser printer B-Roll
- Rule 15 Pure Typography Subtitles (Zero box wrapper, Arial bold 52, White, multi-layer shadow, safe-zone)
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

STD_BEAT1 = V4_DIR / "std_beat1_8.0s.mp4"
BEAT2_3_SEAMLESS = V4_DIR / "beat2_3_seamless_31s.mp4"
STD_BEAT4 = V4_DIR / "std_beat4_5.0s.mp4"
BEAT5_MOCKUP = V4_DIR / "mockup_beat5_16.0s.mp4"
VO_AOEDE = V4_DIR / "fotocopy_pc_aoede_60s_vo.wav"

def generate_subtitles_ass(ass_path):
    print(f"[ASS Subtitles] Generating Rule 15 pure typography subtitles for Aoede at {ass_path}...")
    ass_content = """[Script Info]
Title: NUSA Kasir Fotocopy Commercial V8 Aoede Female VO
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
Dialogue: 0,0:00:00.46,0:00:04.30,Default,,0,0,0,,Buka usaha fotocopy kok masih ribet\\Ncolok-cabut flashdisk pelanggan?
Dialogue: 0,0:00:04.62,0:00:07.34,Default,,0,0,0,,Awas, laptop toko rawan kena virus!
Dialogue: 0,0:00:08.54,0:00:11.26,Default,,0,0,0,,Solusinya, pakai NUSA Kasir Fotocopy!
Dialogue: 0,0:00:11.98,0:00:16.38,Default,,0,0,0,,Cukup buka menu Portal File dari HP tokomu,\\Nlalu klik Buka di PC.
Dialogue: 0,0:00:16.94,0:00:21.42,Default,,0,0,0,,Alamat server lokal langsung aktif tanpa kabel\\ndan tanpa install software apapun!
Dialogue: 0,0:00:22.36,0:00:25.08,Default,,0,0,0,,Sekarang buka Google Chrome di komputer tokomu.
Dialogue: 0,0:00:25.48,0:00:29.08,Default,,0,0,0,,Semua berkas antrean pelanggan\\nlangsung masuk otomatis di monitor PC!
Dialogue: 0,0:00:29.64,0:00:34.84,Default,,0,0,0,,Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi\\nlangsung tersimpan dan siap diprint.
Dialogue: 0,0:00:35.32,0:00:37.72,Default,,0,0,0,,Zero kabel data, zero colok flashdisk!
Dialogue: 0,0:00:39.70,0:00:43.30,Default,,0,0,0,,Hasil cetak langsung keluar dari mesin percetakanmu\\ndengan cepat dan aman.
Dialogue: 0,0:00:44.81,0:00:49.77,Default,,0,0,0,,Biaya print per lembar, cetak warna, sampai jasa jilid\\notomatis terhitung rapi di kasir!
Dialogue: 0,0:00:50.01,0:00:50.97,Default,,0,0,0,,Praktis banget kan?
Dialogue: 0,0:00:51.45,0:00:55.85,Default,,0,0,0,,NUSA Kasir Fotocopy, sekali beli aktif selamanya\\ntanpa biaya bulanan.
Dialogue: 0,0:00:56.25,0:00:57.29,Default,,0,0,0,,Download sekarang juga!
"""
    ass_path.write_text(ass_content, encoding='utf-8')
    print("[ASS Subtitles] Saved successfully.")

def assemble():
    clean_master = V4_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    print(f"[Assembly V8 Aoede] Concatenating 4 parts -> {clean_master.name}...")

    filter_concat = "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[v_clean]"

    cmd_clean = [
        "ffmpeg", "-y",
        "-i", str(STD_BEAT1),
        "-i", str(BEAT2_3_SEAMLESS),
        "-i", str(STD_BEAT4),
        "-i", str(BEAT5_MOCKUP),
        "-i", str(VO_AOEDE),
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

    # Create Subtitled Master
    ass_path = V4_DIR / "subtitles_v8_aoede.ass"
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

    # Copy Deliverables to Artifact Directory
    artifact_clean = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    artifact_master = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"

    shutil.copy2(clean_master, artifact_clean)
    shutil.copy2(subtitled_master, artifact_master)
    print(f"[Delivery] Copied clean master to {artifact_clean}")
    print(f"[Delivery] Copied subtitled master to {artifact_master}")

    # Extract Audit Frames
    audit_points = [
        (4.0, "v8_audit_beat1_4s.png", "Beat 1: USB Flashdrive plugged into laptop"),
        (14.0, "v8_audit_beat2_14s.png", "Beat 2: NUSA Kasir Fotocopy Portal File & Touch Ripple"),
        (18.0, "v8_audit_workstation_18s.png", "Beat 3: Symmetrical LAN Workstation (cy=872, 152px margins)"),
        (29.6, "v8_audit_smart_zoom_click_29s.png", "Beat 3: Smart Zoom into 'Unduh ke PC' + Cursor Click Ripple"),
        (35.0, "v8_audit_toast_35s.png", "Beat 3: Skripsi PDF Download Toast in Macro View"),
        (37.5, "v8_audit_dual_view_37s.png", "Beat 3: Restored Wide Dual View (Zero Kabel Zero Flashdisk)"),
        (42.0, "v8_audit_beat4_42s.png", "Beat 4: Laser Printer continuous physical output"),
        (50.0, "v8_audit_beat5_pos_50s.png", "Beat 5: NUSA Kasir POS - Touch Tap Ripples & Kalkulasi"),
        (58.0, "v8_audit_beat5_outro_58s.png", "Beat 5: Outro Call to Action & Digital Struk")
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
