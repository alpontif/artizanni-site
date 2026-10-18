"""Add every photograph used in the 2026 Project Portfolio, with its approved caption and chapter,
from the image archive (Artizanni_Project_Images.zip, INDEX_Site_Photographs.csv).
Photos already on the site keep their key; their caption and sector are replaced by the portfolio's."""
import csv, json, pathlib, sys, re
from PIL import Image, ImageOps
ROOT = pathlib.Path(__file__).resolve().parent.parent
ARCH = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corp/imgs")
OUT = ROOT / "docs/img"
SECT = {"Water Resources & Marine Works": "water", "Power Infrastructure": "power", "Drainage, Erosion Control & Reclamation": "drainage",
        "Commercial & Retail": "commercial", "Industrial, Warehousing & Cold Chain": "industrial", "Residential Development": "residential",
        "Structures in Frame": "structures", "Mechanical & Electrical": "mep", "Interiors, Fitout & Finishes": "interiors",
        "Roads, Paving & External Works": "roads", "Design & Consultancy": "consultancy"}
man = json.loads((ROOT / "src/photos.json").read_text())
# old key -> source filename token, from prep_photos.py
src = (ROOT / "tools/prep_photos.py").read_text()
old = {k: tok for k, tok in re.findall(r'"([a-z0-9-]+)":\s*\("([^"]+)"', src)}
rows = list(csv.DictReader(open(ARCH / "INDEX_Site_Photographs.csv")))
added = updated = 0
for r in rows:
    sec = SECT.get(r["Portfolio section"])
    if not sec: continue
    if r["Filename"] == "1000107501.jpg": continue          # EPC table scan, not a photo
    hit = [k for k, tok in old.items() if tok in r["Filename"]]
    if hit:
        k = hit[0]; man[k]["sector"] = sec; man[k]["caption"] = r["Caption"]; man[k]["plate"] = int(r["Plate no."]); updated += 1; continue
    k = "p" + r["Plate no."]
    im = ImageOps.exif_transpose(Image.open(ARCH / "Site_Photographs" / r["Filename"])).convert("RGB")
    meta = {}
    for w in (1600, 800):
        c = im.copy(); c.thumbnail((w, w), Image.LANCZOS)
        c.save(OUT / f"{k}-{w}.jpg", quality=78, optimize=True, progressive=True)
        c.save(OUT / f"{k}-{w}.webp", quality=74, method=5)
        if w == 1600: meta = {"w": c.width, "h": c.height}
    man[k] = {"sector": sec, "caption": r["Caption"], "plate": int(r["Plate no."]), **meta}; added += 1
(ROOT / "src/photos.json").write_text(json.dumps(man, indent=1))
print("added", added, "updated", updated, "total", len(man))
