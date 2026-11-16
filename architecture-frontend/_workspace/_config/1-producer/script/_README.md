# 1-producer/script — do-not-run register

This unit holds no builder of its own. Every script here is a shared helper or a throwaway:

| script | what it is | run it? |
|---|---|---|
| `_lib/mfe_frame.py` | the shared micro-frontend frame (`build_page`); imported by each slot's builder (`<slot>/_workspace/1-producer/script/build_*.py`) | **no** — a library, not a builder |
| `_lib/render_png.py` | the PNG render helper (`render`); imported by each slot's builder | **no** — a library, not a builder |
| `🚫frame_dryrun.py` | T-001's dry run of the frame on all seven pages (git-ignored, may be absent) | **no** — throwaway; it rewrites the label table in `mfe_frame.py`, which is frozen |

Both helpers need `DIAGRAM_KIT` (the prompt master's `shared/prompts/3-diagram`) in the environment, never in a file.
