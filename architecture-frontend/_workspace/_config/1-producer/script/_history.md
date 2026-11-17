# History — 1-producer/script

## 2026-11-17 15:01 — diagram-architecture-io
**Action:** Updated (1 file)
**Notes:** `KIT_FINGERPRINT` set to the digest of the craft kit with S as the default; nothing else in the library changed. T-001.
- _lib/mfe_frame.py

## 2026-11-17 10:51 — diagram-architecture-io
**Action:** Updated (1 file)
**Notes:** `KIT_FINGERPRINT` set to the digest of the craft kit cut to four styles; nothing else in the library changed. T-001.
- _lib/mfe_frame.py

## 2026-11-17 01:20 — diagram-architecture-io
**Action:** Updated (1 file)
**Notes:** The frame library draws each column in its tier's colours (a group white with the column's stroke, the build band dashed), the legend with its area swatches in two columns, and the edge classes in the standard's arrow types; the legend's rows sit on a 10-px grid. Geometry of nodes, routes and labels unchanged. T-001.
- _lib/mfe_frame.py

## 2026-11-17 00:31 — diagram-architecture-io
**Action:** Updated (1 file)
**Notes:** The frame library draws each node from an `art` spec: a crafted icon (`gen_craft`, an image cell) or a generic shape of `PROMPT_ICON.md`; the kit fingerprint covers both. Geometry, routes, labels and classes unchanged. T-001.
- _lib/mfe_frame.py

## 2026-11-16 19:30 — diagram-architecture-io
**Action:** Updated (1 file)
**Notes:** The frame library redrawn in the icon form: every node an icon (`gen_icons.style_p3`) with its NAME as the caption, no subtitles; new geometry, routes and label slides; caption, port and step-number checks; the kit fingerprint; the step number bound to its next word in a wrap. T-001.
- _lib/mfe_frame.py

## 2026-11-16 16:03 — diagram-architecture-io
**Action:** Created (2 files)
**Notes:** The shared frame library and the render helper, imported by each micro-frontend slot's builder; proved by T-001's dry run on all seven pages.
- _lib/mfe_frame.py
- _lib/render_png.py
