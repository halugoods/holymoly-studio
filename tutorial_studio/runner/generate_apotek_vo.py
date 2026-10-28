#!/usr/bin/env python3
"""
Generate Voiceover for NUSA Apotek using Gemini Native Audio TTS
Voice: Kore (caring, calm, articulate Indonesian pharmacist / apoteker persona)
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
VO_FILE = OUT_DIR / "apotek_farmasi_vo.wav"

SCRIPT_TEXT = (
    "Transaksi farmasi dan apotek jadi jauh lebih cepat dan teratur dengan NUSA Apotek! "
    "Tinggal pilih obat bebas, vitamin, atau produk kesehatan dalam satu keranjang rapi. "
    "Total belanja dan uang kembalian terhitung otomatis tanpa repot kalkulator. "
    "Struk transaksi apotek digital langsung siap dicetak atau dikirim ke WhatsApp pasien!"
)

PROMPT = (
    "Kamu adalah apoteker dan pemilik farmasi modern di Indonesia yang ramah, cermat, dan profesional. "
    "Bacakan naskah tutorial fitur kasir apotek dan manajemen obat berikut dengan intonasi hangat, tenang, dan artikulasi jelas tanpa kesan kaku: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO Apotek via gemini-2.5-flash-preview-tts (Voice: Kore)...")

resp = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=PROMPT,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
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
