# -*- coding: utf-8 -*-
"""Shared shell, navigation, icons and UI partials for the Wellforge website.

This is the presentation layer. All page copy lives in the content_*.py modules
and in build_site.py; nothing in this file invents wording.
"""

import hashlib as _hashlib
import os as _os
import re as _re
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

import content_services as _SERVICES

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_ASSET_HASH = {}


def asset(path, depth=0):
    """Site-relative URL for an asset, stamped with a hash of its contents.

    Stylesheets, scripts and generated artwork keep the same filename when they
    are rebuilt, so a browser will happily go on serving the previous copy and
    the change appears not to have happened. The stamp changes whenever the
    bytes change, which forces a fresh fetch - and leaves the URL untouched when
    nothing changed, so caching still works.
    """
    if path not in _ASSET_HASH:
        full = _os.path.join(_ROOT, path.replace("/", _os.sep))
        try:
            with open(full, "rb") as fh:
                _ASSET_HASH[path] = _hashlib.md5(fh.read()).hexdigest()[:8]
        except (IOError, OSError):
            _ASSET_HASH[path] = ""      # not built yet; ship the bare path
    stamp = _ASSET_HASH[path]
    return rel(depth) + path + ("?v=" + stamp if stamp else "")

SITE = {
    "name": "Wellforge Energy Solutions",
    "legal": "Wellforge Energy Solutions Private Limited",
    "short": "Wellforge",
    "tagline": "Forged for the Field. Built to Perform.",
    "domain": "https://www.wellforgeenergysolutions.com",
    "phone": "+91-8384031002",
    "phone_link": "+918384031002",
    "email": "sales@wellforgeenergysolutions.com",
    # A role rather than a name: it survives staff changes, and it is what the
    # contact page shows and what the sales contactPoint reports in JSON-LD.
    "contact_person": "General Manager",
    "address_line": "Gurugram, Haryana, India",
    "whatsapp": "https://wa.me/918384031002",
}

# ---------------------------------------------------------------------------
# Icons  (24x24, stroke = currentColor)
# ---------------------------------------------------------------------------
_ICON_PATHS = {
    "phone": '<path d="M6.4 3.5h3.1l1.5 3.8-1.9 1.2a11.2 11.2 0 0 0 5.4 5.4l1.2-1.9 3.8 1.5v3.1a1.7 1.7 0 0 1-1.8 1.7A15.6 15.6 0 0 1 4.7 5.3 1.7 1.7 0 0 1 6.4 3.5Z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3.6 6.2 8.4 6 8.4-6"/>',
    "pin": '<path d="M12 21.5s7-6 7-11.3a7 7 0 1 0-14 0C5 15.5 12 21.5 12 21.5Z"/><circle cx="12" cy="10" r="2.6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18Z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 6.8V12l3.4 2.1"/>',
    "user-check": '<circle cx="9.5" cy="8" r="3.6"/><path d="M3.2 20a6.4 6.4 0 0 1 12.1-2.9"/><path d="m16.4 15.9 1.9 1.9 3.4-3.6"/>',
    "shield": '<path d="M12 2.8 19 6v5.6c0 4.4-3 8.1-7 9.6-4-1.5-7-5.2-7-9.6V6Z"/><path d="m8.9 11.9 2.1 2.1 4.1-4.2"/>',
    "bolt": '<path d="M13.2 2 4.6 13.4h6l-1.1 8.6 8.9-11.7h-6.1Z"/>',
    "tag": '<path d="M20.5 12.5 12.4 20.6a1.9 1.9 0 0 1-2.7 0L3.4 14.3V3.6h10.7l6.4 6.3a1.8 1.8 0 0 1 0 2.6Z"/><circle cx="8" cy="8.1" r="1.5"/>',
    "derrick": '<path d="M12 2.5 4.5 21.5M12 2.5 19.5 21.5M7.6 12.5h8.8M6.2 17h11.6M3 21.5h18M10 5.4h4"/>',
    "well": '<path d="M3 7.5h18M3 12h18M3 16.5h18"/><path d="M12 3.5v13.4"/><path d="m9.6 16.9 2.4 3.6 2.4-3.6Z"/>',
    "wrench": '<path d="M15.2 3.5a5.2 5.2 0 0 0-5 6.7L3.6 16.8a2 2 0 0 0 2.8 2.8l6.6-6.6a5.2 5.2 0 0 0 6.4-6.6L16.6 9 15 7.4l2.6-3.1a5.2 5.2 0 0 0-2.4-.8Z"/>',
    "building": '<path d="M3 21.5h18M5.2 21.5V9.2L12 4.1l6.8 5.1v12.3"/><path d="M10 21.5v-5.2h4v5.2M9.4 11.6h1.8M12.8 11.6h1.8"/>',
    "network": '<circle cx="5" cy="6" r="2.4"/><circle cx="19" cy="6" r="2.4"/><circle cx="12" cy="18.4" r="2.4"/><path d="M7.4 6h9.2M6.3 8.1l4.5 8.2M17.7 8.1l-4.5 8.2"/>',
    "downhole": '<path d="M12 2.2v19.6"/><path d="M7.5 6h9M6.4 10.2h11.2M7.5 14.4h9M8.8 18.6h6.4"/><path d="M9.6 2.2h4.8"/>',
    "steel": '<rect x="2.6" y="5.4" width="18.8" height="5.4" rx="2.7"/><rect x="2.6" y="13.2" width="18.8" height="5.4" rx="2.7"/><path d="M8.1 5.4v5.4M8.1 13.2v5.4"/>',
    "machinery": '<circle cx="12" cy="12" r="3.3"/><path d="M12 2.6v3M12 18.4v3M21.4 12h-3M5.6 12h-3M18.6 5.4l-2.1 2.1M7.5 16.5l-2.1 2.1M18.6 18.6l-2.1-2.1M7.5 7.5 5.4 5.4"/>',
    "fluids": '<path d="M12 2.6s6.3 6.8 6.3 11a6.3 6.3 0 0 1-12.6 0C5.7 9.4 12 2.6 12 2.6Z"/><path d="M7.6 14.6c1.5-1.2 2.9-1.2 4.4 0s2.9 1.2 4.4 0"/>',
    "subsea": '<path d="M7 3.4h10v5.2H7z"/><path d="M9 8.6v4M15 8.6v4"/><path d="M3 15.4c2-1.6 4-1.6 6 0s4 1.6 6 0 4-1.6 6 0"/><path d="M3 20c2-1.6 4-1.6 6 0s4 1.6 6 0 4-1.6 6 0"/>',
    "doc": '<path d="M13.4 2.8H6.6a1.8 1.8 0 0 0-1.8 1.8v14.8a1.8 1.8 0 0 0 1.8 1.8h10.8a1.8 1.8 0 0 0 1.8-1.8V8.4Z"/><path d="M13.4 2.8v5.6h5.8M8.4 13h7.2M8.4 16.6h7.2"/>',
    "arrow-right": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "chevron": '<path d="m4 8 8 8 8-8"/>',
    "rotate": '<path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M20.5 4.2V9h-4.8"/>',
    "arrow-down": '<path d="M12 4v15M6 13l6 6 6-6"/>',
    "layers": '<path d="m12 3 9 4.8-9 4.8-9-4.8Z"/><path d="m3 12.4 9 4.8 9-4.8M3 17l9 4.8L21 17"/>',
    "target": '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="4.6"/><circle cx="12" cy="12" r="1"/>',
}

_ICON_FILLED = {
    "whatsapp": ('<path fill="currentColor" d="M17.5 14.4c-.3-.2-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-2.4-1.5 9 9 0 0 1-1.7-2.1c-.2-.3 0-.5.1-.6l.5-.6a2 2 0 0 0 .3-.5.6.6 0 0 0 0-.6L9 6.6c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.3 3.3 0 0 0-1 2.5 5.8 5.8 0 0 0 1.2 3 13 13 0 0 0 5 4.4 16 16 0 0 0 1.7.6 4 4 0 0 0 1.8.1 3 3 0 0 0 2-1.4 2.4 2.4 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.4Z"/>'
                 '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.5 15.2L2 22.5l5.4-1.4A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/>'),
}


def icon(name, cls=""):
    """Return an inline SVG icon."""
    attr_cls = ' class="%s"' % cls if cls else ""
    if name in _ICON_FILLED:
        return ('<svg%s viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
                % (attr_cls, _ICON_FILLED[name]))
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (attr_cls, _ICON_PATHS[name]))


def range_id(title):
    """Stable anchor id for a product group heading."""
    plain = _re.sub(r"&[a-zA-Z#0-9]+;", " ", title).lower()
    return "range-" + _re.sub(r"-+", "-", _re.sub(r"[^a-z0-9]+", "-", plain)).strip("-")


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
import content_products as _PRODUCTS

# Derived from the product content, so the menu and the footer can never drift
# out of step with the category pages that actually exist.
PRODUCT_LINKS = [(c["nav_title"], "products/%s.html" % c["slug"]) for c in _PRODUCTS.CATEGORIES]

# The mega-menu: every category with its product groups beneath it. Groups link
# to their own section on the category page.
PRODUCT_MEGA = [
    {
        "title": c["nav_title"],
        "href": "products/%s.html" % c["slug"],
        "groups": [(r["title"], "products/%s.html#%s" % (c["slug"], range_id(r["title"])))
                   for r in c["ranges"]],
    }
    for c in _PRODUCTS.CATEGORIES
]

NAV = [
    {"key": "home", "label": "Home", "href": "index.html"},
    {"key": "about", "label": "About Us", "href": "about.html", "panel": [
        ("Our Story &amp; Purpose", "about.html#our-story"),
        ("Mission &amp; Vision", "about.html#mission-vision"),
        ("Core Values", "about.html#core-values"),
        ("Leadership &amp; Expertise", "about.html#leadership"),
    ]},
    {"key": "sourcing", "label": "Strategic Sourcing", "href": "strategic-sourcing.html", "panel": [
        ("Who We Serve", "strategic-sourcing.html#who-we-serve"),
        ("Sourcing Process (5 Steps)", "strategic-sourcing.html#sourcing-process"),
        ("The Wellforge Advantage", "strategic-sourcing.html#wellforge-advantage"),
        ("Compliance &amp; Standards", "strategic-sourcing.html#compliance-standards"),
    ]},
    {"key": "services", "label": "Our Services", "href": "our-services.html",
     # generated from content_services.SERVICES - reorder there, the menu follows
     "panel": [(svc["nav"], "our-services.html#" + svc["id"]) for svc in _SERVICES.SERVICES]},
    {"key": "products", "label": "Products &amp; Equipment", "href": "product-sourcing.html",
     "mega": PRODUCT_MEGA},
    {"key": "blogs", "label": "Blogs", "href": "blogs.html"},
]


def rel(depth):
    return "../" * depth



# ---------------------------------------------------------------------------
# 3D scenes
# ---------------------------------------------------------------------------
SCENE_POSTER = {
    "rig": "art/cat-drilling-equipment-tools.svg",
    "tricone": "art/cat-drilling-equipment-tools.svg",
    "pdc": "art/cat-drilling-equipment-tools.svg",
    "casing": "art/cat-downhole-completion-octg.svg",
    "packer": "art/cat-downhole-completion-octg.svg",
    "tree": "art/cat-surface-production-artificial-lift.svg",
    "mudmotor": "art/cat-fluids-solids-control-workover.svg",
    "gears": "art/cat-casting-forging-machining.svg",
    "valve": "art/cat-plant-machinery-industrial-tools.svg",
}


def scene(name, depth=0, caption="", cls="", poster=True, hint=True):
    """An interactive WebGL model.

    The <canvas> sits on top of a still illustration. If WebGL is unavailable
    the canvas never initialises and the illustration is what the visitor sees,
    so the block is never empty.
    """
    r = rel(depth)
    fallback = ""
    if poster:
        fallback = ('<img class="scene__poster" src="%s" alt="" '
                    'loading="lazy" decoding="async" width="860" height="620">'
                    % asset("assets/img/" + SCENE_POSTER.get(name, "art/grid-tech.svg"), depth))
    hint_html = ""
    if hint:
        hint_html = ('<span class="scene__hint">%s Drag to rotate</span>'
                     % icon("rotate"))
    cap = '<p class="scene__caption">%s</p>' % caption if caption else ""
    return """<div class="scene %s" data-scene="%s">
  %s
  <canvas class="scene__canvas" role="img" aria-label="Interactive 3D model"></canvas>
  %s
  %s
</div>""" % (cls, name, fallback, hint_html, cap)


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------
def logo(depth, footer=False):
    """Header / footer logo lockup.

    The site runs on a dark ground throughout, so both header and footer use
    the light variant of the artwork (silver "W" and light wordmark). The
    brand-gold "F" arrow is common to both.
    """
    r = rel(depth)
    return ('<a class="logo" href="%sindex.html" aria-label="%s - home">'
            '<img class="logo__img" src="%s" '
            'alt="%s" width="973" height="309" decoding="async">'
            '</a>' % (r, SITE["name"],
                      asset("assets/img/logo-full-light.png", depth), SITE["name"]))


def head(page, depth):
    r = rel(depth)
    canonical = SITE["domain"] + "/" + page["path"]
    og_image = SITE["domain"] + "/assets/img/og-image.png"
    schema = page.get("schema", "")
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{legal}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogimage}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimage}">
<meta name="theme-color" content="#0A101C">
<meta name="color-scheme" content="dark light">
<meta name="geo.region" content="IN-HR">
<meta name="geo.placename" content="Gurugram, Haryana, India">
<link rel="icon" type="image/png" sizes="180x180" href="{r}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{css}">
<script>
/* Scroll-reveal only hides content while the interface script is alive. If it
   is blocked or never boots, the flag is dropped and every section shows. */
(function (d) {{
  var h = d.documentElement;
  h.className += " js";
  setTimeout(function () {{
    if (!h.hasAttribute("data-wf-ready")) h.className = h.className.replace(/\\bjs\\b/, "");
  }}, 2500);
}})(document);
</script>
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
{schema}
</head>
<body data-page="{nav}">
<a class="skip-link" href="#main">Skip to content</a>
<div class="page-progress" aria-hidden="true"><span></span></div>
""".format(title=page["title"], desc=page["desc"], keywords=page.get("keywords", ""),
           css=asset("assets/css/style.css", depth),
           canonical=canonical, ogimage=og_image, ogtype=page.get("ogtype", "website"),
           name=SITE["name"], legal=SITE["legal"], r=r, schema=schema,
           nav=page.get("nav") or "page")


def header(page, depth):
    r = rel(depth)
    items = []
    for entry in NAV:
        current = " is-current" if entry["key"] == page.get("nav") else ""
        has_panel = "panel" in entry or "mega" in entry
        is_mega = "mega" in entry
        cls = ("nav__item"
               + (" nav__item--has-panel" if has_panel else "")
               + (" nav__item--mega" if is_mega else "")
               + current)
        caret = icon("chevron", "nav__caret") if has_panel else ""
        aria = ' aria-current="page"' if current else ""
        panel = ""
        if is_mega:
            cols = []
            for col in entry["mega"]:
                groups = "".join(
                    '<li><a href="%s%s">%s</a></li>' % (r, href, lbl)
                    for lbl, href in col["groups"])
                cols.append(
                    '<div class="nav__col">'
                    '<a class="nav__col-head" href="%s%s">'
                    '<span>%s</span>%s</a>'
                    '<ul>%s</ul></div>'
                    % (r, col["href"], col["title"],
                       icon("arrow-right", "nav__panel-arrow"), groups))
            panel = ('<div class="nav__panel nav__panel--mega">'
                     '<div class="nav__mega-grid">%s</div>'
                     '<a class="nav__mega-all" href="%sproduct-sourcing.html">'
                     'View all product categories %s</a>'
                     '</div>' % ("".join(cols), r, icon("arrow-right", "nav__panel-arrow")))
        elif has_panel:
            links = "".join(
                '<li><a href="%s%s"><span>%s</span>%s</a></li>'
                % (r, href, lbl, icon("arrow-right", "nav__panel-arrow"))
                for lbl, href in entry["panel"])
            panel = ('<div class="nav__panel"><p class="nav__panel-tag">%s</p>'
                     '<ul>%s</ul></div>' % (entry["label"], links))
        items.append('<li class="%s"><a class="nav__link" href="%s%s"%s>%s%s</a>%s</li>'
                     % (cls, r, entry["href"], aria, entry["label"], caret, panel))

    items.append('<li class="nav__item nav__mobile-cta">'
                 '<a class="btn btn--gold btn--block" href="%scontact.html">Contact Us</a></li>' % r)

    return """<div class="topbar">
  <div class="wrap">
    <p class="topbar__tag">{derrick} Global Oil &amp; Gas Sourcing</p>
    <div class="topbar__set">
      <a class="topbar__item" href="tel:{phone_link}">{phone_i}<span>{phone}</span></a>
      <a class="topbar__item" href="mailto:{email}">{mail_i}<span>{email}</span></a>
    </div>
  </div>
</div>

<header class="site-header" id="site-header">
  <div class="wrap">
    {logo}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle navigation menu">
      <span></span><span></span><span></span>
    </button>
    <nav id="primary-nav" class="nav" aria-label="Primary">
      <ul class="nav__list">{items}</ul>
    </nav>
    <a class="btn btn--gold btn--sm header__cta" href="{r}contact.html">
      Request a Quote {arrow}
    </a>
  </div>
</header>
<div class="nav-backdrop"></div>
""".format(derrick=icon("derrick", "topbar__ico"),
           phone_i=icon("phone"), phone_link=SITE["phone_link"], phone=SITE["phone"],
           mail_i=icon("mail"), email=SITE["email"], logo=logo(depth),
           items="".join(items), r=r, arrow=icon("arrow-right", "btn__arrow"))


MARQUEE_ITEMS = [
    "API 5CT", "API 5L", "API 6A", "API 7-1", "API 10D", "API 11D1", "API 11D2",
    "ASME B16.5", "ISO 11960", "ISO 14310", "ISO 3183", "NACE MR0175", "EN 10204 3.1",
]


# ---------------------------------------------------------------------------
# Photography
# ---------------------------------------------------------------------------
# Alt text lives here so it stays with the image rather than being retyped at
# every call site. Sources and licences: assets/img/photo/CREDITS.md
PHOTO_ALT = {
    "offshore-platform-dusk": "Offshore production platform lit at dusk above a calm sea",
    "offshore-rigs-flare": "Offshore drilling rigs at sea with a gas flare burning at dusk",
    "crew-transfer": "Crew transfer vessel alongside an offshore production platform",
    "tricone-bit": "Close-up of a worn tricone rock bit showing its tungsten carbide inserts",
    "pipeline-inspection": "Technician carrying out ultrasonic inspection on a pipeline weld",
    "pumpjack": "Beam pumping unit operating at an onshore oil field",
    "mud-tanks": "Mud tanks and shale shakers on a drilling site at sunset",
    "offshore-inspector": "View from a helicopter approaching an offshore production platform",
}

PHOTO_SIZE = {"wide": (2000, 900), "card": (1200, 800)}


def photo(slug, variant="wide", depth=0, cls="", caption="", eyebrow="", lazy=True):
    """A full-width photographic band.

    The image is already darkened when it is generated, and a gradient plus the
    technical grid go over the top, so headline text stays legible and the
    photograph sits inside the palette instead of fighting it.
    """
    w, h = PHOTO_SIZE.get(variant, PHOTO_SIZE["wide"])
    text = ""
    if eyebrow or caption:
        text = ('<div class="wrap"><div class="photo-band__text">'
                + ('<p class="eyebrow">%s</p>' % eyebrow if eyebrow else "")
                + ('<p class="photo-band__caption">%s</p>' % caption if caption else "")
                + "</div></div>")
    return """<section class="photo-band {cls}">
  <img src="{src}" alt="{alt}" width="{w}" height="{h}"{loading} decoding="async">
  <span class="photo-band__veil" aria-hidden="true"></span>
  {text}
</section>""".format(
        cls=cls,
        src=asset("assets/img/photo/%s-%s.jpg" % (slug, variant), depth),
        alt=PHOTO_ALT.get(slug, ""), w=w, h=h,
        loading=' loading="lazy"' if lazy else "",
        text=text)


def photo_figure(slug, variant="card", depth=0, caption=""):
    """A photograph used inline in a content column, beside prose or a table."""
    w, h = PHOTO_SIZE.get(variant, PHOTO_SIZE["card"])
    cap = '<figcaption>%s</figcaption>' % caption if caption else ""
    return """<figure class="figure figure--photo reveal">
  <img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">
  {cap}
</figure>""".format(src=asset("assets/img/photo/%s-%s.jpg" % (slug, variant), depth),
                    alt=PHOTO_ALT.get(slug, ""), w=w, h=h, cap=cap)


def marquee():
    """Continuous strip of the specifications Wellforge supplies against."""
    run = "".join('<span>%s</span><i aria-hidden="true">&bull;</i>' % s for s in MARQUEE_ITEMS)
    return ('<div class="marquee" aria-label="Standards we supply against">'
            '<div class="marquee__track">%s%s</div></div>' % (run, run))


def footer(depth):
    r = rel(depth)
    quick = [("About Us", "about.html"), ("Strategic Sourcing", "strategic-sourcing.html"),
             ("Our Services", "our-services.html"),
             ("Products &amp; Equipment", "product-sourcing.html"),
             ("Blogs", "blogs.html"), ("Contact Us", "contact.html")]
    quick_html = "".join('<li><a href="%s%s">%s</a></li>' % (r, href, label) for label, href in quick)
    cats_html = "".join('<li><a href="%s%s">%s</a></li>' % (r, href, label)
                        for label, href in PRODUCT_LINKS)

    return """{marquee}
<footer class="site-footer">
  <div class="footer-main">
    <div class="wrap">
      <div class="footer-grid">

        <div class="footer-brand">
          {logo}
          <p class="footer-tagline">{tagline}</p>
          <p>Oil &amp; gas equipment sourcing and supply chain solutions for drilling companies, E&amp;P
             operators, contractors and service providers. Headquartered in Gurugram, India &mdash; serving
             clients globally.</p>
          <a class="btn btn--whatsapp btn--sm" href="{whatsapp}" target="_blank" rel="noopener">
            {wa} WhatsApp
          </a>
        </div>

        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul>{quick}</ul>
        </div>

        <div class="footer-col">
          <h4>Product Categories</h4>
          <ul>{cats}</ul>
        </div>

        <div class="footer-col">
          <h4>Contact</h4>
          <ul class="footer-contact">
            <li>{pin}<span>{legal}<br>{address}</span></li>
            <li>{phone_i}<span><a href="tel:{phone_link}">{phone}</a></span></li>
            <li>{mail_i}<span><a href="mailto:{email}">{email}</a></span></li>
          </ul>
          <div class="footer-badges">
            <span class="badge"><span>API</span> Specifications</span>
            <span class="badge"><span>ISO</span> 11960</span>
            <span class="badge"><span>ISO</span> 14310</span>
          </div>
        </div>

      </div>
    </div>
  </div>

  <div class="wrap">
    <div class="footer-bottom">
      <p class="mb-0">&copy; <span data-year>2026</span> {legal} &middot; Gurugram, Haryana, India</p>
      <ul>
        <li><a href="{r}privacy-policy.html">Privacy Policy</a></li>
        <li><a href="{r}terms-of-use.html">Terms of Use</a></li>
        <li><a href="{r}sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
</footer>

<a class="wa-float" href="{whatsapp}" target="_blank" rel="noopener" aria-label="Message Wellforge on WhatsApp">{wa}</a>
<button class="to-top" type="button" aria-label="Back to top">{up}</button>

<script src="{js_engine}" defer></script>
<script src="{js_scenes}" defer></script>
<script src="{js_main}" defer></script>
</body>
</html>
""".format(marquee=marquee(), logo=logo(depth, footer=True), tagline=SITE["tagline"],
           quick=quick_html, cats=cats_html,
           pin=icon("pin"), legal=SITE["legal"], address=SITE["address_line"],
           phone_i=icon("phone"), phone_link=SITE["phone_link"],
           phone=SITE["phone"], mail_i=icon("mail"), email=SITE["email"],
           whatsapp=SITE["whatsapp"], wa=icon("whatsapp"), r=r,
           js_engine=asset("assets/js/wf3d.js", depth),
           js_scenes=asset("assets/js/wf-scenes.js", depth),
           js_main=asset("assets/js/main.js", depth),
           up=icon("arrow-down", "to-top__ico"))


# ---------------------------------------------------------------------------
# Reusable blocks
# ---------------------------------------------------------------------------
def page_hero(eyebrow, title, lead, crumbs=None, depth=0, scene_name=None, aside=None):
    """Interior page hero. Optionally carries a 3D model or an illustration."""
    r = rel(depth)
    crumb_html = ""
    if crumbs:
        parts = ['<li><a href="%sindex.html">Home</a></li>' % r]
        for label, href in crumbs[:-1]:
            parts.append('<li><a href="%s%s">%s</a></li>' % (r, href, label))
        parts.append('<li><span aria-current="page">%s</span></li>' % crumbs[-1][0])
        crumb_html = ('<nav class="crumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>'
                      % "".join(parts))
    # An empty eyebrow simply omits the line.
    eyebrow_html = '<p class="eyebrow">%s</p>' % eyebrow if eyebrow else ""

    side = aside or ""
    if scene_name and not aside:
        side = scene(scene_name, depth=depth, cls="scene--hero")
    cls = " page-hero--split" if side else ""

    return """<section class="page-hero{cls}">
  <div class="page-hero__bg" aria-hidden="true"></div>
  <div class="wrap">
    <div class="page-hero__text">
      {crumbs}
      {eyebrow}
      <h1>{title}</h1>
      <p class="page-hero__lead">{lead}</p>
    </div>
    {side}
  </div>
</section>""".format(cls=cls, crumbs=crumb_html, eyebrow=eyebrow_html, title=title,
                     lead=lead, side=side)


STATS = [
    ("5+", "Core Service<br>Verticals"),
    ("360&deg;", "Supply Chain<br>Coverage"),
    ("API", "Spec Compliant<br>Standards"),
    ("3+", "Continents<br>Served"),
]

_LEADING_NUMBER = _re.compile(r"^(\d+)(.*)$")


def stats_block(extra_class=""):
    """The statistics strip.

    Numeric figures count up when they scroll into view, but the real value is
    always in the markup - main.js resets it to zero only when it is about to
    animate, so with JavaScript off (or for a crawler) the numbers still read
    correctly. Non-numeric figures like "API" are simply printed.
    """
    cards = []
    for value, label in STATS:
        m = _LEADING_NUMBER.match(value)
        if m:
            figure = ('<span data-count="%s">%s</span><i>%s</i>'
                      % (m.group(1), m.group(1), m.group(2)))
        else:
            figure = value
        cards.append('<div class="stat reveal"><p class="stat__num">%s</p>'
                     '<p class="stat__label">%s</p></div>' % (figure, label))
    return '<div class="stats %s">%s</div>' % (extra_class, "".join(cards))


def section_head(eyebrow, title, lead="", center=False, extra=""):
    cls = "section-head section-head--center" if center else "section-head"
    lead_html = '<p class="lead">%s</p>' % lead if lead else ""
    return ('<div class="%s reveal"><p class="eyebrow">%s</p><h2>%s</h2>%s%s</div>'
            % (cls, eyebrow, title, lead_html, extra))


REQUIREMENT_OPTIONS = [c["short"] for c in _PRODUCTS.CATEGORIES] + ["General Enquiry"]


def enquiry_form(form_id, subject, button_label, heading=None, blurb=None, preselect=None,
                 compact=False):
    """Standard enquiry form used on the contact page and every category page."""
    options = "".join(
        '<option value="%s"%s>%s</option>'
        % (opt, " selected" if preselect == opt else "", opt)
        for opt in REQUIREMENT_OPTIONS)

    head_html = ""
    if heading:
        head_html += '<p class="form-card__tag">Enquiry</p><h3>%s</h3>' % heading
    if blurb:
        head_html += "<p>%s</p>" % blurb

    return """<div class="form-card reveal">
  {head}
  <form id="{fid}" data-enquiry data-subject="{subject}" novalidate>
    <div class="field-grid">
      <div class="field">
        <label for="{fid}-name">Name</label>
        <input id="{fid}-name" name="name" type="text" autocomplete="name" placeholder="Full name">
      </div>
      <div class="field">
        <label for="{fid}-email">Email <span class="req">*</span></label>
        <input id="{fid}-email" name="email" type="email" required autocomplete="email" placeholder="you@company.com">
        <span class="field__error">Please enter a valid email address.</span>
      </div>
      <div class="field">
        <label for="{fid}-phone">Phone</label>
        <input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" placeholder="+91 00000 00000">
      </div>
      <div class="field">
        <label for="{fid}-company">Company</label>
        <input id="{fid}-company" name="company" type="text" autocomplete="organization" placeholder="Company name">
      </div>
      <div class="field field--full">
        <label for="{fid}-requirement">Requirement Type</label>
        <select id="{fid}-requirement" name="requirement">{options}</select>
      </div>
      <div class="field field--full">
        <label for="{fid}-message">Message</label>
        <textarea id="{fid}-message" name="message" placeholder="Tell us about your requirement - specification, grade, quantity, delivery location and required date."></textarea>
      </div>
    </div>
    <div class="hp-field" aria-hidden="true">
      <label for="{fid}-hp">Do not fill this field</label>
      <input id="{fid}-hp" name="company_website" type="text" tabindex="-1" autocomplete="off">
    </div>
    <div class="btn-row" style="margin-top:24px">
      <button class="btn btn--gold" type="submit">{button} {arrow}</button>
    </div>
    <p class="form-note">We respond to enquiries within 24 hours. Your details are used only to
       respond to this enquiry.</p>
    <p class="form-status"></p>
  </form>
</div>""".format(head=head_html, fid=form_id, subject=subject, options=options,
                 button=button_label, arrow=icon("arrow-right", "btn__arrow"))


def cta_banner(title, body, buttons_html, center=False):
    cls = "cta-banner cta-banner--center" if center else "cta-banner"
    inner = """<h2>{title}</h2>
    <p class="lead">{body}</p>
    <div class="btn-row btn-row--center" style="margin-top:32px">{buttons}</div>"""
    if center:
        return """<section class="{cls}">
  <div class="cta-banner__glow" aria-hidden="true"></div>
  <div class="wrap">
    {inner}
  </div>
</section>""".format(cls=cls, inner=inner.format(title=title, body=body, buttons=buttons_html))
    return """<section class="{cls}">
  <div class="cta-banner__glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="cta-split">
      <div>
        <h2>{title}</h2>
        <p class="lead mb-0">{body}</p>
      </div>
      <div class="btn-row">{buttons}</div>
    </div>
  </div>
</section>""".format(cls=cls, title=title, body=body, buttons=buttons_html)


def render(page, body, depth=0):
    return head(page, depth) + header(page, depth) + \
        '<main id="main">\n' + body + '\n</main>\n' + footer(depth)
