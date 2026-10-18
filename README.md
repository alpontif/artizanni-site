# artizanni.com

Website for **Artizanni Business Services Limited** (RC 1065469), Utako, Abuja: design-build, engineering, construction, interiors, real estate, project and property management, and the escrow-backed "Build from abroad" service. Every enquiry ends in a pre-written WhatsApp message (or email) carrying a reference number `ART-<type>-YYMMDD-XXXX` (P project, D diaspora, R personnel register, C contact). Nothing is sent to a server.

Same set-up as yellowmetal.store and buildocrat.store: a static site in `docs/`, built by `build.py`, served by GitHub Pages.

## Where things live

| Path | What it is |
|---|---|
| `src/content.py` | **All words**: services, sectors, contracting register, diaspora milestones, FAQs, contact details |
| `src/photos.json` | Photo captions and sectors (images in `docs/img/`, 1600 px and 800 px, JPEG + WebP) |
| `src/style.css`, `src/app.js`, `src/pwa.js` | Design, enquiry forms / WhatsApp / lightbox, install-as-app |
| `site-config.json` | Google / Bing verification codes, GA4 ID (loads only after visitor consent), IndexNow key. Blank = off |
| `build.py` | Builds every page in `docs/` plus sitemap, robots, llms.txt, manifest, service worker |
| `tools/prep_photos.py` | One-off photo selection and compression (already run) |
| `tools/make_icons.py` | One-off app icons and social image (already run) |
| `.github/workflows/build.yml` | On every push: rebuild, commit `docs/`, ping IndexNow |

## Changing things

Edit `src/content.py` (or the CSS/JS), then `python3 build.py` locally, or just push and the workflow rebuilds. To add photos: put the files somewhere the script can read, add them to `PHOTOS` in `tools/prep_photos.py`, run it, then rebuild.

## Run locally

```
python3 build.py
cd docs && python3 -m http.server 8000
```

## One-time setup (GitHub Pages and domain)

1. Create the repo `alpontif/artizanni-site` (public) and push this folder to `main`.
2. **Settings → Pages → Deploy from a branch**, branch `main`, folder `/docs`. Save.
3. **Custom domain:** `artizanni.com`. Save. `docs/CNAME` is already in place.
4. At the DNS provider for `artizanni.com`: four **A** records on `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; and a **CNAME** `www` → `alpontif.github.io`. **Do not touch the MX records** if `aec@artizanni.com` / `kola@artizanni.com` mailboxes are hosted on this domain.
5. Once DNS resolves, tick **Enforce HTTPS**.
6. **Settings → Actions → General → Workflow permissions:** *Read and write*.
7. Point the old `artizanni.umso.co` site to artizanni.com (link or redirect) and update the email footer, LinkedIn page and letterhead.

## Search engines and AI assistants

Built automatically: `sitemap.xml`; `robots.txt` (allows search and AI crawlers, hides `/requests/`); `llms.txt` and `llms-full.txt`; JSON-LD on every page (Organization + GeneralContractor, WebSite, BreadcrumbList, Service, FAQPage, CollectionPage, ItemList); IndexNow after each build; installable app with offline pages.

After launch: add `https://artizanni.com` in **Google Search Console** (HTML tag → paste the `content` value into `google_site_verification`, push, verify, submit the sitemap) and **Bing Webmaster Tools** (import from Search Console). Create or claim the **Google Business Profile** for the Utako office with the same name, address and phone as the site.

## Content rules (ART-KB-BRAND)

Only facts from the Company Fact Sheet, Corporate Profile 2026, the Project Portfolio or the MD. No invented clients, values, testimonials or awards; no superlatives. Secure-space (panic room) work is never shown. Diaspora clients are private. The MD approves before publication.
