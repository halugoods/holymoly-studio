#!/usr/bin/env python3
"""
Holymoly Studio - Indonesia History 60s Voiceover Synthesis
Generates 6 natural Indonesian narration tracks using id-ID-ArdiNeural
"""

import sys
from pathlib import Path

# Add project root
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from holymoly_studio.engine.tts import synthesize

SCENE_NARRATIONS = [
    (1, "Maret 1942. Di tengah runtuhnya Hindia Belanda, tentara Jepang mendarat di Jawa membawa propaganda Saudara Tua."),
    (2, "Slogan Tiga A bergema di mana-mana. Jepang Cahaya Asia, Pelindung Asia, Pemimpin Asia. Namun harapan segera berganti duka."),
    (3, "Romusha. Jutaan rakyat dipaksa memeras keringat membangun rel kereta maut, menembus belantara tanpa belas kasihan."),
    (4, "Dari tekanan lahirlah perlawanan. Pemuda dilatih militer dalam PETA, yang justru menjadi bara api tentara nasional."),
    (5, "Agustus 1945. Hiroshima dan Nagasaki luluh lantak. Para pemuda bertindak cepat mendesak Bung Karno di Rengasdengklok."),
    (6, "17 Agustus 1945. Di Pegangsaan Timur, teks proklamasi dibacakan. Dari tiga setengah tahun derita, lahirlah Indonesia Merdeka."),
]

AUDIO_OUT_DIR = Path("C:/Users/ertyui/flow-mcp-out/IndonesiaHistory60s/audio")
AUDIO_OUT_DIR.mkdir(parents=True, exist_ok=True)

for num, text in SCENE_NARRATIONS:
    out_file = AUDIO_OUT_DIR / f"narration_scene_{num:02d}.mp3"
    synthesize(text=text, output_path=out_file, voice="id-ID-ArdiNeural", rate="+0%")
    print(f"Generated scene {num} narration -> {out_file}")

print("All 6 historical narrations synthesized successfully!")
