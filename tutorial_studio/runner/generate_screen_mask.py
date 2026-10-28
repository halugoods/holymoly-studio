from PIL import Image, ImageDraw
from pathlib import Path

mask = Image.new("RGBA", (700, 1710), (0, 0, 0, 0))
draw = ImageDraw.Draw(mask)
draw.rounded_rectangle([0, 0, 700, 1710], radius=32, fill=(255, 255, 255, 255))
out_p = Path("C:/Users/ertyui/ZCodeProject/holymoly_studio/tutorial_studio/output/screen_mask_700x1710.png")
mask.save(str(out_p))
print(f"Saved {out_p}")
