#!/usr/bin/env python3
"""
Assemble NUSA Kasir Fotocopy Flagship Hybrid Commercial Master (63.00s)
Rule 12 (Flow B-Roll Hybrid Studio) + Rule 11 (Centered Z Flip 3 Mockup) + Rule 15 (Pure Typo Subtitles)

Beat Structure (Total 63.00s):
- Beat 1 (00.0s - 08.0s, 8.0s): Flow B-Roll 1 (Hand plugging flash drive into counter laptop)
- Beat 2 (08.0s - 23.5s, 15.5s): Centered Z Flip 3 Mockup (Dashboard -> Portal File -> Buka di PC Dialog)
- Beat 3 (23.5s - 41.5s, 18.0s): Workstation Desktop Chrome with 1.40x Punch-In on download
- Beat 4 (41.5s - 46.5s, 05.0s): Flow B-Roll 2 (Locked-off macro photocopy laser printer dispensing Skripsi pages)
- Beat 5 (46.5s - 63.0s, 16.5s): Centered Z Flip 3 Mockup (Bayar di Kasir -> Layanan Cetak -> Checkout -> Struk)
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
FLOW_DIR = Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc")
ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

VO_AUDIO = OUT_DIR / "fotocopy_pc_connect_v3_vo.wav"
FINAL_MASTER_SUB = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"
FINAL_MASTER_CLEAN = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
ASS_SUB_FILE = OUT_DIR / "fotocopy_pc_v3_pure_typo.ass"

CLIPS = [
    {
        "id": "beat_01_flashdisk_broll",
        "file": FLOW_DIR / "scene-01.mp4",
        "dur": 8.000,
        "type": "flow"
    },
    {
        "id": "beat_02_mockup_portal_pc",
        "file": OUT_DIR / "mockup_beat2_15.5s.mp4",
        "dur": 15.500,
        "type": "mockup"
    },
    {
        "id": "beat_03_workstation_chrome",
        "file": OUT_DIR / "workstation_beat3_18s.mp4",
        "dur": 18.000,
        "type": "workstation"
    },
    {
        "id": "beat_04_printer_broll",
        "file": FLOW_DIR / "scene-02.mp4",
        "dur": 5.000,
        "type": "flow"
    },
    {
        "id": "beat_05_mockup_checkout_struk",
        "file": OUT_DIR / "mockup_beat5_16.5s.mp4",
        "dur": 16.500,
        "type": "mockup"
    }
]

SUBTITLE_PHRASES = [
    {"start": "0:00:00.50", "end": "0:00:04.56", "text": "Buka usaha fotocopy kok masih ribet\\ncolok-cabut flashdisk pelanggan?"},
    {"start": "0:00:05.11", "end": "0:00:07.80", "text": "Awas, laptop toko rawan kena virus!"},
    {"start": "0:00:08.54", "end": "0:00:11.33", "text": "Solusinya, pakai NUSA Kasir Fotocopy!"},
    {"start": "0:00:12.01", "end": "0:00:16.87", "text": "Cukup buka menu Portal File dari HP tokomu,\\nlalu klik Buka di PC."},
    {"start": "0:00:17.66", "end": "0:00:22.95", "text": "Alamat server lokal langsung aktif tanpa perlu kabel\\ndan tanpa install software apapun!"},
    {"start": "0:00:23.79", "end": "0:00:26.53", "text": "Sekarang buka Google Chrome\\ndi komputer tokomu."},
    {"start": "0:00:27.18", "end": "0:00:31.07", "text": "Semua berkas antrean pelanggan\\nlangsung masuk otomatis di monitor PC!"},
    {"start": "0:00:31.90", "end": "0:00:37.59", "text": "Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi\\nlangsung tersimpan dan siap diprint."},
    {"start": "0:00:38.41", "end": "0:00:40.91", "text": "Zero kabel data, zero colok flashdisk!"},
    {"start": "0:00:41.66", "end": "0:00:45.69", "text": "Hasil cetak langsung keluar dari mesin percetakanmu\\ndengan cepat dan aman."},
    {"start": "0:00:46.49", "end": "0:00:51.97", "text": "Biaya print per lembar, cetak warna, sampai jasa jilid\\notomatis terhitung rapi di kasir!"},
    {"start": "0:00:52.75", "end": "0:00:56.00", "text": "Praktis banget kan?"},
    {"start": "0:00:56.39", "end": "0:00:59.60", "text": "NUSA Kasir Fotocopy, sekali beli aktif selamanya\\ntanpa biaya bulanan."},
    {"start": "0:01:00.19", "end": "0:01:01.38", "text": "Download sekarang juga!"}
]

def generate_ass_subtitles():
    print(f"[Subtitles] Generating Rule 15 Universal Pure Typography ASS: {ASS_SUB_FILE.name}...")
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: PureTypo,Arial,52,&H00FFFFFF,&H0000FFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3.5,4.5,2,40,40,240,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]
    for sub in SUBTITLE_PHRASES:
        lines.append(f"Dialogue: 0,{sub['start']},{sub['end']},PureTypo,,0,0,0,,{sub['text']}")
    
    with open(ASS_SUB_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[Subtitles] ASS file created ({len(SUBTITLE_PHRASES)} dialogue events)")

def standardize_clip(clip_info, out_path):
    src = clip_info["file"]
    dur = clip_info["dur"]
    print(f"[Standardize] {clip_info['id']} ({dur:.3f}s): {src.name} -> {out_path.name}...")

    vf_filters = [
        "scale=1080:1920:force_original_aspect_ratio=increase",
        "crop=1080:1920",
        "fps=60",
        f"tpad=stop_mode=clone:stop_duration={dur}"
    ]

    cmd = [
        "ffmpeg", "-y",
        "-err_detect", "ignore_err",
        "-max_error_rate", "1.0",
        "-i", str(src),
        "-vf", ",".join(vf_filters),
        "-t", f"{dur:.3f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    subprocess.run(cmd, check=True)

def assemble_master():
    print("=" * 70)
    print("NUSA KASIR FOTOCOPY: ASSEMBLING MASTER COMMERCIAL (63.00s)")
    print("=" * 70)

    # 1. Standardize all 5 clips
    std_clips = []
    for idx, c in enumerate(CLIPS):
        std_file = OUT_DIR / f"std_v3_part_{idx+1}_{c['id']}.mp4"
        standardize_clip(c, std_file)
        std_clips.append(std_file)

    # 2. Concat list
    concat_list = OUT_DIR / "concat_v3_63s.txt"
    with open(concat_list, "w") as f:
        for p in std_clips:
            f.write(f"file '{p.resolve()}'\n")

    temp_video = OUT_DIR / "temp_video_v3_63s.mp4"
    print(f"\n[Concat] Concatenating 5 clips to {temp_video.name}...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(temp_video)
    ]
    subprocess.run(concat_cmd, check=True)

    # 3. Create Clean Master (Keynote Clean, No Subtitles)
    print(f"\n[Mux Clean] Muxing video with Gemini Native Audio (Clean Master)...")
    clean_temp = OUT_DIR / "fotocopy_clean_master_temp.mp4"
    mux_clean_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(VO_AUDIO),
        "-map_metadata", "-1",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "63.000",
        str(clean_temp)
    ]
    subprocess.run(mux_clean_cmd, check=True)

    # 4. Create Flagship Master with Rule 15 Pure Typography Subtitles
    generate_ass_subtitles()
    print(f"\n[Mux Master] Burning Rule 15 Pure Typography Subtitles...")
    sub_temp = OUT_DIR / "fotocopy_sub_master_temp.mp4"
    ass_escaped = str(ASS_SUB_FILE).replace("\\", "/").replace(":", "\\:")
    mux_sub_cmd = [
        "ffmpeg", "-y",
        "-i", str(clean_temp),
        "-vf", f"ass='{ass_escaped}'",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-t", "63.000",
        str(sub_temp)
    ]
    subprocess.run(mux_sub_cmd, check=True)

    # 5. Sanitize C2PA Metadata & Deploy to Artifacts
    print(f"\n[Sanitize & Deploy] Copying to final artifacts...")
    shutil.copyfile(clean_temp, FINAL_MASTER_CLEAN)
    shutil.copyfile(sub_temp, FINAL_MASTER_SUB)

    print(f"[Success] Deliverable 1 (Master): {FINAL_MASTER_SUB.name} ({FINAL_MASTER_SUB.stat().st_size} bytes)")
    print(f"[Success] Deliverable 2 (Clean):  {FINAL_MASTER_CLEAN.name} ({FINAL_MASTER_CLEAN.stat().st_size} bytes)")

    # 6. Extract 7 Audit Frames (Rule 12 Pre-Delivery Audit Loop)
    audit_points = [
        ("beat_1_4s", 4.0, "Beat 1: USB Flashdisk counter laptop B-roll"),
        ("beat_2_16s", 16.0, "Beat 2: Z Flip 3 Mockup Portal File & Buka di PC dialog"),
        ("beat_3_28s", 28.0, "Beat 3: Desktop Chrome Browser Queue Overview"),
        ("beat_3_36s", 36.0, "Beat 3: Desktop Chrome 1.40x Punch-In Download Toast"),
        ("beat_4_44s", 44.0, "Beat 4: Laser Printer Photocopy Struk output"),
        ("beat_5_54s", 54.0, "Beat 5: Kasir POS Checkout & Layanan Cetak"),
        ("beat_5_61s", 61.0, "Beat 5: Digital Struk Lunas & Outro")
    ]
    print(f"\n[Audit Loop] Extracting {len(audit_points)} key proof frames...")
    for label, sec, desc in audit_points:
        frame_png = ARTIFACT_DIR / f"audit_v3_{label}.png"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{sec:.2f}",
            "-i", str(FINAL_MASTER_SUB),
            "-vframes", "1",
            str(frame_png)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  [Frame] {sec:4.1f}s: {frame_png.name} ({desc})")

if __name__ == "__main__":
    assemble_master()
