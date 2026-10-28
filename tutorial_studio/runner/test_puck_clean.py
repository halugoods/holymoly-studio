import os
import wave
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

text = (
    "Buka usaha fotocopy kok masih ribet colok-cabut flashdisk pelanggan? "
    "Semua berkas antrean pelanggan langsung masuk otomatis di monitor PC!"
)

prompt = (
    "Kamu adalah voiceover profesional iklan televisi nasional di Jakarta. "
    "Bicaralah dengan bahasa Indonesia baku siaran metropolitan yang bersih, netral, renyah, modern, dan percaya diri. "
    "Sama sekali jangan gunakan logat daerah, cengkok, atau aksen medhok. "
    "Artikulasi setiap kata dengan presisi tinggi. Khususnya kata 'pelanggan', lafalkan secara sempurna dengan bunyi 'ngg' yang mantap dan tegas (pe-lang-gan, bukan pelangan): "
    f"{text}"
)

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

raw = resp.candidates[0].content.parts[0].inline_data.data
out_p = r"C:\Users\ertyui\ZCodeProject\holymoly_studio\tutorial_studio\output\fresh_v4\test_puck_clean_acc.wav"
with wave.open(out_p, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(raw)
print("Generated test_puck_clean_acc.wav:", len(raw), "bytes")
