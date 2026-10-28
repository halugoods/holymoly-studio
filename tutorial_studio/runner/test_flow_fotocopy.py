import subprocess
import time

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("Testing Fotocopy Flow...")
run("adb shell am start -S -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant fotocopy --ez pro true --ez onboarding false")
time.sleep(3.5)

# 1. Tap Kasir
run("adb shell input -d 0 tap 540 2464")
time.sleep(1.5)

# 2. Tap Layanan
run("adb shell input -d 0 tap 789 485")
time.sleep(1.5)

# 3. Tap Print Warna Dokumen A4 (x=795, y=1430)
run("adb shell input -d 0 tap 795 1430")
time.sleep(1.2)

# Check what button is at bottom
run("adb shell uiautomator dump /sdcard/ui_foto_pos.xml")
run("adb pull /sdcard/ui_foto_pos.xml ui_foto_pos.xml")

with open("ui_foto_pos.xml", "r", encoding="utf-8") as f:
    text = f.read()

if "Lanjut Pembayaran" in text:
    print("Found 'Lanjut Pembayaran'!")
    run("adb shell input -d 0 tap 540 2494")
elif "Bayar" in text:
    print("Found 'Bayar'!")
    run("adb shell input -d 0 tap 884 2475")
else:
    print("Neither found!")

time.sleep(1.5)

# Swipe up all the way
run("adb shell input -d 0 swipe 500 2300 500 400 300")
time.sleep(1.0)

# Tap Uang Pas (183, 1375)
run("adb shell input -d 0 tap 183 1375")
time.sleep(0.8)

# Tap Konfirmasi Pembayaran (540, 2294)
run("adb shell input -d 0 tap 540 2294")
time.sleep(2.0)

# Dump and verify
run("adb shell uiautomator dump /sdcard/ui_foto_receipt.xml")
run("adb pull /sdcard/ui_foto_receipt.xml ui_foto_receipt.xml")

with open("ui_foto_receipt.xml", "r", encoding="utf-8") as f:
    text = f.read()

if "Struk Pesanan" in text:
    print("[SUCCESS] Fotocopy Struk Pesanan VERIFIED on screen!")
else:
    print("[FAIL] Struk Pesanan not found!")
