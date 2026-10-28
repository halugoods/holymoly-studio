#!/usr/bin/env python3
"""
Transcribe fotocopy_pc_connect_60s_vo.wav with timestamps using Gemini 2.5 Flash
"""

import os
import json
from pathlib import Path
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDULUXlOf7iaWmOPxRSGs9lSiSzgLQrEic")
client = genai.Client(api_key=API_KEY)

VO_FILE = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fotocopy_pc_connect_60s_vo.wav")
OUT_JSON = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fotocopy_pc_connect_timestamps.json")

print("[Transcribe] Uploading fotocopy_pc_connect_60s_vo.wav to Gemini...")
uploaded = client.files.upload(file=str(VO_FILE))

prompt = (
    "Transkripsikan audio rekaman komersial NUSA Kasir Fotocopy ini dengan presisi waktu (timestamp start dan end dalam detik). "
    "Kembalikan HANYA format JSON valid tanpa markdown, dengan struktur array of objects:\n"
    "[\n"
    "  {\n"
    "    \"sentence\": \"teks kalimat\",\n"
    "    \"start_sec\": 0.0,\n"
    "    \"end_sec\": 4.5\n"
    "  }\n"
    "]"
)

print("[Transcribe] Analyzing audio timestamps...")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[uploaded, prompt]
)

text = resp.text.strip()
if text.startswith("```json"):
    text = text[7:]
elif text.startswith("```"):
    text = text[3:]
if text.endswith("```"):
    text = text[:-3]
text = text.strip()

data = json.loads(text)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"[Transcribe] Berhasil disimpan ke: {OUT_JSON}")
for item in data:
    print(f"  [{item['start_sec']:.2f}s - {item['end_sec']:.2f}s] {item['sentence']}")
