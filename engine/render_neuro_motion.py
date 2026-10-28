import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import time

WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 20.25
TOTAL_FRAMES = int(DURATION * FPS)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)

def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)

def create_neural_nodes(n_nodes=40):
    np.random.seed(42)
    nodes = []
    for _ in range(n_nodes):
        x = np.random.uniform(80, WIDTH - 80)
        y = np.random.uniform(400, HEIGHT - 300)
        vx = np.random.uniform(-0.8, 0.8)
        vy = np.random.uniform(-0.8, 0.8)
        size = np.random.uniform(4, 9)
        nodes.append({"x": x, "y": y, "vx": vx, "vy": vy, "size": size})
    return nodes

def render_neuro_video():
    print(f"Rendering {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    out_dir = r"C:\Users\ertyui\.gemini\antigravity\brain\16f1eea6-9828-4575-8da6-2b56ae393744"
    raw_video = os.path.join(out_dir, "edu_neuro_raw.mp4")
    master_video = os.path.join(out_dir, "edu_neuro_motion_final.mp4")
    vo_audio = os.path.join(out_dir, "edu_brain_vo.wav")
    
    # FFmpeg pipe for highest visual fidelity
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        raw_video
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    font_title = ImageFont.truetype(FONT_BOLD, 46)
    font_sub = ImageFont.truetype(FONT_REG, 24)
    font_tag = ImageFont.truetype(FONT_BOLD, 20)
    font_val = ImageFont.truetype(FONT_BOLD, 64)
    font_card_lbl = ImageFont.truetype(FONT_BOLD, 22)
    font_card_sub = ImageFont.truetype(FONT_REG, 24)
    
    nodes = create_neural_nodes(45)
    
    # Pre-generate pulses
    pulses = []
    
    for f in range(TOTAL_FRAMES):
        t = f / FPS
        
        # 1. Base dark background
        img_np = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        # Gradient from top (3, 7, 18) to bottom (10, 18, 42)
        grad = np.linspace(15, 35, HEIGHT, dtype=np.uint8)[:, None]
        img_np[:, :, 0] = grad + 15  # Blue
        img_np[:, :, 1] = grad + 5   # Green
        img_np[:, :, 2] = grad       # Red
        
        # 2. Update and draw neural network nodes
        for n in nodes:
            n["x"] += n["vx"]
            n["y"] += n["vy"]
            if n["x"] < 60 or n["x"] > WIDTH - 60: n["vx"] *= -1
            if n["y"] < 380 or n["y"] > HEIGHT - 300: n["vy"] *= -1
            
        # Draw axon connection lines
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dx = nodes[i]["x"] - nodes[j]["x"]
                dy = nodes[i]["y"] - nodes[j]["y"]
                dist = np.hypot(dx, dy)
                if dist < 210:
                    alpha = (1.0 - dist / 210) * 0.35
                    # Subtle breathing pulse
                    pulse_mod = 0.8 + 0.3 * np.sin(t * 4.0 + i)
                    color = (int(255 * alpha * pulse_mod), int(180 * alpha * pulse_mod), int(40 * alpha * pulse_mod))
                    pt1 = (int(nodes[i]["x"]), int(nodes[i]["y"]))
                    pt2 = (int(nodes[j]["x"]), int(nodes[j]["y"]))
                    cv2.line(img_np, pt1, pt2, color, 1, cv2.LINE_AA)
                    
        # Draw node glowing dots
        for i, n in enumerate(nodes):
            pt = (int(n["x"]), int(n["y"]))
            glow = int(180 + 75 * np.sin(t * 3.0 + i))
            cv2.circle(img_np, pt, int(n["size"] * 2.2), (glow // 3, glow // 2, glow), -1, cv2.LINE_AA)
            cv2.circle(img_np, pt, int(n["size"]), (255, 230, 180), -1, cv2.LINE_AA)
            
        # 3. Text and UI overlays via PIL
        img_pil = Image.fromarray(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Top Header (Clean minimalist Apple/Gojek taxonomy)
        # Category Tag Badge
        badge_box = (80, 120, 430, 166)
        draw.rounded_rectangle(badge_box, radius=8, fill=(15, 25, 45, 200), outline=(0, 240, 255), width=1)
        draw.text((100, 130), "DOKUMENTER SAINS // 0.1s REAKSI", font=font_tag, fill=(0, 240, 255))
        
        # Main Title
        draw.text((80, 190), "BAGAIMANA OTAK MENGINGAT", font=font_title, fill=(255, 255, 255))
        draw.text((80, 255), "Kecepatan sinapsis merekam memori dalam hitungan milidetik", font=font_sub, fill=(148, 163, 184))
        draw.line((80, 310, WIDTH - 80, 310), fill=(51, 65, 85), width=2)
        
        # 4. Animated Metric Cards (Dynamic Timing based on Narration Beats)
        # Beat 1: 86 Miliar Neuron (t: 1.5s to 6.5s)
        # Beat 2: 100 Triliun Sinapsis (t: 6.8s to 11.8s)
        # Beat 3: 430 km/jam Transmisi (t: 12.0s to 18.5s)
        
        cards = [
            {
                "start": 1.5, "end": 6.8, "title": "POPULASI NEURON AKTIF",
                "max_val": 86, "unit": "MILIAR", "sub": "Unit Pemroses Kognitif",
                "color": (0, 240, 255), "bg_glow": (0, 40, 60)
            },
            {
                "start": 6.9, "end": 12.0, "title": "JARINGAN KONEKSI SINAPSIS",
                "max_val": 100, "unit": "TRILIUN", "sub": "Jalur Transmisi Informasi",
                "color": (255, 183, 3), "bg_glow": (60, 40, 0)
            },
            {
                "start": 12.1, "end": 19.5, "title": "KECEPATAN TRANSMISI SINYAL",
                "max_val": 430, "unit": "KM / JAM", "sub": "Impuls Listrik Instan",
                "color": (6, 214, 160), "bg_glow": (0, 50, 35)
            }
        ]
        
        for c in cards:
            if c["start"] <= t <= c["end"]:
                dur_in = 0.5
                progress = min(1.0, (t - c["start"]) / dur_in)
                ease_p = ease_out_back(progress)
                
                # Card geometry centered around y=1100
                card_w = 920
                card_h = 320
                cx = WIDTH // 2
                cy = 1250
                
                # Entrance spring transform
                curr_y = int(cy + (1.0 - ease_p) * 120)
                alpha_box = int(255 * min(1.0, (t - c["start"]) / 0.3))
                
                # Exit fade if near end
                if c["end"] - t < 0.4:
                    exit_p = (c["end"] - t) / 0.4
                    curr_y -= int((1.0 - exit_p) * 60)
                
                x1 = cx - card_w // 2
                y1 = curr_y - card_h // 2
                x2 = cx + card_w // 2
                y2 = curr_y + card_h // 2
                
                # Inset Grouped Card (Apple Glassmorphism / Gojek anti-slop standard)
                draw.rounded_rectangle((x1, y1, x2, y2), radius=24, fill=(12, 18, 34), outline=c["color"], width=2)
                
                # Accent Header Stripe
                draw.rounded_rectangle((x1 + 40, y1 + 35, x1 + 46, y1 + 65), radius=3, fill=c["color"])
                draw.text((x1 + 60, y1 + 38), c["title"], font=font_card_lbl, fill=c["color"])
                
                # Animated Counter rolling up
                count_p = min(1.0, (t - c["start"]) / 1.6)
                curr_count = int(c["max_val"] * ease_out_cubic(count_p))
                val_text = f"{curr_count:,}".replace(",", ".")
                
                draw.text((x1 + 50, y1 + 100), f"{val_text} {c['unit']}", font=font_val, fill=(255, 255, 255))
                draw.text((x1 + 50, y1 + 215), c["sub"], font=font_card_sub, fill=(148, 163, 184))
                
                # Subtle progress indicator bar inside card
                bar_x1 = x1 + 50
                bar_y = y2 - 35
                bar_x2 = x2 - 50
                draw.line((bar_x1, bar_y, bar_x2, bar_y), fill=(30, 41, 59), width=4)
                active_x2 = bar_x1 + int((bar_x2 - bar_x1) * count_p)
                draw.line((bar_x1, bar_y, active_x2, bar_y), fill=c["color"], width=4)
                
        # 5. Footer Audio Waveform Tracker
        footer_y = HEIGHT - 140
        draw.line((80, footer_y, WIDTH - 80, footer_y), fill=(30, 41, 59), width=1)
        draw.text((80, footer_y + 25), "GEMINI NATIVE AUDIO // AOEDE NATURAL 1.0X", font=font_tag, fill=(100, 116, 139))
        
        # Write frame to FFmpeg pipe
        frame_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        proc.stdin.write(frame_bgr.tobytes())
        
        if f % 120 == 0:
            print(f"  Rendered {f}/{TOTAL_FRAMES} frames ({(f/TOTAL_FRAMES)*100:.1f}%)...")
            
    proc.stdin.close()
    proc.wait()
    print("Video encoding complete!")
    
    # Mux with Voiceover
    print("Muxing with voiceover audio...")
    cmd_mux = (
        f'ffmpeg -i "{raw_video}" -i "{vo_audio}" '
        f'-c:v copy -c:a aac -b:a 256k -shortest "{master_video}" -y'
    )
    subprocess.run(cmd_mux, shell=True, check=True)
    print(f"Final Educational Motion Graphic Video: {master_video}")
    
    # Extract audit frame
    audit_frame = os.path.join(out_dir, "audit_edu_neuro_frame.png")
    subprocess.run(f'ffmpeg -ss 4.0 -i "{master_video}" -vframes 1 -q:v 2 "{audit_frame}" -y', shell=True, check=True)
    print(f"Audit frame saved: {audit_frame}")

if __name__ == '__main__':
    render_neuro_video()
