#!/usr/bin/env python3
"""
Holymoly Studio - Produksi Narasi & Dialog 2-Arah Sejarah v2
(by Halu Goods Indonesia)

Menggunakan Gemini Native Audio TTS (flow_narrate) dengan 2 karakter suara:
- Charon (Bung Karno / Narator Dokumenter Berat)
- Puck (Chaerul Saleh / Pemuda PETA Menggebu-gebu)
"""

import json
import sys
import time
from pathlib import Path

# Add root project to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from holymoly_studio.engine.flow_client import request_api

PROJECT = "SejarahJepangV2"

SCRIPT = [
    {
        "id": "scene_01",
        "voice": "Charon",
        "style": "slowly, grave and cinematic, like a grand historic documentary narrator",
        "text": "Maret sembilan belas empat puluh dua. Deru kapal perang Dai Nippon merapat ke Batavia, menjanjikan saudara tua yang membebaskan Nusantara.",
    },
    {
        "id": "scene_02",
        "voice": "Charon",
        "style": "cold and dramatic, recounting harsh betrayal",
        "text": "Namun janji luruh jadi abu. Semboyan Tiga A berubah jadi rampasan paksa. Lumbung desa dikuras habis demi logistik perang Asia Timur Raya.",
    },
    {
        "id": "scene_03",
        "voice": "Charon",
        "style": "deep emotional sorrow and raw human pain, whispered gravity",
        "text": "Ratusan ribu rakyat dipaksa jadi Romusha. Bertelanjang kaki menebas rimba belantara, mengorbankan nyawa demi bantalan rel maut.",
    },
    {
        "id": "scene_04",
        "voice": "Puck",
        "style": "fierce, passionate, heroic battle cry of a young freedom fighter",
        "text": "Dari penindasan itu, bara PETA menyala! Di Blitar, Sudanco Supriyadi mengangkat senjata melawan kezaliman perwira Jepang!",
    },
    {
        "id": "scene_05a_dialog_pemuda",
        "voice": "Puck",
        "style": "intense urgent whispered confrontation, breathless young revolutionary",
        "text": "Bung Karno! Dai Nippon sudah hancur. Ribuan pemuda sudah siap di luar, proklamirkan kemerdekaan sekarang juga!",
    },
    {
        "id": "scene_05b_dialog_soekarno",
        "voice": "Charon",
        "style": "deep commanding voice of Bung Karno, firm and visionary authority",
        "text": "Revolusi ini milik seluruh rakyat, Chaerul! Kita putuskan nasib bangsa ini dengan martabat kita sendiri!",
    },
    {
        "id": "scene_06",
        "voice": "Charon",
        "style": "triumphant, solemn, goosebumps inducing historic victory",
        "text": "Tujuh belas Agustus sembilan belas empat puluh lima. Di Pegangsaan Timur, Sang Saka Merah Putih berkibar tegak. Indonesia merdeka!",
    },
]


def produce_all_lines():
    print(f"[Holymoly Studio v2] Starting TTS Generation for {PROJECT}...")
    results = {}

    for item in SCRIPT:
        print(f"Generating line {item['id']} ({item['voice']})...")
        res = request_api(
            "narrate",
            {
                "project": PROJECT,
                "text": item["text"],
                "voice": item["voice"],
                "engine": "gemini",
                "style": item["style"],
            },
        )
        results[item["id"]] = {
            "output": res.get("output"),
            "duration": res.get("duration"),
            "voice": item["voice"],
            "text": item["text"],
        }
        print(f"  -> Finished: {res.get('output')} ({res.get('duration')}s)")
        time.sleep(1)

    out_json = Path(f"C:/Users/ertyui/flow-mcp-out/{PROJECT}/lines_metadata.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[Holymoly Studio v2] All lines saved to: {out_json}")


if __name__ == "__main__":
    produce_all_lines()
