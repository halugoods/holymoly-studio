#!/usr/bin/env python3
"""
Master Video Assembly Script for NUSA Kasir Fotocopy V5 (Puck VO + Seamless Transition)
- Total Duration: exactly 60.000s @ 60 FPS (1080x1920)
- Audio: Voice Puck (energetic, friendly copy center owner persona from ep7)
- Seamless Beat 2 & Beat 3 with continuous scrolling grid background,
  shrinking phone mockup (full frame visible at bottom, zero cropping),
  and web browser window gliding in from top with zoom settling.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
V4_DIR = OUT_DIR / "fresh_v4"
ARTIFACT_DIR = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744")

GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"

BROLL1 = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_fresh_v4/scene-01.mp4")
BEAT2_3_SEAMLESS = V4_DIR / "beat2_3_seamless_31s.mp4"
BROLL2 = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-02.mp4")
BEAT5_RAW = V4_DIR / "mobile_beat5_15.0s.mp4"
VO_PUCK = V4_DIR / "fotocopy_pc_puck_60s_vo.wav"

def generate_subtitles_ass(ass_path):
    print(f"[ASS Subtitles] Generating Rule 15 pure typography subtitles at {ass_path}...")
    ass_content = """[Script Info]
Title: NUSA Kasir Fotocopy Commercial V5 Puck
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
Dialogue: 0,0:00:00.30,0:00:04.40,Default,,0,0,0,,Buka usaha fotocopy kok masih ribet\\Ncolok-cabut flashdisk pelanggan?
Dialogue: 0,0:00:04.70,0:00:07.10,Default,,0,0,0,,Awas, laptop toko rawan kena virus!
Dialogue: 0,0:00:08.40,0:00:11.20,Default,,0,0,0,,Solusinya, pakai NUSA Kasir Fotocopy!
Dialogue: 0,0:00:11.60,0:00:15.80,Default,,0,0,0,,Cukup buka menu Portal File dari HP tokomu,\\Nlalu klik Buka di PC.
Dialogue: 0,0:00:16.20,0:00:20.50,Default,,0,0,0,,Alamat server lokal langsung aktif tanpa kabel\\ndan tanpa install software apapun!
Dialogue: 0,0:00:22.60,0:00:25.00,Default,,0,0,0,,Sekarang buka Google Chrome di komputer tokomu.
Dialogue: 0,0:00:25.30,0:00:29.00,Default,,0,0,0,,Semua berkas antrean pelanggan\\nlangsung masuk otomatis di monitor PC!
Dialogue: 0,0:00:29.50,0:00:34.50,Default,,0,0,0,,Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi\\nlangsung tersimpan dan siap diprint.
Dialogue: 0,0:00:35.00,0:00:37.20,Default,,0,0,0,,Zero kabel data, zero colok flashdisk!
Dialogue: 0,0:00:39.50,0:00:43.20,Default,,0,0,0,,Hasil cetak langsung keluar dari mesin percetakanmu\\ndengan cepat dan aman.
Dialogue: 0,0:00:44.80,0:00:49.80,Default,,0,0,0,,Biaya print per lembar, cetak warna, sampai jasa jilid\\notomatis terhitung rapi di kasir!
Dialogue: 0,0:00:50.20,0:00:51.20,Default,,0,0,0,,Praktis banget kan?
Dialogue: 0,0:00:51.50,0:00:55.20,Default,,0,0,0,,NUSA Kasir Fotocopy, sekali beli aktif selamanya\\ntanpa biaya bulanan.
Dialogue: 0,0:00:55.40,0:00:57.00,Default,,0,0,0,,Download sekarang juga!
"""
    ass_path.write_text(ass_content, encoding='utf-8')
    print("[ASS Subtitles] Saved successfully.")

def render_beat5_mockup(out_path, duration=16.000):
    print(f"[Beat 5 Mockup] Rendering mockup_beat5 ({duration:.3f}s @ 60 FPS)...")
    filter_complex = (
        "[1:v]tpad=stop_mode=clone:stop_duration=3,fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
        "[scaled_screen][2:v]alphamerge[masked_screen];"
        "[0:v][masked_screen]overlay=x=190:y=105:shortest=1[bg_screen];"
        "[bg_screen][3:v]overlay=x=0:y=0:shortest=1[final_v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(GRID_MP4),
        "-i", str(BEAT5_RAW),
        "-loop", "1", "-i", str(MASK_PNG),
        "-loop", "1", "-i", str(FRAME_PNG),
        "-filter_complex", filter_complex,
        "-map", "[final_v]",
        "-t", f"{duration:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Beat 5 Mockup] Saved {out_path.name} ({out_path.stat().st_size} bytes)")

def assemble():
    std_beat1 = V4_DIR / "std_beat1_8.0s.mp4"
    std_beat4 = V4_DIR / "std_beat4_5.0s.mp4"
    std_beat5 = V4_DIR / "mockup_beat5_16.0s.mp4"

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

    # 3. Render Beat 5 Mockup (16.000s)
    render_beat5_mockup(std_beat5, 16.000)

    # 4. Concatenate:
    # 0: std_beat1 (8.000s)
    # 1: beat2_3_seamless_31s (31.000s)
    # 2: std_beat4 (5.000s)
    # 3: mockup_beat5 (16.000s)
    # Total = 8.000 + 31.000 + 5.000 + 16.000 = 60.000s
    clean_master = V4_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    print(f"[Assembly] Concatenating 4 parts -> {clean_master.name}...")

    filter_concat = "[0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[v_clean]"

    cmd_clean = [
        "ffmpeg", "-y",
        "-i", str(std_beat1),
        "-i", str(BEAT2_3_SEAMLESS),
        "-i", str(std_beat4),
        "-i", str(std_beat5),
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

    # 5. Create Subtitled Master
    ass_path = V4_DIR / "subtitles_v5_puck.ass"
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

    # 6. Copy Deliverables to Artifact Directory
    artifact_clean = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    artifact_master = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"

    shutil.copy2(clean_master, artifact_clean)
    shutil.copy2(subtitled_master, artifact_master)
    print(f"[Delivery] Copied clean master to {artifact_clean}")
    print(f"[Delivery] Copied subtitled master to {artifact_master}")

    # 7. Extract Audit Frames
    audit_points = [
        (4.0, "v5_audit_beat1_4s.png", "Beat 1: USB Flashdrive plugged into laptop"),
        (14.0, "v5_audit_beat2_14s.png", "Beat 2: NUSA Kasir Fotocopy Portal File & Buka di PC"),
        (21.5, "v5_audit_trans_21s.png", "Transition: Phone shrinks smoothly, Web descends from top"),
        (26.0, "v5_audit_workstation_26s.png", "Beat 3: Workstation - Web queue top, Phone bottom fully framed"),
        (34.0, "v5_audit_toast_34s.png", "Beat 3: Skripsi PDF Download Toast"),
        (42.0, "v5_audit_beat4_42s.png", "Beat 4: Laser Printer continuous physical output"),
        (50.0, "v5_audit_beat5_50s.png", "Beat 5: NUSA Kasir POS - Print & Jilid auto-kalkulasi"),
        (58.0, "v5_audit_beat5_58s.png", "Beat 5: Outro Call to Action")
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
