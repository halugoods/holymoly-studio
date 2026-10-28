#!/usr/bin/env python3
"""
Test Vector Mockup Renderer for Samsung Galaxy Z Flip 3
- Canvas: 1080x1920 (9:16)
- Center-aligned phone mockup with realistic bezels, rounded corners, punch-hole camera, and drop shadow
- Animated vertical scrolling grid background with soft Gaussian blur
- Zero subtitles/HUD badges
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

def create_scrolling_grid_background(width, height, offset_y, grid_size=64, base_color=(15, 18, 24), line_color=(45, 55, 70), blur_radius=2.5):
    """Creates a sleek studio backdrop with an out-of-focus scrolling grid"""
    bg = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(bg)

    # Subtle vertical gradient / vignette
    # Draw vertical lines
    for x in range(0, width + grid_size, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)

    # Draw moving horizontal lines (scrolling vertically)
    start_y = int(offset_y % grid_size) - grid_size
    for y in range(start_y, height + grid_size, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)

    # Apply soft depth-of-field blur to grid
    if blur_radius > 0:
        bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Add a soft radial glow / spotlight in center
    center_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(center_glow)
    glow_draw.ellipse([width//2 - 400, height//2 - 600, width//2 + 400, height//2 + 600], fill=(35, 45, 60, 40))
    center_glow = center_glow.filter(ImageFilter.GaussianBlur(radius=80))
    bg.paste(center_glow, (0, 0), center_glow)

    return bg

def render_zflip3_mockup(screen_img, canvas_w=1080, canvas_h=1920, scale=1.0):
    """
    Renders the screen image inside a precision-crafted Samsung Galaxy Z Flip 3 vector mockup
    Screen native: 1080x2640 -> scaled to fit mockup
    """
    # Base dimensions at scale 1.0
    screen_w = int(700 * scale)
    screen_h = int(1710 * scale)
    bezel = int(15 * scale)
    phone_w = screen_w + 2 * bezel
    phone_h = screen_h + 2 * bezel
    
    corner_radius_outer = int(46 * scale)
    corner_radius_inner = int(32 * scale)

    # 1. Resize screen image to screen_w x screen_h
    # Convert numpy BGR to PIL RGB if needed
    if isinstance(screen_img, np.ndarray):
        screen_pil = Image.fromarray(cv2.cvtColor(screen_img, cv2.COLOR_BGR2RGB))
    else:
        screen_pil = screen_img
    screen_resized = screen_pil.resize((screen_w, screen_h), Image.Resampling.LANCZOS)

    # Mask screen to have rounded inner corners
    screen_mask = Image.new("L", (screen_w, screen_h), 0)
    mask_draw = ImageDraw.Draw(screen_mask)
    mask_draw.rounded_rectangle([0, 0, screen_w, screen_h], radius=corner_radius_inner, fill=255)
    
    screen_rounded = Image.new("RGBA", (screen_w, screen_h), (0, 0, 0, 0))
    screen_rounded.paste(screen_resized, (0, 0), screen_mask)

    # 2. Build the phone body (outer bezel + shadow)
    # Extra padding for drop shadow
    pad = 60
    phone_canvas_w = phone_w + 2 * pad
    phone_canvas_h = phone_h + 2 * pad
    phone_canvas = Image.new("RGBA", (phone_canvas_w, phone_canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(phone_canvas)

    # Draw soft drop shadow
    shadow_mask = Image.new("RGBA", (phone_canvas_w, phone_canvas_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_mask)
    s_draw.rounded_rectangle(
        [pad, pad, pad + phone_w, pad + phone_h],
        radius=corner_radius_outer,
        fill=(0, 0, 0, 140)
    )
    shadow_blurred = shadow_mask.filter(ImageFilter.GaussianBlur(radius=22))
    phone_canvas.paste(shadow_blurred, (0, 4), shadow_blurred)

    # Outer phone rim (Armor Aluminum chassis - dark titanium finish)
    phone_x1 = pad
    phone_y1 = pad
    phone_x2 = pad + phone_w
    phone_y2 = pad + phone_h

    # Chassis outer rim (subtle metallic border)
    draw.rounded_rectangle(
        [phone_x1, phone_y1, phone_x2, phone_y2],
        radius=corner_radius_outer,
        fill=(38, 42, 48), # Metallic chassis body
        outline=(70, 75, 85), # Specular chamfer edge
        width=int(max(1, 2 * scale))
    )

    # Inner bezel (matte black rubber buffer around foldable screen)
    inner_bezel_x1 = phone_x1 + int(2 * scale)
    inner_bezel_y1 = phone_y1 + int(2 * scale)
    inner_bezel_x2 = phone_x2 - int(2 * scale)
    inner_bezel_y2 = phone_y2 - int(2 * scale)
    draw.rounded_rectangle(
        [inner_bezel_x1, inner_bezel_y1, inner_bezel_x2, inner_bezel_y2],
        radius=corner_radius_outer - int(2 * scale),
        fill=(16, 18, 22) # Matte black bezel
    )

    # Side buttons (Right edge: Power / Fingerprint + Volume rocker)
    btn_x = phone_x2
    btn_w = int(3 * scale)
    # Volume rocker
    vol_y1 = phone_y1 + int(280 * scale)
    vol_y2 = phone_y1 + int(420 * scale)
    draw.rounded_rectangle([btn_x, vol_y1, btn_x + btn_w, vol_y2], radius=int(2 * scale), fill=(60, 65, 75))
    # Power button
    pwr_y1 = phone_y1 + int(460 * scale)
    pwr_y2 = phone_y1 + int(560 * scale)
    draw.rounded_rectangle([btn_x, pwr_y1, btn_x + btn_w, pwr_y2], radius=int(2 * scale), fill=(60, 65, 75))

    # Hinge caps (Left & Right edge subtle indicators at Y center)
    hinge_cy = phone_y1 + phone_h // 2
    hinge_h = int(24 * scale)
    # Left hinge cap
    draw.rectangle([phone_x1 - int(1 * scale), hinge_cy - hinge_h//2, phone_x1 + int(4 * scale), hinge_cy + hinge_h//2], fill=(45, 50, 58))
    # Right hinge cap
    draw.rectangle([phone_x2 - int(4 * scale), hinge_cy - hinge_h//2, phone_x2 + int(1 * scale), hinge_cy + hinge_h//2], fill=(45, 50, 58))

    # Paste the rounded screen inside the bezel
    screen_paste_x = phone_x1 + bezel
    screen_paste_y = phone_y1 + bezel
    phone_canvas.paste(screen_rounded, (screen_paste_x, screen_paste_y), screen_rounded)

    # Punch-hole front camera (Infinity-O at center top of screen)
    cam_cx = screen_paste_x + screen_w // 2
    cam_cy = screen_paste_y + int(26 * scale)
    cam_r = int(9 * scale)
    # Camera outer dark ring
    draw.ellipse([cam_cx - cam_r, cam_cy - cam_r, cam_cx + cam_r, cam_cy + cam_r], fill=(10, 10, 12))
    # Camera inner glass lens reflection
    lens_r = int(4 * scale)
    draw.ellipse([cam_cx - lens_r, cam_cy - lens_r, cam_cx + lens_r, cam_cy + lens_r], fill=(20, 30, 45))
    draw.ellipse([cam_cx - int(2*scale), cam_cy - int(2*scale), cam_cx, cam_cy], fill=(60, 80, 110))

    # Top earpiece speaker slit in top bezel
    speaker_w = int(48 * scale)
    speaker_h = int(3 * scale)
    spk_x1 = phone_x1 + (phone_w - speaker_w) // 2
    spk_y = phone_y1 + int(6 * scale)
    draw.rounded_rectangle([spk_x1, spk_y, spk_x1 + speaker_w, spk_y + speaker_h], radius=1, fill=(25, 28, 32))

    return phone_canvas, phone_canvas_w, phone_canvas_h

def composite_frame(screen_frame, frame_idx, canvas_w=1080, canvas_h=1920, scale=1.0):
    # 1. Background with scrolling blurred grid
    scroll_speed = 2.0 # pixels per frame
    offset_y = frame_idx * scroll_speed
    canvas = create_scrolling_grid_background(canvas_w, canvas_h, offset_y=offset_y, grid_size=60, blur_radius=2.2)

    # 2. Render phone mockup
    phone_img, pw, ph = render_zflip3_mockup(screen_frame, canvas_w, canvas_h, scale=scale)

    # 3. Paste phone strictly centered in canvas
    paste_x = (canvas_w - pw) // 2
    paste_y = (canvas_h - ph) // 2
    canvas.paste(phone_img, (paste_x, paste_y), phone_img)

    return canvas

def main():
    video_path = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/fnb_catalog_24s_synced.mp4")
    cap = cv2.VideoCapture(str(video_path))
    cap.set(cv2.CAP_PROP_POS_MSEC, 5000) # Seek to 5.0s
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to read video frame!")
        return

    print("Read frame:", frame.shape)
    result = composite_frame(frame, frame_idx=60, scale=1.0)
    
    out_path = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/test_mockup_preview.png")
    result.save(str(out_path))
    print(f"Saved preview to: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
