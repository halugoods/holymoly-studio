#!/usr/bin/env python3
"""
Generate Clean Metropolitan Accent VO for NUSA Kasir Fotocopy (V7)
Voice: Puck
Target: Non-medhok, dialek Indonesia standar metropolitan Jakarta, renyah, tegas, artikulatif
Khusus kata 'pelanggan': konsonan ganda 'ngg' tebal dan jelas ('pe-lang-gan', zero 'pelangan').
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
VO_FILE = OUT_DIR / "fotocopy_pc_puck_v7_clean.wav"

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
    "Kamu adalah voiceover talent profesional komersial televisi nasional di Jakarta. "
    "Bicaralah dengan dialek bahasa Indonesia standar siaran metropolitan yang bersih, netral, renyah, modern, artikulatif, dan percaya diri. "
    "PENTING: DILARANG menggunakan logat daerah, cengkok, atau aksen medhok sama sekali! "
    "Artikulasikan kata demi kata dengan sangat jelas seperti pembawa acara profesional. "
    "Khusus kata 'pelanggan', ucapkan dengan bunyi konsonan ganda yang mantap dan tegas (pe-lang-gan, bukan pelangan). "
    "Beri jeda napas alami antar kalimat: "
    f"{SCRIPT_TEXT}"
)

print("[TTS] Generating clean metropolitan Puck VO...")
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

dur = len(raw_pcm) / (24000 * 2)
print(f"[TTS Success] Saved {VO_FILE.name} ({len(raw_pcm)} bytes, {dur:.2f}s)")
