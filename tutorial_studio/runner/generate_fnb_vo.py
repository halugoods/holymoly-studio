#!/usr/bin/env python3
"""
Generate Voiceover for NUSA F&B (Resto & Cafe) using Gemini Native Audio TTS
Voice: Aoede (warm, friendly, articulate female barista / cafe owner tone)
"""

import os
import sys
import wave
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
VO_FILE = OUT_DIR / "fnb_catalog_vo.wav"

SCRIPT_TEXT = (
    "Mau menu resto dan cafe kamu tampil makin estetik dan menggugah selera? "
    "Di NUSA F&B, tinggal buka daftar produk dan pilih menu favoritmu. "
    "Ganti foto jadi super gampang berkat katalog Privacy Shield, "
    "bebas pilih puluhan foto makanan HD tanpa perlu akses galeri pribadi HP. "
    "Katalog langsung terupdate seketika, rapi, dan siap dipesan pelanggan!"
)

PROMPT = (
    "Kamu adalah barista dan pemilik cafe modern Indonesia yang ramah, hangat, dan antusias. "
    "Bacakan naskah tutorial fitur katalog menu aplikasi kasir restoran berikut dengan intonasi natural, santai, dan jelas tanpa kesan kaku atau robotik: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO F&B via gemini-2.5-flash-preview-tts (Voice: Aoede)...")

resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
            )
        ),
    ),
)

raw_pcm = resp.candidates[0].content.parts[0].inline_data.data

with wave.open(str(VO_FILE), "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(raw_pcm)

duration_sec = len(raw_pcm) / (24000 * 2)
print(f"[TTS] Berhasil! Disimpan ke: {VO_FILE}")
print(f"[TTS] Ukuran: {len(raw_pcm)} bytes, Durasi aktual: {duration_sec:.2f} detik")
