#!/usr/bin/env python3
"""Build artizanni.com into docs/ (served by GitHub Pages).

    python3 build.py

Words live in src/content.py, photo captions in src/photos.json, keys and IDs in site-config.json.
Front-end files (src/style.css, app.js, pwa.js) are copied with a version stamp for cache-busting.
"""
import hashlib, html, json, pathlib, shutil, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from content import (SITE, SERVICES, DIASPORA, SECTORS, REGISTER, STAGES, MILESTONES, DIASPORA_FAQ, GENERAL_FAQ, STATES, GROUP,  # noqa
                     REGISTER_STATUS, PROFILE, PLANT, NUMBERS, JOURNEY, ENGAGEMENTS, CLIENTS)

DOCS = ROOT / "docs"
CFG = json.loads((ROOT / "site-config.json").read_text())
PH = json.loads((ROOT / "src/photos.json").read_text())
DOMAIN = CFG.get("domain") or SITE["domain"]
BASE = f"https://{DOMAIN}/"
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)

# ------------------------------------------------------------------ assets + version stamp
(DOCS / "assets").mkdir(parents=True, exist_ok=True)
h = hashlib.sha1()
for f in ("style.css", "app.js", "pwa.js"):
    b = (ROOT / "src" / f).read_bytes(); h.update(b); (DOCS / "assets" / f).write_bytes(b)
h.update((ROOT / "src/content.py").read_bytes())
V = h.hexdigest()[:10]

PAGES = []   # (path, title, priority) for sitemap / llms

# ------------------------------------------------------------------ icons (inline SVG)
MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="3" fill="#1A1A1A"/>'
        '<path d="M20 8.5 31.5 31.5h-23z" fill="none" stroke="#C9973A" stroke-width="2.6" stroke-linejoin="miter"/>'
        '<path d="M13.6 24.8h12.8" stroke="#C9973A" stroke-width="2.2"/><path d="M20 12v18" stroke="#C9973A" stroke-width="1" opacity=".6"/></svg>')
WA = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2.2a9.7 9.7 0 0 0-8.3 14.8L2.3 21.8l4.9-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-2.9.8.8-2.8-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3Z"/></svg>')
ARW = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I = lambda d: f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
ICONS = {
 "build": I('<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6M9 11h6"/>'),
 "arch": I('<path d="M3 20h18"/><path d="M5 20 12 4l7 16"/><path d="M8.5 12h7"/><circle cx="12" cy="4" r="1"/>'),
 "eng": I('<path d="M2 18h20M4 18l4-9 4 9 4-9 4 9M8 9h8"/>'),
 "crane": I('<path d="M5 21V3l14 4H5M9 7v14M3 21h8M17 7v6"/><path d="M15.5 13h3v2.5h-3z"/>'),
 "int": I('<path d="M4 20v-7a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v7M2 14h4v4H2zM18 14h4v4h-4zM6 17h12M12 4v6"/>'),
 "land": I('<path d="M3 20h18M4 20l5-8 4 5 3-4 4 7"/><path d="M15 4v6M15 4h4l-1 1.5 1 1.5h-4"/>'),
 "pm": I('<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 8h8M8 12h8M8 16h5"/><path d="m14.5 16 1.2 1.2L18 15"/>'),
 "people": I('<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 4.5a3 3 0 0 1 0 6M18 14a5 5 0 0 1 3 6"/>'),
 "shield": I('<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="M9.5 12.5 11 14l3.5-3.5"/>'),
 "globe": I('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
 "phone": I('<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>'),
 "mail": I('<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 6 9 7 9-7"/>'),
 "pin": I('<path d="M12 21s-7-6.6-7-12a7 7 0 0 1 14 0c0 5.4-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/>'),
}

# ------------------------------------------------------------------ helpers
def root_for(path):
    depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
    return "../" * depth if depth else "./"

def pic(R, key, cls="", eager=False, sizes="(max-width:760px) 100vw, 50vw", alt=None):
    p = PH[key]; a = E(alt if alt is not None else p["caption"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{R}img/{key}-800.webp 800w, {R}img/{key}-1600.webp 1600w" sizes="{sizes}">'
            f'<img src="{R}img/{key}-800.jpg" srcset="{R}img/{key}-800.jpg 800w, {R}img/{key}-1600.jpg 1600w" sizes="{sizes}" '
            f'alt="{a}" width="{p["w"]}" height="{p["h"]}" class="{cls}" {load}></picture>')

def fig(R, key, ratio="ratio-43", cap=True, lb=False, sizes="(max-width:760px) 100vw, 33vw"):
    inner = pic(R, key, sizes=sizes)
    if lb:
        inner = f'<button class="ph {ratio}" type="button" data-lb="{R}img/{key}-1600.jpg" data-cap="{E(PH[key]["caption"])}" aria-label="Enlarge: {E(PH[key]["caption"])}">{inner}</button>'
    else:
        inner = f'<div class="ph {ratio}">{inner}</div>'
    return f'<figure>{inner}{"<figcaption>" + E(PH[key]["caption"]) + "</figcaption>" if cap else ""}</figure>'

def gallery(R, keys):
    out = []
    for k in keys:
        p = PH[k]
        out.append(f'<figure><button type="button" data-lb="{R}img/{k}-1600.jpg" data-cap="{E(p["caption"])}" aria-label="Enlarge: {E(p["caption"])}">'
                   f'<div class="ph">{pic(R, k, sizes="(max-width:760px) 100vw, 33vw")}</div></button><figcaption>{E(p["caption"])}</figcaption></figure>')
    return f'<div class="gallery">{"".join(out)}</div>'

def crumbs(R, trail):
    parts = [f'<a href="{R}">Home</a>']
    for name, href in trail[:-1]:
        parts.append(f'<a href="{R}{href}">{E(name)}</a>')
    parts.append(f'<span aria-current="page">{E(trail[-1][0])}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>/</span>'.join(parts) + '</nav>'

def crumbs_ld(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    for i, (n, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": n, "item": BASE + href})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def cta(R, title="Tell us about your project.", text="Answer a few questions and send them to us on WhatsApp or email. You get a reference number straight away.", sub="", label="Start a project"):
    return f'''<section class="cta"><div class="wrap"><div><p class="eyebrow">Next step</p><h2>{E(title)}</h2><p>{E(text)}</p></div>
<div class="btns"><a class="btn btn-gold" href="{R}start/{sub}">{label} {ARW}</a><a class="btn btn-line" data-wa-quick href="https://wa.me/{SITE["whatsapp"]}">{WA}Chat on WhatsApp</a></div></div></section>'''

ORG_ID = BASE + "#org"
ORG = {
  "@type": ["Organization", "GeneralContractor"], "@id": ORG_ID, "name": "Artizanni Business Services Limited",
  "alternateName": ["Artizanni", "Artizanni Interiors"], "url": BASE, "logo": BASE + "icons/icon-512.png", "image": BASE + "og.jpg",
  "description": SITE["description"], "foundingDate": "2012-09-17", "telephone": SITE["phone_href"], "email": SITE["email"],
  "identifier": [{"@type": "PropertyValue", "propertyID": "CAC RC", "value": "1065469"}],
  "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": "Utako, Abuja", "addressRegion": "Federal Capital Territory", "addressCountry": "NG"},
  "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"][0], "longitude": SITE["geo"][1]},
  "areaServed": {"@type": "Country", "name": "Nigeria"},
  "founder": {"@type": "Person", "name": SITE["md"], "jobTitle": "Managing Director", "honorificPrefix": "Engr.",
              "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "Professional registration", "recognizedBy": {"@type": "Organization", "name": "COREN"}, "identifier": "R29685"}]},
  "knowsAbout": ["Design and build", "Architecture", "Structural engineering", "Civil engineering", "MEP engineering", "Interior design and fit-out",
                 "Land due diligence", "Project management", "Property management", "Escrow-backed construction for diaspora clients"],
  "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": SITE["phone_href"], "email": SITE["email"], "areaServed": "NG", "availableLanguage": ["en"]},
                   {"@type": "ContactPoint", "contactType": "customer service", "telephone": SITE["phone_href"], "email": SITE["alt_email"], "areaServed": "NG", "availableLanguage": ["en"]}],
}

NAV = [("Services", "services/"), ("Projects", "projects/"), ("Build from abroad", "diaspora/"), ("About", "about/"), ("Contact", "contact/")]

GA_ID = "G-9S4BZKWDJ5"
GA_TAG = (
    "<!-- Google tag (gtag.js) -->\n"
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GA_ID}');\n"
    "</script>"
)

def page(path, title, desc, body, active=None, ld=None, og=None, hero_pre="", noindex=False, prio="0.7"):
    R = root_for(path)
    canon = BASE + path
    ogimg = BASE + (f"img/{og}-1600.jpg" if og else "og.jpg")
    nav = "".join(f'<a href="{R}{href}"{" aria-current=\"page\"" if active == href else ""}>{n}</a>' for n, href in NAV)
    org = ORG
    website = {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "Artizanni", "publisher": {"@id": ORG_ID}}
    if path == "":
        org = {**ORG, "name": "Artizanni", "legalName": "Artizanni Business Services Ltd", "telephone": SITE["phone"],
               "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": "Utako District, Abuja",
                           "addressRegion": "FCT", "addressCountry": "NG"}}
        website["alternateName"] = "Artizanni Business Services"
    graph = [org, website]
    if ld: graph += ld if isinstance(ld, list) else [ld]
    verif = ""
    if CFG.get("google_site_verification"): verif += f'<meta name="google-site-verification" content="{E(CFG["google_site_verification"])}">'
    if CFG.get("bing_site_verification"): verif += f'<meta name="msvalidate.01" content="{E(CFG["bing_site_verification"])}">'
    art = json.dumps({"wa": SITE["whatsapp"], "email": SITE["email"] + "," + SITE["alt_email"], "root": R, "ga": CFG.get("ga4_measurement_id") or "", "waIcon": WA})
    full_title = title if title.startswith("Artizanni") else f"{title} | Artizanni"
    doc = f'''<!doctype html>
<html lang="en-NG">
<head>
{GA_TAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta name="theme-color" content="#1A1A1A">
<meta property="og:type" content="website"><meta property="og:site_name" content="Artizanni"><meta property="og:locale" content="en_NG">
<meta property="og:title" content="{E(full_title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{ogimg}">
<meta name="twitter:card" content="summary_large_image">
{verif}
<link rel="icon" href="{R}favicon.png" type="image/png"><link rel="apple-touch-icon" href="{R}icons/apple-touch-icon.png"><link rel="manifest" href="{R}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap">
<link rel="stylesheet" href="{R}assets/style.css?v={V}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="logo" href="{R}" aria-label="Artizanni home">{MARK}<div><b>ARTIZANNI</b><span>DESIGN · ENGINEER · BUILD</span></div></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn btn-gold btn-sm" href="{R}start/">Start a project</a></nav>
</div></header>
{hero_pre}
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="cols">
<div><a class="logo" href="{R}">{MARK}<div><b>ARTIZANNI</b><span>BUSINESS SERVICES LTD</span></div></a>
<p>Design-build, engineering, interiors and real estate. {E(SITE["address"])}.</p>
<p><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a><br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><br><a href="mailto:{SITE["alt_email"]}">{SITE["alt_email"]}</a></p></div>
<div><h4>Services</h4><ul>{"".join(f'<li><a href="{R}services/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)}<li><a href="{R}diaspora/">Build from abroad</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{R}projects/">Projects</a></li><li><a href="{R}about/">About</a></li><li><a href="{R}start/">Start a project</a></li><li><a href="{R}contact/">Contact</a></li><li><a href="{R}requests/">My requests</a></li><li><a href="{R}privacy/">Privacy notice</a></li><li><a href="#" data-install hidden>Install the app</a></li></ul></div>
<div><h4>Group companies</h4><ul>{"".join(f'<li><a href="{u}" rel="noopener">{E(n)}</a><br><span>{E(d)}</span></li>' for n, u, d in GROUP)}</ul></div>
</div>
<div class="legal"><span>© {datetime.date.today().year} Artizanni Business Services Limited · RC 1065469 · Utako, Abuja</span><span>Engineering led by {E(SITE["md"])}, {E(SITE["md_post"])}</span></div>
</div></footer>
<a class="wa-float" data-wa-quick href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener" aria-label="Chat with Artizanni on WhatsApp">{WA}<span>WhatsApp</span></a>
<script>window.ART={art};</script>
<script src="{R}assets/app.js?v={V}" defer></script>
<script src="{R}assets/pwa.js?v={V}" defer></script>
</body>
</html>
'''
    out = DOCS / path / "index.html" if path and not path.endswith(".html") else DOCS / (path or "index.html")
    if path == "": out = DOCS / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    if not noindex and not path.endswith(".html"):
        PAGES.append((path, full_title, desc, prio))
    return R

def phead(R, trail, eyebrow, h1, lede="", photo=None, extra=""):
    if photo:
        return (f'<section class="phead phead-photo">{pic(R, photo, eager=True, sizes="100vw")}<div class="wrap">{crumbs(R, trail)}'
                f'<p class="eyebrow">{E(eyebrow)}</p><h1>{E(h1)}</h1>{f"<p class=lede>{E(lede)}</p>" if lede else ""}{extra}</div></section>')
    return (f'<section class="phead"><div class="wrap">{crumbs(R, trail)}<p class="eyebrow">{E(eyebrow)}</p><h1>{E(h1)}</h1>'
            f'{f"<p class=lede>{E(lede)}</p>" if lede else ""}{extra}</div></section>')

def faq_html(items):
    return "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

SEC = {s["slug"]: s for s in SECTORS}
def clients_strip():
    return ('<div class="clients"><p class="eyebrow">Selected clients &amp; partners</p><ul>' +
            "".join(f'<li><b>{E(n)}</b><span>{E(t)}</span></li>' for n, t in CLIENTS) +
            '</ul><p class="small muted">As listed in our Corporate Profile 2026. Engagements are held under NDA; references on request.</p></div>')
def md_quote(R, cls="s"):
    return (f'<section class="{cls} quote"><div class="wrap"><figure class="pull"><blockquote><p>{E(PROFILE["md_quote"])}</p></blockquote>'
            f'<figcaption><b>{E(SITE["md"])}</b><span>Founder and Managing Director · {E(SITE["md_post"])}</span></figcaption></figure></div></section>')
def journey_html():
    return '<ol class="journey">' + "".join(f'<li><span class="tag">{E(a)}</span><h3>{E(b)}</h3><p>{E(c)}</p></li>' for a, b, c in JOURNEY) + '</ol>' 
SECURE_LINE = lambda R: f'<div class="aside-line">{ICONS["shield"]}<p><b>Secure spaces.</b> We also design and build protected rooms for homes and offices, on a strictly confidential basis.</p><a class="btn btn-line btn-sm" href="{R}services/secure-spaces/">Learn more</a></div>'
def sector_photos(slug):
    return [k for k, v in PH.items() if v["sector"] == slug]

# ================================================================== HOME
def build_home():
    R = "./"
    svc_cards = []
    for i, s in enumerate([x for x in SERVICES if x["slug"] != "secure-spaces"], 1):
        svc_cards.append(f'<a class="svc" href="{R}services/{s["slug"]}/"><span class="no">{i:02d}</span>{ICONS[s["icon"]]}<h3>{E(s["name"])}</h3><p>{E(s["short"])}</p><span class="more">Read more {ARW}</span></a>')
    svc_cards.insert(0, f'<a class="svc feature" href="{R}diaspora/"><span class="no">00</span>{ICONS["globe"]}<h3>Build from abroad</h3><p>{E(DIASPORA["short"])}</p><span class="more">How escrow works {ARW}</span></a>')
    sectors = "".join(f'<a class="sector" href="{R}projects/{s["slug"]}/"><div class="ph">{pic(R, s["hero"], sizes="(max-width:640px) 100vw, (max-width:980px) 50vw, 25vw")}</div><h3>{E(s["name"])}</h3><p>{E(s["standfirst"])}</p></a>' for s in SECTORS[:8])
    steps = "".join(f'<li><b>{n}</b><h3>{E(t)}</h3><p>{E(d)}</p></li>' for n, t, d in STAGES)
    hero = f'''<section class="hero">{pic(R, "reclaim-aerial", eager=True, sizes="100vw", alt="Aerial view of land reclamation works by Artizanni in Lagos")}
<p class="hero-cap">{E(PH["reclaim-aerial"]["caption"])}</p>
<div class="wrap"><p class="eyebrow">Design-build firm · Abuja · Since 2012</p>
<h1>Artizanni: designed, engineered and built by one accountable team.</h1>
<p class="lede">Architecture, civil, structural and MEP engineering, construction, interiors and real estate, led by a COREN-registered engineer. For Nigerians abroad, your money stays in escrow until each stage is verified.</p>
<div class="btns"><a class="btn btn-gold" href="{R}start/">Start a project {ARW}</a><a class="btn btn-line" href="{R}diaspora/">Build from abroad</a></div>
<dl class="titleblock"><div><dt>Registered</dt><dd>RC 1065469</dd></div><div><dt>Established</dt><dd>2012, Abuja</dd></div><div><dt>Engineer of record</dt><dd>COREN R29685</dd></div><div><dt>Escrow partner</dt><dd>First Trustees</dd></div></dl>
</div></section>'''
    body = f'''
<section class="s" style="padding-bottom:0"><div class="wrap">
<div class="stats"><div><b>2012</b><span>Incorporated in Abuja (RC 1065469)</span></div><div><b>26<em>+</em></b><span>Engagements in our recorded contracting register</span></div><div><b>11</b><span>Sectors of delivered work, from marine civils to retail fit-out</span></div><div><b>₦0</b><span>Taken up front. Every payment follows certified progress</span></div></div>
</div></section>

<section class="s"><div class="wrap">
<div class="shead"><div><p class="eyebrow">01 / What we do</p><h2>One firm from land to keys.</h2><p class="lede">Most property failures in Nigeria are coordination failures, not engineering failures: land bought on a bad title, drawings that ignore the engineer, a contractor building to a different standard, an owner with no one watching. We remove those seams. Appoint us for the whole project or for the part you need.</p></div><a class="btn btn-line" href="{R}services/">All services {ARW}</a></div>
<div class="grid g3">{"".join(svc_cards)}</div>
{SECURE_LINE(R)}
</div></section>

<section class="s alt"><div class="wrap">
<div class="shead"><div><p class="eyebrow">02 / Work on record</p><h2>Built in the wet, on transmission sites and in city streets.</h2><p class="lede">Cofferdams and dam rehabilitation, substation civils, channels and reclamation, homes, frames, stores and fit-outs. Photographs are from our own site records.</p></div><a class="btn btn-line" href="{R}projects/">See projects {ARW}</a></div>
<div class="mosaic">
<a class="ph a" href="{R}projects/water/">{pic(R, "cofferdam-2", sizes="(max-width:760px) 100vw, 66vw")}</a>
<a class="ph b" href="{R}projects/residential/">{pic(R, "duplex-3", sizes="(max-width:760px) 50vw, 33vw")}</a>
<a class="ph b" href="{R}projects/interiors/">{pic(R, "int-3", sizes="(max-width:760px) 50vw, 33vw")}</a>
<a class="ph c" href="{R}projects/structures/">{pic(R, "slab-2", sizes="(max-width:760px) 50vw, 33vw")}</a>
<a class="ph c" href="{R}projects/industrial/">{pic(R, "panel-1", sizes="(max-width:760px) 50vw, 33vw")}</a>
<a class="ph c" href="{R}projects/drainage/">{pic(R, "gabion-wall", sizes="(max-width:760px) 50vw, 33vw")}</a>
</div>
<div class="grid g4" style="margin-top:48px">{sectors}</div>
{clients_strip()}
</div></section>

<section class="s dark"><div class="wrap">
<div class="shead"><div><p class="eyebrow">03 / How a project runs</p><h2>Six stages. Evidence at every one.</h2><p class="lede">Each stage ends with something you can check: a report, a drawing set, a priced bill, an inspection record or a handover file.</p></div></div>
<ol class="steps">{steps}</ol>
</div></section>

<section class="s"><div class="wrap split">
<div><p class="eyebrow">04 / Build from abroad</p><h2>Your money moves only when the work is proven.</h2>
<p class="lede">Too many Nigerians abroad have sent money home for a house that was never built. Our diaspora service removes the need for trust.</p>
<ul class="ticks"><li>Funds are held by <b>First Trustees</b> in escrow, not paid to us up front.</li><li>Release happens per milestone (M0 to M8), against a verification pack with geotagged photos, video, test results and a QS valuation.</li><li>Title is checked by a lawyer and surveyor before any money goes into land.</li><li>Weekly reports and calls in your time zone.</li></ul>
<div class="btns"><a class="btn btn-ink" href="{R}diaspora/">How it works {ARW}</a><a class="btn btn-line" href="{R}start/?service=diaspora">Book a discovery call</a></div></div>
<div>{fig(R, "duplex-1", "ratio-43", sizes="(max-width:900px) 100vw, 50vw")}</div>
</div></section>

{md_quote(R)}
<section class="s alt"><div class="wrap">
<div class="shead"><div><p class="eyebrow">05 / Why clients appoint us</p><h2>Engineers who build, builders who document.</h2></div></div>
<div class="grid g4">
<div><h3>Engineer-led</h3><p class="muted">The practice is led by {E(SITE["md"])}, a COREN-registered civil and structural engineer (MNSE, PMP). Designs are sealed by registered professionals.</p></div>
<div><h3>Priced by people who build</h3><p class="muted">The team that designs your project also prepares the bill of quantities and the programme, so drawings, cost and site agree.</p></div>
<div><h3>Proof, not promises</h3><p class="muted">Inspections before every pour, cube tests, dated photo reports and certified valuations, kept in a handover file you own.</p></div>
<div><h3>Registered and compliant</h3><p class="muted">CAC-registered since 2012, SCUML-registered for real-estate due diligence, with a current tax clearance certificate.</p></div>
</div></div></section>
{cta(R)}'''
    page("", "Artizanni | Design-build, engineering and construction in Nigeria", SITE["description"], body, ld=[], hero_pre=hero, prio="1.0")

# ================================================================== SERVICES
def build_services():
    R = root_for("services/")
    cards = "".join(f'<a class="svc" href="{R}services/{s["slug"]}/"><span class="no">{i:02d}</span>{ICONS[s["icon"]]}<h3>{E(s["name"])}</h3><p>{E(s["short"])}</p><span class="more">Read more {ARW}</span></a>' for i, s in enumerate([x for x in SERVICES if x["slug"] != "secure-spaces"], 1))
    cards = f'<a class="svc feature" href="{R}diaspora/"><span class="no">00</span>{ICONS["globe"]}<h3>Build from abroad</h3><p>{E(DIASPORA["short"])}</p><span class="more">How escrow works {ARW}</span></a>' + cards
    trail = [("Services", "services/")]
    body = phead(R, trail, "Services", "Everything a building needs, from one accountable firm.",
                 "Appoint us end to end under design and build, or for one discipline. Every service is run by registered professionals and documented to the same standard.") + f'''
<section class="s"><div class="wrap"><div class="grid g3">{cards}</div>{SECURE_LINE(R)}</div></section>
<section class="s alt"><div class="wrap split"><div><p class="eyebrow">Ways to work with us</p><h2>Pick the engagement that fits.</h2><p class="lede">Every engagement starts with a consultation to set your objective, budget and timeline. Then we propose the model that fits.</p>
<p class="eyebrow" style="margin-top:28px">Who we serve</p><p>{E(PROFILE["serves"])}</p></div>
<div class="eng">{"".join(f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in ENGAGEMENTS)}</div></div></section>
<section class="s"><div class="wrap split"><div><p class="eyebrow">Common questions</p><h2>Before you appoint us</h2></div><div>{faq_html(GENERAL_FAQ)}</div></div></section>
{cta(R)}'''
    page("services/", "Services", "Design and build, architecture, civil, structural and MEP engineering, construction, interiors, real estate, project management, personnel and secure spaces in Nigeria.", body, active="services/", ld=[crumbs_ld(trail), faq_ld(GENERAL_FAQ)], prio="0.9")

    for s in SERVICES:
        path = f'services/{s["slug"]}/'; R = root_for(path)
        trail = [("Services", "services/"), (s["name"], path)]
        photo = s["photos"][0] if s["photos"] else None
        head = phead(R, trail, "Service", s["name"], s["short"], photo=photo)
        strip = "".join(f'<div>{fig(R, k, "ratio-43", lb=True, sizes="(max-width:640px) 100vw, 33vw")}</div>' for k in s["photos"][1:4])
        rel = [sec for sec in SECTORS if any(PH.get(k, {}).get("sector") == sec["slug"] for k in s["photos"])][:4]
        form_extra = ""
        if s["slug"] == "personnel":
            form_extra = personnel_form(R)
        if s["slug"] == "secure-spaces":
            side = f'''<div class="note terra"><b>Confidential by design.</b> {E(s["notes"])}</div>
<div class="btns" style="margin-top:18px"><a class="btn btn-ink" href="tel:{SITE["phone_href"]}">{ICONS["phone"]}Call to arrange a consultation</a></div>'''
        else:
            side = f'<div class="note">{E(s["notes"])}</div>'
        body = head + f'''
<section class="s"><div class="wrap split">
<div class="prose"><p class="lede" style="color:var(--fg)">{E(s["intro"])}</p>{side}</div>
<div><p class="eyebrow">What this covers</p><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in s["items"])}</ul>
<div class="btns"><a class="btn btn-gold" href="{R}start/?service={s["slug"]}">Start a {E(s["name"].split(" &")[0].split(",")[0].lower()) if s["slug"] not in ("interiors","personnel","secure-spaces") else "request"} {ARW}</a><a class="btn btn-line" data-wa-quick="{E(s["name"])}" href="https://wa.me/{SITE["whatsapp"]}">{WA}Ask on WhatsApp</a></div></div>
</div></section>
{f'<section class="s alt" style="padding-top:56px;padding-bottom:56px"><div class="wrap"><div class="grid g3">{strip}</div></div></section>' if strip else ''}
{form_extra}
{('<section class="s"><div class="wrap"><p class="eyebrow">Related work</p><div class="grid g4">' + "".join(f'<a class="sector" href="{R}projects/{x["slug"]}/"><div class="ph">{pic(R, x["hero"], sizes="25vw")}</div><h3>{E(x["name"])}</h3><p>{E(x["standfirst"])}</p></a>' for x in rel) + '</div></div></section>') if rel else ''}
{cta(R, sub="?service=" + s["slug"]) if s["slug"] != "secure-spaces" else ""}'''
        ld = [crumbs_ld(trail), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["short"] + " " + s["intro"],
               "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Nigeria"}, "url": BASE + path}]
        page(path, s["name"], f'{s["short"]} Artizanni, Abuja: {s["intro"][:110]}', body, active="services/", ld=ld, og=photo, prio="0.8")

def personnel_form(R):
    disc = ["Site engineer (civil/structural)", "MEP engineer", "Quantity surveyor", "Site supervisor / foreman", "Mason / bricklayer", "Steel fixer",
            "Carpenter / formwork", "Tiler", "Plumber", "Electrician", "Painter / decorator", "HSE officer", "Storekeeper", "Other"]
    opts = "".join(f'<label class="opt"><input type="radio" name="disc" value="{E(d)}"><span>{E(d)}</span></label>' for d in disc)
    states = "".join(f'<option>{E(s)}</option>' for s in STATES)
    return f'''<section class="s" id="register"><div class="wrap split">
<div><p class="eyebrow">For professionals and artisans</p><h2>Register your interest for placements</h2><p class="lede">Tell us your trade and where you can work. When a suitable placement comes up we will contact you. Do not send ID documents or bank details here.</p></div>
<div><form class="form" data-wa="R" data-title="Personnel register" data-intro="I would like to be considered for placements.">
<fieldset data-label="Discipline" data-need><legend>Your discipline</legend><div class="opts">{opts}</div></fieldset>
<div class="row2 fieldrow"><div><label class="f" for="pn">Full name</label><input class="in" id="pn" name="name" data-label="Name" required autocomplete="name"></div>
<div><label class="f" for="py">Years of experience</label><input class="in" id="py" name="years" data-label="Years of experience" inputmode="numeric"></div></div>
<div class="row2 fieldrow"><div><label class="f" for="ps">State you can work in</label><select class="in" id="ps" name="state" data-label="State"><option value="">Choose…</option>{states}</select></div>
<div><label class="f" for="pc">Phone</label><input class="in" id="pc" name="phone" data-label="Phone" type="tel" autocomplete="tel"></div></div>
<div class="fieldrow"><label class="f" for="pq">Qualifications and registrations (e.g. COREN, NIQS, trade certificate)</label><input class="in" id="pq" name="quals" data-label="Qualifications"></div>
<label class="consent"><input type="checkbox" required data-skip> I agree that Artizanni may keep these details to consider me for placements, as described in the <a href="{R}privacy/">privacy notice</a>.</label>
<div class="btns" style="margin-top:18px"><button class="btn btn-gold" type="submit">Prepare my message {ARW}</button></div>
</form><div class="form" data-out hidden style="margin-top:16px"></div></div>
</div></section>'''

# ================================================================== PROJECTS
def register_table(rows, filters=True):
    chips = ""
    if filters:
        used = [s for s in SECTORS if any(r[4] == s["slug"] for r in rows)]
        chips = '<div class="reg-tools" role="group" aria-label="Filter by sector"><button class="chip" type="button" data-filter="all" aria-pressed="true">All ' + str(len(rows)) + '</button>' + \
                "".join(f'<button class="chip" type="button" data-filter="{s["slug"]}" aria-pressed="false">{E(s["name"].split(",")[0].split(" &")[0])} {len([r for r in rows if r[4]==s["slug"]])}</button>' for s in used) + '</div>'
    st = lambda n: REGISTER_STATUS.get(n, "Completed")
    trs = "".join(f'<tr data-sector="{r[4]}"><td>{r[0]:02d}</td><td class="cl">{E(r[1])}</td><td>{E(r[2])}</td><td class="ro">{E(r[3])}</td><td><span class="st {st(r[0]).lower()}">{st(r[0])}</span></td></tr>' for r in rows)
    return chips + f'<div style="overflow-x:auto"><table class="reg" data-register><thead><tr><th>No.</th><th>Client</th><th>Engagement</th><th>Role</th><th>Status</th></tr></thead><tbody>{trs}</tbody></table></div>'

def build_projects():
    path = "projects/"; R = root_for(path); trail = [("Projects", path)]
    cards = "".join(f'<a class="sector" href="{R}projects/{s["slug"]}/"><div class="ph">{pic(R, s["hero"], sizes="(max-width:640px) 100vw, (max-width:980px) 50vw, 33vw")}</div><h3>{E(s["name"])}<small>{len(sector_photos(s["slug"]))} photos</small></h3><p>{E(s["standfirst"])}</p></a>' for s in SECTORS)
    nums = "".join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in NUMBERS)
    body = phead(R, trail, "Projects", "Built, not rendered.",
                 "Eleven sectors of delivered work, from cofferdams in live rivers to fitted-out retail floors. The photographs are from our own sites, most taken by the people running them. Reinforcement is shown before it is covered, and mud where there was mud.") + f'''
<section class="s" style="padding-bottom:0"><div class="wrap"><div class="stats">{nums}</div></div></section>
<section class="s"><div class="wrap"><div class="grid g3">{cards}</div>{clients_strip()}</div></section>
<section class="s alt" id="register"><div class="wrap">
<div class="shead"><div><p class="eyebrow">Contracting register</p><h2>Recorded engagements</h2><p class="lede">The 26 engagements in our Corporate Profile 2026, delivered as design consultant, design-and-build contractor or specialist sub-contractor. Status is as printed in the profile.</p></div></div>
{register_table(REGISTER)}
<p class="small muted" style="margin-top:14px">Recent residential, commercial and interiors projects shown in the photographs are not all listed in this register. Contract values are shared with prospective clients on request.</p>
</div></section>
{cta(R)}'''
    ld = [crumbs_ld(trail), {"@type": "ItemList", "name": "Artizanni project sectors", "itemListElement": [{"@type": "ListItem", "position": i, "url": BASE + f'projects/{s["slug"]}/', "name": s["name"]} for i, s in enumerate(SECTORS, 1)]}]
    page(path, "Projects", "Artizanni projects: water and dam works, substation civils, drainage and reclamation, homes, RC frames, building services, retail, cold rooms, interiors, roads and design consultancy in Nigeria.", body, active=path, ld=ld, prio="0.9")

    for s in SECTORS:
        path = f'projects/{s["slug"]}/'; R = root_for(path); trail = [("Projects", "projects/"), (s["name"], path)]
        rows = [r for r in REGISTER if r[4] == s["slug"]]
        photos = sector_photos(s["slug"])
        facts = "".join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in s["facts"])
        others = [x for x in SECTORS if x["slug"] != s["slug"]][:4] if False else [x for x in SECTORS if x["slug"] != s["slug"]]
        idx = SECTORS.index(s); nxt = SECTORS[(idx + 1) % len(SECTORS)]; prv = SECTORS[idx - 1]
        body = phead(R, trail, f"Sector {idx + 1:02d}", s["name"], s["standfirst"], photo=s["hero"]) + f'''
<section class="s"><div class="wrap split">
<div class="prose">{"".join(f"<p>{E(p)}</p>" for p in s["body"])}</div>
<dl class="facts">{facts}</dl>
</div></section>
{f'<section class="s alt" style="padding-top:56px"><div class="wrap"><p class="eyebrow">Photographs ({len(photos)})</p>{gallery(R, photos)}</div></section>' if photos else ''}
{f'<section class="s"><div class="wrap"><p class="eyebrow">From the register</p>{register_table(rows, filters=False)}</div></section>' if rows else ''}
<section class="s" style="padding-top:0"><div class="wrap"><div class="btns" style="justify-content:space-between"><a class="btn btn-line" href="{R}projects/{prv["slug"]}/">← {E(prv["name"])}</a><a class="btn btn-line" href="{R}projects/{nxt["slug"]}/">{E(nxt["name"])} →</a></div></div></section>
{cta(R)}'''
        ld = [crumbs_ld(trail), {"@type": "CollectionPage", "name": s["name"], "description": s["standfirst"], "url": BASE + path,
              "about": {"@id": ORG_ID}, "image": [BASE + f"img/{k}-1600.jpg" for k in photos[:6]]}]
        page(path, f'{s["name"]} projects', f'{s["standfirst"]} Artizanni work on record in Nigeria.', body, active="projects/", ld=ld, og=s["hero"])

# ================================================================== DIASPORA
FLOW_SVG = '''<svg class="flow" viewBox="0 0 980 300" role="img" aria-labelledby="flowT flowD">
<title id="flowT">How your money moves</title><desc id="flowD">You pay into an escrow account held by First Trustees. Artizanni builds and submits a milestone verification pack. Only when the milestone is verified does First Trustees release that stage's funds to Artizanni.</desc>
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#C9973A"/></marker></defs>
<g font-size="15" fill="currentColor">
<rect x="10" y="90" width="220" height="110" rx="4" fill="none" stroke="currentColor" stroke-opacity=".35"/>
<text x="120" y="135" text-anchor="middle" font-weight="700" font-size="18">You</text><text x="120" y="160" text-anchor="middle" opacity=".7">anywhere in the world</text>
<rect x="380" y="70" width="220" height="150" rx="4" fill="#C9973A" fill-opacity=".14" stroke="#C9973A" stroke-width="2"/>
<text x="490" y="128" text-anchor="middle" font-weight="700" font-size="18">First Trustees</text><text x="490" y="153" text-anchor="middle" opacity=".75">escrow account</text><text x="490" y="176" text-anchor="middle" opacity=".75">holds funds until release</text>
<rect x="750" y="90" width="220" height="110" rx="4" fill="none" stroke="currentColor" stroke-opacity=".35"/>
<text x="860" y="135" text-anchor="middle" font-weight="700" font-size="18">Artizanni</text><text x="860" y="160" text-anchor="middle" opacity=".7">builds your project</text>
<path d="M232 145H372" stroke="#C9973A" stroke-width="2.5" marker-end="url(#ah)"/><text x="302" y="134" text-anchor="middle" font-size="13" opacity=".8">1. You fund</text>
<path d="M860 88V40H500v22" fill="none" stroke="currentColor" stroke-opacity=".55" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ah)"/><text x="680" y="32" text-anchor="middle" font-size="13" opacity=".8">2. Milestone verification pack (photos, video, tests, QS valuation)</text>
<path d="M602 175H742" stroke="#C9973A" stroke-width="2.5" marker-end="url(#ah)"/><text x="672" y="200" text-anchor="middle" font-size="13" opacity=".8">3. Stage released</text>
<path d="M860 202v48H120v-44" fill="none" stroke="currentColor" stroke-opacity=".35" stroke-width="1.5" marker-end="url(#ah)"/><text x="490" y="272" text-anchor="middle" font-size="13" opacity=".8">Weekly report and video to you, every week, in your time zone</text>
</g></svg>'''

def build_diaspora():
    path = "diaspora/"; R = root_for(path); trail = [("Build from abroad", path)]
    ms = "".join(f'<li><b>{m}</b><h3>{E(t)}</h3><p>Evidence: {E(e)}</p></li>' for m, t, e in MILESTONES)
    steps = [("01", "Discovery call", "In your time zone: your plans, budget, location and timing."),
             ("02", "Due diligence", "Identity and source-of-funds checks (we are SCUML-registered), then an engagement letter."),
             ("03", "Title check", "Lawyer and surveyor verify the land. You get a go / no-go report before any land money moves."),
             ("04", "Design & price", "Drawings, bill of quantities and programme, then milestone values agreed."),
             ("05", "Escrow deed", "Agreed with you and First Trustees. You fund the escrow, not Artizanni."),
             ("06", "Build & release", "Weekly reports; a verification pack and release at each milestone, through to handover.")]
    body = phead(R, trail, "For Nigerians abroad", "Build at home without sending money on trust.",
                 "If you cannot be on site, we are your presence on site. Your construction funds are held in escrow by First Trustees and released to us one verified milestone at a time.", photo="duplex-5",
                 extra=f'<div class="btns" style="margin-top:24px"><a class="btn btn-gold" href="{R}start/?service=diaspora">Book a discovery call {ARW}</a><a class="btn btn-line" style="color:#fff" href="#how">See how it works</a></div>') + f'''
<section class="s"><div class="wrap split">
<div><p class="eyebrow">The problem</p><h2>Distance makes building expensive in ways a budget does not show.</h2></div>
<div class="prose"><p>Building from abroad usually means sending money to a relative, an agent or a contractor and hoping the photographs are real. Unverified title, inflated progress and funds diverted to other jobs are common stories.</p>
<p>Our service is built so that you do not have to rely on any one person's honesty, including ours. The money sits with an independent trustee, the land is checked by a lawyer, and every release is backed by evidence you can review before it is paid.</p></div>
</div></section>
<section class="s alt" id="how"><div class="wrap"><div class="shead"><div><p class="eyebrow">How your money moves</p><h2>Escrow first, evidence always.</h2><p class="lede">{E(PROFILE["payments"])}</p></div></div>{FLOW_SVG}
<div style="margin-top:48px"><p class="eyebrow">The three-stage journey</p>{journey_html()}</div></div></section>
<section class="s"><div class="wrap"><div class="shead"><div><p class="eyebrow">Milestones</p><h2>Nine release points, each with its own evidence.</h2><p class="lede">Our default schedule. The exact milestones and values are set in your contract and escrow deed.</p></div></div><ol class="ms">{ms}</ol></div></section>
<section class="s dark"><div class="wrap"><div class="shead"><div><p class="eyebrow">Getting started</p><h2>From first call to first release</h2></div></div><ol class="steps">{"".join(f"<li><b>{n}</b><h3>{E(t)}</h3><p>{E(d)}</p></li>" for n, t, d in steps)}</ol></div></section>
<section class="s"><div class="wrap split"><div><p class="eyebrow">What you receive</p><h2>Reporting you can check from anywhere</h2>
<ul class="ticks"><li>Weekly written report with dated photographs and a short video walk-through</li><li>A Milestone Verification Pack before every release: geotagged photos, video, inspection and test records, QS valuation</li><li>Scheduled calls in your time zone</li><li>Handover file: as-built drawings, test certificates, manuals and keys</li><li>Optional property management after handover</li></ul></div>
<div>{fig(R, "duplex-4", "ratio-43", sizes="(max-width:900px) 100vw, 50vw")}</div></div></section>
<section class="s alt"><div class="wrap split"><div><p class="eyebrow">Questions</p><h2>What people ask before they start</h2><p class="muted small">This page explains how our service works. It is not legal or financial advice; your escrow deed and contract govern the details, and we recommend you take independent legal advice.</p></div><div>{faq_html(DIASPORA_FAQ)}</div></div></section>
{cta(R, "Book a discovery call.", "Tell us where you live, where you want to build and roughly when. We will arrange a call in your time zone.", "?service=diaspora", "Book a discovery call")}'''
    ld = [crumbs_ld(trail), faq_ld(DIASPORA_FAQ), {"@type": "Service", "name": "Build from abroad: escrow-backed construction for Nigerians in the diaspora",
          "serviceType": "Construction project management with escrow", "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Nigeria"},
          "audience": {"@type": "Audience", "audienceType": "Nigerians living abroad"}, "description": DIASPORA["short"], "url": BASE + path}]
    page(path, "Build in Nigeria from abroad with escrow", "For Nigerians in the UK, US, Canada and elsewhere: build or buy in Nigeria with funds held in escrow by First Trustees and released only against verified milestones.", body, active=path, ld=ld, og="duplex-5", prio="0.9")

# ================================================================== ABOUT
def build_about():
    path = "about/"; R = root_for(path); trail = [("About", path)]
    plant = "".join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in PLANT)
    body = phead(R, trail, "About Artizanni", "A contractor that designs.",
                 "Artizanni Business Services Limited was incorporated in Abuja on 17 September 2012. We design, engineer and build, and we stay accountable for all three.") + f'''
<section class="s"><div class="wrap split">
<div class="prose">{"".join(f"<p>{E(x)}</p>" for x in PROFILE["story"])}
<p>Today the practice works across three connected markets: infrastructure and building construction across Nigeria; property development and project management for Nigerians abroad, structured so clients carry no upfront capital risk; and premium interiors through Artizanni Interiors. One discipline binds them: engineering rigour at every stage, and what is agreed on paper is what is delivered on site.</p></div>
<div>{fig(R, "frame-4", "ratio-43", sizes="(max-width:900px) 100vw, 50vw")}</div>
</div></section>
<section class="s alt"><div class="wrap"><div class="grid g3 mvh">
<div><p class="eyebrow">Our mission</p><p class="big">{E(PROFILE["mission"])}</p></div>
<div><p class="eyebrow">Our vision</p><p class="big">{E(PROFILE["vision"])}</p></div>
<div><p class="eyebrow">How we work</p><p class="big">{E(PROFILE["how"])}</p></div>
</div></div></section>
{md_quote(R)}
<section class="s"><div class="wrap split">
<div><p class="eyebrow">Leadership</p><h2>{E(SITE["md"])}</h2><p class="muted" style="font-family:var(--mono);font-size:.85rem">Founder and Managing Director · {E(SITE["md_post"])}</p>
<p>A COREN-registered civil and structural engineer, member of the Nigerian Society of Engineers and certified Project Management Professional, with more than fifteen years in Nigerian construction, heavy-equipment operations and engineering practice. He has led Artizanni from a specialist construction practice into an integrated design-build, infrastructure and property group.</p>
<p class="muted">{E(SITE["md_quals"])}</p></div>
<div><p class="eyebrow">People</p><h2>One delivery team</h2>
<ul class="ticks"><li>{E(PROFILE["team"])}</li><li>Collective memberships: {E(PROFILE["memberships"])}.</li><li>{E(PROFILE["workforce"])}</li><li>{E(PROFILE["model"])}</li></ul></div>
</div></section>
<section class="s alt"><div class="wrap split">
<div><p class="eyebrow">Plant &amp; capability</p><h2>Owned plant shortens the programme.</h2><p class="lede">Hired plant arrives when the hire company can spare it. We hold our own earthmoving and compaction plant, bought through established dealer channels, and hire specialist equipment only where a scheme needs it.</p>
<dl class="facts">{plant}</dl></div>
<div>{fig(R, "loader-gabion", "ratio-43", sizes="(max-width:900px) 100vw, 50vw")}
<p class="eyebrow" style="margin-top:28px">Coverage</p><p>{E(PROFILE["coverage"])}</p>
<p class="eyebrow" style="margin-top:20px">Who we build for</p><p>{E(PROFILE["serves"])}</p></div>
</div></section>
<section class="s"><div class="wrap split">
<div><p class="eyebrow">Governance &amp; compliance</p><h2>Registered, compliant and documented for prequalification.</h2>
<p class="muted">{E(PROFILE["nda"])}</p>
<div class="dl"><a class="btn btn-ink" href="{R}downloads/Artizanni-Corporate-Profile-2026.pdf" download>Download the Corporate Profile 2026 <span class="small">(PDF, 7.6 MB)</span></a></div></div>
<dl class="facts">
<div><dt>Company</dt><dd>Artizanni Business Services Limited, a private company limited by shares under CAMA</dd></div>
<div><dt>Registration</dt><dd>CAC RC 1065469, incorporated 17 Sep 2012</dd></div>
<div><dt>Head office</dt><dd>{E(SITE["address"])}</dd></div>
<div><dt>Engineer of record</dt><dd>COREN Reg. No. R29685</dd></div>
<div><dt>AML / CFT</dt><dd>Registered with SCUML (real estate is a designated business)</dd></div>
<div><dt>Tax</dt><dd>Compliant taxpayer with a current tax clearance certificate</dd></div>
<div><dt>Escrow partner</dt><dd>First Trustees</dd></div>
<div><dt>Banking &amp; accounts</dt><dd>Guaranty Trust Bank · iMetrics Ltd (accountants)</dd></div>
<div><dt>Plant supply</dt><dd>SMT Nigeria Ltd</dd></div>
</dl>
</div></section>
<section class="s alt"><div class="wrap"><div class="shead"><div><p class="eyebrow">How we work</p><h2>Principles we hold ourselves to</h2></div></div>
<div class="grid g3">
<div><h3>Sealed by registered professionals</h3><p class="muted">Engineering designs are sealed by COREN-registered engineers and architectural permit drawings by ARCON-registered architects. Nothing is issued for construction without it.</p></div>
<div><h3>No upfront payments</h3><p class="muted">{E(PROFILE["payments"])}</p></div>
<div><h3>Safety stops work</h3><p class="muted">Anyone on our sites can stop an unsafe activity: unshored trenches, failing props, unprotected work at height or live electrics.</p></div>
<div><h3>Clients' money is protected</h3><p class="muted">For diaspora clients, funds sit in escrow with First Trustees and are released only against evidence.</p></div>
<div><h3>Related parties disclosed</h3><p class="muted">Where a group company (plant, materials) supplies your project, we tell you and compare at least one independent quote.</p></div>
<div><h3>Confidential by default</h3><p class="muted">Every brief is under NDA. We follow the Nigeria Data Protection Act 2023 and never publish diaspora or secure-space clients.</p></div>
</div></div></section>
<section class="s"><div class="wrap"><div class="shead"><div><p class="eyebrow">Group companies</p><h2>Plant, materials and price data from the same founder</h2><p class="lede">Used on Artizanni projects only on arm's-length terms, with an independent comparison quote.</p></div></div>
<div class="grid g3">{"".join(f'<a class="svc" href="{u}" rel="noopener"><h3>{E(n)}</h3><p>{E(d)}</p><span class="more">{E(u.split("//")[1].strip("/"))} {ARW}</span></a>' for n, u, d in GROUP)}</div></div></section>
{cta(R)}'''
    ld = [crumbs_ld(trail), {"@type": "AboutPage", "url": BASE + path, "about": {"@id": ORG_ID}},
          {"@type": "DigitalDocument", "name": "Artizanni Corporate Profile 2026", "encodingFormat": "application/pdf", "url": BASE + "downloads/Artizanni-Corporate-Profile-2026.pdf", "author": {"@id": ORG_ID}}]
    page(path, "About", "Artizanni Business Services Limited (RC 1065469), an Abuja design-build and engineering firm founded in 2012 and led by Engr. Akolade Maruf Ibrahim, COREN R29685. Mission, people, plant and compliance.", body, active=path, ld=ld, prio="0.8")

# ================================================================== START (wizard)
def build_start():
    path = "start/"; R = root_for(path); trail = [("Start a project", path)]
    svc = [("design-build", "Design & build (everything)"), ("architecture", "Architecture / drawings"), ("engineering", "Engineering design or assessment"),
           ("construction", "Construction / civil works"), ("interiors", "Interiors & fit-out"), ("real-estate", "Land or property purchase"),
           ("project-management", "Project or property management"), ("personnel", "Personnel for my project"), ("diaspora", "Build from abroad (escrow)"),
           ("secure-spaces", "Secure space (confidential)"), ("unsure", "Not sure yet")]
    types = ["Home / duplex", "Estate or several units", "Commercial / retail", "Office", "Industrial / warehouse / cold room", "School, hospital or worship centre",
             "Roads, drainage, power or water works", "Renovation or extension", "Interior only", "Land only", "Other"]
    stage = ["Just an idea", "I have land, no drawings", "I have approved drawings", "Construction has started", "Building complete: fit-out or management"]
    when = ["As soon as possible", "Within 3 months", "In 3 to 6 months", "In 6 to 12 months", "Later / flexible"]
    budget = ["Prefer to discuss", "Under ₦50 million", "₦50 to 150 million", "₦150 to 500 million", "Over ₦500 million"]
    radios = lambda name, opts: "".join(f'<label class="opt"><input type="radio" name="{name}" value="{E(v if isinstance(v, str) else v[1])}"{f" data-slug=\"{v[0]}\"" if not isinstance(v, str) else ""}><span>{E(v if isinstance(v, str) else v[1])}</span></label>' for v in opts)
    states = "".join(f'<option>{E(s)}</option>' for s in STATES)
    body = phead(R, trail, "Start a project", "Tell us what you want to build.",
                 "Two minutes. Your answers become a message with a reference number that you send to us on WhatsApp or by email. Nothing is sent until you press send.") + f'''
<section class="s"><div class="wrap split">
<div><form class="form" data-wa="P" data-title="Project enquiry" data-intro="I would like to discuss a project." id="wizard">
<fieldset data-label="Service" data-need><legend>1. What do you need?</legend><div class="opts">{radios("service", svc)}</div></fieldset>
<fieldset data-label="Project type"><legend>2. What kind of project?</legend><div class="opts">{radios("type", types)}</div></fieldset>
<fieldset data-label="Stage"><legend>3. Where are you now?</legend><div class="opts">{radios("stage", stage)}</div></fieldset>
<fieldset><legend>4. Where is the site?</legend><div class="row2"><div><label class="f" for="st">State</label><select class="in" id="st" name="state" data-label="State"><option value="">Choose…</option>{states}</select></div>
<div><label class="f" for="area">Town or area</label><input class="in" id="area" name="area" data-label="Town / area" placeholder="e.g. Lekki, Gwarinpa, Festac"></div></div></fieldset>
<fieldset data-label="Timing"><legend>5. When do you want to start?</legend><div class="opts">{radios("when", when)}</div></fieldset>
<fieldset data-label="Budget indication"><legend>6. Budget indication <small>Optional. Helps us suggest the right approach; it is not a quotation.</small></legend><div class="opts">{radios("budget", budget)}</div></fieldset>
<fieldset><legend>7. About you</legend>
<div class="row2 fieldrow"><div><label class="f" for="nm">Your name</label><input class="in" id="nm" name="name" data-label="Name" required autocomplete="name"></div>
<div><label class="f" for="loc">Where you live</label><input class="in" id="loc" name="based" data-label="Based in" placeholder="e.g. Abuja, or London, UK" autocomplete="country-name"></div></div>
<div class="row2 fieldrow"><div><label class="f" for="ph">Phone (optional)</label><input class="in" id="ph" name="phone" data-label="Phone" type="tel" autocomplete="tel"></div>
<div><label class="f" for="em">Email (optional)</label><input class="in" id="em" name="email" data-label="Email" type="email" autocomplete="email"></div></div>
<div class="fieldrow"><label class="f" for="bt">Best time to call (and your time zone if abroad)</label><input class="in" id="bt" name="time" data-label="Best time to call"></div>
<div class="fieldrow"><label class="f" for="dt">Anything else? Plot size, number of rooms, what matters most</label><textarea class="in" id="dt" name="details" data-label="Details"></textarea></div></fieldset>
<p class="small muted" data-secure hidden style="border-left:3px solid var(--terra);padding-left:12px">For secure spaces, please leave out addresses and plans. Just ask for a call.</p>
<label class="consent"><input type="checkbox" required data-skip> I agree that Artizanni may use these details to respond to my enquiry, as described in the <a href="{R}privacy/">privacy notice</a>.</label>
<div class="btns" style="margin-top:20px"><button class="btn btn-gold" type="submit">Prepare my message {ARW}</button></div>
</form>
<div class="form" data-out hidden style="margin-top:16px" aria-live="polite"></div></div>
<aside><div style="position:sticky;top:96px"><p class="eyebrow">What happens next</p><ol class="ticks" style="list-style:none"><li>You send the message from your own WhatsApp or email.</li><li>We reply, usually with a few questions and a time for a call or site visit.</li><li>For larger projects we propose a brief and feasibility stage with a fixed fee before design.</li></ol>
<div class="note small">Prefer to talk? Call <a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a> or email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> or <a href="mailto:{SITE["alt_email"]}">{SITE["alt_email"]}</a>.</div>
<p class="small muted" style="margin-top:14px">Your requests are listed on <a href="{R}requests/">My requests</a> on this device.</p></div></aside>
</div></section>
<script>
(function(){{var q=new URLSearchParams(location.search).get("service");if(q){{var i=document.querySelector('#wizard input[data-slug="'+q.replace(/[^a-z-]/g,"")+'"]');if(i)i.checked=true;}}
var sec=document.querySelector("[data-secure]");document.querySelectorAll('#wizard input[name=service]').forEach(function(r){{r.addEventListener("change",function(){{sec.hidden=!(r.checked&&r.dataset.slug==="secure-spaces");}});}});}})();
</script>'''
    page(path, "Start a project", "Tell Artizanni about your building, interiors, land or diaspora project and send it on WhatsApp or email with a reference number.", body, active=None, ld=[crumbs_ld(trail)], prio="0.9")

# ================================================================== CONTACT, REQUESTS, PRIVACY, 404, OFFLINE
def build_contact():
    path = "contact/"; R = root_for(path); trail = [("Contact", path)]
    maps = "https://www.google.com/maps/search/?api=1&query=" + "Anthony+Enahoro+Street+Utako+Abuja"
    body = phead(R, trail, "Contact", "Talk to an engineer.", "WhatsApp is fastest. For confidential matters, call.") + f'''
<section class="s"><div class="wrap split">
<div class="cblock">
<a class="cline" data-wa-quick="Contact page" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener">{WA.replace("<svg", "<svg class=\"ic\" style=\"width:22px;height:22px;color:#1FA855\"")}<div><b>WhatsApp</b><span>{SITE["phone"]}</span></div></a>
<a class="cline" href="tel:{SITE["phone_href"]}">{ICONS["phone"]}<div><b>Call</b><span>{SITE["phone"]}</span></div></a>
<a class="cline" href="mailto:{SITE["email"]}">{ICONS["mail"]}<div><b>Email</b><span>{SITE["email"]}</span></div></a>
<a class="cline" href="mailto:{SITE["alt_email"]}">{ICONS["mail"]}<div><b>Email (alternative)</b><span>{SITE["alt_email"]}</span></div></a>
<a class="cline" href="{maps}" target="_blank" rel="noopener">{ICONS["pin"]}<div><b>Head office</b><span>{E(SITE["address"])}<br>Visits by appointment. Open in Google Maps.</span></div></a>
<p class="small muted">Artizanni Business Services Limited · RC 1065469</p>
</div>
<div><form class="form" data-wa="C" data-title="Website message" data-intro="I have a question.">
<h3>Send a quick message</h3>
<div class="fieldrow"><label class="f" for="cn">Your name</label><input class="in" id="cn" name="name" data-label="Name" required autocomplete="name"></div>
<div class="fieldrow"><label class="f" for="ct">Topic</label><select class="in" id="ct" name="topic" data-label="Topic"><option>General question</option><option>New project</option><option>Build from abroad</option><option>Interiors</option><option>Land or property</option><option>Personnel / placements</option><option>Supplier or partner</option><option>Media</option></select></div>
<div class="fieldrow"><label class="f" for="cm">Message</label><textarea class="in" id="cm" name="message" data-label="Message" required></textarea></div>
<label class="consent"><input type="checkbox" required data-skip> I agree that Artizanni may use these details to reply, as described in the <a href="{R}privacy/">privacy notice</a>.</label>
<div class="btns" style="margin-top:18px"><button class="btn btn-gold" type="submit">Prepare my message {ARW}</button></div>
</form><div class="form" data-out hidden style="margin-top:16px" aria-live="polite"></div></div>
</div></section>'''
    ld = [crumbs_ld(trail), {"@type": "ContactPage", "url": BASE + path, "about": {"@id": ORG_ID}}]
    page(path, "Contact", f"Contact Artizanni in Utako, Abuja: WhatsApp or call {SITE['phone']}, email {SITE['email']} or {SITE['alt_email']}.", body, active=path, ld=ld, prio="0.8")

def build_requests():
    path = "requests/"; R = root_for(path)
    body = phead(R, [("My requests", path)], "On this device", "My requests", "Requests you prepared on this site are kept only in this browser so you can reopen them. We cannot see this list.") + \
        '<section class="s"><div class="wrap"><div class="reqs" data-requests></div></div></section>'
    page(path, "My requests", "Your Artizanni enquiries saved on this device.", body, noindex=True)

def build_privacy():
    path = "privacy/"; R = root_for(path); trail = [("Privacy notice", path)]
    body = phead(R, trail, "Privacy notice", "How we handle your information.", f"Last updated {datetime.date.today().strftime('%d %B %Y')}.") + f'''
<section class="s"><div class="wrap prose">
<h2>Who we are</h2><p>Artizanni Business Services Limited (RC 1065469), {E(SITE["address"])}, is the data controller for information collected through artizanni.com. Contact: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> or <a href="mailto:{SITE["alt_email"]}">{SITE["alt_email"]}</a>.</p>
<h2>What this website collects</h2><p>This website does not send form answers to a server. When you use a form, your browser assembles a message that <b>you</b> choose to send to us on WhatsApp or by email. We receive only what you send.</p>
<p>A copy of each message you prepare is stored in your own browser (local storage) so you can reopen it on the <a href="{R}requests/">My requests</a> page. You can clear it at any time by clearing this site's data in your browser.</p>
<p>If analytics is switched on, we ask for your consent first and use Google Analytics with IP anonymisation to count visits and clicks. If you decline, no analytics script is loaded.</p>
<h2>How we use your information</h2><p>To reply to your enquiry, prepare proposals, deliver services you engage us for, consider you for placements if you register, and meet legal duties such as customer due diligence for real-estate transactions under anti-money-laundering rules.</p>
<h2>Lawful basis</h2><p>Your consent when you send us a message; steps at your request before a contract; performance of a contract; and legal obligations. We do not sell personal data or use it for automated decisions.</p>
<h2>Sharing</h2><p>Only where needed: for example our escrow trustee, lawyers and surveyors on your instruction, our accountants, and regulators where the law requires. WhatsApp and email providers process messages under their own terms.</p>
<h2>How long we keep it</h2><p>Enquiries that do not become projects: up to 24 months. Project and client records: as long as the law requires for contract, tax and AML purposes.</p>
<h2>Your rights</h2><p>Under the Nigeria Data Protection Act 2023 you may ask to access, correct or delete your data, object to or restrict processing, withdraw consent, or request a copy in a portable format. Email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>. You may also complain to the Nigeria Data Protection Commission.</p>
<h2>Please do not send</h2><p>Bank or card details, passwords, or copies of identity documents through this website or WhatsApp. If we need identity documents for due diligence, we will tell you how to send them securely.</p>
</div></section>'''
    page(path, "Privacy notice", "How Artizanni Business Services Limited collects and uses personal information under the Nigeria Data Protection Act 2023.", body, ld=[crumbs_ld(trail)], prio="0.3")

def build_misc():
    R = "/"
    body = f'<section class="phead"><div class="wrap"><p class="eyebrow">404</p><h1>That page is not on the drawings.</h1><p class="lede">The link may be old. Try the home page or tell us what you were looking for.</p><div class="btns" style="margin-top:20px"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line" href="/projects/">Projects</a><a class="btn btn-line" href="/contact/">Contact</a></div></div></section>'
    # 404 and offline use absolute paths (they are served from any URL depth)
    for name, b in (("404.html", body), ("offline.html", body.replace("404", "Offline").replace("That page is not on the drawings.", "You are offline.").replace("The link may be old. Try the home page or tell us what you were looking for.", "Pages you have opened before still work. Reconnect to see the rest."))):
        page(name, "Page not found" if name == "404.html" else "Offline", "Artizanni", b, noindex=True)
        f = DOCS / name; s = f.read_text(); s = s.replace('href="../', 'href="/').replace('src="../', 'src="/').replace('"root": "../"', '"root": "/"')
        f.write_text(s)

# ================================================================== STANDARD KIT
def build_kit():
    (DOCS / "CNAME").write_text(DOMAIN + "\n")
    (DOCS / ".nojekyll").write_text("")
    key = CFG.get("indexnow_key")
    if key: (DOCS / f"{key}.txt").write_text(key)
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
            "Google-Extended", "Applebot", "Applebot-Extended", "Bingbot", "Googlebot", "CCBot", "*"]
    (DOCS / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\nDisallow: /requests/\n\n" for b in bots) + f"Sitemap: {BASE}sitemap.xml\n")
    urls = "".join(f'<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>' for p, t, d, pr in PAGES)
    (DOCS / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    man = {"name": "Artizanni — design, engineer, build", "short_name": "Artizanni", "start_url": "/?src=app", "scope": "/", "display": "standalone",
           "background_color": "#FAF7F2", "theme_color": "#1A1A1A", "description": SITE["description"],
           "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
           "shortcuts": [{"name": "Start a project", "url": "/start/"}, {"name": "Build from abroad", "url": "/diaspora/"}, {"name": "My requests", "url": "/requests/"}]}
    (DOCS / "manifest.webmanifest").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    shell = ["/", "/services/", "/projects/", "/diaspora/", "/about/", "/start/", "/contact/", "/requests/", "/offline.html",
             f"/assets/style.css?v={V}", f"/assets/app.js?v={V}", f"/assets/pwa.js?v={V}", "/icons/icon-192.png", "/manifest.webmanifest"]
    (DOCS / "sw.js").write_text(f'''// Artizanni service worker, edition {V}
const V = "art-{V}";
const SHELL = {json.dumps(shell)};
self.addEventListener("install", ev => {{ ev.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); }});
self.addEventListener("activate", ev => {{ ev.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); }});
self.addEventListener("message", ev => {{ if (ev.data && ev.data.t === "warm") caches.open(V).then(c => Promise.all(ev.data.urls.map(u => c.match(u).then(hit => hit || c.add(u).catch(() => {{}}))))); }});
self.addEventListener("fetch", ev => {{
  const u = new URL(ev.request.url);
  if (ev.request.method !== "GET" || u.origin !== location.origin) return;
  if (ev.request.mode === "navigate") {{
    ev.respondWith(fetch(ev.request).then(r => {{ if (r.ok) {{ const c = r.clone(); caches.open(V).then(x => x.put(ev.request, c)); }} return r; }})
      .catch(() => caches.match(ev.request, {{ ignoreSearch: true }}).then(r => r || caches.match("/offline.html"))));
    return;
  }}
  ev.respondWith(caches.match(ev.request).then(r => r || fetch(ev.request).then(res => {{
    if (res.ok && !u.pathname.startsWith("/img/")) {{ const c = res.clone(); caches.open(V).then(x => x.put(ev.request, c)); }} return res; }})));
}});
''')
    # llms.txt / llms-full.txt
    lines = [f"# Artizanni Business Services Limited", "", f"> {SITE['description']}", "",
             f"- Registered: CAC RC 1065469, incorporated 17 September 2012", f"- Head office: {SITE['address']}",
             f"- Managing Director: {SITE['md']}, {SITE['md_post']}", "- Escrow partner for diaspora clients: First Trustees",
             f"- Contact: WhatsApp/phone {SITE['phone']}, {SITE['email']}, {SITE['alt_email']}", "", "## Pages", ""]
    lines += [f"- [{t}]({BASE}{p}): {d}" for p, t, d, pr in PAGES]
    (DOCS / "llms.txt").write_text("\n".join(lines) + "\n")
    full = lines + ["", "## Services", ""] + [f"### {s['name']}\n{s['short']} {s['intro']}\n" + "\n".join(f"- {x}" for x in s["items"]) + "\n" for s in SERVICES]
    full += ["## Build from abroad (escrow)", DIASPORA["short"], ""] + [f"- {m}: {t} (evidence: {e})" for m, t, e in MILESTONES]
    full += ["", "## Contracting register (from the Corporate Profile)", ""] + [f"{r[0]}. {r[1]}: {r[2]} ({r[3]})" for r in REGISTER]
    full += ["", "## FAQ", ""] + [f"Q: {q}\nA: {a}\n" for q, a in DIASPORA_FAQ + GENERAL_FAQ]
    (DOCS / "llms-full.txt").write_text("\n".join(full) + "\n")

if __name__ == "__main__":
    for d in ["services", "projects", "diaspora", "about", "start", "contact", "requests", "privacy"]:
        shutil.rmtree(DOCS / d, ignore_errors=True)
    build_home(); build_services(); build_projects(); build_diaspora(); build_about(); build_start(); build_contact(); build_requests(); build_privacy(); build_misc(); build_kit()
    print(f"built {len(PAGES)} indexable pages, edition {V}")
