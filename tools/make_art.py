# -*- coding: utf-8 -*-
"""
Generates every image on the Wellforge site except the logo.

Run:  python tools/make_art.py

Nothing here is stock artwork - the textures, the five category illustrations,
the section diagrams and the six article covers are all drawn from primitives
in this file, so any of them can be re-proportioned or recoloured by editing
the constants at the top and re-running.

Outputs
    assets/img/art/*.svg      textures, category art, diagrams
    assets/img/blog/*.svg      article covers
    assets/img/og-image.png    social share card (uses the real logo)
"""

import io
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- palette ---------------------------------------------------------------
INK        = "#070C16"      # deepest background
NAVY       = "#101A2E"
NAVY_MID   = "#18253F"
NAVY_LIT   = "#22314F"
STEEL      = "#8FA1BC"
STEEL_DIM  = "#5A6B88"
STEEL_LINE = "#41506B"
ICE        = "#DCE5F1"
GOLD       = "#D9A22B"
GOLD_LIT   = "#F2C85C"
GOLD_DIM   = "#9A741F"
RUST       = "#C4562C"

HEAD_FONT = "Oswald, 'Arial Narrow', Arial, sans-serif"
BODY_FONT = "Barlow, 'Helvetica Neue', Arial, sans-serif"


def write(relpath, text):
    full = os.path.join(ROOT, relpath)
    folder = os.path.dirname(full)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)
    with io.open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  wrote %s" % relpath)


# SVG is XML, and XML predefines only these five entities. An HTML entity such
# as &middot; makes the whole document unparseable - and a browser loading it
# through <img> then renders nothing at all, with no console error. Everything
# else is written out as a literal character instead.
_XML_ENTITIES = {"amp", "lt", "gt", "quot", "apos"}
_ENTITY_CHAR = {
    "middot": u"·", "bull": u"•", "deg": u"°", "plusmn": u"±",
    "times": u"×", "minus": u"−", "mdash": u"—", "ndash": u"–",
    "nbsp": u" ", "hellip": u"…", "Oslash": u"Ø", "oslash": u"ø",
    "rsquo": u"’", "lsquo": u"‘", "ldquo": u"“", "rdquo": u"”",
    "frac12": u"½", "frac14": u"¼", "frac34": u"¾",
}


def xml_safe(markup):
    """Replace non-XML entities with literal characters; keep numeric refs."""
    def repl(m):
        name = m.group(1)
        if name.startswith("#") or name in _XML_ENTITIES:
            return m.group(0)
        if name in _ENTITY_CHAR:
            return _ENTITY_CHAR[name]
        raise ValueError("unmapped entity &%s; in generated SVG" % name)
    return re.sub(r"&(#?[A-Za-z0-9]+);", repl, markup)


def svg(width, height, body, defs="", style="", extra_attr=""):
    return xml_safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d"%s>\n'
        '%s%s%s\n</svg>\n'
        % (width, height, width, height, extra_attr,
           ("<defs>%s</defs>\n" % defs) if defs else "",
           ("<style>%s</style>\n" % style) if style else "",
           body)
    )


# ===========================================================================
#  Drawing helpers - the small vocabulary every illustration is built from
# ===========================================================================
def line(x1, y1, x2, y2, stroke=STEEL_LINE, w=1.4, dash=None, opacity=1.0, cap="round"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.2f" '
            'stroke-linecap="%s" fill="none" opacity="%.2f"%s/>'
            % (x1, y1, x2, y2, stroke, w, cap, opacity, d))


def rect(x, y, w, h, fill="none", stroke=None, sw=1.4, rx=0, opacity=1.0):
    s = ' stroke="%s" stroke-width="%.2f"' % (stroke, sw) if stroke else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"%s '
            'opacity="%.2f"/>' % (x, y, w, h, rx, fill, s, opacity))


def circle(cx, cy, r, fill="none", stroke=None, sw=1.4, opacity=1.0):
    s = ' stroke="%s" stroke-width="%.2f"' % (stroke, sw) if stroke else ""
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s opacity="%.2f"/>'
            % (cx, cy, r, fill, s, opacity))


def ellipse(cx, cy, rx, ry, fill="none", stroke=None, sw=1.4, opacity=1.0):
    s = ' stroke="%s" stroke-width="%.2f"' % (stroke, sw) if stroke else ""
    return ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"%s opacity="%.2f"/>'
            % (cx, cy, rx, ry, fill, s, opacity))


def path(d, fill="none", stroke=None, sw=1.4, opacity=1.0, dash=None, extra=""):
    s = ' stroke="%s" stroke-width="%.2f" stroke-linejoin="round" stroke-linecap="round"' \
        % (stroke, sw) if stroke else ""
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="%s"%s opacity="%.2f"%s%s/>' % (d, fill, s, opacity, da, extra)


def text(x, y, s, size=14, fill=STEEL, font=BODY_FONT, weight="500", anchor="start",
         spacing=0, opacity=1.0):
    ls = ' letter-spacing="%.1f"' % spacing if spacing else ""
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" font-weight="%s" '
            'fill="%s" text-anchor="%s"%s opacity="%.2f">%s</text>'
            % (x, y, font, size, weight, fill, anchor, ls, opacity, s))


_ENTITY = re.compile(r"&(?:#\d+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]*);")


def upper_safe(s):
    """Uppercase display text without mangling XML entities (&amp; -> &AMP;)."""
    out, last = [], 0
    for m in _ENTITY.finditer(s):
        out.append(s[last:m.start()].upper())
        out.append(m.group(0))
        last = m.end()
    out.append(s[last:].upper())
    return "".join(out)


def label(x, y, s, size=12, fill=GOLD):
    """Small uppercase engineering-drawing caption."""
    return text(x, y, upper_safe(s), size=size, fill=fill, font=HEAD_FONT, weight="600", spacing=1.6)


def leader(x1, y1, x2, y2, tx, ty, s, size=11, colour=GOLD):
    """Callout: a thin leader line, a node, and a label."""
    return (line(x1, y1, x2, y2, colour, 1.0, opacity=0.75)
            + circle(x1, y1, 2.6, fill=colour)
            + text(tx, ty, s, size=size, fill=colour, font=HEAD_FONT, weight="500", spacing=1.2))


def dim(x1, y, x2, s, colour=STEEL_DIM, size=11):
    """Horizontal dimension line with arrow ticks and a centred caption."""
    out = [line(x1, y, x2, y, colour, 1.0)]
    for x in (x1, x2):
        out.append(line(x, y - 5, x, y + 5, colour, 1.0))
    out.append(rect((x1 + x2) / 2 - 24, y - 9, 48, 18, fill=NAVY))
    out.append(text((x1 + x2) / 2, y + 4, s, size=size, fill=colour, anchor="middle",
                    font=HEAD_FONT, spacing=0.8))
    return "".join(out)


def hatch_def(pid, colour=STEEL_LINE, gap=7, opacity=0.5):
    return ('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse" '
            'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="%d" '
            'stroke="%s" stroke-width="1" opacity="%.2f"/></pattern>'
            % (pid, gap, gap, gap, colour, opacity))


def grid_def(pid, size=32, colour="#FFFFFF", opacity=0.05):
    return ('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">'
            '<path d="M%d 0 H0 V%d" fill="none" stroke="%s" stroke-width="1" opacity="%.3f"/>'
            '</pattern>' % (pid, size, size, size, size, colour, opacity))


def lgrad(gid, stops, x1="0%", y1="0%", x2="0%", y2="100%"):
    body = "".join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>'
                   % (o, c, a) for o, c, a in stops)
    return ('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'
            % (gid, x1, y1, x2, y2, body))


def rgrad(gid, stops, cx="50%", cy="50%", r="60%"):
    body = "".join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>'
                   % (o, c, a) for o, c, a in stops)
    return ('<radialGradient id="%s" cx="%s" cy="%s" r="%s">%s</radialGradient>'
            % (gid, cx, cy, r, body))


def flowing(dash="10 14", dur="2.4s", reverse=False):
    """Reusable class that animates stroke-dashoffset - fluid and material flow."""
    return dash, dur, reverse


ANIM_STYLE = """
  .flow { stroke-dasharray: 9 13; animation: dashmove 1.9s linear infinite; }
  .flow-slow { stroke-dasharray: 5 11; animation: dashmove 3.4s linear infinite; }
  .flow-rev { animation-direction: reverse; }
  @keyframes dashmove { to { stroke-dashoffset: -44; } }
  .pulse { animation: pulse 2.8s ease-in-out infinite; transform-origin: center; }
  .pulse-b { animation-delay: .9s; }
  .pulse-c { animation-delay: 1.8s; }
  @keyframes pulse { 0%,100% { opacity:.25; r:4 } 50% { opacity:1; r:7 } }
  .draw { stroke-dasharray: 900; stroke-dashoffset: 900;
          animation: draw 3.4s cubic-bezier(.6,0,.2,1) forwards; }
  @keyframes draw { to { stroke-dashoffset: 0; } }
  .rot { animation: rot 14s linear infinite; transform-origin: center; }
  @keyframes rot { to { transform: rotate(360deg); } }
  .bob { animation: bob 4.5s ease-in-out infinite; }
  @keyframes bob { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-9px) } }
  @media (prefers-reduced-motion: reduce) {
    .flow, .flow-slow, .pulse, .draw, .rot, .bob { animation: none; }
    .draw { stroke-dashoffset: 0; }
  }
"""


# ===========================================================================
#  1. Textures
# ===========================================================================
def art_textures():
    # Technical grid, tiles seamlessly behind dark sections.
    body = (rect(0, 0, 160, 160, fill="none")
            + path("M160 0 H0 V160", stroke="#FFFFFF", sw=1, opacity=0.055)
            + path("M80 0 V160 M0 80 H160", stroke="#FFFFFF", sw=1, opacity=0.028)
            + circle(0, 0, 1.6, fill=GOLD, opacity=0.30)
            + circle(160, 0, 1.6, fill=GOLD, opacity=0.30)
            + circle(0, 160, 1.6, fill=GOLD, opacity=0.30)
            + circle(160, 160, 1.6, fill=GOLD, opacity=0.30))
    write("assets/img/art/grid-tech.svg", svg(160, 160, body))

    # Seismic / topographic contours - the backdrop behind quiet sections.
    rows = []
    for i in range(14):
        y = 40 + i * 46
        amp = 16 + (i % 4) * 7
        d = ["M-20 %.1f" % y]
        for x in range(0, 1500, 60):
            d.append("q 30 %.1f 60 0" % (amp if (x // 60 + i) % 2 == 0 else -amp))
        rows.append(path(" ".join(d), stroke=STEEL_LINE, sw=1.1,
                         opacity=0.16 + 0.03 * (i % 3)))
    write("assets/img/art/topo.svg", svg(1440, 680, "".join(rows)))

    # Blueprint hatch, for the light sections.
    body = (rect(0, 0, 120, 120, fill="none")
            + path("M0 120 L120 0 M-30 30 L30 -30 M90 150 L150 90",
                   stroke="#1B2A4A", sw=1, opacity=0.055))
    write("assets/img/art/blueprint.svg", svg(120, 120, body))

    # Film grain, laid over the hero so the gradients do not band.
    defs = ('<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" '
            'numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
            '</filter>')
    write("assets/img/art/noise.svg",
          svg(220, 220, '<rect width="220" height="220" filter="url(#n)" opacity="0.42"/>', defs))


# ===========================================================================
#  2. Category illustrations
# ===========================================================================
W, H = 860, 620


def frame(title, code):
    """Shared drawing-sheet chrome: corner ticks, title block, sheet code."""
    o = []
    for (x, y, dx, dy) in ((24, 24, 1, 1), (W - 24, 24, -1, 1),
                           (24, H - 24, 1, -1), (W - 24, H - 24, -1, -1)):
        o.append(line(x, y, x + 26 * dx, y, GOLD, 1.6, opacity=0.7))
        o.append(line(x, y, x, y + 26 * dy, GOLD, 1.6, opacity=0.7))
    o.append(label(30, H - 42, title, size=13))
    o.append(text(W - 30, H - 42, code, size=12, fill=STEEL_DIM, anchor="end",
                  font=HEAD_FONT, spacing=2.2))
    return "".join(o)


def base_defs(extra=""):
    return (lgrad("bg", [("0%", NAVY_MID, "1"), ("100%", INK, "1")], y2="100%")
            + rgrad("glow", [("0%", GOLD, "0.20"), ("70%", GOLD, "0.03"), ("100%", GOLD, "0")])
            + hatch_def("hatch")
            + grid_def("g")
            + extra)


def sheet(body, title, code, defs_extra=""):
    head = (rect(0, 0, W, H, fill="url(#bg)")
            + rect(0, 0, W, H, fill="url(#g)")
            + ellipse(W * 0.5, H * 0.46, 330, 250, fill="url(#glow)"))
    return svg(W, H, head + body + frame(title, code),
               defs=base_defs(defs_extra), style=ANIM_STYLE,
               extra_attr=' role="img" aria-label="%s"' % title)


def cat_downhole():
    """A retrievable packer set inside cased hole, with the flow path below."""
    cx, top, bot = 430, 96, 500
    o = []

    # Casing walls, hatched, with the cement sheath behind them.
    for sx in (-1, 1):
        x = cx + sx * 150
        o.append(rect(min(x, x + sx * 34), top, 34, bot - top, fill="url(#hatch)",
                      stroke=STEEL_LINE, sw=1.4))
        x2 = cx + sx * 116
        o.append(line(x2, top, x2, bot, STEEL_DIM, 1.2, opacity=0.7))
    o.append(label(cx + 196, 116, "casing"))
    o.append(label(cx - 232, 116, "cement"))

    # Mandrel through-bore.
    o.append(rect(cx - 30, top, 60, bot - top, fill=NAVY_LIT, stroke=STEEL, sw=1.5))
    o.append(line(cx, top - 26, cx, bot + 26, GOLD, 1.0, dash="3 7", opacity=0.55))

    # Upper slips.
    for sy in (0, 1):
        y = 168 + sy * 4
        for sx in (-1, 1):
            o.append(path("M%d %d L%d %d L%d %d L%d %d Z"
                          % (cx + sx * 30, y, cx + sx * 112, y + 22,
                             cx + sx * 112, y + 58, cx + sx * 30, y + 44),
                          fill=NAVY_LIT, stroke=ICE, sw=1.4))
        break
    for k in range(7):
        for sx in (-1, 1):
            xx = cx + sx * (46 + k * 10)
            o.append(line(xx, 176 + k * 3.4, xx, 200 + k * 3.4, GOLD_LIT, 1.6, opacity=0.85))

    # Element stack - three elastomer packing elements energised against casing.
    for i, y in enumerate((248, 300, 352)):
        o.append(path("M%d %d C%d %d %d %d %d %d L%d %d C%d %d %d %d %d %d Z"
                      % (cx - 30, y, cx - 118, y + 6, cx - 118, y + 38, cx - 30, y + 44,
                         cx + 30, y + 44, cx + 118, y + 38, cx + 118, y + 6, cx + 30, y),
                      fill="#1B1F27", stroke=STEEL_DIM, sw=1.3))
        o.append(rect(cx - 118, y + 44, 236, 8, fill=GOLD, opacity=0.9))

    # Lower slips and shoe.
    for sx in (-1, 1):
        o.append(path("M%d %d L%d %d L%d %d L%d %d Z"
                      % (cx + sx * 30, 452, cx + sx * 112, 430,
                         cx + sx * 112, 394, cx + sx * 30, 408),
                      fill=NAVY_LIT, stroke=ICE, sw=1.4))
    o.append(path("M%d 500 L%d 500 L%d 538 L%d 538 Z" % (cx - 30, cx + 30, cx + 18, cx - 18),
                  fill=NAVY_LIT, stroke=STEEL, sw=1.4))

    # Perforations firing into the formation, with production flowing up the bore.
    for k in range(4):
        y = 452 + k * 22
        for sx in (-1, 1):
            o.append(path("M%d %d L%d %d" % (cx + sx * 118, y, cx + sx * 176, y - 10),
                          stroke=RUST, sw=2.4, opacity=0.85))
            o.append(circle(cx + sx * 176, y - 10, 3.2, fill=RUST))
    o.append(path("M%d 520 L%d 150" % (cx, cx), stroke=GOLD_LIT, sw=3,
                  extra=' class="flow"', opacity=0.95))

    # Callouts.
    o.append(leader(cx + 118, 270, 640, 246, 648, 250, "ELEMENT STACK"))
    o.append(leader(cx + 112, 186, 640, 158, 648, 162, "SLIP ASSEMBLY"))
    o.append(leader(cx - 118, 466, 190, 500, 96, 504, "PERFORATIONS"))
    o.append(dim(cx - 150, 566, cx + 150, "2–20 in"))
    o.append(text(96, 150, "API 11D1", size=15, fill=ICE, font=HEAD_FONT, weight="600", spacing=2))
    o.append(text(96, 172, "15,000 psi · 400°F", size=12, fill=STEEL_DIM,
                  font=HEAD_FONT, spacing=1.4))
    return sheet("".join(o), "Downhole, Completion &amp; OCTG", "WF-CAT-02")


def cat_steel():
    """Casing joints in section, a coupling detail and an isometric pipe end."""
    o = []

    # Three nested pipe ends, drawn isometrically.
    for i, (cx, cy, ro, ri, col) in enumerate((
            (232, 232, 118, 92, STEEL),
            (232, 232, 84, 64, STEEL_DIM),
            (232, 232, 52, 36, GOLD))):
        o.append(ellipse(cx, cy, ro, ro * 0.36, fill="none", stroke=col, sw=2.0,
                         opacity=0.9 - i * 0.12))
        o.append(ellipse(cx, cy, ri, ri * 0.36, fill=NAVY, stroke=col, sw=1.4,
                         opacity=0.85 - i * 0.1))
        # Wall thickness, shaded between the two ellipses.
        o.append(path("M%d %d A %d %d 0 0 0 %d %d L %d %d A %d %d 0 0 1 %d %d Z"
                      % (cx - ro, cy, ro, ro * 0.36, cx + ro, cy,
                         cx + ri, cy, ri, ri * 0.36, cx - ri, cy),
                      fill=col, opacity=0.18))
    o.append(label(150, 108, "OD / ID / WT"))
    o.append(dim(114, 372, 350, "4 1/2–13 3/8 in"))

    # A joint with its coupling, in longitudinal section.
    x0, y0, ln, oD, iD = 470, 196, 330, 74, 52
    o.append(rect(x0, y0 - oD / 2, ln, oD, fill="url(#hatch)", stroke=STEEL, sw=1.6))
    o.append(rect(x0, y0 - iD / 2, ln, iD, fill=NAVY, stroke=STEEL_DIM, sw=1.2))
    o.append(line(x0 - 30, y0, x0 + ln + 30, y0, GOLD, 1.0, dash="4 8", opacity=0.6))

    # Coupling over the make-up.
    o.append(rect(x0 + 120, y0 - oD / 2 - 16, 96, oD + 32, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=3))
    for k in range(9):
        xx = x0 + 126 + k * 10
        o.append(line(xx, y0 - oD / 2 - 10, xx + 6, y0 - oD / 2 + 2, GOLD_LIT, 1.3, opacity=0.8))
        o.append(line(xx, y0 + oD / 2 + 10, xx + 6, y0 + oD / 2 - 2, GOLD_LIT, 1.3, opacity=0.8))

    # Mill stencil bands.
    o.append(rect(x0 + 20, y0 - oD / 2, 10, oD, fill=GOLD, opacity=0.85))
    o.append(rect(x0 + 38, y0 - oD / 2, 5, oD, fill=GOLD, opacity=0.55))
    o.append(rect(x0 + 292, y0 - oD / 2, 10, oD, fill=RUST, opacity=0.85))

    o.append(leader(x0 + 168, y0 - oD / 2 - 16, x0 + 190, 118, x0 + 198, 114, "COUPLING"))
    o.append(leader(x0 + 25, y0 + oD / 2, x0 - 6, 316, x0 - 100, 320, "GRADE STENCIL"))

    # Grade ladder.
    grades = ["J55", "K55", "N80", "L80", "C90", "T95", "P110", "Q125"]
    for i, g in enumerate(grades):
        gx = 470 + (i % 4) * 92
        gy = 420 + (i // 4) * 44
        o.append(rect(gx, gy, 78, 30, fill=NAVY_LIT, stroke=STEEL_LINE, sw=1, rx=3))
        o.append(text(gx + 39, gy + 20, g, size=14, fill=GOLD_LIT if i in (2, 3, 6) else STEEL,
                      anchor="middle", font=HEAD_FONT, weight="600", spacing=1.4))
    o.append(label(470, 404, "API 5CT grades"))
    return sheet("".join(o), "Steel &amp; Tubular Products", "WF-CAT-02")


def cat_machinery():
    """CNC spindle over a chucked workpiece, driven by a gear train."""
    o = []

    # Machine column and bed.
    o.append(rect(96, 96, 62, 400, fill=NAVY_LIT, stroke=STEEL_LINE, sw=1.5, rx=3))
    o.append(rect(96, 496, 640, 26, fill=NAVY_LIT, stroke=STEEL_LINE, sw=1.5, rx=3))
    o.append(rect(96, 522, 640, 10, fill=GOLD, opacity=0.75))
    for k in range(11):
        o.append(line(120 + k * 56, 496, 120 + k * 56, 522, STEEL_LINE, 1, opacity=0.5))

    # Cross rail and spindle head.
    o.append(rect(158, 128, 470, 34, fill=NAVY_LIT, stroke=STEEL, sw=1.5, rx=3))
    o.append(rect(392, 128, 116, 92, fill=NAVY_MID, stroke=ICE, sw=1.6, rx=4))
    o.append(rect(432, 220, 36, 62, fill=STEEL_DIM, stroke=ICE, sw=1.3))
    o.append(path("M432 282 L468 282 L456 322 L444 322 Z", fill=GOLD, stroke=GOLD_LIT, sw=1.2))
    o.append(circle(450, 174, 26, fill="none", stroke=GOLD, sw=2))
    o.append(circle(450, 174, 12, fill=NAVY, stroke=STEEL, sw=1.4))

    # Workpiece in a three-jaw chuck.
    o.append(ellipse(450, 400, 96, 34, fill=NAVY_LIT, stroke=STEEL, sw=1.6))
    o.append(rect(354, 400, 192, 78, fill=NAVY_LIT, stroke=STEEL, sw=1.6))
    o.append(ellipse(450, 478, 96, 34, fill=NAVY_MID, stroke=STEEL, sw=1.6))
    o.append(ellipse(450, 400, 44, 15, fill=INK, stroke=GOLD, sw=1.6))
    for k in range(3):
        a = k * 120 + 30
        rx = 450 + math.cos(math.radians(a)) * 118
        ry = 400 + math.sin(math.radians(a)) * 42
        o.append(rect(rx - 15, ry - 11, 30, 22, fill=STEEL_DIM, stroke=ICE, sw=1.2, rx=2))
    # Swarf / chip stream off the cut.
    o.append(path("M470 330 q 40 26 34 62", stroke=GOLD_LIT, sw=2.2, opacity=0.9,
                  extra=' class="flow"'))

    # Gear train driving the spindle.
    def gear(cx, cy, r, teeth, colour, cls=""):
        pts, step = [], 360.0 / teeth
        for t in range(teeth):
            for (rr, off) in ((r, 0.0), (r, 0.20), (r * 1.18, 0.32), (r * 1.18, 0.50),
                              (r, 0.62), (r, 0.82)):
                a = math.radians(t * step + off * step)
                pts.append("%.1f %.1f" % (cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        return ('<g%s style="transform-origin:%.1fpx %.1fpx">' % (cls, cx, cy)
                + path("M" + " L".join(pts) + " Z", fill=NAVY_LIT, stroke=colour, sw=1.6)
                + circle(cx, cy, r * 0.34, fill=NAVY, stroke=colour, sw=1.4)
                + circle(cx, cy, r * 0.12, fill=colour) + "</g>")

    o.append(gear(654, 224, 66, 18, GOLD, cls=' class="rot"'))
    o.append(gear(654, 224 + 108, 44, 12, STEEL, cls=' class="rot"'))

    o.append(leader(450, 174, 300, 96, 200, 100, "5-AXIS SPINDLE"))
    o.append(leader(546, 440, 660, 452, 668, 456, "±0.005 mm"))
    o.append(dim(354, 566, 546, "Ø 800 mm"))
    return sheet("".join(o), "Casting, Forging &amp; Machining", "WF-CAT-05")


def cat_fluids():
    """The active mud circulation loop: pits, pump, well, shakers, back to pits."""
    o = []

    # Mud pits with fluid level.
    o.append(rect(70, 350, 210, 132, fill=NAVY_LIT, stroke=STEEL, sw=1.6, rx=4))
    o.append(rect(76, 396, 198, 80, fill=GOLD_DIM, opacity=0.42))
    o.append(path("M76 398 q 24 -10 49 0 t 49 0 t 49 0 t 49 0", stroke=GOLD, sw=2, opacity=0.9))
    o.append(label(78, 336, "active pits"))

    # Triplex pump.
    o.append(rect(70, 232, 128, 74, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=4))
    for k in range(3):
        o.append(circle(100 + k * 34, 269, 15, fill=NAVY, stroke=GOLD, sw=1.8))
    o.append(label(78, 218, "mud pump"))

    # Standpipe up and the well down.
    o.append(path("M198 269 H332 V182 H452", stroke=STEEL, sw=6, opacity=0.5))
    o.append(path("M198 269 H332 V182 H452", stroke=GOLD_LIT, sw=2.6, extra=' class="flow"'))

    # Wellbore: annulus walls, drill pipe, bit.
    o.append(rect(452, 150, 26, 340, fill="url(#hatch)", stroke=STEEL_LINE, sw=1.3))
    o.append(rect(568, 150, 26, 340, fill="url(#hatch)", stroke=STEEL_LINE, sw=1.3))
    o.append(rect(506, 150, 34, 300, fill=NAVY_LIT, stroke=STEEL, sw=1.5))
    o.append(path("M506 450 L540 450 L534 492 L512 492 Z", fill=STEEL_DIM, stroke=ICE, sw=1.4))
    for k in range(6):
        o.append(circle(512 + (k % 2) * 22, 460 + (k // 2) * 12, 3.4, fill=GOLD_LIT))
    # Down the pipe, out of the bit, up the annulus.
    o.append(path("M523 158 V446", stroke=GOLD_LIT, sw=3, extra=' class="flow"'))
    o.append(path("M490 486 V156", stroke=RUST, sw=2.6, extra=' class="flow flow-rev"'))
    o.append(path("M556 486 V156", stroke=RUST, sw=2.6, extra=' class="flow flow-rev"'))
    o.append(label(452, 124, "annulus return"))

    # Shale shaker deck, returning cuttings to the pit.
    o.append(path("M594 156 H700 V232", stroke=RUST, sw=2.6, extra=' class="flow"'))
    o.append(path("M652 244 L790 244 L764 314 L678 314 Z", fill=NAVY_LIT, stroke=ICE, sw=1.6))
    for k in range(5):
        o.append(line(664 + k * 22, 252, 654 + k * 22, 306, STEEL_LINE, 1.2, opacity=0.7))
    o.append(label(654, 232, "shakers"))
    o.append(path("M700 320 V420 H286", stroke=GOLD, sw=2.4, extra=' class="flow"', opacity=0.9))

    # Chemical drums on the additive skid.
    for k in range(3):
        x = 620 + k * 56
        o.append(rect(x, 402, 44, 78, fill=NAVY_LIT, stroke=STEEL, sw=1.4, rx=5))
        o.append(ellipse(x + 22, 402, 22, 8, fill=NAVY_MID, stroke=STEEL, sw=1.2))
        o.append(rect(x + 4, 428, 36, 12, fill=GOLD, opacity=0.8))
    o.append(label(620, 392, "additives"))
    o.append(text(70, 566, "BARITE · BENTONITE · POLYMERS · LCM · CEMENT ADDITIVES",
                  size=12, fill=STEEL_DIM, font=HEAD_FONT, spacing=2.4))
    return sheet("".join(o), "Fluids, Solids Control &amp; Workover", "WF-CAT-04")


def cat_subsea():
    """Platform, riser, subsea tree and flowline tie-back to a manifold."""
    o = []
    sea = 214

    # Sky, sea and seabed.
    o.append(rect(0, sea, W, 300, fill=NAVY_MID, opacity=0.55))
    for k in range(5):
        y = sea + 26 + k * 62
        o.append(path("M0 %d q 60 -9 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 120 0 t 140 0"
                      % y, stroke=STEEL_LINE, sw=1.1, opacity=0.30))
    o.append(path("M0 %d q 46 -12 92 0 t 92 0 t 92 0 t 92 0 t 92 0 t 92 0 t 92 0 t 116 0"
                  % sea, stroke=STEEL, sw=2.2, opacity=0.85))
    o.append(rect(0, 512, W, H - 512, fill="url(#hatch)", opacity=0.55))
    o.append(line(0, 512, W, 512, STEEL_DIM, 1.6))
    o.append(label(30, 200, "mean sea level"))
    o.append(label(30, 542, "seabed"))

    # Fixed platform: jacket legs, deck, flare and derrick.
    o.append('<g class="bob">')
    o.append(rect(196, 120, 240, 20, fill=NAVY_LIT, stroke=ICE, sw=1.6))
    o.append(rect(210, 92, 92, 28, fill=NAVY_LIT, stroke=STEEL, sw=1.4))
    o.append(rect(332, 84, 62, 36, fill=NAVY_LIT, stroke=STEEL, sw=1.4))
    o.append(path("M262 92 L246 40 L294 40 L278 92", fill="none", stroke=GOLD, sw=1.8))
    o.append(path("M252 40 h36 M256 62 h28", stroke=GOLD, sw=1.4, opacity=0.8))
    # Flare boom.
    o.append(path("M436 128 L520 96", stroke=STEEL, sw=2.4))
    o.append(path("M520 96 q 16 -18 6 -34 q 20 14 12 34 z", fill=RUST, opacity=0.9))
    o.append('</g>')
    for sx in (0, 1):
        x0 = 226 + sx * 168
        o.append(line(x0, 140, x0 - 16 + sx * 32, 512, STEEL, 2.4))
    o.append(line(226, 300, 394, 300, STEEL_LINE, 1.6, opacity=0.7))
    o.append(line(216, 410, 404, 410, STEEL_LINE, 1.6, opacity=0.7))
    o.append(path("M226 140 L394 300 M394 140 L226 300 M216 300 L404 410 M404 300 L216 410",
                  stroke=STEEL_LINE, sw=1.2, opacity=0.55))

    # Riser down to the subsea tree.
    o.append(path("M316 140 V500", stroke=GOLD, sw=3.4, opacity=0.9))
    o.append(path("M316 150 V496", stroke=GOLD_LIT, sw=1.8, extra=' class="flow-slow flow-rev"'))

    # Subsea tree with guide frame.
    tx = 316
    o.append(rect(tx - 54, 452, 108, 60, fill="none", stroke=RUST, sw=2.2))
    o.append(rect(tx - 26, 436, 52, 76, fill=NAVY_LIT, stroke=ICE, sw=1.6))
    o.append(circle(tx - 44, 470, 9, fill=GOLD, opacity=0.9))
    o.append(circle(tx + 44, 470, 9, fill=GOLD, opacity=0.9))
    o.append(leader(tx + 54, 462, 420, 430, 428, 434, "SUBSEA TREE"))

    # Flowline to the manifold, and a second well tied back.
    o.append(path("M370 500 q 90 26 168 0 q 60 -20 118 4", stroke=STEEL, sw=3, opacity=0.75))
    o.append(path("M370 500 q 90 26 168 0 q 60 -20 118 4", stroke=GOLD_LIT, sw=1.8,
                  extra=' class="flow"'))
    o.append(rect(656, 470, 96, 44, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=3))
    for k in range(3):
        o.append(circle(680 + k * 24, 492, 8, fill="none", stroke=GOLD, sw=1.6))
    o.append(leader(704, 470, 730, 420, 660, 412, "MANIFOLD"))

    # ROV, station-keeping.
    o.append('<g class="bob">')
    o.append(rect(536, 372, 52, 32, fill=NAVY_LIT, stroke=GOLD, sw=1.6, rx=3))
    o.append(circle(548, 388, 5, fill=GOLD_LIT))
    o.append(circle(576, 388, 5, fill=GOLD_LIT))
    o.append(path("M562 404 V446", stroke=STEEL_LINE, sw=1.2, dash="3 5"))
    o.append('</g>')
    o.append(text(30, 566, "API 6A · API 17D · ONSHORE, OFFSHORE &amp; SUBSEA PRODUCTION",
                  size=12, fill=STEEL_DIM, font=HEAD_FONT, spacing=2.2))
    return sheet("".join(o), "Subsea, Offshore &amp; Onshore Equipment", "WF-CAT-05")



def cat_drilling():
    """Rig floor in elevation: derrick, drawworks, rotary table and BOP stack."""
    o = []
    floor = 300
    cx = 300

    # Derrick legs and bracing rising off the floor.
    for sx in (-1, 1):
        o.append(line(cx + sx * 150, floor, cx + sx * 58, 60, STEEL, 3.4))
    for k in range(5):
        t0, t1 = k / 5.0, (k + 1) / 5.0
        y0 = floor + (60 - floor) * t0
        y1 = floor + (60 - floor) * t1
        w0 = 150 + (58 - 150) * t0
        w1 = 150 + (58 - 150) * t1
        o.append(line(cx - w0, y0, cx + w0, y0, STEEL_LINE, 1.6, opacity=0.75))
        if k % 2 == 0:
            o.append(line(cx - w0, y0, cx + w1, y1, STEEL_LINE, 1.3, opacity=0.55))
        else:
            o.append(line(cx + w0, y0, cx - w1, y1, STEEL_LINE, 1.3, opacity=0.55))
    o.append(rect(cx - 74, 42, 148, 18, fill=GOLD, opacity=0.9))
    o.append(label(cx - 70, 32, "crown block"))

    # Travelling block, hook and swivel on the drill line.
    o.append(line(cx - 16, 60, cx - 16, 150, STEEL_DIM, 1.6))
    o.append(line(cx + 16, 60, cx + 16, 150, STEEL_DIM, 1.6))
    o.append(rect(cx - 34, 150, 68, 52, fill=NAVY_LIT, stroke=ICE, sw=1.8, rx=3))
    for k in range(3):
        o.append(circle(cx - 18 + k * 18, 176, 11, fill="none", stroke=GOLD, sw=1.6))
    o.append(path("M%d 202 v26 a20 20 0 1 0 8 0 v-26" % (cx - 4), stroke=GOLD, sw=3))
    o.append(leader(cx + 34, 176, 470, 150, 478, 154, "HOOK BLOCK / SWIVEL"))

    # Drill floor, rotary table and master bushing.
    o.append(rect(cx - 178, floor, 356, 16, fill=STEEL_DIM))
    o.append(rect(cx - 178, floor + 16, 356, 8, fill=GOLD, opacity=0.85))
    o.append(ellipse(cx, floor, 62, 20, fill=NAVY_LIT, stroke=ICE, sw=1.8))
    o.append(ellipse(cx, floor, 30, 10, fill=INK, stroke=GOLD, sw=1.8))
    o.append(leader(cx + 62, floor, 470, 300, 478, 304, "ROTARY TABLE"))
    o.append(leader(cx - 62, floor, 150, 262, 56, 266, "MASTER BUSHING"))

    # Drawworks with its brake band.
    o.append(rect(cx - 268, 236, 92, 64, fill=NAVY_LIT, stroke=STEEL, sw=1.6, rx=3))
    o.append(circle(cx - 222, 268, 26, fill="none", stroke=GOLD, sw=2.4))
    o.append(circle(cx - 222, 268, 11, fill=GOLD, opacity=0.85))
    o.append(path("M%d 244 a 26 26 0 0 1 0 48" % (cx - 196), stroke=RUST, sw=3.2))
    o.append(label(cx - 268, 226, "drawworks"))

    # BOP stack below the floor: annular over two ram bodies.
    o.append(rect(cx - 56, floor + 24, 112, 42, fill=NAVY_LIT, stroke=ICE, sw=1.8, rx=4))
    o.append(label(cx + 70, floor + 52, "annular"))
    for k in range(2):
        y = floor + 74 + k * 46
        o.append(rect(cx - 64, y, 128, 38, fill=NAVY_LIT, stroke=STEEL, sw=1.6, rx=3))
        for sx in (-1, 1):
            o.append(rect(cx + (32 if sx > 0 else -64), y + 8, 32, 22, fill=GOLD, opacity=0.8))
    o.append(leader(cx + 64, floor + 96, 470, 420, 478, 424, "RAM BOPs"))
    o.append(line(cx, floor + 66, cx, floor + 172, GOLD, 1.0, dash="3 7", opacity=0.6))

    # Choke and kill lines running off the stack.
    for y in (floor + 90, floor + 136):
        o.append(path("M%d %d H%d" % (cx - 64, y, cx - 190), stroke=RUST, sw=2.6,
                      extra=' class="flow"'))
        o.append(circle(cx - 190, y, 9, fill="none", stroke=RUST, sw=2.2))
    o.append(label(cx - 256, floor + 120, "choke &amp; kill"))

    o.append(dim(cx - 178, 566, cx + 178, "15,000 psi"))
    o.append(text(478, 500, "API 7K &middot; 8C &middot; 16A &middot; 16C", size=13, fill=ICE,
                  font=HEAD_FONT, weight="600", spacing=2))
    return sheet("".join(o), "Drilling Equipment &amp; Tools", "WF-CAT-01")


def cat_surface():
    """Wellhead and christmas tree beside a beam pumping unit."""
    o = []
    ground = 430

    o.append(rect(0, ground, W, 8, fill=STEEL_DIM, opacity=0.8))
    o.append(rect(0, ground + 8, W, H - ground - 8, fill="url(#hatch)", opacity=0.45))

    # --- christmas tree stack -------------------------------------------
    tx = 236
    o.append(rect(tx - 52, ground - 30, 104, 30, fill=NAVY_LIT, stroke=STEEL, sw=1.6))
    o.append(rect(tx - 44, ground - 62, 88, 32, fill=NAVY_LIT, stroke=STEEL, sw=1.6))
    o.append(label(tx + 64, ground - 40, "casing head"))
    o.append(rect(tx - 40, ground - 96, 80, 34, fill=NAVY_LIT, stroke=ICE, sw=1.6))
    o.append(label(tx + 64, ground - 74, "tubing head"))

    # Valve bodies and wing valves up the tree.
    for y in (ground - 140, ground - 184):
        o.append(rect(tx - 26, y, 52, 44, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=2))
        for sx in (-1, 1):
            o.append(rect(tx + (26 if sx > 0 else -58), y + 10, 32, 24,
                          fill=STEEL_DIM, stroke=ICE, sw=1.3, rx=2))
            o.append(circle(tx + sx * 74, y + 22, 12, fill="none", stroke=GOLD, sw=2.2))
            o.append(line(tx + sx * 62, y + 22, tx + sx * 86, y + 22, GOLD, 2))

    # Crown valve and cap.
    o.append(rect(tx - 22, ground - 220, 44, 36, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=2))
    o.append(circle(tx, ground - 236, 16, fill="none", stroke=GOLD, sw=2.6))
    o.append(line(tx - 20, ground - 236, tx + 20, ground - 236, GOLD, 2.2))
    o.append(line(tx, ground - 256, tx, ground - 216, GOLD, 2.2))
    o.append(leader(tx + 26, ground - 162, 424, ground - 214, 432, ground - 218, "CHOKE VALVE"))
    o.append(label(tx - 62, ground - 272, "christmas tree"))

    # Flowline away to the manifold.
    o.append(path("M%d %d H%d" % (tx + 86, ground - 162, 470), stroke=STEEL, sw=4, opacity=0.7))
    o.append(path("M%d %d H%d" % (tx + 86, ground - 162, 470), stroke=GOLD_LIT, sw=2,
                  extra=' class="flow"'))

    # Well below ground.
    o.append(rect(tx - 22, ground, 44, H - ground, fill=NAVY, stroke=STEEL_LINE, sw=1.4))
    o.append(line(tx, ground, tx, H - 30, GOLD, 1.0, dash="4 8", opacity=0.55))

    # --- beam pumping unit ----------------------------------------------
    px = 646
    o.append(rect(px - 96, ground - 14, 210, 14, fill=NAVY_LIT, stroke=STEEL, sw=1.4))
    o.append(path("M%d %d L%d %d L%d %d Z"
                  % (px - 4, 214, px - 42, ground - 14, px + 34, ground - 14),
                  fill="none", stroke=STEEL, sw=3))
    o.append(rect(px - 108, 202, 190, 14, fill=STEEL_DIM, stroke=ICE, sw=1.4))
    o.append(path("M%d 202 a 40 40 0 0 0 -34 44 l 20 8 a 34 34 0 0 1 26 -36 z" % (px - 96),
                  fill=GOLD, opacity=0.9))
    o.append(circle(px - 4, 209, 8, fill=GOLD))

    # Gearbox, crank and counterweight - the crank turns.
    o.append(rect(px + 58, ground - 92, 62, 78, fill=NAVY_LIT, stroke=STEEL, sw=1.5, rx=3))
    crank = (circle(px + 89, ground - 54, 30, fill="none", stroke=GOLD, sw=2.6)
             + rect(px + 79, ground - 88, 20, 30, fill=GOLD, opacity=0.85))
    o.append('<g class="rot" style="transform-origin:%.1fpx %.1fpx">%s</g>'
             % (px + 89, ground - 54, crank))
    o.append(line(px + 82, 209, px + 89, ground - 54, STEEL, 3))
    o.append(label(px - 108, 186, "beam pumping unit"))

    # Polished rod, sucker rod string and downhole pump.
    o.append(line(px - 96, 246, px - 96, ground - 14, STEEL_LINE, 3))
    o.append(rect(px - 112, ground - 14, 32, 22, fill=NAVY_LIT, stroke=ICE, sw=1.4))
    o.append(line(px - 96, ground + 8, px - 96, H - 74, GOLD_LIT, 2.4, dash="14 10"))
    o.append(rect(px - 108, H - 74, 24, 46, fill=NAVY_LIT, stroke=GOLD, sw=1.6))
    o.append(leader(px - 108, H - 52, 470, H - 52, 380, H - 56, "ROD PUMP"))

    o.append(text(30, 566, "API 6A &middot; API 6D &middot; API 11B &middot; API 11E &middot; API RP 11S",
                  size=12, fill=STEEL_DIM, font=HEAD_FONT, spacing=2.2))
    return sheet("".join(o), "Surface Production &amp; Artificial Lift", "WF-CAT-03")


def cat_plant():
    """Site plant: generator set, switchgear, compressor, crane and torque tooling."""
    o = []

    # Generator set on its skid, with an exhaust stack.
    o.append(rect(70, 250, 210, 108, fill=NAVY_LIT, stroke=STEEL, sw=1.6, rx=4))
    o.append(rect(70, 358, 210, 14, fill=STEEL_DIM))
    for k in range(7):
        o.append(line(92 + k * 26, 262, 92 + k * 26, 346, STEEL_LINE, 1.4, opacity=0.6))
    o.append(rect(196, 262, 72, 84, fill=NAVY_MID, stroke=GOLD, sw=1.6, rx=3))
    o.append('<g class="rot" style="transform-origin:232px 304px">%s</g>'
             % circle(232, 304, 22, fill="none", stroke=GOLD, sw=2.2))
    o.append(path("M104 250 V196 h30", stroke=STEEL, sw=3.4))
    o.append(path("M134 196 q 18 -22 4 -40", stroke=STEEL_DIM, sw=2, opacity=0.7))
    o.append(label(70, 238, "generator set"))
    o.append(dim(70, 404, 280, "10-2,500 kVA"))

    # Switchgear / MCC cubicles.
    for k in range(3):
        x = 330 + k * 58
        o.append(rect(x, 250, 52, 122, fill=NAVY_LIT, stroke=STEEL, sw=1.5, rx=2))
        o.append(rect(x + 8, 262, 36, 20, fill=GOLD, opacity=0.75))
        for j in range(3):
            o.append(line(x + 10, 296 + j * 16, x + 42, 296 + j * 16, STEEL_LINE, 1.4))
        o.append(circle(x + 26, 352, 6, fill=GOLD_LIT, opacity=0.9))
    o.append(label(330, 238, "switchgear / MCC"))

    # Screw compressor package.
    o.append(rect(548, 268, 132, 104, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=4))
    o.append('<g class="rot" style="transform-origin:586px 314px">%s</g>'
             % circle(586, 314, 26, fill="none", stroke=GOLD, sw=2.4))
    o.append(circle(642, 314, 18, fill="none", stroke=STEEL, sw=2))
    o.append(path("M680 300 h56", stroke=STEEL, sw=4, opacity=0.7))
    o.append(path("M680 300 h56", stroke=GOLD_LIT, sw=2, extra=' class="flow"'))
    o.append(label(548, 256, "air compressor"))

    # Overhead crane on its runway beam.
    o.append(rect(70, 116, 700, 12, fill=STEEL_DIM))
    o.append(rect(70, 128, 700, 5, fill=GOLD, opacity=0.6))
    o.append(rect(430, 100, 96, 16, fill=NAVY_LIT, stroke=ICE, sw=1.5))
    o.append(line(478, 133, 478, 186, STEEL_LINE, 2))
    o.append(path("M466 186 h24 v18 h-24 z", fill=GOLD, opacity=0.85))
    o.append(label(70, 104, "overhead crane"))

    # Hydraulic torque wrench on a bolted flange.
    o.append(circle(752, 470, 58, fill="none", stroke=STEEL, sw=3))
    o.append(circle(752, 470, 30, fill=NAVY, stroke=STEEL_LINE, sw=1.6))
    for k in range(8):
        a = math.radians(k * 45)
        o.append(circle(752 + math.cos(a) * 44, 470 + math.sin(a) * 44, 6,
                        fill=GOLD, opacity=0.85))
    o.append(rect(700, 424, 46, 26, fill=GOLD, stroke=GOLD_LIT, sw=1.4, rx=3))
    o.append(path("M700 437 h-42", stroke=STEEL, sw=5))
    o.append(leader(716, 424, 640, 396, 452, 392, "HYDRAULIC TORQUE WRENCH"))

    o.append(text(30, 566, "IEC 60034 &middot; IEC 60076 &middot; ASME VIII &middot; ATEX / IECEx",
                  size=12, fill=STEEL_DIM, font=HEAD_FONT, spacing=2.2))
    return sheet("".join(o), "Plant, Machinery &amp; Industrial Tools", "WF-CAT-06")


CATEGORY_ART = [
    ("drilling-equipment-tools", cat_drilling),
    ("downhole-completion-octg", cat_downhole),
    ("surface-production-artificial-lift", cat_surface),
    ("fluids-solids-control-workover", cat_fluids),
    ("casting-forging-machining", cat_machinery),
    ("plant-machinery-industrial-tools", cat_plant),
]


def art_categories():
    for slug, fn in CATEGORY_ART:
        write("assets/img/art/cat-%s.svg" % slug, fn())


# ===========================================================================
#  3. Section diagrams
# ===========================================================================
def art_wellbore():
    """A cased well in section - the sourcing page's supporting diagram."""
    w, h = 420, 720
    cx = w / 2
    o = [rect(0, 0, w, h, fill="none")]

    strings = [
        (150, 90,  "CONDUCTOR", "30 in"),
        (118, 210, "SURFACE",   "20 in"),
        (86,  368, "INTERMEDIATE", "13 3/8 in"),
        (56,  520, "PRODUCTION", "9 5/8 in"),
    ]
    for i, (hw, depth, name, size) in enumerate(strings):
        for sx in (-1, 1):
            x = cx + sx * hw
            o.append(line(x, 70, x, depth, STEEL, 2.2, opacity=0.9 - i * 0.06))
            o.append(line(x + sx * 12, 70, x + sx * 12, depth, STEEL_LINE, 1.4, opacity=0.6))
            # Cement sheath.
            o.append(rect(min(x, x + sx * 12), 70, 12, depth - 70,
                          fill="url(#hatch)", opacity=0.7))
            o.append(path("M%.1f %.1f h%.1f" % (x, depth, sx * 12), stroke=GOLD, sw=2.4))
        o.append(text(cx + hw + 22, depth - 6, "%s · %s" % (name, size), size=11,
                      fill=GOLD if i == 3 else STEEL_DIM, font=HEAD_FONT, spacing=1.3))

    # Tubing, packer and perforated interval.
    o.append(rect(cx - 20, 70, 40, 560, fill=NAVY_LIT, stroke=STEEL, sw=1.5))
    o.append(path("M%d 560 C%d 566 %d 594 %d 600 L%d 600 C%d 594 %d 566 %d 560 Z"
                  % (cx - 20, cx - 54, cx - 54, cx - 20, cx + 20, cx + 54, cx + 54, cx + 20),
                  fill="#1B1F27", stroke=GOLD, sw=1.6))
    o.append(text(cx + 62, 586, "PRODUCTION PACKER", size=11, fill=GOLD,
                  font=HEAD_FONT, spacing=1.3))
    for k in range(6):
        y = 616 + k * 16
        for sx in (-1, 1):
            o.append(path("M%.1f %.1f l%.1f -6" % (cx + sx * 56, y, sx * 26),
                          stroke=RUST, sw=2.2))
    o.append(path("M%d 700 V90" % cx, stroke=GOLD_LIT, sw=3, extra=' class="flow"'))

    # Wellhead.
    o.append(rect(cx - 46, 40, 92, 30, fill=NAVY_LIT, stroke=ICE, sw=1.6, rx=2))
    o.append(rect(cx - 16, 16, 32, 24, fill=GOLD, opacity=0.9))
    o.append(text(cx, 12, "WELLHEAD", size=11, fill=ICE, anchor="middle",
                  font=HEAD_FONT, spacing=2))

    return svg(w, h, "".join(o), defs=hatch_def("hatch", STEEL_LINE, 6, 0.45), style=ANIM_STYLE,
               extra_attr=' role="img" aria-label="Cased well schematic"')


def art_process():
    """The five-step sourcing process as a flow line with a travelling pulse."""
    w, h = 1120, 240
    steps = [("01", "Requirement\nCapture"), ("02", "Global Vendor\nScreening"),
             ("03", "Technical\nEvaluation"), ("04", "QA/QC &amp;\nInspection"),
             ("05", "Logistics &amp;\nDelivery")]
    o = [rect(0, 0, w, h, fill="none")]
    y = 96
    x0, gap = 118, (w - 236) / 4.0

    o.append(line(x0, y, x0 + gap * 4, y, STEEL_LINE, 2.4, opacity=0.6))
    o.append(path("M%d %d H%d" % (x0, y, x0 + gap * 4), stroke=GOLD, sw=2.8,
                  extra=' class="flow"'))

    for i, (num, name) in enumerate(steps):
        cx = x0 + gap * i
        o.append(circle(cx, y, 30, fill=NAVY, stroke=GOLD if i == 0 else STEEL_DIM, sw=2))
        o.append(circle(cx, y, 30, fill="none", stroke=GOLD, sw=2, opacity=0.9))
        o.append(text(cx, y + 7, num, size=19, fill=GOLD_LIT, anchor="middle",
                      font=HEAD_FONT, weight="600", spacing=1))
        for j, ln in enumerate(name.split("\n")):
            o.append(text(cx, y + 60 + j * 20, ln, size=14, fill=ICE, anchor="middle",
                          font=HEAD_FONT, weight="500", spacing=1.1))
        o.append(circle(cx, y - 52, 4, fill=GOLD, opacity=0.5))
        o.append(line(cx, y - 46, cx, y - 32, STEEL_LINE, 1, opacity=0.5))
    return svg(w, h, "".join(o), style=ANIM_STYLE,
               extra_attr=' role="img" aria-label="Five step sourcing process"')


def art_compliance_seal():
    """A rosette of standard designations - used behind the compliance section."""
    r, n = 300, 3
    o = []
    rings = [
        (250, ["API 5CT", "API 5L", "API 6A", "API 7-1", "API 11D1", "ASME B16.5"], GOLD),
        (190, ["ISO 11960", "ISO 14310", "ISO 3183", "ISO 9001"], STEEL),
        (130, ["NACE MR0175", "EN 10204 3.1", "ISO 15156"], STEEL_DIM),
    ]
    o.append(circle(r, r, 288, fill="none", stroke=GOLD, sw=1.2, opacity=0.35))
    for radius, items, colour in rings:
        o.append(circle(r, r, radius, fill="none", stroke=colour, sw=1, opacity=0.28))
        for i, s in enumerate(items):
            a = math.radians(i * 360.0 / len(items) - 90)
            x, y = r + math.cos(a) * radius, r + math.sin(a) * radius
            o.append(circle(x, y, 4, fill=colour, opacity=0.9))
            o.append(text(x, y - 12, s, size=12, fill=colour, anchor="middle",
                          font=HEAD_FONT, weight="500", spacing=1.4, opacity=0.95))
    o.append(circle(r, r, 62, fill=NAVY, stroke=GOLD, sw=1.6))
    o.append(text(r, r - 4, "API", size=26, fill=GOLD_LIT, anchor="middle",
                  font=HEAD_FONT, weight="700", spacing=2))
    o.append(text(r, r + 20, "ISO", size=17, fill=STEEL, anchor="middle",
                  font=HEAD_FONT, weight="600", spacing=3))
    del n
    return svg(600, 600, "".join(o), extra_attr=' role="img" aria-label="Standards we supply against"')


def art_section():
    write("assets/img/art/wellbore.svg", art_wellbore())
    write("assets/img/art/process-flow.svg", art_process())
    write("assets/img/art/standards-rosette.svg", art_compliance_seal())


# ===========================================================================
#  4. Article covers
# ===========================================================================
BLOG_MOTIF = {}


def motif_pipes(seed):
    """Stacked tubular sections receding into the distance."""
    o = []
    for i in range(5):
        cx = 900 + i * 6
        ry = 150 - i * 22
        o.append(ellipse(cx, 338, ry * 1.0, ry, fill="none", stroke=GOLD,
                         sw=3 - i * 0.35, opacity=0.85 - i * 0.13))
    o.append(ellipse(900, 338, 52, 52, fill=GOLD, opacity=0.30))
    for i in range(6):
        o.append(line(660, 150 + i * 74, 790, 150 + i * 74, GOLD, 3, opacity=0.55 - i * 0.06))
    del seed
    return "".join(o)


def motif_certificate(seed):
    """A stamped document with a compliance tick."""
    o = [rect(760, 140, 290, 380, fill="none", stroke=GOLD, sw=3, opacity=0.85, rx=6)]
    for i in range(7):
        o.append(line(796, 210 + i * 40, 1014 - (i % 3) * 46, 210 + i * 40, GOLD, 6,
                      opacity=0.30 if i % 2 else 0.45))
    o.append(circle(1030, 470, 62, fill="none", stroke=GOLD, sw=4, opacity=0.9))
    o.append(path("M1002 470 l20 22 l38 -46", stroke=GOLD, sw=8, opacity=0.95))
    del seed
    return "".join(o)


def motif_network(seed):
    """A sourcing network - nodes and routes."""
    pts = [(760, 200), (990, 150), (1090, 330), (900, 430), (700, 380), (960, 290)]
    o = []
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 330:
                o.append(line(a[0], a[1], b[0], b[1], GOLD, 2, opacity=0.35))
    for i, p in enumerate(pts):
        r = 20 if i == 5 else 12
        o.append(circle(p[0], p[1], r, fill=GOLD, opacity=0.85 if i == 5 else 0.55))
        o.append(circle(p[0], p[1], r + 12, fill="none", stroke=GOLD, sw=2, opacity=0.35))
    del seed
    return "".join(o)


def motif_gauge(seed):
    """Pressure / temperature gauge - the HPHT article."""
    o = [circle(920, 330, 150, fill="none", stroke=GOLD, sw=4, opacity=0.85),
         circle(920, 330, 118, fill="none", stroke=GOLD, sw=1.6, opacity=0.4)]
    for i in range(28):
        a = math.radians(-210 + i * (240.0 / 27))
        r0, r1 = (118, 148) if i % 4 == 0 else (132, 148)
        o.append(line(920 + math.cos(a) * r0, 330 + math.sin(a) * r0,
                      920 + math.cos(a) * r1, 330 + math.sin(a) * r1,
                      GOLD, 3 if i % 4 == 0 else 1.6, opacity=0.8))
    a = math.radians(-38)
    o.append(line(920, 330, 920 + math.cos(a) * 116, 330 + math.sin(a) * 116, GOLD, 6))
    o.append(circle(920, 330, 16, fill=GOLD, opacity=0.9))
    del seed
    return "".join(o)


def motif_clock(seed):
    """Lead time - a clock face collapsing into a progress bar."""
    o = [circle(900, 280, 128, fill="none", stroke=GOLD, sw=4, opacity=0.85)]
    o.append(line(900, 280, 900, 190, GOLD, 6))
    o.append(line(900, 280, 962, 306, GOLD, 6))
    for i in range(12):
        a = math.radians(i * 30 - 90)
        o.append(circle(900 + math.cos(a) * 106, 280 + math.sin(a) * 106, 4, fill=GOLD,
                        opacity=0.7))
    for i in range(4):
        o.append(rect(720 + i * 6, 452 + i * 26, 360 - i * 78, 14, fill=GOLD,
                      opacity=0.65 - i * 0.14, rx=7))
    del seed
    return "".join(o)


def motif_growth(seed):
    """Make-in-India / market growth - an ascending column chart with a rig."""
    o = []
    for i in range(5):
        h = 70 + i * 62
        o.append(rect(714 + i * 74, 470 - h, 48, h, fill=GOLD, opacity=0.28 + i * 0.14, rx=3))
    o.append(path("M700 452 L790 372 L864 400 L938 288 L1024 210", stroke=GOLD, sw=4,
                  opacity=0.95))
    for x, y in ((790, 372), (864, 400), (938, 288), (1024, 210)):
        o.append(circle(x, y, 8, fill=GOLD))
    del seed
    return "".join(o)


COVER_MOTIFS = [motif_certificate, motif_pipes, motif_gauge, motif_growth,
                motif_clock, motif_network]

# ---------------------------------------------------------------------------
#  The real logo, embedded rather than redrawn
# ---------------------------------------------------------------------------
_LOGO_CACHE = {}


def logo_data_uri(filename="logo-full-light.png"):
    """Base64 data URI for a logo file.

    An SVG loaded through <img src="..."> runs in a restricted mode where
    browsers refuse to fetch external resources, so a relative <image href>
    would silently render nothing. Embedding the bytes is what makes the real
    artwork show up inside a cover.
    """
    if filename not in _LOGO_CACHE:
        import base64
        path = os.path.join(ROOT, "assets", "img", filename)
        with open(path, "rb") as fh:
            _LOGO_CACHE[filename] = ("data:image/png;base64,"
                                     + base64.b64encode(fh.read()).decode("ascii"))
    return _LOGO_CACHE[filename]


def logo_lockup(x, y, width, filename="logo-full-light.png", opacity=1.0):
    """Place approved logo artwork at its true aspect ratio.

    Pass logo-mark-light.png for the WF monogram alone, or the default
    logo-full-light.png for the monogram plus the wordmark.
    """
    from PIL import Image
    path = os.path.join(ROOT, "assets", "img", filename)
    iw, ih = Image.open(path).size
    height = width * ih / float(iw)
    return ('<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" href="%s" '
            'opacity="%.2f" preserveAspectRatio="xMidYMid meet"/>'
            % (x, y, width, height, logo_data_uri(filename), opacity))


def blog_cover(index, category_label, title_words):
    w, h = 1200, 675
    motif = COVER_MOTIFS[index % len(COVER_MOTIFS)]
    defs = (lgrad("bg", [("0%", "#132247", "1"), ("55%", NAVY, "1"), ("100%", INK, "1")],
                  x2="100%", y2="100%")
            + grid_def("g", 48, "#FFFFFF", 0.045)
            + rgrad("gl", [("0%", GOLD, "0.24"), ("100%", GOLD, "0")], cx="72%", cy="48%", r="55%"))

    o = [rect(0, 0, w, h, fill="url(#bg)"), rect(0, 0, w, h, fill="url(#g)"),
         rect(0, 0, w, h, fill="url(#gl)")]
    o.append(motif(index))

    # Left rule and category strap.
    o.append(rect(0, 0, 12, h, fill=GOLD))
    o.append(text(70, 108, upper_safe(category_label), size=27, fill=GOLD, font=HEAD_FONT,
                  weight="600", spacing=6))
    o.append(line(70, 132, 300, 132, GOLD, 2, opacity=0.6))

    # Article title, wrapped by the caller into short lines.
    for i, ln in enumerate(title_words):
        o.append(text(70, 224 + i * 56, ln, size=45, fill=ICE, font=HEAD_FONT,
                      weight="500", spacing=0.6))

    # The WF monogram on its own - the covers are read small, and the wordmark
    # is illegible at card size.
    o.append(logo_lockup(70, 524, 132, filename="logo-mark-light.png"))
    return svg(w, h, "".join(o), defs=defs,
               extra_attr=' role="img" aria-label="%s"' % category_label)


def art_blog_covers():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from content_blog import POSTS, CATEGORY_LABEL

    # Short display lines per article, so the cover typography stays legible.
    LINES = {
        "api-5ct-casing-and-tubing-grades-buyers-guide":
            ["Understanding API 5CT", "Casing &amp; Tubing Grades", "A Buyer&#8217;s Guide"],
        "reduce-oilfield-equipment-lead-times":
            ["Five Ways to Reduce", "Oilfield Equipment", "Lead Times"],
        "hpht-well-completions-sourcing-guide":
            ["HPHT Well Completions", "What to Specify", "Before You Buy"],
        "make-in-india-oilfield-sector-opportunities":
            ["Make in India", "and the Opportunity in", "the Oilfield Sector"],
        "signs-you-need-a-strategic-sourcing-partner":
            ["Signs You Need a", "Strategic Sourcing", "Partner"],
        "api-vs-iso-oilfield-compliance-standards":
            ["API vs ISO", "Oilfield Compliance", "Standards Compared"],
    }
    for i, post in enumerate(POSTS):
        cat = CATEGORY_LABEL[post["cat"]].replace("&amp;", "&amp;")
        lines = LINES.get(post["slug"], [post["slug"].replace("-", " ").title()])
        write("assets/img/blog/%s.svg" % post["slug"], blog_cover(i, cat, lines))


# ===========================================================================
#  5. Social share card (PNG - Open Graph will not render SVG)
# ===========================================================================
def art_og_image():
    from PIL import Image, ImageDraw

    W_, H_ = 1200, 630
    img = Image.new("RGB", (W_, H_), (7, 12, 22))
    d = ImageDraw.Draw(img, "RGBA")

    # Diagonal navy wash.
    for y in range(H_):
        t = y / float(H_)
        d.line([(0, y), (W_, y)],
               fill=(int(19 + 5 * (1 - t)), int(34 + 10 * (1 - t)), int(71 - 18 * t)))

    # Technical grid.
    for x in range(0, W_, 48):
        d.line([(x, 0), (x, H_)], fill=(255, 255, 255, 12))
    for y in range(0, H_, 48):
        d.line([(0, y), (W_, y)], fill=(255, 255, 255, 12))

    # Gold glow behind the artwork side.
    for r in range(340, 0, -12):
        a = int(26 * (1 - r / 340.0))
        d.ellipse([880 - r, 300 - r, 880 + r, 300 + r], fill=(217, 162, 43, a))

    # Derrick silhouette, drawn from the same geometry as the 3D hero.
    base_y, top_y, cx = 540, 120, 880
    hw_b, hw_t = 150, 42
    def leg(t):
        return hw_b + (hw_t - hw_b) * t
    for sx in (-1, 1):
        d.line([(cx + sx * hw_b, base_y), (cx + sx * hw_t, top_y)], fill=(217, 162, 43, 220), width=5)
    for i in range(9):
        t0, t1 = i / 9.0, (i + 1) / 9.0
        y0, y1 = base_y + (top_y - base_y) * t0, base_y + (top_y - base_y) * t1
        d.line([(cx - leg(t0), y0), (cx + leg(t0), y0)], fill=(143, 161, 188, 150), width=3)
        if i % 2 == 0:
            d.line([(cx - leg(t0), y0), (cx + leg(t1), y1)], fill=(143, 161, 188, 110), width=2)
        else:
            d.line([(cx + leg(t0), y0), (cx - leg(t1), y1)], fill=(143, 161, 188, 110), width=2)
    d.line([(cx - leg(1.0) - 14, top_y), (cx + leg(1.0) + 14, top_y)],
           fill=(242, 200, 92, 255), width=7)
    d.line([(cx, top_y), (cx, base_y + 40)], fill=(199, 208, 218, 200), width=6)
    d.rectangle([cx - 190, base_y, cx + 190, base_y + 16], fill=(217, 162, 43, 235))

    # Gold rule down the left edge.
    d.rectangle([0, 0, 12, H_], fill=(217, 162, 43))

    # The real logo lockup, composited in.
    logo_path = os.path.join(ROOT, "assets", "img", "logo-full-light.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        target_w = 430
        logo = logo.resize((target_w, max(1, int(logo.height * target_w / float(logo.width)))),
                           Image.LANCZOS)
        img.paste(logo, (70, 132), logo)

    # Headline and strap, rendered as vector-ish bars when no font is available.
    try:
        from PIL import ImageFont
        font_big = ImageFont.truetype("arialbd.ttf", 52)
        font_mid = ImageFont.truetype("arial.ttf", 25)
        font_sm = ImageFont.truetype("arialbd.ttf", 19)
    except Exception:
        font_big = font_mid = font_sm = None

    if font_big:
        d.text((70, 300), "Forged for the Field.", font=font_big, fill=(238, 243, 250))
        d.text((70, 362), "Built to Perform.", font=font_big, fill=(217, 162, 43))
        d.text((70, 442), "Oil & gas equipment sourcing, engineering", font=font_mid,
               fill=(155, 168, 190))
        d.text((70, 476), "and supply chain solutions.", font=font_mid, fill=(155, 168, 190))
        d.text((70, 545), "API & ISO COMPLIANT  ·  GURUGRAM, INDIA", font=font_sm,
               fill=(217, 162, 43))

    img.save(os.path.join(ROOT, "assets", "img", "og-image.png"), optimize=True)
    print("  wrote assets/img/og-image.png")


# ===========================================================================
def main():
    print("Generating Wellforge artwork...")
    art_textures()
    art_categories()
    art_section()
    art_blog_covers()
    art_og_image()
    print("Done.")


if __name__ == "__main__":
    main()
