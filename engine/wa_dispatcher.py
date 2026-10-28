#!/usr/bin/env python3
"""
WhatsApp Dispatcher via ezpzpay / whatsmeow (Port 3098 RPC)
Routes video previews, audit frames, and Google Drive links to partners:
- Session 6c95738a-b866-49c2-8ee4-98794b234d8e -> +62 878-8246-3786
- Session 25e0f061-2456-43c5-be71-19b9a7e0ab21 -> +62 851-5695-5735
"""

import os
import re
import sys
import time
import subprocess
import requests
from pathlib import Path

EZPZ_DIR = Path(r"C:\Users\ertyui\ZCodeProject\ezpzpay")
EZPZD_EXE = EZPZ_DIR / "ezpzd.exe"
RPC_URL = "http://127.0.0.1:3098/api/call"
STATUS_URL = "http://127.0.0.1:3098/api/status"

SESSION_PHONE_MAP = {
    "6c95738a-b866-49c2-8ee4-98794b234d8e": "6287882463786@s.whatsapp.net",
    "25e0f061-2456-43c5-be71-19b9a7e0ab21": "6285156955735@s.whatsapp.net",
}

def ensure_daemon():
    """Ensure ezpzd daemon is running on port 3098."""
    try:
        r = requests.get(STATUS_URL, timeout=1.0)
        if r.status_code == 200 and r.json().get("running"):
            return True
    except Exception:
        pass

    if not EZPZD_EXE.exists():
        print(f"[WA Dispatcher] ezpzd.exe not found at {EZPZD_EXE}")
        return False

    print("[WA Dispatcher] Spawning ezpzd.exe in background...")
    flags = 0x08000000 | 0x00000200 # CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
    subprocess.Popen([str(EZPZD_EXE)], cwd=str(EZPZ_DIR), creationflags=flags)
    
    for _ in range(30):
        time.sleep(0.2)
        try:
            r = requests.get(STATUS_URL, timeout=1.0)
            if r.status_code == 200 and r.json().get("running"):
                print("[WA Dispatcher] ezpzd daemon confirmed online")
                return True
        except Exception:
            pass
    return False

def get_active_wa_session():
    """Get active connected WhatsApp session ID."""
    if not ensure_daemon():
        return None
    try:
        r = requests.post(RPC_URL, json={"method": "ListSessions", "args": []}, timeout=3.0)
        if r.status_code == 200:
            sessions = r.json().get("result", [])
            for s in sessions:
                if s.get("connected"):
                    return s.get("id")
    except Exception as e:
        print(f"[WA Dispatcher] ListSessions error: {e}")
    return None

def phone_to_jid(phone_or_jid: str) -> str:
    """Normalize phone number to WhatsApp JID."""
    if "@" in phone_or_jid:
        return phone_or_jid
    digits = re.sub(r"\D", "", phone_or_jid)
    if digits.startswith("0"):
        digits = "62" + digits[1:]
    return f"{digits}@s.whatsapp.net"

def send_wa_text(target: str, message: str) -> bool:
    """Send WhatsApp text message."""
    sid = get_active_wa_session()
    if not sid:
        print("[WA Dispatcher] No active WhatsApp session")
        return False
    jid = phone_to_jid(target)
    try:
        r = requests.post(RPC_URL, json={
            "method": "SendText",
            "args": [sid, jid, message, None]
        }, timeout=10.0)
        res = r.json()
        print(f"[WA Dispatcher] SendText to {jid}: {res}")
        return res.get("result") is not None
    except Exception as e:
        print(f"[WA Dispatcher] SendText error: {e}")
        return False

def send_wa_image(target: str, image_path: str, caption: str = "") -> bool:
    """Send WhatsApp image."""
    sid = get_active_wa_session()
    if not sid:
        print("[WA Dispatcher] No active WhatsApp session")
        return False
    jid = phone_to_jid(target)
    p = str(Path(image_path).resolve())
    try:
        r = requests.post(RPC_URL, json={
            "method": "SendImage",
            "args": [sid, jid, p, caption, None]
        }, timeout=15.0)
        res = r.json()
        print(f"[WA Dispatcher] SendImage to {jid}: {res}")
        return res.get("result") is not None
    except Exception as e:
        print(f"[WA Dispatcher] SendImage error: {e}")
        return False

def send_wa_video(target: str, video_path: str, caption: str = "") -> bool:
    """Send WhatsApp video."""
    sid = get_active_wa_session()
    if not sid:
        print("[WA Dispatcher] No active WhatsApp session")
        return False
    jid = phone_to_jid(target)
    p = str(Path(video_path).resolve())
    try:
        r = requests.post(RPC_URL, json={
            "method": "SendVideo",
            "args": [sid, jid, p, caption, None]
        }, timeout=30.0)
        res = r.json()
        print(f"[WA Dispatcher] SendVideo to {jid}: {res}")
        return res.get("result") is not None
    except Exception as e:
        print(f"[WA Dispatcher] SendVideo error: {e}")
        return False

def dispatch_preview(conversation_id: str, video_path: str = None, audit_frames: list = None, gdrive_link: str = None, notes: str = None):
    """
    Dispatch preview and cloud download links to WhatsApp based on session routing.
    """
    target_jid = SESSION_PHONE_MAP.get(conversation_id)
    if not target_jid:
        print(f"[WA Dispatcher] Unmapped conversation ID: {conversation_id}. Defaulting to +62 878-8246-3786")
        target_jid = "6287882463786@s.whatsapp.net"

    print(f"[WA Dispatcher] Dispatching to {target_jid} for session {conversation_id}...")
    
    # 1. Send header message
    msg = f"🎬 *[Holymoly Studio AI Video Preview]*\nSession: `{conversation_id[:8]}...`"
    if gdrive_link:
        msg += f"\n\n📥 *Download Full High-Res Master (Google Drive)*:\n{gdrive_link}"
    if notes:
        msg += f"\n\n📝 *Catatan Perubahan / Deskripsi*:\n{notes}"
    msg += "\n\n💡 _Balas chat ini atau di sesi Antigravity untuk mengajukan revisi!_"
    
    send_wa_text(target_jid, msg)

    # 2. Send audit frames (if provided)
    if audit_frames:
        for idx, img in enumerate(audit_frames):
            if Path(img).exists():
                caption = f"Audit Frame {idx+1}/{len(audit_frames)}: {Path(img).name}"
                send_wa_image(target_jid, img, caption)

    # 3. Send video preview directly
    if video_path and Path(video_path).exists():
        send_wa_video(target_jid, video_path, f"▶️ Video Preview: {Path(video_path).name}")

if __name__ == "__main__":
    sid = get_active_wa_session()
    print(f"Active WA Session: {sid}")
    if len(sys.argv) > 2:
        cmd = sys.argv[1]
        target = sys.argv[2]
        if cmd == "text" and len(sys.argv) > 3:
            send_wa_text(target, sys.argv[3])
        elif cmd == "image" and len(sys.argv) > 3:
            cap = sys.argv[4] if len(sys.argv) > 4 else ""
            send_wa_image(target, sys.argv[3], cap)
        elif cmd == "video" and len(sys.argv) > 3:
            cap = sys.argv[4] if len(sys.argv) > 4 else ""
            send_wa_video(target, sys.argv[3], cap)
