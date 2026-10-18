"""One-off: copy curated project photos into docs/img as web-sized JPEG + WebP.
Sources are the Artizanni project photo archive (Claude Project files). Captions describe
only what is visible in each photograph. Output manifest: src/photos.json"""
import json, os, sys, pathlib
from PIL import Image, ImageOps

U = "/root/.claude/uploads/de60ba8e-6f8c-58fb-a06f-683a14d943d9"
P = "/root/.claude/projects/-home-claude/de60ba8e-6f8c-58fb-a06f-683a14d943d9/tool-results"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/img"; OUT.mkdir(parents=True, exist_ok=True)

def find(token):
    for d in (U, P):
        for f in os.listdir(d):
            if token in f and f.lower().endswith((".jpg", ".jpeg")):
                return os.path.join(d, f)
    sys.exit("missing " + token)

# key: (source token, sector, caption, crop_bottom_fraction)
PHOTOS = {
 "reclaim-aerial":   ("_28633", "drainage", "Reclamation platform and access embankment advancing across low-lying wetland, Lagos", 0),
 "reclaim-aerial-2": ("_28634", "drainage", "Aerial view of the reclamation works and channel alignment, Lagos", 0),
 "reclaim-dawn":     ("_29025", "drainage", "Sand-filled formation to the reclaimed corridor at first light", 0.06),
 "reclaim-fill":     ("_29022", "drainage", "Sand fill placed against the channel lining, with plant at the working front", 0.06),
 "reclaim-dredge":   ("_28782", "drainage", "Dredge discharge lines delivering sand fill to the platform", 0.08),
 "reclaim-stockpile":("_30109", "drainage", "Sand stockpiles and discharge point on the reclaimed area", 0.05),
 "gabion-wall":      ("_31279", "drainage", "Gabion wall with geotextile backing to the channel bank", 0),
 "gabion-lining":    ("_28751", "drainage", "Geotextile and rock lining laid along the channel", 0),
 "gabion-excavator": ("_30921", "drainage", "Excavator placing rock to the gabion revetment", 0),
 "channel-lined":    ("_28835", "drainage", "Lined channel and access corridor during construction", 0.05),
 "channel-plant":    ("_28845", "drainage", "Long-reach plant working the channel through a built-up area", 0.05),
 "channel-gabion":   ("_29020", "drainage", "Gabion revetment running the length of the channel", 0.05),
 "channel-road":     ("_28769", "roads",    "Roller and loader forming the corridor beside the new channel", 0.22),
 "corridor-roller":  ("_28771", "roads",    "Compaction of the formation alongside the gabion line", 0.22),
 "loader-gabion":    ("_29160", "roads",    "Wheel loader and aggregate at the gabion working front", 0.05),
 "excavator-fill":   ("_28775", "drainage", "Tracked excavator handling fill at the reclamation front", 0.22),
 "plant-lowbed":     ("_30140", "plant",    "Paver delivered to site on a low-bed trailer", 0),
 "cofferdam":        ("IMG_20210102_143413", "water", "Cofferdam of geomembrane and rock armour in a live watercourse", 0),
 "cofferdam-2":      ("IMG_20210102_143408", "water", "Cofferdam alignment against the barrage structure", 0),
 "cofferdam-armour": ("IMG_20201230_174820", "water", "Bagged fill and rock armour forming the cofferdam face", 0),
 "causeway":         ("WhatsApp_Image_20220104", "water", "Temporary causeway across the channel, viewed from the structure", 0),
 "reservoir":        ("20181215_133326", "water", "Impounded reservoir upstream of a dam structure", 0),
 "dewater-apron":    ("IMG20180707WA0056", "water", "Dewatered apron with starter bars set for new concrete", 0),
 "dewater-pump":     ("IMG20210314WA0016", "water", "Dewatering pump drawing down the work area", 0),
 "geomembrane":      ("IMG20210412WA0065", "water", "Geomembrane being laid against the existing structure", 0),
 "trench-rebar":     ("IMG20180531WA0020", "power", "Reinforcement fixed in a cable trench", 0),
 "trench-rebar-2":   ("IMG20180531WA0019", "power", "Steel fixing in a reinforced concrete trench", 0),
 "deck-tower":       ("IMG20180808WA0008", "power", "Deck formwork with an HV transmission tower beyond", 0),
 "stone-rebar":      ("20180616_183808", "water", "Rock fill and reinforcement at the works front", 0),
 # buildings
 "duplex-1":   ("_11664", "residential", "Detached duplex with stone-coated roof during external finishing", 0),
 "duplex-2":   ("_11797", "residential", "Entrance bay and sweeping stair under construction", 0),
 "duplex-3":   ("_11888", "residential", "Arched openings and moulded entrance bay before render", 0),
 "duplex-4":   ("_11886", "residential", "Duplex at roof completion with scaffold retained", 0),
 "duplex-5":   ("_12041", "residential", "Classical duplex frontage during finishing", 0),
 "duplex-6":   ("_11737", "residential", "Two-storey home, render and glazing in progress", 0),
 "brick-clad": ("_11740", "residential", "Facing brick plinth and arched windows on completion", 0),
 "unit-3":     ("_11799", "residential", "Three-storey block with scaffold to the façade", 0),
 "roof-tile":  ("_11743", "interiors", "Stone-coated roof sheet: profile detail", 0),
 "slab-1":     ("_12081", "structures", "Suspended slab reinforcement ready for inspection", 0),
 "slab-2":     ("_12087", "structures", "Two-way reinforcement across the deck", 0),
 "slab-3":     ("_12260", "structures", "Deck reinforcement over a long-span frame", 0),
 "stair-1":    ("_12079", "structures", "Stair flight formed in the deck", 0),
 "stair-2":    ("_12083", "structures", "Reinforcement to a cast stair flight", 0),
 "frame-1":    ("_11658", "structures", "Frame interior with formwork and props", 0),
 "frame-2":    ("_11726", "structures", "Columns and blockwork rising across the plot", 0),
 "frame-3":    ("_11994", "structures", "Lintels and blockwork between structural columns", 0),
 "frame-4":    ("_12016", "structures", "Column cages and blockwork at first floor", 0),
 "slab-edge":  ("_12266", "structures", "Slab and stair reinforcement at the deck edge", 0),
 "retail-1":   ("_12098", "commercial", "Façade cladding and signage installation from scaffold", 0),
 "retail-2":   ("_12114", "commercial", "Glazed frontage and canopy to a trading building", 0),
 "retail-3":   ("_12441", "commercial", "Paved access along the completed frontage", 0),
 "retail-4":   ("_12443", "commercial", "Completed ancillary units and covered walkway", 0),
 "coldroom-1": ("_11771", "industrial", "Insulated panel cold room, freestanding installation", 0),
 "coldroom-2": ("_11774", "industrial", "Cold room shell under a steel roof", 0),
 "coldroom-3": ("_11780", "industrial", "Lit chilled store interior on completion", 0),
 "panel-1":    ("_11790", "industrial", "Panel-clad process building with loading doors", 0),
 "panel-2":    ("_11791", "industrial", "Loading canopies to the process hall", 0),
 "yard-1":     ("_12283", "industrial", "Covered storage bay under a long-span canopy", 0),
 "yard-2":     ("_12284", "industrial", "Logistics yard and hardstanding", 0),
 "int-1":      ("_12125", "interiors", "Polished floor and feature colour wall on completion", 0),
 "int-2":      ("_12126", "interiors", "Production area with stainless equipment and colour-blocked walls", 0),
 "int-3":      ("_12127", "interiors", "Colour blocking to the sales floor", 0),
 "int-4":      ("_12132", "interiors", "Shelving system being installed", 0),
 "int-5":      ("_12134", "interiors", "Sales floor with gondola units positioned", 0),
 "int-6":      ("_12201", "interiors", "Granite worktop and tiled base", 0),
 "int-7":      ("_12202", "interiors", "Polished stone counter installation", 0),
 "site-1":     ("_11801", "design", "Setting out and excavation to foundation lines", 0),
 "site-2":     ("_12281", "design", "Site survey on an undeveloped plot", 0),
}

def save(src, key, crop):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if crop:
        w, h = im.size; im = im.crop((0, 0, w, int(h * (1 - crop))))
    meta = {}
    for wmax in (1600, 800):
        c = im.copy(); c.thumbnail((wmax, wmax), Image.LANCZOS)
        c.save(OUT / f"{key}-{wmax}.jpg", quality=78, optimize=True, progressive=True)
        c.save(OUT / f"{key}-{wmax}.webp", quality=74, method=5)
        if wmax == 1600: meta = {"w": c.width, "h": c.height}
    return meta

man = {}
for key, (tok, sector, cap, crop) in PHOTOS.items():
    m = save(find(tok), key, crop)
    man[key] = {"sector": sector, "caption": cap, **m}
(ROOT / "src/photos.json").write_text(json.dumps(man, indent=1))
tot = sum(f.stat().st_size for f in OUT.iterdir())
print(len(man), "photos,", round(tot / 1e6, 1), "MB")
