#!/usr/bin/env python3
"""
Generate Pilot Voiceover for NUSA Kasir Kelontong using Gemini Native Audio TTS
Voice: Puck (energetic, friendly, creator tone)
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
VO_FILE = OUT_DIR / "pilot_kelontong_vo.wav"

SCRIPT_TEXT = (
    "Jualan kelontong jadi jauh lebih sat-set! "
    "Tinggal pilih barang belanjaan beras dan minyak goreng, "
    "lalu klik bayar dan pilih QRIS kasir otomatis. "
    "QR code langsung muncul seketika dengan nominal pas. "
    "Begitu pelanggan bayar, status lunas otomatis dan struk belanja langsung jadi!"
)

PROMPT = (
    "Kamu adalah konten kreator UMKM Indonesia yang energik, ramah, dan luwes. "
    "Bacakan naskah tutorial aplikasi kasir kelontong berikut dengan intonasi natural, santai, dan jelas tanpa terdengar seperti robot: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO natural via gemini-2.5-flash-preview-tts (Voice: Puck)...")

resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
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
