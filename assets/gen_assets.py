#!/usr/bin/env python3
"""Generate Melta Labs brand binary assets (icons + OG image) with Pillow.
Run: python3 assets/gen_assets.py  (from repo root)"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

NAVY_900 = (10, 31, 60)     # #0A1F3C
NAVY_800 = (14, 42, 78)     # #0E2A4E
ACCENT   = (30, 99, 216)    # #1E63D8
WHITE    = (255, 255, 255)
MUTED    = (160, 178, 204)

# 'M' monogram polyline on a /64 grid (matches favicon.svg)
M_PTS = [(14, 46), (14, 20), (32, 35), (50, 20), (50, 46)]
SUPER = 4  # supersample factor for crisp anti-aliasing


def _scale_pts(box, ox, oy):
    """Scale the /64 M points into a square of side `box` at offset (ox,oy)."""
    return [(ox + x / 64.0 * box, oy + y / 64.0 * box) for (x, y) in M_PTS]


def draw_mark(draw, box, ox, oy, stroke=WHITE):
    pts = _scale_pts(box, ox, oy)
    w = max(2, int(round(5.5 / 64.0 * box)))
    draw.line(pts, fill=stroke, width=w, joint="curve")
    r = w / 2.0
    for (x, y) in pts:  # round the caps/joints
        draw.ellipse([x - r, y - r, x + r, y + r], fill=stroke)


def rounded_tile(size, bg, radius_ratio=0.22, content_ratio=1.0, stroke=WHITE,
                 full_bleed=False):
    """Return an RGBA tile image of side `size` with the M monogram."""
    s = size * SUPER
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if full_bleed:
        d.rectangle([0, 0, s, s], fill=bg)
    else:
        rad = int(radius_ratio * s)
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=rad, fill=bg)
    box = s * content_ratio
    off = (s - box) / 2.0
    draw_mark(d, box, off, off, stroke=stroke)
    return img.resize((size, size), Image.LANCZOS)


def save_png(img, name):
    p = os.path.join(ASSETS, name)
    img.save(p, "PNG")
    print("wrote", os.path.relpath(p, ROOT))


def load_font(paths, size):
    for p, idx in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=idx)
            except Exception:
                continue
    return ImageFont.load_default()


BOLD = [("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
        ("/System/Library/Fonts/HelveticaNeue.ttc", 0),
        ("/System/Library/Fonts/Helvetica.ttc", 0),
        ("/Library/Fonts/Arial Bold.ttf", 0)]
REG = [("/System/Library/Fonts/Supplemental/Arial.ttf", 0),
       ("/System/Library/Fonts/Helvetica.ttc", 0),
       ("/System/Library/Fonts/SFNS.ttf", 0)]

# ---- App / favicon icons -----------------------------------------------------
# Rounded navy tiles on transparent (manifest "any", logo)
for size, name in [(192, "icon-192.png"), (512, "icon-512.png"),
                   (512, "logo-512.png")]:
    save_png(rounded_tile(size, NAVY_800), name)

# Maskable: full-bleed navy, M kept inside ~62% safe zone
save_png(rounded_tile(512, NAVY_800, content_ratio=0.62, full_bleed=True),
         "icon-maskable-512.png")

# Apple touch icon: full-bleed navy square (Apple applies its own mask).
# Referenced at site ROOT (/apple-touch-icon.png), so write it there.
_apple = rounded_tile(180, NAVY_800, content_ratio=0.78, full_bleed=True)
_apple_path = os.path.join(ROOT, "apple-touch-icon.png")
_apple.save(_apple_path, "PNG")
print("wrote", os.path.relpath(_apple_path, ROOT))

# Favicon .ico (multi-size) + 32px png, written to repo ROOT
master = rounded_tile(256, NAVY_800)
ico_path = os.path.join(ROOT, "favicon.ico")
master.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote", os.path.relpath(ico_path, ROOT))

# ---- OG / social card 1200x630 ----------------------------------------------
def make_og():
    W, H = 1200, 630
    s = SUPER
    img = Image.new("RGB", (W * s, H * s), NAVY_900)
    d = ImageDraw.Draw(img)
    # subtle accent rule top
    d.rectangle([0, 0, W * s, 8 * s], fill=ACCENT)

    f_brand = load_font(BOLD, 96 * s)
    f_tag = load_font(REG, 40 * s)
    f_dom = load_font(REG, 30 * s)

    # Monogram tile (rounded navy-800 with subtle accent border), left-aligned block
    tile = 150
    margin = 96
    cy = H // 2
    tile_img = rounded_tile(tile, NAVY_800)
    # paste centered group: tile at top, text to the right
    brand = "Melta Labs"
    tag = "Software Development Company"
    dom = "meltalabs.com"

    bb = d.textbbox((0, 0), brand, font=f_brand)
    brand_h = bb[3] - bb[1]
    tb = d.textbbox((0, 0), tag, font=f_tag)

    text_x = (margin + tile + 40) * s
    # vertically center the brand+tag block
    block_h = brand_h + 28 * s + (tb[3] - tb[1])
    top = (H * s - block_h) // 2

    d.text((text_x, top - bb[1]), brand, font=f_brand, fill=WHITE)
    # accent underline under brand
    brand_w = bb[2] - bb[0]
    d.rectangle([text_x, top + brand_h + 12 * s, text_x + min(brand_w, 360 * s),
                 top + brand_h + 18 * s], fill=ACCENT)
    d.text((text_x, top + brand_h + 30 * s - tb[1]), tag, font=f_tag, fill=MUTED)

    # domain bottom-left
    d.text((margin * s, (H - 70) * s), dom, font=f_dom, fill=MUTED)

    img = img.resize((W, H), Image.LANCZOS)
    # paste tile vertically centered on the left
    ty = (H - tile) // 2
    img.paste(tile_img, (margin, ty), tile_img)
    p = os.path.join(ASSETS, "og-image.png")
    img.save(p, "PNG", optimize=True)
    print("wrote", os.path.relpath(p, ROOT))


make_og()
print("done")
