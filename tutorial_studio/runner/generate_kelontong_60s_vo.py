#!/usr/bin/env python3
"""
Generate 60-Second Flagship Voiceover for NUSA Kasir Kelontong
Model: gemini-2.5-flash-preview-tts
Voice: Puck (energetic, friendly, articulate UMKM owner persona matching ep7_fotocopy_cetak_commercial)
Synchronization: Word-anchored per-beat positioning on 60.00s canvas
Phonetics: "QRIS" is rendered as "Kris" for natural Indonesian pronunciation
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
VO_FILE = OUT_DIR / "kelontong_60s_vo.wav"

SAMPLE_RATE = 24000
TOTAL_DURATION = 60.0  # seconds
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

# 6 Clean beats precisely timed to visual cuts
# Visual cuts:
# Beat 1: 0.0s - 9.0s (Warung & buku manual)
# Beat 2: 9.0s - 24.0s (Mockup POS Kasir)
# Beat 3: 24.0s - 30.0s (B-Roll Customer scan QRIS standee)
# Beat 4: 30.0s - 42.0s (Mockup QRIS & Struk belanja)
# Beat 5: 42.0s - 48.0s (B-Roll Thermal printer struk)
# Beat 6: 48.0s - 60.0s (Mockup Laporan Penjualan)
BEATS = [
    {
        "id": "beat_01_hook",
        "start_sec": 0.5,
        "max_sec": 8.0,
        "text": "Punya warung kelontong yang ramai itu berkah, tapi kalau catat transaksi masih manual di buku, bisa bikin pusing tiap tutup toko."
    },
    {
        "id": "beat_02_pos",
        "start_sec": 9.5,
        "max_sec": 14.0,
        "text": "Dengan NUSA Kasir, semua barang tinggal tap. Mau cari beras, minyak goreng, sampai bumbu dapur, kategorinya rapi dan total belanja langsung terhitung otomatis tanpa ribet kalkulator."
    },
    {
        "id": "beat_03_customer",
        "start_sec": 24.5,
        "max_sec": 5.0,
        "text": "Pelanggan mau bayar nontunai? Tenang, langsung siapin Kris dalam hitungan detik."
    },
    {
        "id": "beat_04_qris_struk",
        "start_sec": 30.5,
        "max_sec": 11.0,
        "text": "Tinggal pilih metode Kris, kodenya langsung muncul di layar. Begitu pelanggan scan dan bayar, transaksi otomatis tercatat lunas dan struk belanja langsung siap dicetak."
    },
    {
        "id": "beat_05_printer",
        "start_sec": 42.5,
        "max_sec": 5.0,
        "text": "Struk rapi keluar seketika, pelanggan puas dan percaya dengan transparansi belanja di tokomu."
    },
    {
        "id": "beat_06_laporan_outro",
        "start_sec": 48.5,
        "max_sec": 10.5,
        "text": "Laporan penjualan dan laba rugi pun langsung rekap otomatis tiap hari. NUSA Kasir, kasir pintar serba bisa untuk UMKM Indonesia."
    }
]

PERSONA_PROMPT_PREFIX = (
    "Kamu adalah pemilik usaha toko kelontong modern di Indonesia yang cekatan, ramah, dan energik. "
    "Bacakan kalimat tutorial fitur kasir toko kelontong berikut dengan intonasi lincah, mantap, dan artikulasi jelas tanpa kesan kaku: "
)

def generate_beat_audio(beat):
    prompt = f"{PERSONA_PROMPT_PREFIX}{beat['text']}"
    print(f"\n[TTS] Generating {beat['id']} (start={beat['start_sec']}s)...")
    print(f"      Text: \"{beat['text']}\"")
    
    resp = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=prompt,
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
    # 24000 Hz, 16-bit mono = 2 bytes per sample
    samples = np.frombuffer(raw_pcm, dtype=np.int16)
    dur = len(samples) / SAMPLE_RATE
    print(f"      -> Got {len(samples)} samples ({dur:.2f}s, max allowed: {beat['max_sec']}s)")
    return samples

def main():
    print("=================================================================")
    print(" NUSA KASIR KELONTONG 60S - VOICEOVER GENERATOR (GEMINI TTS PUCK)")
    print("=================================================================")
    print(f"Voice: Puck (Persona: Energetic, modern Indonesian shop owner)")
    print(f"Format: {SAMPLE_RATE} Hz, 16-bit Mono, Target: {TOTAL_DURATION}s")
    print(f"Pronunciation Rule: 'QRIS' -> 'Kris'")
    
    # Initialize 60s silent buffer
    full_audio = np.zeros(TOTAL_SAMPLES, dtype=np.int16)
    
    for beat in BEATS:
        samples = generate_beat_audio(beat)
        
        start_idx = int(beat["start_sec"] * SAMPLE_RATE)
        end_idx = start_idx + len(samples)
        
        # Guard against overflow beyond canvas
        if end_idx > TOTAL_SAMPLES:
            print(f"[WARN] Beat {beat['id']} truncated to fit total duration!")
            samples = samples[:TOTAL_SAMPLES - start_idx]
            end_idx = TOTAL_SAMPLES
            
        full_audio[start_idx:end_idx] = samples
        actual_end_sec = end_idx / SAMPLE_RATE
        print(f"      Placed at {beat['start_sec']:.1f}s - {actual_end_sec:.2f}s")
        
    # Write composite 60-second WAV file
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
