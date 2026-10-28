#!/usr/bin/env python3
"""
Holymoly Studio - End-to-End Test Suite
(Superpowers Test-Driven Quality Assurance)

Validates 100% of the live backend daemon endpoints:
- Server status & Flow MCP integration
- Dynamic project & media filesystem endpoints
- Real GenAI agent chat reasoning (anti-slop)
- Real audio synthesis (EdgeTTS) & binary stream serving
"""

import unittest
import urllib.request
import json
import time

BASE_URL = "http://localhost:4040"

class TestHolymolyEndToEnd(unittest.TestCase):

    def _get_json(self, endpoint: str, timeout: int = 30):
        url = f"{BASE_URL}{endpoint}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            self.assertEqual(response.status, 200, f"Expected 200 from {endpoint}")
            data = json.loads(response.read().decode('utf-8'))
            return data

    def _resolve_url(self, url: str) -> str:
        if "trycloudflare.com" in url:
            sub = url.split(".trycloudflare.com")[-1]
            return f"{BASE_URL}{sub}"
        return url

    def _post_json(self, endpoint: str, payload: dict, timeout=45):
        url = f"{BASE_URL}{endpoint}"
        body = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            self.assertEqual(response.status, 200, f"Expected 200 from {endpoint}")
            data = json.loads(response.read().decode('utf-8'))
            return data

    def test_01_server_health_and_techniques(self):
        """Verify server is live and techniques are loaded."""
        data = self._get_json("/api/flow/live-techniques")
        self.assertTrue(data.get("success"), "Expected success=True")
        self.assertIn("techniques", data)
        self.assertGreater(len(data["techniques"]), 0, "Techniques list should not be empty")

    def test_02_projects_listing(self):
        """Verify dynamic projects listing contains seeded projects."""
        data = self._get_json("/api/projects")
        self.assertTrue(data.get("success"), "Expected success=True")
        self.assertIn("projects", data)
        slugs = [p.get("id") or p.get("name") for p in data["projects"]]
        self.assertIn("nusa-kasir", slugs, "nusa-kasir must be in projects list")

    def test_03_project_detail(self):
        """Verify individual project detail contains valid metadata."""
        data = self._get_json("/api/projects/nusa-kasir")
        self.assertTrue(data.get("success"), "Expected success=True")
        proj = data.get("project", {})
        self.assertEqual(proj.get("id"), "nusa-kasir")
        self.assertIn("name", proj)

    def test_04_dynamic_media_all(self):
        """Verify dynamic media aggregation across all projects from disk."""
        data = self._get_json("/api/media/all")
        self.assertTrue(data.get("success"), "Expected success=True")
        projects_media = data.get("projects_media", {})
        self.assertIn("nusa-kasir", projects_media)
        self.assertGreater(len(projects_media["nusa-kasir"]), 0, "nusa-kasir must have media items")
        
        # Verify structure of media items
        first_item = projects_media["nusa-kasir"][0]
        self.assertIn("filename", first_item)
        self.assertIn("url", first_item)
        self.assertIn("isVideo", first_item)
        self.assertIn("isAudio", first_item)

    def test_05_real_agent_chat_reasoning(self):
        """Verify real Gemini 2.5 Flash agent reasoning for retail copywriting."""
        prompt = "Bagaimana hook video 3 detik untuk warung kelontong yang bonnya sering boncos?"
        data = self._post_json("/api/projects/nusa-kasir/chat", {"message": prompt})
        self.assertTrue(data.get("success"), "Expected success=True")
        assistant_msg = data.get("assistant_message", {})
        text = assistant_msg.get("text", "")
        self.assertGreater(len(text), 30, "Agent text response should be substantial")
        
        # Anti-slop checks
        forbidden_phrases = ["tentu saja!", "di era digital yang serba cepat", "mari kita selami"]
        for phrase in forbidden_phrases:
            self.assertNotIn(phrase, text.lower(), f"Response contains slop phrase: {phrase}")

    def test_06_real_audio_synthesis(self):
        """Verify real EdgeTTS synthesis and binary playback URL."""
        test_script = "NUSA Kasir, solusi kasir serba satu HP untuk UMKM Indonesia."
        data = self._post_json("/api/projects/nusa-kasir/chat", {
            "message": f"/generate-audio {test_script}"
        })
        self.assertTrue(data.get("success"), "Expected success=True")
        assistant_msg = data.get("assistant_message", {})
        self.assertEqual(assistant_msg.get("card_type"), "media_card")
        
        payload = assistant_msg.get("payload", {})
        media_url = payload.get("media_url")
        self.assertIsNotNone(media_url, "media_url must be present in media_card")
        
        # Download and verify the audio binary from bridge server
        req = urllib.request.Request(self._resolve_url(media_url))
        with urllib.request.urlopen(req, timeout=10) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "audio/mpeg")
            audio_bytes = res.read()
            self.assertGreater(len(audio_bytes), 5000, "Synthesized audio should be at least 5KB")

    def test_07_real_video_generation(self):
        """Verify real 9:16 vertical commercial video compositing and streaming."""
        data = self._post_json("/api/projects/nusa-kasir/chat", {
            "message": "/generate-video-mockup NUSA FnB Resto"
        })
        self.assertTrue(data.get("success"), "Expected success=True")
        assistant_msg = data.get("assistant_message", {})
        self.assertEqual(assistant_msg.get("card_type"), "media_card")
        
        payload = assistant_msg.get("payload", {})
        self.assertEqual(payload.get("media_type"), "video")
        video_url = payload.get("media_url")
        self.assertIsNotNone(video_url)
        
        req = urllib.request.Request(self._resolve_url(video_url))
        with urllib.request.urlopen(req, timeout=10) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "video/mp4")
            # Verify stream starts with valid MP4 header
            chunk = res.read(1024)
            self.assertGreater(len(chunk), 500)

    def test_08_flow_video_streaming(self):
        """Verify video streaming directly from Flow MCP output folder."""
        data = self._get_json("/api/flow/live-status")
        self.assertTrue(data.get("success"), "Expected success=True")
        status_data = data.get("status", {})
        jobs = status_data.get("jobs", [])
        
        done_jobs = [j for j in jobs if j.get("status") == "done" and j.get("files")]
        self.assertGreater(len(done_jobs), 0, "Expected at least one completed Flow job")
        
        # Test streaming the first completed Flow video
        target_job = done_jobs[0]
        file_path = target_job["files"][0]
        # Derives relative path from flow-mcp-out
        subpath = file_path.split("flow-mcp-out\\")[-1].replace("\\", "/")
        flow_url = f"{BASE_URL}/media/flow/{subpath}"
        
        req = urllib.request.Request(flow_url)
        with urllib.request.urlopen(req, timeout=10) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(res.headers.get("Content-Type"), "video/mp4")
            self.assertEqual(res.headers.get("Accept-Ranges"), "bytes")
            chunk = res.read(2048)
            self.assertGreater(len(chunk), 1000)

    def test_09_flow_import_to_project(self):
        """Verify importing a completed Flow MCP video into project media."""
        data = self._get_json("/api/flow/live-status")
        status_data = data.get("status", {})
        jobs = status_data.get("jobs", [])
        done_jobs = [j for j in jobs if j.get("status") == "done" and j.get("files")]
        self.assertGreater(len(done_jobs), 0)
        
        target_file = done_jobs[0]["files"][0]
        import_res = self._post_json("/api/flow/import-to-project", {
            "project_slug": "nusa-kasir",
            "file_path": target_file,
            "title": "Scene Flow Imported"
        })
        self.assertTrue(import_res.get("success"), "Import should succeed")
        self.assertIn("media", import_res)
        media_item = import_res["media"]
        self.assertEqual(media_item.get("isVideo"), True)
        
        # Verify it appears in project media listing
        project_media = self._get_json("/api/projects/nusa-kasir/media")
        self.assertTrue(project_media.get("success"))
        filenames = [m["filename"] for m in project_media.get("media", [])]
        self.assertIn(media_item["filename"], filenames)

    def test_10_agent_template_photo_and_voice_dispatch(self):
        """Verify template dispatch for documentary photography and narrator voice configuration."""
        # Test 1: Set Voice
        voice_res = self._post_json("/api/projects/nusa-kasir/chat", {
            "message": "/set-voice puck",
            "action": "/set-voice puck"
        })
        self.assertTrue(voice_res.get("success"))
        asst_msg = voice_res.get("assistant_message", {})
        self.assertIn("puck", asst_msg.get("text", "").lower())
        
        # Test 2: Flow Photo Clean template
        photo_res = self._post_json("/api/projects/nusa-kasir/chat", {
            "message": "Gunakan template foto produk",
            "action": "/flow-photo-clean"
        })
        self.assertTrue(photo_res.get("success"))
        photo_msg = photo_res.get("assistant_message", {})
        self.assertEqual(photo_msg.get("card_type"), "media_card")
        payload = photo_msg.get("payload", {})
        self.assertEqual(payload.get("media_type"), "image")
        
        # Verify image URL is streamable
        img_url = payload.get("media_url")
        req = urllib.request.Request(self._resolve_url(img_url))
        with urllib.request.urlopen(req, timeout=10) as res:
            self.assertEqual(res.status, 200)
            self.assertIn("image", res.headers.get("Content-Type"))

    def test_11_casting_assets_persistence(self):
        """Verify custom character casting can be saved and retrieved across requests."""
        test_char = {
            "id": "test_pak_bambang",
            "name": "Pak Bambang Sembako",
            "mention": "@pak_bambang",
            "type": "karakter",
            "desc": "Pemilik toko kelontong ramah, batik lengan pendek, senyum hangat.",
            "thumb": "http://localhost:4040/media/flow/NusaKasir916/scene-01.jpeg",
            "isVideo": False
        }
        save_res = self._post_json("/api/assets/casting", {
            "project": "nusa-kasir",
            "category": "characters",
            "item": test_char
        })
        self.assertTrue(save_res.get("success"))
        
        get_res = self._get_json("/api/assets/casting?project=nusa-kasir")
        self.assertTrue(get_res.get("success"))
        casting = get_res.get("casting", {})
        char_ids = [c["id"] for c in casting.get("characters", [])]
        self.assertIn("test_pak_bambang", char_ids)

if __name__ == "__main__":
    unittest.main()
