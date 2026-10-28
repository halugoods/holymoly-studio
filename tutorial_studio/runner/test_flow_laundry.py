import subprocess
import time

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("Testing Laundry Full Checkout Flow...")
# 1. Launch fresh
run("adb shell am start -S -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant laundry --ez pro true --ez onboarding false")
time.sleep(3)

# 2. Tap Kasir
run("adb shell input tap 540 2464")
time.sleep(1.5)

# 3. Tap Layanan
run("adb shell input tap 789 485")
time.sleep(1.5)

# 4. Tap Tambah Cuci Komplit
run("adb shell input tap 284 1392")
time.sleep(1.2)

# 5. Tap 3 kg
run("adb shell input tap 245 2205")
time.sleep(0.8)

# 6. Tap Tambah ke Keranjang
run("adb shell input tap 540 2378")
time.sleep(1.5)

# 7. Tap Bayar
run("adb shell input tap 884 2475")
time.sleep(1.5)

# 8. Swipe up form
run("adb shell input swipe 500 2200 500 800 300")
time.sleep(1.0)

# 9. Tap Uang Pas
run("adb shell input tap 183 1554")
time.sleep(1.0)

# 10. Tap Konfirmasi Pembayaran
run("adb shell input tap 540 2473")
time.sleep(2.0)

# 11. Dump UI to verify Struk Pesanan
run("adb shell uiautomator dump /sdcard/ui_laundry_verify.xml")
run("adb pull /sdcard/ui_laundry_verify.xml ui_laundry_verify.xml")

with open("ui_laundry_verify.xml", "r", encoding="utf-8") as f:
    text = f.read()

if "Struk Pesanan" in text:
    print("[SUCCESS] Laundry Struk Pesanan verified successfully on screen!")
else:
    print("[FAIL] Struk Pesanan not found in dump!")
