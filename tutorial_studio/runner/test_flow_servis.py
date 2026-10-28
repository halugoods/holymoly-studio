import subprocess
import time

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("Testing Servis Flow...")
run("adb shell am start -S -n com.nusa.dev/com.example.nusa_kasir.MainActivity --es variant servis --ez pro true --ez onboarding false")
time.sleep(3.5)

# 1. Tap Kasir
run("adb shell input -d 0 tap 540 2464")
time.sleep(1.5)

# 2. Tap Layanan
run("adb shell input -d 0 tap 789 485")
time.sleep(1.5)

# 3. Tap Jasa Ganti Baterai (x=284, y=1430 or y=2200)
# Let's dump the Layanan tab
run("adb shell uiautomator dump /sdcard/ui_servis_services.xml")
run("adb pull /sdcard/ui_servis_services.xml ui_servis_services.xml")
python_dump = "python holymoly_studio/tutorial_studio/runner/dump_nodes.py ui_servis_services.xml"
print(run(python_dump))
