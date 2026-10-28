#!/usr/bin/env python3
"""
Generate Extended Voiceover for NUSA Fotocopy 'Sambungkan ke Komputer' Commercial
Voice: Charon (Authoritative, energetic, warm Indonesian copy center owner persona)
Model: gemini-2.5-flash-preview-tts (1.0x native speed, continuous take)
Duration target: ~70 - 75 seconds
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
VO_FILE = OUT_DIR / "fotocopy_pc_connect_extended_vo.wav"

SCRIPT_TEXT = (
    "Buka usaha fotocopy kok masih ribet colok-cabut flashdisk pelanggan? "
    "Awas, laptop toko rawan banget kena virus, macet, dan bikin antrean makin panjang! "
    "Sekarang saatnya beralih ke NUSA Kasir Fotocopy. "
    "Cukup buka aplikasi NUSA Kasir di HP Androidmu, lalu pilih menu Portal File. "
    "Tinggal klik Buka di PC, alamat server lokal tokomu langsung aktif otomatis tanpa perlu install software apapun di laptop! "
    "Sekarang buka Google Chrome di komputer tokomu. "
    "Lihat! Semua berkas PDF skripsi, makalah, dan brosur kiriman pelanggan langsung muncul rapi di layar monitor. "
    "Operator tinggal satu kali klik tombol Unduh ke PC, berkas langsung terdownload dan siap dicetak ke mesin fotocopy! "
    "Zero colok flashdisk, bebas risiko virus, dan tanpa kabel data sama sekali. "
    "Biaya cetak per lembar, print warna, sampai jasa jilid dan laminating otomatis masuk ke kasir dan langsung bisa kamu terima pembayarannya. "
    "Praktis, aman, dan bikin usahamu terlihat jauh lebih profesional. "
    "Sekali beli aktif selamanya tanpa biaya langganan bulanan. "
    "Cek dan download NUSA Kasir Fotocopy sekarang juga!"
)

PROMPT = (
    "Kamu adalah pemilik usaha fotocopy dan percetakan modern di Indonesia yang cekatan, ramah, artikulatif, dan percaya diri. "
    "Bacakan naskah komersial fitur Sambungkan ke Komputer berikut dengan tempo santai, artikulasi kata sangat jelas, berwibawa, dan hangat. "
    "Beri jeda napas alami antar kalimat tanpa terburu-buru, dan jangan mengeja singkatan seperti kata 'Kris' atau 'PC': "
    f"{SCRIPT_TEXT}"
)

print(f"[TTS] Menghasilkan audio VO Extended Fotocopy PC Connect via gemini-2.5-flash-preview-tts (Voice: Charon)...")

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
