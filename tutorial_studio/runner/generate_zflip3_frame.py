#!/usr/bin/env python3
"""
Generate precision Samsung Galaxy Z Flip 3 Frame Asset (1080x1920 RGBA)
With:
- Screen window cutout: 700 x 1710 at (190, 105) with rounded corners (r=32)
- Outer chassis: 730 x 1740 at (175, 90) with outer rounded corners (r=46)
- Armor Aluminum dark metallic frame + specular edges
- Infinity-O camera punch-hole + glass lens reflection
- Top ear-speaker slit
- Side volume & power buttons
- Soft Gaussian drop shadow
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

def generate_zflip3_overlay(canvas_w=1080, canvas_h=1920):
    screen_w = 700
    screen_h = 1710
    bezel = 15
    phone_w = screen_w + 2 * bezel # 730
    phone_h = screen_h + 2 * bezel # 1740
    
    screen_x = (canvas_w - screen_w) // 2 # 190
    screen_y = (canvas_h - screen_h) // 2 # 105
    phone_x = (canvas_w - phone_w) // 2   # 175
    phone_y = (canvas_h - phone_h) // 2   # 90
    
    corner_outer = 46
    corner_inner = 32

    # Canvas RGBA
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # 1. Realistic Multi-Layer Drop Shadow
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    # Ambient soft shadow
    s_draw.rounded_rectangle(
        [phone_x - 5, phone_y - 2, phone_x + phone_w + 5, phone_y + phone_h + 10],
        radius=corner_outer + 5,
        fill=(0, 0, 0, 160)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=26))
    canvas.paste(shadow, (0, 8), shadow)

    # Tight contact shadow
    contact = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(contact)
    c_draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_w, phone_y + phone_h],
        radius=corner_outer,
        fill=(0, 0, 0, 140)
    )
    contact = contact.filter(ImageFilter.GaussianBlur(radius=10))
    canvas.paste(contact, (0, 4), contact)

    # 2. Side Buttons (Right Edge: Volume rocker & Power button)
    btn_x = phone_x + phone_w
    btn_w = 4
    draw = ImageDraw.Draw(canvas)
    # Volume
    draw.rounded_rectangle([btn_x, phone_y + 280, btn_x + btn_w, phone_y + 420], radius=2, fill=(65, 70, 80))
    # Power
    draw.rounded_rectangle([btn_x, phone_y + 460, btn_x + btn_w, phone_y + 560], radius=2, fill=(65, 70, 80))

    # 3. Outer Phone Body (Armor Aluminum dark titanium finish)
    draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_w, phone_y + phone_h],
        radius=corner_outer,
        fill=(32, 35, 42),
        outline=(78, 86, 98),
        width=2
    )

    # 4. Inner Bezel Cushion (Matte black rubber gasket around folding screen)
    draw.rounded_rectangle(
        [phone_x + 3, phone_y + 3, phone_x + phone_w - 3, phone_y + phone_h - 3],
        radius=corner_outer - 3,
        fill=(14, 16, 20)
    )

    # 5. Hinge Protection Caps (Middle left & right edges)
    h_cy = phone_y + phone_h // 2
    draw.rectangle([phone_x - 1, h_cy - 12, phone_x + 5, h_cy + 12], fill=(45, 50, 58))
    draw.rectangle([phone_x + phone_w - 5, h_cy - 12, phone_x + phone_w + 1, h_cy + 12], fill=(45, 50, 58))

    # 6. Top Earpiece Speaker Slit
    spk_w = 48
    spk_x = phone_x + (phone_w - spk_w) // 2
    spk_y = phone_y + 6
    draw.rounded_rectangle([spk_x, spk_y, spk_x + spk_w, spk_y + 3], radius=1, fill=(26, 28, 34))

    # 7. Screen Cutout (Transparent Hole with rounded corners)
    screen_mask = Image.new("L", (canvas_w, canvas_h), 255)
    m_draw = ImageDraw.Draw(screen_mask)
    m_draw.rounded_rectangle(
        [screen_x, screen_y, screen_x + screen_w, screen_y + screen_h],
        radius=corner_inner,
        fill=0
    )
    
    # Apply cutout mask to alpha channel of canvas
    r, g, b, a = canvas.split()
    a_new = Image.fromarray(np.minimum(np.array(a), np.array(screen_mask)))
    canvas = Image.merge("RGBA", (r, g, b, a_new))
    draw = ImageDraw.Draw(canvas)

    # 8. Front Camera Punch-hole (Infinity-O at center top of screen)
    cam_cx = screen_x + screen_w // 2
    cam_cy = screen_y + 28
    cam_r = 9
    # Camera outer dark gasket
    draw.ellipse([cam_cx - cam_r, cam_cy - cam_r, cam_cx + cam_r, cam_cy + cam_r], fill=(12, 14, 18, 255))
    # Camera inner glass lens
    draw.ellipse([cam_cx - 5, cam_cy - 5, cam_cx + 5, cam_cy + 5], fill=(24, 34, 52, 255))
    # Specular lens glint
    draw.ellipse([cam_cx - 2, cam_cy - 2, cam_cx, cam_cy], fill=(85, 110, 150, 255))

    out_file = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/zflip3_frame.png")
    canvas.save(str(out_file), "PNG")
    print(f"[Overlay] Saved precision Z Flip 3 frame to: {out_file} ({out_file.stat().st_size / 1024:.1f} KB)")
    return out_file

if __name__ == "__main__":
    generate_zflip3_overlay()
