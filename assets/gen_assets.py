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

# Brand mark: white "melta" wordmark (or "m" monogram at small sizes) in
# Plus Jakarta Sans ExtraBold on an accent-blue tile. Font is vendored (OFL).
FONT = os.path.join(ASSETS, "fonts", "PlusJakartaSans-Variable.ttf")
SUPER = 4  # supersample factor for crisp anti-aliasing


def brand_font(size):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([800])  # ExtraBold
    return f


def draw_word(draw, text, box, ox, oy, fill=WHITE, ink_ratio=0.80):
    """Draw `text` so its ink spans `ink_ratio` of a `box` square, centred."""
    f = brand_font(1000)
    kern = -0.03 * 1000
    widths = [f.getlength(ch) for ch in text]
    total = sum(widths) + kern * (len(text) - 1)
    # ink bounds of the whole run (first/last glyph side-bearings)
    l0 = f.getbbox(text[0])[0]
    r1 = widths[-1] - f.getbbox(text[-1])[2]
    ink_w = total - l0 - r1
    top = min(f.getbbox(ch)[1] for ch in text)
    bot = max(f.getbbox(ch)[3] for ch in text)
    k = box * ink_ratio / ink_w
    f = brand_font(max(1, int(round(1000 * k))))
    k = f.size / 1000.0
    x = ox + (box - ink_w * k) / 2 - l0 * k
    y = oy + (box - (bot - top) * k) / 2 - top * k
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += (w + kern) * k


def rounded_tile(size, bg=None, radius_ratio=0.22, content_ratio=1.0,
                 full_bleed=False, text="melta"):
    """Return an RGBA tile of side `size` with the wordmark (or monogram)."""
    bg = bg or ACCENT
    s = size * SUPER
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if full_bleed:
        d.rectangle([0, 0, s, s], fill=bg)
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(radius_ratio * s), fill=bg)
    box = s * content_ratio
    off = (s - box) / 2.0
    draw_word(d, text, box, off, off, ink_ratio=0.80 if text != "m" else 0.66)
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
# Rounded accent tiles on transparent (manifest "any", logo)
for size, name in [(192, "icon-192.png"), (512, "icon-512.png"),
                   (512, "logo-512.png")]:
    save_png(rounded_tile(size), name)

# Slack / social avatar: full-bleed 1024 (platforms apply their own mask)
save_png(rounded_tile(1024, full_bleed=True), "avatar-1024.png")

# Maskable: full-bleed, wordmark kept inside the ~80% safe zone
save_png(rounded_tile(512, content_ratio=0.80, full_bleed=True),
         "icon-maskable-512.png")

# Apple touch icon: full-bleed square (Apple applies its own mask).
# Referenced at site ROOT (/apple-touch-icon.png), so write it there.
_apple = rounded_tile(180, full_bleed=True)
_apple_path = os.path.join(ROOT, "apple-touch-icon.png")
_apple.save(_apple_path, "PNG")
print("wrote", os.path.relpath(_apple_path, ROOT))

# Favicon .ico (16/32/48): "m" monogram, the full word is illegible that small
master = rounded_tile(256, text="m")
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

    # Wordmark tile (rounded accent blue), left-aligned block
    tile = 150
    margin = 96
    cy = H // 2
    tile_img = rounded_tile(tile)
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
