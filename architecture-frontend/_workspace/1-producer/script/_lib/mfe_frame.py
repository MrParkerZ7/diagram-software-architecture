# -*- coding: utf-8 -*-
"""The shared micro-frontend frame: one page layout for the seven micro-frontend diagrams.

Contract (current truth, read it first): ../../analysis/micro-frontend-frame.md
A shared helper under _lib/, never a builder and never run on its own. A slot's builder imports it and calls
build_page() with data only: title words, statements, node states, cables, companions. This module owns every
coordinate, style, class marker, port, waypoint, label wrap and label slide, and checks its own output before it
writes (the 20-px grid, the class markers, captions clear of cables and labels, cables clear of container titles).

The page is an architecture page in the prompt master's standard: every part is an icon with its name as a caption,
and the numbered arrows between the icons carry the workflow. No part is a text card.

Environment (never written into a committed file): DIAGRAM_KIT = the prompt master's shared/prompts/3-diagram folder.
"""
import base64
import hashlib
import html
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
sys.path.insert(0, os.path.join(KIT, "icons"))
sys.path.insert(0, os.path.join(KIT, "icons", "craft"))
import gen_text  # noqa: E402
import gen_craft  # noqa: E402

GRID = 20
PAGE_W, PAGE_H = 3240, 1840

# ----------------------------------------------------------------------------------------------------- containers
# id: (title, parent, absolute x, y, w, h, role); role: column | group | legend.  All swimlane;startSize=0.
CONTAINERS = {
    "C-BROWSER": ("Browser (one page at run time)", "1", 40, 320, 920, 780, "column"),
    "G-REMOTES": ("Team UIs (micro-frontends)", "C-BROWSER", 60, 360, 240, 460, "group"),
    "G-SHELL": ("App shell", "C-BROWSER", 460, 360, 160, 360, "group"),
    "C-EDGE": ("Edge (CDN and proxy)", "1", 1240, 320, 400, 780, "column"),
    "C-ORIGIN": ("Origin (servers)", "1", 1840, 320, 700, 780, "column"),
    "G-SERVERS": ("Team servers", "C-ORIGIN", 1860, 900, 660, 180, "group"),
    "C-BACKEND": ("Backend (APIs and content)", "1", 2740, 320, 340, 780, "column"),
    "G-APIS": ("Team APIs", "C-BACKEND", 2760, 500, 300, 460, "group"),
    "C-BUILD": ("Build time (before any request)", "1", 1240, 1180, 1300, 460, "column"),
    "G-CI": ("Team pipelines", "C-BUILD", 2080, 1220, 440, 160, "group"),
    "C-LEGEND": ("Legend", "1", 40, 1180, 920, 520, "legend"),
}
GROUPS = ("G-REMOTES", "G-SHELL", "G-SERVERS", "G-APIS", "G-CI")
# Area colours: the master's PROMPT_ARROW_STYLE.md § Component Color Standards -> Subnet Types (the tier frames of an
# architecture diagram, on any cloud or none) and PROMPT_CONTAINER.md § Frame Colors by Purpose (the Optional row, for
# the build phase, which is outside the request path). tier: (fill, stroke, font colour, what the legend says)
TIERS = {
    "client": ("#F5F5F5", "#666666", "#333333", "Client: the browser, outside the system"),
    "public": ("#F0F7E6", "#7AA116", "#3D7317", "Public: the internet-facing edge"),
    "compute": ("#EDF4FA", "#147EBA", "#0D5594", "Compute / app: the origin servers"),
    "integration": ("#FFF8F0", "#D6B656", "#B8860B", "Integration: the APIs and the content"),
    "build": ("#FFFFFF", "#999999", "#666666", "Outside the request path: build and deploy"),
}
TIER_OF = {"C-BROWSER": "client", "C-EDGE": "public", "C-ORIGIN": "compute", "C-BACKEND": "integration",
           "C-BUILD": "build"}          # a group takes its column's stroke and font colour, on a white fill
GROUP_FILL = "#FFFFFF"
LEGEND_FILL, LEGEND_STROKE, TITLE_FONT = "#F5F5F5", "#666666", "#333333"   # the legend: the standard's grey box


def tier_of(cid):
    """The tier of a column, or of the column that holds a group (None for the legend)."""
    while cid not in TIER_OF:
        cid = CONTAINERS[cid][1]
        if cid == "1":
            return None
    return TIER_OF[cid]

# ------------------------------------------------------------------------------------------------------- nodes
# id: (NAME = the caption, art, parent, absolute x, y, size, team: a | b | c | None = platform)
# art = "craft:<subject>" (a crafted icon of the prompt master's craft kit, an image cell) or "shape:<key>" (a generic
# shape of PROMPT_ICON.md, SHAPES below). The page names no provider, so no provider's product icon stands in for a
# generic part; a generic shape comes first, then a crafted icon (the contract, § Nodes).
# Every node is one square icon. The hubs are 160 (or 120) so a cable can leave a face beside the caption.
NODES = {
    "B-PAGE": ("Browser tab", "craft:browser-tab", "C-BROWSER", 780, 640, 160, None),
    "B-SHELL": ("Runtime loader", "craft:runtime-loader", "G-SHELL", 500, 400, 80, None),
    "B-ROUTER": ("Client router", "craft:client-router", "G-SHELL", 500, 520, 80, None),
    "B-UI-A": ("Team A · Catalog UI", "craft:ui-component", "G-REMOTES", 140, 400, 80, "a"),
    "B-UI-B": ("Team B · Cart UI", "craft:ui-component", "G-REMOTES", 140, 540, 80, "b"),
    "B-UI-C": ("Team C · Account UI", "craft:ui-component", "G-REMOTES", 140, 680, 80, "c"),
    "B-BUS": ("Event bus", "craft:event-bus", "C-BROWSER", 140, 920, 80, None),
    "B-SHARED": ("Shared libraries", "craft:shared-library", "C-BROWSER", 500, 920, 80, None),
    "E-ROUTER": ("Edge router", "shape:router", "C-EDGE", 1360, 560, 160, None),
    "E-CACHE": ("Page cache", "shape:cache", "C-EDGE", 1460, 860, 80, None),
    "E-CDN": ("CDN", "craft:cdn", "C-EDGE", 1260, 900, 160, None),
    "O-COMPOSER": ("Page composer", "shape:web_server", "C-ORIGIN", 1920, 520, 160, None),
    "O-BFF": ("BFF", "craft:bff", "C-ORIGIN", 2260, 600, 160, None),
    "O-SRV-A": ("Team A server", "shape:web_server", "G-SERVERS", 1940, 940, 80, "a"),
    "O-SRV-B": ("Team B server", "shape:web_server", "G-SERVERS", 2160, 940, 80, "b"),
    "O-SRV-C": ("Team C server", "shape:web_server", "G-SERVERS", 2380, 940, 80, "c"),
    "K-API-A": ("Catalog API (team A)", "craft:api-service", "G-APIS", 2880, 540, 80, "a"),
    "K-API-B": ("Order API (team B)", "craft:api-service", "G-APIS", 2880, 680, 80, "b"),
    "K-API-C": ("Account API (team C)", "craft:api-service", "G-APIS", 2880, 820, 80, "c"),
    "K-CMS": ("Headless CMS", "craft:headless-cms", "C-BACKEND", 2880, 980, 80, None),
    "D-REGISTRY": ("Registry", "craft:manifest-registry", "C-BUILD", 2000, 1480, 120, None),
    "D-INTEGRATION": ("Integration build", "craft:ci-pipeline", "C-BUILD", 1660, 1500, 80, None),
    "D-CI-A": ("Team A pipeline", "craft:ci-pipeline", "G-CI", 2120, 1260, 80, "a"),
    "D-CI-B": ("Team B pipeline", "craft:ci-pipeline", "G-CI", 2260, 1260, 80, "b"),
    "D-CI-C": ("Team C pipeline", "craft:ci-pipeline", "G-CI", 2400, 1260, 80, "c"),
}
# The highlight (owner, 2026-11-17: L or S by default, a framed F or G only for a parent, a hub or something important):
# the crafted hubs, the parts the page's arrows meet at, are drawn in the craft kit's highlight style (G, a navy tile with a
# gold rim) and every other crafted icon in the kit's default (L). The set is the same on all seven pages, so they still
# compare part for part; the pivot keeps its amber caption, which is the one thing that moves. The generic hubs (the edge
# router, the page composer) are shapes of PROMPT_ICON.md, not crafted icons, and take no highlight.
HIGHLIGHT = ("B-PAGE", "E-CDN", "O-BFF", "D-REGISTRY")
assert set(HIGHLIGHT) == {c for c, n in NODES.items() if n[1].startswith("craft:") and n[5] >= 120}, \
    "HIGHLIGHT is the crafted hubs: every crafted icon of size 120 or 160, and no other"

# Cell order (z): each container, then its children, depth first.
ORDER = ["C-BROWSER", "G-REMOTES", "B-UI-A", "B-UI-B", "B-UI-C", "G-SHELL", "B-SHELL", "B-ROUTER", "B-PAGE", "B-BUS",
         "B-SHARED",
         "C-EDGE", "E-ROUTER", "E-CACHE", "E-CDN",
         "C-ORIGIN", "O-COMPOSER", "O-BFF", "G-SERVERS", "O-SRV-A", "O-SRV-B", "O-SRV-C",
         "C-BACKEND", "G-APIS", "K-API-A", "K-API-B", "K-API-C", "K-CMS",
         "C-BUILD", "D-INTEGRATION", "D-REGISTRY", "G-CI", "D-CI-A", "D-CI-B", "D-CI-C"]

# ------------------------------------------------------------------------------------------------ colour classes
# The class is said by the caption's tint (the prompt master's rule: the container, the caption's tint or a faded
# icon say a class, never a card). class: (caption fill, caption border, legend badge kit kind)
CLASSES = {
    "team-a": ("#DAE8FC", "#6C8EBF", "info"),
    "team-b": ("#D5E8D4", "#82B366", "success"),
    "team-c": ("#E1D5E7", "#9673A6", "accent"),
    "platform": ("#ECEFF1", "#90A4AE", "neutral"),
    "pivot": ("#FFD54F", "#E69500", "note"),
    "muted": ("#F5F5F5", "#BDBDBD", "neutral"),
}
# The generic shapes of PROMPT_ICON.md the page uses (General Network Shapes; the generic cache of Database Types).
_NET = ("html=1;aspect=fixed;sketch=0;outlineConnect=0;gradientColor=none;fillColor=#036897;strokeColor=#ffffff;"
        "dashed=0;pointerEvents=1;shadow=1;")
SHAPES = {
    "router": "shape=mxgraph.networks.router;" + _NET,
    "web_server": "shape=mxgraph.networks.web_server;" + _NET,
    "cache": "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=15;html=1;aspect=fixed;strokeColor=#d79b00;"
             "fillColor=#ffe6cc;strokeWidth=2;shadow=1;",
}
MUTED_KEYS = "opacity=40;textOpacity=40;opacityGroup=1;"   # opacityGroup: a stencil or a group of parts fades as one
MUTED_GROUP = "strokeColor=#BDBDBD;fontColor=#9E9E9E;opacity=45;"
CAPTION_FONT = "#1F2937"
CAP_CHAR_W, CAP_PAD, CAP_H, CAP_GAP = 7.4, 10, 20, 2   # caption estimate: bold 12 (a little wider than drawn)

# ------------------------------------------------------------------------------------------------- edge classes
# The arrow format of PROMPT_ARROW_STYLE.md: the arrow type by what the call is (an HTTP request: classic; a lightweight
# call: open; a publish or deploy: classic), strokeWidth 2, shadow=1, the standard's neutral gray (#232F3E) for HTTP and a
# lighter gray for a build link. flowAnimation=1 is on the solid request arrows only, as the standard's own examples have
# it: draw.io draws an animated arrow with moving dashes, so on a dashed or dotted class it would blur the three classes.
EDGE_CLASSES = {
    "net": "strokeColor=#232F3E;strokeWidth=2;endArrow=classic;endFill=1;flowAnimation=1;shadow=1;",
    "page": "strokeColor=#232F3E;strokeWidth=2;dashed=1;dashPattern=1 3;endArrow=open;endFill=0;shadow=1;",
    "build": "strokeColor=#616161;strokeWidth=2;dashed=1;dashPattern=14 8;endArrow=classic;endFill=1;shadow=1;",
}
LABEL_STYLE = "fontSize=11;fontColor=#232F3E;labelBackgroundColor=#FFFFFF;"
CHAR_W, LINE_H = 6.0, 13.2            # label estimate at font 11 (a little wider than drawn, on purpose)

# --------------------------------------------------------------------------------------------------- routing
# (from, to): (start point on the source's wall, [waypoints], end point on the target's wall), absolute px.
# Every segment is axis-aligned; every bend sits in free space (a gutter, a street, the east lane), never inside a
# rectangle; inside a container a cable is one straight segment. No cable touches a caption: a cable leaves an icon's
# bottom face only beside its caption. See the contract's Routing table and Paper check.
ROUTES = {
    ("B-PAGE", "E-ROUTER"): ((940, 680), [], (1360, 680)),
    ("B-PAGE", "E-CDN"): ((940, 760), [(1100, 760), (1100, 980)], (1260, 980)),
    ("B-PAGE", "G-SHELL"): ((780, 680), [], (620, 680)),
    ("B-PAGE", "G-REMOTES"): ((780, 760), [], (300, 760)),
    ("B-SHELL", "G-REMOTES"): ((500, 440), [], (300, 440)),
    ("B-ROUTER", "G-REMOTES"): ((500, 560), [], (300, 560)),
    ("G-REMOTES", "B-BUS"): ((180, 820), [], (180, 920)),
    ("G-SHELL", "B-SHARED"): ((540, 720), [], (540, 920)),
    ("E-ROUTER", "O-COMPOSER"): ((1520, 600), [], (1920, 600)),
    ("E-ROUTER", "O-BFF"): ((1520, 680), [(1780, 680), (1780, 740)], (2260, 740)),
    ("E-ROUTER", "G-SERVERS"): ((1520, 680), [(1780, 680), (1780, 1000)], (1860, 1000)),
    ("E-ROUTER", "E-CACHE"): ((1500, 720), [], (1500, 860)),
    ("E-CACHE", "O-COMPOSER"): ((1540, 880), [(1740, 880), (1740, 640)], (1920, 640)),
    ("O-COMPOSER", "O-BFF"): ((2080, 660), [], (2260, 660)),
    ("O-COMPOSER", "G-SERVERS"): ((1940, 680), [], (1940, 900)),
    ("G-SERVERS", "O-BFF"): ((2300, 900), [], (2300, 760)),
    ("O-BFF", "G-APIS"): ((2420, 720), [], (2760, 720)),
    ("O-BFF", "K-API-B"): ((2420, 720), [], (2880, 720)),
    ("K-CMS", "O-COMPOSER"): ((2960, 1000), [(3120, 1000), (3120, 260), (2020, 260)], (2020, 520)),
    ("G-CI", "E-CDN"): ((2120, 1220), [(2120, 1140), (1380, 1140)], (1380, 1060)),
    ("G-CI", "D-REGISTRY"): ((2100, 1380), [], (2100, 1480)),
    ("D-REGISTRY", "E-CDN"): ((2040, 1480), [(2040, 1160), (1280, 1160)], (1280, 1060)),
    ("G-CI", "G-SERVERS"): ((2500, 1220), [(2500, 1140), (2240, 1140)], (2240, 1080)),
    ("D-REGISTRY", "D-INTEGRATION"): ((2000, 1540), [], (1740, 1540)),
    ("D-INTEGRATION", "K-CMS"): ((1660, 1560), [(1200, 1560), (1200, 1680), (3120, 1680), (3120, 1020)],
                                 (2960, 1020)),
    ("D-INTEGRATION", "K-API-A"): ((1660, 1520), [(1160, 1520), (1160, 1700), (3160, 1700), (3160, 580)],
                                   (2960, 580)),
    ("D-INTEGRATION", "E-CDN"): ((1700, 1500), [(1700, 1160), (1300, 1160)], (1300, 1060)),
    ("D-INTEGRATION", "E-CACHE"): ((1700, 1500), [(1700, 920)], (1540, 920)),
    ("D-INTEGRATION", "O-COMPOSER"): ((1660, 1560), [(1200, 1560), (1200, 1680), (3120, 1680), (3120, 260),
                                                     (1980, 260)], (1980, 520)),
}

# (abbr, from, to): (wrap, (label centre x, y)) - the centre lies on the route; the frame turns it into the edge
# geometry x (the label slide). Found by the dry run (every label clear of icons, captions, walls, titles and cables)
# and frozen.
LABELS = {
    # LABELS-BEGIN (written by the dry run; do not edit by hand)
    ("CSR", "B-PAGE", "E-CDN"): (30, (1100, 870)),
    ("CSR", "B-PAGE", "E-ROUTER"): (18, (1100, 680)),
    ("CSR", "B-PAGE", "G-SHELL"): (20, (700, 680)),
    ("CSR", "B-SHELL", "G-REMOTES"): (16, (380, 440)),
    ("CSR", "D-REGISTRY", "E-CDN"): (22, (1280, 1130)),
    ("CSR", "E-ROUTER", "O-BFF"): (26, (2150, 740)),
    ("CSR", "G-CI", "D-REGISTRY"): (16, (2100, 1430)),
    ("CSR", "G-CI", "E-CDN"): (32, (1750, 1140)),
    ("CSR", "G-SHELL", "B-SHARED"): (18, (540, 830)),
    ("CSR", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("SPA", "B-PAGE", "E-CDN"): (20, (1100, 870)),
    ("SPA", "B-PAGE", "E-ROUTER"): (20, (1100, 680)),
    ("SPA", "B-PAGE", "G-SHELL"): (18, (700, 680)),
    ("SPA", "B-ROUTER", "G-REMOTES"): (20, (380, 560)),
    ("SPA", "D-REGISTRY", "E-CDN"): (22, (1280, 1130)),
    ("SPA", "E-ROUTER", "O-BFF"): (26, (2150, 740)),
    ("SPA", "G-CI", "D-REGISTRY"): (16, (2100, 1430)),
    ("SPA", "G-CI", "E-CDN"): (32, (1750, 1140)),
    ("SPA", "G-REMOTES", "B-BUS"): (18, (180, 880)),
    ("SPA", "G-SHELL", "B-SHARED"): (18, (540, 830)),
    ("SPA", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("MPA", "B-PAGE", "E-CDN"): (30, (1100, 870)),
    ("MPA", "B-PAGE", "E-ROUTER"): (34, (1100, 680)),
    ("MPA", "E-ROUTER", "G-SERVERS"): (16, (1780, 840)),
    ("MPA", "G-CI", "E-CDN"): (22, (1570, 1140)),
    ("MPA", "G-CI", "G-SERVERS"): (18, (2370, 1140)),
    ("MPA", "G-SERVERS", "O-BFF"): (20, (2300, 840)),
    ("MPA", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("SSR", "B-PAGE", "E-CDN"): (26, (1100, 870)),
    ("SSR", "B-PAGE", "E-ROUTER"): (20, (1100, 680)),
    ("SSR", "B-PAGE", "G-REMOTES"): (22, (690, 760)),
    ("SSR", "E-ROUTER", "O-COMPOSER"): (18, (1740, 600)),
    ("SSR", "G-CI", "E-CDN"): (26, (1570, 1140)),
    ("SSR", "G-CI", "G-SERVERS"): (20, (2370, 1140)),
    ("SSR", "G-SERVERS", "O-BFF"): (18, (2300, 840)),
    ("SSR", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("SSR", "O-COMPOSER", "G-SERVERS"): (30, (1940, 800)),
    ("SSG", "B-PAGE", "E-CDN"): (24, (1100, 870)),
    ("SSG", "B-PAGE", "E-ROUTER"): (28, (1100, 680)),
    ("SSG", "B-PAGE", "G-REMOTES"): (28, (550, 760)),
    ("SSG", "D-INTEGRATION", "E-CDN"): (18, (1700, 1360)),
    ("SSG", "D-INTEGRATION", "K-API-A"): (22, (3160, 810)),
    ("SSG", "D-INTEGRATION", "K-CMS"): (18, (1440, 1560)),
    ("SSG", "D-REGISTRY", "D-INTEGRATION"): (22, (1890, 1540)),
    ("SSG", "E-ROUTER", "O-BFF"): (26, (2150, 740)),
    ("SSG", "G-CI", "D-REGISTRY"): (24, (2100, 1440)),
    ("SSG", "O-BFF", "K-API-B"): (22, (2640, 720)),
    ("ISR", "B-PAGE", "E-CDN"): (26, (1100, 870)),
    ("ISR", "B-PAGE", "E-ROUTER"): (20, (1100, 680)),
    ("ISR", "D-INTEGRATION", "E-CACHE"): (26, (1700, 1360)),
    ("ISR", "E-CACHE", "O-COMPOSER"): (30, (1740, 760)),
    ("ISR", "E-ROUTER", "E-CACHE"): (24, (1500, 810)),
    ("ISR", "G-CI", "G-SERVERS"): (30, (2370, 1140)),
    ("ISR", "G-SERVERS", "O-BFF"): (16, (2300, 840)),
    ("ISR", "K-CMS", "O-COMPOSER"): (28, (2020, 440)),
    ("ISR", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("ISR", "O-COMPOSER", "G-SERVERS"): (26, (1940, 800)),
    ("RSC", "B-PAGE", "E-CDN"): (18, (1100, 870)),
    ("RSC", "B-PAGE", "E-ROUTER"): (30, (1100, 680)),
    ("RSC", "B-PAGE", "G-REMOTES"): (22, (540, 760)),
    ("RSC", "D-INTEGRATION", "O-COMPOSER"): (22, (3120, 1400)),
    ("RSC", "D-REGISTRY", "D-INTEGRATION"): (18, (1890, 1540)),
    ("RSC", "E-ROUTER", "O-COMPOSER"): (20, (1740, 600)),
    ("RSC", "G-CI", "D-REGISTRY"): (24, (2100, 1440)),
    ("RSC", "O-BFF", "G-APIS"): (18, (2640, 720)),
    ("RSC", "O-COMPOSER", "O-BFF"): (18, (2170, 660)),
    # LABELS-END
}

# ------------------------------------------------------------------------------------------------- furniture
TITLE_PREFIX = "Micro-frontends with"
STATEMENT_HEADINGS = ("Where the HTML is produced", "Where and when the micro-frontends are composed",
                      "Trade-off for micro-frontends")
STATEMENT_BOXES = ((40, 100, 1000, 120), (1120, 100, 1000, 120), (2200, 100, 1000, 120))
# Capacity of a statement card, measured on the renders: about 160 characters a line at font 12 in a 1000-px card
# (counted at 150, so a line never overflows), the heading plus 5 lines.
STATEMENT_CHARS, STATEMENT_LINES = 150, 5
TITLE_BOX = (40, 20, 3160, 60)
COMPANIONS_BOX = (40, 1760, 3160, 60)
COMPANIONS_HEADING = "Companions (same frame):"
LEGEND_BADGES = (("team-a", "Team A · Catalog"), ("team-b", "Team B · Cart and orders"), ("team-c", "Team C · Account"),
                 ("platform", "Shared or platform-owned"), ("pivot", "Where the micro-frontends are composed (the pivot)"),
                 ("muted", "Not used in this approach"))
LEGEND_SAMPLES = (("net", "Network request at run time: the arrow is the request, the label says what comes back"),
                  ("page", "Call inside the page (no network)"),
                  ("build", "Build or deploy, before any request"))
LEGEND_LINES = (
    "Each part is an icon; its caption names it, and the caption's colour is its class. Numbers = the order of the "
    "steps of the flow drawn; numbered dashed steps are build steps and come before any request; an unnumbered cable "
    "stands outside that order (a build or deploy link, a standing link, or a separate trigger).",
    "BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), "
    "drawn where this example uses them; the headless CMS is a data source, not a BFF.")
LEGEND_L, LEGEND_R, LEGEND_COL = 20, 480, 420      # the legend's two columns (x, x, width), relative to the legend
LEGEND_ARROWS_Y = 250                              # the Arrows heading; the samples follow it, 40 px apart
LEGEND_NOTES = ((300, 80), (390, 50))              # (y, height) of the two note paragraphs, right column
LEGEND_ICONS_Y = 410                             # the Icons heading; its sample row follows 30 px below
LEGEND_HUB_ART = "cdn"                           # the crafted subject the legend draws its highlight sample from
LEGEND_HUB_TEXT = ("Navy tile with a gold rim: a hub, where several arrows meet (the generic router and the servers keep "
                   "their own shape)")
TIER_ORDER = ("client", "public", "compute", "integration", "build")
ROW = ("text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=11;"
       "fontColor=#37474F;kitExempt=1;")

# ------------------------------------------------------------------------------------------- kit fingerprint
# The frame calls the prompt master's kit live. This digest is of the kit's OUTPUT for fixed probes (one icon per glyph
# the frame uses, and one text-kit cell per pattern it uses), taken when the frame was last proved. If the kit changes
# what it draws, build_page refuses to write until the frame is proved again: re-run the dry run on all seven pages,
# both gates, look at every render, then set KIT_FINGERPRINT to the new digest (the contract's Frame proof says how).
KIT_FINGERPRINT = "c25be24ee48fa96378e5e77ac71fda54acb33482804e8acce2c1f67ef3214349"


def craft_svg(subject, uid, highlight=False):
    """The crafted icon of a subject: in the style its category maps to (the craft kit's style map, L), or in the kit's
    highlight style when `highlight` (a hub of HIGHLIGHT)."""
    return gen_craft.icon_svg(gen_craft.style_for(subject, highlight=highlight), subject, uid)


def kit_fingerprint():
    h = hashlib.sha256()
    for art, hl in sorted({(n[1], cid in HIGHLIGHT) for cid, n in NODES.items()}):
        kind, _, ref = art.partition(":")
        body = craft_svg(ref, "probe_", hl) if kind == "craft" else SHAPES[ref]
        h.update(("%s|%s|%s\n" % (art, "highlight" if hl else "default", body)).encode("utf-8"))
    for pat, kind in (("t4", "info"), ("t3", "neutral"), ("t1", "neutral")):
        for cell in gen_text.text("probe", pat, kind, "probe", 0, 0, 240, 60, color="#FFFFFF"):
            h.update(cell.encode("utf-8"))
    return h.hexdigest()


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
        return (n[3], n[4], n[5], n[5])
    c = CONTAINERS[cid]
    return (c[2], c[3], c[4], c[5])


def caption_box(cid):
    """The caption under an icon (estimate, a little wider than drawn): centred, CAP_GAP below the glyph."""
    x, y, s, _ = abs_rect(cid)
    w = len(NODES[cid][0]) * CAP_CHAR_W + CAP_PAD
    return (x + s / 2.0 - w / 2.0, y + s + CAP_GAP, w, CAP_H)


def _parent_of(cid):
    return NODES[cid][2] if cid in NODES else CONTAINERS[cid][1]


def _rel(cid, x, y):
    p = _parent_of(cid)
    if p == "1":
        return x, y
    px, py, _, _ = abs_rect(p)
    return x - px, y - py


def wrap_label(text, wrap):
    """`\n` forces a break; each forced line is word-wrapped at `wrap` characters. -> list of lines.
    A step number never parts from its "·", nor from the word after it ("6 · one" stays on one line)."""
    out = []
    for part in str(text).split("\n"):
        words, units, i = part.split(" "), [], 0
        while i < len(words):
            w = words[i]
            i += 1
            while i < len(words) and words[i] == "·":       # "1 · 3 · static" is one unit
                w += " ·"
                i += 1
                if i < len(words):
                    w += " " + words[i]
                    i += 1
            units.append(w)
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


def _face(cid, pt):
    """Which wall of cid the point lies on: left | right | top | bottom (asserted to lie on one, not a corner)."""
    x, y, w, h = abs_rect(cid)
    on_x = pt[0] in (x, x + w) and y < pt[1] < y + h
    on_y = pt[1] in (y, y + h) and x < pt[0] < x + w
    assert on_x or on_y, "%s is not on a wall of %s (corners excluded)" % (pt, cid)
    if on_x:
        return "left" if pt[0] == x else "right"
    return "top" if pt[1] == y else "bottom"


def _ports(pair):
    """exit/entry fractions of a route's end points on their cells' walls."""
    a, _pts, b = ROUTES[pair]
    out = []
    for cid, pt in ((pair[0], a), (pair[1], b)):
        _face(cid, pt)
        x, y, w, h = abs_rect(cid)
        out.append((round((pt[0] - x) / float(w), 6), round((pt[1] - y) / float(h), 6)))
    return out


def _fmt(v):
    s = ("%.6f" % v).rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def _rect_hit(a, b, pad=0.0):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (ax - pad < bx + bw and bx < ax + aw + pad and ay - pad < by + bh and by < ay + ah + pad)


def _seg_hits_rect(p, q, r, pad=0.0):
    """True when the axis-aligned segment p-q comes within `pad` of the rect r (edges included)."""
    x0, x1 = min(p[0], q[0]), max(p[0], q[0])
    y0, y1 = min(p[1], q[1]), max(p[1], q[1])
    rx, ry, rw, rh = r
    return x0 <= rx + rw + pad and rx - pad <= x1 and y0 <= ry + rh + pad and ry - pad <= y1


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
            why.append("on icon %s" % cid)
        if _rect_hit(axis_box, caption_box(cid)):
            why.append("on the caption of %s" % cid)
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


def _check_captions(cables):
    """No cable comes within 4 px of a caption, and every caption sits inside its parent container."""
    bad = []
    for pair in cables:
        pts = path_of(pair)
        for cid in NODES:
            cb = caption_box(cid)
            for k in range(len(pts) - 1):
                if _seg_hits_rect(pts[k], pts[k + 1], cb, pad=4):
                    bad.append("%s -> %s touches the caption of %s" % (pair[0], pair[1], cid))
                    break
    for cid in NODES:
        cx, cy, cw, ch = caption_box(cid)
        px, py, pw, ph = abs_rect(_parent_of(cid))
        if cx < px + 4 or cy < py + 4 or cx + cw > px + pw - 4 or cy + ch > py + ph - 4:
            bad.append("the caption of %s leaves %s" % (cid, _parent_of(cid)))
    return bad


def _check_ports(cables):
    """Two cables of one page never share an end point on one face."""
    seen, bad = {}, []
    for pair in cables:
        a, _pts, b = ROUTES[pair]
        for cid, pt in ((pair[0], a), (pair[1], b)):
            key = (cid, pt)
            if key in seen and seen[key] != pair:
                bad.append("%s -> %s and %s -> %s share the port %s on %s" % (pair + seen[key] + (pt, cid)))
            seen[key] = pair
    return bad


def _statement_lines(text):
    return len(wrap_label(text, STATEMENT_CHARS))


# =================================================================================================== the page
def build_page(abbr, full_name, statements, states, cables, companions, out_path):
    """Write one micro-frontend page to `out_path` (a .drawio holding exactly one diagram). Data only:
    abbr        'CSR' ... 'RSC' (keys the label slides)
    full_name   the title after '<ABBR>: '
    statements  3 strings: where the HTML is produced; where and when the micro-frontends are composed; the trade-off
    states      {node id: 'active' | 'muted' | 'pivot'} for every node (never a group: a group is muted when all its
                members are)
    cables      [(n, from id, to id, 'net' | 'page' | 'build', label)]: n is the step number as a string, or '-' for a
                cable outside the numbered order; a numbered label starts with '<n> ·'; a label may hold '\\n'
    companions  6 file names
    Returns a dict of what was written (cells, cables, pivot, muted)."""
    if KIT_FINGERPRINT and kit_fingerprint() != KIT_FINGERPRINT:
        raise ValueError("mfe_frame.build_page(%s): the prompt master's 3-diagram kit now draws differently from the "
                         "kit this frame was proved on (KIT_FINGERPRINT). Prove the frame again: run the dry run on all "
                         "seven pages, both gates, look at every render, then set KIT_FINGERPRINT to "
                         "mfe_frame.kit_fingerprint() and record it in the contract's Frame proof." % abbr)
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
    for cid in NODES:
        st = states.get(cid)
        if st not in ("active", "muted", "pivot"):
            errors.append("%s: state %r (active, muted or pivot needed)" % (cid, st))
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
        if n != "-" and not str(label).startswith("%s ·" % n):
            errors.append("%s -> %s: step %s, but its label does not start with '%s ·'" % (a, b, n, n))
        if n == "-" and re.match(r"^\d+ ·", str(label)):
            errors.append("%s -> %s: an unnumbered cable whose label starts with a step number" % (a, b))
        if (a, b) in pairs:
            errors.append("%s -> %s drawn twice" % (a, b))
        pairs.append((a, b))
    if errors:
        raise ValueError("mfe_frame.build_page(%s):\n  " % abbr + "\n  ".join(errors))

    # ---------------------------------------------------------------- self-checks before writing
    problems = _check_titles(pairs) + _check_captions(pairs) + _check_ports(pairs)
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
        if _statement_lines(s) > STATEMENT_LINES:
            problems.append("statement S%d needs more than %d lines of %d characters"
                            % (k + 1, STATEMENT_LINES, STATEMENT_CHARS))
    if problems:
        raise ValueError("mfe_frame.build_page(%s) refused to write:\n  " % abbr + "\n  ".join(problems))

    # ---------------------------------------------------------------- cells
    cls_of = {}
    for cid, n in NODES.items():
        st = states[cid]
        cls_of[cid] = ("pivot" if st == "pivot" else "muted" if st == "muted" else
                       ("team-" + n[6]) if n[6] else "platform")
    group_muted = {g: all(states[c] == "muted" for c, n in NODES.items() if n[2] == g) for g in GROUPS}

    def container_xml(cid):
        title, parent, x, y, w, h, role = CONTAINERS[cid]
        has_frame_child = any(CONTAINERS[k][1] == cid for k in CONTAINERS)
        sw = 4 if (parent == "1" and has_frame_child) else 3
        tier = tier_of(cid)
        if tier is None:                                   # the legend: the standard's gray box
            fill, stroke, font = LEGEND_FILL, LEGEND_STROKE, TITLE_FONT
        else:
            tfill, stroke, font = TIERS[tier][:3]
            fill = GROUP_FILL if role == "group" else tfill
        st = ("swimlane;startSize=0;labelBorderColor=none;textShadow=1;labelBackgroundColor=default;rounded=0;html=1;"
              "fillColor=%s;swimlaneFillColor=%s;strokeColor=%s;strokeWidth=%d;fontColor=%s;fontSize=14;fontStyle=1;"
              "shadow=1;" % (fill, fill, stroke, sw, font))
        if tier == "build" and role == "column":            # outside the request path: the Optional row, dashed
            st += "dashed=1;"
        if role == "group" and group_muted.get(cid):
            st = st.replace("strokeColor=%s;" % stroke, "").replace("fontColor=%s;" % font, "") + MUTED_GROUP
        if role == "legend":
            st += "kitExempt=1;"
        rx, ry = _rel(cid, x, y)
        return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"><mxGeometry x="%d" y="%d" width="%d" '
                'height="%d" as="geometry"/></mxCell>' % (cid, gen_text.X(title), st, parent, rx, ry, w, h))

    def icon_xml(cid):
        name, art, parent, x, y, size, _team = NODES[cid]
        cls = cls_of[cid]
        fill, border, _kind = CLASSES[cls]
        kind, _, ref = art.partition(":")
        if kind == "craft":      # a crafted icon: one standalone SVG, an image cell (the craft kit's cell form)
            svg = craft_svg(ref, "i%s_" % re.sub(r"\W", "", cid), cid in HIGHLIGHT)
            head = ("shape=image;html=1;aspect=fixed;imageAspect=0;image=data:image/svg+xml,%s;"
                    % base64.b64encode(svg.encode("utf-8")).decode("ascii"))
        else:                    # a generic shape of PROMPT_ICON.md
            head = SHAPES[ref]
        st = ("%sverticalLabelPosition=bottom;verticalAlign=top;align=center;"
              "spacingTop=%d;fontSize=12;fontStyle=1;fontColor=%s;labelBackgroundColor=%s;labelBorderColor=%s;"
              "mfeClass=%s;" % (head, CAP_GAP, CAPTION_FONT, fill, border, cls))
        if cid in HIGHLIGHT:
            st += "mfeHub=1;"                              # the highlight marker (draw.io ignores the key; the checks read it)
        if cls == "muted":
            st += MUTED_KEYS
        rx, ry = _rel(cid, x, y)
        return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="%s"><mxGeometry x="%d" y="%d" width="%d" '
                'height="%d" as="geometry"/></mxCell>' % (cid, gen_text.X(_esc(name)), st, parent, rx, ry, size, size))

    body = []
    for cid in ORDER:
        body.append(container_xml(cid) if cid in CONTAINERS else icon_xml(cid))

    # legend (its rows are its children): two columns. Left: the areas (the Component Legend of PROMPT_ARROW_STYLE.md) and
    # the arrows (the Arrow Legend); right: the caption colours and the notes.
    lx, ly = CONTAINERS["C-LEGEND"][2], CONTAINERS["C-LEGEND"][3]
    body.append(container_xml("C-LEGEND"))
    HEAD = ROW.replace("fontSize=11;", "fontSize=12;fontStyle=1;")
    for cid_, text, xx in (("L-HEAD-AREAS", "Areas: a frame's colour says its tier", LEGEND_L),
                           ("L-HEAD-ARROWS", "Arrows", LEGEND_L),
                           ("L-HEAD-CAPTIONS", "Captions: a caption's colour says who owns the part", LEGEND_R),
                           ("L-HEAD-ICONS", "Icons: a framed icon is a highlight", LEGEND_L)):
        yy = {"L-HEAD-AREAS": 20, "L-HEAD-ARROWS": LEGEND_ARROWS_Y, "L-HEAD-CAPTIONS": 20, "L-HEAD-ICONS": LEGEND_ICONS_Y}[cid_]
        body.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" y="%d" '
                    'width="%d" height="20" as="geometry"/></mxCell>' % (cid_, gen_text.X(_esc(text)), HEAD, xx, yy,
                                                                          LEGEND_COL))
    for i, tier in enumerate(TIER_ORDER):
        tfill, tstroke, tfont, text = TIERS[tier]
        st = ("rounded=0;html=1;whiteSpace=wrap;fillColor=%s;strokeColor=%s;strokeWidth=2;fontColor=%s;fontSize=11;"
              "fontStyle=1;align=left;spacingLeft=10;verticalAlign=middle;kitExempt=1;%s"
              % (tfill, tstroke, tfont, "dashed=1;" if tier == "build" else ""))
        body.append('<mxCell id="L-AREA-%s" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" '
                    'y="%d" width="%d" height="30" as="geometry"/></mxCell>'
                    % (tier, gen_text.X(_esc(text)), st, LEGEND_L, 50 + i * 40, LEGEND_COL))
    for i, (cls, text) in enumerate(LEGEND_BADGES):
        fill, _border, kind = CLASSES[cls]
        out = gen_text.text("L-BADGE-%s" % cls, "t4", kind, _esc(text), LEGEND_R, 50 + i * 40, LEGEND_COL, 30,
                            color=fill)
        for s_ in out:
            s_ = s_.replace("shadow=1;", "shadow=0;")
            if cls == "muted":
                s_ = _style_add(s_, MUTED_KEYS)
            body.append(_reparent(_style_add(s_, "kitExempt=1;"), "C-LEGEND"))
    for i, (cls, text) in enumerate(LEGEND_SAMPLES):
        body.append('<mxCell id="L-CAPTION-%s" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" '
                    'y="%d" width="%d" height="40" as="geometry"/></mxCell>'
                    % (cls, gen_text.X(_esc(text)), ROW, LEGEND_L + 120, LEGEND_ARROWS_Y + 30 + i * 40,
                       LEGEND_COL - 120))
    hub_svg = craft_svg(LEGEND_HUB_ART, "ilegendhub_", True)      # the sample: the highlight style, as the hubs are drawn
    body.append('<mxCell id="L-HUB-SAMPLE" value="" style="shape=image;html=1;aspect=fixed;imageAspect=0;image=data:image/svg+xml,%s;'
                'kitExempt=1;" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" y="%d" width="40" height="40" as="geometry"/></mxCell>'
                % (base64.b64encode(hub_svg.encode("utf-8")).decode("ascii"), LEGEND_L, LEGEND_ICONS_Y + 30))
    body.append('<mxCell id="L-HUB-TEXT" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" y="%d" width="%d" '
                'height="40" as="geometry"/></mxCell>'
                % (gen_text.X(_esc(LEGEND_HUB_TEXT)), ROW, LEGEND_L + 50, LEGEND_ICONS_Y + 30, LEGEND_COL - 50))
    for i, (text, (yy, hh)) in enumerate(zip(LEGEND_LINES, LEGEND_NOTES)):
        body.append('<mxCell id="L-LINE-%d" value="%s" style="%s" vertex="1" parent="C-LEGEND"><mxGeometry x="%d" '
                    'y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
                    % (i + 1, gen_text.X(_esc(text)), ROW.replace("verticalAlign=middle", "verticalAlign=top"),
                       LEGEND_R, yy, LEGEND_COL, hh))

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
        y = ly + LEGEND_ARROWS_Y + 50 + i * 40
        edges.append('<mxCell id="L-SAMPLE-%s" value="" style="edgeStyle=none;rounded=0;html=1;%skitExempt=1;" '
                     'edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="%d" y="%d" '
                     'as="sourcePoint"/><mxPoint x="%d" y="%d" as="targetPoint"/></mxGeometry></mxCell>'
                     % (cls, EDGE_CLASSES[cls], lx + LEGEND_L, y, lx + LEGEND_L + 100, y))

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
    """Checks on the file itself: grid, one diagram, class markers, the icon form."""
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
                grid = 10 if str(c.get("id", "")).startswith("L-") else GRID      # the legend's rows: the 10-px grid
                assert float(v) % grid == 0, "%s %s=%s off the %d-px grid" % (c.get("id"), k, v, grid)
        for p in g.iter("mxPoint"):
            for k in ("x", "y"):
                assert float(p.get(k)) % GRID == 0, "%s point off the grid" % c.get("id")
    icons = [c for c in root.iter("mxCell") if "mfeClass=" in (c.get("style") or "")]
    assert len(icons) == len(NODES), "every content icon carries mfeClass (%d of %d)" % (len(icons), len(NODES))
    pivots = [c for c in icons if "mfeClass=pivot;" in c.get("style")]
    assert len(pivots) == 1, "exactly one mfeClass=pivot"
    hubs = sorted(c.get("id") for c in icons if "mfeHub=1;" in c.get("style"))
    assert hubs == sorted(HIGHLIGHT), "the highlighted icons are exactly %s, got %s" % (sorted(HIGHLIGHT), hubs)
    for c in icons:                                    # every crafted icon is the one its role gets: highlight or default
        m = re.search(r"image=data:image/svg\+xml,([^;]*);", c.get("style"))
        if not m:
            continue
        cid = c.get("id")
        want = craft_svg(NODES[cid][1].partition(":")[2], "i%s_" % re.sub(r"\W", "", cid), cid in HIGHLIGHT)
        assert base64.b64decode(m.group(1)).decode("utf-8") == want, \
            "%s: the crafted icon is not the %s one" % (cid, "highlight" if cid in HIGHLIGHT else "default")
    for c in icons:
        st = c.get("style")
        assert "verticalLabelPosition=bottom;" in st, "%s: an icon with its caption under it" % c.get("id")
        assert "whiteSpace=wrap" not in st, "%s: a caption, never a wrapped card label" % c.get("id")
        assert "<br>" not in (c.get("value") or ""), "%s: a caption is one line, no subtitle" % c.get("id")
        if "mfeClass=muted;" in st:
            assert MUTED_KEYS in st, "%s: a muted icon is faded (%s)" % (c.get("id"), MUTED_KEYS)
