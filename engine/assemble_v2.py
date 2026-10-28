#!/usr/bin/env python3
"""
Holymoly Studio - Assembler & Subtitle & Metadata Cleaner Pipeline v2
(by Halu Goods Indonesia)
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from holymoly_studio.engine.flow_client import request_api
from holymoly_studio.engine.cleaner import clean_mp4_binary

PROJECT = "SejarahJepangV2"
CLIPS_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60sVideo")
AUDIO_DIR = Path("C:/Users/ertyui/flow-mcp-out/SejarahJepangV2")
OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/output_clean")

CLIPS = [
    str(CLIPS_DIR / "scene-07.mp4"),
    str(CLIPS_DIR / "scene-08.mp4"),
    str(CLIPS_DIR / "scene-09.mp4"),
    str(CLIPS_DIR / "scene-10.mp4"),
    str(CLIPS_DIR / "scene-13.mp4"),
    str(CLIPS_DIR / "scene-12.mp4"),
]


def assemble_v2():
    print("[Holymoly Studio v2] Assembling Master Video with 2-Way Dialogue...")

    # 1. Check audio files
    audio_files = sorted(list(AUDIO_DIR.glob("narration-*.m4a")))
    print(f"Found {len(audio_files)} narration takes.")

    # 2. Concat audio takes or build voice track
    # We can use ffmpeg to merge speech into one continuous track
    combined_audio = AUDIO_DIR / "dialogue_master.wav"
    filter_complex = []
    inputs = []
    for idx, af in enumerate(audio_files):
        inputs.extend(["-i", str(af)])
    
    # Simple concat filter for audio
    concat_filter = f"".join([f"[{i}:a]" for i in range(len(audio_files))]) + f"concat=n={len(audio_files)}:v=0:a=1[outa]"
    cmd_audio = ["ffmpeg", "-y"] + inputs + ["-filter_complex", concat_filter, "-map", "[outa]", str(combined_audio)]
    print("Combining audio takes...")
    subprocess.run(cmd_audio, check=True)

    assembled_video = str(AUDIO_DIR / "sejarah_jepang_v2_assembled.mp4")
    if not Path(assembled_video).exists() or Path(assembled_video).stat().st_size == 0:
        print("[Holymoly Studio v2] Calling flow_assemble...")
        res_assemble = request_api("assemble", {
            "project": PROJECT,
            "clips": CLIPS,
            "voiceover": str(combined_audio.resolve()),
            "clip_volume": 0.2,
            "music_volume": 0.2,
            "hold_last_frame": True,
            "output_name": "sejarah_jepang_v2_assembled"
        })
        assembled_video = res_assemble.get("output")
    print(f"  -> Assembled Video: {assembled_video}")

    # 4. Transcribe with Whisper CLI
    print("[Holymoly Studio v2] Transcribing with Whisper (id language)...")
    res_transcribe = request_api("transcribe", {
        "video": assembled_video,
        "language": "id",
        "words": True
    })
    print(f"  -> Transcribed words: {len(res_transcribe.get('words', []))}")

    # 5. Burn Kinetic Bold Pop Subtitles
    print("[Holymoly Studio v2] Burning Bold Pop subtitles (#FFE135)...")
    res_captions = request_api("captions", {
        "video": assembled_video,
        "style": "bold",
        "color": "#FFE135",
        "position": "bottom",
        "size": "medium",
        "letters": "capitals"
    })
    captioned_video = res_captions.get("output")
    print(f"  -> Captioned Video: {captioned_video}")

    # 6. Metadata & C2PA Cleaning
    final_output = OUT_DIR / "sejarah_jepang_v2_final_clean.mp4"
    print(f"[Holymoly Studio v2] Stripping C2PA and normalizing brand to {final_output}...")
    clean_stats = clean_mp4_binary(captioned_video, str(final_output))
    print(f"  -> Cleaned Output Stats: {clean_stats}")
    print("[Holymoly Studio v2] SUCCESS! Benchmark Video v2 Completed!")
    return str(final_output)


if __name__ == "__main__":
    assemble_v2()
