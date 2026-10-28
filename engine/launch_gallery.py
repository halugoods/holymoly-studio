import os
import sys
import webbrowser
import http.server
import socketserver
from pathlib import Path

GALLERY_DIR = Path(__file__).resolve().parent.parent / "gallery"
PORT = 5188

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(GALLERY_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS and caching
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def main():
    print("=" * 60)
    print("🎬 HOLYMOLY STUDIO · MOTION RECIPE & SKILL PICKER")
    print(f"📍 Directory: {GALLERY_DIR}")
    print(f"🌐 Server URL: http://localhost:{PORT}")
    print("=" * 60)
    
    url = f"http://localhost:{PORT}/index.html"
    webbrowser.open(url)
    
    with socketserver.TCPServer(("127.0.0.1", PORT), CustomHandler) as httpd:
        print(f"\n[OK] Server running at {url}. Tekan Ctrl+C untuk berhenti.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[STOP] Server dimatikan.")

if __name__ == "__main__":
    main()
