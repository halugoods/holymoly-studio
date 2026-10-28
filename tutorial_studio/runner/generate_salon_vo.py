#!/usr/bin/env python3
"""
Generate Voiceover for NUSA Salon using Gemini Native Audio TTS
Voice: Aoede (stylish, warm, confident salon & beauty specialist persona)
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
VO_FILE = OUT_DIR / "salon_treatment_vo.wav"

SCRIPT_TEXT = (
    "Bikin bisnis salon dan barbershop kamu naik kelas dengan NUSA Salon! "
    "Gabungkan paket potong rambut, cuci blow styling, dan produk vitamin rambut dalam satu kasir fleksibel. "
    "Dukung reservasi jadwal stylist, hitung tagihan otomatis, "
    "dan struk elegan langsung siap dikirim ke WhatsApp pelanggan!"
)

PROMPT = (
    "Kamu adalah pemilik studio salon kecantikan dan barbershop modern di Indonesia yang modis, percaya diri, dan ramah. "
    "Bacakan naskah tutorial fitur kasir salon, kombinasi treatment dan retail produk berikut dengan intonasi anggun, energik, dan artikulasi jelas tanpa kesan kaku: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO Salon via gemini-2.5-flash-preview-tts (Voice: Aoede)...")

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
