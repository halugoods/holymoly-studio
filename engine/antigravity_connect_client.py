#!/usr/bin/env python3
"""
Antigravity ConnectRPC Native Client
(by Halu Goods Indonesia)

Directly connects to the local Antigravity LanguageServerService (language_server.exe)
via ConnectRPC (HTTPS / JSON), completely eliminating the need for CLI (agy.exe) subprocesses.

Provides:
- Dynamic discovery of language_server port and CSRF token
- StartCascade (genuine session creation in Antigravity)
- SendUserCascadeMessage (dispatching user prompts)
- GetCascadeTrajectorySteps (retrieving CoT, thoughts, tool calls, and markdown answers)
- GetRemoteControlInfo (instance 15d998c3-d6d6-4852-a801-e994f696bf04-v2 binding)
"""

import os
import re
import ssl
import json
import uuid
import time
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Ignore self-signed TLS certificates on 127.0.0.1
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HOLYMOLY_PROJECT_ID = "4869d63a-9382-4289-ae85-0da46b2f354c"
HOLYMOLY_WORKSPACE_URI = "file:///c%3A/Users/ertyui/ZCodeProject/holymoly_studio"

class AntigravityConnectClient:
    def __init__(self):
        self.pid = None
        self.csrf_token = None
        self.port = None
        self.base_url = None
        self.last_discover_time = 0

    def is_available(self) -> bool:
        return self.discover()

    def discover(self, force=False):
        """Auto-discover language_server.exe PID, port, and CSRF token."""
        now = time.time()
        if not force and self.base_url and (now - self.last_discover_time < 30):
            return True

        try:
            # 1. Get process command line for CSRF token
            cmd_out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_Process -Filter \"Name = 'language_server.exe'\").CommandLine"],
                text=True, stderr=subprocess.DEVNULL
            )
            csrf_match = re.search(r'--csrf_token\s+([a-f0-9-]+)', cmd_out)
            if not csrf_match:
                return False
            self.csrf_token = csrf_match.group(1)

            # 2. Get PID
            pid_out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-Process -Name 'language_server' -ErrorAction SilentlyContinue).Id"],
                text=True, stderr=subprocess.DEVNULL
            ).strip().splitlines()
            if not pid_out:
                return False
            self.pid = int(pid_out[0].strip())

            # 3. Get listening ports on loopback
            ports_out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 f"(Get-NetTCPConnection -OwningProcess {self.pid} -State Listen | Where-Object LocalAddress -eq '127.0.0.1').LocalPort"],
                text=True, stderr=subprocess.DEVNULL
            )
            ports = [int(p.strip()) for p in ports_out.strip().splitlines() if p.strip()]

            # 4. Probe ports to find the active HTTPS ConnectRPC server
            for p in sorted(ports, reverse=True):
                candidate_url = f"https://127.0.0.1:{p}"
                try:
                    req = urllib.request.Request(
                        f"{candidate_url}/exa.language_server_pb.LanguageServerService/GetRemoteControlInfo",
                        data=b"{}",
                        headers={
                            "Content-Type": "application/json",
                            "x-codeium-csrf-token": self.csrf_token
                        }
                    )
                    with urllib.request.urlopen(req, context=SSL_CTX, timeout=2) as resp:
                        if resp.status == 200:
                            self.port = p
                            self.base_url = candidate_url
                            self.last_discover_time = now
                            return True
                except Exception:
                    continue

        except Exception as e:
            print(f"[AntigravityClient] Discovery failed: {e}")

        return False

    def call_rpc(self, method: str, payload: dict = None) -> dict:
        """Call a method on LanguageServerService via ConnectRPC."""
        if not self.base_url:
            if not self.discover():
                raise RuntimeError("Could not connect to Antigravity LanguageServer. Is Antigravity running?")

        payload = payload or {}
        url = f"{self.base_url}/exa.language_server_pb.LanguageServerService/{method}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-codeium-csrf-token": self.csrf_token
            }
        )

        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
                res_bytes = resp.read()
                if not res_bytes:
                    return {}
                return json.loads(res_bytes.decode("utf-8"))
        except urllib.error.HTTPError as e:
            # If 401 or 403, try to re-discover once (port or token might have refreshed)
            if e.code in (401, 403, 502, 503) and self.discover(force=True):
                url = f"{self.base_url}/exa.language_server_pb.LanguageServerService/{method}"
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "x-codeium-csrf-token": self.csrf_token
                    }
                )
                with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
                    res_bytes = resp.read()
                    return json.loads(res_bytes.decode("utf-8")) if res_bytes else {}
            err_body = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"RPC {method} failed with code {e.code}: {err_body}")

    def get_remote_control_info(self) -> dict:
        """Fetch remote control state and instance UUID."""
        return self.call_rpc("GetRemoteControlInfo")

    def get_default_model(self) -> str:
        """Fetch the default model ID or fallback to MODEL_PLACEHOLDER_M318."""
        try:
            cfg = self.call_rpc("GetCascadeModelConfigData")
            m = cfg.get("defaultOverrideModelConfig", {}).get("modelOrAlias", {}).get("model")
            if m:
                return m
        except Exception:
            pass
        return "MODEL_PLACEHOLDER_M318"

    def get_local_user_info(self) -> dict:
        """Fetch local host user info."""
        return self.call_rpc("GetLocalUserInfo")

    def start_cascade(self, cascade_id: str = None, workspace_dir: str = None, model: str = None, project_id: str = HOLYMOLY_PROJECT_ID) -> str:
        """Start a new cascade (session) in Antigravity associated with the holymoly_studio project."""
        cid = cascade_id or str(uuid.uuid4())
        model_id = model or self.get_default_model()
        ws_uri = f"file:///{Path(workspace_dir or r'C:\Users\ertyui\ZCodeProject\holymoly_studio').as_posix()}"
        uris = [HOLYMOLY_WORKSPACE_URI]

        payload = {
            "cascadeId": cid,
            "source": 1,  # CASCADE_CLIENT
            "workspaceUris": uris,
            "requestedModel": model_id
        }
        if project_id:
            payload["projectId"] = project_id

        res = self.call_rpc("StartCascade", payload)
        return res.get("cascadeId", cid)

    def send_message(self, cascade_id: str, message_text: str, items: list = None, model: str = None) -> dict:
        """Send a user message to an active cascade session with proper model config."""
        if not items:
            items = [{"text": message_text}]
        model_id = model or self.get_default_model()
        return self.call_rpc("SendUserCascadeMessage", {
            "cascadeId": cascade_id,
            "items": items,
            "cascadeConfig": {
                "plannerConfig": {
                    "planModel": model_id
                }
            }
        })

    def get_trajectory_steps(self, cascade_id: str) -> list:
        """Fetch all steps (thoughts, tool calls, and responses) for a cascade."""
        res = self.call_rpc("GetCascadeTrajectorySteps", {"cascadeId": cascade_id})
        return res.get("steps", [])

# Singleton client instance
_client = None

def get_client() -> AntigravityConnectClient:
    global _client
    if _client is None:
        _client = AntigravityConnectClient()
        _client.discover()
    return _client

if __name__ == "__main__":
    client = get_client()
    print("Discovered Base URL:", client.base_url)
    print("CSRF Token:", client.csrf_token[:8] + "..." if client.csrf_token else None)
    try:
        remote_info = client.get_remote_control_info()
        print("Remote Control Info:", json.dumps(remote_info, indent=2))
        user_info = client.get_local_user_info()
        print("User Info:", json.dumps(user_info, indent=2))
    except Exception as e:
        print("RPC Test Error:", e)
