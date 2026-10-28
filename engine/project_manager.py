#!/usr/bin/env python3
"""
Holymoly Studio - Project Manager & Onboarding Engine
Handles project workspaces in c:\\Users\\ertyui\\ZCodeProject\\projects,
automated 8-Question Grill-Me onboarding interview seeder,
dynamic SKILL.md generation, and chat session logging.
"""

import os
import re
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio")
PROJECTS_DIR = BASE_DIR / "projects"
SKILLS_DIR = Path(r"C:\Users\ertyui\ZCodeProject\.agents\skills")
ASSETS_DIR = BASE_DIR / "assets"
MANIFEST_PATH = ASSETS_DIR / "nusa_variants_manifest.json"

ONBOARDING_QUESTIONS = [
    {
        "index": 1,
        "key": "role",
        "title": "Peran & Identitas Pembuat",
        "question": "Halo! Selamat datang di project baru. Kamu berperan sebagai apa dalam pembuatan konten ini?",
        "options": [
            {"key": "A", "label": "Founder / Business Owner", "desc": "Fokus branding, edukasi produk, dan konversi penjualan langsung."},
            {"key": "B", "label": "Performance Marketer / Ads", "desc": "Fokus video iklan direct response, hook 3 detik, ROAS tinggi."},
            {"key": "C", "label": "Content Creator / SMM", "desc": "Fokus storytelling organik, relatable, viral TikTok & Reels."},
            {"key": "D", "label": "Technical Educator / Trainer", "desc": "Fokus tutorial step-by-step, fitur aplikasi detail, no-nonsense."}
        ]
    },
    {
        "index": 2,
        "key": "category",
        "title": "Kategori Bisnis & Industri Target",
        "question": "Apa bidang usaha atau industri target dari project ini?",
        "options": [
            {"key": "A", "label": "Retail / Toko Kelontong & Sembako", "desc": "Kasir POS, stok barang, barcode scan, bon utang."},
            {"key": "B", "label": "FnB / Resto, Kafe, Kuliner", "desc": "Menu pesanan, split bill, cetak dapur, QRIS meja."},
            {"key": "C", "label": "Jasa / Laundry, Bengkel, Salon, Servis", "desc": "Layanan per-kilo/per-item, status pengerjaan, nota WA."},
            {"key": "D", "label": "Multi-Business / 8 Varian NUSA", "desc": "Kombinasi 8 varian usaha serba 1 HP serba bisa."}
        ]
    },
    {
        "index": 3,
        "key": "goal",
        "title": "Tujuan Utama Konten (Campaign Goal)",
        "question": "Apa tujuan utama dari video/konten yang ingin kamu buat di project ini?",
        "options": [
            {"key": "A", "label": "Hard Selling / Iklan Berbayar", "desc": "Menonjolkan harga, diskon, dan ajakan download/beli langsung."},
            {"key": "B", "label": "Storytelling Problem-Solution", "desc": "Mengangkat keresahan pemilik usaha (bon jebol) lalu tawarkan solusi."},
            {"key": "C", "label": "Demo Tutorial Fitur Aplikasi", "desc": "Panduan praktis cara pakai fitur kasir POS dari input sampai struk."},
            {"key": "D", "label": "Social Proof & Testimoni UMKM", "desc": "Kisah sukses UMKM bertumbuh omzetnya setelah pakai aplikasi."}
        ]
    },
    {
        "index": 4,
        "key": "visual_style",
        "title": "Gaya Visual & Format Editing",
        "question": "Gaya visual dan editing mana yang ingin dijadikan referensi default project?",
        "options": [
            {"key": "A", "label": "Centered Vector Mockup Z Flip 3", "desc": "HP di tengah 9:16, scrolling blurred grid, zero crop, Rule 15 subtitle."},
            {"key": "B", "label": "Hybrid B-Roll + Vector Mockup 60s", "desc": "Suasana toko riil sinematik bergantian dengan mockup POS."},
            {"key": "C", "label": "Vox Investigative Documentary 9:16", "desc": "Tempo investigatif, foto riil 100% fresh, quad-warp UI, word sync."},
            {"key": "D", "label": "Fast Editorial Montage (0.8s Cut)", "desc": "Pacing cepat, sound effect punchy, strobe, impact keyword besar."}
        ]
    },
    {
        "index": 5,
        "key": "voiceover",
        "title": "Voiceover & Karakter Suara Talent",
        "question": "Gaya voiceover (TTS) mana yang cocok dengan kepribadian brand kamu?",
        "options": [
            {"key": "A", "label": "Charon (Maskulin Berwibawa & Hangat)", "desc": "Suara berat, matang, kredibel ala dokumenter TV atau mentor bisnis."},
            {"key": "B", "label": "Puck (Pemuda Energik & Santai)", "desc": "Santai, antusias, kasual sehari-hari ala kreator TikTok/Reels."},
            {"key": "C", "label": "Kore (Feminim Ramah & Elegan)", "desc": "Lembut, ramah, artikulasi jelas ala presenter edukasi/CS premium."},
            {"key": "D", "label": "Tanpa Voiceover (Audio Beat Murni)", "desc": "Fokus visual ritmik, teks tipografi menyala, dan beat musik."}
        ]
    },
    {
        "index": 6,
        "key": "tone",
        "title": "Tone of Voice Bahasa Naskah",
        "question": "Bahasa dan nada tutur seperti apa yang paling pas untuk audiens kamu?",
        "options": [
            {"key": "A", "label": "Bahasa Indonesia Kasual & Akrab", "desc": "Gaya santai warung ('bon jebol', 'omzet melejit', 'anti ribet')."},
            {"key": "B", "label": "Semi-Formal Profesional UMKM", "desc": "Lugas, terstruktur, menghormati pengusaha ('Bapak/Ibu UMKM')."},
            {"key": "C", "label": "Direct Call-to-Action (To-the-Point)", "desc": "Kalimat pendek, padat, mendesak, langsung ke poin keuntungan."},
            {"key": "D", "label": "Modern Street & Tech-Savvy", "desc": "Trendi, segar, cocok untuk merchant muda dan pengusaha rintisan."}
        ]
    },
    {
        "index": 7,
        "key": "assets",
        "title": "Aset Visual & Screenshot",
        "question": "Bagaimana preferensi penggunaan tangkapan layar (screenshot)?",
        "options": [
            {"key": "A", "label": "Pakai Seed Hint Otomatis NUSA", "desc": "Gunakan library screenshot 8 varian yang sudah terverifikasi."},
            {"key": "B", "label": "Akan Upload Screenshot Sendiri", "desc": "Sediakan slot kosong untuk upload UI produksi milik sendiri."},
            {"key": "C", "label": "Generate Mockup & B-Roll Fresh", "desc": "Buat visual toko dan foto produk baru pakai Flow MCP."},
            {"key": "D", "label": "Rekam Langsung via ADB HP/Emulator", "desc": "Hubungkan perangkat fisik untuk rekam alur transaksi riil."}
        ]
    },
    {
        "index": 8,
        "key": "channel",
        "title": "Kanal Distribusi Utama",
        "question": "Di platform mana konten ini utamanya akan diunggah?",
        "options": [
            {"key": "A", "label": "TikTok & Instagram Reels (9:16)", "desc": "Safe-zone subtitle bawah, durasi 15s–60s, visual eye-catching."},
            {"key": "B", "label": "YouTube Shorts (9:16)", "desc": "Fokus retensi 30 detik pertama, hook kuat, transisi cepat."},
            {"key": "C", "label": "YouTube Longform / Web (16:9)", "desc": "Video demo horizontal resolusi tinggi 1080p/4K."},
            {"key": "D", "label": "WhatsApp Status & Story", "desc": "Ukuran file ringan, teks jelas terbaca di layar HP kecil."}
        ]
    }
]

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'project'

def get_iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def ensure_projects_root():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    nusa_dir = PROJECTS_DIR / "nusa-kasir"
    nusa_meta = nusa_dir / "project.json"
    needs_seed = False
    if not nusa_dir.exists() or not nusa_meta.exists():
        needs_seed = True
    else:
        try:
            with open(nusa_meta, "r", encoding="utf-8") as f:
                d = json.load(f)
            if not d.get("id") or not d.get("name"):
                needs_seed = True
        except Exception:
            needs_seed = True

    if needs_seed:
        _seed_default_nusa_project(nusa_dir)

def delete_project(slug: str) -> bool:
    import shutil
    p_dir = PROJECTS_DIR / slug
    if p_dir.exists() and p_dir.is_dir():
        shutil.rmtree(p_dir, ignore_errors=True)
        return True
    return False

def _seed_default_nusa_project(target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    now = get_iso_now()
    
    project_meta = {
        "id": "nusa-kasir",
        "name": "NUSA Kasir",
        "description": "Ekosistem Konten & Video Studio 8 Varian UMKM Indonesia",
        "type": "nusa",
        "default_variant": "kelontong",
        "created_at": now,
        "last_active": now,
        "status": "active",
        "session_id": "15d998c3-d6d6-4852-a801-e994f696bf04-v2",
        "onboarding_completed": True,
        "onboarding_answers": {
            "role": "Founder / Business Owner",
            "category": "Multi-Business / 8 Varian NUSA",
            "goal": "Demo Tutorial Fitur Aplikasi & Storytelling Solusi",
            "visual_style": "Centered Vector Mockup Z Flip 3",
            "voiceover": "Charon (Maskulin Berwibawa & Hangat)",
            "tone": "Bahasa Indonesia Kasual & Akrab",
            "assets": "Pakai Seed Hint Otomatis NUSA",
            "channel": "TikTok & Instagram Reels (9:16)"
        }
    }
    
    with open(target_dir / "project.json", "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2)
        
    skill_content = _generate_skill_content(project_meta)
    with open(target_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)
        
    try:
        dest_skill_dir = SKILLS_DIR / "hm-project-nusa-kasir"
        dest_skill_dir.mkdir(parents=True, exist_ok=True)
        with open(dest_skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
    except Exception as e:
        print(f"[ProjectManager] Failed to sync nusa-kasir skill: {e}")

    _init_project_folders_and_docs(target_dir, project_meta)
        
    chat_init = [
        {
            "id": "msg_001",
            "role": "assistant",
            "timestamp": now,
            "text": "Selamat datang di project **NUSA Kasir**! 🚀\n\nWorkspace ini siap memproduksi video komersial, tutorial layar HP (Z Flip 3 mockup), dan B-roll sinematik untuk 8 varian UMKM Indonesia.\n\nKetik `/` untuk memilih template motion graphics atau `@` untuk menyebut aset karakter/produk.",
            "card_type": "welcome_card",
            "payload": {
                "variant": "kelontong",
                "recommended_commands": ["/hm-mockup-zflip3", "/hm-flow-broll", "/hm-vox-docu", "/hm-editorial-fast"]
            }
        }
    ]
    with open(target_dir / "chat_session.json", "w", encoding="utf-8") as f:
        json.dump(chat_init, f, indent=2)

DOC_TEMPLATES = {
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

def _init_project_folders_and_docs(p_dir: Path, meta: dict):
    doc_dir = p_dir / "documentation"
    doc_dir.mkdir(exist_ok=True)
    p_name = meta.get("name", p_dir.name)
    p_id = meta.get("id", p_dir.name)
    p_var = meta.get("default_variant", "kelontong")

    for fname, template in DOC_TEMPLATES.items():
        fpath = doc_dir / fname
        if not fpath.exists():
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(template.format(name=p_name, id=p_id, variant=p_var))

    asset_lib = p_dir / "asset library"
    asset_lib.mkdir(exist_ok=True)
    for sub in ["kelontong", "fnb", "laundry", "bengkel", "salon", "apotek", "fotocopy", "servis"]:
        (asset_lib / sub).mkdir(exist_ok=True)

    (p_dir / "media").mkdir(exist_ok=True)

def list_project_docs(slug: str) -> list:
    ensure_projects_root()
    doc_dir = PROJECTS_DIR / slug / "documentation"
    if not doc_dir.exists():
        return []
    
    doc_titles = {
        "01_overview.md": "Project Overview & Vision",
        "02_creative_direction.md": "Creative Direction & Rule 15 Subtitles",
        "03_target_audience.md": "Target Audience & Customer Pain Points",
        "04_voiceover_speech.md": "Voiceover & Phonetics Guidelines",
        "05_asset_manifest.md": "Asset Library & Evidence Manifest",
    }
    
    docs = []
    for f in sorted(doc_dir.glob("*.md")):
        stat = f.stat()
        docs.append({
            "id": f.stem,
            "filename": f.name,
            "title": doc_titles.get(f.name, f.stem.replace("_", " ").title()),
            "size_bytes": stat.st_size,
            "size_formatted": f"{stat.st_size / 1024:.1f} KB" if stat.st_size >= 1024 else f"{stat.st_size} B",
            "last_modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M"),
        })
    return docs

def get_project_doc(slug: str, filename: str) -> str:
    ensure_projects_root()
    doc_file = PROJECTS_DIR / slug / "documentation" / filename
    if not doc_file.exists():
        # Try appending .md if missing
        if not filename.endswith(".md"):
            doc_file = PROJECTS_DIR / slug / "documentation" / f"{filename}.md"
    if not doc_file.exists():
        return None
    with open(doc_file, "r", encoding="utf-8") as f:
        return f.read()

def list_project_asset_slots(slug: str, variant: str) -> list:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    
    # 1. Load manifest data
    manifest_slots = []
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
            v_info = manifest_data.get("variants", {}).get(variant, {})
            manifest_slots = v_info.get("slots", [])
        except Exception as e:
            print(f"[ProjectManager] Error reading manifest: {e}")

    # 2. Check project folder for variant
    variant_dir = p_dir / "asset library" / variant
    variant_dir.mkdir(parents=True, exist_ok=True)
    
    disk_files = {f.stem.lower(): f for f in variant_dir.iterdir() if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')}
    
    slots_out = []
    seen_stems = set()
    
    for s in manifest_slots:
        slot_id = s.get("slot_id", "")
        name = s.get("name", slot_id)
        desc = s.get("description", "")
        status = s.get("status", "missing")
        hint_url = s.get("hint_image_url")
        verified_url = s.get("verified_image_url")
        
        # Check if project has an overriding disk file
        matching_file = disk_files.get(slot_id.lower())
        if not matching_file:
            # Check partial match
            for k, f in disk_files.items():
                if slot_id.lower() in k or k in slot_id.lower():
                    matching_file = f
                    break
                    
        if matching_file:
            seen_stems.add(matching_file.stem.lower())
            status = "verified"
            verified_url = f"http://localhost:4040/media/projects/{slug}/asset library/{variant}/{matching_file.name}"
            
        slots_out.append({
            "id": slot_id,
            "slot_id": slot_id,
            "name": name,
            "description": desc,
            "status": status,
            "verified": (status == "verified"),
            "image_url": verified_url or hint_url,
            "hint_image_url": hint_url,
            "verified_image_url": verified_url,
            "resolution": s.get("resolution", "700x1710"),
            "is_custom": False,
        })
        
    # Any extra custom files in project directory
    for k, f in disk_files.items():
        if k not in seen_stems:
            slots_out.append({
                "id": f.stem,
                "slot_id": f.stem,
                "name": f.stem.replace("_", " ").replace("-", " ").title(),
                "description": f"Custom Asset Slot ({f.name})",
                "status": "verified",
                "verified": True,
                "image_url": f"http://localhost:4040/media/projects/{slug}/asset library/{variant}/{f.name}",
                "hint_image_url": None,
                "verified_image_url": f"http://localhost:4040/media/projects/{slug}/asset library/{variant}/{f.name}",
                "resolution": "Custom",
                "is_custom": True,
            })
            
    return slots_out

def list_project_media(slug: str) -> list:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    media_dir = p_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    
    media_items = []
    
    # 1. Project-specific media
    for f in sorted(media_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if f.is_file():
            ext = f.suffix.lower()
            if ext in ('.mp4', '.mov', '.webm', '.png', '.jpg', '.jpeg', '.webp', '.wav', '.mp3'):
                stat = f.stat()
                is_video = ext in ('.mp4', '.mov', '.webm')
                is_audio = ext in ('.wav', '.mp3')
                is_image = ext in ('.png', '.jpg', '.jpeg', '.webp')
                size_kb = stat.st_size / 1024
                size_str = f"{size_kb / 1024:.1f} MB" if size_kb >= 1024 else f"{size_kb:.0f} KB"
                media_items.append({
                    "id": f.name,
                    "filename": f.name,
                    "title": f.stem.replace("_", " ").title(),
                    "url": f"http://localhost:4040/media/projects/{slug}/media/{f.name}",
                    "isVideo": is_video,
                    "isAudio": is_audio,
                    "isImage": is_image,
                    "size_formatted": size_str,
                    "last_modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M"),
                })
                
    # 2. Fall back to studio shared media so it's not a dead void
    if not media_items:
        shared_media_dir = BASE_DIR / "media"
        if shared_media_dir.exists():
            for f in sorted(shared_media_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
                if f.is_file():
                    ext = f.suffix.lower()
                    if ext in ('.mp4', '.mov', '.webm', '.png', '.jpg', '.jpeg', '.webp', '.wav', '.mp3'):
                        stat = f.stat()
                        is_video = ext in ('.mp4', '.mov', '.webm')
                        is_audio = ext in ('.wav', '.mp3')
                        is_image = ext in ('.png', '.jpg', '.jpeg', '.webp')
                        size_kb = stat.st_size / 1024
                        size_str = f"{size_kb / 1024:.1f} MB" if size_kb >= 1024 else f"{size_kb:.0f} KB"
                        media_items.append({
                            "id": f.name,
                            "filename": f.name,
                            "title": f.stem.replace("_", " ").title(),
                            "url": f"http://localhost:4040/media/{f.name}",
                            "isVideo": is_video,
                            "isAudio": is_audio,
                            "isImage": is_image,
                            "size_formatted": size_str,
                            "last_modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M"),
                        })
    return media_items

def _generate_skill_content(meta: dict) -> str:
    name = meta.get("name", "Project")
    answers = meta.get("onboarding_answers", {})
    role = answers.get("role", "Content Creator")
    cat = answers.get("category", "General UMKM")
    goal = answers.get("goal", "Demo Tutorial & Problem-Solution")
    style = answers.get("visual_style", "Centered Vector Mockup Z Flip 3")
    vo = answers.get("voiceover", "Charon")
    tone = answers.get("tone", "Bahasa Indonesia Kasual & Akrab")
    channel = answers.get("channel", "TikTok & Instagram Reels (9:16)")
    
    return f"""---
name: {meta.get("id", "project")}
description: Production guidelines and creative direction for {name}.
---

# {name} - Creative Engine & Directives

## 1. Identitas & Target Audiens
- **Project**: {name}
- **Role Creator**: {role}
- **Kategori Industri**: {cat}
- **Campaign Goal**: {goal}
- **Distribusi Utama**: {channel}

## 2. Aturan Visual & Motion Editing
- **Format Kanvas**: 9:16 Vertikal (1080x1920) atau 16:9 Landscape sesuai target channel.
- **Visual Reference**: {style}
- **Zero Hallucinated Code UI**: Wajib gunakan screenshot atau screen recording asli dari Asset Library / HP fisik. DILARANG membuat fake mockup dari kode/HTML.
- **Standar Baku Subtitle (Rule 15)**:
  - 100% Pure White Typography (#FFFFFF), font size 48px - 56px, font-weight: 800.
  - Zero box / zero card wrapper di belakang teks.
  - Deep multi-layer shadow: `text-shadow: 0 2px 14px rgba(0,0,0,0.95), 0 0 4px rgba(0,0,0,0.85);`
  - Word-by-word onset illumination.

## 3. Audio & Voiceover Direction
- **Voiceover Character**: {vo} (Native Gemini Flash TTS 1.0x speed, zero time-stretch rubberband).
- **Tone of Voice**: {tone}
- Pelafalan QRIS wajib ditulis fonetis sebagai "Kris".
- Ducking bed musik di bawah narator -7 dB, abrupt silence cut pada outro punchline.
"""

def list_projects() -> list:
    ensure_projects_root()
    projects = []
    
    # Load manifest for verified asset counts
    manifest_data = {}
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception:
            pass
            
    variants_dict = manifest_data.get("variants", {})

    for item in PROJECTS_DIR.iterdir():
        if item.is_dir():
            meta_file = item / "project.json"
            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        
                    # Calculate assets stats
                    total_slots = 0
                    verified_slots = 0
                    if meta.get("type") == "nusa":
                        for v_id, v_info in variants_dict.items():
                            slots = v_info.get("slots", [])
                            total_slots += len(slots)
                            verified_slots += sum(1 for s in slots if s.get("status") == "verified")
                            
                    meta["total_assets_count"] = total_slots
                    meta["verified_assets_count"] = verified_slots
                    projects.append(meta)
                except Exception as e:
                    print(f"[ProjectManager] Error reading {meta_file}: {e}")
                    
    # Sort by last_active descending
    projects.sort(key=lambda p: p.get("last_active", ""), reverse=True)
    return projects

def get_project(slug: str) -> dict:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    meta_file = p_dir / "project.json"
    if not meta_file.exists():
        return None
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return meta

def create_project(name: str, description: str = "", p_type: str = "custom", variant: str = None) -> dict:
    ensure_projects_root()
    slug = slugify(name)
    p_dir = PROJECTS_DIR / slug
    counter = 1
    while p_dir.exists():
        slug = f"{slugify(name)}-{counter}"
        p_dir = PROJECTS_DIR / slug
        counter += 1
        
    p_dir.mkdir(parents=True, exist_ok=True)
    now = get_iso_now()
    
    meta = {
        "id": slug,
        "name": name,
        "description": description or f"Creative studio workspace for {name}",
        "type": p_type,
        "default_variant": variant or ("kelontong" if p_type == "nusa" else None),
        "created_at": now,
        "last_active": now,
        "status": "onboarding",
        "session_id": "15d998c3-d6d6-4852-a801-e994f696bf04-v2",
        "onboarding_completed": False,
        "onboarding_step": 1,
        "onboarding_answers": {}
    }
    
    with open(p_dir / "project.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    skill_content = _generate_skill_content(meta)
    with open(p_dir / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)
        
    # Sync SKILL.md to .agents/skills
    try:
        dest_skill_dir = SKILLS_DIR / f"hm-project-{slug}"
        dest_skill_dir.mkdir(parents=True, exist_ok=True)
        with open(dest_skill_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
    except Exception as e:
        print(f"[ProjectManager] Failed to sync skill to .agents/skills: {e}")

    # Initialize folders and documentation
    _init_project_folders_and_docs(p_dir, meta)
        
    first_q = ONBOARDING_QUESTIONS[0]
    chat_init = [
        {
            "id": f"msg_{int(datetime.now().timestamp()*1000)}",
            "role": "assistant",
            "timestamp": now,
            "text": f"Selamat datang di project baru **{name}**!\n\nAgar konten dan video yang kita buat presisi sesuai kebutuhanmu, mari jawab 8 pertanyaan singkat berikut:",
            "card_type": "onboarding_question",
            "question_data": first_q
        }
    ]
    with open(p_dir / "chat_session.json", "w", encoding="utf-8") as f:
        json.dump(chat_init, f, indent=2)
        
    return meta

def get_project_chat(slug: str) -> list:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    chat_file = p_dir / "chat_session.json"
    if not chat_file.exists():
        return []
    with open(chat_file, "r", encoding="utf-8") as f:
        return json.load(f)

def add_chat_message(slug: str, message: dict) -> dict:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    chat_file = p_dir / "chat_session.json"
    history = []
    if chat_file.exists():
        with open(chat_file, "r", encoding="utf-8") as f:
            history = json.load(f)
            
    now = get_iso_now()
    if "id" not in message:
        message["id"] = f"msg_{int(datetime.now().timestamp()*1000)}"
    if "timestamp" not in message:
        message["timestamp"] = now
        
    history.append(message)
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
        
    # Update last_active in project.json
    meta_file = p_dir / "project.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["last_active"] = now
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
            
    return message

def answer_onboarding(slug: str, step_index: int, selected_key: str, custom_text: str = None) -> dict:
    ensure_projects_root()
    p_dir = PROJECTS_DIR / slug
    meta_file = p_dir / "project.json"
    if not meta_file.exists():
        return {"error": "Project not found"}
        
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    q_item = next((q for q in ONBOARDING_QUESTIONS if q["index"] == step_index), None)
    if not q_item:
        return {"error": "Invalid step"}
        
    # Find option label
    opt = next((o for o in q_item["options"] if o["key"] == selected_key), None)
    label = opt["label"] if opt else (custom_text or selected_key)
    
    # Record answer in user message
    user_msg = {
        "id": f"msg_{int(datetime.now().timestamp()*1000)}",
        "role": "user",
        "timestamp": get_iso_now(),
        "text": f"**{q_item['title']}**: {label}",
        "card_type": "onboarding_answer",
        "answer_data": {
            "step": step_index,
            "key": q_item["key"],
            "selected": selected_key,
            "label": label
        }
    }
    add_chat_message(slug, user_msg)
    
    meta["onboarding_answers"][q_item["key"]] = label
    
    # Check if there is next question
    next_step = step_index + 1
    next_q = next((q for q in ONBOARDING_QUESTIONS if q["index"] == next_step), None)
    
    bot_msg = None
    if next_q:
        meta["onboarding_step"] = next_step
        bot_msg = {
            "id": f"msg_{int(datetime.now().timestamp()*1000) + 1}",
            "role": "assistant",
            "timestamp": get_iso_now(),
            "text": f"Pertanyaan {next_step} dari 8:",
            "card_type": "onboarding_question",
            "question_data": next_q
        }
    else:
        # Onboarding complete!
        meta["onboarding_completed"] = True
        meta["status"] = "active"
        # Regenerate SKILL.md
        skill_content = _generate_skill_content(meta)
        with open(p_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(skill_content)
            
        bot_msg = {
            "id": f"msg_{int(datetime.now().timestamp()*1000) + 1}",
            "role": "assistant",
            "timestamp": get_iso_now(),
            "text": f"🎉 **Onboarding Selesai!** Arahan kreatif untuk **{meta['name']}** telah berhasil disintesis ke dalam `SKILL.md`.\n\nSekarang kamu bisa mulai membuat konten dengan mengetik perintah atau memilih salah satu template video berikut:",
            "card_type": "completion_card",
            "payload": {
                "skill_summary": meta["onboarding_answers"],
                "recommended_commands": ["/hm-mockup-zflip3", "/hm-flow-broll", "/hm-vox-docu", "/hm-editorial-fast"]
            }
        }
        
    add_chat_message(slug, bot_msg)
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    return {
        "success": True,
        "is_complete": meta.get("onboarding_completed", False),
        "next_step": next_step if next_q else None,
        "assistant_message": bot_msg
    }

if __name__ == "__main__":
    ensure_projects_root()
    print("Projects:", [p["id"] for p in list_projects()])
