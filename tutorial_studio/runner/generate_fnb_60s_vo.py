#!/usr/bin/env python3
"""
Generate 60-Second Flagship Voiceover for NUSA Kasir FnB / Kafe
Model: gemini-2.5-flash-preview-tts
Voice: Puck (energetic, friendly, articulate Indonesian cafe owner)
Audio canvas: Exactly 60.00s, 24kHz, 16-bit Mono
Pronunciation: "QRIS" -> "Kris"
"""

import os
import sys
import wave
import struct
import numpy as np
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

OUT_DIR = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
VO_FILE = OUT_DIR / "fnb_60s_vo.wav"

SAMPLE_RATE = 24000
TOTAL_DURATION = 60.0
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

# 6 Story beats aligned with the visual cuts:
# Beat 1 (0.0s - 9.0s): Barista pusing catat manual bon kertas di jam makan siang
# Beat 2 (9.0s - 24.0s): Mockup Z Flip 3 NUSA FnB input menu kopi susu & mie goreng instan
# Beat 3 (24.0s - 30.0s): B-Roll Customer scan QRIS standee di meja bar kafe
# Beat 4 (30.0s - 42.0s): Mockup Bayar QRIS lunas & order terkirim ke dapur
# Beat 5 (42.0s - 48.0s): B-Roll Steady cam thermal printer cetak struk pesanan
# Beat 6 (48.0s - 60.0s): Mockup Laporan Omzet harian realtime & Outro CTA
BEATS = [
    {
        "id": "beat_01_hook",
        "start_sec": 0.5,
        "max_sec": 8.0,
        "text": "Pernah nggak sih, kafe lagi rame-ramenya tapi kamu malah pusing gara-gara pesanan ketuker dan bon kertas hilang?"
    },
    {
        "id": "beat_02_pos",
        "start_sec": 9.5,
        "max_sec": 14.0,
        "text": "Udah saatnya ganti cara lama pakai NUSA Kasir FnB. Cukup satu HP Android, kamu bisa catat puluhan pesanan pelanggan cuma dalam hitungan detik. Varian kopi, level gula, sampai menu makanan, semua rapi di layar kasir."
    },
    {
        "id": "beat_03_customer",
        "start_sec": 24.5,
        "max_sec": 5.0,
        "text": "Bayarnya? Pelanggan tinggal scan Kris langsung dari meja bar, lunas detik itu juga."
    },
    {
        "id": "beat_04_qris_struk",
        "start_sec": 30.5,
        "max_sec": 11.0,
        "text": "Nggak perlu lagi ribet cari uang kembalian. Transaksi otomatis tervalidasi dan langsung terhubung rapi ke bagian dapur tanpa ada pesanan yang terlewat."
    },
    {
        "id": "beat_05_printer",
        "start_sec": 42.5,
        "max_sec": 5.0,
        "text": "Struk pesanan tercetak otomatis, cepat dan profesional."
    },
    {
        "id": "beat_06_laporan",
        "start_sec": 48.5,
        "max_sec": 11.0,
        "text": "Dan yang paling tenang, semua grafik omzet, menu terlaris, sampai laba harian bisa kamu pantau langsung dari HP secara realtime. NUSA Kasir FnB, satu HP serba bisa."
    }
]

def generate_beat_audio(beat):
    print(f"\n[TTS] Generating {beat['id']}: \"{beat['text'][:45]}...\"")
    prompt = f"Bacakan kalimat komersial berikut dengan intonasi santai, ramah, artikulatif, dan percaya diri seorang pemilik kafe modern:\n\"{beat['text']}\""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="audio/x-wav",
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck"
                    )
                )
            )
        )
    )
    
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            audio_bytes = part.inline_data.data
            import io
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                channels = wf.getnchannels()
                sw = wf.getsampwidth()
                rate = wf.getframerate()
                nframes = wf.getnframes()
                raw_frames = wf.readframes(nframes)
                
            samples = np.frombuffer(raw_frames, dtype=np.int16)
            if channels > 1:
                samples = samples[::channels]
            dur = len(samples) / rate
            print(f"      Audio returned: {dur:.2f}s (target max: {beat['max_sec']}s)")
            return samples
            
    raise RuntimeError("No audio data returned from Gemini TTS!")

def main():
    print("=================================================================")
    print(" NUSA KASIR FNB 60S - VOICEOVER GENERATOR (GEMINI TTS PUCK)")
    print("=================================================================")
    print(f"Voice: Puck (Persona: Energetic, friendly Indonesian cafe owner)")
    print(f"Format: {SAMPLE_RATE} Hz, 16-bit Mono, Target: {TOTAL_DURATION}s")
    print(f"Pronunciation Rule: 'QRIS' -> 'Kris'")
    
    full_audio = np.zeros(TOTAL_SAMPLES, dtype=np.int16)
    
    for beat in BEATS:
        samples = generate_beat_audio(beat)
        start_idx = int(beat["start_sec"] * SAMPLE_RATE)
        end_idx = start_idx + len(samples)
        
        if end_idx > TOTAL_SAMPLES:
            print(f"[WARN] Beat {beat['id']} truncated to fit total duration!")
            samples = samples[:TOTAL_SAMPLES - start_idx]
            end_idx = TOTAL_SAMPLES
            
        full_audio[start_idx:end_idx] = samples
        actual_end_sec = end_idx / SAMPLE_RATE
        print(f"      Placed at {beat['start_sec']:.1f}s - {actual_end_sec:.2f}s")
        
    print(f"\n[Saving] Writing master audio to {VO_FILE}...")
    with wave.open(str(VO_FILE), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(full_audio.tobytes())
        
    mb = VO_FILE.stat().st_size / (1024 * 1024)
    print(f"[Done] Master VO created successfully: {VO_FILE} ({mb:.2f} MB, {TOTAL_DURATION:.2f}s)")

if __name__ == "__main__":
    main()
