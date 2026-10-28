#!/usr/bin/env python3
"""
Generate Voiceover for NUSA Bengkel using Gemini Native Audio TTS
Voice: Fenrir (deep, solid, reliable Indonesian automotive workshop owner persona)
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
VO_FILE = OUT_DIR / "bengkel_servis_vo.wav"

SCRIPT_TEXT = (
    "Kelola bengkel motor dan mobil jadi jauh lebih rapi dengan NUSA Bengkel! "
    "Tinggal pilih jasa servis berkala, tambahkan sparepart dan oli mesin langsung dalam satu transaksi. "
    "Total tagihan dan hitungan uang kembalian otomatis akurat. "
    "Struk servis digital langsung jadi, siap cetak printer thermal atau kirim ke WhatsApp pelanggan!"
)

PROMPT = (
    "Kamu adalah pemilik bengkel motor dan mobil modern di Indonesia yang terpercaya, solid, dan profesional. "
    "Bacakan naskah tutorial fitur kasir bengkel, kombinasi jasa servis dan sparepart berikut dengan intonasi mantap, ramah, dan artikulasi jelas tanpa kesan kaku: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO Bengkel via gemini-2.5-flash-preview-tts (Voice: Fenrir)...")

resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Fenrir")
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
