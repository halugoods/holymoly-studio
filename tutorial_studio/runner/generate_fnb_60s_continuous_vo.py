#!/usr/bin/env python3
"""
Generate 60-Second Flagship Continuous Voiceover for NUSA Kasir FnB
One Continuous Take (Zero dead silence injection, natural breathing transitions)
Voice: Puck (gemini-2.5-flash-preview-tts)
"""

import os
import wave
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
VO_FILE = OUT_DIR / "fnb_60s_continuous_vo.wav"

SCRIPT_TEXT = (
    "Pernah nggak sih, kafe lagi rame-ramenya tapi kamu malah pusing gara-gara pesanan ketuker dan bon kertas hilang? "
    "Udah saatnya ganti cara lama pakai NUSA Kasir FnB. "
    "Cukup satu HP Android, kamu bisa catat puluhan pesanan pelanggan cuma dalam hitungan detik. "
    "Varian kopi, level gula, sampai menu makanan siap saji, semua rapi dalam satu layar kasir. "
    "Bayarnya? Pelanggan tinggal scan Kris langsung dari meja bar, lunas detik itu juga. "
    "Nggak perlu lagi ribet cari uang kembalian. "
    "Transaksi otomatis tervalidasi dan langsung terhubung rapi ke bagian dapur tanpa ada pesanan yang terlewat. "
    "Struk pesanan otomatis tercetak rapi, cepat dan profesional. "
    "Dan yang paling tenang, semua grafik omzet, menu terlaris, sampai laba harian bisa kamu pantau langsung dari HP secara realtime. "
    "Kelola kafe dan kuliner jadi makin sat-set dan anti bocor. NUSA Kasir FnB, satu HP serba bisa."
)

PROMPT = (
    "Kamu adalah pemilik dan barista kafe modern Indonesia yang sukses, ramah, artikulatif, dan percaya diri. "
    "Bacakan naskah iklan komersial TV berdurasi 60 detik berikut dengan tempo santai, artikulasi kata sangat jelas, berwibawa, dan hangat. "
    "Beri jeda napas alami antar kalimat tanpa terburu-buru:\n"
    f"{SCRIPT_TEXT}"
)

print("[TTS] Generating 60s continuous voiceover via gemini-2.5-flash-preview-tts (Puck)...")

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
print(f"[TTS] Selesai! Disimpan ke: {VO_FILE}")
print(f"[TTS] Ukuran: {len(raw_pcm)} bytes, Durasi aktual: {duration_sec:.2f} detik")
