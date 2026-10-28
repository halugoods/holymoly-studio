#!/usr/bin/env python3
"""
Generate and Test Female Voiceover (Aoede) for NUSA Kasir Fotocopy
Voice: Aoede (Female, stylish, warm, professional broadcast talent like ep6 salon)
"""

import os
import sys
import wave
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fresh_v4")
OUT_DIR.mkdir(parents=True, exist_ok=True)
VO_FILE = OUT_DIR / "fotocopy_pc_aoede_raw.wav"

SCRIPT_TEXT = (
    "Buka usaha fotocopy kok masih ribet colok-cabut flashdisk pelanggan? "
    "Awas, laptop toko rawan kena virus! "
    "Solusinya, pakai NUSA Kasir Fotocopy! "
    "Cukup buka menu Portal File dari HP tokomu, lalu klik Buka di PC. "
    "Alamat server lokal langsung aktif tanpa kabel dan tanpa install software apapun! "
    "Sekarang buka Google Chrome di komputer tokomu. "
    "Semua berkas antrean pelanggan langsung masuk otomatis di monitor PC! "
    "Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi langsung tersimpan dan siap diprint. "
    "Zero kabel data, zero colok flashdisk! "
    "Hasil cetak langsung keluar dari mesin percetakanmu dengan cepat dan aman. "
    "Biaya print per lembar, cetak warna, sampai jasa jilid otomatis terhitung rapi di kasir! "
    "Praktis banget kan? "
    "NUSA Kasir Fotocopy, sekali beli aktif selamanya tanpa biaya bulanan. "
    "Download sekarang juga!"
)

PROMPT = (
    "Kamu adalah voiceover talent wanita profesional untuk iklan komersial televisi dan video tutorial di Jakarta, "
    "seperti pembawa acara yang modern, ramah, energik, anggun, dan terpercaya. "
    "Bicaralah dengan dialek bahasa Indonesia standar siaran metropolitan yang bersih, tanpa logat daerah (non-medhok), "
    "tempo santai dan mengalir, artikulasi jelas dan hidup. "
    "PENTING: Kata 'pelanggan' wajib dilafalkan secara sempurna dengan bunyi 'ngg' yang tegas dan mantap (pe-lang-gan, bukan pelangan). "
    "Kata 'QRIS' jika ada dilafalkan 'Kris'. "
    "Bacakan naskah komersial NUSA Kasir Fotocopy berikut dengan penuh keyakinan dan keramahan alami: "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Generating Female VO via gemini-2.5-flash-preview-tts (Voice: Aoede)...")

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
print(f"[TTS] Success! Saved to: {VO_FILE}")
print(f"[TTS] Size: {len(raw_pcm)} bytes, Duration: {duration_sec:.2f}s")
