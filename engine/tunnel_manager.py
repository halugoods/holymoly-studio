#!/usr/bin/env python3
"""
Cloudflare Tunnel Manager for Holymoly Studio
(by Halu Goods Indonesia)

Spawns and manages 'cloudflared tunnel' background daemon to provide a secure public
HTTPS relay URL (e.g. https://xxx.trycloudflare.com) for bridge_server.py (port 4040).

Allows mobile devices outside the local WiFi network (4G/5G/cellular) to stream media
and interact with the studio without 'localhost' resolution failures or ExoPlayer crashes.
"""

import os
import re
import sys
import time
import shutil
import threading
import subprocess
from typing import Optional

CLOUDFLARED_PATH = r"C:\Program Files (x86)\cloudflared\cloudflared.exe"

class TunnelManager:
    def __init__(self, target_port: int = 4040):
        self.target_port = target_port
        self.process: Optional[subprocess.Popen] = None
        self.public_url: Optional[str] = None
        self._lock = threading.Lock()
        self._is_running = False

    def is_available(self) -> bool:
        return os.path.exists(CLOUDFLARED_PATH) or shutil.which("cloudflared") is not None

    def start(self, timeout: int = 25) -> Optional[str]:
        """Start cloudflared tunnel and wait for the public URL."""
        with self._lock:
            if self._is_running and self.public_url:
                return self.public_url

            bin_path = CLOUDFLARED_PATH if os.path.exists(CLOUDFLARED_PATH) else "cloudflared"
            cmd = [bin_path, "tunnel", "--url", f"http://127.0.0.1:{self.target_port}", "--no-autoupdate"]

            try:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                self._is_running = True
            except Exception as e:
                print(f"[TunnelManager] Failed to launch cloudflared: {e}")
                return None

        # Background thread to monitor output and extract URL
        url_event = threading.Event()

        def _monitor():
            pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
            while self._is_running and self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if not line:
                    break
                match = pattern.search(line)
                if match:
                    with self._lock:
                        self.public_url = match.group(0)
                    url_event.set()
                    print(f"[TunnelManager] Cloudflare Tunnel established: {self.public_url}")

            with self._lock:
                self._is_running = False

        thread = threading.Thread(target=_monitor, daemon=True)
        thread.start()

        # Wait up to timeout seconds for URL
        url_event.wait(timeout=timeout)
        return self.public_url

    def stop(self):
        """Stop the tunnel daemon."""
        with self._lock:
            self._is_running = False
            if self.process and self.process.poll() is None:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=3)
                except Exception:
                    try:
                        self.process.kill()
                    except Exception:
                        pass
                self.process = None
                self.public_url = None

    def get_public_url(self) -> Optional[str]:
        if not self.is_alive:
            self.public_url = None
        return self.public_url

    @property
    def is_alive(self) -> bool:
        return self._is_running and self.process is not None and self.process.poll() is None

_tunnel_instance: Optional[TunnelManager] = None

def get_tunnel_manager(target_port: int = 4040) -> TunnelManager:
    global _tunnel_instance
    if _tunnel_instance is None:
        _tunnel_instance = TunnelManager(target_port=target_port)
    return _tunnel_instance

if __name__ == "__main__":
    tm = get_tunnel_manager()
    print("Cloudflared available:", tm.is_available())
    if tm.is_available():
        print("Starting tunnel...")
        url = tm.start(timeout=20)
        print("Result URL:", url)
        if url:
            time.sleep(3)
        tm.stop()
        print("Tunnel stopped.")
