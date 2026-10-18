"""One-off: app icons and the social sharing image (docs/icons/*, docs/og.jpg), in the programme-sheet style."""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageChops
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "docs"; F = ROOT / "tools/fonts"; (D / "icons").mkdir(parents=True, exist_ok=True)
INDIGO, PAPER, INK, MUTED = (37, 34, 98), (241, 240, 235), (36, 35, 47), (93, 93, 107)
B = {"b1": (76, 179, 160), "b2": (169, 219, 240), "b3": (43, 90, 174), "b4": (238, 78, 60), "b5": (234, 180, 211), "b6": (240, 106, 46)}
SERIF = str(F / "source-serif-4-latin-600-normal.ttf"); ITAL = str(F / "source-serif-4-latin-400-italic.ttf")
SANS = str(F / "libre-franklin-latin-500-normal.ttf"); SANSB = str(F / "libre-franklin-latin-700-normal.ttf")

def mark(size, pad=0.0, radius=0.05):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=INDIGO)
    m = S * (0.2 + pad); w = S * 0.065
    top, bl, br = (S / 2, m), (m, S - m), (S - m, S - m)
    d.polygon([top, br, bl], outline=PAPER, width=int(w))
    y = S * 0.62; k = (y - m) / (S - 2 * m)
    x0 = S / 2 - k * (S / 2 - m); x1 = S / 2 + k * (S / 2 - m)
    d.line([(S / 2, m + 2 * w), (S / 2, S - m - w)], fill=B["b2"], width=int(w * 0.5))
    d.line([(x0 + w * 0.5, y), (x1 - w * 0.5, y)], fill=B["b6"], width=int(w))
    return im.resize((size, size), Image.LANCZOS)

mark(192).save(D / "icons/icon-192.png"); mark(512).save(D / "icons/icon-512.png")
mark(180, radius=0).convert("RGB").save(D / "icons/apple-touch-icon.png")
mark(512, pad=0.08, radius=0).save(D / "icons/maskable-512.png")
mark(48).save(D / "favicon.png")

# social image 1200x630: a programme sheet
W, H = 1200, 630
im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
L, R = 64, W - 64
d.line([(L, 56), (R, 56)], fill=(154, 153, 163), width=2)
d.text((L, 70), "Artizanni", font=ImageFont.truetype(SANSB, 19), fill=INK)
d.text((L, 96), "Design-build since 2012 · RC 1065469", font=ImageFont.truetype(SANS, 17), fill=MUTED)
for i, (wf, off) in enumerate([(1, 0), (.6, .12), (.46, .4), (.36, .22)]):
    d.rectangle([470 + off * 70, 74 + i * 9, 470 + off * 70 + 70 * wf, 77 + i * 9], fill=(138, 138, 150))
d.text((R - 150, 70), "artizanni.com", font=ImageFont.truetype(SANSB, 19), fill=INK)
d.text((L, 150), "Designed, engineered and built", font=ImageFont.truetype(SERIF, 58), fill=INDIGO)
d.text((L, 222), "by one accountable team.", font=ImageFont.truetype(ITAL, 58), fill=B["b3"])
# gridlines + gantt bars (multiply overlaps, as in the reference)
gx0, gx1, gy = L, R, 330
for k in range(5):
    x = gx0 + (gx1 - gx0) * k / 4; d.line([(x, gy), (x, H - 40)], fill=(222, 221, 215), width=1)
labs = ["PRE-CONTRACT", "PRE-CONTRACT", "POST-CONTRACT", "POST-CONTRACT"]
for k, t in enumerate(labs):
    d.text((gx0 + (gx1 - gx0) * k / 4 + 8, gy + 4), t, font=ImageFont.truetype(SANS, 13), fill=(138, 138, 150))
bars = [(0, 17, "b1", "01 Brief"), (10, 21, "b2", "02 Design"), (24, 19, "b3", "03 Quantities"), (45, 33, "b4", "04 Construction"), (74, 11, "b5", "05 Handover"), (82, 18, "b6", "06 Aftercare")]
layer = Image.new("RGB", (W, H), (255, 255, 255)); ld = ImageDraw.Draw(layer)
f = ImageFont.truetype(SANS, 15)
for i, (x, w, c, t) in enumerate(bars):
    y = gy + 36 + i * 36; xa = gx0 + (gx1 - gx0) * x / 100; xb = gx0 + (gx1 - gx0) * (x + w) / 100
    tmp = Image.new("RGB", (W, H), (255, 255, 255)); ImageDraw.Draw(tmp).rectangle([xa, y, xb, y + 26], fill=B[c])
    layer = ImageChops.multiply(layer, tmp)
im = ImageChops.multiply(im, layer); d = ImageDraw.Draw(im)
for i, (x, w, c, t) in enumerate(bars):
    y = gy + 36 + i * 36; xa = gx0 + (gx1 - gx0) * x / 100; xb = gx0 + (gx1 - gx0) * (x + w) / 100
    if i < 5: d.text((xa, y + 28), t, font=f, fill=INK)
    else: d.text((xb - d.textlength(t, font=f), y + 28), t, font=f, fill=INK)
im.save(D / "og.jpg", quality=88, optimize=True)
print("icons + og done")
