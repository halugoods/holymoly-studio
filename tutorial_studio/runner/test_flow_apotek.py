import subprocess
import time

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("Testing Apotek Flow...")
run("adb shell am start -S -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant apotek --ez pro true --ez onboarding false")
time.sleep(3.5)

# 1. Tap Kasir
run("adb shell input -d 0 tap 540 2464")
time.sleep(1.5)

# 2. Tap Paracetamol
run("adb shell input -d 0 tap 284 1250")
time.sleep(1.2)

# 3. Tap Vitamin C
run("adb shell input -d 0 tap 795 1250")
time.sleep(1.2)

# 4. Tap Bayar (bottom right)
run("adb shell input -d 0 tap 884 2475")
time.sleep(1.5)

# 5. Swipe up form pembayaran
run("adb shell input -d 0 swipe 500 2200 500 800 300")
time.sleep(1.0)

# 6. Tap Uang Pas (183, 1554)
run("adb shell input -d 0 tap 183 1554")
time.sleep(0.8)

# 7. Tap Konfirmasi Pembayaran (540, 2473)
run("adb shell input -d 0 tap 540 2473")
time.sleep(2.0)

# Dump and verify
run("adb shell uiautomator dump /sdcard/ui_apotek_test.xml")
run("adb pull /sdcard/ui_apotek_test.xml ui_apotek_test.xml")

with open("ui_apotek_test.xml", "r", encoding="utf-8") as f:
    text = f.read()

if "Struk Pesanan" in text:
    print("[SUCCESS] Apotek Struk Pesanan VERIFIED on screen!")
else:
    print("[FAIL] Struk Pesanan not found!")
