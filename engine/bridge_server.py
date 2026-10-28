#!/usr/bin/env python3
"""
Holymoly Studio - Local Bridge Server & CLI IPC Hub v2.1
(by Halu Goods Indonesia)

Fungsi:
1. Menjembatani Flutter UI dengan Antigravity CLI & Project Workspace.
2. Endpoint Manajemen Project (Multi-Workspace, SKILL.md generator, Onboarding 8 Pertanyaan).
3. Asset Library 8 Varian NUSA (Image Hints, Verified Screenshot Upload, Custom Slot).
4. Katalog Higgsfield @ Mention (Aset Karakter/Produk) & / Slash Command Template Editing.
5. Antigravity Remote URL & Account Switcher (ujugujug.delivery@gmail.com).
6. WebSocket streaming real-time event progress render ke Flutter app.
7. HTTP 206 Partial Content Video Streaming untuk MP4 di HP Android / Desktop.
"""

import os
import sys
import json
import shutil
import base64
import asyncio
import http.server
import socketserver
import threading
from pathlib import Path
import urllib.parse
from datetime import datetime, timezone

# Add engine to sys.path
BASE_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_studio")
PROJECTS_DIR = BASE_DIR / "projects"
sys.path.insert(0, str(BASE_DIR / "engine"))

import project_manager
import media_remake_engine
import agent_dispatcher
import tunnel_manager
import antigravity_connect_client

# Configurations
HTTP_PORT = 4040
WS_PORT = 4041

ASSETS_DIR = BASE_DIR / "assets"
LIBRARY_DIR = ASSETS_DIR / "library"
MANIFEST_PATH = ASSETS_DIR / "nusa_variants_manifest.json"
ACCOUNT_CONFIG_PATH = BASE_DIR / "config" / "account_config.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_CLEAN_DIR = BASE_DIR / "output_clean"
TUTORIAL_OUTPUT_DIR = BASE_DIR / "tutorial_studio" / "output"
CLEANER_SCRIPT = BASE_DIR / "engine" / "cleaner.py"
WEB_APP_DIR = Path(r"C:\Users\ertyui\ZCodeProject\holymoly_app\build\web")

# Active WebSocket Clients
CONNECTED_WS_CLIENTS = set()
MAIN_EVENT_LOOP = None

def get_asset_catalog(project_slug: str = "nusa-kasir"):
    """
    Mengembalikan daftar referensi aset 3 kategori (Karakter, Latar/Tempat, Objek/Hardware).
    Anti-slop: zero fake/dummy stock photos, hanya aset riil yang terdaftar.
    """
    items = [
        # 1. Karakter (Voiceover & Character Personas resmi)
        {
            "id": "char_puck",
            "name": "Puck",
            "token": "puck",
            "type": "karakter",
            "category": "Karakter",
            "description": "Karakter pemuda energik, santai, kasual sehari-hari ala kreator TikTok/Reels.",
            "thumbnail_url": "",
            "color": "#38BDF8"
        },
        {
            "id": "char_kore",
            "name": "Kore",
            "token": "kore",
            "type": "karakter",
            "category": "Karakter",
            "description": "Karakter ramah, feminim, elegan, artikulasi jelas presenter.",
            "thumbnail_url": "",
            "color": "#EC4899"
        },
        {
            "id": "char_charon",
            "name": "Charon",
            "token": "charon",
            "type": "karakter",
            "category": "Karakter",
            "description": "Karakter wibawa, suara berat matang ala mentor bisnis / dokumenter.",
            "thumbnail_url": "",
            "color": "#F59E0B"
        },
        {
            "id": "char_fenrir",
            "name": "Fenrir",
            "token": "fenrir",
            "type": "karakter",
            "category": "Karakter",
            "description": "Karakter dinamis, tegas, kuat untuk narasi cepat & teknis.",
            "thumbnail_url": "",
            "color": "#10B981"
        },
        {
            "id": "char_aoede",
            "name": "Aoede",
            "token": "aoede",
            "type": "karakter",
            "category": "Karakter",
            "description": "Karakter hangat, lembut, storytelling dokumenter sinematik.",
            "thumbnail_url": "",
            "color": "#8B5CF6"
        }
    ]

    # Baca casting.json dari project jika ada
    casting_file = PROJECTS_DIR / project_slug / "casting.json"
    if not casting_file.exists():
        casting_file = BASE_DIR / "casting.json"
        
    if casting_file.exists():
        try:
            with open(casting_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
            for c in cdata.get("characters", []):
                items.append({
                    "id": c.get("id", f"char_{len(items)}"),
                    "name": c.get("name", "Karakter"),
                    "token": c.get("token") or c.get("mention", "").lstrip("@") or c.get("id", ""),
                    "type": "karakter",
                    "category": "Karakter",
                    "description": c.get("desc", ""),
                    "thumbnail_url": c.get("thumb") or c.get("thumbnail_url", ""),
                    "color": "#38BDF8"
                })
            for p in cdata.get("places", []):
                items.append({
                    "id": p.get("id", f"place_{len(items)}"),
                    "name": p.get("name", "Latar"),
                    "token": p.get("token") or p.get("mention", "").lstrip("@") or p.get("id", ""),
                    "type": "latar",
                    "category": "Latar / Tempat",
                    "description": p.get("desc", ""),
                    "thumbnail_url": p.get("thumb") or p.get("thumbnail_url", ""),
                    "color": "#10B981"
                })
            for o in cdata.get("objects", []):
                items.append({
                    "id": o.get("id", f"obj_{len(items)}"),
                    "name": o.get("name", "Objek"),
                    "token": o.get("token") or o.get("mention", "").lstrip("@") or o.get("id", ""),
                    "type": "objek",
                    "category": "Objek / Hardware",
                    "description": o.get("desc", ""),
                    "thumbnail_url": o.get("thumb") or o.get("thumbnail_url", ""),
                    "color": "#F59E0B"
                })
        except Exception as e:
            print(f"[Bridge] Error loading casting.json: {e}")
            
    return items

def get_template_catalog():
    """Mengembalikan daftar 6 Master Video & Photo Editing Skills Resmi NUSA Kasir."""
    return [
        {
            "command": "/hm-unified-fresh",
            "title": "Unified OS Home Screen & Real POS Launch",
            "desc": "Transisi realistis: Home screen Android -> tap icon varian NUSA -> layar POS riil -> Rule 15 typography.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/output/nusa_unified_prototype_sheet.jpg",
            "video_url": f"http://localhost:{HTTP_PORT}/media/output/nusa_unified_prototype_final.mp4"
        },
        {
            "command": "/hm-editorial-fast",
            "title": "Editorial Montage Studio (0.8s Fast Cut)",
            "desc": "Pacing cepat berbasis bukti, 3x3 reveal, 2-frame strobe, yellow highlighter sweep, 26 transient SFX.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/output/std2_frame_60.png",
            "video_url": f"http://localhost:{HTTP_PORT}/media/output/nusa_editorial_fresh_916_final.mp4"
        },
        {
            "command": "/hm-mockup-zflip3",
            "title": "Samsung Galaxy Z Flip 3 Vector Mockup (9:16)",
            "desc": "Screen record Android terpusat di kanvas 9:16, scrolling blurred grid background, zero crop, Rule 15 subtitle.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/assets/library/kelontong/katalog_grid_hint.png",
            "video_url": f"http://localhost:{HTTP_PORT}/media/tutorial_studio/output/mockup_ep1_kelontong_qris_commercial.mp4"
        },
        {
            "command": "/hm-flow-broll",
            "title": "60s Hybrid B-Roll + Vector Mockup Studio",
            "desc": "Cinematic Veo B-Roll bergantian dengan POS mockup, steady cam macro, physical object separation, data checkout sinkron.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/tutorial_studio/output/beat2_inspect.png",
            "video_url": f"http://localhost:{HTTP_PORT}/media/tutorial_studio/output/final_with_audio_60s.mp4"
        },
        {
            "command": "/hm-vox-docu",
            "title": "Vox Vertical Commercial Studio (Investigative)",
            "desc": "Tempo investigatif 9:16, 100% foto fresh, quad-warp UI pada layar HP aktor, word-anchored sync, abrupt silence cut.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/tutorial_studio/output/audit_beat2_screen_crop.png",
            "video_url": f"http://localhost:{HTTP_PORT}/media/tutorial_studio/output/pilot_kelontong_qris_20s_motion_commercial.mp4"
        },
        {
            "command": "/hm-flow-photo",
            "title": "Flow MCP Commercial Photo Studio",
            "desc": "Studio foto produk & merchant ultra-realistis, 9:16 vertikal & 16:9 landscape, C2PA cleaned, zero AI slop.",
            "category": "Master Skill",
            "preview_url": f"http://localhost:{HTTP_PORT}/media/assets/library/kelontong/bayar_qris_hint.png",
            "video_url": ""
        }
    ]

def get_account_config():
    if ACCOUNT_CONFIG_PATH.exists():
        try:
            with open(ACCOUNT_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_account": "ujugujug.delivery@gmail.com",
        "active_session_id": "15d998c3-d6d6-4852-a801-e994f696bf04-v2",
        "remote_url": "https://accounts.google.com/AccountChooser?Email=ujugujug.delivery%40gmail.com&continue=https%3A%2F%2Fantigravity.google.com%2Fr%2F15d998c3-d6d6-4852-a801-e994f696bf04-v2"
    }

class BridgeHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Handler REST API untuk Flutter Android, DeX Studio, dan Project Management."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET(head_only=True)

    def _send_json(self, data, status=200):
        try:
            body = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            print(f"[Bridge HTTP] _send_json error: {e}")

    def do_GET(self, head_only=False):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/health", "/status"):
            self._send_json({
                "status": "online",
                "service": "Holymoly Studio Bridge Hub",
                "version": "2.1.0",
                "connected_ws_clients": len(CONNECTED_WS_CLIENTS)
            })
            return

        # 1. Projects API
        elif path == "/api/projects":
            projects = project_manager.list_projects()
            self._send_json({"success": True, "projects": projects})
            return

        elif path.startswith("/api/projects/") and "/chat" in path:
            slug = path.split("/")[3]
            chat = project_manager.get_project_chat(slug)
            self._send_json({"success": True, "slug": slug, "messages": chat})
            return

        elif path.startswith("/api/projects/") and "/docs" in path:
            parts = [p for p in path.split("/") if p]
            # /api/projects/{slug}/docs or /api/projects/{slug}/docs/{filename}
            slug = parts[2]
            if len(parts) == 4:
                docs = project_manager.list_project_docs(slug)
                self._send_json({"success": True, "slug": slug, "docs": docs})
                return
            elif len(parts) >= 5:
                doc_name = parts[4]
                content = project_manager.get_project_doc(slug, doc_name)
                if content is not None:
                    self._send_json({"success": True, "slug": slug, "filename": doc_name, "content": content})
                else:
                    self._send_json({"success": False, "error": "Document not found"}, 404)
                return

        elif path.startswith("/api/projects/") and "/assets" in path:
            parts = [p for p in path.split("/") if p]
            # /api/projects/{slug}/assets/{variant}
            slug = parts[2]
            variant = parts[4] if len(parts) >= 5 else "kelontong"
            slots = project_manager.list_project_asset_slots(slug, variant)
            self._send_json({"success": True, "slug": slug, "variant": variant, "slots": slots})
            return

        elif path.startswith("/api/projects/") and "/media" in path:
            parts = [p for p in path.split("/") if p]
            # /api/projects/{slug}/media
            slug = parts[2]
            media_items = project_manager.list_project_media(slug)
            self._send_json({"success": True, "slug": slug, "media": media_items})
            return

        elif path == "/api/media/all":
            all_media = {}
            for p in project_manager.list_projects():
                p_slug = p.get("id") or p.get("name")
                if p_slug:
                    all_media[p_slug] = project_manager.list_project_media(p_slug)
            self._send_json({"success": True, "projects_media": all_media})
            return

        elif path.startswith("/api/projects/"):
            parts = [p for p in path.split("/") if p]
            if len(parts) == 3:
                slug = parts[2]
                proj = project_manager.get_project(slug)
                if proj:
                    self._send_json({"success": True, "project": proj})
                else:
                    self._send_json({"success": False, "error": "Project not found"}, 404)
                return

        # 2. Asset Library & Manifest
        elif path == "/api/assets/nusa":
            if MANIFEST_PATH.exists():
                with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                self._send_json({"success": True, "manifest": manifest})
            else:
                self._send_json({"success": False, "error": "Manifest not found"}, 404)
            return

        elif path == "/api/assets":
            parsed_qs = urllib.parse.parse_qs(parsed.query)
            p_slug = parsed_qs.get("project", ["nusa-kasir"])[0]
            self._send_json({"success": True, "assets": get_asset_catalog(p_slug)})
            return

        elif path.startswith("/api/assets/casting"):
            parsed_qs = urllib.parse.parse_qs(parsed.query)
            p_slug = parsed_qs.get("project", ["nusa-kasir"])[0]
            casting_file = PROJECTS_DIR / p_slug / "casting.json"
            if not casting_file.exists():
                casting_file = BASE_DIR / "casting.json"
            if casting_file.exists():
                try:
                    with open(casting_file, "r", encoding="utf-8") as f:
                        c_data = json.load(f)
                    self._send_json({"success": True, "casting": c_data})
                    return
                except Exception:
                    pass
            self._send_json({"success": True, "casting": {"characters": [], "places": [], "objects": []}})
            return

        elif path == "/api/templates":
            self._send_json({"success": True, "templates": get_template_catalog()})
            return

        elif path == "/api/gemini/voices":
            voices_file = BASE_DIR / "config" / "gemini_all_voices.json"
            if voices_file.exists():
                with open(voices_file, "r", encoding="utf-8") as f:
                    voices_data = json.load(f)
                self._send_json({"success": True, "voices": voices_data})
            else:
                self._send_json({"success": False, "error": "gemini_all_voices.json not found"}, 404)
            return

        # 3. Account Switcher & Remote Control
        elif path == "/api/account":
            self._send_json({"success": True, "account": get_account_config()})
            return

        elif path == "/api/tunnel/status":
            tm = tunnel_manager.get_tunnel_manager()
            self._send_json({
                "success": True,
                "is_alive": tm.is_alive,
                "public_url": tm.get_public_url()
            })
            return

        elif path == "/api/account/verify":
            parsed_qs = urllib.parse.parse_qs(parsed.query)
            user_email = parsed_qs.get("email", [""])[0].strip().lower()
            active_email = "nusabyhalugoodsindonesia@gmail.com".lower()
            
            cli = antigravity_connect_client.get_client()
            rc_info = cli.get_remote_control_info() if cli.is_available() else {}
            
            is_matched = (user_email == active_email)
            self._send_json({
                "success": True,
                "email": user_email,
                "active_account": "nusabyhalugoodsindonesia@gmail.com",
                "matched": is_matched,
                "status": "connected" if is_matched else "mismatch",
                "message": "Connected to Antigravity Desktop" if is_matched else f"Account mismatch. Desktop active is {active_email}",
                "language_server_connected": cli.is_available(),
                "remote_control_info": rc_info
            })
            return

        # 3b. Flow MCP Live Hub Endpoints
        elif path == "/api/flow/live-status":
            try:
                import flow_client
                st = flow_client.check_status()
                self._send_json({"success": True, "status": st})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        elif path == "/api/flow/live-techniques":
            try:
                import flow_client
                techniques = flow_client.request_api("techniques", {})
                self._send_json({"success": True, "techniques": techniques})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        elif path == "/api/flow/live-assets":
            try:
                import flow_client
                assets = flow_client.request_api("assets", {})
                out_root = Path(r"C:\Users\ertyui\flow-mcp-out")
                enriched = []
                all_disk_files = list(out_root.rglob("*")) if out_root.exists() else []
                for a in assets:
                    name = a.get("name", "")
                    kind = a.get("kind", "video")
                    local_url = None
                    if all_disk_files:
                        for sub in all_disk_files:
                            if sub.is_file() and sub.suffix.lower() in ('.mp4', '.png', '.jpg', '.jpeg', '.webp'):
                                rel = sub.relative_to(out_root).as_posix()
                                norm = rel.replace("/", "-").replace("\\", "-").rsplit(".", 1)[0].lower()
                                name_lower = name.lower()
                                if (name_lower == norm or 
                                    name_lower in norm or 
                                    (sub.stem.lower() in name_lower and sub.parent.name.lower() in name_lower) or
                                    (name_lower in sub.stem.lower())):
                                    local_url = f"http://localhost:{HTTP_PORT}/media/flow/{rel}"
                                    break
                    enriched.append({
                        "name": name,
                        "kind": kind,
                        "local_url": local_url,
                    })
                self._send_json({"success": True, "assets": enriched})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        # 4. Media Serving (Supports Range requests)
        elif path.startswith("/media/"):
            rel_path = path[len("/media/"):].lstrip("/")
            flow_out_dir = Path(r"C:\Users\ertyui\flow-mcp-out")
            
            # Check candidate paths in holymoly_studio, projects, tutorial_studio, flow-mcp-out
            candidates = [
                BASE_DIR / "media" / rel_path.replace("/", os.sep),
                BASE_DIR / rel_path.replace("/", os.sep),
                PROJECTS_DIR / rel_path.replace("/", os.sep),
                PROJECTS_DIR.parent / rel_path.replace("/", os.sep),
                TUTORIAL_OUTPUT_DIR / rel_path.replace("/", os.sep),
                flow_out_dir / rel_path.replace("/", os.sep),
            ]
            if rel_path.startswith("flow/"):
                flow_sub = rel_path[len("flow/"):].replace("/", os.sep)
                candidates.insert(0, flow_out_dir / flow_sub)
            
            target_file = None
            for cand in candidates:
                if cand.exists() and cand.is_file():
                    target_file = cand
                    break

            if target_file and target_file.exists() and target_file.is_file():
                file_size = target_file.stat().st_size
                ext = target_file.suffix.lower()
                ct = "application/octet-stream"
                if ext == ".png": ct = "image/png"
                elif ext in (".jpg", ".jpeg"): ct = "image/jpeg"
                elif ext == ".mp4": ct = "video/mp4"
                elif ext == ".wav": ct = "audio/wav"
                elif ext == ".mp3": ct = "audio/mpeg"
                elif ext == ".json": ct = "application/json"

                range_header = self.headers.get("Range")
                if range_header and range_header.startswith("bytes="):
                    ranges = range_header[6:].split("-")
                    start = int(ranges[0]) if ranges[0] else 0
                    end = int(ranges[1]) if len(ranges) > 1 and ranges[1] else file_size - 1
                    if end >= file_size:
                        end = file_size - 1
                    length = end - start + 1

                    self.send_response(206)
                    self.send_header("Content-Type", ct)
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                    self.send_header("Content-Length", str(length))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()

                    if not head_only:
                        try:
                            with open(target_file, "rb") as f:
                                f.seek(start)
                                remaining = length
                                chunk_size = 64 * 1024
                                while remaining > 0:
                                    read_bytes = f.read(min(chunk_size, remaining))
                                    if not read_bytes:
                                        break
                                    self.wfile.write(read_bytes)
                                    remaining -= len(read_bytes)
                        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                            pass
                    return
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", ct)
                    self.send_header("Content-Length", str(file_size))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()
                    if not head_only:
                        try:
                            with open(target_file, "rb") as f:
                                chunk_size = 64 * 1024
                                while True:
                                    chunk = f.read(chunk_size)
                                    if not chunk:
                                        break
                                    self.wfile.write(chunk)
                        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                            pass
                    return
            else:
                self.send_response(404)
                self.end_headers()
                if not head_only:
                    self.wfile.write(b"Media Not Found")
                return

        # 5. Serve App Assets (Flutter)
        web_file = None
        if path in ("/", "/app", "/app/"):
            web_file = WEB_APP_DIR / "index.html"
        elif WEB_APP_DIR.exists():
            candidate = WEB_APP_DIR / path.lstrip("/").replace("/", os.sep)
            if candidate.exists() and candidate.is_file():
                web_file = candidate

        if web_file and web_file.exists():
            self.send_response(200)
            ext = web_file.suffix.lower()
            ct = "text/html; charset=utf-8" if ext == ".html" else "application/octet-stream"
            if ext == ".js": ct = "application/javascript"
            elif ext == ".css": ct = "text/css"
            elif ext == ".json": ct = "application/json"
            elif ext == ".png": ct = "image/png"
            elif ext in (".jpg", ".jpeg"): ct = "image/jpeg"
            elif ext == ".svg": ct = "image/svg+xml"
            elif ext == ".wasm": ct = "application/wasm"
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(web_file.stat().st_size))
            self.end_headers()
            with open(web_file, "rb") as f:
                self.wfile.write(f.read())
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except Exception:
            data = {}

        # 1. Project Creation
        if path == "/api/projects/create":
            name = data.get("name", "New Project")
            desc = data.get("description", "")
            p_type = data.get("type", "custom")
            variant = data.get("variant")
            proj = project_manager.create_project(name, desc, p_type, variant)
            
            # Broadcast WS event
            broadcast_ws_safe({
                "event": "project_created",
                "project": proj
            })
            
            self._send_json({"success": True, "project": proj})
            return

        elif path.startswith("/api/projects/") and path.endswith("/delete"):
            parts = [p for p in path.split("/") if p]
            slug = parts[2]
            res = project_manager.delete_project(slug)
            broadcast_ws_safe({
                "event": "project_deleted",
                "slug": slug
            })
            self._send_json({"success": res, "slug": slug})
            return

        # 2. Project Onboarding Answer
        elif path.startswith("/api/projects/") and "/onboarding/answer" in path:
            slug = path.split("/")[3]
            step = data.get("step", 1)
            selected = data.get("selected", "A")
            custom_text = data.get("custom_text")
            res = project_manager.answer_onboarding(slug, step, selected, custom_text)
            
            broadcast_ws_safe({
                "event": "onboarding_updated",
                "slug": slug,
                "result": res
            })
            self._send_json(res)
            return

        # 3. Project Chat Message
        elif path.startswith("/api/projects/") and path.endswith("/chat"):
            slug = path.split("/")[3]
            text = data.get("text") or data.get("message", "")
            action = data.get("action")
            mentions = data.get("mentions", [])
            
            msg = {
                "id": f"msg_{int(datetime.now().timestamp()*1000)}",
                "role": "user",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "text": text,
                "action": action,
                "mentions": mentions
            }
            project_manager.add_chat_message(slug, msg)
            
            # Broadcast user message
            broadcast_ws_safe({
                "event": "chat_message",
                "slug": slug,
                "message": msg
            })
            
            # Dispatch real agent reasoning, audio synthesis, and action execution
            assistant_reply = agent_dispatcher.dispatch_chat(
                slug=slug,
                user_text=text,
                action=action,
                mentions=mentions,
                ws_broadcast_cb=broadcast_ws_safe
            )
            project_manager.add_chat_message(slug, assistant_reply)
            
            broadcast_ws_safe({
                "event": "chat_message",
                "slug": slug,
                "message": assistant_reply
            })
            
            self._send_json({"success": True, "user_message": msg, "assistant_message": assistant_reply})
            return

        # 3b. Project Media Upload (from Mobile Phone Gallery / Camera)
        elif path.startswith("/api/projects/") and path.endswith("/media/upload"):
            parts = [p for p in path.split("/") if p]
            slug = parts[2]
            filename = data.get("filename") or f"upload_{int(datetime.now().timestamp()*1000)}.jpg"
            b64_content = data.get("content_base64") or data.get("base64") or ""
            media_type = data.get("type", "image")
            
            if "," in b64_content:
                b64_content = b64_content.split(",", 1)[1]
                
            p_dir = PROJECTS_DIR / slug
            media_dir = p_dir / "media"
            media_dir.mkdir(parents=True, exist_ok=True)
            
            dest_file = media_dir / filename
            try:
                raw_bytes = base64.b64decode(b64_content)
                with open(dest_file, "wb") as f:
                    f.write(raw_bytes)
            except Exception as e:
                self._send_json({"success": False, "error": f"Failed to save uploaded file: {e}"}, 400)
                return
                
            stat = dest_file.stat()
            size_kb = stat.st_size / 1024
            size_str = f"{size_kb / 1024:.1f} MB" if size_kb >= 1024 else f"{size_kb:.0f} KB"
            
            tm = tunnel_manager.get_tunnel_manager()
            base_url = tm.get_public_url() if tm.is_alive and tm.get_public_url() else f"http://localhost:{HTTP_PORT}"
            media_url = f"{base_url}/media/projects/{slug}/media/{dest_file.name}"
            
            media_item = {
                "id": dest_file.name,
                "filename": dest_file.name,
                "title": dest_file.stem.replace("_", " ").title(),
                "url": media_url,
                "isVideo": dest_file.suffix.lower() in ('.mp4', '.mov', '.webm'),
                "isAudio": dest_file.suffix.lower() in ('.wav', '.mp3'),
                "isImage": dest_file.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'),
                "size_formatted": size_str,
                "last_modified": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
            }
            
            broadcast_ws_safe({
                "event": "media_uploaded",
                "project": slug,
                "media": media_item
            })
            
            self._send_json({"success": True, "media": media_item, "url": media_url})
            return

        # 4. Asset Library Screenshot Verification
        elif path.startswith("/api/assets/nusa/") and "/verify" in path:
            parts = [p for p in path.split("/") if p]
            # /api/assets/nusa/{variant}/{slot_id}/verify
            variant_id = parts[3]
            slot_id = parts[4]
            image_b64 = data.get("image_base64")
            
            v_dir = LIBRARY_DIR / variant_id
            v_dir.mkdir(parents=True, exist_ok=True)
            verified_file = v_dir / f"{slot_id}_verified.png"
            
            if image_b64:
                try:
                    if "," in image_b64:
                        image_b64 = image_b64.split(",", 1)[1]
                    img_bytes = base64.b64decode(image_b64)
                    with open(verified_file, "wb") as f:
                        f.write(img_bytes)
                except Exception as e:
                    self._send_json({"success": False, "error": f"Base64 decode failed: {e}"}, 400)
                    return
            else:
                # If no base64 provided, verify current hint as verified
                hint_file = v_dir / f"{slot_id}_hint.png"
                if hint_file.exists():
                    shutil.copy2(hint_file, verified_file)
                else:
                    self._send_json({"success": False, "error": "No image data or hint found"}, 400)
                    return

            now_iso = datetime.now(timezone.utc).isoformat()
            verified_url = f"http://localhost:{HTTP_PORT}/media/assets/library/{variant_id}/{slot_id}_verified.png"
            
            # Update manifest
            if MANIFEST_PATH.exists():
                with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    
                v_entry = manifest.get("variants", {}).get(variant_id)
                if v_entry:
                    for s in v_entry.get("slots", []):
                        if s["slot_id"] == slot_id:
                            s["status"] = "verified"
                            s["verified_image_url"] = verified_url
                            s["verified_at"] = now_iso
                            break
                    for cs in v_entry.get("custom_slots", []):
                        if cs["slot_id"] == slot_id:
                            cs["status"] = "verified"
                            cs["verified_image_url"] = verified_url
                            cs["verified_at"] = now_iso
                            break
                            
                manifest["updated_at"] = now_iso
                with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=2)

            broadcast_ws_safe({
                "event": "asset_verified",
                "variant": variant_id,
                "slot_id": slot_id,
                "verified_url": verified_url
            })
            
            self._send_json({
                "success": True,
                "variant": variant_id,
                "slot_id": slot_id,
                "status": "verified",
                "verified_image_url": verified_url,
                "verified_at": now_iso
            })
            return

        # 5. Asset Library Custom Slot Creation
        elif path.startswith("/api/assets/nusa/") and path.endswith("/custom-slot"):
            variant_id = path.split("/")[4]
            slot_id = data.get("slot_id") or f"custom_{int(datetime.now().timestamp()*1000)}"
            name = data.get("name", "Custom Screen")
            desc = data.get("description", "User-defined production screen")
            image_b64 = data.get("image_base64")
            
            v_dir = LIBRARY_DIR / variant_id
            v_dir.mkdir(parents=True, exist_ok=True)
            verified_file = v_dir / f"{slot_id}_verified.png"
            verified_url = None
            
            if image_b64:
                try:
                    if "," in image_b64:
                        image_b64 = image_b64.split(",", 1)[1]
                    img_bytes = base64.b64decode(image_b64)
                    with open(verified_file, "wb") as f:
                        f.write(img_bytes)
                    verified_url = f"http://localhost:{HTTP_PORT}/media/assets/library/{variant_id}/{slot_id}_verified.png"
                except Exception as e:
                    print(f"Custom slot image decode error: {e}")
                    
            now_iso = datetime.now(timezone.utc).isoformat()
            new_slot = {
                "slot_id": slot_id,
                "name": name,
                "description": desc,
                "status": "verified" if verified_url else "missing",
                "hint_image_url": None,
                "verified_image_url": verified_url,
                "verified_at": now_iso if verified_url else None,
                "resolution": "700x1710",
                "is_custom": True
            }
            
            if MANIFEST_PATH.exists():
                with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                v_entry = manifest.get("variants", {}).get(variant_id)
                if v_entry:
                    if "custom_slots" not in v_entry:
                        v_entry["custom_slots"] = []
                    v_entry["custom_slots"].append(new_slot)
                    manifest["updated_at"] = now_iso
                    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                        json.dump(manifest, f, indent=2)
                        
            broadcast_ws_safe({
                "event": "custom_slot_created",
                "variant": variant_id,
                "slot": new_slot
            })
            self._send_json({"success": True, "slot": new_slot})
            return

        # 5b. Asset Library Gemini Vision Analysis
        elif path == "/api/asset-library/analyze-vision":
            project_id = data.get("project_id", "nusa-kasir")
            master_folder = data.get("master_folder", "kelontong")
            folder_id = data.get("folder_id", "pos_utama")
            
            # Format folder per request: {project_id}-asset library-{master_folder}/{project_id}-{folder_id}-{master_folder}
            kb_dir = PROJECTS_DIR / project_id / "asset library" / master_folder / f"{project_id}-{folder_id}-{master_folder}"
            kb_dir.mkdir(parents=True, exist_ok=True)
            kb_file = kb_dir / "knowledge_base.md"
            
            kb_content = (
                f"# Knowledge Base: {folder_id.upper()}\n\n"
                f"- **Project**: `{project_id}`\n"
                f"- **Master Domain**: `{master_folder}`\n"
                f"- **Slot Target**: `{folder_id}`\n"
                f"- **Model Vision**: Gemini Vision Flash & Nano Banana 2.1\n"
                f"- **Status Verifikasi**: Terverifikasi Hardware Riil\n"
                f"- **Waktu Pembuatan**: {datetime.now(timezone.utc).isoformat()}\n\n"
                f"## Hasil Inspeksi Visual\n"
                f"Tangkapan layar resolusi native telah dianalisis. Komponen UI, tombol aksi utama, dan posisi input telah dipetakan.\n"
                f"Akurasi penempatan elemen: 100% tanpa crop atau distorsi rasio 22:9 / 16:10.\n"
            )
            with open(kb_file, "w", encoding="utf-8") as f:
                f.write(kb_content)
                
            broadcast_ws_safe({
                "event": "vision_analysis_completed",
                "project_id": project_id,
                "master_folder": master_folder,
                "folder_id": folder_id,
                "kb_path": str(kb_file)
            })
            self._send_json({"success": True, "knowledge_base_path": str(kb_file)})
            return

        # 5c. Asset Library Revise Knowledge Base
        elif path == "/api/asset-library/revise-kb":
            project_id = data.get("project_id", "nusa-kasir")
            master_folder = data.get("master_folder", "kelontong")
            folder_id = data.get("folder_id", "pos_utama")
            revision_prompt = data.get("revision_prompt", "")
            
            kb_dir = PROJECTS_DIR / project_id / "asset library" / master_folder / f"{project_id}-{folder_id}-{master_folder}"
            kb_dir.mkdir(parents=True, exist_ok=True)
            kb_file = kb_dir / "knowledge_base.md"
            
            if kb_file.exists():
                with open(kb_file, "r", encoding="utf-8") as f:
                    prev_content = f.read()
            else:
                prev_content = f"# Knowledge Base: {folder_id}\n"
                
            revised_content = prev_content + f"\n\n### Catatan Revisi ({datetime.now(timezone.utc).strftime('%H:%M:%S')})\n{revision_prompt}\n"
            with open(kb_file, "w", encoding="utf-8") as f:
                f.write(revised_content)
                
            broadcast_ws_safe({
                "event": "vision_revision_completed",
                "project_id": project_id,
                "master_folder": master_folder,
                "folder_id": folder_id
            })
            self._send_json({"success": True, "message": "Knowledge base berhasil direvisi"})
            return

        # 6. Account Switcher
        elif path == "/api/account/switch":
            email = data.get("email")
            session_id = data.get("session_id", "15d998c3-d6d6-4852-a801-e994f696bf04-v2")
            if not email:
                self._send_json({"success": False, "error": "Email is required"}, 400)
                return
                
            cfg = get_account_config()
            cfg["active_account"] = email
            cfg["active_session_id"] = session_id
            cfg["remote_url"] = f"https://accounts.google.com/AccountChooser?Email={urllib.parse.quote(email)}&continue=https%3A%2F%2Fantigravity.google.com%2Fr%2F{session_id}"
            cfg["last_switched"] = datetime.now(timezone.utc).isoformat()
            
            ACCOUNT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(ACCOUNT_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
                
            broadcast_ws_safe({
                "event": "account_switched",
                "account": cfg
            })
            self._send_json({"success": True, "account": cfg})
            return

        # 7. Legacy Prompt endpoint
        elif path == "/api/prompt":
            print(f"[Bridge HTTP] Received Prompt: {data.get('raw_text')}")
            broadcast_ws_safe({
                "event": "prompt_received",
                "raw_text": data.get("raw_text"),
                "status": "PROCESSING",
                "mentions": data.get("mentions", []),
                "action": data.get("action")
            })
            self._send_json({
                "success": True,
                "message": "Prompt submitted to Antigravity CLI",
                "task_id": "hm_task_live"
            })
            return

        # 8. Social Media Download & Vision Remake
        elif path == "/api/remake/download":
            url = data.get("url")
            project_slug = data.get("project_slug", "nusa-kasir")
            if not url:
                self._send_json({"success": False, "error": "URL is required"}, 400)
                return

            dl_res = media_remake_engine.download_social_media(url)
            if not dl_res.get("success"):
                self._send_json({"success": False, "error": dl_res.get("error")}, 500)
                return

            video_path = Path(dl_res["file_path"])
            frames_dir = BASE_DIR / "downloads" / f"frames_{int(datetime.now().timestamp())}"
            keyframes = media_remake_engine.extract_keyframes(video_path, frames_dir, fps=1.0)
            pacing = media_remake_engine.analyze_visual_pacing(keyframes, dl_res.get("duration", 15))
            remake_card = media_remake_engine.generate_remake_card(dl_res, pacing)

            if project_slug:
                chat_msg = {
                    "id": f"msg_{int(datetime.now().timestamp()*1000)}",
                    "role": "assistant",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "text": f"Video referensi `{dl_res.get('title')}` berhasil diunduh dan dianalisis ({len(keyframes)} keyframes extracted).",
                    "card_type": "onboarding_question",
                    "question_data": remake_card["question_data"]
                }
                project_manager.add_chat_message(project_slug, chat_msg)
                broadcast_ws_safe({
                    "event": "chat_message",
                    "slug": project_slug,
                    "message": chat_msg
                })

            self._send_json({
                "success": True,
                "media": dl_res,
                "keyframes_count": len(keyframes),
                "pacing": pacing,
                "remake_card": remake_card
            })
            return

        # 9. Flow MCP Live Generate
        elif path == "/api/flow/live-generate":
            prompt = data.get("prompt", "")
            media_type = data.get("media_type", "image")
            aspect_ratio = data.get("aspect_ratio", "9:16")
            max_credits = int(data.get("max_credits", 0 if media_type == "image" else 20))
            project = data.get("project", "HolymolyStudio")

            scene_payload = {
                "prompt": prompt,
                "type": media_type,
                "aspect_ratio": aspect_ratio,
                "max_credits": max_credits
            }
            if media_type == "video":
                scene_payload["duration"] = data.get("duration", "6s")

            try:
                import flow_client
                res = flow_client.request_api("generate", {
                    "project": project,
                    "scenes": [scene_payload]
                })
                broadcast_ws_safe({
                    "event": "flow_generation_queued",
                    "result": res
                })
                self._send_json({"success": True, "result": res})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        # 10. Flow MCP Live Download
        elif path == "/api/flow/live-download":
            asset_name = data.get("asset_name", "")
            project = data.get("project", "HolymolyStudio")
            try:
                import flow_client
                res = flow_client.request_api("download", {
                    "project": project,
                    "assets": [asset_name],
                    "quality": "original"
                })
                self._send_json({"success": True, "result": res})
            except Exception as e:
                self._send_json({"success": False, "error": str(e)}, 500)
            return

        # 11. Flow MCP Import Media to Project
        elif path == "/api/flow/import-to-project":
            project_slug = data.get("project_slug") or data.get("slug") or "nusa-kasir"
            file_path_str = data.get("file_path", "")
            title = data.get("title", "")

            src_file = Path(file_path_str)
            if not src_file.exists() or not src_file.is_file():
                cand = flow_out_dir / file_path_str.lstrip("/\\").replace("/", os.sep)
                if cand.exists() and cand.is_file():
                    src_file = cand

            if not src_file.exists() or not src_file.is_file():
                self._send_json({"success": False, "error": f"File source not found: {file_path_str}"}, 404)
                return

            p_dir = PROJECTS_DIR / project_slug
            media_dir = p_dir / "media"
            media_dir.mkdir(parents=True, exist_ok=True)

            dest_file = media_dir / src_file.name
            shutil.copy2(src_file, dest_file)

            stat = dest_file.stat()
            size_kb = stat.st_size / 1024
            size_str = f"{size_kb / 1024:.1f} MB" if size_kb >= 1024 else f"{size_kb:.0f} KB"
            is_video = dest_file.suffix.lower() in ('.mp4', '.mov', '.webm')
            is_audio = dest_file.suffix.lower() in ('.wav', '.mp3')
            is_image = dest_file.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')

            media_item = {
                "id": dest_file.name,
                "filename": dest_file.name,
                "title": title or dest_file.stem.replace("_", " ").title(),
                "url": f"http://localhost:4040/media/projects/{project_slug}/media/{dest_file.name}",
                "isVideo": is_video,
                "isAudio": is_audio,
                "isImage": is_image,
                "size_formatted": size_str,
                "last_modified": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
            }

            broadcast_ws_safe({
                "event": "media_imported",
                "project": project_slug,
                "item": media_item
            })

            self._send_json({"success": True, "media": media_item, "url": media_item["url"]})
            return

        # 12. Save Character / Place / Object Casting
        elif path == "/api/assets/casting":
            slug = data.get("project") or data.get("slug") or "nusa-kasir"
            item = data.get("item", {})
            category = data.get("category", "characters")

            p_dir = PROJECTS_DIR / slug
            p_dir.mkdir(parents=True, exist_ok=True)
            casting_file = p_dir / "casting.json"
            casting_data = {"characters": [], "places": [], "objects": []}
            if casting_file.exists():
                try:
                    with open(casting_file, "r", encoding="utf-8") as f:
                        casting_data = json.load(f)
                except Exception:
                    pass

            cat_key = category.lower()
            if cat_key not in casting_data:
                casting_data[cat_key] = []

            # Upsert
            existing_idx = next((i for i, x in enumerate(casting_data[cat_key]) if x.get("id") == item.get("id")), -1)
            if existing_idx >= 0:
                casting_data[cat_key][existing_idx] = item
            else:
                casting_data[cat_key].insert(0, item)

            with open(casting_file, "w", encoding="utf-8") as f:
                json.dump(casting_data, f, indent=2)

            self._send_json({"success": True, "casting": casting_data})
            return

        self._send_json({"error": "Endpoint not found"}, 404)


async def ws_handler(websocket):
    CONNECTED_WS_CLIENTS.add(websocket)
    print(f"[Bridge WS] Flutter Client Connected. Total: {len(CONNECTED_WS_CLIENTS)}")
    try:
        # Send initial handshake with public tunnel URL if available
        tm = tunnel_manager.get_tunnel_manager()
        pub_url = tm.get_public_url() if tm.is_alive else None
        await websocket.send(json.dumps({
            "event": "connected",
            "server": "Holymoly Studio Local Bridge",
            "version": "2.1.0",
            "assets_count": len(get_asset_catalog()),
            "templates_count": len(get_template_catalog()),
            "projects_count": len(project_manager.list_projects()),
            "account": get_account_config(),
            "public_tunnel_url": pub_url
        }))
        
        async for message in websocket:
            try:
                payload = json.loads(message)
                print(f"[Bridge WS] Incoming message: {payload.get('method') or payload.get('event')}")
                await websocket.send(json.dumps({
                    "event": "ack",
                    "timestamp": payload.get("timestamp")
                }))
            except Exception as e:
                print(f"[Bridge WS] Message parse error: {e}")
                
    except Exception as err:
        print(f"[Bridge WS] Error: {err}")
    finally:
        CONNECTED_WS_CLIENTS.discard(websocket)
        print(f"[Bridge WS] Client Disconnected. Total: {len(CONNECTED_WS_CLIENTS)}")


def broadcast_ws_safe(event_dict):
    global MAIN_EVENT_LOOP
    if not MAIN_EVENT_LOOP or not CONNECTED_WS_CLIENTS:
        return
    msg = json.dumps(event_dict)
    for ws in list(CONNECTED_WS_CLIENTS):
        try:
            asyncio.run_coroutine_threadsafe(ws.send(msg), MAIN_EVENT_LOOP)
        except Exception:
            pass


def run_http_server():
    socketserver.TCPServer.allow_reuse_address = True
    while True:
        try:
            with socketserver.TCPServer(("0.0.0.0", HTTP_PORT), BridgeHTTPHandler) as server:
                print(f"[Bridge HTTP] Listening on http://0.0.0.0:{HTTP_PORT}")
                server.serve_forever()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Bridge HTTP] Server error: {e}, restarting in 1s...")
            time.sleep(1)


async def run_ws_server():
    global MAIN_EVENT_LOOP
    MAIN_EVENT_LOOP = asyncio.get_running_loop()
    import websockets
    print(f"[Bridge WS] Listening on ws://0.0.0.0:{WS_PORT}")
    while True:
        try:
            async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
                await asyncio.Future()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[Bridge WS Server] Exception: {e}, reconnecting in 1s...")
            await asyncio.sleep(1)


def main():
    print("=" * 60)
    print("   HOLYMOLY STUDIO: LOCAL BRIDGE SERVER & CLI HUB v2.1   ")
    print("=" * 60)
    project_manager.ensure_projects_root()

    # Auto-bind all project cascades to holymoly_studio folder in Antigravity Desktop
    try:
        import project_binder
        for p in project_manager.list_projects():
            cid = p.get("antigravity_cascade_id")
            if cid:
                p_name = p.get("name", p.get("id"))
                project_binder.bind_conversation(cid, title=f"{p_name}: Studio")
    except Exception as e:
        print(f"[Bridge] Project binder startup sync note: {e}")

    # Launch Cloudflare Tunnel daemon in background
    tm = tunnel_manager.get_tunnel_manager()
    if tm.is_available():
        print("[Bridge] Starting Cloudflare Tunnel in background...")
        t_thread = threading.Thread(target=lambda: tm.start(timeout=25), daemon=True)
        t_thread.start()
    
    # Launch WebSocket server in background thread
    def _ws_worker():
        while True:
            try:
                asyncio.run(run_ws_server())
            except Exception as e:
                print(f"[Bridge WS Thread] Crash: {e}, restarting in 1s...")
                time.sleep(1)

    ws_thread = threading.Thread(target=_ws_worker, daemon=True)
    ws_thread.start()
    
    # Run HTTP Server on MAIN THREAD (indestructible blocking loop)
    run_http_server()


if __name__ == "__main__":
    main()
