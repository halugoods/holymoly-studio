#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path

source_dir = Path(r"C:\Users\ertyui\ZCodeProject\projects")
target_dir = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio\projects")
skills_dir = Path(r"C:\Users\ertyui\ZCodeProject\.agents\skills")

target_dir.mkdir(parents=True, exist_ok=True)

# Copy projects
if source_dir.exists():
    for item in source_dir.iterdir():
        if item.is_dir():
            dest = target_dir / item.name
            if not dest.exists():
                shutil.copytree(item, dest)
                print(f"Copied {item.name} to {dest}")

doc_templates = {
    "01_overview.md": """# Project Overview & Executive Summary

## 1. Identitas Project
- **Nama Project**: {name}
- **Slug**: {id}
- **Varian Utama**: {variant}
- **Tipe**: Full Commercial & Production Studio Workspace

## 2. Tujuan Konten (Campaign Goal)
Menghasilkan materi video komersial resolusi tinggi (9:16 vertikal), demo fitur kasir POS 1 HP tanpa hardware rumit, dan materi edukasi UMKM Indonesia dengan konversi tinggi.

## 3. Ekosistem
Terintegrasi langsung dengan Holymoly Studio Engine, Bridge Daemon port 4040/4041, dan Antigravity Agent Workspace.
""",
    "02_creative_direction.md": """# Creative Direction & Subtitle Rules

## 1. Standar Universal Tipografi Murni (Rule 15)
- Dilarang keras menggunakan box wrapper, background pill hitam, atau rounded card di belakang teks.
- Subtitle wajib teks putih bersih (#FFFFFF), font size 48px - 56px, font-weight: 800.
- Deep multi-layer shadow:
  `text-shadow: 0 2px 14px rgba(0,0,0,0.95), 0 0 4px rgba(0,0,0,0.85);`
- Word-by-word onset illumination: kata aktif menyala kuning/putih terang, kata pasif redup (opacity 0.35).
- Safe zone bawah: top: 1540px / bottom: 220px (bebas dari overlay UI TikTok/Reels/Shorts).

## 2. Mockup Frame Standar (Samsung Galaxy Z Flip 3)
- Frame vektor HP terkunci di tengah kanvas 9:16 (cx = 540, cy = 960).
- Ukuran proporsional 730x1740 px.
- Zero crop: status bar atas dan bar navigasi bawah terlihat 100% utuh.
""",
    "03_target_audience.md": """# Target Audience & Customer Persona

## 1. Profil Pengguna
- Pemilik usaha retail, UMKM, dan toko mandiri di seluruh Indonesia.
- Menggunakan smartphone Android pribadi untuk seluruh operasional toko.
- Butuh solusi 100% offline saat internet mati, dan sinkronisasi instan saat online.

## 2. Pain Points Utama
1. Bon utang berceceran di kertas robek.
2. Kasbon pelanggan tidak tercatat rapi, memicu kerugian di akhir bulan.
3. Antrean kasir lambat karena kalkulator manual.
4. Laporan omzet tidak akurat.
""",
    "04_voiceover_speech.md": """# Voiceover & Phonetics Guidelines

## 1. Pilihan Talent Suara (Gemini TTS)
- **Budi (Puck)**: Maskulin muda, santai, energik, artikulasi jernih (Tutorial & Demo).
- **Bambang (Charon)**: Maskulin berwibawa, berat, hangat (Komersial & Brand).
- **Siti (Kore)**: Feminin lembut, ramah, meyakinkan (Apotek, Salon, FnB).

## 2. Aturan Pelafalan Fonetis Wajib
- QRIS -> dibaca "Kris" (BUKAN "Q-R-I-S").
- Tap -> dibaca "tep".
- Scan -> dibaca "sken".
- Cashless -> dibaca "kesles".
- Checkout -> dibaca "cekaut".
- POS -> dibaca "P-O-S" atau "mesin kasir".
""",
    "05_asset_manifest.md": """# Asset Library & Evidence Manifest

## 1. Master Folders
- `kelontong/`: Retail sembako, beras karung, minyak goreng, barcode scan.
- `fnb/`: Kafe, resto, pesanan meja, split bill, cetak dapur.
- `laundry/`: Kiloan, satuan, status cuci/setrika/selesai.
- `bengkel/`: Sparepart motor, oli, jasa mekanik, nota rincian servis.
- `salon/`: Treatment rambut, potong, facial, appointment kasir.
- `apotek/`: Obat resep, bebas, racikan, struk medis.
- `fotocopy/`: ATK, jilid, print per-lembar.
- `servis/`: Elektronik, gadget, sparepart, garansi servis.

## 2. Protokol Tangkapan Layar Riil
Seluruh tangkapan layar di-generate langsung dari aplikasi produksi atau screen capture hardware ADB Samsung Z Flip 3. Zero fake mockup dari HTML.
"""
}

for p_dir in target_dir.iterdir():
    if p_dir.is_dir():
        # Documentation folder
        doc_dir = p_dir / "documentation"
        doc_dir.mkdir(exist_ok=True)
        
        meta = {}
        meta_file = p_dir / "project.json"
        if meta_file.exists():
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
        p_name = meta.get("name", p_dir.name)
        p_id = meta.get("id", p_dir.name)
        p_var = meta.get("default_variant", "kelontong")
        
        for fname, template in doc_templates.items():
            fpath = doc_dir / fname
            if not fpath.exists():
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(template.format(name=p_name, id=p_id, variant=p_var))
                    print(f"Created doc {fpath}")
                    
        # Asset Library folders
        asset_lib = p_dir / "asset library"
        asset_lib.mkdir(exist_ok=True)
        for sub in ["kelontong", "fnb", "laundry", "bengkel", "salon", "apotek", "fotocopy", "servis"]:
            (asset_lib / sub).mkdir(exist_ok=True)
            
        (p_dir / "media").mkdir(exist_ok=True)
        
        # Sync SKILL.md to .agents/skills/hm-project-{slug}/SKILL.md
        skill_src = p_dir / "SKILL.md"
        if skill_src.exists():
            dest_skill_dir = skills_dir / f"hm-project-{p_id}"
            dest_skill_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(skill_src, dest_skill_dir / "SKILL.md")
            print(f"Synced skill to {dest_skill_dir / 'SKILL.md'}")

print("Setup successfully completed!")
