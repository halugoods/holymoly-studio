#!/usr/bin/env python3
"""
Generate Voiceover for NUSA Fotocopy Commercial V3
Model: gemini-2.5-flash-preview-tts (Voice: Charon, 1.0x native speed)
"""

import os
import wave
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
VO_FILE = OUT_DIR / "fotocopy_pc_connect_v3_vo.wav"

SCRIPT_TEXT = (
    "Buka usaha fotocopy kok masih ribet colok-cabut flashdisk pelanggan? "
    "Awas, laptop toko rawan kena virus! "
    "Solusinya, pakai NUSA Kasir Fotocopy! "
    "Cukup buka menu Portal File dari HP tokomu, lalu klik Buka di PC. "
    "Alamat server lokal langsung aktif tanpa perlu kabel dan tanpa install software apapun! "
    "Sekarang buka Google Chrome di komputer tokomu. "
    "Semua berkas antrean pelanggan langsung masuk otomatis di monitor PC! "
    "Tinggal satu kali klik Unduh ke PC, dokumen PDF skripsi langsung tersimpan dan siap diprint. "
    "Zero kabel data, zero colok flashdisk! "
    "Hasil cetak langsung keluar dari mesin percetakanmu dengan cepat dan aman. "
    "Biaya print per lembar, cetak warna, sampai jasa jilid otomatis terhitung rapi di kasir! "
    "Praktis banget kan? NUSA Kasir Fotocopy, sekali beli aktif selamanya tanpa biaya bulanan. "
    "Download sekarang juga!"
)

PROMPT = (
    "Kamu adalah pemilik usaha fotocopy dan percetakan modern di Indonesia yang cekatan, ramah, artikulatif, dan percaya diri. "
    "Bacakan naskah komersial fitur Sambungkan ke Komputer berikut dengan tempo santai, artikulasi kata sangat jelas, berwibawa, dan hangat. "
    "Beri jeda napas alami antar kalimat tanpa terburu-buru, dan jangan mengeja singkatan seperti kata 'Kris' atau 'PC': "
    f"{SCRIPT_TEXT}"
)

print("[TTS] Generating Voiceover V3 via gemini-2.5-flash-preview-tts...")
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
print(f"[TTS] Berhasil! Disimpan ke: {VO_FILE.name}")
print(f"[TTS] Ukuran: {len(raw_pcm)} bytes, Durasi aktual: {duration_sec:.2f} detik")
