#!/usr/bin/env python3
"""
Test Mobile Beat 2 Navigation Flow:
1. Ensure Dashboard at Top
2. Swipe Up to Reveal Portal File
3. Tap Portal File (x=540, y=2110)
4. Verify Screen is 'Portal File Percetakan'
5. Tap Buka di PC (x=907, y=496)
6. Verify Dialog 'Buka di PC Kasir' with server IP
"""

import time
import subprocess
import xml.etree.ElementTree as ET

DEVICE = "R5CR81GTJDD"

def adb(cmd):
    return subprocess.run(f"adb -s {DEVICE} shell {cmd}", shell=True, capture_output=True, text=True)

def get_ui_text():
    adb("uiautomator dump /sdcard/ui.xml")
    res = subprocess.run(f"adb -s {DEVICE} pull /sdcard/ui.xml ui_temp.xml", shell=True, capture_output=True, text=True)
    adb("rm /sdcard/ui.xml")
    try:
        tree = ET.parse("ui_temp.xml")
        texts = []
        for n in tree.iter():
            t = n.attrib.get('text', '') or n.attrib.get('content-desc', '')
            if t:
                texts.append(t)
        return " | ".join(texts)
    except:
        return ""

print("Step 1: Ensure Dashboard at Top...")
adb("input swipe 500 600 500 2200 300")
time.sleep(1.0)
ui1 = get_ui_text()
print("  UI Check:", "NUSA" in ui1, "Laporan" in ui1)

print("Step 2: Swipe to reveal Portal File...")
adb("input swipe 500 2000 500 800 350")
time.sleep(1.0)
ui2 = get_ui_text()
print("  Portal File visible:", "Portal File" in ui2)

print("Step 3: Tap Portal File (540, 2110)...")
adb("input tap 540 2110")
time.sleep(2.0)
ui3 = get_ui_text()
print("  Portal File Screen open:", "Portal File Percetakan" in ui3)

print("Step 4: Tap Buka di PC (907, 496)...")
adb("input tap 907 496")
time.sleep(1.5)
ui4 = get_ui_text()
print("  Buka di PC Dialog open:", "Buka di PC Kasir" in ui4 or "portal-file" in ui4)
