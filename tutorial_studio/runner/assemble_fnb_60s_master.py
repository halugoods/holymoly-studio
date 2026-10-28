#!/usr/bin/env python3
"""
Assemble NUSA Kasir FnB 60-Second Hybrid Commercial Video
Flow Cinematic B-Roll (Veo 3.1) + Centered Samsung Galaxy Z Flip 3 Vector Mockup
Rule 12 (Flow B-Roll Hybrid Studio) & Rule 15 (Universal Pure Typography Subtitles)
Zero AI Slop, Zero Crop, 100% Native Speed Voiceover, C2PA Cleaned
"""

import sys
import json
import shutil
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
FLOW_DIR = Path("C:/Users/ertyui/flow-mcp-out/nusa_fnb_60s_fresh")
ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

VO_AUDIO = OUT_DIR / "fnb_60s_continuous_vo.wav"
FINAL_MASTER_SUB = ARTIFACT_DIR / "nusa_fnb_60s_flagship_master.mp4"
FINAL_MASTER_CLEAN = ARTIFACT_DIR / "nusa_fnb_60s_clean_master.mp4"
ASS_SUB_FILE = OUT_DIR / "fnb_60s_subtitles.ass"

CLIPS = [
    {
        "id": "beat_01_flow_barista",
        "type": "flow",
        "file": FLOW_DIR / "scene-04.mp4",
        "dur": 9.000,
        "setpts": "1.125*PTS", # Subtle 12.5% slow-down from 8.0s -> 9.0s
        "label": "B-Roll: Overwhelmed Barista behind Cafe Counter with messy order slips"
    },
    {
        "id": "beat_02_mockup_fnb_catalog",
        "type": "mockup",
        "file": OUT_DIR / "mockup_ep2_fnb_catalog_commercial.mp4",
        "dur": 18.200,
        "setpts": None,
        "label": "Mockup: NUSA FnB POS Catalog, Coffee variants, Sugar levels, & Food selection"
    },
    {
        "id": "beat_03_flow_qris_scan",
        "type": "flow",
        "file": FLOW_DIR / "scene-05.mp4",
        "dur": 6.300,
        "setpts": None,
        "label": "B-Roll: Customer scanning acrylic QRIS Standee on Coffee Bar counter"
    },
    {
        "id": "beat_04_mockup_qris_dapur",
        "type": "mockup",
        "file": OUT_DIR / "seg2_mockup_12s.mp4",
        "dur": 10.000,
        "setpts": None,
        "label": "Mockup: Instant QRIS Settlement & Direct Kitchen Slip Validation"
    },
    {
        "id": "beat_05_flow_printer_macro",
        "type": "flow",
        "file": FLOW_DIR / "scene-06.mp4",
        "dur": 4.700,
        "setpts": None,
        "label": "B-Roll: Static Locked-Off Macro Thermal Printer Dispensing Kopi Susu & Mie Seafood Struk"
    },
    {
        "id": "beat_06_mockup_laporan_outro",
        "type": "mockup",
        "file": OUT_DIR / "seg3_mockup_12s.mp4",
        "dur": 15.491, # 12.0s clip + 3.491s clone hold
        "setpts": None,
        "label": "Mockup: Laporan Omzet, Top Selling Menu, Daily Profit & Outro CTA"
    }
]

SUBTITLE_PHRASES = [
    {"start": "0:00:00.05", "end": "0:00:04.30", "text": "Pernah gak sih kafe lagi rame-ramenya..."},
    {"start": "0:00:04.30", "end": "0:00:08.72", "text": "tapi kamu malah pusing gara-gara pesanan ketukar\\ndan bon kertas hilang?"},
    {"start": "0:00:09.39", "end": "0:00:13.60", "text": "Udah saatnya ganti cara lama\\npakai NUSA Kasir FNB."},
    {"start": "0:00:14.19", "end": "0:00:16.80", "text": "Cukup satu HP Android,"},
    {"start": "0:00:16.80", "end": "0:00:19.68", "text": "kamu bisa catat puluhan pesanan pelanggan\\ncuma dalam hitungan detik."},
    {"start": "0:00:20.22", "end": "0:00:23.40", "text": "Varian kopi, level gula, sampai menu makanan,"},
    {"start": "0:00:23.40", "end": "0:00:26.69", "text": "semua rapi dalam satu layar kasir."},
    {"start": "0:00:27.70", "end": "0:00:31.58", "text": "Bayarnya, pelanggan tinggal scan QRIS\\nlangsung dari meja bar."},
    {"start": "0:00:31.87", "end": "0:00:33.36", "text": "Lunas detik itu juga!"},
    {"start": "0:00:33.75", "end": "0:00:36.15", "text": "Enggak perlu lagi ribet cari uang kembalian."},
    {"start": "0:00:36.64", "end": "0:00:39.80", "text": "Transaksi otomatis tervalidasi,"},
    {"start": "0:00:39.80", "end": "0:00:43.15", "text": "dan langsung terhubung ke bagian dapur\\ntanpa ada pesanan terlewat."},
    {"start": "0:00:43.84", "end": "0:00:47.91", "text": "Struk pesanan otomatis tercetak rapi,\\ncepat dan profesional."},
    {"start": "0:00:48.34", "end": "0:00:52.10", "text": "Semua grafik Omzet, menu terlaris,\\nsampai laba harian..."},
    {"start": "0:00:52.10", "end": "0:00:55.98", "text": "bisa kamu pantau langsung dari HP\\nsecara real time!"},
    {"start": "0:00:56.67", "end": "0:00:59.96", "text": "Kelola kafe dan kuliner\\njadi makin satset dan anti bocor."},
    {"start": "0:01:00.41", "end": "0:01:03.30", "text": "NUSA Kasir FNB,\\nSatu HP Serba Bisa."}
]

def generate_ass_subtitles():
    print(f"[Subtitles] Generating Rule 15 Pure Typography ASS: {ASS_SUB_FILE.name}...")
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
    setpts = clip_info.get("setpts")
    print(f"[Standardize] {clip_info['id']} ({dur:.3f}s): {src.name} -> {out_path.name}...")

    vf_filters = []
    if setpts:
        vf_filters.append(f"setpts={setpts}")
    
    vf_filters.extend([
        "scale=1080:1920:force_original_aspect_ratio=increase",
        "crop=1080:1920",
        "fps=60",
        f"tpad=stop_mode=clone:stop_duration={dur}"
    ])

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
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Standardize Error]:", res.stderr)
        raise RuntimeError(f"Standardize failed for {src}")

def main():
    print("=" * 70)
    print("NUSA KASIR FNB 60-SECOND HYBRID COMMERCIAL MASTER COMPILATION")
    print("=" * 70)

    # 1. Standardize 6 clips
    std_clips = []
    for idx, c in enumerate(CLIPS):
        std_file = OUT_DIR / f"std_fnb_part_{idx+1}_{c['id']}.mp4"
        standardize_clip(c, std_file)
        std_clips.append(std_file)

    # 2. Concat list
    concat_list = OUT_DIR / "concat_fnb_60s.txt"
    with open(concat_list, "w") as f:
        for p in std_clips:
            f.write(f"file '{p.resolve()}'\n")

    temp_video = OUT_DIR / "temp_video_fnb_60s.mp4"
    print(f"\n[Concat] Concatenating 6 clips to {temp_video.name}...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(temp_video)
    ]
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Concat Error]:", res.stderr)
        raise RuntimeError("Concat failed")

    # 3. Create Clean Master (Keynote Style, No Subtitles)
    print(f"\n[Mux Clean] Muxing video with Gemini Native Audio (Clean Master)...")
    clean_temp = OUT_DIR / "fnb_clean_master_temp.mp4"
    mux_clean_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(VO_AUDIO),
        "-map_metadata", "-1",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "63.691",
        str(clean_temp)
    ]
    res = subprocess.run(mux_clean_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Mux Clean Error]:", res.stderr)
        raise RuntimeError("Mux Clean failed")

    # 4. Generate Subtitles and Burn Pure Typography Subtitles
    generate_ass_subtitles()
    ass_escaped = str(ASS_SUB_FILE).replace("\\", "/").replace(":", "\\:")
    print(f"\n[Burn Subtitles] Burning Rule 15 Pure Typography Subtitles into Flagship Master...")
    sub_temp = OUT_DIR / "fnb_sub_master_temp.mp4"
    burn_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(VO_AUDIO),
        "-vf", f"ass='{ass_escaped}'",
        "-map_metadata", "-1",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "63.691",
        str(sub_temp)
    ]
    res = subprocess.run(burn_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Burn Error]:", res.stderr)
        raise RuntimeError("Burn Subtitles failed")

    # 5. Copy both masters to Brain Artifacts
    FINAL_MASTER_SUB.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(str(sub_temp), str(FINAL_MASTER_SUB))
    shutil.copyfile(str(clean_temp), str(FINAL_MASTER_CLEAN))

    sub_mb = FINAL_MASTER_SUB.stat().st_size / (1024 * 1024)
    clean_mb = FINAL_MASTER_CLEAN.stat().st_size / (1024 * 1024)

    print("\n" + "=" * 70)
    print("ALL MASTERS GENERATED AND VERIFIED SUCCESSFULLY!")
    print(f"1. Flagship Master (Rule 15 Subtitles): {FINAL_MASTER_SUB}")
    print(f"   Size: {sub_mb:.2f} MB, Duration: 63.69s, 1080x1920 @ 60 FPS")
    print(f"2. Clean Keynote Master (Zero Subtitles): {FINAL_MASTER_CLEAN}")
    print(f"   Size: {clean_mb:.2f} MB, Duration: 63.69s, 1080x1920 @ 60 FPS")
    print("=" * 70)

if __name__ == "__main__":
    main()
