---
project: analyze
type: default
type-version: 2
root: ../../..
---

# 001-micro-frontend-csr workspace

> The work about the CSR micro-frontend diagram: its spec, builder and render.

## What it is

The work about the slot's one item, the CSR micro-frontend diagram [`../micro-frontend-csr-architecture.drawio`](../micro-frontend-csr-architecture.drawio): its unit spec and sources, its builder, and its PNG render.

## Where it fits

It sits in slot `001-micro-frontend-csr` of the [architecture-frontend](../../README.md) library, which keeps the item itself at the slot's root. The page is drawn on the shared micro-frontend frame, which lives in the library's own [`_workspace`](../../_workspace/README.md); the six companion diagrams are the library's slots 002 to 007.

## What only this level knows

- **The spec** [`1-producer/analysis/spec_micro-frontend-csr-architecture-drawio/micro-frontend-csr-architecture.md`](1-producer/analysis/spec_micro-frontend-csr-architecture-drawio/micro-frontend-csr-architecture.md): the CSR page's text, states, cables and their sources (`_origins.md` beside it).
- **The builder** `1-producer/script/build_micro_frontend_csr.py` passes data only to the frame and writes the item into the slot's root, the one write outside this workspace, since the item is what this workspace exists to make; the render goes to `2-generated/artifact/micro-frontend-csr-architecture.png`.

## Working with it

Sample, with `DIAGRAM_KIT` set to the prompt master's `shared/prompts/3-diagram` folder: `python 1-producer/script/build_micro_frontend_csr.py` rebuilds the `.drawio` byte for byte, runs both gates and renders the PNG; `--no-render` skips the PNG.
