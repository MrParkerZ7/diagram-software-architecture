# Micro-frontend frame — the contract

> The one page layout that the seven micro-frontend diagrams of this library (slots 001 to 007: CSR, SPA, MPA, SSR,
> SSG, ISR, RSC) are drawn from, so that they compare part for part and only the composition point moves.
> **Status: frozen when T-001 closes** (after the dry run below met the bar on all seven pages). A later need is a new
> ticket that redraws the affected slots under the library's storage policy; T-002 to T-007 use the frame as it is.
> **Form (2026-11-16, the owner's word):** an architecture page in the prompt master's standard. Every part is an
> icon with its name as a caption, and the numbered arrows between the icons carry the workflow; no part is a text card
> (prompt master `shared/prompts/PROMPT_BEHAVIORAL_FEEDBACK_diagrams.md` § *An architecture diagram is icons joined by
> workflow arrows*). The first frame drew every node as a T1 clay card with a subtitle; the owner rejected it
> (*"the diagram workflow should be bease with icon arrow workflow relation, but you just use icon text box which in
> correct standard for diagrams architect"*), and this contract replaces it.

**Implemented by** `../script/_lib/mfe_frame.py` (`build_page`, every coordinate, style, port, waypoint, wrap and slide
below) and `../script/_lib/render_png.py` (`render`). The tables of this contract are generated from `mfe_frame.py`'s
own data at the dry run, so the two agree; when they ever disagree, the code is what was proved, and the difference is a
defect to fix here.

**Environment** (never written into a committed file): `DIAGRAM_KIT` = the prompt master's `shared/prompts/3-diagram`
folder; `mfe_frame` exits with `DIAGRAM_KIT must point to the prompt master's shared/prompts/3-diagram` when it is unset
or wrong, before anything is written. The render helper finds the browser and the draw.io viewer at run time (§ Render
helper).

## Page and spacing

- **Page:** 3240 x 1840. All geometry (cells, ports, waypoints) is in multiples of 20 (`PROMPT_OBJECT.md` mod-10 rule,
  kept stricter here). The kit's own chrome (a flat T1's fold, a T3's notches) keeps the kit's offsets.
- **Streets** (horizontal free space between bands):
  - the **top street**, between the statement cards and the columns: y 220 to 320 (its cables run at y 260);
  - the **band street**, between the columns and the build band: y 1100 to 1180 (its cables run at y 1140 and 1160);
  - the **street below the band**: y 1640 to 1740 (its cables run at y 1680 and 1700).
- **Gutters** (vertical free space between columns):
  - **Browser–Edge: x 960 to 1240, 280 px** (MPA cable 1's 3-line label at a 34-character wrap needs about 210 px plus 20
    clear on each side); its cable runs at x 1100;
  - **Edge–Origin: x 1640 to 1840, 200 px;** its cables run at x 1700 (the integration build's rise), 1740 (the page
    cache to the composer) and 1780 (the edge router to the BFF and the team servers);
  - **Origin–Backend:** x 2540 to 2740, 200 px.
- **The east lane:** x 3080 to 3240, east of the Backend column; its cables run at x 3120 and 3160.
- **The free space west of the band** (x 960 to 1240, below y 1100): its cables run at x 1160 and 1200.
- **Container titles.** Every container is `swimlane;startSize=0`; its title (font 14, bold) is centred on its top wall
  and reaches about 12 px above and below it. The frame computes each title's box (about 8.2 px a character plus 16, 24
  high) and refuses a cable that touches one.
- **Insets:** an icon sits at least 40 px below its container's top wall; a group at least 40 px below its column's top
  (G-SHELL and G-REMOTES sit higher, 40 px below the column's wall, with their titles clear of the column's), so two
  titles never stack; a caption sits at least 4 px inside its container.

## Placement

- **Plan:** ROAD (`PROMPT_CITY_PLAN_LAYOUT.md` § *Scope*, cloud architecture). The order axis is the request path, left
  to right (Browser, Edge, Origin, Backend); the build band sits below Edge and Origin. No `--centre` is asserted (a ROAD
  page has no downtown); `check_layout.py`'s info line reports the content centre in the Edge column, which is expected
  for this plan.
- **Coordinates** below are absolute page positions. A child is written relative to its container
  (`PROMPT_CONTAINER.md` § *Coordinate System*).
- **Z-order:** containers with their children first (depth first), then the cables, then the page furniture.
- **Why this placement.** Inside a container a cable is one straight segment (§ Routing rule), and a caption under an
  icon closes that icon's bottom face to cables. So the links inside a container run sideways, or vertically into a
  group's wall, or leave a **hub** icon's bottom face beside its caption:
  - **The Browser reads right to left:** the Browser tab (a 160 hub) sends `2` and `1` into the App shell group's
    right wall below both of its members (so the arrow enters the shell, not one member), and the hydration arrow under
    the shell into the Team UIs group; the runtime loader and the client router, stacked in the shell, each reach the
    Team UIs group's right wall by a straight line; the Team UIs group's bottom wall drops into the event bus.
  - **The Edge:** the edge router (160) faces the Browser tab across the gutter (`B-PAGE → E-ROUTER` is straight) and
    drops into the page cache from the right side of its bottom face; the CDN (160, a 3-letter caption) takes three
    build arrows into its bottom face.
  - **The Origin:** the page composer (160) faces the edge router across the gutter, reaches the BFF (160) sideways and
    drops into the Team servers group from the left side of its bottom face; the Team servers group rises into the
    BFF's bottom face beside its caption; the BFF reaches the Team APIs sideways.
  - **The build band:** the Team pipelines group sits above the registry (120), which takes it through its top face
    and passes to the integration build sideways; the registry's other top port and the pipelines' top wall rise to the
    band street, and the integration build's top face rises to the CDN, the page cache or the east lane.

## Containers

All are `swimlane;startSize=0;labelBorderColor=none;textShadow=1;labelBackgroundColor=default;rounded=0;html=1;`
with `fillColor` = `swimlaneFillColor`, `fontSize=14;fontStyle=1;fontColor=#37474F;shadow=1`
(`PROMPT_CONTAINER.md` § *Default Group/Container Style*).
- **Stroke width** (§ *Border Width Hierarchy*, T-232): 4 = a frame on the page holding another frame; 3 = every other
  frame, a frame on its own included. Icons carry no stroke.
- **Fills and strokes are cool and neutral only:** columns, the band and the legend `#FFFFFF` / `#5F6B7A`; groups
  `#F4F6F9` / `#8A97A8`.
- **A muted group** (every member muted) keeps its swimlane and strokeWidth 3, with `strokeColor=#BDBDBD`,
  `fontColor=#9E9E9E`, `opacity=45`. A group never takes a state of its own.
- **G-SHELL, the App shell group** (new with this form): the shell's two parts, the runtime loader (CSR's pivot) and
  the client router (SPA's pivot). It says that the shell owns its router, which the first frame drew as a cable.
- **C-LEGEND** carries `kitExempt=1` (page furniture); its rows are its children.

| id | title | in | x,y,w,h (absolute) | strokeWidth | fill / stroke |
|---|---|---|---|---|---|
| C-BROWSER | Browser (one page at run time) | page | 40,320,920,780 | 4 | #FFFFFF / #5F6B7A |
| G-REMOTES | Team UIs (micro-frontends) | C-BROWSER | 60,360,240,460 | 3 | #F4F6F9 / #8A97A8 |
| G-SHELL | App shell | C-BROWSER | 460,360,160,360 | 3 | #F4F6F9 / #8A97A8 |
| C-EDGE | Edge (CDN and proxy) | page | 1240,320,400,780 | 3 | #FFFFFF / #5F6B7A |
| C-ORIGIN | Origin (servers) | page | 1840,320,700,780 | 4 | #FFFFFF / #5F6B7A |
| G-SERVERS | Team servers | C-ORIGIN | 1860,900,660,180 | 3 | #F4F6F9 / #8A97A8 |
| C-BACKEND | Backend (APIs and content) | page | 2740,320,340,780 | 4 | #FFFFFF / #5F6B7A |
| G-APIS | Team APIs | C-BACKEND | 2760,500,300,460 | 3 | #F4F6F9 / #8A97A8 |
| C-BUILD | Build time (before any request) | page | 1240,1180,1300,460 | 4 | #FFFFFF / #5F6B7A |
| G-CI | Team pipelines | C-BUILD | 2080,1220,440,160 | 3 | #F4F6F9 / #8A97A8 |
| C-LEGEND | Legend | page | 40,1180,800,400 | 3 | #FFFFFF / #5F6B7A |

## Nodes

- **Form:** every content node is **one icon**: a kit clay glyph, `gen_icons.style_p3(<key>_p3, CLAY_DEMO[<key>],
  "#FFFFFF")`, in a square cell (`shape=stencil(…);html=1;aspect=fixed;strokeColor=none;shadow=1;`). No node is a text
  card (`kit_coverage_check.py --architecture` passes 25/25).
- **Caption:** the node's NAME, under the icon: `verticalLabelPosition=bottom;verticalAlign=top;align=center;
  spacingTop=2;fontSize=12;fontStyle=1;fontColor=#1F2937;`, with the class's tint (§ Colour classes). One line, never a
  subtitle. The frame estimates a caption at 7.4 px a character plus 10, 20 high, 2 px under the icon.
- **Size:** 80, or a hub: 160 for the Browser tab, the edge router, the CDN, the page composer and the BFF, 120 for the
  registry. A hub's size lets a cable leave its bottom face beside the caption.
- **Marker:** each icon's style also carries `mfeClass=<class>` (draw.io ignores the unknown key; the checks read it).
- **Glyphs** come only from the 3-diagram kit's `CLAY_DEMO` (G-001 D1), never from `mxgraph.*` libraries, which the
  headless viewer does not draw.

| id | NAME (the caption) | glyph (CLAY_DEMO key) | in | x,y (absolute) | size | class when active |
|---|---|---|---|---|---|---|
| B-PAGE | Browser tab | client-browser | C-BROWSER | 780,640 | 160 | platform |
| B-SHELL | Runtime loader | webapp | G-SHELL | 500,400 | 80 | platform |
| B-ROUTER | Client router | page-route | G-SHELL | 500,520 | 80 | platform |
| B-UI-A | Team A · Catalog UI | ui-component | G-REMOTES | 140,400 | 80 | team-a |
| B-UI-B | Team B · Cart UI | ui-component | G-REMOTES | 140,540 | 80 | team-b |
| B-UI-C | Team C · Account UI | ui-component | G-REMOTES | 140,680 | 80 | team-c |
| B-BUS | Event bus | event-stream | C-BROWSER | 140,920 | 80 | platform |
| B-SHARED | Shared libraries | module-package | C-BROWSER | 500,920 | 80 | platform |
| E-ROUTER | Edge router | load-balancer | C-EDGE | 1360,560 | 160 | platform |
| E-CACHE | Page cache | cache | C-EDGE | 1460,860 | 80 | platform |
| E-CDN | CDN | cdn | C-EDGE | 1260,900 | 160 | platform |
| O-COMPOSER | Page composer | service | C-ORIGIN | 1920,520 | 160 | platform |
| O-BFF | BFF | api-gateway | C-ORIGIN | 2260,600 | 160 | platform |
| O-SRV-A | Team A server | service | G-SERVERS | 1940,940 | 80 | team-a |
| O-SRV-B | Team B server | service | G-SERVERS | 2160,940 | 80 | team-b |
| O-SRV-C | Team C server | service | G-SERVERS | 2380,940 | 80 | team-c |
| K-API-A | Catalog API (team A) | microservice | G-APIS | 2880,540 | 80 | team-a |
| K-API-B | Order API (team B) | microservice | G-APIS | 2880,680 | 80 | team-b |
| K-API-C | Account API (team C) | microservice | G-APIS | 2880,820 | 80 | team-c |
| K-CMS | Headless CMS | docs-multi | C-BACKEND | 2880,980 | 80 | platform |
| D-REGISTRY | Registry | registry | C-BUILD | 2000,1480 | 120 | platform |
| D-INTEGRATION | Integration build | ci-pipeline | C-BUILD | 1660,1500 | 80 | platform |
| D-CI-A | Team A pipeline | ci-pipeline | G-CI | 2120,1260 | 80 | team-a |
| D-CI-B | Team B pipeline | ci-pipeline | G-CI | 2260,1260 | 80 | team-b |
| D-CI-C | Team C pipeline | ci-pipeline | G-CI | 2400,1260 | 80 | team-c |

## Page furniture

Every furniture cell carries `kitExempt=1`, appended to each cell the kit returns (a title, a statement and a legend row
are not content nodes, and it keeps them out of `check_layout.py`'s centrality box).
- **Title:** a T3 flat banner (kind `neutral`) at 40,20,3160,60: `Micro-frontends with <ABBR>: <full name>`.
- **Statement cards:** three T1 flat cards (kind `neutral`, `color=#FFFFFF`), 1000 x 120 at y 100: S1 at x 40, S2 at
  x 1120, S3 at x 2200 (80 px apart, so S3 ends on the title's right edge). Label `<b>heading</b><br>statement`, font 12.
  Headings: S1 `Where the HTML is produced`, S2 `Where and when the micro-frontends are composed`, S3 `Trade-off for
  micro-frontends`.
  **Capacity: the heading plus 5 lines, counted at 150 characters a line.** Measured on the renders: a 1000-px card at
  font 12 holds about 160 characters a line, so the count is a little short of what is drawn, never over it. The
  longest statement, ISR S3 (513 characters), counts 4 lines and is drawn in 3. The frame refuses a statement that
  needs more.
- **Companions:** a T1 flat card (kind `neutral`, `color=#FFFFFF`) at 40,1760,3160,60:
  `<b>Companions (same frame):</b>` followed by the other six file names, each
  `00N-micro-frontend-<x>/micro-frontend-<x>-architecture.drawio`, joined by ` · `.
- **Legend:** § Legend.

## Colour classes

The class is said by the **caption's tint** (`labelBackgroundColor`, with `labelBorderColor`), as the prompt master's
rule asks (the container, the caption's tint or a faded icon say a class, never a card). The glyph keeps its own
colours. **The pivot's caption is the one amber pill on the page** (#FFD54F), so the composition point is found at a
glance.

| class | caption fill / border | extra style keys | used for |
|---|---|---|---|
| team-a | #DAE8FC / #6C8EBF | none | B-UI-A, O-SRV-A, K-API-A, D-CI-A |
| team-b | #D5E8D4 / #82B366 | none | B-UI-B, O-SRV-B, K-API-B, D-CI-B |
| team-c | #E1D5E7 / #9673A6 | none | B-UI-C, O-SRV-C, K-API-C, D-CI-C |
| platform | #ECEFF1 / #90A4AE | none | every other node (shared or platform-owned) |
| pivot | #FFD54F / #E69500 | none | the one composition point of the page (replaces its class) |
| muted | #F5F5F5 / #BDBDBD | `opacity=40;textOpacity=40;opacityGroup=1;` | a part this approach does not use |

- **Why `opacityGroup=1` is required:** `gen_icons` writes `<alpha alpha="1"/>` before every stencil primitive, and
  draw.io's stencil `alpha` replaces the cell's opacity instead of multiplying it, so `opacity` alone fades only the
  caption. With `opacityGroup=1` the viewer draws the whole glyph in one group at 40 % (`mxShape.isOpacityGroup`).
  **Proved in the dry-run renders:** without it, the muted page composer and team servers drew at full colour; with it,
  every muted icon reads faded.
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
- **The number is checked:** a cable whose `n` is a number has a label that starts with `<n> ·`; a cable with `n` `-`
  has a label that starts with no step number. `build_page` refuses either mismatch.
- **Endpoints:** a cable may end on a group (G-REMOTES, G-SHELL, G-SERVERS, G-APIS, G-CI): one cable stands for the
  group's members.

## Labels

Font 11. The frame estimates a label at 6.0 px a character and 13.2 px a line (a little wider than drawn, on purpose).
- **Wrap:** set per page in the routing table, 16 to 36 characters. Words wrap whole, and **a step number never parts
  from its `·` nor from the word after it** (`6 · one` stays on one line; `1 · 3 · static` is one unit).
- **Forced line break:** a ticket writes `\n`; the frame turns it into `<br>` and wraps each line on its own.
- **Height:** at most 3 lines on a horizontal run, at most 5 on a vertical run.
- **Clearance (checked by the frame before it writes; it refuses the page otherwise):** a label sits on a run at least
  its own extent plus 40 px long (20 clear before and after it along the run), and its box, 6 px around, touches no
  icon, no caption, no container wall, no container title, no page furniture, no other cable and no other label.
- **Slide:** the label's centre is a point on its route; the frame turns it into the edge geometry `x` (-1 at the
  source end, 1 at the target end).

## Routing rule

Every gate finding counts, not just the exit code.
- **No bend inside a rectangle.** `check_layout.py` reports WAYPOINT-IN for a waypoint inside any node or container
  rectangle, the cable's own column, group or band included, and it fails in every profile. A cable that leaves its own
  container and comes back in is RE-ENTRY (fails the report profile). So **every bend sits in free space**: a street, a
  gutter, the east lane, or the free space west of the build band.
- **Inside a container a cable is one straight segment:** port to port, or port to the container's wall, with no icon
  and no caption in the way.
- **No cable touches a caption** (within 4 px) and **no cable touches a container title**: the frame checks every
  segment against every caption box and title box. `check_layout.py` measures the glyph and not the caption under it,
  so this check is the frame's.
- **Ports:** explicit fractions on the cell's wall (a corner is never a port), asserted to lie on it; two cables of one
  page never share an end point on one face (checked).
- **The routing table** keeps the route (ports and waypoints) per `(from_id, to_id)` pair, and the label slide and wrap
  per `(abbr, from_id, to_id)`, because one pair carries labels of different lengths on different pages. An unknown pair,
  or a label with no slide for its page, raises an error and is never auto-routed.

## Adjacency invariant

A run-time cable joins adjacent columns, or stays inside one container as one straight segment, or runs in a street, a
gutter or the east lane outside every column. A build cable rises from the build band to the column above it, straight
or through the band street, or leaves the band and bends only in free space. No cable crosses a third party's container
(WALL-CUT, hard in both profiles), puts a bend inside a rectangle (WAYPOINT-IN), leaves and re-enters its own container
(RE-ENTRY), or runs through a container title or a caption. Browser network traffic leaves from B-PAGE only; HTML
rendered at request time (or served from the page cache) and API requests go to E-ROUTER; static files, prebuilt HTML
included (CSR's and SPA's index.html, SSG's pages), go to E-CDN.

## Routing table

### Routes

Absolute points; the exit point lies on the source's wall and the entry point on the target's.

| from → to | exit (x, y) | waypoints | entry (x, y) | exitX,exitY → entryX,entryY | drawn on |
|---|---|---|---|---|---|
| B-PAGE → E-ROUTER | 940,680 | none (straight) | 1360,680 | 1,0.25 → 0,0.75 | CSR, SPA, MPA, SSR, SSG, ISR, RSC |
| B-PAGE → E-CDN | 940,760 | 1100,760 · 1100,980 | 1260,980 | 1,0.75 → 0,0.5 | CSR, SPA, MPA, SSR, SSG, ISR, RSC |
| B-PAGE → G-SHELL | 780,680 | none (straight) | 620,680 | 0,0.25 → 1,0.888889 | CSR, SPA |
| B-PAGE → G-REMOTES | 780,760 | none (straight) | 300,760 | 0,0.75 → 1,0.869565 | SSR, SSG, RSC |
| B-SHELL → G-REMOTES | 500,440 | none (straight) | 300,440 | 0,0.5 → 1,0.173913 | CSR |
| B-ROUTER → G-REMOTES | 500,560 | none (straight) | 300,560 | 0,0.5 → 1,0.434783 | SPA |
| G-REMOTES → B-BUS | 180,820 | none (straight) | 180,920 | 0.5,1 → 0.5,0 | SPA |
| E-ROUTER → O-COMPOSER | 1520,600 | none (straight) | 1920,600 | 1,0.25 → 0,0.5 | SSR, RSC |
| E-ROUTER → O-BFF | 1520,680 | 1780,680 · 1780,740 | 2260,740 | 1,0.75 → 0,0.875 | CSR, SPA, SSG |
| E-ROUTER → G-SERVERS | 1520,680 | 1780,680 · 1780,1000 | 1860,1000 | 1,0.75 → 0,0.555556 | MPA |
| E-ROUTER → E-CACHE | 1500,720 | none (straight) | 1500,860 | 0.875,1 → 0.5,0 | ISR |
| E-CACHE → O-COMPOSER | 1540,880 | 1740,880 · 1740,640 | 1920,640 | 1,0.25 → 0,0.75 | ISR |
| O-COMPOSER → O-BFF | 2080,660 | none (straight) | 2260,660 | 1,0.875 → 0,0.375 | RSC |
| O-COMPOSER → G-SERVERS | 1940,680 | none (straight) | 1940,900 | 0.125,1 → 0.121212,0 | SSR, ISR |
| G-SERVERS → O-BFF | 2300,900 | none (straight) | 2300,760 | 0.666667,0 → 0.25,1 | MPA, SSR, ISR |
| O-BFF → G-APIS | 2420,720 | none (straight) | 2760,720 | 1,0.75 → 0,0.478261 | CSR, SPA, MPA, SSR, ISR, RSC |
| O-BFF → K-API-B | 2420,720 | none (straight) | 2880,720 | 1,0.75 → 0,0.5 | SSG |
| K-CMS → O-COMPOSER | 2960,1000 | 3120,1000 · 3120,260 · 2020,260 | 2020,520 | 1,0.25 → 0.625,0 | ISR |
| G-CI → E-CDN | 2120,1220 | 2120,1140 · 1380,1140 | 1380,1060 | 0.090909,0 → 0.75,1 | CSR, SPA, MPA, SSR |
| G-CI → D-REGISTRY | 2100,1380 | none (straight) | 2100,1480 | 0.045455,1 → 0.833333,0 | CSR, SPA, SSG, RSC |
| D-REGISTRY → E-CDN | 2040,1480 | 2040,1160 · 1280,1160 | 1280,1060 | 0.333333,0 → 0.125,1 | CSR, SPA |
| G-CI → G-SERVERS | 2500,1220 | 2500,1140 · 2240,1140 | 2240,1080 | 0.954545,0 → 0.575758,1 | MPA, SSR, ISR |
| D-REGISTRY → D-INTEGRATION | 2000,1540 | none (straight) | 1740,1540 | 0,0.5 → 1,0.5 | SSG, RSC |
| D-INTEGRATION → K-CMS | 1660,1560 | 1200,1560 · 1200,1680 · 3120,1680 · 3120,1020 | 2960,1020 | 0,0.75 → 1,0.5 | SSG |
| D-INTEGRATION → K-API-A | 1660,1520 | 1160,1520 · 1160,1700 · 3160,1700 · 3160,580 | 2960,580 | 0,0.25 → 1,0.5 | SSG |
| D-INTEGRATION → E-CDN | 1700,1500 | 1700,1160 · 1300,1160 | 1300,1060 | 0.5,0 → 0.25,1 | SSG |
| D-INTEGRATION → E-CACHE | 1700,1500 | 1700,920 | 1540,920 | 0.5,0 → 1,0.75 | ISR |
| D-INTEGRATION → O-COMPOSER | 1660,1560 | 1200,1560 · 1200,1680 · 3120,1680 · 3120,260 · 1980,260 | 1980,520 | 0,0.75 → 0.375,0 | RSC |

### Label slides and wraps

`centre` is the label's centre on its route; `slide` is the edge geometry `x` the frame writes; `lines` is the drawn
line count at that wrap. Found by the dry run's clearance-first placer and frozen into `mfe_frame.LABELS`.

| page | from → to | wrap | centre (x, y) | slide (edge x) | lines |
|---|---|---|---|---|---|
| CSR | B-PAGE → E-CDN | 30 | 1100,870 | 0 | 3 |
| CSR | B-PAGE → G-SHELL | 20 | 700,680 | 0 | 1 |
| CSR | B-SHELL → G-REMOTES | 16 | 380,440 | 0.2 | 3 |
| CSR | B-PAGE → E-ROUTER | 18 | 1100,680 | -0.2381 | 2 |
| CSR | E-ROUTER → O-BFF | 26 | 2150,740 | 0.725 | 1 |
| CSR | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| CSR | G-CI → E-CDN | 32 | 1750,1140 | 0 | 1 |
| CSR | G-CI → D-REGISTRY | 16 | 2100,1430 | 0 | 2 |
| CSR | D-REGISTRY → E-CDN | 22 | 1280,1130 | 0.8814 | 1 |
| SPA | B-PAGE → G-SHELL | 18 | 700,680 | 0 | 3 |
| SPA | B-PAGE → E-CDN | 20 | 1100,870 | 0 | 2 |
| SPA | B-ROUTER → G-REMOTES | 20 | 380,560 | 0.2 | 2 |
| SPA | B-PAGE → E-ROUTER | 20 | 1100,680 | -0.2381 | 2 |
| SPA | E-ROUTER → O-BFF | 26 | 2150,740 | 0.725 | 1 |
| SPA | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| SPA | G-REMOTES → B-BUS | 18 | 180,880 | 0.2 | 2 |
| SPA | G-CI → E-CDN | 32 | 1750,1140 | 0 | 1 |
| SPA | G-CI → D-REGISTRY | 16 | 2100,1430 | 0 | 2 |
| SPA | D-REGISTRY → E-CDN | 22 | 1280,1130 | 0.8814 | 1 |
| MPA | B-PAGE → E-ROUTER | 34 | 1100,680 | -0.2381 | 3 |
| MPA | E-ROUTER → G-SERVERS | 16 | 1780,840 | 0.2727 | 3 |
| MPA | G-SERVERS → O-BFF | 20 | 2300,840 | -0.1429 | 2 |
| MPA | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| MPA | B-PAGE → E-CDN | 30 | 1100,870 | 0 | 1 |
| MPA | G-CI → G-SERVERS | 18 | 2370,1140 | 0.05 | 2 |
| MPA | G-CI → E-CDN | 22 | 1570,1140 | 0.4 | 1 |
| SSR | B-PAGE → E-ROUTER | 20 | 1100,680 | -0.2381 | 1 |
| SSR | E-ROUTER → O-COMPOSER | 18 | 1740,600 | 0.1 | 3 |
| SSR | O-COMPOSER → G-SERVERS | 30 | 1940,800 | 0.0909 | 2 |
| SSR | G-SERVERS → O-BFF | 18 | 2300,840 | -0.1429 | 2 |
| SSR | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| SSR | B-PAGE → E-CDN | 26 | 1100,870 | 0 | 1 |
| SSR | B-PAGE → G-REMOTES | 22 | 690,760 | -0.625 | 2 |
| SSR | G-CI → G-SERVERS | 20 | 2370,1140 | 0.05 | 2 |
| SSR | G-CI → E-CDN | 26 | 1570,1140 | 0.4 | 1 |
| SSG | G-CI → D-REGISTRY | 24 | 2100,1440 | 0.2 | 2 |
| SSG | D-REGISTRY → D-INTEGRATION | 22 | 1890,1540 | -0.1538 | 2 |
| SSG | D-INTEGRATION → K-CMS | 18 | 1440,1560 | -0.8675 | 2 |
| SSG | D-INTEGRATION → K-API-A | 22 | 3160,810 | 0.785 | 2 |
| SSG | D-INTEGRATION → E-CDN | 18 | 1700,1360 | -0.6667 | 2 |
| SSG | B-PAGE → E-CDN | 24 | 1100,870 | 0 | 2 |
| SSG | B-PAGE → G-REMOTES | 28 | 550,760 | -0.0417 | 2 |
| SSG | B-PAGE → E-ROUTER | 28 | 1100,680 | -0.2381 | 2 |
| SSG | E-ROUTER → O-BFF | 26 | 2150,740 | 0.725 | 1 |
| SSG | O-BFF → K-API-B | 22 | 2640,720 | -0.0435 | 2 |
| ISR | D-INTEGRATION → E-CACHE | 26 | 1700,1360 | -0.6216 | 2 |
| ISR | B-PAGE → E-ROUTER | 20 | 1100,680 | -0.2381 | 1 |
| ISR | E-ROUTER → E-CACHE | 24 | 1500,810 | 0.2857 | 2 |
| ISR | E-CACHE → O-COMPOSER | 30 | 1740,760 | 0.0323 | 4 |
| ISR | O-COMPOSER → G-SERVERS | 26 | 1940,800 | 0.0909 | 2 |
| ISR | G-SERVERS → O-BFF | 16 | 2300,840 | -0.1429 | 1 |
| ISR | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| ISR | K-CMS → O-COMPOSER | 28 | 2020,440 | 0.9292 | 3 |
| ISR | B-PAGE → E-CDN | 26 | 1100,870 | 0 | 2 |
| ISR | G-CI → G-SERVERS | 30 | 2370,1140 | 0.05 | 3 |
| RSC | G-CI → D-REGISTRY | 24 | 2100,1440 | 0.2 | 2 |
| RSC | D-REGISTRY → D-INTEGRATION | 18 | 1890,1540 | -0.1538 | 2 |
| RSC | D-INTEGRATION → O-COMPOSER | 22 | 3120,1400 | 0.0451 | 1 |
| RSC | B-PAGE → E-ROUTER | 30 | 1100,680 | -0.2381 | 2 |
| RSC | E-ROUTER → O-COMPOSER | 20 | 1740,600 | 0.1 | 2 |
| RSC | O-COMPOSER → O-BFF | 18 | 2170,660 | 0 | 3 |
| RSC | O-BFF → G-APIS | 18 | 2640,720 | 0.2941 | 2 |
| RSC | B-PAGE → E-CDN | 18 | 1100,870 | 0 | 2 |
| RSC | B-PAGE → G-REMOTES | 22 | 540,760 | 0 | 3 |

## Paper check

Each page's cables, checked by the frame's own checks before writing and then by the gate in the dry run: 0 WAYPOINT-IN,
0 RE-ENTRY, 0 WALL-CUT, 0 CUTS-NODE, 0 CROSS and 0 COLLINEAR on each of the seven pages, and no cable within 4 px of a
caption or a title.
- **CSR:** 1 · 2 · 3 · 4 · 5 · 6 and the three build cables (G-CI → E-CDN and D-REGISTRY → E-CDN through the band
  street, G-CI → D-REGISTRY).
- **SPA:** 1 to 7 and the three build cables. The first frame's unnumbered `owns the router` cable (B-SHELL → B-ROUTER)
  is gone: the App shell group holds the router.
- **MPA:** 1 to 5, and G-CI → G-SERVERS (through the band street) and G-CI → E-CDN.
- **SSR:** 1 to 8 (step 6 rides on cable 2), and the two build cables.
- **SSG:** 1 to 9 and the product-data cable: D-INTEGRATION rises to E-CDN through the band street, and its two east
  routes leave its west face, drop to the street below the band and rise in the east lane (K-CMS by the inner lane at
  x 3120, K-API-A by the outer at x 3160, so the two never cross).
- **ISR:** 0 to 7, the CDN cable, the K-CMS trigger by the east lane and the top street, and G-CI → G-SERVERS. Cable 0
  rises at x 1700 and enters E-CACHE's east face at y 920, below cable 3's exit at y 880.
- **RSC:** 1 to 7 and the three build cables, with D-INTEGRATION → O-COMPOSER by the street below the band, the east
  lane and the top street.

## Legend

C-LEGEND, titled `Legend`, at 40,1180,800,400; every row is its child and carries `kitExempt=1`.
- **Badges:** one **flat** T4 badge per colour class (240 x 40, three to a row), its class's caption fill (the muted
  badge carries the muted keys too), labelled `Team A · Catalog`, `Team B · Cart and orders`, `Team C · Account`,
  `Shared or platform-owned`, `Where the micro-frontends are composed (the pivot)`, `Not used in this approach`. A
  badge has the colour of the captions it decodes.
- **Sample cables:** one per edge class, the class style verbatim, with free source and target points (so the gate
  excludes them as UNVERIFIABLE, and they are the only excluded edges), captioned `Network request at run time: the
  arrow is the request, the label says what comes back`, `Call inside the page (no network)`, `Build or deploy, before
  any request`.
- **The two fixed lines:**
  - `Each part is an icon; its caption names it, and the caption's colour is its class. Numbers = the order of the steps of the flow drawn; numbered dashed steps are build steps and come before any request; an unnumbered cable stands outside that order (a build or deploy link, a standing link, or a separate trigger).`
  - `BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), drawn where this example uses them; the headless CMS is a data source, not a BFF.`

## Frame-static text

The text the frame fixes, the same on all seven pages. A slot's page-text table covers its cable labels only;
everything here is sourced once, in this table (`frame-static` in a slot's table points here).

| text | where | source |
|---|---|---|
| `Micro-frontends with` | the title prefix | no claim |
| `Browser tab`, `Runtime loader`, `Client router`, `Team A · Catalog UI`, `Team B · Cart UI`, `Team C · Account UI`, `Event bus`, `Shared libraries` | captions, Browser column | no claim (the example shop's parts) |
| `Edge router`, `Page cache`, `CDN` | captions, Edge column | no claim |
| `Page composer`, `BFF`, `Team A server`, `Team B server`, `Team C server` | captions, Origin column | no claim |
| `Catalog API (team A)`, `Order API (team B)`, `Account API (team C)`, `Headless CMS` | captions, Backend column | no claim |
| `Registry`, `Integration build`, `Team A pipeline`, `Team B pipeline`, `Team C pipeline` | captions, build band | no claim |
| `Browser (one page at run time)`, `Team UIs (micro-frontends)`, `App shell`, `Edge (CDN and proxy)`, `Origin (servers)`, `Team servers`, `Backend (APIs and content)`, `Team APIs`, `Build time (before any request)`, `Team pipelines`, `Legend` | container titles | no claim |
| `Where the HTML is produced`, `Where and when the micro-frontends are composed`, `Trade-off for micro-frontends` | statement headings | no claim |
| `Team A · Catalog`, `Team B · Cart and orders`, `Team C · Account`, `Shared or platform-owned`, `Where the micro-frontends are composed (the pivot)`, `Not used in this approach` | legend badge labels | no claim |
| `Network request at run time: the arrow is the request, the label says what comes back`, `Call inside the page (no network)`, `Build or deploy, before any request` | legend sample-cable captions | no claim (the frame's own conventions) |
| `Each part is an icon; … a standing link, or a separate trigger).` | legend line 1 | no claim (the frame's own conventions) |
| `BFF and page cache are separate choices from the rendering approach (ISR alone is built on its page cache), drawn where this example uses them; the headless CMS is a data source, not a BFF.` | legend line 2 | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15): rendering, the BFF and caching are three independent concerns, and a CMS is a data source, not a BFF · nextjs.org/docs/app/guides/incremental-static-regeneration (read 2026-11-15 by the plan): ISR serves cached pages and regenerates them |
| `Companions (same frame):` | the companions heading | no claim |

## Frame API

`../script/_lib/mfe_frame.py`:
```
build_page(abbr, full_name, statements[3], states{node_id: "active"|"muted"|"pivot"},
           cables[(n, from_id, to_id, edge_class, label)], companions[6], out_path)
    -> writes the .drawio, returns {path, cells, cables, pivot, muted}
```
- It owns every coordinate, style, class marker, port, waypoint, label wrap and label slide above. A builder passes
  data only. There are no subtitles: a part's caption is its NAME.
- **`states` names every node** (all 25) and takes node ids only: a group id raises an error (a group is muted when
  every member is muted, and drawn normally otherwise).
- **It refuses to write** (ValueError, nothing written) on: a missing or unknown state, not exactly one pivot, an
  unknown pair, an unknown edge class, a label with no slide for its page, a step number its label does not start with,
  a label that is not clear, a cable through a title or a caption, a caption outside its container, two cables sharing
  a port, a statement over capacity, and a kit whose output no longer matches `KIT_FINGERPRINT`.
- **The kit fingerprint.** The frame calls the prompt master's kit live. `KIT_FINGERPRINT` is the sha256 of the kit's
  output for fixed probes (each glyph the frame uses through `gen_icons.style_p3`, and one `gen_text` cell per pattern
  it uses: T4, T3, T1), taken when the frame was proved. If the kit draws differently, `build_page` refuses to write and
  says how to prove the frame again: the dry run on all seven pages, both gates, every render looked at, then
  `KIT_FINGERPRINT = mfe_frame.kit_fingerprint()` and a new line in § Frame proof.
- **Deterministic output:** `<mxfile host="mfe-frame">`, diagram id `mfe-<abbr lowercase>`, one `<diagram>`, cells in a
  fixed order, LF line ends, UTF-8, no timestamp, so a rebuild is byte-identical. The repo's `.gitattributes` keeps
  `*.drawio` as stored (`-text`), so a manifest's sha256 (of the LF bytes) matches on every checkout.
- **Checks on the written text** (asserted): one `<diagram>`, unique ids, every vertex and every point on the 20-px grid,
  every content icon carries `mfeClass`, exactly one `mfeClass=pivot`, every icon's caption under it
  (`verticalLabelPosition=bottom`), no wrapped card label and no subtitle, and `opacity=40;textOpacity=40;opacityGroup=1;`
  on every muted icon.

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

- **Date:** 2026-11-16 (T-001's second dry run, for the icon form: a throwaway, git-ignored dry-run script in this
  workspace's script unit).
- **Prompt master at the dry run:** the 3-diagram kit as of commit `2a65231f`, the last commit that changed it (it added
  `kit_coverage_check.py --architecture` and the rule this form follows), with no uncommitted edit in the kit folder.
  `KIT_FINGERPRINT` = `babc75c06a532248a51ade77da8d5ea9c6ec09600bf8abff9ddddda6116cdcf9`.
- **What ran, per page:** the full page data of T-001 to T-007 (title, S1 to S3, every state, every cable with its full
  label, forced breaks included, the companions) through `build_page`; `kit_coverage_check.py --architecture` and
  `check_layout.py` (report profile, ROAD, no `--centre`), every finding read; a render through `render_png.render`
  (headless Chrome with the draw.io viewer of the VS Code extension 1.19.0), looked at whole and in full-resolution
  crops.
- **Fixes the dry run made to the frame** (all seven re-run after each): the BFF moved up 40 px (MPA cable 3's label
  had no room above the Team servers' title); the Browser tab moved down 20 px and then 20 more, with the App shell
  group raised to 360, so the hydration label fits under the shell and arrow 2 enters the shell below both members;
  the pipelines' deploy to the Team servers routed through the band street (ISR's 73-character label needs a
  horizontal run); the Backend icons put on the 20-px grid; `opacityGroup=1` added to the muted keys (the renders
  showed muted icons at full colour without it); the pivot's caption made a stronger amber (#FFD54F) so it is found at
  a glance; label slides and per-page wraps found and frozen (§ Label slides and wraps).

| page | pivot | kit_coverage_check.py --architecture | check_layout.py | CROSS | COLLINEAR | STRADDLE | OFF-PAGE | DEPTH-STROKE | excluded edges | other soft findings kept |
|---|---|---|---|---|---|---|---|---|---|---|
| CSR | B-SHELL | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SPA | B-ROUTER | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| MPA | E-ROUTER | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SSR | O-COMPOSER | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| SSG | D-INTEGRATION | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| ISR | O-COMPOSER | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |
| RSC | O-COMPOSER | exit 0 (25/25 icons with a caption) | exit 0 | 0 | 0 | 0 | 0 | 0 | L-SAMPLE-net, L-SAMPLE-page, L-SAMPLE-build (the legend samples only) | none |

- **CSR:** pivot B-SHELL, the one amber caption; 9 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **SPA:** pivot B-ROUTER, the one amber caption; 7 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **MPA:** pivot E-ROUTER, the one amber caption; 12 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **SSR:** pivot O-COMPOSER, the one amber caption; 8 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **SSG:** pivot D-INTEGRATION, the one amber caption; 10 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **ISR:** pivot O-COMPOSER, the one amber caption; 5 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
- **RSC:** pivot O-COMPOSER, the one amber caption; 9 muted icons faded with their captions; every label clear of icons, captions, walls, titles and cables; no cable through a title or a caption; the render looked at.
