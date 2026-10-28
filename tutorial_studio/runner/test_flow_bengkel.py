import subprocess
import time

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("Testing Bengkel Flow...")
run("adb shell am start -S -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant bengkel --ez pro true --ez onboarding false")
time.sleep(3.5)

# Tap Kasir
run("adb shell input -d 0 tap 540 2464")
time.sleep(1.5)

# Tab Layanan
run("adb shell input -d 0 tap 789 485")
time.sleep(1.5)

# Tambah Jasa Servis Ringan
run("adb shell input -d 0 tap 284 1430")
time.sleep(1.2)

# Tab Produk
run("adb shell input -d 0 tap 290 485")
time.sleep(1.2)

# Tambah Oli Mesin
run("adb shell input -d 0 tap 284 1430")
time.sleep(1.2)

# Bayar
run("adb shell input -d 0 tap 884 2475")
time.sleep(1.5)

# Swipe up form pembayaran
run("adb shell input -d 0 swipe 500 2200 500 800 300")
time.sleep(1.0)

# Tap Uang Pas (183, 1554)
run("adb shell input -d 0 tap 183 1554")
time.sleep(0.8)

# Tap Konfirmasi Pembayaran (540, 2473)
run("adb shell input -d 0 tap 540 2473")
time.sleep(2.0)

# Dump and verify
run("adb shell uiautomator dump /sdcard/ui_bengkel_test.xml")
run("adb pull /sdcard/ui_bengkel_test.xml ui_bengkel_test.xml")

with open("ui_bengkel_test.xml", "r", encoding="utf-8") as f:
    text = f.read()

if "Struk Pesanan" in text:
    print("[SUCCESS] Bengkel Struk Pesanan VERIFIED on screen!")
else:
    print("[FAIL] Struk Pesanan not found!")
