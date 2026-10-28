#!/usr/bin/env python3
"""
Google Drive Sync Helper for Holymoly Studio
Account: nusabyhalugoodsindonesia@gmail.com
Target Folder: Holymoly Studio Video Outputs (ID: 14CIAznZOlM9NWapNg9w1Y2WA-raJzUTv)
"""

import os
import re
import json
import subprocess
from pathlib import Path

HOLYMOLY_FOLDER_ID = "14CIAznZOlM9NWapNg9w1Y2WA-raJzUTv"
ACCOUNT = "nusabyhalugoodsindonesia@gmail.com"

def upload_video_deliverable(file_path: str, share: bool = True) -> dict:
    """
    Upload a video deliverable to Holymoly Studio folder in Google Drive.
    Returns dict with file_id, view_link, and name.
    """
    p = Path(file_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    print(f"[GDrive Sync] Uploading {p.name} ({p.stat().st_size / 1024 / 1024:.2f} MB) to GDrive...")
    cmd = [
        "gdrive", "mutate", "upload", str(p),
        "--parent", HOLYMOLY_FOLDER_ID,
        "--json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[GDrive Sync] Upload error: {res.stderr}")
        return None

    # Parse output to extract file ID
    out = res.stdout.strip()
    match = re.search(r"\(ID:\s*([a-zA-Z0-9_-]+)\)", out)
    if not match:
        try:
            data = json.loads(out)
            file_id = data.get("id") or data.get("ID")
        except Exception:
            file_id = None
    else:
        file_id = match.group(1)

    if not file_id:
        print(f"[GDrive Sync] Could not parse file ID from output: {out}")
        return None

    print(f"[GDrive Sync] Uploaded successfully! File ID: {file_id}")

    if share:
        share_cmd = ["gdrive", "mutate", "share", file_id, "--type", "anyone", "--role", "reader"]
        subprocess.run(share_cmd, capture_output=True, text=True)
        print(f"[GDrive Sync] Shared as public reader link")

    view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return {
        "file_id": file_id,
        "name": p.name,
        "view_link": view_link,
        "folder_id": HOLYMOLY_FOLDER_ID
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = upload_video_deliverable(sys.argv[1])
        print(json.dumps(res, indent=2))
    else:
        print("Usage: python gdrive_sync.py <file_path>")
