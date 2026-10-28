import subprocess
import time
import urllib.request
import json
import base64
import asyncio
from pathlib import Path
import websockets
import tempfile
import shutil

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_PNG = Path(r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744\flutter_studio_mention_preview.png")

async def capture():
    temp_dir = tempfile.mkdtemp()
    cmd = [
        CHROME_PATH,
        "--headless=new",
        f"--user-data-dir={temp_dir}",
        "--incognito",
        "--disable-cache",
        "--remote-debugging-port=9222",
        "--window-size=1280,800",
        "--disable-gpu",
        "--no-sandbox",
        "http://localhost:4040/?nocache=" + str(time.time())
    ]
    proc = subprocess.Popen(cmd)
    try:
        await asyncio.sleep(4)

        req = urllib.request.urlopen("http://localhost:9222/json")
        targets = json.loads(req.read().decode("utf-8"))
        ws_url = None
        for t in targets:
            if "webSocketDebuggerUrl" in t and "localhost:4040" in t.get("url", ""):
                ws_url = t["webSocketDebuggerUrl"]
                break
        
        if not ws_url:
            print("[Capture] No matching page target found")
            return

        print(f"[Capture] Connecting to DevTools: {ws_url}")
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Network.setCacheDisabled", "params": {"cacheDisabled": True}}))

            print("[Capture] Waiting 7s for CanvasKit render...")
            await asyncio.sleep(7)

            # Click on @ Mention button (x: 60, y: 755)
            click_press = {
                "id": 10,
                "method": "Input.dispatchMouseEvent",
                "params": {"type": "mousePressed", "x": 60, "y": 755, "button": "left", "clickCount": 1}
            }
            click_release = {
                "id": 11,
                "method": "Input.dispatchMouseEvent",
                "params": {"type": "mouseReleased", "x": 60, "y": 755, "button": "left", "clickCount": 1}
            }
            await ws.send(json.dumps(click_press))
            await ws.send(json.dumps(click_release))

            await asyncio.sleep(1.5)

            # Capture screenshot
            await ws.send(json.dumps({
                "id": 12,
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == 12:
                    if "result" in resp and "data" in resp["result"]:
                        img_bytes = base64.b64decode(resp["result"]["data"])
                        with open(OUTPUT_PNG, "wb") as f:
                            f.write(img_bytes)
                        print(f"[Capture] SUCCESS: {len(img_bytes)} bytes written to {OUTPUT_PNG}")
                    break
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(capture())
