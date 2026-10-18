"""One-off: app icons and the social sharing image (docs/icons/*, docs/og.jpg). Needs Pillow and Poppins fonts."""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs"; (D / "icons").mkdir(parents=True, exist_ok=True)
GOLD, INK, CREAM = (201, 151, 58), (26, 26, 26), (250, 247, 242)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
import os
if not os.path.exists(FB): FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"

def mark(size, pad=0.0, radius=0.08):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=INK)
    m = S * (0.18 + pad); w = S * 0.075
    top, bl, br = (S / 2, m), (m, S - m), (S - m, S - m)
    d.polygon([top, br, bl], outline=GOLD, width=int(w))
    y = S * 0.62
    k = (y - m) / (S - 2 * m)
    x0 = S / 2 - k * (S / 2 - m); x1 = S / 2 + k * (S / 2 - m)
    d.line([(x0 + w * 0.5, y), (x1 - w * 0.5, y)], fill=GOLD, width=int(w * 0.8))
    d.line([(S / 2, m + 2 * w), (S / 2, S - m - w)], fill=GOLD + (150,), width=int(w * 0.35))
    return im.resize((size, size), Image.LANCZOS)

mark(192).save(D / "icons/icon-192.png"); mark(512).save(D / "icons/icon-512.png")
mark(180, radius=0).convert("RGB").save(D / "icons/apple-touch-icon.png")
mark(512, pad=0.08, radius=0).save(D / "icons/maskable-512.png")
mark(48).save(D / "favicon.png")

# social image 1200x630
ph = ImageOps.exif_transpose(Image.open(D / "img/reclaim-aerial-1600.jpg")).convert("RGB")
ph = ImageOps.fit(ph, (1200, 630), centering=(0.5, 0.55))
ph = ImageEnhance.Brightness(ph).enhance(0.55)
ov = Image.new("RGBA", (1200, 630), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for y in range(630): od.line([(0, y), (1200, y)], fill=(26, 26, 26, int(200 * y / 630)))
ph = Image.alpha_composite(ph.convert("RGBA"), ov)
ph.alpha_composite(mark(96), (64, 64))
d = ImageDraw.Draw(ph)
d.text((180, 78), "ARTIZANNI", font=ImageFont.truetype(FB, 44), fill=CREAM)
d.text((182, 130), "BUSINESS SERVICES LTD · RC 1065469", font=ImageFont.truetype(FM, 17), fill=GOLD)
f = ImageFont.truetype(FB, 54)
d.text((64, 380), "Designed, engineered and built", font=f, fill=CREAM)
d.text((64, 446), "by one accountable team.", font=f, fill=CREAM)
d.text((64, 540), "Abuja · since 2012 · design-build · interiors · real estate · build from abroad", font=ImageFont.truetype(FM, 22), fill=(230, 214, 180))
d.rectangle([64, 356, 164, 360], fill=GOLD)
ph.convert("RGB").save(D / "og.jpg", quality=84, optimize=True)
print("icons + og done")
