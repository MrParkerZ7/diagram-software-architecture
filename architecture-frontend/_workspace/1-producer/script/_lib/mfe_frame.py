# -*- coding: utf-8 -*-
"""The shared micro-frontend frame: one page layout for the seven micro-frontend diagrams.

Contract (current truth, read it first): ../../analysis/micro-frontend-frame.md
A shared helper under _lib/, never a builder and never run on its own. A slot's builder imports it and calls
build_page() with data only: title words, statements, node states and subtitles, cables, companions. This module owns
every coordinate, style, class marker, port, waypoint, label wrap and label slide, and checks its own output before it
writes (the 20-px grid, the class markers and shadow keys, label clearance, cables clear of container titles).

Environment (never written into a committed file): DIAGRAM_KIT = the prompt master's shared/prompts/3-diagram folder.
"""
import html
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

KIT = os.environ.get("DIAGRAM_KIT", "")
if not KIT or not os.path.isfile(os.path.join(KIT, "text", "gen_text.py")):
    raise SystemExit("DIAGRAM_KIT must point to the prompt master's shared/prompts/3-diagram")
sys.path.insert(0, os.path.join(KIT, "text"))
import gen_text  # noqa: E402  (loads ../icons/gen_icons itself)

GRID = 20
PAGE_W, PAGE_H = 3060, 1680

# ----------------------------------------------------------------------------------------------------- containers
# id: (title, parent, absolute x, y, w, h, role); role: column | group | legend.  All swimlane;startSize=0.
CONTAINERS = {
    "C-BROWSER": ("Browser (one page at run time)", "1", 40, 320, 800, 720, "column"),
    "G-REMOTES": ("Team UIs (micro-frontends)", "C-BROWSER", 60, 680, 760, 160, "group"),
    "C-EDGE": ("Edge (CDN and proxy)", "1", 1120, 320, 340, 720, "column"),
    "C-ORIGIN": ("Origin (servers)", "1", 1660, 320, 700, 720, "column"),
    "G-SERVERS": ("Team servers", "C-ORIGIN", 1680, 680, 660, 160, "group"),
    "C-BACKEND": ("Backend (APIs and content)", "1", 2560, 320, 340, 720, "column"),
    "G-APIS": ("Team APIs", "C-BACKEND", 2580, 360, 300, 400, "group"),
    "C-BUILD": ("Build time (before any request)", "1", 1120, 1140, 1240, 360, "column"),
    "G-CI": ("Team pipelines", "C-BUILD", 1680, 1180, 660, 160, "group"),
    "C-LEGEND": ("Legend", "1", 40, 1140, 800, 400, "legend"),
}
GROUPS = ("G-REMOTES", "G-SERVERS", "G-APIS", "G-CI")
COLUMN_FILL, COLUMN_STROKE = "#FFFFFF", "#5F6B7A"
GROUP_FILL, GROUP_STROKE = "#F4F6F9", "#8A97A8"
TITLE_FONT = "#37474F"

# ------------------------------------------------------------------------------------------------------- nodes
# id: (NAME, CLAY_DEMO icon key, parent, absolute x, y, w, h, team: a | b | c | None = platform)
NODES = {
    "B-PAGE": ("Browser tab", "client-browser", "C-BROWSER", 220, 360, 420, 80, None),
    "B-ROUTER": ("Client router", "page-route", "C-BROWSER", 80, 520, 180, 80, None),
    "B-SHELL": ("App shell", "webapp", "C-BROWSER", 600, 520, 180, 80, None),
    "B-UI-A": ("Team A · Catalog UI", "ui-component", "G-REMOTES", 100, 720, 180, 80, "a"),
    "B-UI-B": ("Team B · Cart UI", "ui-component", "G-REMOTES", 340, 720, 180, 80, "b"),
    "B-UI-C": ("Team C · Account UI", "ui-component", "G-REMOTES", 580, 720, 180, 80, "c"),
    "B-BUS": ("Event bus", "event-stream", "C-BROWSER", 80, 920, 400, 80, None),
    "B-SHARED": ("Shared libraries", "module-package", "C-BROWSER", 520, 920, 280, 80, None),
    "E-ROUTER": ("Edge router", "load-balancer", "C-EDGE", 1160, 360, 260, 80, None),
    "E-CACHE": ("Page cache", "cache", "C-EDGE", 1160, 520, 260, 80, None),
    "E-CDN": ("CDN", "cdn", "C-EDGE", 1160, 920, 260, 80, None),
    "O-COMPOSER": ("Page composer", "service", "C-ORIGIN", 1700, 360, 340, 80, None),
    "O-BFF": ("BFF", "api-gateway", "C-ORIGIN", 1920, 520, 400, 80, None),
    "O-SRV-A": ("Team A server", "service", "G-SERVERS", 1700, 720, 180, 80, "a"),
    "O-SRV-B": ("Team B server", "service", "G-SERVERS", 1920, 720, 180, 80, "b"),
    "O-SRV-C": ("Team C server", "service", "G-SERVERS", 2140, 720, 180, 80, "c"),
    "K-API-A": ("Catalog API (team A)", "microservice", "G-APIS", 2600, 400, 260, 80, "a"),
    "K-API-B": ("Order API (team B)", "microservice", "G-APIS", 2600, 520, 260, 80, "b"),
    "K-API-C": ("Account API (team C)", "microservice", "G-APIS", 2600, 640, 260, 80, "c"),
    "K-CMS": ("Headless CMS", "docs-multi", "C-BACKEND", 2600, 920, 260, 80, None),
    "D-REGISTRY": ("Registry", "registry", "C-BUILD", 1160, 1220, 220, 80, None),
    "D-INTEGRATION": ("Integration build", "ci-pipeline", "C-BUILD", 1320, 1380, 260, 80, None),
    "D-CI-A": ("Team A pipeline", "ci-pipeline", "G-CI", 1700, 1220, 180, 80, "a"),
    "D-CI-B": ("Team B pipeline", "ci-pipeline", "G-CI", 1920, 1220, 180, 80, "b"),
    "D-CI-C": ("Team C pipeline", "ci-pipeline", "G-CI", 2140, 1220, 180, 80, "c"),
}
# Cell order (z): each container, then its children, depth first; legend last in the container block.
ORDER = ["C-BROWSER", "B-PAGE", "B-ROUTER", "B-SHELL", "G-REMOTES", "B-UI-A", "B-UI-B", "B-UI-C", "B-BUS", "B-SHARED",
         "C-EDGE", "E-ROUTER", "E-CACHE", "E-CDN",
         "C-ORIGIN", "O-COMPOSER", "O-BFF", "G-SERVERS", "O-SRV-A", "O-SRV-B", "O-SRV-C",
         "C-BACKEND", "G-APIS", "K-API-A", "K-API-B", "K-API-C", "K-CMS",
         "C-BUILD", "D-REGISTRY", "D-INTEGRATION", "G-CI", "D-CI-A", "D-CI-B", "D-CI-C"]

# ------------------------------------------------------------------------------------------------ colour classes
# class: (kit kind, fill, style keys that replace the kit's shadow=1)
CLASSES = {
    "team-a": ("info", "#DAE8FC", "shadow=0;"),
    "team-b": ("success", "#D5E8D4", "shadow=0;"),
    "team-c": ("accent", "#E1D5E7", "shadow=0;"),
    "platform": ("neutral", "#CFD8DC", "shadow=0;"),
    "pivot": ("note", "#FFF2CC", "shadow=1;"),
    "muted": ("neutral", "#F5F5F5", "shadow=0;opacity=45;textOpacity=60;opacityGroup=1;"),
}
MUTED_GROUP = "strokeColor=#BDBDBD;fontColor=#9E9E9E;opacity=45;"

# ------------------------------------------------------------------------------------------------- edge classes
EDGE_CLASSES = {
    "net": "strokeColor=#232F3E;strokeWidth=2;endArrow=block;endFill=1;",
    "page": "strokeColor=#232F3E;strokeWidth=2;dashed=1;dashPattern=1 3;endArrow=open;endFill=0;",
    "build": "strokeColor=#616161;strokeWidth=2;dashed=1;dashPattern=6 4;endArrow=block;endFill=1;",
}
LABEL_STYLE = "fontSize=11;fontColor=#232F3E;labelBackgroundColor=#FFFFFF;"
DEFAULT_WRAP = 24
CHAR_W, LINE_H = 6.0, 13.2            # label estimate at font 11 (a little wider than drawn, on purpose)

# --------------------------------------------------------------------------------------------------- routing
# (from, to): (start point on the source's wall, [waypoints], end point on the target's wall), absolute px.
# Every segment is axis-aligned; every bend sits in free space (a street, a gutter, the east lane, or the free space
# west, south and east of the build band). See the contract's Routing table and Paper check.
ROUTES = {
    ("B-PAGE", "E-ROUTER"): ((640, 380), [], (1160, 380)),
    ("B-PAGE", "E-CDN"): ((640, 420), [(980, 420), (980, 940)], (1160, 940)),
    ("B-PAGE", "B-SHELL"): ((620, 440), [], (620, 520)),
    ("B-PAGE", "B-ROUTER"): ((240, 440), [], (240, 520)),
    ("B-PAGE", "G-REMOTES"): ((580, 440), [], (580, 680)),
    ("B-SHELL", "G-REMOTES"): ((700, 600), [], (700, 680)),
    ("B-ROUTER", "G-REMOTES"): ((160, 600), [], (160, 680)),
    ("B-SHELL", "B-ROUTER"): ((600, 560), [], (260, 560)),
    ("G-REMOTES", "B-BUS"): ((280, 840), [], (280, 920)),
    ("E-ROUTER", "O-BFF"): ((1420, 420), [(1560, 420), (1560, 560)], (1920, 560)),
    ("E-ROUTER", "G-SERVERS"): ((1420, 420), [(1560, 420), (1560, 760)], (1680, 760)),
    ("E-ROUTER", "O-COMPOSER"): ((1420, 400), [], (1700, 400)),
    ("E-ROUTER", "E-CACHE"): ((1280, 440), [], (1280, 520)),
    ("E-CACHE", "O-COMPOSER"): ((1420, 540), [(1560, 540), (1560, 380)], (1700, 380)),
    ("O-BFF", "G-APIS"): ((2320, 560), [], (2580, 560)),
    ("O-BFF", "K-API-B"): ((2320, 560), [], (2600, 560)),
    ("O-COMPOSER", "O-BFF"): ((1980, 440), [], (1980, 520)),
    ("O-COMPOSER", "G-SERVERS"): ((1780, 440), [], (1780, 680)),
    ("G-SERVERS", "O-BFF"): ((2180, 680), [], (2180, 600)),
    ("K-CMS", "O-COMPOSER"): ((2860, 960), [(2960, 960), (2960, 260), (1840, 260)], (1840, 360)),
    ("G-CI", "E-CDN"): ((1680, 1320), [(1080, 1320), (1080, 980)], (1160, 980)),
    ("G-CI", "D-REGISTRY"): ((1680, 1260), [], (1380, 1260)),
    ("D-REGISTRY", "E-CDN"): ((1280, 1220), [], (1280, 1000)),
    ("G-CI", "G-SERVERS"): ((2240, 1180), [], (2240, 840)),
    ("D-REGISTRY", "D-INTEGRATION"): ((1360, 1300), [], (1360, 1380)),
    ("D-INTEGRATION", "K-CMS"): ((1580, 1400), [(2720, 1400)], (2720, 1000)),
    ("D-INTEGRATION", "K-API-A"): ((1580, 1440), [(2960, 1440), (2960, 440)], (2860, 440)),
    ("D-INTEGRATION", "E-CDN"): ((1320, 1420), [(1080, 1420), (1080, 980)], (1160, 980)),
    ("D-INTEGRATION", "E-CACHE"): ((1520, 1380), [(1520, 580)], (1420, 580)),
    ("D-INTEGRATION", "O-COMPOSER"): ((1580, 1420), [(2960, 1420), (2960, 260), (1840, 260)], (1840, 360)),
}

# (abbr, from, to): (wrap, (label centre x, y)) - the centre lies on the route; the frame turns it into the edge
# geometry x (the label slide). Found by the dry run (every label clear of cards, walls, titles and cables) and frozen.
LABELS = {
    # LABELS-BEGIN (written by the dry run; do not edit by hand)
    ("CSR", "B-PAGE", "B-SHELL"): (24, (620, 480)),
    ("CSR", "B-PAGE", "E-CDN"): (30, (980, 680)),
    ("CSR", "B-PAGE", "E-ROUTER"): (24, (980, 380)),
    ("CSR", "B-SHELL", "G-REMOTES"): (24, (700, 640)),
    ("CSR", "D-REGISTRY", "E-CDN"): (24, (1280, 1090)),
    ("CSR", "E-ROUTER", "O-BFF"): (26, (1800, 560)),
    ("CSR", "G-CI", "D-REGISTRY"): (26, (1520, 1260)),
    ("CSR", "G-CI", "E-CDN"): (24, (1530, 1320)),
    ("CSR", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("SPA", "B-PAGE", "B-ROUTER"): (28, (240, 480)),
    ("SPA", "B-PAGE", "E-CDN"): (24, (980, 680)),
    ("SPA", "B-PAGE", "E-ROUTER"): (24, (980, 380)),
    ("SPA", "B-ROUTER", "G-REMOTES"): (24, (160, 640)),
    ("SPA", "B-SHELL", "B-ROUTER"): (24, (430, 560)),
    ("SPA", "D-REGISTRY", "E-CDN"): (24, (1280, 1090)),
    ("SPA", "E-ROUTER", "O-BFF"): (26, (1800, 560)),
    ("SPA", "G-CI", "D-REGISTRY"): (26, (1520, 1260)),
    ("SPA", "G-CI", "E-CDN"): (24, (1530, 1320)),
    ("SPA", "G-REMOTES", "B-BUS"): (24, (280, 880)),
    ("SPA", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("MPA", "B-PAGE", "E-CDN"): (30, (980, 690)),
    ("MPA", "B-PAGE", "E-ROUTER"): (34, (980, 380)),
    ("MPA", "E-ROUTER", "G-SERVERS"): (24, (1560, 590)),
    ("MPA", "G-CI", "E-CDN"): (24, (1530, 1320)),
    ("MPA", "G-CI", "G-SERVERS"): (24, (2240, 940)),
    ("MPA", "G-SERVERS", "O-BFF"): (24, (2180, 640)),
    ("MPA", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("SSR", "B-PAGE", "E-CDN"): (26, (980, 680)),
    ("SSR", "B-PAGE", "E-ROUTER"): (24, (980, 380)),
    ("SSR", "B-PAGE", "G-REMOTES"): (24, (580, 480)),
    ("SSR", "E-ROUTER", "O-COMPOSER"): (24, (1560, 400)),
    ("SSR", "G-CI", "E-CDN"): (26, (1530, 1320)),
    ("SSR", "G-CI", "G-SERVERS"): (24, (2240, 940)),
    ("SSR", "G-SERVERS", "O-BFF"): (24, (2180, 640)),
    ("SSR", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("SSR", "O-COMPOSER", "G-SERVERS"): (30, (1780, 560)),
    ("SSG", "B-PAGE", "E-CDN"): (24, (980, 680)),
    ("SSG", "B-PAGE", "E-ROUTER"): (28, (980, 380)),
    ("SSG", "B-PAGE", "G-REMOTES"): (28, (580, 480)),
    ("SSG", "D-INTEGRATION", "E-CDN"): (24, (1230, 1420)),
    ("SSG", "D-INTEGRATION", "K-API-A"): (24, (2960, 1250)),
    ("SSG", "D-INTEGRATION", "K-CMS"): (24, (2720, 1230)),
    ("SSG", "D-REGISTRY", "D-INTEGRATION"): (24, (1360, 1340)),
    ("SSG", "E-ROUTER", "O-BFF"): (26, (1800, 560)),
    ("SSG", "G-CI", "D-REGISTRY"): (24, (1520, 1260)),
    ("SSG", "O-BFF", "K-API-B"): (24, (2460, 560)),
    ("ISR", "B-PAGE", "E-CDN"): (26, (980, 680)),
    ("ISR", "B-PAGE", "E-ROUTER"): (24, (980, 380)),
    ("ISR", "D-INTEGRATION", "E-CACHE"): (26, (1520, 1280)),
    ("ISR", "E-CACHE", "O-COMPOSER"): (30, (1560, 460)),
    ("ISR", "E-ROUTER", "E-CACHE"): (24, (1280, 480)),
    ("ISR", "G-CI", "G-SERVERS"): (30, (2240, 940)),
    ("ISR", "G-SERVERS", "O-BFF"): (24, (2180, 630)),
    ("ISR", "K-CMS", "O-COMPOSER"): (28, (2400, 260)),
    ("ISR", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("ISR", "O-COMPOSER", "G-SERVERS"): (26, (1780, 550)),
    ("RSC", "B-PAGE", "E-CDN"): (24, (980, 680)),
    ("RSC", "B-PAGE", "E-ROUTER"): (28, (980, 380)),
    ("RSC", "B-PAGE", "G-REMOTES"): (32, (580, 480)),
    ("RSC", "D-INTEGRATION", "O-COMPOSER"): (24, (1960, 1420)),
    ("RSC", "D-REGISTRY", "D-INTEGRATION"): (24, (1360, 1340)),
    ("RSC", "E-ROUTER", "O-COMPOSER"): (24, (1560, 400)),
    ("RSC", "G-CI", "D-REGISTRY"): (24, (1520, 1260)),
    ("RSC", "O-BFF", "G-APIS"): (24, (2460, 560)),
    ("RSC", "O-COMPOSER", "O-BFF"): (24, (1980, 480)),
    # LABELS-END
}

# ------------------------------------------------------------------------------------------------- furniture
TITLE_PREFIX = "Micro-frontends with"
STATEMENT_HEADINGS = ("Where the HTML is produced", "Where and when the micro-frontends are composed",
                      "Trade-off for micro-frontends")
STATEMENT_BOXES = ((40, 100, 940, 120), (1060, 100, 940, 120), (2080, 100, 940, 120))
STATEMENT_CHARS, STATEMENT_LINES = 130, 5          # capacity: the heading plus 5 lines of about 130 characters
TITLE_BOX = (40, 20, 2980, 60)
COMPANIONS_BOX = (40, 1580, 2980, 60)
COMPANIONS_HEADING = "Companions (same frame):"
LEGEND_BADGES = (("team-a", "Team A · Catalog"), ("team-b", "Team B · Cart and orders"), ("team-c", "Team C · Account"),
                 ("platform", "Shared or platform-owned"), ("pivot", "Where the micro-frontends are composed (the pivot)"),
                 ("muted", "Not used in this approach"))
LEGEND_SAMPLES = (("net", "Network request at run time: the arrow is the request, the label says what comes back"),
                  ("page", "Call inside the page (no network)"),
                  ("build", "Build or deploy, before any request"))
LEGEND_LINES = (
    "Numbers = the order of the steps of the flow drawn; numbered dashed steps are build steps and come before any "
    "request; an unnumbered cable stands outside that order (a build or deploy link, a standing link, or a separate "
    "trigger) · yellow = where the micro-frontends are composed",
    "BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), "
    "drawn where this example uses them; the headless CMS is a data source, not a BFF.")
MUTED_DEFAULT = "not used in %s"
ROW = ("text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=11;"
       "fontColor=#37474F;kitExempt=1;")


# =================================================================================================== helpers
def _esc(s):
    return html.escape(str(s), quote=False)


def _style_add(cell_xml, extra):
    """Append style keys to the first style attribute of one cell."""
    return re.sub(r'style="([^"]*)"', lambda m: 'style="%s%s"' % (m.group(1), extra), cell_xml, count=1)


def _reparent(cell_xml, parent):
    assert cell_xml.count('parent="1"') == 1, "cannot re-parent: %s" % cell_xml[:80]
    return cell_xml.replace('parent="1"', 'parent="%s"' % parent)


def abs_rect(cid):
    if cid in NODES:
        n = NODES[cid]
        return (n[3], n[4], n[5], n[6])
    c = CONTAINERS[cid]
    return (c[2], c[3], c[4], c[5])


def _parent_of(cid):
    return NODES[cid][2] if cid in NODES else CONTAINERS[cid][1]


def _rel(cid, x, y):
    p = _parent_of(cid)
    if p == "1":
        return x, y
    px, py, _, _ = abs_rect(p)
    return x - px, y - py


def wrap_label(text, wrap):
    """`\n` forces a break; each forced line is word-wrapped at `wrap` characters. -> list of lines."""
    out = []
    for part in str(text).split("\n"):
        words, units, i = part.split(" "), [], 0
        while i < len(words):                          # a step number never parts from its "·"
            w = words[i]
            if i + 1 < len(words) and words[i + 1] == "·":
                w += " ·"
                i += 1
            units.append(w)
            i += 1
        line = ""
        for word in units:
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= wrap:
                line += " " + word
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def label_box(lines, cx, cy):
    w = max(len(s) for s in lines) * CHAR_W + 6
    h = len(lines) * LINE_H + 4
    return (cx - w / 2.0, cy - h / 2.0, w, h)


def title_box(cid):
    """The swimlane title, centred on the top wall (bold 14: about 8.2 px a character, 12 px above and below)."""
    x, y, w, _ = abs_rect(cid)
    tw = len(CONTAINERS[cid][0]) * 8.2 + 16
    return (x + w / 2.0 - tw / 2.0, y - 12, tw, 24)


def path_of(pair):
    a, pts, b = ROUTES[pair]
    return [a] + list(pts) + [b]


def _seg_len(p, q):
    return abs(q[0] - p[0]) + abs(q[1] - p[1])


def slide_of(pair, point):
    """Edge geometry x (-1 source end .. 1 target end) of a point that lies on the route."""
    pts = path_of(pair)
    total = sum(_seg_len(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
    run = 0.0
    for k in range(len(pts) - 1):
        p, q = pts[k], pts[k + 1]
        if _on_seg(point, p, q):
            d = run + _seg_len(p, point)
            return round(2.0 * d / total - 1.0, 4), k
        run += _seg_len(p, q)
    raise ValueError("label point %s is not on the route %s" % (point, pair))


def _on_seg(pt, p, q):
    if p[0] == q[0] == pt[0]:
        return min(p[1], q[1]) <= pt[1] <= max(p[1], q[1])
    if p[1] == q[1] == pt[1]:
        return min(p[0], q[0]) <= pt[0] <= max(p[0], q[0])
    return False


def _ports(pair):
    """exit/entry fractions of a route's end points on their cells' walls (asserted to lie on the wall)."""
    a, _pts, b = ROUTES[pair]
    out = []
    for cid, pt in ((pair[0], a), (pair[1], b)):
        x, y, w, h = abs_rect(cid)
        fx, fy = (pt[0] - x) / float(w), (pt[1] - y) / float(h)
        assert -1e-9 <= fx <= 1 + 1e-9 and -1e-9 <= fy <= 1 + 1e-9, "%s: %s off %s" % (pair, pt, cid)
        assert fx in (0.0, 1.0) or fy in (0.0, 1.0), "%s: %s not on the wall of %s" % (pair, pt, cid)
        out.append((round(fx, 6), round(fy, 6)))
    return out


def _fmt(v):
    s = ("%.6f" % v).rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def _rect_hit(a, b, pad=0.0):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (ax - pad < bx + bw and bx < ax + aw + pad and ay - pad < by + bh and by < ay + ah + pad)


def _seg_hits_rect(p, q, r):
    """True when the axis-aligned segment p-q touches the rect r (inclusive of its edges)."""
    x0, x1 = min(p[0], q[0]), max(p[0], q[0])
    y0, y1 = min(p[1], q[1]), max(p[1], q[1])
    rx, ry, rw, rh = r
    return x0 <= rx + rw and rx <= x1 and y0 <= ry + rh and ry <= y1


def _crosses_border(box, r):
    """True when `box` is neither fully inside nor fully outside the rect r (it lies on r's wall)."""
    bx, by, bw, bh = box
    rx, ry, rw, rh = r
    inside = bx >= rx and by >= ry and bx + bw <= rx + rw and by + bh <= ry + rh
    outside = bx + bw <= rx or rx + rw <= bx or by + bh <= ry or ry + rh <= by
    return not inside and not outside


def label_problems(pair, lines, centre, cables, placed, horizontal_max=3, vertical_max=5):
    """Why a label at `centre` is not clear (empty list = clear). `cables`: the page's pairs; `placed`: label boxes
    already on the page."""
    why = []
    pts = path_of(pair)
    seg = None
    for k in range(len(pts) - 1):
        if _on_seg(centre, pts[k], pts[k + 1]):
            seg = (pts[k], pts[k + 1])
            break
    if seg is None:
        return ["not on its route"]
    p, q = seg
    horiz = p[1] == q[1]
    if len(lines) > (horizontal_max if horiz else vertical_max):
        why.append("%d lines on a %s run" % (len(lines), "horizontal" if horiz else "vertical"))
    box = label_box(lines, *centre)
    bx, by, bw, bh = box
    # the run: 20 px clear before and after the label, along the run
    if horiz:
        lo, hi = min(p[0], q[0]), max(p[0], q[0])
        if bx - 20 < lo or bx + bw + 20 > hi:
            why.append("run too short")
        axis_box = (bx - 20, by - 6, bw + 40, bh + 12)
    else:
        lo, hi = min(p[1], q[1]), max(p[1], q[1])
        if by - 20 < lo or by + bh + 20 > hi:
            why.append("run too short")
        axis_box = (bx - 6, by - 20, bw + 12, bh + 40)
    if bx < 10 or by < 10 or bx + bw > PAGE_W - 10 or by + bh > PAGE_H - 10:
        why.append("off page")
    for cid in NODES:
        if _rect_hit(axis_box, abs_rect(cid)):
            why.append("on card %s" % cid)
    for cid in CONTAINERS:
        if _crosses_border(axis_box, abs_rect(cid)):
            why.append("on the wall of %s" % cid)
        if _rect_hit(axis_box, title_box(cid)):
            why.append("on the title of %s" % cid)
    for fr in (TITLE_BOX, COMPANIONS_BOX) + STATEMENT_BOXES:
        if _rect_hit(axis_box, fr):
            why.append("on page furniture")
    near = (bx - 6, by - 6, bw + 12, bh + 12)
    for other in cables:
        if other == pair:
            continue
        op = path_of(other)
        for k in range(len(op) - 1):
            if _seg_hits_rect(op[k], op[k + 1], near):
                why.append("on cable %s -> %s" % other)
                break
    for ob in placed:
        if _rect_hit(near, ob):
            why.append("on another label")
    return why


def _check_titles(cables):
    """No cable crosses a container title."""
    bad = []
    for pair in cables:
        pts = path_of(pair)
        for cid in CONTAINERS:
            tb = title_box(cid)
            for k in range(len(pts) - 1):
                if _seg_hits_rect(pts[k], pts[k + 1], tb):
                    bad.append("%s -> %s crosses the title of %s" % (pair[0], pair[1], cid))
    return bad


def _fit_lines(text, chars):
    n = 0
    for part in str(text).split("\n"):
        n += max(1, len(wrap_label(part, chars)))
    return n


def _card_fits(cid, label_name, subtitle):
    """Rough text-fit estimate for a T1 clay + icon card (the render is the real check)."""
    x, y, w, h = abs_rect(cid)
    fs = 12 if w >= 220 else 11
    isz = 28 if not (h < 56 or w < 150) else max(14, min(28, h - 20, int((w - 16) * 0.34)))
    left = (6 if isz < 24 else 8) + isz + 6
    top = 10 if isz < 24 else 14
    usable = w - left - 10
    name_lines = _fit_lines(label_name, int(usable / (fs * 0.62)))
    sub_lines = _fit_lines(subtitle, int(usable / (fs * 0.52)))
    need = top + (name_lines + sub_lines) * fs * 1.2 + 4
    return need <= h, name_lines + sub_lines


# =================================================================================================== the page
def build_page(abbr, full_name, statements, states, subtitles, cables, companions, out_path):
    """Write one micro-frontend page to `out_path` (a .drawio holding exactly one diagram). Data only:
    abbr        'CSR' ... 'RSC' (keys the label slides)
    full_name   the title after '<ABBR>: '
    statements  3 strings: where the HTML is produced; where and when the micro-frontends are composed; the trade-off
    states      {node id: 'active' | 'muted' | 'pivot'} for every node (never a group: a group is muted when all its
                members are)
    subtitles   {node id: str}; a muted node with none gets 'not used in <ABBR>'
    cables      [(n, from id, to id, 'net' | 'page' | 'build', label)]; a label may hold '\\n' (a forced break)
    companions  6 file names
    Returns a dict of what was written (cells, cables, pivot, muted)."""
    errors = []
    if len(statements) != 3:
        errors.append("statements: 3 needed, got %d" % len(statements))
    if len(companions) != 6:
        errors.append("companions: 6 needed, got %d" % len(companions))
    for cid in states:
        if cid in CONTAINERS:
            errors.append("%s is a group or a container: it takes no state" % cid)
        elif cid not in NODES:
            errors.append("unknown node %s" % cid)
    for cid in subtitles:
        if cid not in NODES:
            errors.append("subtitle for %s, which is not a node" % cid)
    for cid in NODES:
        st = states.get(cid)
        if st not in ("active", "muted", "pivot"):
            errors.append("%s: state %r (active, muted or pivot needed)" % (cid, st))
        if st in ("active", "pivot") and not subtitles.get(cid):
            errors.append("%s: an active node needs a subtitle" % cid)
    pivots = [c for c in NODES if states.get(c) == "pivot"]
    if len(pivots) != 1:
        errors.append("exactly one pivot needed, got %s" % pivots)
    pairs = []
    for cab in cables:
        n, a, b, cls, label = cab
        if (a, b) not in ROUTES:
            errors.append("no route for %s -> %s (an unknown pair is never auto-routed)" % (a, b))
        if cls not in EDGE_CLASSES:
            errors.append("%s -> %s: unknown edge class %r" % (a, b, cls))
        if label and (abbr, a, b) not in LABELS:
            errors.append("no label slide for %s %s -> %s" % (abbr, a, b))
        if (a, b) in pairs:
            errors.append("%s -> %s drawn twice" % (a, b))
        pairs.append((a, b))
    if errors:
        raise ValueError("mfe_frame.build_page(%s):\n  " % abbr + "\n  ".join(errors))

    # ---------------------------------------------------------------- self-checks before writing
    problems = _check_titles(pairs)
    placed = []
    label_cells = {}
    for n, a, b, cls, label in cables:
        if not label:
            continue
        wrap, centre = LABELS[(abbr, a, b)]
        lines = wrap_label(label, wrap)
        why = label_problems((a, b), lines, centre, pairs, placed)
        if why:
            problems.append("label %s -> %s: %s" % (a, b, "; ".join(sorted(set(why)))))
        placed.append(label_box(lines, *centre))
        label_cells[(a, b)] = (lines, centre)
    for k, s in enumerate(statements):
        if len(wrap_label(s, STATEMENT_CHARS)) > STATEMENT_LINES:
            problems.append("statement S%d needs more than %d lines of %d characters"
                            % (k + 1, STATEMENT_LINES, STATEMENT_CHARS))
    subs = {}
    for cid in NODES:
        sub = subtitles.get(cid) or (MUTED_DEFAULT % abbr)
        subs[cid] = sub
        ok, nl = _card_fits(cid, NODES[cid][0], sub)
        if not ok:
            problems.append("%s: text may overflow (%d lines)" % (cid, nl))
    if problems:
        raise ValueError("mfe_frame.build_page(%s) refused to write:\n  " % abbr + "\n  ".join(problems))

    # ---------------------------------------------------------------- cells
    cls_of = {}
    for cid, n in NODES.items():
        st = states[cid]
        cls_of[cid] = ("pivot" if st == "pivot" else "muted" if st == "muted" else
                       ("team-" + n[7]) if n[7] else "platform")
    group_muted = {g: all(states[c] == "muted" for c, n in NODES.items() if n[2] == g) for g in GROUPS}

    def container_xml(cid):
        title, parent, x, y, w, h, role = CONTAINERS[cid]
        has_frame_child = any(CONTAINERS[k][1] == cid for k in CONTAINERS)
        sw = 4 if (parent == "1" and has_frame_child) else 3
        fill, stroke = (GROUP_FILL, GROUP_STROKE) if role == "group" else (COLUMN_FILL, COLUMN_STROKE)
        st = ("swimlane;startSize=0;labelBorderColor=none;textShadow=1;labelBackgroundColor=default;rounded=0;html=1;"
              "fillColor=%s;swimlaneFillColor=%s;strokeColor=%s;strokeWidth=%d;fontColor=%s;fontSize=14;fontStyle=1;"
              "shadow=1;" % (fill, fill, stroke, sw, TITLE_FONT))
        if role == "group" and group_muted.get(cid):
            st = st.replace("strokeColor=%s;" % stroke, "").replace("fontColor=%s;" % TITLE_FONT, "") + MUTED_GROUP
        if role == "legend":
            st += "kitExempt=1;"
        rx, ry = _rel(cid, x, y)
        return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"><mxGeometry x="%d" y="%d" width="%d" '
                'height="%d" as="geometry"/></mxCell>' % (cid, gen_text.X(title), st, parent, rx, ry, w, h))

    def card_xml(cid):
        name, icon, parent, x, y, w, h, _team = NODES[cid]
        cls = cls_of[cid]
        kind, fill, keys = CLASSES[cls]
        fs = 12 if w >= 220 else 11
        label = "<b>%s</b><br>%s" % (_esc(name), _esc(subs[cid]))
        rx, ry = _rel(cid, x, y)
        out = gen_text.text(cid, "t1", kind, label, rx, ry, w, h, color=fill, style="clay", icon=icon, font_size=fs)
        assert len(out) == 1, "%s: expected one composite cell, got %d" % (cid, len(out))
        s = out[0]
        assert s.count("shadow=1;") == 1, "%s: the kit's shadow key moved" % cid
        s = s.replace("shadow=1;", keys)
        s = _style_add(s, "mfeClass=%s;" % cls)
        return _reparent(s, parent)

    body = []
    for cid in ORDER:
        body.append(container_xml(cid) if cid in CONTAINERS else card_xml(cid))

    # legend (its rows are its children)
    lx, ly = CONTAINERS["C-LEGEND"][2], CONTAINERS["C-LEGEND"][3]
    body.append(container_xml("C-LEGEND"))
    for i, (cls, text) in enumerate(LEGEND_BADGES):
        kind, fill, keys = CLASSES[cls]
        bx, by = 20 + (i % 3) * 260, 40 + (i // 3) * 60
        out = gen_text.text("L-BADGE-%s" % cls, "t4", kind, _esc(text), bx, by, 240, 40, color=fill)
        for s in out:
            s = s.replace("shadow=1;", keys)
            body.append(_reparent(_style_add(s, "kitExempt=1;"), "C-LEGEND"))
    for i, (cls, text) in enumerate(LEGEND_SAMPLES):
        body.append('<mxCell id="L-CAPTION-%s" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="140" '
                    'y="%d" width="640" height="40" as="geometry"/></mxCell>'
                    % (cls, gen_text.X(_esc(text)), ROW, 160 + i * 40))
    for i, (text, (yy, hh)) in enumerate(zip(LEGEND_LINES, ((280, 60), (340, 40)))):
        body.append('<mxCell id="L-LINE-%d" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="20" '
                    'y="%d" width="760" height="%d" as="geometry"/></mxCell>'
                    % (i + 1, gen_text.X(_esc(text)), ROW.replace("verticalAlign=middle", "verticalAlign=top"), yy, hh))

    # content cables (parent 1), then the legend's sample cables
    edges = []
    for n, a, b, cls, label in cables:
        (ex, ey), (nx, ny) = _ports((a, b))
        st = ("edgeStyle=none;rounded=0;html=1;exitX=%s;exitY=%s;exitDx=0;exitDy=0;entryX=%s;entryY=%s;entryDx=0;"
              "entryDy=0;%s%s" % (_fmt(ex), _fmt(ey), _fmt(nx), _fmt(ny), EDGE_CLASSES[cls], LABEL_STYLE))
        value, pos = "", ""
        if label:
            lines, centre = label_cells[(a, b)]
            value = "<br>".join(_esc(s) for s in lines)
            lp, _seg = slide_of((a, b), centre)
            pos = ' x="%s"' % _fmt(lp)
        _a, pts, _b = ROUTES[(a, b)]
        arr = ""
        if pts:
            arr = '<Array as="points">%s</Array>' % "".join('<mxPoint x="%d" y="%d"/>' % p for p in pts)
        edges.append('<mxCell id="X-%s--%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
                     '<mxGeometry%s relative="1" as="geometry">%s</mxGeometry></mxCell>'
                     % (a, b, gen_text.X(value), st, a, b, pos, arr))
    for i, (cls, _text) in enumerate(LEGEND_SAMPLES):
        y = ly + 180 + i * 40
        edges.append('<mxCell id="L-SAMPLE-%s" value="" style="edgeStyle=none;rounded=0;html=1;%skitExempt=1;" '
                     'edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="%d" y="%d" '
                     'as="sourcePoint"/><mxPoint x="%d" y="%d" as="targetPoint"/></mxGeometry></mxCell>'
                     % (cls, EDGE_CLASSES[cls], lx + 20, y, lx + 120, y))

    # page furniture (top level, front)
    front = []
    title = "%s %s: %s" % (TITLE_PREFIX, abbr, full_name)
    for s in gen_text.text("F-TITLE", "t3", "neutral", _esc(title), *TITLE_BOX):
        front.append(_style_add(s, "kitExempt=1;"))
    for k, (head, text) in enumerate(zip(STATEMENT_HEADINGS, statements)):
        label = "<b>%s</b><br>%s" % (_esc(head), _esc(text))
        for s in gen_text.text("F-S%d" % (k + 1), "t1", "neutral", label, *STATEMENT_BOXES[k], color="#FFFFFF"):
            front.append(_style_add(s, "kitExempt=1;"))
    comp = "<b>%s</b> %s" % (_esc(COMPANIONS_HEADING), " · ".join(_esc(c) for c in companions))
    for s in gen_text.text("F-COMPANIONS", "t1", "neutral", comp, *COMPANIONS_BOX, color="#FFFFFF"):
        front.append(_style_add(s, "kitExempt=1;"))

    cells = body + edges + front
    xml = ('<mxfile host="mfe-frame">\n<diagram name="%s" id="mfe-%s">\n<mxGraphModel dx="1600" dy="900" grid="1" '
           'gridSize="20" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
           'pageWidth="%d" pageHeight="%d" math="0" shadow="0">\n<root>\n<mxCell id="0"/>\n<mxCell id="1" parent="0"/>\n'
           % (gen_text.X(title), abbr.lower(), PAGE_W, PAGE_H) + "\n".join(cells)
           + '\n</root>\n</mxGraphModel>\n</diagram>\n</mxfile>\n')
    _verify(xml, abbr)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(xml.encode("utf-8"))
    return {"path": out_path, "cells": len(cells) + 2, "cables": len(cables), "pivot": pivots[0],
            "muted": sorted(c for c in NODES if states[c] == "muted")}


def _verify(xml, abbr):
    """Checks on the file itself: grid, one diagram, class markers and shadow keys."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    assert len(root.findall("diagram")) == 1, "exactly one <diagram>"
    ids = [c.get("id") for c in root.iter("mxCell")]
    assert len(ids) == len(set(ids)), "duplicate cell ids"
    for c in root.iter("mxCell"):
        g = c.find("mxGeometry")
        if g is None:
            continue
        if c.get("vertex") == "1" and c.get("style", "").find("shape=stencil") >= 0 and c.get("id", "").endswith(
                ("_fold", "_nl", "_nr")):
            continue                                   # the kit's own chrome (fold, notches) sits at its own offsets
        for k in ("x", "y", "width", "height"):
            v = g.get(k)
            if v is not None and c.get("vertex") == "1":
                assert float(v) % GRID == 0, "%s %s=%s off the %d-px grid" % (c.get("id"), k, v, GRID)
        for p in g.iter("mxPoint"):
            for k in ("x", "y"):
                assert float(p.get(k)) % GRID == 0, "%s point off the grid" % c.get("id")
    cards = [c for c in root.iter("mxCell") if "mfeClass=" in (c.get("style") or "")]
    assert len(cards) == len(NODES), "every content card carries mfeClass (%d of %d)" % (len(cards), len(NODES))
    pivots = [c for c in cards if "mfeClass=pivot;" in c.get("style")]
    assert len(pivots) == 1, "exactly one mfeClass=pivot"
    for c in cards:
        st = c.get("style")
        assert st.count("shadow=") == 1, "%s: %d shadow keys" % (c.get("id"), st.count("shadow="))
        assert ("shadow=1;" in st) == ("mfeClass=pivot;" in st), "%s: shadow=1 only on the pivot" % c.get("id")
        if "mfeClass=muted;" in st:
            for k in ("opacity=45;", "textOpacity=60;", "opacityGroup=1;"):
                assert k in st, "%s: muted card lacks %s" % (c.get("id"), k)
