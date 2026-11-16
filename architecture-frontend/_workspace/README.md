---
project: analyze
type: default
type-version: 2
root: ../..
---

# architecture-frontend workspace

> The control centre of the architecture-frontend library: the work its diagrams share.

## What it is

The library's own project workspace, its control centre: the work that serves more than one of its diagrams. Today that is the shared micro-frontend frame, the one page layout that the seven micro-frontend diagrams (CSR, SPA, MPA, SSR, SSG, ISR, RSC) are all drawn from, so that they compare node for node.

## Where it fits

It sits at the root of the [architecture-frontend](../README.md) library, beside its storage slots, under the [workspace root](../../README.md). A diagram is a slot of the library; the work about one diagram (its spec, builder and render) is in that slot's own `_workspace/`, and only what several slots share is here.

## What only this level knows

- **The frame contract**, [`1-producer/analysis/micro-frontend-frame.md`](1-producer/analysis/micro-frontend-frame.md): the grid, the containers and nodes, the colour and edge classes, every route and label slide, the legend, and the dry-run proof on all seven pages. It is frozen: a change becomes a new ticket that redraws the slots.
- **The frame library** `1-producer/script/_lib/mfe_frame.py` (`build_page`) and the **render helper** `1-producer/script/_lib/render_png.py` (`render`). Neither is run on its own; the script unit's do-not-run register says so.
- **Environment, never committed:** `DIAGRAM_KIT` points at the prompt master's `shared/prompts/3-diagram` folder; the render helper finds Chrome or Edge and the draw.io `viewer.min.js` itself, or takes `CHROME_PATH` and `DRAWIO_VIEWER_JS`.

## Working with it

A slot's builder imports the frame by walking up to the library's `project: library` marker and passes data only. Sample, from the library folder with `DIAGRAM_KIT` set: `python 001-micro-frontend-csr/_workspace/1-producer/script/build_micro_frontend_csr.py` rebuilds the CSR diagram in its slot and renders its PNG.
