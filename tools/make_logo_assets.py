# -*- coding: utf-8 -*-
"""
Build every Wellforge logo asset from the master artwork.

The master artwork is a 3D rendered lockup. This script flattens it to a clean
two-colour mark and exports all the sizes and variants the site needs:

    navy blue    #1B2A4A     the W and the wordmark
    dark golden  #B8861F     the F and arrow

Method
------
1. Flood-fill the white background inward from the borders, so specular
   highlights inside the shapes are not punched out.
2. Close enclosed white letter counters (the holes in O, R, ...) above a size
   threshold; smaller enclosed whites are highlights and stay filled.
3. Repaint every remaining pixel navy or gold according to its original hue.
4. Despeckle: flip small colour islands left over from the 3D shading to
   whichever colour surrounds them.
5. Render at source resolution with hard edges, then downsample with LANCZOS so
   the edges anti-alias cleanly.

Output (assets/img/)
--------------------
    logo-full.png         header lockup, navy wordmark
    logo-full-light.png   footer lockup, white wordmark for dark backgrounds
    logo-mark.png         WF monogram on its own
    logo-mark-light.png   WF monogram for dark backgrounds
    favicon.png           180 px tab icon on a navy tile
    apple-touch-icon.png  512 px home-screen icon

Run:  python tools/make_logo_assets.py
"""

import colorsys
import os
import sys
from collections import deque

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
SRC = os.path.join(OUT, "source", "logo-original.png")

NAVY = (0x1B, 0x2A, 0x4A)
NAVY_TILE = (0x1B, 0x2A, 0x4A)
GOLD_DARK = (0xB8, 0x86, 0x1F)
LIGHT = (0xFF, 0xFF, 0xFF)

BG_SCORE = 0.86            # (1 - saturation) * value above this is white-ish

# Letter counters (the holes in O, R, G ...) are printed pure white, while the
# highlights inside the metallic mark are tinted - measured saturation is about
# 0.02 for a counter versus 0.28 for a highlight. Detecting counters on
# brightness alone fills them in, so the test is brightness AND neutrality.
COUNTER_MIN_VALUE = 0.85
COUNTER_MAX_SAT = 0.12
COUNTER_MIN_AREA = 40
GOLD_HUE = (8.0, 62.0)     # degrees; the arrow's warm hue range in the source


# ---------------------------------------------------------------------------
# Flattening
# ---------------------------------------------------------------------------
def analyse(img):
    w, h = img.size
    px = img.load()
    hue = [0.0] * (w * h)
    sat = [0.0] * (w * h)
    whiteish = bytearray(w * h)
    counterish = bytearray(w * h)
    for y in range(h):
        row = y * w
        for x in range(w):
            r, g, b = px[x, y]
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            i = row + x
            hue[i], sat[i] = hh * 360.0, ss
            if (1.0 - ss) * vv >= BG_SCORE:
                whiteish[i] = 1
            if vv >= COUNTER_MIN_VALUE and ss <= COUNTER_MAX_SAT:
                counterish[i] = 1
    return w, h, hue, sat, whiteish, counterish


def flood_background(w, h, whiteish):
    bg = bytearray(w * h)
    q = deque()

    def push(i):
        if whiteish[i] and not bg[i]:
            bg[i] = 1
            q.append(i)

    for x in range(w):
        push(x)
        push((h - 1) * w + x)
    for y in range(h):
        push(y * w)
        push(y * w + w - 1)

    while q:
        i = q.popleft()
        x, y = i % w, i // w
        if x > 0:     push(i - 1)
        if x < w - 1: push(i + 1)
        if y > 0:     push(i - w)
        if y < h - 1: push(i + w)
    return bg


def close_counters(w, h, whiteish, bg):
    seen = bytearray(w * h)
    holes = 0
    for start in range(w * h):
        if not whiteish[start] or bg[start] or seen[start]:
            continue
        blob, q = [], deque([start])
        seen[start] = 1
        while q:
            i = q.popleft()
            blob.append(i)
            x, y = i % w, i // w
            for j in ((i - 1) if x > 0 else -1, (i + 1) if x < w - 1 else -1,
                      (i - w) if y > 0 else -1, (i + w) if y < h - 1 else -1):
                if j >= 0 and whiteish[j] and not bg[j] and not seen[j]:
                    seen[j] = 1
                    q.append(j)
        if len(blob) >= COUNTER_MIN_AREA:
            holes += 1
            for i in blob:
                bg[i] = 1
    return holes


def despeckle(w, h, bg, kind, min_area):
    seen = bytearray(w * h)
    flipped = 0
    for start in range(w * h):
        if bg[start] or seen[start]:
            continue
        k = kind[start]
        blob, q = [], deque([start])
        seen[start] = 1
        border = {0: 0, 1: 0}
        while q:
            i = q.popleft()
            blob.append(i)
            x, y = i % w, i // w
            for j in ((i - 1) if x > 0 else -1, (i + 1) if x < w - 1 else -1,
                      (i - w) if y > 0 else -1, (i + w) if y < h - 1 else -1):
                if j < 0 or bg[j]:
                    continue
                if kind[j] == k:
                    if not seen[j]:
                        seen[j] = 1
                        q.append(j)
                else:
                    border[kind[j]] += 1
        if len(blob) < min_area and border[1 - k] > 0:
            flipped += 1
            for i in blob:
                kind[i] = 1 - k
    return flipped


def flatten(img, navy=NAVY, gold=GOLD_DARK, quiet=False):
    w, h, hue, sat, whiteish, counterish = analyse(img)
    bg = flood_background(w, h, whiteish)
    holes = close_counters(w, h, counterish, bg)

    kind = bytearray(w * h)                      # 0 = navy, 1 = gold
    for i in range(w * h):
        if not bg[i] and GOLD_HUE[0] <= hue[i] <= GOLD_HUE[1] and sat[i] > 0.10:
            kind[i] = 1

    flipped = despeckle(w, h, bg, kind, min_area=max(400, (w * h) // 1400))
    if not quiet:
        print("  closed %d letter counters, removed %d shading speckles" % (holes, flipped))

    out = Image.new("RGBA", (w, h))
    dst = out.load()
    for y in range(h):
        row = y * w
        for x in range(w):
            i = row + x
            dst[x, y] = (0, 0, 0, 0) if bg[i] else (gold if kind[i] else navy) + (255,)
    return out


# ---------------------------------------------------------------------------
# Cropping / export helpers
# ---------------------------------------------------------------------------
def autocrop(img, pad=0):
    box = img.getbbox()
    if not box:
        return img
    l, t, r, b = box
    return img.crop((max(0, l - pad), max(0, t - pad),
                     min(img.width, r + pad), min(img.height, b + pad)))


def resize(img, width):
    # A near-identity resample (401px -> 400px, say) would anti-alias flat
    # two-colour artwork and blow its palette from 3 values to ~1800, taking the
    # file from 5 KB to 27 KB for no visible gain. Only resample when the change
    # is actually worth it; the browser downscales the rest cleanly.
    if img.width <= width * 1.02:
        return img
    c = img.copy()
    c.thumbnail((width, img.height * 4), Image.LANCZOS)
    return c


def split_mark(img, min_gap=14, gold=GOLD_DARK, tol=70):
    """The monogram alone - the W, the F and the whole arrow.

    A single vertical cut cannot do this. The arrow of the F rises above the
    wordmark and overhangs its first letter, so cutting at the gap between mark
    and wordmark slices the arrowhead off. (That was the old behaviour, and it
    shipped a clipped monogram.)

    Instead: find the gap as before, then past it keep only the arrow's own gold
    pixels and erase the wordmark. The two never overlap vertically, so what
    survives is the complete mark.
    """
    px = img.split()[3].load()
    w, h = img.size
    empty = []
    for x in range(w):
        e = True
        for y in range(0, h, 2):
            if px[x, y] > 8:
                e = False
                break
        empty.append(e)
    runs, start = [], None
    for x, e in enumerate(empty):
        if e and start is None:
            start = x
        elif not e and start is not None:
            runs.append((start, x)); start = None
    if start is not None:
        runs.append((start, w))
    runs = [r for r in runs if r[0] > w * 0.15 and r[1] < w * 0.75 and (r[1] - r[0]) >= min_gap]
    cut = max(runs, key=lambda r: r[1] - r[0])[0] if runs else int(w * 0.36)

    out = img.copy()
    pix = out.load()
    gr, gg, gb = gold
    for x in range(cut, w):
        for y in range(h):
            r, g, b, a = pix[x, y]
            if a < 8:
                continue
            near_gold = (abs(r - gr) < tol and abs(g - gg) < tol and abs(b - gb) < tol)
            if not near_gold:
                pix[x, y] = (0, 0, 0, 0)          # wordmark - drop it
    return autocrop(out)


def tile(mark, size, bg, radius_ratio=0.16, inset=0.14):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    plate = Image.new("RGBA", (size, size), bg + (255,))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                           radius=int(size * radius_ratio), fill=255)
    canvas.paste(plate, (0, 0), mask)
    avail = int(size * (1 - inset * 2))
    m = mark.copy()
    m.thumbnail((avail, avail), Image.LANCZOS)
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


def social(lockup, w=1200, h=630):
    card = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    card.alpha_composite(Image.new("RGBA", (w, 10), GOLD_DARK + (255,)), (0, h - 10))
    l = lockup.copy()
    l.thumbnail((int(w * 0.72), int(h * 0.52)), Image.LANCZOS)
    card.alpha_composite(l, ((w - l.width) // 2, (h - l.height) // 2 - 10))
    return card.convert("RGB")


# ---------------------------------------------------------------------------
def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else SRC
    if not os.path.isfile(src_path):
        sys.exit("Source artwork not found: %s" % src_path)

    print("source: %s" % src_path)
    src = Image.open(src_path).convert("RGB")
    print("  size: %dx%d" % src.size)

    print("flattening to navy + dark gold...")
    full = autocrop(flatten(src), pad=2)
    print("flattening light variant...")
    full_light = autocrop(flatten(src, navy=LIGHT, quiet=True), pad=2)
    print("  lockup cropped to %dx%d" % full.size)

    mark = split_mark(full)
    mark_light = split_mark(full_light)
    print("  monogram cropped to %dx%d" % mark.size)

    def save(im, name, **kw):
        p = os.path.join(OUT, name)
        im.save(p, **kw)
        print("  wrote assets/img/%s  (%dx%d, %.0f KB)"
              % (name, im.width, im.height, os.path.getsize(p) / 1024.0))

    save(resize(full, 1000), "logo-full.png", optimize=True)
    save(resize(full_light, 1000), "logo-full-light.png", optimize=True)
    save(resize(mark, 400), "logo-mark.png", optimize=True)
    save(resize(mark_light, 400), "logo-mark-light.png", optimize=True)
    save(tile(mark_light, 180, NAVY_TILE), "favicon.png", optimize=True)
    save(tile(mark_light, 512, NAVY_TILE), "apple-touch-icon.png", optimize=True)
    # og-image.png is produced by tools/make_art.py, which has the artwork.
    print("done.")


if __name__ == "__main__":
    main()
