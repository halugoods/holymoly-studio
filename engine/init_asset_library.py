#!/usr/bin/env python3
"""
Initialize Asset Library Manifest & Image Hints for 8 NUSA Variants.
"""

import os
import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio")
ASSETS_DIR = BASE_DIR / "assets"
LIB_DIR = ASSETS_DIR / "library"
TUT_OUTPUT = BASE_DIR / "tutorial_studio" / "output"

VARIANTS = [
    {"id": "kelontong", "name": "NUSA Kelontong", "desc": "Toko Kelontong dan Sembako", "pkg": "com.nusa.kelontong", "color": "#F97316"},
    {"id": "fnb", "name": "NUSA FnB", "desc": "Kafe, Resto dan Kuliner", "pkg": "com.nusa.fnb", "color": "#DC2626"},
    {"id": "laundry", "name": "NUSA Laundry", "desc": "Laundry Kiloan dan Satuan", "pkg": "com.nusa.laundry", "color": "#EC4899"},
    {"id": "bengkel", "name": "NUSA Bengkel", "desc": "Bengkel Motor dan Mobil", "pkg": "com.nusa.bengkel", "color": "#EAB308"},
    {"id": "salon", "name": "NUSA Salon", "desc": "Salon, Barbershop dan Spa", "pkg": "com.nusa.salon", "color": "#3B82F6"},
    {"id": "apotek", "name": "NUSA Apotek", "desc": "Apotek dan Toko Obat", "pkg": "com.nusa.apotek", "color": "#10B981"},
    {"id": "fotocopy", "name": "NUSA Fotocopy", "desc": "Fotocopy dan Percetakan", "pkg": "com.nusa.fotocopy", "color": "#8B5CF6"},
    {"id": "servis", "name": "NUSA Servis", "desc": "Servis HP dan Elektronik", "pkg": "com.nusa.servis", "color": "#152C63"}
]

DASH_MAP = {
    "kelontong": TUT_OUTPUT / "sandbox_kelontong_pos.png",
    "fnb": TUT_OUTPUT / "sandbox_kelontong_pos.png",
    "laundry": TUT_OUTPUT / "laundry_start.png",
    "bengkel": TUT_OUTPUT / "bengkel_dash.png",
    "salon": TUT_OUTPUT / "salon_dash.png",
    "apotek": TUT_OUTPUT / "apotek_dash.png",
    "fotocopy": TUT_OUTPUT / "fotocopy_dash.png",
    "servis": TUT_OUTPUT / "servis_dash.png",
}

SHARED_HINTS = {
    "bayar_qris": TUT_OUTPUT / "after_qris_tap.png",
    "bayar_tunai": TUT_OUTPUT / "after_bayar_tap.png",
    "laporan_omzet": TUT_OUTPUT / "after_laporan_tap.png",
    "keranjang_cart": TUT_OUTPUT / "after_add_items.png",
    "struk_thermal": TUT_OUTPUT / "after_confirm_payment.png",
}

STANDARD_SLOTS = [
    {"slot_id": "auth_login", "name": "Splash dan Login Akun", "desc": "Layar Login Google dan Lisensi Offline/Pro"},
    {"slot_id": "katalog_grid", "name": "Katalog POS dan Grid Produk", "desc": "Grid produk/layanan siap transaksi kasir"},
    {"slot_id": "search_filter", "name": "Pencarian dan Kategori", "desc": "Filter kategori dan pencarian instan nama produk"},
    {"slot_id": "keranjang_cart", "name": "Keranjang Belanja", "desc": "Daftar item belanjaan dan rincian subtotal"},
    {"slot_id": "bayar_qris", "name": "Bayar QRIS Dinamis", "desc": "Layar QRIS ShopeePay Tag 54 dinamis otomatis"},
    {"slot_id": "bayar_tunai", "name": "Bayar Tunai dan Kembalian", "desc": "Input nominal uang tunai dan hitung kembalian"},
    {"slot_id": "struk_thermal", "name": "Struk Cetak Thermal", "desc": "Cetak struk kasir Bluetooth 58mm/80mm ESC/POS"},
    {"slot_id": "struk_wa", "name": "Struk Digital WhatsApp", "desc": "Kirim bukti transaksi PDF via WhatsApp Gateway"},
    {"slot_id": "laporan_omzet", "name": "Laporan Omzet Penjualan", "desc": "Grafik penjualan harian dan total transaksi"},
    {"slot_id": "laporan_kas", "name": "Rekap Kas dan Shift", "desc": "Rekap uang kas masuk/keluar dan tutup shift"},
    {"slot_id": "kelola_produk", "name": "Manajemen Produk/Jasa", "desc": "Tambah, ubah harga, stok, dan barcode produk"},
    {"slot_id": "kelola_karyawan", "name": "Manajemen Karyawan", "desc": "Hak akses kasir vs owner dan kode PIN kasir"},
    {"slot_id": "setting_printer", "name": "Pengaturan Printer", "desc": "Pemasangan printer Bluetooth dan custom footer"},
    {"slot_id": "setting_toko", "name": "Pengaturan Toko", "desc": "Nama toko, alamat, no WhatsApp, dan logo toko"},
    {"slot_id": "cloud_sync", "name": "Status Delta Sync", "desc": "Indikator koneksi cloud dan antrian sinkronisasi"}
]

def main():
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    
    manifest = {
        "version": "1.0.0",
        "updated_at": "2026-10-27T02:11:00Z",
        "variants": {}
    }
    
    for v in VARIANTS:
        v_id = v["id"]
        v_dir = LIB_DIR / v_id
        v_dir.mkdir(parents=True, exist_ok=True)
        
        slots_data = []
        for s in STANDARD_SLOTS:
            s_id = s["slot_id"]
            hint_src = None
            if s_id == "katalog_grid" and v_id in DASH_MAP:
                hint_src = DASH_MAP[v_id]
            elif s_id in SHARED_HINTS:
                hint_src = SHARED_HINTS[s_id]
                
            hint_file_name = f"{s_id}_hint.png"
            dest_hint = v_dir / hint_file_name
            has_hint = False
            
            if hint_src and hint_src.exists():
                shutil.copy2(hint_src, dest_hint)
                has_hint = True
                
            hint_url = f"http://localhost:4040/media/assets/library/{v_id}/{hint_file_name}" if has_hint else None
            
            slots_data.append({
                "slot_id": s_id,
                "name": s["name"],
                "description": s["desc"],
                "status": "hint" if has_hint else "missing",
                "hint_image_url": hint_url,
                "verified_image_url": None,
                "verified_at": None,
                "resolution": "700x1710",
                "is_custom": False
            })
            
        manifest["variants"][v_id] = {
            "variant_id": v_id,
            "name": v["name"],
            "description": v["desc"],
            "package_name": v["pkg"],
            "accent_color": v["color"],
            "icon_url": f"http://localhost:4040/media/assets/variant_icons/{v_id}.png",
            "slots": slots_data,
            "custom_slots": []
        }
        
    out_path = ASSETS_DIR / "nusa_variants_manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"[OK] Manifest generated at {out_path} with {len(VARIANTS)} variants and {len(STANDARD_SLOTS)} slots each.")

if __name__ == "__main__":
    main()
