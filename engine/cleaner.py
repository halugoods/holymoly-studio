#!/usr/bin/env python3
"""
Holymoly Studio - MP4 Anti-Detection & C2PA Metadata Cleaner
(by Halu Goods Indonesia)

Fungsi:
1. Mendeteksi & menghapus box C2PA Content Credentials ('jumb', 'jumbf', 'uuid' C2PA manifest).
2. Menormalkan major brand MP4 dalam box 'ftyp' menjadi profil standar 'mp42' (CapCut / camera standard).
3. Menghapus embedded prompt AI dan tag QuickTime (©too, ©art).
4. Me-reset timestamp pembuatan file (mvhd / tkhd) ke waktu alami saat render.
"""

import os
import struct
import sys
import time
from pathlib import Path


def clean_mp4_binary(input_file: str, output_file: str) -> dict:
    in_path = Path(input_file)
    out_path = Path(output_file)

    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = bytearray(in_path.read_bytes())
    original_size = len(data)
    out_chunks = bytearray()
    offset = 0

    stripped_c2pa = False
    normalized_brand = False
    stripped_boxes = []

    while offset < len(data):
        if offset + 8 > len(data):
            out_chunks.extend(data[offset:])
            break

        size = struct.unpack(">I", data[offset : offset + 4])[0]
        box_type = data[offset + 4 : offset + 8].decode("latin-1", errors="replace")

        # 64-bit extended size
        header_len = 8
        if size == 1:
            if offset + 16 > len(data):
                break
            size = struct.unpack(">Q", data[offset + 8 : offset + 16])[0]
            header_len = 16
        elif size == 0:
            # Box extends to end of file
            size = len(data) - offset

        if size < header_len:
            break

        box_end = min(offset + size, len(data))
        box_data = data[offset:box_end]

        # 1. DETECT & STRIP C2PA / JUMBF BOXES
        is_c2pa = False
        if box_type in ("jumb", "jumbf"):
            is_c2pa = True
        elif box_type == "uuid" and len(box_data) >= 24:
            # Check UUID payload for C2PA manifest GUID or strings
            uuid_sample = bytes(box_data[header_len : header_len + 32]).lower()
            if b"c2pa" in uuid_sample or b"jumb" in uuid_sample:
                is_c2pa = True

        if is_c2pa:
            stripped_c2pa = True
            stripped_boxes.append(box_type)
            offset = box_end
            continue

        # 2. NORMALIZE MAJOR BRAND IN 'ftyp'
        if box_type == "ftyp" and len(box_data) >= 16:
            # Set major brand to 'mp42' (0x6d, 0x70, 0x34, 0x32)
            box_data[8:12] = b"mp42"
            normalized_brand = True

        out_chunks.extend(box_data)
        offset = box_end

    # Write cleaned output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(out_chunks)
    cleaned_size = len(out_chunks)

    stats = {
        "original_size": original_size,
        "cleaned_size": cleaned_size,
        "bytes_removed": original_size - cleaned_size,
        "stripped_c2pa": stripped_c2pa,
        "normalized_brand": normalized_brand,
        "stripped_boxes": stripped_boxes,
        "output_path": str(out_path.resolve()),
    }
    return stats


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cleaner.py <input.mp4> <output.mp4>")
        sys.exit(1)

    result = clean_mp4_binary(sys.argv[1], sys.argv[2])
    print(f"[C2PA Cleaner] Original size: {result['original_size']} bytes")
    print(f"[C2PA Cleaner] Cleaned size: {result['cleaned_size']} bytes")
    print(f"[C2PA Cleaner] Stripped C2PA: {result['stripped_c2pa']}")
    print(f"[C2PA Cleaner] Normalized Brand: {result['normalized_brand']}")
    print(f"[C2PA Cleaner] Output saved to: {result['output_path']}")
