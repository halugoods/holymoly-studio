#!/usr/bin/env python3
"""
Holymoly Studio - Gemini Native Audio TTS Synthesis
Generates 6 natural Indonesian narration tracks for IndonesiaHistory60s
using model 'gemini-2.5-flash-preview-tts' (Voice: Charon / Puck)
"""

import os
import sys
import time
import wave
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic"
client = genai.Client(api_key=API_KEY)

AUDIO_OUT_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60s/gemini_audio")
AUDIO_OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    (1, "Maret 1942. Di tengah runtuhnya Hindia Belanda, armada tentara Jepang mendarat di Jawa membawa propaganda Saudara Tua."),
    (2, "Slogan Tiga A bergema di mana-mana. Jepang Cahaya Asia, Pelindung Asia, Pemimpin Asia. Namun harapan segera berganti duka."),
    (3, "Romusha. Beras disita, jutaan rakyat dipaksa memeras keringat menembus hutan rimba membangun jalur rel kereta maut."),
    (4, "Dari tekanan lahirlah perlawanan. Pemuda dilatih militer dalam PETA, yang justru menjadi bara api tentara nasional."),
    (5, "Agustus 1945. Bom atom meluluhlantakkan Hiroshima dan Nagasaki. Para pemuda bertindak cepat mendesak Bung Karno di Rengasdengklok."),
    (6, "17 Agustus 1945. Di Pegangsaan Timur, teks proklamasi dibacakan. Dari tiga setengah tahun derita, lahirlah Indonesia Merdeka."),
]

VOICE_NAME = "Charon"  # Dignified, informative documentary narrator

print(f"=== Synthesizing 6 Scenes with Gemini Native Audio ({VOICE_NAME}) ===")

for num, text in SCENES:
    out_file = AUDIO_OUT_DIR / f"scene_{num:02d}.wav"
    prompt = f"Bacakan naskah dokumenter sejarah berikut dengan intonasi tenang, berwibawa, jernih, dan mendalam: {text}"

    print(f"Synthesizing Scene {num}...")
    success = False
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
                        )
                    ),
                ),
            )
            raw_pcm = resp.candidates[0].content.parts[0].inline_data.data
            with wave.open(str(out_file), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(raw_pcm)

            print(f"  -> Saved {out_file.name} ({len(raw_pcm)} bytes, ~{len(raw_pcm)/48000:.1f}s)")
            success = True
            break
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    if not success:
        raise RuntimeError(f"Failed to generate audio for Scene {num}")

print("\nAll 6 Gemini Native Audio narration tracks synthesized successfully!")
