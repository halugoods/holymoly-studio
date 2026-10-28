#!/usr/bin/env python3
"""
Holymoly Studio - Flow Client Engine
(by Halu Goods Indonesia)

Direct client communicating with local Flow MCP Studio daemon.
Generates images (Imagen 3 / Nano Banana = 0 credits) and videos (Veo).
"""

import json
import os
import time
from pathlib import Path
import urllib.request
import urllib.error

TOKEN_PATH = Path(os.path.expanduser("~/.flow-mcp/token"))
PORT = int(os.environ.get("FLOW_MCP_PORT", "8787"))
BASE_URL = f"http://127.0.0.1:{PORT}"


def get_token() -> str:
    if not TOKEN_PATH.exists():
        raise RuntimeError(f"Flow token not found at {TOKEN_PATH}. Ensure Flow MCP is running.")
    return TOKEN_PATH.read_text("utf-8").strip()


def request_api(endpoint: str, data: dict = None, timeout: int = 300) -> dict:
    url = f"{BASE_URL}/api/{endpoint.lstrip('/')}"
    headers = {
        "x-flow-token": get_token(),
        "Content-Type": "application/json",
    }
    payload = json.dumps(data or {}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"API {endpoint} error {e.code}: {err_msg}")


def check_status() -> dict:
    return request_api("status", {})


def generate_single(
    prompt: str,
    project: str = "HolymolyStudio",
    media_type: str = "image",
    aspect_ratio: str = "1:1",
    max_credits: int = 0,
    timeout_total: int = 180,
) -> str:
    print(f"[Holymoly Studio] Submitting prompt to Flow ({media_type}, max_credits={max_credits})...")
    res = request_api(
        "generate",
        {
            "project": project,
            "scenes": [
                {
                    "prompt": prompt,
                    "type": media_type,
                    "aspect_ratio": aspect_ratio,
                    "max_credits": max_credits,
                }
            ],
        },
    )

    jobs = res.get("jobs", [])
    if not jobs:
        raise RuntimeError("No jobs queued by Flow.")
    job_id = jobs[0]["id"]
    print(f"[Holymoly Studio] Job queued: {job_id}. Waiting for render...")

    start_time = time.time()
    while time.time() - start_time < timeout_total:
        wait_res = request_api("wait", {"job_ids": [job_id], "timeout_seconds": 30})
        job = wait_res.get("jobs", [{}])[0]
        status = job.get("status")
        if status == "done":
            files = job.get("files", [])
            if files:
                print(f"[Holymoly Studio] Render finished -> {files[0]}")
                return files[0]
            raise RuntimeError("Job marked done but no files returned.")
        elif status == "failed":
            raise RuntimeError(f"Job failed: {job.get('error')}")

        print(f"[Holymoly Studio] Status: {status}... continuing wait")
        time.sleep(2)

    raise TimeoutError("Render timed out waiting for Flow.")
