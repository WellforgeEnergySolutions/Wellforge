# Wellforge Energy Solutions — Website

A static, fully responsive B2B website for **Wellforge Energy Solutions Pvt. Ltd.**,
Gurugram, Haryana, India.

No frameworks, no build dependencies, no database, **no third-party JavaScript** —
plain HTML, CSS and vanilla JS that can be uploaded to any host. The 3D runs on a
small WebGL engine written for this site, so the pages work offline and open
straight from the filesystem.

All page copy is taken from the approved source document
`Wellforge_Website_Content.pdf`.

---

## Viewing the site

Open `index.html` directly in a browser, or serve the folder:

```bash
python -m http.server 8123
```

Then visit <http://localhost:8123>.

---

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| About Us | `about.html` |
| Strategic Sourcing | `strategic-sourcing.html` |
| Our Services | `our-services.html` |
| Products & Equipment (hub) | `product-sourcing.html` |
| Drilling Equipment & Tools | `products/drilling-equipment-tools.html` |
| Downhole, Completion & OCTG | `products/downhole-completion-octg.html` |
| Surface Production, Valves & Artificial Lift | `products/surface-production-artificial-lift.html` |
| Fluids, Solids Control & Workover Processing | `products/fluids-solids-control-workover.html` |
| Casting, Forging & Machining Components | `products/casting-forging-machining.html` |
| Plant, Machinery & Industrial Tools | `products/plant-machinery-industrial-tools.html` |
| Blogs | `blogs.html` + 6 articles in `blog/` |
| Contact Us | `contact.html` |
| Privacy Policy / Terms of Use | `privacy-policy.html`, `terms-of-use.html` |

Plus `sitemap.xml` and `robots.txt`.

---

## The 3D

Nine oilfield models are generated from primitives at page load — there are no
mesh files to download and no 3D library to fetch.

| Model | Where it appears |
| --- | --- |
| Land drilling rig | homepage hero |
| Gear train | About Us hero, and Casting, Forging & Machining |
| PDC drill bit | Strategic Sourcing hero |
| Retrievable production packer | Products & Equipment hub hero |
| Tricone rock bit | Drilling Equipment & Tools |
| API 5CT casing joint | Downhole, Completion & OCTG |
| Subsea christmas tree | Surface Production, Valves & Artificial Lift |
| Positive displacement mud motor | Fluids, Solids Control & Workover, and Contact |
| Flanged gate valve | Our Services hero, and Plant, Machinery & Industrial Tools |

Each model rotates on its own and can be **dragged to rotate**. On touch devices a
vertical swipe still scrolls the page; only a clearly horizontal drag turns the
model.

| File | What it holds |
| --- | --- |
| `assets/js/wf3d.js` | the engine — 4×4 maths, geometry builders (lathe, cylinder, tube, box, torus, sphere), one PBR-flavoured shader, drag-to-orbit camera |
| `assets/js/wf-scenes.js` | the hardware — material palette, the nine models, and each one's camera framing |

**It degrades cleanly.** Every 3D block is a still technical illustration with a
`<canvas>` on top. If WebGL is unavailable, the canvas never initialises and the
illustration is what the visitor sees. Under `prefers-reduced-motion` the 3D is
not started at all.

Scenes pause automatically when scrolled out of view or when the tab is hidden.

### Adding or changing a model

Add an entry to `MODELS` in `assets/js/wf-scenes.js` with a `build(scene)` and a
camera framing, then reference it by name — `scene("your-model")` in
`tools/templates.py`, or via `page_hero(..., scene_name="your-model")`.

---

## Editing content

The HTML files are **generated**. Edit the sources, then rebuild:

```bash
python tools/build_site.py
```

| What you want to change | File |
| --- | --- |
| Header, footer, navigation, icons, forms, hero blocks | `tools/templates.py` |
| Product categories and groups (drives the mega-menu) | `tools/content_products.py` |
| Product category copy, spec tables, product ranges | `tools/content_products.py` |
| Service pillars (also drives the "Our Services" menu) | `tools/content_services.py` |
| About Us copy | `tools/content_about.py` |
| Blog articles | `tools/content_blog.py` |
| Page layout and section order | `tools/build_site.py` |
| Colours, typography, all styling | `assets/css/style.css` |
| Menus, forms, filters, reveals, tilt | `assets/js/main.js` |
| 3D models and their framing | `assets/js/wf-scenes.js` |
| Illustrations, textures, article covers, share image | `tools/make_art.py` |
| Photography: which photos, crops, darkening | `tools/fetch_photos.py` |
| Where each photo sits on the page | `tools/build_site.py` (`CATEGORY_PHOTO`) |
| Logo files (regenerate from artwork) | `tools/make_logo_assets.py` |

Every contact detail (address, phone, email, WhatsApp) lives in **one place** —
the `SITE` dictionary at the top of `tools/templates.py`. Change it there and
rebuild to update all 21 pages.

If you would rather stop using the generator, just edit the HTML files directly
and ignore the `tools/` folder — the output is completely standalone.

---

## Imagery

Two kinds, from two generators.

**Drawn artwork** — the six category illustrations, the section diagrams, the
four textures, the six article covers and the social share card:

```bash
python tools/make_art.py
```

**Photography** — eight photographs, downloaded once and prepared for the
layout:

```bash
python tools/fetch_photos.py          # needs network
python tools/fetch_photos.py --check  # verify what is on disk
```

Every photograph is **public domain or CC0** — free for commercial use, no
attribution required, no share-alike obligation. That constraint is deliberate:
CC BY would force a visible credit beside each image, and CC BY-SA would drag a
share-alike obligation onto a commercial site. Provenance is recorded in
`assets/img/photo/CREDITS.md`.

Photographs are cover-cropped, darkened slightly, and laid under a gradient veil
plus the technical grid, so they sit inside the navy-and-gold palette instead of
fighting it. Alt text lives in `PHOTO_ALT` in `tools/templates.py`.

### Where the photographs sit

| Page | Photograph |
| --- | --- |
| Home | Offshore platform at dusk, before the closing CTA |
| About Us | Platform approach (markets served) + crew transfer beside the leadership copy |
| Strategic Sourcing | Crew transfer, under "Who We Serve" |
| Our Services | Ultrasonic pipeline inspection, under the QA/QC pillar |
| Contact | Offshore platform, beside the company details |
| Drilling Equipment & Tools | Offshore rigs with gas flare |
| Downhole, Completion & OCTG | Worn tricone rock bit |
| Surface Production & Artificial Lift | Beam pumping unit |
| Fluids, Solids Control & Workover | Mud tanks and shale shakers |

**Categories 05 and 06 carry no photograph.** No public-domain image of casting,
forging, precision machining or industrial plant was good enough to earn its
place, and a generic factory stock shot would say nothing about what Wellforge
actually supplies. Their technical illustrations stand alone until real
photography is available — ideally of your own suppliers' work.

See `assets/img/README.md` for what every file is and how to swap one out.

---

## Enquiry forms

Forms appear at the bottom of every product category page and on the contact
page. Out of the box they **compose a pre-filled email** to
`sales@wellforgeenergysolutions.com` using the visitor's mail client — this
works on static hosting with no backend.

To capture submissions server-side instead, open `assets/js/main.js` and set:

```js
var FORM_ENDPOINT = 'https://formspree.io/f/xxxxxxx';   // or Web3Forms, Netlify, your own handler
```

Submissions are then POSTed as JSON and the mail-client fallback is skipped.
Client-side validation, the honeypot anti-spam field and the success message all
keep working either way.

---

## Before going live

1. **Set a form endpoint** (above) so enquiries are captured server-side.
2. **Update the domain.** `tools/templates.py` → `SITE["domain"]` is set to
   `https://www.wellforgeenergysolutions.com`. It drives canonical URLs, Open
   Graph tags, JSON-LD and `sitemap.xml`. Change it and rebuild.
3. **Review the legal pages.** `privacy-policy.html` and `terms-of-use.html` are
   standard templates and carry a visible note asking for review — remove the
   note (`LEGAL_NOTE` in `tools/build_site.py`) once approved.
4. **Company profile PDF.** The "Download Company Profile" buttons currently open
   an email requesting it. When the PDF exists, drop it in and point those links
   at the file.
5. **Verify in Google Search Console** and submit `sitemap.xml`.

---

## SEO

- Unique `<title>`, meta description and keywords per page, targeting
  *oilfield equipment sourcing India*, *API certified casing and tubing supplier*,
  *downhole completion tools supplier* and *oil and gas procurement partner*.
- Canonical URLs, Open Graph and Twitter card tags on every page.
- JSON-LD structured data: `Organization` + `WebSite` (home), `BreadcrumbList`
  (interior pages), `ItemList` (product hub), `BlogPosting` (articles),
  `ContactPage` (contact), with full `PostalAddress` and `ContactPoint`.
- Semantic headings (exactly one `h1` per page), visible breadcrumbs,
  descriptive link text, `sitemap.xml` and `robots.txt`.
- Geo meta tags for Gurugram, Haryana.

## Accessibility & performance

- Skip link, visible focus rings, ARIA on the menu, breadcrumbs and filters.
- Keyboard-operable navigation and dropdowns; `Escape` closes the mobile drawer.
- `prefers-reduced-motion` honoured — scroll reveals, card tilt, the marquee, the
  SVG animations and the 3D are all disabled.
- **Scroll reveals fail safe.** Content is only hidden while `<html>` carries the
  `js` class, which `main.js` confirms at boot; if the script is blocked or never
  arrives, the flag is dropped after 2.5 s and every section shows. A `<noscript>`
  rule covers JavaScript being switched off entirely.
- No third-party JavaScript. The only external request is Google Fonts
  (Oswald + Barlow), with system-font fallbacks.
- Flat-colour PNG logo assets (~5 KB), SVG artwork everywhere else, lazy loading
  on card and article images. Print stylesheet included, and it drops the
  decoration and prints the copy on white.

---

## Brand

| Token | Value |
| --- | --- |
| Page ground | `#0A101C` (deep navy-black) |
| Panel surface | `#101A2E` → `#1E2E4C` |
| Gold / amber (accent) | `#D9A22B`, highlight `#F2C85C` |
| Reading sheet (articles, legal) | `#F4F6FA` with `#121A29` text |
| Body text on dark | `#E9EEF6`, muted `#9DACC5` |
| Headline face | Oswald (bold, condensed, uppercase) |
| Body face | Barlow |

The logo is unchanged from the approved artwork. It is used in its light variant
throughout, because the site runs on a dark ground in both the header and the
footer.
