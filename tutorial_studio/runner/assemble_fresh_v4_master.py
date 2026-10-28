#!/usr/bin/env python3
"""
Master Video Assembly Script for NUSA Kasir Fotocopy V4 Commercial
- 60.000s Total Duration @ 60 FPS (1080x1920)
- 5 Script-Driven Beats:
  1. Beat 1 (0.00s - 8.00s, 8.00s): Fresh Flow B-Roll 1 (Macro steady cam of USB flash drive into laptop)
  2. Beat 2 (8.00s - 23.00s, 15.00s): Z Flip 3 Mockup (NUSA Kasir Fotocopy -> Portal File -> Buka di PC)
  3. Beat 3 (23.00s - 40.30s, 17.30s): Chrome Workstation (Browser file queue -> Download Skripsi PDF -> Toast)
  4. Beat 4 (40.30s - 45.00s, 4.70s): Flow B-Roll 2 (Macro laser printer continuous printout)
  5. Beat 5 (45.00s - 60.00s, 15.00s): Z Flip 3 Mockup (POS Kasir print kalkulasi -> Tunai -> Digital Struk)
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
MOCKUP_BEAT2 = V4_DIR / "mockup_beat2_15.0s.mp4"
WORKSTATION_BEAT3 = V4_DIR / "workstation_beat3_17.3s.mp4"
BROLL2 = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-02.mp4")
MOCKUP_BEAT5 = V4_DIR / "mockup_beat5_15.0s.mp4"
VO_WAV = V4_DIR / "fotocopy_pc_v4_vo.wav"

def generate_subtitles_ass(ass_path):
    print(f"[ASS Subtitles] Generating Rule 15 pure typography subtitles at {ass_path}...")
    # Safe zone bottom MarginV = 240, Alignment = 2 (bottom center), Fontsize = 52, Bold = 1
    # PrimaryColour: &H00FFFFFF (White), Outline: 3.5 (&H00000000 Black), Shadow: 2.0
    ass_content = """[Script Info]
Title: NUSA Kasir Fotocopy Commercial V4
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
Dialogue: 0,0:00:00.00,0:00:04.66,Default,,0,0,0,,Buka usaha fotocopy kok masih ribet\\Ncolok-cabut flashdisk pelanggan?
Dialogue: 0,0:00:05.21,0:00:08.08,Default,,0,0,0,,Awas, laptop toko rawan kena virus!
Dialogue: 0,0:00:08.73,0:00:11.67,Default,,0,0,0,,Solusinya, pakai NUSA Kasir Fotocopy!
Dialogue: 0,0:00:12.42,0:00:17.29,Default,,0,0,0,,Cukup buka menu Portal File dari HP tokomu,\\Nlalu klik Buka di PC.
Dialogue: 0,0:00:17.90,0:00:22.91,Default,,0,0,0,,Alamat server lokal langsung aktif tanpa kabel\\ndan tanpa install software apapun!
Dialogue: 0,0:00:23.63,0:00:26.24,Default,,0,0,0,,Sekarang buka Google Chrome di komputer tokomu.
Dialogue: 0,0:00:26.77,0:00:30.51,Default,,0,0,0,,Semua berkas antrean pelanggan\\nlangsung masuk otomatis di monitor PC!
Dialogue: 0,0:00:31.26,0:00:37.01,Default,,0,0,0,,Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi\\nlangsung tersimpan dan siap diprint.
Dialogue: 0,0:00:37.51,0:00:40.12,Default,,0,0,0,,Zero kabel data, zero colok flashdisk!
Dialogue: 0,0:00:40.79,0:00:44.52,Default,,0,0,0,,Hasil cetak langsung keluar dari mesin percetakanmu\\ndengan cepat dan aman.
Dialogue: 0,0:00:45.19,0:00:50.46,Default,,0,0,0,,Biaya print per lembar, cetak warna, sampai jasa jilid\\notomatis terhitung rapi di kasir!
Dialogue: 0,0:00:50.90,0:00:51.80,Default,,0,0,0,,Praktis banget kan?
Dialogue: 0,0:00:52.43,0:00:56.85,Default,,0,0,0,,NUSA Kasir Fotocopy, sekali beli aktif selamanya\\ntanpa biaya bulanan.
Dialogue: 0,0:00:57.28,0:00:58.61,Default,,0,0,0,,Download sekarang juga!
"""
    ass_path.write_text(ass_content, encoding='utf-8')
    print("[ASS Subtitles] Saved successfully.")

def standardize_clip(input_path, output_path, duration):
    print(f"[Standardize] Processing {input_path.name} -> {output_path.name} ({duration:.3f}s @ 1080x1920 60fps)...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-t", f"{duration:.3f}",
        "-vf", "fps=60,scale=1080:1920:flags=lanczos,setsar=1",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    print(f"[Standardize] Saved {output_path.name} ({output_path.stat().st_size} bytes)")

def assemble():
    std_beat1 = V4_DIR / "std_beat1_8.0s.mp4"
    std_beat4 = V4_DIR / "std_beat4_4.7s.mp4"

    # 1. Standardize Beat 1 (8.000s) and Beat 4 (4.700s)
    standardize_clip(BROLL1, std_beat1, 8.000)
    standardize_clip(BROLL2, std_beat4, 4.700)

    # 2. Concat 5 beats and mux with VO to create clean master
    clean_master = V4_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    print(f"[Assembly] Concatenating 5 beats -> {clean_master.name}...")

    # Filter complex concat 5 video streams
    filter_concat = (
        "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0[v_clean]"
    )

    cmd_clean = [
        "ffmpeg", "-y",
        "-i", str(std_beat1),          # 0: 8.000s
        "-i", str(MOCKUP_BEAT2),       # 1: 15.000s
        "-i", str(WORKSTATION_BEAT3),  # 2: 17.300s
        "-i", str(std_beat4),          # 3: 4.700s
        "-i", str(MOCKUP_BEAT5),       # 4: 15.000s
        "-i", str(VO_WAV),             # 5: audio
        "-filter_complex", filter_concat,
        "-map", "[v_clean]",
        "-map", "5:a",
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

    # 3. Create Subtitled Master
    ass_path = V4_DIR / "subtitles.ass"
    generate_subtitles_ass(ass_path)

    subtitled_master = V4_DIR / "nusa_fotocopy_pc_connect_master.mp4"
    print(f"[Subtitles] Burning subtitles onto master -> {subtitled_master.name}...")

    # Escape path for ffmpeg ass filter on windows
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

    # 4. Copy Deliverables to Artifact Directory
    artifact_clean = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
    artifact_master = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"

    shutil.copy2(clean_master, artifact_clean)
    shutil.copy2(subtitled_master, artifact_master)
    print(f"[Delivery] Copied clean master to {artifact_clean}")
    print(f"[Delivery] Copied subtitled master to {artifact_master}")

    # 5. Extract 7 Audit Frames
    audit_points = [
        (4.0, "audit_v4_beat1_4s.png", "Beat 1: USB Flashdrive plugged into laptop"),
        (14.0, "audit_v4_beat2_14s.png", "Beat 2: NUSA Kasir Fotocopy Portal File & Buka di PC"),
        (26.0, "audit_v4_beat3_26s.png", "Beat 3: Chrome Workstation - Local Server Web POS Queue"),
        (34.0, "audit_v4_beat3_34s.png", "Beat 3: Chrome Workstation - Skripsi Download Toast"),
        (42.0, "audit_v4_beat4_42s.png", "Beat 4: Laser Printer continuous physical output"),
        (50.0, "audit_v4_beat5_50s.png", "Beat 5: NUSA Kasir POS - Print & Jilid auto-kalkulasi"),
        (58.0, "audit_v4_beat5_58s.png", "Beat 5: Outro Call to Action")
    ]

    print("[Audit] Extracting 7 key audit frames...")
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
