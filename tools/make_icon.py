"""
Icon generator for Aion2 Optimizer.
Draws a shield with a lightning bolt (network + speed) in AION 2 brand colors.
Requires: pip install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ---------- Settings ----------
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
SIZES = [16, 24, 32, 48, 64, 128, 256]

# Colors (match the UI — bg #0D1117, accent #FFD700)
BG_COLOR = (13, 17, 23, 255)        # #0D1117
SHIELD_COLOR = (255, 215, 0, 255)   # #FFD700 (AION gold)
BOLT_COLOR = (13, 17, 23, 255)      # dark background inside the bolt
ACCENT = (0, 168, 232, 255)         # #00A8E8 (network blue)


def draw_shield(size):
    """Draws a shield with a lightning bolt in the center."""
    # Render at 4x resolution for smooth anti-aliasing, then downscale
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ---- Circular background ----
    margin = int(s * 0.04)
    draw.ellipse(
        [margin, margin, s - margin, s - margin],
        fill=BG_COLOR,
        outline=ACCENT,
        width=max(1, int(s * 0.02)),
    )

    # ---- Shield ----
    cx, cy = s // 2, s // 2
    w = int(s * 0.42)   # shield width
    h = int(s * 0.50)   # shield height
    top = cy - h // 2
    bottom = cy + h // 2
    left = cx - w // 2
    right = cx + w // 2

    # Top of shield is flat, bottom comes to a point
    shield_points = [
        (left, top),                       # top-left
        (right, top),                      # top-right
        (right, top + int(h * 0.55)),      # right-middle
        (cx, bottom),                      # bottom (tip)
        (left, top + int(h * 0.55)),       # left-middle
    ]
    draw.polygon(shield_points, fill=SHIELD_COLOR)

    # ---- Lightning bolt ----
    bolt_w = int(w * 0.35)
    bolt_h = int(h * 0.55)
    bx = cx
    by = cy

    bolt_points = [
        (bx + bolt_w // 3, by - bolt_h // 2),   # top
        (bx - bolt_w // 2, by + bolt_h // 10),  # left-middle
        (bx - bolt_w // 8, by + bolt_h // 10),  # inner-left
        (bx - bolt_w // 3, by + bolt_h // 2),   # bottom
        (bx + bolt_w // 2, by - bolt_h // 10),  # right-middle
        (bx + bolt_w // 8, by - bolt_h // 10),  # inner-right
    ]
    draw.polygon(bolt_points, fill=BOLT_COLOR)

    # Downscale to target size with anti-aliasing
    return img.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # Generate all sizes
    frames = [draw_shield(s) for s in SIZES]

    # Save as a multi-layer .ico
    frames[0].save(
        OUTPUT,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=frames[1:],
    )

    print(f"✅ Icon saved: {os.path.abspath(OUTPUT)}")
    print(f"   Sizes: {', '.join(f'{s}x{s}' for s in SIZES)}")


if __name__ == "__main__":
    main()