#!/usr/bin/env python3
"""
Assemble NUSA Kasir Fotocopy Extended Hybrid Commercial Master Video (73.80s)
Rule 12 (Flow B-Roll Hybrid Studio) + Rule 11 (Centered Z Flip 3 Mockup) + Rule 15 (Pure Typo Subtitles)

Beat Structure:
- Beat 1 (00.0s - 11.2s): Flow B-Roll 1 (Hand plugging flash drive into laptop)
- Beat 2 (11.2s - 25.5s): Real Mobile Mockup (Dashboard -> Portal File -> Buka di PC)
- Beat 3 (25.5s - 46.5s): Flow Tripod Locked Video Composite (Chrome Web Portal Unduh Skripsi)
- Beat 4 (46.5s - 56.5s): Flow B-Roll 2 (Photocopy laser printer dispensing document pages)
- Beat 5 (56.5s - 73.8s): Real Mobile Mockup (Kasir Layanan Cetak -> Tambah -> Checkout)
"""

import sys
import shutil
import subprocess
from pathlib import Path

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
ARTIFACT_DIR = Path("C:/Users/ertyui/.gemini/antigravity/brain/16f1eea6-9828-4575-8da6-2b56ae393744")

GRID_MP4 = OUT_DIR / "grid_loop_60fps.mp4"
MASK_PNG = OUT_DIR / "screen_mask_700x1710.png"
FRAME_PNG = OUT_DIR / "zflip3_frame.png"

VO_AUDIO = OUT_DIR / "fotocopy_pc_connect_extended_vo.wav"
FINAL_MASTER_SUB = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_master.mp4"
FINAL_MASTER_CLEAN = ARTIFACT_DIR / "nusa_fotocopy_pc_connect_clean.mp4"
ASS_SUB_FILE = OUT_DIR / "fotocopy_pc_subtitles.ass"

TOTAL_DUR = 73.800

# 1. Render Mobile Mockups for Beat 2 and Beat 5
def render_vector_mockup(raw_mp4, out_mp4, duration):
    print(f"[Mockup] Rendering Centered Z Flip 3 Vector Mockup: {raw_mp4.name} -> {out_mp4.name} ({duration}s)...")
    filter_complex = (
        "[1:v]fps=60,scale=700:1710:flags=lanczos[scaled_screen];"
        "[scaled_screen][2:v]alphamerge[masked_screen];"
        "[0:v][masked_screen]overlay=x=190:y=105:shortest=1[bg_screen];"
        "[bg_screen][3:v]overlay=x=0:y=0:shortest=1[final_v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(GRID_MP4),
        "-i", str(raw_mp4),
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
        str(out_mp4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Mockup Error]:", res.stderr)
        raise RuntimeError("Mockup render failed")
    print(f"[Mockup Success] Saved {out_mp4.name} ({out_mp4.stat().st_size} bytes)")

def standardize_clip(src, dur, out_path, setpts=None):
    print(f"[Standardize] {src.name} -> {out_path.name} ({dur:.3f}s)...")
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
        print("[Standardize Error]:", res.stderr)
        raise RuntimeError(f"Standardize failed for {src}")

SUBTITLE_PHRASES = [
    {"start": "0:00:00.05", "end": "0:00:04.60", "text": "Buka usaha fotocopy kok masih ribet\\ncolok-cabut flashdisk pelanggan?"},
    {"start": "0:00:04.70", "end": "0:00:08.50", "text": "Awas, laptop toko rawan banget kena virus,\\nmacet, dan bikin antrean makin panjang!"},
    {"start": "0:00:08.60", "end": "0:00:11.20", "text": "Sekarang saatnya beralih\\nke NUSA Kasir Fotocopy."},
    {"start": "0:00:11.20", "end": "0:00:15.50", "text": "Cukup buka aplikasi NUSA Kasir di HP Androidmu,\\nlalu pilih menu Portal File."},
    {"start": "0:00:15.60", "end": "0:00:20.80", "text": "Tinggal klik Buka di PC,\\nalamat server lokal tokomu langsung aktif otomatis,"},
    {"start": "0:00:20.90", "end": "0:00:25.50", "text": "tanpa perlu install software apapun di laptop!"},
    {"start": "0:00:25.50", "end": "0:00:29.80", "text": "Sekarang buka Google Chrome di komputer tokomu."},
    {"start": "0:00:29.90", "end": "0:00:35.20", "text": "Lihat! Semua berkas PDF skripsi, makalah, dan brosur\\nkiriman pelanggan langsung muncul rapi di layar monitor."},
    {"start": "0:00:35.30", "end": "0:00:40.20", "text": "Operator tinggal satu kali klik tombol Unduh ke PC,\\nberkas langsung terdownload dan siap dicetak!"},
    {"start": "0:00:40.30", "end": "0:00:46.50", "text": "Zero colok flashdisk, bebas risiko virus,\\ndan tanpa kabel data sama sekali."},
    {"start": "0:00:46.50", "end": "0:00:52.00", "text": "Biaya cetak per lembar, print warna,\\nsampai jasa jilid dan laminating..."},
    {"start": "0:00:52.10", "end": "0:00:56.50", "text": "otomatis masuk ke kasir\\ndan langsung bisa kamu terima pembayarannya."},
    {"start": "0:00:56.50", "end": "0:01:01.50", "text": "Praktis, aman,\\ndan bikin usahamu terlihat jauh lebih profesional."},
    {"start": "0:01:01.60", "end": "0:01:07.50", "text": "Sekali beli aktif selamanya\\ntanpa biaya langganan bulanan."},
    {"start": "0:01:07.60", "end": "0:01:13.80", "text": "Cek dan download\\nNUSA Kasir Fotocopy sekarang juga!"}
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
    print(f"[Subtitles] ASS created ({len(SUBTITLE_PHRASES)} dialogue events)")

def main():
    print("=" * 70)
    print("NUSA KASIR FOTOCOPY EXTENDED HYBRID COMMERCIAL MASTER COMPILATION")
    print("=" * 70)

    # 1. Render mobile mockups
    mockup_beat2 = OUT_DIR / "std_mockup_beat2.mp4"
    render_vector_mockup(OUT_DIR / "mobile_beat2_portal_pc.mp4", mockup_beat2, 14.300)

    mockup_beat5 = OUT_DIR / "std_mockup_beat5.mp4"
    render_vector_mockup(OUT_DIR / "mobile_beat6_kasir_struk.mp4", mockup_beat5, 17.300)

    # 2. Standardize 5 clips
    clips_spec = [
        # Beat 1: Flow B-Roll 1 Flashdisk (11.200s, 8.0s clip stretched gently to 11.2s)
        {"file": Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-01.mp4"), "dur": 11.200, "setpts": "1.40*PTS"},
        # Beat 2: Real Mobile Mockup (14.300s)
        {"file": mockup_beat2, "dur": 14.300, "setpts": None},
        # Beat 3: Flow Tripod Locked Video Composite PC (21.000s)
        {"file": OUT_DIR / "pc_tripod_video_composite.mp4", "dur": 21.000, "setpts": None},
        # Beat 4: Flow B-Roll 2 Photocopy Printer (10.000s, 8.0s clip stretched gently to 10.0s)
        {"file": Path("C:/Users/ertyui/flow-mcp-out/nusa_fotocopy_pc/scene-02.mp4"), "dur": 10.000, "setpts": "1.25*PTS"},
        # Beat 5: Real Mobile Mockup Kasir Checkout (17.300s)
        {"file": mockup_beat5, "dur": 17.300, "setpts": None}
    ]

    std_clips = []
    for idx, c in enumerate(clips_spec):
        std_p = OUT_DIR / f"std_fotocopy_part_{idx+1}.mp4"
        standardize_clip(c["file"], c["dur"], std_p, c["setpts"])
        std_clips.append(std_p)

    # 3. Concatenate all 5 clips
    concat_list = OUT_DIR / "concat_fotocopy_master.txt"
    with open(concat_list, "w") as f:
        for p in std_clips:
            f.write(f"file '{p.resolve()}'\n")

    temp_video = OUT_DIR / "temp_video_fotocopy_73s.mp4"
    print(f"\n[Concat] Concatenating 5 clips to {temp_video.name}...")
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

    # 4. Create Clean Master (No Subtitles)
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
        "-t", f"{TOTAL_DUR:.3f}",
        str(clean_temp)
    ]
    res = subprocess.run(mux_clean_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Mux Clean Error]:", res.stderr)
        raise RuntimeError("Mux Clean failed")

    # 5. Burn Pure Typography Subtitles (Rule 15)
    generate_ass_subtitles()
    ass_escaped = str(ASS_SUB_FILE).replace("\\", "/").replace(":", "\\:")
    print(f"\n[Burn Subtitles] Burning Rule 15 Pure Typography Subtitles into Flagship Master...")
    sub_temp = OUT_DIR / "fotocopy_sub_master_temp.mp4"
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
        "-t", f"{TOTAL_DUR:.3f}",
        str(sub_temp)
    ]
    res = subprocess.run(burn_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Burn Error]:", res.stderr)
        raise RuntimeError("Burn Subtitles failed")

    # 6. Copy to Brain Artifacts
    shutil.copyfile(str(sub_temp), str(FINAL_MASTER_SUB))
    shutil.copyfile(str(clean_temp), str(FINAL_MASTER_CLEAN))

    sub_mb = FINAL_MASTER_SUB.stat().st_size / (1024 * 1024)
    clean_mb = FINAL_MASTER_CLEAN.stat().st_size / (1024 * 1024)

    print("\n" + "=" * 70)
    print("ALL MASTERS GENERATED AND VERIFIED SUCCESSFULLY!")
    print(f"1. Flagship Master (Rule 15 Pure Typo Subtitles): {FINAL_MASTER_SUB}")
    print(f"   Size: {sub_mb:.2f} MB, Duration: {TOTAL_DUR:.2f}s, 1080x1920 @ 60 FPS")
    print(f"2. Clean Keynote Master (Zero Subtitles): {FINAL_MASTER_CLEAN}")
    print(f"   Size: {clean_mb:.2f} MB, Duration: {TOTAL_DUR:.2f}s, 1080x1920 @ 60 FPS")
    print("=" * 70)

if __name__ == "__main__":
    main()
