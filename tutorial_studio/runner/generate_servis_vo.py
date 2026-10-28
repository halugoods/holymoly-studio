#!/usr/bin/env python3
"""
Generate Voiceover for NUSA Servis using Gemini Native Audio TTS
Voice: Charon (trustworthy, calm, articulate electronics technician persona)
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
VO_FILE = OUT_DIR / "servis_gadget_vo.wav"

SCRIPT_TEXT = (
    "Kelola konter servis HP, laptop, dan elektronik jadi jauh lebih profesional dengan NUSA Servis! "
    "Catat jasa perbaikan, pasang sparepart baru, dan aksesoris dalam satu nota terintegrasi. "
    "Hitung tagihan transparan, bebas ribet hitung manual, "
    "dan struk tanda terima servis langsung siap dikirim ke WhatsApp pelanggan!"
)

PROMPT = (
    "Kamu adalah teknisi dan pemilik konter servis smartphone dan gadget modern di Indonesia yang terpercaya, teliti, dan solutif. "
    "Bacakan naskah tutorial fitur kasir servis elektronik, kombinasi jasa perbaikan dan sparepart berikut dengan intonasi meyakinkan, tenang, dan artikulasi jelas: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO Servis via gemini-2.5-flash-preview-tts (Voice: Charon)...")

resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Charon")
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
