# -*- coding: utf-8 -*-
"""
Download and prepare the site's photography.

Run:  python tools/fetch_photos.py            (needs network, once)
      python tools/fetch_photos.py --check    (verify what is already on disk)

Licensing
---------
Every photograph here is public domain or CC0 - free for commercial use with no
attribution required and no share-alike obligation. That constraint is
deliberate: this is a commercial site, and CC BY-SA imagery would drag a
share-alike obligation onto it while CC BY would require a visible credit beside
every image.

Credits are still recorded in assets/img/photo/CREDITS.md, because knowing where
a file came from matters when someone asks two years from now.

Each source photo is written out at the sizes and crops the layout needs, and
darkened so it sits under the navy/gold palette rather than fighting it.
"""

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "photo")
UA = "WellforgeSiteBuild/1.0 (https://www.wellforgeenergysolutions.com)"

# slug -> source file on Wikimedia Commons, plus how the site uses it.
PHOTOS = {
    "offshore-platform-dusk": {
        "file": "Holstein at Dusk.jpg",
        "licence": "CC0 1.0",
        "credit": "US Bureau of Safety and Environmental Enforcement",
        "alt": "Offshore production platform lit at dusk above a calm sea",
        "crops": [("wide", 2000, 900), ("card", 1200, 800)],
    },
    "offshore-rigs-flare": {
        "file": "An oil rig offshore Vungtau.jpg",
        "licence": "Public domain",
        "credit": "Wikimedia Commons",
        "alt": "Offshore drilling rigs at sea with a gas flare burning at dusk",
        "crops": [("wide", 2000, 900)],
    },
    "crew-transfer": {
        "file": "Oil Platform Crew Transfer.jpg",
        "licence": "CC0 1.0",
        "credit": "US Bureau of Safety and Environmental Enforcement",
        "alt": "Crew transfer vessel alongside an offshore production platform",
        "crops": [("wide", 2000, 900), ("card", 1200, 800)],
    },
    "tricone-bit": {
        "file": "Drill bit tricone worn.jpg",
        "licence": "Public domain",
        "credit": "Wikimedia Commons",
        "alt": "Close-up of a worn tricone rock bit showing its tungsten carbide inserts",
        "crops": [("wide", 1600, 720)],
    },
    "pipeline-inspection": {
        "file": "Ultrasonic pipeline test.jpg",
        "licence": "Public domain",
        "credit": "US Government",
        "alt": "Technician carrying out ultrasonic inspection on a pipeline weld",
        "crops": [("wide", 1600, 720)],
    },
    "pumpjack": {
        "file": "Oil pump Talara Peru.JPG",
        "licence": "Public domain",
        "credit": "Wikimedia Commons",
        "alt": "Beam pumping unit operating at an onshore oil field",
        "crops": [("wide", 1600, 720)],
    },
    "mud-tanks": {
        "file": "Mud tank and shakers during groundwater well drilling.jpg",
        "licence": "Public domain",
        "credit": "Wikimedia Commons",
        "alt": "Mud tanks and shale shakers on a drilling site at sunset",
        "crops": [("wide", 1600, 720)],
    },
    "offshore-inspector": {
        "file": "A Day in the Life of an Inspector (32251895411).jpg",
        "licence": "Public domain",
        "credit": "US Bureau of Safety and Environmental Enforcement",
        "alt": "View from a helicopter approaching an offshore production platform",
        "crops": [("wide", 2000, 900)],
    },
}


# ---------------------------------------------------------------------------
def commons_urls(titles):
    """Resolve Commons file titles to direct download URLs."""
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    got = {}
    titles = list(titles)
    for i in range(0, len(titles), 6):
        params = {
            "action": "query", "format": "json",
            "titles": "|".join("File:" + t for t in titles[i:i + 6]),
            "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        }
        req = Request("https://commons.wikimedia.org/w/api.php?" + urlencode(params),
                      headers={"User-Agent": UA})
        data = json.loads(urlopen(req, timeout=60).read().decode("utf-8"))
        for page in (data.get("query", {}).get("pages", {}) or {}).values():
            if "imageinfo" in page:
                ii = page["imageinfo"][0]
                got[page["title"][5:]] = {
                    "url": ii["url"],
                    "page": ii.get("descriptionurl", ""),
                    "w": ii.get("width"), "h": ii.get("height"),
                }
    return got


def download(url):
    from urllib.request import urlopen, Request
    req = Request(url, headers={"User-Agent": UA})
    return urlopen(req, timeout=180).read()


def prepare(img, width, height, darken=0.26):
    """Cover-crop to the target box, then darken so overlaid text stays legible."""
    from PIL import Image, ImageEnhance
    src = img.convert("RGB")
    sw, sh = src.size
    scale = max(width / float(sw), height / float(sh))
    new = (max(width, int(sw * scale + 0.5)), max(height, int(sh * scale + 0.5)))
    src = src.resize(new, Image.LANCZOS)
    left = (src.width - width) // 2
    top = int((src.height - height) * 0.42)        # bias slightly above centre
    src = src.crop((left, top, left + width, top + height))

    # Take the brightness down a little so overlaid text holds up, but only a
    # little: the CSS veil darkens further, and several of these are already
    # dusk or night shots that go to mud if both passes are heavy.
    src = ImageEnhance.Brightness(src).enhance(1.0 - darken)
    src = ImageEnhance.Color(src).enhance(0.82)
    return src


def main():
    check = "--check" in sys.argv
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    if check:
        missing = []
        for slug, spec in PHOTOS.items():
            for name, w, h in spec["crops"]:
                p = os.path.join(OUT, "%s-%s.jpg" % (slug, name))
                if not os.path.exists(p):
                    missing.append(os.path.relpath(p, ROOT))
        print("missing derivatives: %d" % len(missing))
        for m in missing:
            print("   " + m)
        return 1 if missing else 0

    from PIL import Image
    print("Resolving %d source photographs on Wikimedia Commons..." % len(PHOTOS))
    urls = commons_urls(spec["file"] for spec in PHOTOS.values())

    credits = []
    for slug, spec in PHOTOS.items():
        info = urls.get(spec["file"])
        if not info:
            print("  ! could not resolve %s" % spec["file"])
            continue
        print("  %s  (%sx%s)" % (spec["file"][:52], info["w"], info["h"]))
        raw = download(info["url"])
        img = Image.open(io.BytesIO(raw))
        for name, w, h in spec["crops"]:
            out = prepare(img, w, h)
            path = os.path.join(OUT, "%s-%s.jpg" % (slug, name))
            out.save(path, "JPEG", quality=82, optimize=True, progressive=True)
            print("      -> %s-%s.jpg  %d KB" % (slug, name, os.path.getsize(path) // 1024))
        credits.append((slug, spec, info))

    lines = [
        "# Photography credits",
        "",
        "Every photograph on this site is **public domain or CC0** - free for",
        "commercial use, no attribution required, no share-alike obligation.",
        "The credits below are recorded for provenance, not because they are",
        "legally required.",
        "",
        "Regenerate with `python tools/fetch_photos.py`.",
        "",
        "| File | Source | Licence | Credit |",
        "| --- | --- | --- | --- |",
    ]
    for slug, spec, info in credits:
        lines.append("| `%s-*.jpg` | [%s](%s) | %s | %s |"
                     % (slug, spec["file"], info["page"], spec["licence"], spec["credit"]))
    with io.open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\nwrote assets/img/photo/CREDITS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
