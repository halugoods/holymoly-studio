import sys
sys.stdout.reconfigure(encoding='utf-8')
import subprocess
import time
import xml.etree.ElementTree as ET

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

def dump_ui(label):
    time.sleep(1)
    run("adb shell uiautomator dump /sdcard/ui_dump.xml")
    run("adb pull /sdcard/ui_dump.xml ui_dump.xml")
    with open("ui_dump.xml", "r", encoding="utf-8") as f:
        text = f.read()
    root = ET.fromstring(text)
    print(f"\n=== UI DUMP: {label} ===")
    for node in root.iter("node"):
        text_val = node.attrib.get("text", "").strip()
        desc_val = node.attrib.get("content-desc", "").strip()
        bounds = node.attrib.get("bounds", "")
        if text_val or desc_val:
            content = desc_val if desc_val else text_val
            # replace newlines with space
            content = content.replace("\n", " | ")
            print(f"{bounds} -> {content}")

# 2. Tap Layanan
print("Tapping Layanan (789, 485)...")
run("adb shell input tap 789 485")
dump_ui("AFTER TAP LAYANAN")

# 4. Tap 3 kg
print("Tapping 3 kg (245, 2205)...")
run("adb shell input tap 245 2205")
time.sleep(0.5)

# 5. Tap Tambah ke Keranjang
print("Tapping Tambah ke Keranjang (540, 2378)...")
run("adb shell input tap 540 2378")
dump_ui("AFTER ADD TO CART")





