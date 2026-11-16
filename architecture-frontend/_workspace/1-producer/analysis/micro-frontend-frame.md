# Micro-frontend frame — the contract

> The one page layout that the seven micro-frontend diagrams of this library (slots 001 to 007: CSR, SPA, MPA, SSR,
> SSG, ISR, RSC) are drawn from, so that they compare node for node and only the composition point moves.
> **Status: frozen** (T-001, 2026-11-16, after the dry run below met the bar on all seven pages). A later need is a new
> ticket that redraws the affected slots under the library's storage policy; T-002 to T-007 use the frame as it is.

**Implemented by** `../script/_lib/mfe_frame.py` (`build_page`, every coordinate, style, port, waypoint, wrap and slide
below) and `../script/_lib/render_png.py` (`render`). The tables of this contract were generated from `mfe_frame.py`'s
own data at the dry run, so the two agree; when they ever disagree, the code is what was proved, and the difference is a
defect to fix here.

**Environment** (never written into a committed file): `DIAGRAM_KIT` = the prompt master's `shared/prompts/3-diagram`
folder; `mfe_frame` exits with `DIAGRAM_KIT must point to the prompt master's shared/prompts/3-diagram` when it is unset
or wrong, before anything is written. The render helper finds the browser and the draw.io viewer at run time (§ Render
helper).

## Page and spacing

- **Page:** 3060 x 1680. All geometry (cells, ports, waypoints) is in multiples of 20 (`PROMPT_OBJECT.md` mod-10 rule,
  kept stricter here). The kit's own chrome (a flat T1's fold, a T3's notches) keeps the kit's offsets.
- **Streets** (horizontal free space between bands), 100 px each, so a street carries labels
  (`PROMPT_LAYOUT_PATTERN.md` § 3 asks 80):
  - the **top street**, between the statement cards and the columns: y 220 to 320 (its cables run at y 260);
  - the **band street**, between the columns and the build band: y 1040 to 1140.
- **Gutters** (vertical free space between columns):
  - **Browser–Edge: x 840 to 1120, 280 px** (widened from the planned 200 by the dry run: MPA cable 1's 3-line label at
    a 34-character wrap needs about 210 px plus 20 clear on each side); its cables run at x 980;
  - Edge–Origin: x 1460 to 1660, 200 px; its cables run at x 1560 (and ISR cable 0 at x 1520);
  - Origin–Backend: x 2360 to 2560, 200 px.
- **The east lane:** x 2900 to 3020, east of the Backend column; its cables run at x 2960.
- **The free space west of the band** (x 840 to 1120, below y 1040): its cables run at x 1080.
- **Container titles.** Every container is `swimlane;startSize=0`; its title (font 14, bold) is centred on its top wall
  and reaches about 12 px above and below it. The frame computes each title's box (about 8.2 px a character plus 16, 24
  high) and refuses a cable that touches one. Spans on the top walls that cables cross: G-REMOTES x 325 to 555 (y 680);
  G-SERVERS x 1953 to 2067 (y 680); C-ORIGIN x 1936 to 2084 (y 320); C-BUILD x 1605 to 1875 (y 1140); G-CI x 1945 to
  2075 (y 1180).
- **Insets:** a card sits at least 40 px below its container's top wall; a group at least 40 px below its column's top,
  so two titles never stack; a group's members 40 px below its top wall and at least 20 px from its sides.
- **Row gaps:** 80 px inside a column; 40 px inside a group whose members have no cables between them.

## Placement

- **Plan:** ROAD (`PROMPT_CITY_PLAN_LAYOUT.md` § *Scope*, cloud architecture). The order axis is the request path, left
  to right (Browser, Edge, Origin, Backend); the build band sits below Edge and Origin. No `--centre` is asserted (a ROAD
  page has no downtown); `check_layout.py`'s info line reports the content centre in the Edge–Origin gutter, which is
  expected for this plan.
- **Coordinates** below are absolute page positions. A child is written relative to its container
  (`PROMPT_CONTAINER.md` § *Coordinate System*): the frame passes the kit the relative position and replaces the kit's
  single `parent="1"` with the container id, asserting exactly one replacement (as `_overview_lib.py` `card()` does).
- **Z-order:** containers with their children first (depth first), then the cables, then the page furniture.

## Containers

All are `swimlane;startSize=0;labelBorderColor=none;textShadow=1;labelBackgroundColor=default;rounded=0;html=1;`
with `fillColor` = `swimlaneFillColor`, `fontSize=14;fontStyle=1;fontColor=#37474F;shadow=1`
(`PROMPT_CONTAINER.md` § *Default Group/Container Style*).
- **Stroke width** (§ *Border Width Hierarchy*, T-232): 4 = a frame on the page holding another frame; 3 = every other
  frame, a frame on its own included; 2 = a leaf. Content cards carry no strokeWidth of their own.
- **Fills and strokes are cool and neutral only:** columns, the band and the legend `#FFFFFF` / `#5F6B7A`; groups
  `#F4F6F9` / `#8A97A8`. None comes from `PROMPT_ARROW_STYLE.md`'s Integration row and none is warm.
- **A muted group** (every member muted) keeps its swimlane and strokeWidth 3, with `strokeColor=#BDBDBD`,
  `fontColor=#9E9E9E`, `opacity=45`. A group never takes a state of its own.
- **C-LEGEND** carries `kitExempt=1` (page furniture); its rows are its children.

| id | title | in | x,y,w,h (absolute) | strokeWidth | fill / stroke |
|---|---|---|---|---|---|
| C-BROWSER | Browser (one page at run time) | page | 40,320,800,720 | 4 | #FFFFFF / #5F6B7A |
| G-REMOTES | Team UIs (micro-frontends) | C-BROWSER | 60,680,760,160 | 3 | #F4F6F9 / #8A97A8 |
| C-EDGE | Edge (CDN and proxy) | page | 1120,320,340,720 | 3 | #FFFFFF / #5F6B7A |
| C-ORIGIN | Origin (servers) | page | 1660,320,700,720 | 4 | #FFFFFF / #5F6B7A |
| G-SERVERS | Team servers | C-ORIGIN | 1680,680,660,160 | 3 | #F4F6F9 / #8A97A8 |
| C-BACKEND | Backend (APIs and content) | page | 2560,320,340,720 | 4 | #FFFFFF / #5F6B7A |
| G-APIS | Team APIs | C-BACKEND | 2580,360,300,400 | 3 | #F4F6F9 / #8A97A8 |
| C-BUILD | Build time (before any request) | page | 1120,1140,1240,360 | 4 | #FFFFFF / #5F6B7A |
| G-CI | Team pipelines | C-BUILD | 1680,1180,660,160 | 3 | #F4F6F9 / #8A97A8 |
| C-LEGEND | Legend | page | 40,1140,800,400 | 3 | #FFFFFF / #5F6B7A |

## Nodes

- **Form:** every content node is one text-kit **T1 clay card with an icon**, a single composite cell:
  `gen_text.text(id, "t1", <kind>, label, x, y, w, h, color=<fill>, style="clay", icon=<key>, font_size=<fs>)`.
- **Label:** `<b>NAME</b><br>subtitle`. The NAME never changes between diagrams; each diagram ticket gives the subtitle.
- **Font:** 12 on cards 220 px wide or more, 11 on 180-wide cards. The frame refuses a subtitle its estimate says
  overflows the card (at most 4 lines of text on an 80-high card); the render is the real check.
- **Marker:** each card's style also carries `mfeClass=<class>` (draw.io ignores the unknown key; the checks read it).
- **Why this placement:** every cable that stays inside one container is one straight segment, so the pairs that
  connect inside a container share an x- or y-span: B-PAGE (x 220 to 640) overlaps B-ROUTER (80 to 260) and B-SHELL
  (600 to 780), with the corridor x 260 to 600 between them for B-PAGE → G-REMOTES (at x 580, east of G-REMOTES' title);
  O-BFF overlaps O-COMPOSER's x-span (1920 to 2040); the left half of Origin row 2 (x 1700 to 1880) stays empty for
  O-COMPOSER → G-SERVERS and the cables that enter from the west; D-REGISTRY shares G-CI's row and D-INTEGRATION sits
  below it, offset east, so D-REGISTRY → D-INTEGRATION (x 1360), D-REGISTRY → E-CDN (x 1280) and G-CI → D-REGISTRY
  (y 1260) are straight. On a page that draws G-CI → D-REGISTRY, no cable rises out of D-INTEGRATION's top except
  D-REGISTRY → D-INTEGRATION's arrival: its cables leave by its west or east wall.

| id | NAME | icon (CLAY_DEMO key) | in | x,y,w,h (absolute) | font | class when active |
|---|---|---|---|---|---|---|
| B-PAGE | Browser tab | client-browser | C-BROWSER | 220,360,420,80 | 12 | platform |
| B-ROUTER | Client router | page-route | C-BROWSER | 80,520,180,80 | 11 | platform |
| B-SHELL | App shell | webapp | C-BROWSER | 600,520,180,80 | 11 | platform |
| B-UI-A | Team A · Catalog UI | ui-component | G-REMOTES | 100,720,180,80 | 11 | team-a |
| B-UI-B | Team B · Cart UI | ui-component | G-REMOTES | 340,720,180,80 | 11 | team-b |
| B-UI-C | Team C · Account UI | ui-component | G-REMOTES | 580,720,180,80 | 11 | team-c |
| B-BUS | Event bus | event-stream | C-BROWSER | 80,920,400,80 | 12 | platform |
| B-SHARED | Shared libraries | module-package | C-BROWSER | 520,920,280,80 | 12 | platform |
| E-ROUTER | Edge router | load-balancer | C-EDGE | 1160,360,260,80 | 12 | platform |
| E-CACHE | Page cache | cache | C-EDGE | 1160,520,260,80 | 12 | platform |
| E-CDN | CDN | cdn | C-EDGE | 1160,920,260,80 | 12 | platform |
| O-COMPOSER | Page composer | service | C-ORIGIN | 1700,360,340,80 | 12 | platform |
| O-BFF | BFF | api-gateway | C-ORIGIN | 1920,520,400,80 | 12 | platform |
| O-SRV-A | Team A server | service | G-SERVERS | 1700,720,180,80 | 11 | team-a |
| O-SRV-B | Team B server | service | G-SERVERS | 1920,720,180,80 | 11 | team-b |
| O-SRV-C | Team C server | service | G-SERVERS | 2140,720,180,80 | 11 | team-c |
| K-API-A | Catalog API (team A) | microservice | G-APIS | 2600,400,260,80 | 12 | team-a |
| K-API-B | Order API (team B) | microservice | G-APIS | 2600,520,260,80 | 12 | team-b |
| K-API-C | Account API (team C) | microservice | G-APIS | 2600,640,260,80 | 12 | team-c |
| K-CMS | Headless CMS | docs-multi | C-BACKEND | 2600,920,260,80 | 12 | platform |
| D-REGISTRY | Registry | registry | C-BUILD | 1160,1220,220,80 | 12 | platform |
| D-INTEGRATION | Integration build | ci-pipeline | C-BUILD | 1320,1380,260,80 | 12 | platform |
| D-CI-A | Team A pipeline | ci-pipeline | G-CI | 1700,1220,180,80 | 11 | team-a |
| D-CI-B | Team B pipeline | ci-pipeline | G-CI | 1920,1220,180,80 | 11 | team-b |
| D-CI-C | Team C pipeline | ci-pipeline | G-CI | 2140,1220,180,80 | 11 | team-c |

## Page furniture

Every furniture cell carries `kitExempt=1`, appended to each cell the kit returns (a caption, a legend row and a title
are not content nodes; this is how `_overview_lib.py` treats its legend, rows and captions, and it keeps them out of
`check_layout.py`'s centrality box).
- **Title:** a T3 flat banner (kind `neutral`) at 40,20,2980,60: `Micro-frontends with <ABBR>: <full name>`.
- **Statement cards:** three T1 flat cards (kind `neutral`, `color=#FFFFFF`, a fill no class uses), 940 x 120 at
  y 100: S1 at x 40, S2 at x 1060, S3 at x 2080 (80 px apart, so S3 ends on the title's right edge). Label
  `<b>heading</b><br>statement`, font 12. Headings: S1 `Where the HTML is produced`, S2 `Where and when the
  micro-frontends are composed`, S3 `Trade-off for micro-frontends`.
  **Capacity: the heading plus 5 lines of about 130 characters (about 650 characters).** The frame refuses a statement
  that needs more; the dry run proved all 21 statements fit (the longest, ISR S3, needs 5 lines at the 130-character estimate, the
  limit; drawn at font 12 it takes 3).
- **Companions:** a T1 flat card (kind `neutral`, `color=#FFFFFF`) at 40,1580,2980,60:
  `<b>Companions (same frame):</b>` followed by the other six file names, each
  `00N-micro-frontend-<x>/micro-frontend-<x>-architecture.drawio`, joined by ` · `.
- **Legend:** § Legend.

## Colour classes

Each class is a kit **kind** plus a `color=` fill override, its style keys, and the `mfeClass` marker. The T1 clay card
is one stencil cell (`gen_icons.style_p3_box`): its body takes the fill, its fold takes the kind's own tonal edge colour
(`gen_text.CLAY_PALETTE`), and its style says `strokeColor=none;shadow=1;`. So a class has no stroke colour and no
strokeWidth: stroke width belongs to the topology (`PROMPT_CITY_PLAN_LAYOUT.md` § *Channel collisions*).
**#FFF2CC is the only warm fill on the page**, so the pivot is found by its colour.

| class | kit kind + color= + style keys (replacing the kit's `shadow=1;`) | used for |
|---|---|---|
| team-a | `info`, #DAE8FC, `shadow=0;` | B-UI-A, O-SRV-A, K-API-A, D-CI-A |
| team-b | `success`, #D5E8D4, `shadow=0;` | B-UI-B, O-SRV-B, K-API-B, D-CI-B |
| team-c | `accent`, #E1D5E7, `shadow=0;` | B-UI-C, O-SRV-C, K-API-C, D-CI-C |
| platform | `neutral`, #CFD8DC, `shadow=0;` | every other node (shared or platform-owned) |
| pivot | `note`, #FFF2CC, `shadow=1;` | the one composition point of the page (replaces its class) |
| muted | `neutral`, #F5F5F5, `shadow=0;opacity=45;textOpacity=60;opacityGroup=1;` | a node this approach does not use; subtitle `not used in <ABBR>` unless the ticket gives another |

- **The shadow key is replaced, never appended:** the kit emits `shadow=1;` once on every card, and the frame replaces
  it with the class's keys, so each card's style holds exactly one `shadow=` key (asserted before writing).
- **Why `opacityGroup=1` is required:** `gen_icons` writes `<alpha alpha="1"/>` before every stencil primitive, and
  draw.io's stencil `alpha` replaces the cell's opacity instead of multiplying it, so `opacity` alone fades only the
  text. With `opacityGroup=1` the viewer draws the whole shape in one group at 45 % (`mxShape.isOpacityGroup` in the
  draw.io viewer). **Proved in the dry-run renders:** every muted card, its icon and fold included, reads faded.
- **The pivot's channels** (`PROMPT_CITY_PLAN_LAYOUT.md`: a ROAD pivot takes cross-axis position, size, frame,
  elevation and fill):
  - **fill is the working channel:** #FFF2CC, the only warm fill on the page;
  - **elevation is weak:** every clay card bakes a 4-px stencil shadow (`gen_icons.style_p3_box`: a #000000 alpha-0.18
    copy offset 4 px down), so the pivot's cell `shadow=1` is a faint extra (visible in the renders as a soft outer
    shadow); draw order is not visible because no cards overlap;
  - **frame by colour is nominal:** the `note` kind's amber tonal edge shows only on the 18 px fold.
- **Not used, on purpose (an honest limit):** cross-axis position and size stay fixed so the seven pages compare node for
  node, and stroke width belongs to the topology. The pivot is found by its fill; the checks rest on the fill and the
  style keys, never on elevation.
- **The same across all seven:** `build_page` applies all of this to whichever node a page names as the pivot.

## Edge classes and numbering

Every content cable: `edgeStyle=none;rounded=0;html=1;` (straight segments through explicit waypoints,
`PROMPT_ARROW_STYLE.md` § *Straight lines*), explicit `exitX/exitY/entryX/entryY` with zero `Dx/Dy`, the class style
below, and the label style `fontSize=11;fontColor=#232F3E;labelBackgroundColor=#FFFFFF;`. Every content cable sits on
`parent="1"`.

| class | style | meaning |
|---|---|---|
| net | solid #232F3E, strokeWidth 2, `endArrow=block;endFill=1` | a network request at run time; arrow = request direction, the label says what comes back |
| page | dotted (`dashed=1;dashPattern=1 3`) #232F3E, strokeWidth 2, `endArrow=open;endFill=0` | a call inside the page (no network) |
| build | dashed (`dashed=1;dashPattern=6 4`) #616161, strokeWidth 2, `endArrow=block;endFill=1` | build or deploy, before any request |

- **Numbering:** the steps of the flow a page draws are numbered in order, `1 ·`, `2 ·`. Build steps a ticket numbers
  come first (SSG 1 to 4, ISR 0). One cable may carry two step numbers (a request and its later response, or two
  requests to the same place), and one step may show on two cables (CSR's step 3). An unnumbered cable stands outside
  that order: a build or deploy link, a standing link, or a separate trigger (ISR's CMS publish).
- **Endpoints:** a cable may end on a group (G-REMOTES, G-SERVERS, G-APIS, G-CI): one cable stands for the three teams.

## Labels

Font 11. The frame estimates a label at 6.0 px a character and 13.2 px a line (a little wider than drawn, on purpose).
- **Wrap:** 24 characters a line by default; the routing table sets a per-page wrap (up to 34) where a label fits
  better or only fits that way. Words wrap whole, and **a step number never parts from its `·`** (`7 ·` stays together).
- **Forced line break:** a ticket writes `\n`; the frame turns it into `<br>` and wraps each line on its own.
- **Height:** at most 3 lines on a horizontal run, at most 5 on a vertical run.
- **Clearance (checked by the frame before it writes; it refuses the page otherwise):** a label sits on a run at least
  its own extent plus 40 px long (20 clear before and after it along the run), and its box, 6 px around, touches no
  card, no container wall, no container title, no page furniture, no other cable and no other label.
- **Slide:** the label's centre is a point on its route; the frame turns it into the edge geometry `x` (the
  `lp` of `_overview_lib.cable()`: -1 at the source end, 1 at the target end).

## Routing rule

Every gate finding counts, not just the exit code.
- **No bend inside a rectangle.** `check_layout.py` reports WAYPOINT-IN for a waypoint inside any node or container
  rectangle, the cable's own column, group or band included, and it fails in every profile. A cable that leaves its own
  container and comes back in is RE-ENTRY (fails the report profile). So **every bend sits in free space**: a street, a
  gutter, the east lane, or the free space west, south and east of the build band.
- **Inside a container a cable is one straight segment:** port to port, or port to the container's wall, between cards
  that share an x- or y-span, with no card in the way.
- **No cable through a title:** no cable touches a container's title box (the frame checks every segment).
- **Ports:** explicit fractions on the cell's wall, asserted to lie on it; two cables on one face never share a port.
- **The routing table** keeps the route (ports and waypoints) per `(from_id, to_id)` pair, and the label slide and wrap
  per `(abbr, from_id, to_id)`, because one pair carries labels of different lengths on different pages. An unknown pair,
  or a label with no slide for its page, raises an error and is never auto-routed.

## Adjacency invariant

A run-time cable joins adjacent columns, or stays inside one container as one straight segment, or runs in a street, a
gutter or the east lane outside every column. A build cable runs straight up from the build band to the column directly
above it, or leaves the band and bends only in free space. No cable crosses a third party's container (WALL-CUT, hard in
both profiles), puts a bend inside a rectangle (WAYPOINT-IN), leaves and re-enters its own container (RE-ENTRY), or runs
through a container title. Browser network traffic leaves from B-PAGE only; HTML rendered at request time (or served
from the page cache) and API requests go to E-ROUTER; static files, prebuilt HTML included (CSR's and SPA's index.html,
SSG's pages), go to E-CDN.

## Routing table

### Routes

Absolute points; the exit point lies on the source's wall and the entry point on the target's.

| from → to | exit (x, y) | waypoints | entry (x, y) | exitX,exitY → entryX,entryY | drawn on |
|---|---|---|---|---|---|
| B-PAGE → E-ROUTER | 640,380 | none (straight) | 1160,380 | 1,0.25 → 0,0.25 | CSR, SPA, MPA, SSR, SSG, ISR, RSC |
| B-PAGE → E-CDN | 640,420 | 980,420 · 980,940 | 1160,940 | 1,0.75 → 0,0.25 | CSR, SPA, MPA, SSR, SSG, ISR, RSC |
| B-PAGE → B-SHELL | 620,440 | none (straight) | 620,520 | 0.952381,1 → 0.111111,0 | CSR |
| B-PAGE → B-ROUTER | 240,440 | none (straight) | 240,520 | 0.047619,1 → 0.888889,0 | SPA |
| B-PAGE → G-REMOTES | 580,440 | none (straight) | 580,680 | 0.857143,1 → 0.684211,0 | SSR, SSG, RSC |
| B-SHELL → G-REMOTES | 700,600 | none (straight) | 700,680 | 0.555556,1 → 0.842105,0 | CSR |
| B-ROUTER → G-REMOTES | 160,600 | none (straight) | 160,680 | 0.444444,1 → 0.131579,0 | SPA |
| B-SHELL → B-ROUTER | 600,560 | none (straight) | 260,560 | 0,0.5 → 1,0.5 | SPA |
| G-REMOTES → B-BUS | 280,840 | none (straight) | 280,920 | 0.289474,1 → 0.5,0 | SPA |
| E-ROUTER → O-BFF | 1420,420 | 1560,420 · 1560,560 | 1920,560 | 1,0.75 → 0,0.5 | CSR, SPA, SSG |
| E-ROUTER → G-SERVERS | 1420,420 | 1560,420 · 1560,760 | 1680,760 | 1,0.75 → 0,0.5 | MPA |
| E-ROUTER → O-COMPOSER | 1420,400 | none (straight) | 1700,400 | 1,0.5 → 0,0.5 | SSR, RSC |
| E-ROUTER → E-CACHE | 1280,440 | none (straight) | 1280,520 | 0.461538,1 → 0.461538,0 | ISR |
| E-CACHE → O-COMPOSER | 1420,540 | 1560,540 · 1560,380 | 1700,380 | 1,0.25 → 0,0.25 | ISR |
| O-BFF → G-APIS | 2320,560 | none (straight) | 2580,560 | 1,0.5 → 0,0.5 | CSR, SPA, MPA, SSR, ISR, RSC |
| O-BFF → K-API-B | 2320,560 | none (straight) | 2600,560 | 1,0.5 → 0,0.5 | SSG |
| O-COMPOSER → O-BFF | 1980,440 | none (straight) | 1980,520 | 0.823529,1 → 0.15,0 | RSC |
| O-COMPOSER → G-SERVERS | 1780,440 | none (straight) | 1780,680 | 0.235294,1 → 0.151515,0 | SSR, ISR |
| G-SERVERS → O-BFF | 2180,680 | none (straight) | 2180,600 | 0.757576,0 → 0.65,1 | MPA, SSR, ISR |
| K-CMS → O-COMPOSER | 2860,960 | 2960,960 · 2960,260 · 1840,260 | 1840,360 | 1,0.5 → 0.411765,0 | ISR |
| G-CI → E-CDN | 1680,1320 | 1080,1320 · 1080,980 | 1160,980 | 0,0.875 → 0,0.75 | CSR, SPA, MPA, SSR |
| G-CI → D-REGISTRY | 1680,1260 | none (straight) | 1380,1260 | 0,0.5 → 1,0.5 | CSR, SPA, SSG, RSC |
| D-REGISTRY → E-CDN | 1280,1220 | none (straight) | 1280,1000 | 0.545455,0 → 0.461538,1 | CSR, SPA |
| G-CI → G-SERVERS | 2240,1180 | none (straight) | 2240,840 | 0.848485,0 → 0.848485,1 | MPA, SSR, ISR |
| D-REGISTRY → D-INTEGRATION | 1360,1300 | none (straight) | 1360,1380 | 0.909091,1 → 0.153846,0 | SSG, RSC |
| D-INTEGRATION → K-CMS | 1580,1400 | 2720,1400 | 2720,1000 | 1,0.25 → 0.461538,1 | SSG |
| D-INTEGRATION → K-API-A | 1580,1440 | 2960,1440 · 2960,440 | 2860,440 | 1,0.75 → 1,0.5 | SSG |
| D-INTEGRATION → E-CDN | 1320,1420 | 1080,1420 · 1080,980 | 1160,980 | 0,0.5 → 0,0.75 | SSG |
| D-INTEGRATION → E-CACHE | 1520,1380 | 1520,580 | 1420,580 | 0.769231,0 → 1,0.75 | ISR |
| D-INTEGRATION → O-COMPOSER | 1580,1420 | 2960,1420 · 2960,260 · 1840,260 | 1840,360 | 1,0.5 → 0.411765,0 | RSC |

**Moved from the plan's starting routes by the dry run** (recorded in § Paper check): every column, the band and the
east lane east of the Browser–Edge gutter moved 80 px east with the gutter's widening; ports and bends were put on the
20-px grid (the corridor at x 580, B-ROUTER → G-REMOTES at x 160, E-ROUTER → E-CACHE at x 1280, D-INTEGRATION → K-CMS at
x 2720, the top street at y 260, E-CDN's west entries at y 940 and 980).

### Label slides and wraps

`centre` is the label's centre on its route; `slide` is the edge geometry `x` the frame writes; `lines` is the drawn
line count at that wrap.

| page | from → to | wrap | centre (x, y) | slide (edge x) | lines |
|---|---|---|---|---|---|
| CSR | B-PAGE → E-CDN | 30 | 980,680 | 0.1538 | 3 |
| CSR | B-PAGE → B-SHELL | 24 | 620,480 | 0 | 1 |
| CSR | B-SHELL → G-REMOTES | 24 | 700,640 | 0 | 2 |
| CSR | B-PAGE → E-ROUTER | 24 | 980,380 | 0.3077 | 2 |
| CSR | E-ROUTER → O-BFF | 26 | 1800,560 | 0.625 | 1 |
| CSR | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| CSR | G-CI → E-CDN | 24 | 1530,1320 | -0.7059 | 2 |
| CSR | G-CI → D-REGISTRY | 26 | 1520,1260 | 0.0667 | 1 |
| CSR | D-REGISTRY → E-CDN | 24 | 1280,1090 | 0.1818 | 1 |
| SPA | B-PAGE → B-ROUTER | 28 | 240,480 | 0 | 2 |
| SPA | B-PAGE → E-CDN | 24 | 980,680 | 0.1538 | 2 |
| SPA | B-ROUTER → G-REMOTES | 24 | 160,640 | 0 | 2 |
| SPA | B-PAGE → E-ROUTER | 24 | 980,380 | 0.3077 | 2 |
| SPA | E-ROUTER → O-BFF | 26 | 1800,560 | 0.625 | 1 |
| SPA | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| SPA | G-REMOTES → B-BUS | 24 | 280,880 | 0 | 2 |
| SPA | B-SHELL → B-ROUTER | 24 | 430,560 | 0 | 1 |
| SPA | G-CI → E-CDN | 24 | 1530,1320 | -0.7059 | 2 |
| SPA | G-CI → D-REGISTRY | 26 | 1520,1260 | 0.0667 | 1 |
| SPA | D-REGISTRY → E-CDN | 24 | 1280,1090 | 0.1818 | 1 |
| MPA | B-PAGE → E-ROUTER | 34 | 980,380 | 0.3077 | 3 |
| MPA | E-ROUTER → G-SERVERS | 24 | 1560,590 | 0.0333 | 2 |
| MPA | G-SERVERS → O-BFF | 24 | 2180,640 | 0 | 2 |
| MPA | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| MPA | B-PAGE → E-CDN | 30 | 980,690 | 0.1731 | 1 |
| MPA | G-CI → G-SERVERS | 24 | 2240,940 | 0.4118 | 2 |
| MPA | G-CI → E-CDN | 24 | 1530,1320 | -0.7059 | 1 |
| SSR | B-PAGE → E-ROUTER | 24 | 980,380 | 0.3077 | 1 |
| SSR | E-ROUTER → O-COMPOSER | 24 | 1560,400 | 0 | 2 |
| SSR | O-COMPOSER → G-SERVERS | 30 | 1780,560 | 0 | 2 |
| SSR | G-SERVERS → O-BFF | 24 | 2180,640 | 0 | 2 |
| SSR | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| SSR | B-PAGE → E-CDN | 26 | 980,680 | 0.1538 | 1 |
| SSR | B-PAGE → G-REMOTES | 24 | 580,480 | -0.6667 | 2 |
| SSR | G-CI → G-SERVERS | 24 | 2240,940 | 0.4118 | 2 |
| SSR | G-CI → E-CDN | 26 | 1530,1320 | -0.7059 | 1 |
| SSG | G-CI → D-REGISTRY | 24 | 1520,1260 | 0.0667 | 2 |
| SSG | D-REGISTRY → D-INTEGRATION | 24 | 1360,1340 | 0 | 2 |
| SSG | D-INTEGRATION → K-CMS | 24 | 2720,1230 | 0.7013 | 2 |
| SSG | D-INTEGRATION → K-API-A | 24 | 2960,1250 | 0.2661 | 2 |
| SSG | D-INTEGRATION → E-CDN | 24 | 1230,1420 | -0.7632 | 2 |
| SSG | B-PAGE → E-CDN | 24 | 980,680 | 0.1538 | 2 |
| SSG | B-PAGE → G-REMOTES | 28 | 580,480 | -0.6667 | 2 |
| SSG | B-PAGE → E-ROUTER | 28 | 980,380 | 0.3077 | 2 |
| SSG | E-ROUTER → O-BFF | 26 | 1800,560 | 0.625 | 1 |
| SSG | O-BFF → K-API-B | 24 | 2460,560 | 0 | 2 |
| ISR | D-INTEGRATION → E-CACHE | 26 | 1520,1280 | -0.7778 | 2 |
| ISR | B-PAGE → E-ROUTER | 24 | 980,380 | 0.3077 | 1 |
| ISR | E-ROUTER → E-CACHE | 24 | 1280,480 | 0 | 2 |
| ISR | E-CACHE → O-COMPOSER | 30 | 1560,460 | 0 | 4 |
| ISR | O-COMPOSER → G-SERVERS | 26 | 1780,550 | -0.0833 | 2 |
| ISR | G-SERVERS → O-BFF | 24 | 2180,630 | 0.25 | 1 |
| ISR | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| ISR | K-CMS → O-COMPOSER | 28 | 2400,260 | 0.3465 | 3 |
| ISR | B-PAGE → E-CDN | 26 | 980,680 | 0.1538 | 2 |
| ISR | G-CI → G-SERVERS | 30 | 2240,940 | 0.4118 | 3 |
| RSC | G-CI → D-REGISTRY | 24 | 1520,1260 | 0.0667 | 2 |
| RSC | D-REGISTRY → D-INTEGRATION | 24 | 1360,1340 | 0 | 2 |
| RSC | D-INTEGRATION → O-COMPOSER | 24 | 1960,1420 | -0.7979 | 1 |
| RSC | B-PAGE → E-ROUTER | 28 | 980,380 | 0.3077 | 2 |
| RSC | E-ROUTER → O-COMPOSER | 24 | 1560,400 | 0 | 2 |
| RSC | O-COMPOSER → O-BFF | 24 | 1980,480 | 0 | 2 |
| RSC | O-BFF → G-APIS | 24 | 2460,560 | 0.0769 | 2 |
| RSC | B-PAGE → E-CDN | 24 | 980,680 | 0.1538 | 2 |
| RSC | B-PAGE → G-REMOTES | 32 | 580,480 | -0.6667 | 2 |

## Paper check

Each page's cables, checked against the gate's rules before building and then by the gate itself in the dry run:
0 WAYPOINT-IN, 0 RE-ENTRY, 0 WALL-CUT, 0 CUTS-NODE, 0 CROSS and 0 COLLINEAR on each of the seven pages.
- **CSR:** 1 · 2 · 3 · 4 · 5 · 6 and the three build cables (G-CI → E-CDN west of the band, G-CI → D-REGISTRY,
  D-REGISTRY → E-CDN).
- **SPA:** 1 to 7, B-SHELL → B-ROUTER, and the three build cables.
- **MPA:** 1 to 5, and G-CI → G-SERVERS and G-CI → E-CDN.
- **SSR:** 1 to 8 (step 6 rides on cable 2), and the two build cables.
- **SSG:** 1 to 9 and the product-data cable, with D-INTEGRATION's west route to E-CDN and its east routes to K-CMS and
  K-API-A (the K-API-A route turns further east, so the two never cross).
- **ISR:** 0 to 7, the CDN cable, the K-CMS trigger by the east lane and the top street, and G-CI → G-SERVERS. Cable 0
  rises at x 1520 and cable 3 turns at x 1560, 40 px apart, and cable 3 leaves E-CACHE above cable 0's arrival.
- **RSC:** 1 to 7 and the three build cables, with D-INTEGRATION → O-COMPOSER by the east lane and the top street.

Routes moved from the plan: the Browser–Edge gutter widened to 280 px (all routes east of it shifted 80 px), and the
grid snaps listed under § Routes. No route changed its shape.

## Legend

C-LEGEND, titled `Legend`, at 40,1140,800,400 (taller than planned, 360 → 400, so its two fixed lines fit); every row is
its child and carries `kitExempt=1`.
- **Badges:** one **flat** T4 badge per colour class (240 x 40, three to a row), its class fill and style keys
  (the muted badge carries the muted keys too), labelled `Team A · Catalog`, `Team B · Cart and orders`,
  `Team C · Account`, `Shared or platform-owned`, `Where the micro-frontends are composed (the pivot)`,
  `Not used in this approach`. A flat badge shows the class fill exactly; a clay T4 would add a gradient and a white rim.
- **Sample cables:** one per edge class, the class style verbatim, with free source and target points (so the gate
  excludes them as UNVERIFIABLE, and they are the only excluded edges), captioned `Network request at run time: the
  arrow is the request, the label says what comes back`, `Call inside the page (no network)`, `Build or deploy, before
  any request`.
- **The two fixed lines:**
  - `Numbers = the order of the steps of the flow drawn; numbered dashed steps are build steps and come before any request; an unnumbered cable stands outside that order (a build or deploy link, a standing link, or a separate trigger) · yellow = where the micro-frontends are composed`
  - `BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), drawn where this example uses them; the headless CMS is a data source, not a BFF.`

## Frame-static text

The text the frame fixes, the same on all seven pages. A slot's page-text table covers its content nodes and content
cables only; everything here is sourced once, in this table (`frame-static` in a slot's table points here).

| text | where | source |
|---|---|---|
| `Micro-frontends with` | the title prefix | no claim |
| `Browser tab`, `Client router`, `App shell`, `Team A · Catalog UI`, `Team B · Cart UI`, `Team C · Account UI`, `Event bus`, `Shared libraries` | node NAMEs, Browser column | no claim (the example shop's parts) |
| `Edge router`, `Page cache`, `CDN` | node NAMEs, Edge column | no claim |
| `Page composer`, `BFF`, `Team A server`, `Team B server`, `Team C server` | node NAMEs, Origin column | no claim |
| `Catalog API (team A)`, `Order API (team B)`, `Account API (team C)`, `Headless CMS` | node NAMEs, Backend column | no claim |
| `Registry`, `Integration build`, `Team A pipeline`, `Team B pipeline`, `Team C pipeline` | node NAMEs, build band | no claim |
| `Browser (one page at run time)`, `Team UIs (micro-frontends)`, `Edge (CDN and proxy)`, `Origin (servers)`, `Team servers`, `Backend (APIs and content)`, `Team APIs`, `Build time (before any request)`, `Team pipelines`, `Legend` | container titles | no claim |
| `Where the HTML is produced`, `Where and when the micro-frontends are composed`, `Trade-off for micro-frontends` | statement headings | no claim |
| `Team A · Catalog`, `Team B · Cart and orders`, `Team C · Account`, `Shared or platform-owned`, `Where the micro-frontends are composed (the pivot)`, `Not used in this approach` | legend badge labels | no claim |
| `Network request at run time: the arrow is the request, the label says what comes back`, `Call inside the page (no network)`, `Build or deploy, before any request` | legend sample-cable captions | no claim (the frame's own conventions) |
| `Numbers = the order of the steps … · yellow = where the micro-frontends are composed` | legend line 1 | no claim (the frame's own conventions) |
| `BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), drawn where this example uses them; the headless CMS is a data source, not a BFF.` | legend line 2 | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15): rendering, the BFF and caching are three independent concerns, and a CMS is a data source, not a BFF · nextjs.org/docs/app/guides/incremental-static-regeneration (read 2026-11-15 by the plan): ISR serves cached pages and regenerates them |
| `Companions (same frame):` | the companions heading | no claim |
| `not used in <ABBR>` | the default muted subtitle | no claim |

## Frame API

`../script/_lib/mfe_frame.py`:
```
build_page(abbr, full_name, statements[3], states{node_id: "active"|"muted"|"pivot"},
           subtitles{node_id: str}, cables[(n, from_id, to_id, edge_class, label)],
           companions[6], out_path) -> writes the .drawio, returns {path, cells, cables, pivot, muted}
```
- It owns every coordinate, style, class marker, port, waypoint, label wrap and label slide above. A builder passes
  data only.
- **`states` names every node** (all 25), and **`states` and `subtitles` take node ids only**: a group id in `states`
  raises an error (a group is muted when every member is muted, and drawn normally otherwise). An active node needs a
  subtitle; a muted node with none gets `not used in <ABBR>`.
- **It refuses to write** (ValueError, nothing written) on: a missing or unknown state, not exactly one pivot, an
  unknown pair, an unknown edge class, a label with no slide for its page, a label that is not clear, a cable through a
  title, a statement over capacity, a card subtitle its estimate says overflows.
- **Deterministic output:** `<mxfile host="mfe-frame">`, diagram id `mfe-<abbr lowercase>`, one `<diagram>`, cells in a
  fixed order, LF line ends, UTF-8, no timestamp, so a rebuild is byte-identical.
- **Checks on the written text** (asserted): one `<diagram>`, unique ids, every vertex and every point on the 20-px grid,
  every content card carries `mfeClass`, exactly one `mfeClass=pivot`, one `shadow=` key per card and `shadow=1` on the
  pivot only, `opacity=45;textOpacity=60;opacityGroup=1;` on every muted card.

## Render helper

`../script/_lib/render_png.py`, `render(drawio_path, png_path)`:
- **HTML page:** a temporary page holding `<div class="mxgraph" data-mxgraph="…">`, the value
  `html.escape(json.dumps({"toolbar": "", "nav": False, "resize": True, "lightbox": False, "border": 10, "fit": False,
  "zoom": 1, "xml": <xml>}), quote=True)` (the form and the viewer settings of the prompt master's
  `shared/workflows/project-status-engine.py` `export_drawio`, so an apostrophe in a label cannot break it), with
  `window.IMAGE_PATH` (the viewer's `img/` folder) and `window.DRAWIO_BASE_URL` set, and the draw.io `viewer.min.js`.
- **Finding the viewer:** `DRAWIO_VIEWER_JS`, else the newest
  `<home>/.vscode/extensions/hediet.vscode-drawio-*/drawio/src/main/webapp/js/viewer.min.js`.
- **Finding the browser** (built from environment variables only): `CHROME_PATH`; then `Google\Chrome\Application\chrome.exe`
  and then `Microsoft\Edge\Application\msedge.exe` under `%ProgramFiles%`, `%ProgramFiles(x86)%` and `%LOCALAPPDATA%`;
  then the absolute PATH entries only (an empty PATH entry would search the current folder).
- **Run:** `--headless=new --disable-gpu --no-first-run --hide-scrollbars --allow-file-access-from-files
  --user-data-dir=<new temp dir> --window-size=<page w + 100>,<page h + 100> --virtual-time-budget=15000
  --screenshot=<tmp png> <page URI>`.
- **Finish:** crop with Pillow to the drawn content (the bounding box of non-white pixels) plus 20 px, write `png_path`,
  delete the temporary folder and page. It exits non-zero and names what it looked for (variable names, never a resolved
  path) when no viewer or browser is found, and never reports a render that did not run.

## Row-only README commit

The one procedure for a commit that adds a `## Storage` row to `architecture-frontend/README.md` (T-001 used it first;
T-002 to T-007 use it by name). Builds run in parallel, so the working-tree README may hold another build's uncommitted
row, and other sessions commit to this repo at any moment (board claims), so every step works from one recorded base
commit, `<base>`. Run every line in Git Bash, each as its own call, with the values written out. `<paths>` = this
commit's other exact paths; `<tmp>` = a new temporary folder outside the repo; `<msg>` = the message file written in an
earlier call. **The pre-commit leak check** is the one T-001 to T-007 give in their `## Approach` (a staged-lines
command and a message command); this contract names it and never copies its pattern, because the pattern holds the
words it searches for.

1. `git rev-parse HEAD` (prints `<base>`); `git show <base>:architecture-frontend/README.md > <tmp>/README.md`; then add
   only this ticket's row to `<tmp>/README.md`, in number order, with LF line endings.
2. `diff -q --strip-trailing-cr <tmp>/README.md architecture-frontend/README.md`
   - **Exit 0** (the working-tree README holds no other build's change): commit it as it is, in one call:
     `diff -q --strip-trailing-cr <tmp>/README.md architecture-frontend/README.md && test "$(git rev-parse HEAD)" = <base> && git add -- <paths> architecture-frontend/README.md && ! <the leak check's staged-lines command, on <paths> architecture-frontend/README.md> && ! <its message command, on <msg>> && git commit -F <msg> -- <paths> architecture-frontend/README.md`.
     If it stops at `diff` or `test`, delete `<tmp>` and start again at step 1. If the leak check prints a hit, fix the
     file and start again at step 1. If it stops at `git commit` itself (a hook failed, or `cannot lock ref 'HEAD'`),
     nothing was committed: fix a hook failure, delete `<tmp>` and start again at step 1.
   - **Exit 1** (another build's uncommitted change is there): commit `<base>`'s README plus this row only, through a
     private index:
     1. `git hash-object -w <tmp>/README.md` (prints `<blob>`);
     2. `GIT_INDEX_FILE=<tmp>/index git read-tree <base>`;
     3. `GIT_INDEX_FILE=<tmp>/index git update-index --add --cacheinfo 100644,<blob>,architecture-frontend/README.md`;
     4. `GIT_INDEX_FILE=<tmp>/index git add -- <paths>`;
     5. the leak check, both commands: the staged-lines one on `<paths> architecture-frontend/README.md`, with
        `GIT_INDEX_FILE=<tmp>/index` before its `git diff`, and the message one on `<msg>`. On a hit, fix the file,
        delete `<tmp>` and start again at step 1;
     6. `test "$(git rev-parse HEAD)" = <base> && GIT_INDEX_FILE=<tmp>/index git commit -F <msg> && test "$(git rev-parse HEAD~1)" = <base>`.
        - It stops at the first `test`: another commit landed since step 1, and nothing was committed. Delete `<tmp>`
          and start again at step 1.
        - It stops at `git commit` itself: nothing was committed. Fix a hook failure, delete `<tmp>`, start again.
        - It stops at the last `test`: a commit landed in the instant before `git commit`, and the new commit (`<sha>`)
          undoes it. Run `test "$(git rev-parse HEAD)" = "$(git rev-parse <sha>)" && git fetch -q origin && ! git merge-base --is-ancestor HEAD origin/main && git reset -q --soft HEAD~1`.
          If it succeeds, delete `<tmp>` and start again at step 1. If it fails, do **not** reset: stop, set
          `needs-user` naming `<sha>` and the commit it undid, and never push.
     7. `git reset -q -- <paths> architecture-frontend/README.md`: the shared index follows the new HEAD for these paths
        only, and the other build's row stays an uncommitted change, for that build to commit itself.
- **What it guarantees:** every tree it commits starts from the recorded `<base>`; a race restarts it from step 1; it
  never stages or commits another build's file or row, and it touches the shared index only for this commit's own
  paths. It runs the repo's hooks like any commit (never `--no-verify`), and it carries the spec and the builder
  together, so the spec-sync hook has nothing to block.

## Frame proof

- **Date:** 2026-11-16 (T-001's dry run: a throwaway, git-ignored dry-run script in this workspace's script unit).
- **Prompt master at the dry run:** commit `85d40f2c` (HEAD), with no uncommitted edit in the 3-diagram kit (`git status --porcelain` on the kit folder empty); the last commit that changed the kit is `81912dfc`.
- **What ran, per page:** the full page data of T-001 to T-007 (title, S1 to S3, every state and subtitle, every cable with its full label, forced breaks included, the companions) through `build_page`; `kit_coverage_check.py` and `check_layout.py` (report profile, ROAD, no `--centre`), every finding read; a render through `render_png.render` (headless Chrome with the draw.io viewer of the VS Code extension 1.19.0), looked at whole and in full-resolution crops.
- **Fixes the dry run made to the frame** (frame-only moves, all seven re-run after each): the Browser–Edge gutter widened 200 → 280 px and the page 2980 x 1640 → 3060 x 1680 (MPA cable 1); ports and bends put on the 20-px grid; the legend made 40 px taller and the companions card moved down 40 px; label slides and per-page wraps found and frozen (§ Label slides and wraps); a step number kept with its `·` when a label wraps (ISR cable 3).

| page | pivot | kit_coverage_check.py | check_layout.py | CROSS | COLLINEAR | STRADDLE | OFF-PAGE | DEPTH-STROKE | excluded edges | other soft findings kept |
|---|---|---|---|---|---|---|---|---|---|---|
| CSR | B-SHELL | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SPA | B-ROUTER | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| MPA | E-ROUTER | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SSR | O-COMPOSER | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SSG | D-INTEGRATION | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| ISR | O-COMPOSER | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| RSC | O-COMPOSER | exit 0 (25/25 kit-backed) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |

- **CSR:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot B-SHELL the only warm card; muted cards (9, icons included) faded; class markers and shadow keys checked.
- **SPA:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot B-ROUTER the only warm card; muted cards (7, icons included) faded; class markers and shadow keys checked.
- **MPA:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot E-ROUTER the only warm card; muted cards (12, icons included) faded; class markers and shadow keys checked.
- **SSR:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot O-COMPOSER the only warm card; muted cards (8, icons included) faded; class markers and shadow keys checked.
- **SSG:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot D-INTEGRATION the only warm card; muted cards (10, icons included) faded; class markers and shadow keys checked.
- **ISR:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot O-COMPOSER the only warm card; muted cards (5, icons included) faded; class markers and shadow keys checked.
- **RSC:** `kit_coverage_check.py` exit 0; `check_layout.py` exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE; excluded edges = the three legend samples only; no other soft finding; no label on a card, wall, title or cable; no cable through a title; no overflow; pivot O-COMPOSER the only warm card; muted cards (9, icons included) faded; class markers and shadow keys checked.
