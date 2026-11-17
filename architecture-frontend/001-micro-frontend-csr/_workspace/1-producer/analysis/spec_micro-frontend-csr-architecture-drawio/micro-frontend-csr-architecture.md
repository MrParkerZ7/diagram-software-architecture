# Unit spec — micro-frontend-csr-architecture.drawio

> One page: micro-frontends under client-side rendering (CSR), the first load. The item is stored at the slot's root,
> `../micro-frontend-csr-architecture.drawio` (paths here are from the slot's `_workspace/`).
> **Companions (same frame, one picture per file):** `002-micro-frontend-spa/micro-frontend-spa-architecture.drawio` ·
> `003-micro-frontend-mpa/micro-frontend-mpa-architecture.drawio` · `004-micro-frontend-ssr/micro-frontend-ssr-architecture.drawio` ·
> `005-micro-frontend-ssg/micro-frontend-ssg-architecture.drawio` · `006-micro-frontend-isr/micro-frontend-isr-architecture.drawio` ·
> `007-micro-frontend-rsc/micro-frontend-rsc-architecture.drawio`.
> Made by `diagram-architecture-io "micro-frontends under client-side rendering (CSR)" micro-frontend-csr` (prompt master
> `shared/workflows/diagram-generate.md`, type `architecture`, plan ROAD), in a library slot (T-001).
> **Revision 2 (2026-11-16):** redrawn as an architecture page in the prompt master's standard, every part an icon with
> its name as a caption and the numbered arrows carrying the workflow, on the owner's word (*"the diagram workflow should
> be bease with icon arrow workflow relation"*). Revision 1 drew every node as a text card with a subtitle.
> **Revision 4 (2026-11-17):** the areas and the arrow format follow the prompt master's standards, on the owner's word
> (*"diagram areas & and arrow formant wans't correctly"*): the columns take the tier colours, the legend gains its
> area section, the arrows take the standard's types (§ 5). Revision 3 (the same day) drew the icons from the craft
> kit. No node, route or label moved.
> **Revision 5 (2026-11-17):** the craft kit keeps four icon styles (F, G, I, P), on the owner's word (*"I'm still not satisfy with icon style, remove style T Q U D B A off"*); ten icons are drawn in another style (§ 5). No node, route, label, area or arrow moved.
> **Revision 6 (2026-11-17):** the craft kit made S, Sticker, its default style on the owner's word (*"Good use S as default and update skill"*, then *"now update"* this file); all 19 crafted icons are redrawn in S (§ 5). No node, route, label, area or arrow moved.
> **Revision 7 (2026-11-17):** the craft kit made L, Gel, its default on the owner's word (*"I like L more than G, let mark L as default"*), and said a framed style is for a highlight only (*"I think there's fine we could use L/S by default and F/G sytle for only specific parente or hub or something important as hightlit let update diagram about this"*); the 15 ordinary crafted icons are redrawn in L, the four crafted hubs in G, and the legend gains an Icons section (§ 5). No node, route, label, area or arrow moved.

## 1. Purpose

Show where the HTML is produced and where and when the micro-frontends are composed under CSR on the first load: the
browser gets a nearly empty `index.html`, and the app shell's **runtime loader** (the pivot) reads the registry's
manifest, loads each team's remote entry from the CDN and mounts it, at run time. It is one of seven pages drawn on one
frame, so a reader can compare it part for part with the other six and see the composition point move.

## 2. Ownership & cadence

- **Owner:** `claude` (regenerated whole; `edit_mode: regenerate`). Never edited by hand: a hand edit is lost at the
  next build.
- **Cadence:** one-off. Rebuilt when this spec's content changes, or when the frame changes (a new ticket redraws every
  slot; the frame is frozen).

## 3. Structure

The page is the frame's (`../../_workspace/1-producer/analysis/micro-frontend-frame.md`), in this order: the title
banner; the three statement cards; the four columns (Browser, Edge, Origin, Backend) with their groups; the build band;
the arrows; the legend; the companions card. Every part is an icon whose caption is its frame-static NAME. This slot
gives the frame data only:

- **Title:** `Micro-frontends with CSR: client-side rendering (first load)`.
- **S1 (where the HTML is produced):** `In the browser. The CDN sends a nearly empty index.html; the DOM is built by JavaScript after the shell and the team UIs load.`
- **S2 (where and when composed):** `In the browser, at run time, on the first load: the app shell reads the registry's manifest (an import map or a Module Federation manifest), loads each team's remote entry from the CDN and mounts it.`
- **S3 (trade-off):** `Each team deploys its UI on its own, with no rebuild of the shell. But the first paint waits for several bundles, SEO depends on crawlers running JavaScript, and shared libraries (one React) must stay compatible singleton versions.`
- **Companions:** the six files in the header.

### Node states

| state | nodes |
|---|---|
| pivot | B-SHELL (Runtime loader, in the App shell group) |
| active | B-PAGE, B-SHARED, B-UI-A, B-UI-B, B-UI-C, E-ROUTER, E-CDN, O-BFF, K-API-A, K-API-B, K-API-C, D-REGISTRY, D-CI-A, D-CI-B, D-CI-C |
| muted (9) | B-ROUTER, B-BUS, E-CACHE, O-COMPOSER, O-SRV-A, O-SRV-B, O-SRV-C, K-CMS, D-INTEGRATION |

G-SERVERS is drawn muted because all its members are; G-SHELL is not (its runtime loader is the pivot).

### Page text

Every arrow label on the page. The captions (the node NAMEs), container titles, statement headings, legend and
companions heading are frame-static (sourced once in the frame contract's § Frame-static text). `source` is the Origin
of a row of `_origins.md`, or `§ 8` (unverified). A label that states no fact cites the source of the flow it belongs
to.

| where | text | source |
|---|---|---|
| B-PAGE → E-CDN | 1 · 3 · static files: index.html, import map / manifest, shell, team bundles | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) · https://module-federation.io/configure/remotes.html (read 2026-11-16) |
| B-PAGE → G-SHELL | 2 · the shell boots | https://martinfowler.com/articles/micro-frontends.html (read 2026-11-16) |
| B-SHELL → G-REMOTES | 3 · load each remote entry, mount it | https://module-federation.io/configure/remotes.html (read 2026-11-16) · https://single-spa.js.org/docs/building-applications/ (read 2026-11-16) |
| B-PAGE → E-ROUTER | 4 · team UIs call the API (JSON) | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| E-ROUTER → O-BFF | 5 · /api routed to the BFF | § 8 |
| O-BFF → G-APIS | 6 · the BFF calls the team APIs | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| G-CI → E-CDN | each team uploads its own bundle | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| G-CI → D-REGISTRY | publishes the new version | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| D-REGISTRY → E-CDN | manifest points at it | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |

### Cables

| n | from → to | class |
|---|---|---|
| 1 (and 3) | B-PAGE → E-CDN | net |
| 2 | B-PAGE → G-SHELL | page |
| 3 | B-SHELL → G-REMOTES | page |
| 4 | B-PAGE → E-ROUTER | net |
| 5 | E-ROUTER → O-BFF | net |
| 6 | O-BFF → G-APIS | net |
| – | G-CI → E-CDN | build |
| – | G-CI → D-REGISTRY | build |
| – | D-REGISTRY → E-CDN | build |

## 4. Derivation

- **The flow, first load:** the browser asks the CDN for the static files (step 1: `index.html`, the import map or
  manifest, and the shell's bundle); the page boots the app shell (step 2); the shell's runtime loader fetches each
  team's remote entry from the CDN and mounts it (step 3, the run-time composition: Fowler's run-time integration via
  JavaScript, Module Federation's remote entry, single-spa's mount); the team UIs call the API through the edge router
  and the BFF (steps 4 to 6). Step 3's fetch of the remote entries travels on the same arrow as step 1 (§ 8). Each
  team's pipeline uploads its bundle and publishes the new version to the registry, and the manifest points at it (the
  import-map deploy of single-spa's recommended setup): the three build arrows, unnumbered because they stand outside
  the request's order.
- **The pivot** is B-SHELL, the app shell's runtime loader, where the micro-frontends are composed (G-001 D2). Step 2
  enters the App shell group, and step 3 leaves from the loader.
- **Muted:** the parts the CSR first load does not use. B-ROUTER and B-BUS belong to the navigation after the first
  load (the SPA page, G-001 D3); the page cache, the page composer and the team servers render no HTML in CSR; the
  integration build makes no site; the headless CMS is not drawn in this example. A group is muted when all its members
  are (G-SERVERS).
- **S3's "first paint waits for several bundles"** is derived (Claude, `_origins.md`): the shell, the manifest and each
  remote entry are fetched before the team UIs draw.

## 5. Presentation

The frame's presentation, unchanged (contract § Nodes, § Colour classes, § Edge classes, § Labels): one ROAD page,
3240 x 1840; every part an icon with its NAME as the caption under it: 19 crafted icons (image cells from the craft kit,
`gen_craft`, in the style their category maps to) and 6 generic shapes of `PROMPT_ICON.md` (the edge router, the page
composer, the three team servers, the page cache), as the contract's § Nodes lists them (revision 3, 2026-11-17: the
clay glyphs of revision 2 are gone); the caption's tint is the class (team, platform), the pivot's caption the one amber pill (#FFD54F), muted icons faded
(`opacity=40;textOpacity=40;opacityGroup=1`); net / page / build arrows, labels wrapped and slid by the frame's table
for `CSR`. The `.drawio` is written to the slot's root by the builder; its render is
`2-generated/artifact/micro-frontend-csr-architecture.png` (headless Chrome with the draw.io viewer, cropped to the
drawing plus 20 px). Nothing on the page is written by hand.

**Icon styles (revision 5).** The craft kit keeps four styles. On this page: F for the browser tab, runtime loader, client router, the three team UIs, the shared libraries, the CDN and the headless CMS; P for the event bus, the BFF, the three team APIs and the registry; G for the four pipelines and the integration build. The event bus, the BFF and the APIs were string art (T), the CMS paper-cut (A) and the pipelines embroidery (B) in revision 3.

**Icon style (revision 6).** The craft kit's default is S, Sticker: no tile, a die-cut glyph with a white border and a soft shadow, in the kit's own colour for the subject. It keeps three styles (S, F, G), I and P are gone, and every category maps to S, so all 19 crafted icons on this page are S. This supersedes the per-category styles of revision 5. The six generic shapes (the edge router, the page composer, the three team servers, the page cache) are unchanged.

**Icon style and highlight (revision 7).** The craft kit's default is L, Gel: no tile, a glossy jelly sticker with a white border, in the kit's own colour for the subject; S stays as the flat alternative. A framed style (G, or F) is only for a highlight, so this page draws its four crafted hubs (the browser tab, the CDN, the BFF and the registry) in G, a navy tile with a gold rim, and its other 15 crafted icons in L; the legend's Icons section says what a framed icon is, with a sample. This supersedes the S of revision 6. The six generic shapes (the edge router, the page composer, the three team servers, the page cache) are unchanged.

**Areas and arrows (revision 4).** Each column is drawn in the colour of its tier, from `PROMPT_ARROW_STYLE.md` § Component
Color Standards → Subnet Types: the Browser is *Client / Outside* (gray), the Edge *Public* (green), the Origin
*Compute / App* (blue), the Backend *Integration* (amber); the build band is outside the request path, drawn dashed in
gray (`PROMPT_CONTAINER.md` § Frame Colors by Purpose, the Optional row). A group inside a column is white with that
column's stroke. An HTTP call is a `classic` arrow with `flowAnimation=1`, an in-page call an `open` dotted arrow,
a build link a `classic` long-dashed arrow. The legend holds the Component Legend (the five area colours and the caption
colours) and the Arrow Legend, as the standard requires of an architecture page.

## 6. Inputs

- **The frame contract:** `../../_workspace/1-producer/analysis/micro-frontend-frame.md` (the library's workspace).
- **The frame library:** `../../_workspace/1-producer/script/_lib/mfe_frame.py` (`build_page`) and the render helper
  `../../_workspace/1-producer/script/_lib/render_png.py` (`render`), imported by walking up to the `project: library`
  marker.
- **The 3-diagram kit** through the environment variable `DIAGRAM_KIT` (the prompt master's `shared/prompts/3-diagram`):
  `text/gen_text.py`, `icons/craft/gen_craft.py` (the crafted icons), and the gates `kit_coverage_check.py` and
  `check_layout.py`.
- **The builder:** `1-producer/script/build_micro_frontend_csr.py`.
- **The stored item (output):** `../micro-frontend-csr-architecture.drawio`; the render `2-generated/artifact/micro-frontend-csr-architecture.png`.
- **The page's content:** T-001 § Approach step 3 (`../../../_todo/T-001.md`) and the sources in `_origins.md`.

## 7. Invariants

- Data only: the builder passes the tables of § 3 to `build_page`; every coordinate, style, port, wrap and slide is the
  frame's.
- The `.drawio` holds exactly one `<diagram>`; a rebuild reproduces it byte for byte; its sha256 (of the LF bytes) is in
  the slot's `_config/_manifest.json`.
- Both gates pass: `kit_coverage_check.py --architecture` exit 0 (25/25 icons with a caption, no card); `check_layout.py`
  (report profile, ROAD, no `--centre`) exit 0 with 0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE, and
  the only excluded edges are the three legend samples (the frame's `## Frame proof`, CSR row).
- Exactly one icon carries `mfeClass=pivot` (B-SHELL); every icon's caption sits under it
  (`verticalLabelPosition=bottom`), one line, no subtitle; every muted icon carries `opacity=40`, `textOpacity=40` and
  `opacityGroup=1`.
- The page text matches § 3 word for word; a label no source supports is listed in § 8, never reworded.

## 8. Known gaps

- ⚠ **Unverified (no listed source states it), kept as the plan wrote it:** arrow 5 `5 · /api routed to the BFF`: an
  edge router (a reverse proxy) that sends `/api/*` to the BFF is this example's deployment, a common setup, not a fact
  from the sources. The `JSON` of arrow 4 and the three example teams (Catalog, Cart and orders, Account) are the
  example's too (`_origins.md`, kind `claude`, assumed).
- **Step 3 has no arrow of its own to the CDN:** the runtime loader's fetch of each team's remote entry travels on arrow
  1 (`1 · 3 · …`), which is why that arrow carries both numbers; arrow 3 is the mount inside the page.
- **The stored item is outside this workspace:** the builder writes `../micro-frontend-csr-architecture.drawio` into the
  slot's root, the one write outside its workspace, because the item is what this workspace exists to make (prompt
  master `LIBRARY.md` § 2a; T-008 records the lesson there). The slot's `_config/_manifest.json` (kind `storage`) lists
  it; this workspace's `2-generated/artifact/` manifest binds only the PNG.
- **Spec-folder slug:** the folder is named after the item (`spec_micro-frontend-csr-architecture-drawio/`), while this
  workspace's stage manifest's generated entry is the render (`.png`); `SPEC_DRIVEN_GENERATION.md` rule 5 would derive
  `spec_micro-frontend-csr-architecture-png/` from it. No spec checker is installed here, so it is a known mismatch
  (T-008 records it).
- **No `_discover.md`** in `2-generated/artifact/`'s config: it is the `discover` command's catalog, and no `discover`
  ran; `sync` would name it.
- **The owner's chat is private:** `_origins.md` cites it by title and the date read, with no link; the public pages
  were re-read on 2026-11-16 (the plan read them on 2026-11-15).
- **The craft kit is not committed in the prompt master yet (2026-11-17):** the crafted icons come from
  `icons/craft/` of the master's working tree. `KIT_FINGERPRINT` in the frame makes a build refuse to write if the kit's
  output differs, and the frame's `## Frame proof` is re-run when the master commits the kit.
- **L for the ordinary icons and G for the hubs is Claude's reading (2026-11-17), for the owner to change:** the owner said *"I like L more than G, let mark L as default"*, then that L or S is the default and F or G is for *"specific parente or hub or something important"*. He named no part, so Claude took the page's crafted hubs (the parts its arrows meet at: the 160 and 120 icons) as the highlight, chose G over F because a navy tile with a gold rim stands out of the L icons on a light and a dark ground, and left the pivot to its amber caption. The pipeline icon, a flat row of three circles, is small beside the others in L; the owner may want it redrawn taller. The owner may still not be satisfied with the style.
- **Two tier choices are Claude's reading (2026-11-17), for the owner to change:** the Backend is an *Integration* tier
  (the team APIs behind the BFF, with the headless CMS), not a data tier; the build band takes the *Optional* row
  (dashed gray) because build and deploy are outside the request path, and the standard has no build tier. The
  frame's contract, § Containers, says the same.
- **The routes were not redrawn:** a few cables still bend in a street (arrow 5 steps once between the edge router
  and the BFF), because the frame's seven pages share one set of ports; the standard's straight-line default gives way
  to the frame's reserved streets (`PROMPT_CITY_PLAN_LAYOUT.md`, a ROAD page).
- **No tooltips:** the icons carry no draw.io tooltip (`SPEC_DRIVEN_GENERATION.md` § *Self-explanation*); each part is
  named by its caption, the arrows say what moves, and the legend explains the classes.
