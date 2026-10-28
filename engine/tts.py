#!/usr/bin/env python3
"""
Holymoly Studio - Indonesian Neural TTS Audio Engine
(by Halu Goods Indonesia)

Generates studio-grade natural Indonesian voiceovers using Microsoft Neural TTS:
- 'id-ID-ArdiNeural' (Male, friendly & authoritative)
- 'id-ID-GadisNeural' (Female, warm & expressive)

100% Free, zero credits, instant local MP3 generation.
"""

import asyncio
from pathlib import Path
import edge_tts


async def _synthesize_async(
    text: str,
    output_path: str | Path,
    voice: str = "id-ID-ArdiNeural",
    rate: str = "+0%",
    pitch: str = "+0Hz",
) -> Path:
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(str(out))
    return out


def synthesize(
    text: str,
    output_path: str | Path,
    voice: str = "id-ID-ArdiNeural",
    rate: str = "+0%",
    pitch: str = "+0Hz",
) -> Path:
    """
    Synchronous wrapper for speech synthesis.
    """
    return asyncio.run(_synthesize_async(text, output_path, voice, rate, pitch))


if __name__ == "__main__":
    out = synthesize(
        "Halo! Ini adalah uji coba suara resmi Holymoly Studio Halu Goods Indonesia.",
        "C:/Users/ertyui/ZCodeProject/holymoly_studio/assets/test_synth.mp3",
    )
    print(f"Generated TTS to: {out}")
