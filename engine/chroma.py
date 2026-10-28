#!/usr/bin/env python3
"""
Holymoly Studio - Chroma Key & Background Removal Engine
(by Halu Goods Indonesia)

Advanced border flood-fill + internal pocket cleanup + Gaussian antialiased alpha masking.
Preserves object-internal matching colors (e.g. green scooter body on green screen).
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import label


def remove_screen(
    input_path: str | Path,
    output_path: str | Path,
    tolerance: float = 70.0,
    blur_radius: float = 0.5,
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape

    # Detect reference screen color from the corners
    corners = np.array([
        arr[0, 0][:3],
        arr[0, w - 1][:3],
        arr[h - 1, 0][:3],
        arr[h - 1, w - 1][:3],
    ], dtype=float)
    bg_color = np.median(corners, axis=0)

    # Color difference from reference screen color
    diff = np.sqrt(np.sum((arr[:, :, :3].astype(float) - bg_color) ** 2, axis=2))
    is_bg = diff < tolerance

    # Connected component labeling
    labeled, num_features = label(is_bg)

    # Detect all connected components touching any of the 4 outer image borders
    border_labels = set()
    border_labels.update(np.unique(labeled[0, :]))
    border_labels.update(np.unique(labeled[h - 1, :]))
    border_labels.update(np.unique(labeled[:, 0]))
    border_labels.update(np.unique(labeled[:, w - 1]))
    border_labels.discard(0)

    # Start with outer background
    mask = np.isin(labeled, list(border_labels))

    # Detect enclosed background pockets (e.g., holes under kickstands or between spokes)
    for l in range(1, num_features + 1):
        if l not in border_labels:
            comp_diff = diff[labeled == l]
            if len(comp_diff) > 10 and np.mean(comp_diff) < (tolerance - 15):
                mask[labeled == l] = True

    # Build anti-aliased alpha mask
    alpha = (~mask).astype(np.uint8) * 255
    alpha_img = Image.fromarray(alpha, mode="L")
    if blur_radius > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    out_img = Image.fromarray(arr[:, :, :3], mode="RGB")
    out_img.putalpha(alpha_img)
    out_img.save(output_path, "PNG")

    print(f"[Holymoly Studio] Chroma key complete -> {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python chroma.py <input_image> <output_png> [tolerance]")
        sys.exit(1)
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 70.0
    remove_screen(sys.argv[1], sys.argv[2], tolerance=tol)
