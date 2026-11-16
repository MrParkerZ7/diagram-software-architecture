# Unit spec — micro-frontend-csr-architecture.drawio

> One page: micro-frontends under client-side rendering (CSR), the first load. The item is stored at the slot's root,
> `../micro-frontend-csr-architecture.drawio` (paths here are from the slot's `_workspace/`).
> **Companions (same frame, one picture per file):** `002-micro-frontend-spa/micro-frontend-spa-architecture.drawio` ·
> `003-micro-frontend-mpa/micro-frontend-mpa-architecture.drawio` · `004-micro-frontend-ssr/micro-frontend-ssr-architecture.drawio` ·
> `005-micro-frontend-ssg/micro-frontend-ssg-architecture.drawio` · `006-micro-frontend-isr/micro-frontend-isr-architecture.drawio` ·
> `007-micro-frontend-rsc/micro-frontend-rsc-architecture.drawio`.
> Made by `diagram-architecture-io "micro-frontends under client-side rendering (CSR)" micro-frontend-csr` (prompt master
> `shared/workflows/diagram-generate.md`, type `architecture`, plan ROAD), in a library slot (T-001).

## 1. Purpose

Show where the HTML is produced and where and when the micro-frontends are composed under CSR on the first load: the
browser gets a nearly empty `index.html`, and the **app shell** (the pivot) reads the registry's manifest, loads each
team's remote entry from the CDN and mounts it, at run time. It is one of seven pages drawn on one frame, so a reader can
compare it node for node with the other six and see the composition point move.

## 2. Ownership & cadence

- **Owner:** `claude` (regenerated whole; `edit_mode: regenerate`). Never edited by hand: a hand edit is lost at the
  next build.
- **Cadence:** one-off. Rebuilt when this spec's content changes, or when the frame changes (a new ticket redraws every
  slot; the frame is frozen).

## 3. Structure

The page is the frame's (`../../_workspace/1-producer/analysis/micro-frontend-frame.md`), in this order: the title
banner; the three statement cards; the four columns (Browser, Edge, Origin, Backend) with their groups; the build band;
the cables; the legend; the companions card. This slot gives the frame data only:

- **Title:** `Micro-frontends with CSR: client-side rendering (first load)`.
- **S1 (where the HTML is produced):** `In the browser. The CDN sends a nearly empty index.html; the DOM is built by JavaScript after the shell and the team UIs load.`
- **S2 (where and when composed):** `In the browser, at run time, on the first load: the app shell reads the registry's manifest (an import map or a Module Federation manifest), loads each team's remote entry from the CDN and mounts it.`
- **S3 (trade-off):** `Each team deploys its UI on its own, with no rebuild of the shell. But the first paint waits for several bundles, SEO depends on crawlers running JavaScript, and shared libraries (one React) must stay compatible singleton versions.`
- **Pivot:** B-SHELL. **Muted (9):** B-ROUTER, B-BUS, E-CACHE, O-COMPOSER, O-SRV-A, O-SRV-B, O-SRV-C, K-CMS,
  D-INTEGRATION; G-SERVERS is drawn muted because all its members are. Everything else is active.
- **Companions:** the six files in the header.

### Page text

Every content-node subtitle and every content-cable label on the page. The node NAMEs, container titles, statement
headings, legend and companions heading are frame-static (sourced once in the frame contract's § Frame-static text).
`source` is the Origin of a row of `_origins.md`, or `§ 8` (unverified). A label that states no fact cites the source of
the flow it belongs to.

| where | text | source |
|---|---|---|
| B-PAGE | gets a near-empty index.html | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| B-ROUTER | not used in this first-load view | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| B-SHELL | loads and mounts team UIs at run time | https://martinfowler.com/articles/micro-frontends.html (read 2026-11-16) |
| B-UI-A | own bundle, own deploy | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| B-UI-B | own bundle, own deploy | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| B-UI-C | own bundle, own deploy | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| B-BUS | not used in this first-load view | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| B-SHARED | one React, shared as a singleton | https://module-federation.io/configure/shared.html (read 2026-11-16) |
| E-ROUTER | /api/* to the BFF | § 8 |
| E-CACHE | no HTML to cache | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| E-CDN | index.html, manifest, shell, team bundles | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| O-COMPOSER | no server rendering in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| O-BFF | one API for the browser | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| O-SRV-A | no server rendering in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| O-SRV-B | no server rendering in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| O-SRV-C | no server rendering in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| K-API-A | team data | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| K-API-B | team data | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| K-API-C | team data | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| K-CMS | not used in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| D-REGISTRY | remote manifest / import map | https://module-federation.io/configure/remotes.html (read 2026-11-16) · https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| D-INTEGRATION | no site build in CSR | "Frontend architecture patterns" (the owner's chat with Claude; private, no link; read 2026-11-15) |
| D-CI-A | builds and uploads its UI | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| D-CI-B | builds and uploads its UI | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| D-CI-C | builds and uploads its UI | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) |
| B-PAGE → E-CDN | 1 · 3 · static files: index.html, import map / manifest, shell, team bundles | https://single-spa.js.org/docs/recommended-setup/ (read 2026-11-16) · https://module-federation.io/configure/remotes.html (read 2026-11-16) |
| B-PAGE → B-SHELL | 2 · the shell boots | https://martinfowler.com/articles/micro-frontends.html (read 2026-11-16) |
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
| 2 | B-PAGE → B-SHELL | page |
| 3 | B-SHELL → G-REMOTES | page |
| 4 | B-PAGE → E-ROUTER | net |
| 5 | E-ROUTER → O-BFF | net |
| 6 | O-BFF → G-APIS | net |
| – | G-CI → E-CDN | build |
| – | G-CI → D-REGISTRY | build |
| – | D-REGISTRY → E-CDN | build |

## 4. Derivation

- **The flow, first load:** the browser asks the CDN for the static files (step 1: `index.html`, the import map or
  manifest; step 3: the shell's and each team's bundle, the same cable); the page boots the shell (step 2); the shell
  loads each team's remote entry and mounts it (step 3, the run-time composition: Fowler's run-time integration via
  JavaScript, Module Federation's remote entry, single-spa's mount); the team UIs call the API through the edge router
  and the BFF (steps 4 to 6). Each team's pipeline uploads its bundle and publishes the new version to the registry,
  and the manifest points at it (the import-map deploy of single-spa's recommended setup): the three build cables,
  unnumbered because they stand outside the request's order.
- **The pivot** is B-SHELL, the app shell's run-time loader, where the micro-frontends are composed (G-001 D2).
- **Muted:** the nodes the CSR first load does not use. B-ROUTER and B-BUS belong to the navigation after the first
  load (the SPA page, G-001 D3); the page cache, the page composer and the team servers render no HTML in CSR; the
  integration build makes no site; the headless CMS is not drawn in this example. A group is muted when all its members
  are (G-SERVERS).
- **S3's "first paint waits for several bundles"** is derived (Claude, `_origins.md`): the shell, the manifest and each
  remote entry are fetched before the team UIs draw.

## 5. Presentation

The frame's presentation, unchanged (contract § Colour classes, § Edge classes, § Labels): one ROAD page, 3060 x 1680,
T1 clay + icon cards with the colour class fills, B-SHELL's fill #FFF2CC the only warm one, muted cards faded with
`opacityGroup=1`, net / page / build cables, labels wrapped and slid by the frame's table for `CSR`. The `.drawio` is
written to the slot's root by the builder; its render is `2-generated/artifact/micro-frontend-csr-architecture.png`
(headless Chrome with the draw.io viewer, cropped to the drawing plus 20 px). Nothing on the page is written by hand.

## 6. Inputs

- **The frame contract:** `../../_workspace/1-producer/analysis/micro-frontend-frame.md` (the library's workspace).
- **The frame library:** `../../_workspace/1-producer/script/_lib/mfe_frame.py` (`build_page`) and the render helper
  `../../_workspace/1-producer/script/_lib/render_png.py` (`render`), imported by walking up to the `project: library`
  marker.
- **The 3-diagram kit** through the environment variable `DIAGRAM_KIT` (the prompt master's `shared/prompts/3-diagram`):
  `text/gen_text.py`, `icons/gen_icons.py`, and the gates `kit_coverage_check.py` and `check_layout.py`.
- **The builder:** `1-producer/script/build_micro_frontend_csr.py`.
- **The stored item (output):** `../micro-frontend-csr-architecture.drawio`; the render `2-generated/artifact/micro-frontend-csr-architecture.png`.
- **The page's content:** T-001 § Approach step 3 (`../../../_todo/T-001.md`) and the sources in `_origins.md`.

## 7. Invariants

- Data only: the builder passes the tables of § 3 to `build_page`; every coordinate, style, port, wrap and slide is the
  frame's.
- The `.drawio` holds exactly one `<diagram>`; a rebuild reproduces it byte for byte; its sha256 is in the slot's
  `_config/_manifest.json`.
- Both gates pass: `kit_coverage_check.py` exit 0; `check_layout.py` (report profile, ROAD, no `--centre`) exit 0 with
  0 CROSS, 0 COLLINEAR, 0 STRADDLE, 0 OFF-PAGE, 0 DEPTH-STROKE, and the only excluded edges are the three legend samples
  (the frame's `## Frame proof`, CSR row).
- Exactly one card carries `mfeClass=pivot` (B-SHELL); each card's style holds one `shadow=` key, `shadow=1` on the pivot
  only; every muted card carries `opacity=45`, `textOpacity=60` and `opacityGroup=1`.
- The page text matches § 3 word for word; a subtitle or label no source supports is listed in § 8, never reworded.

## 8. Known gaps

- ⚠ **Unverified (no listed source states it), kept as the plan wrote it:** E-ROUTER's subtitle `/api/* to the BFF` and
  cable 5 `5 · /api routed to the BFF`: an edge router (a reverse proxy) that sends `/api/*` to the BFF is this
  example's deployment, a common setup, not a fact from the sources. The `JSON` of cable 4 and the three example teams
  (Catalog, Cart and orders, Account) are the example's too (`_origins.md`, kind `claude`, assumed).
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
- **No tooltips:** the cards carry no draw.io tooltip (`SPEC_DRIVEN_GENERATION.md` § *Self-explanation*); every card's
  meaning is on its face (NAME and subtitle), and the legend explains the classes.
