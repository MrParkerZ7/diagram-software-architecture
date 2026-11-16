# 1-producer/script — do-not-run register

| script | what it is | run it? |
|---|---|---|
| `build_micro_frontend_csr.py` | the builder of `../micro-frontend-csr-architecture.drawio` and its PNG (named by `2-generated/artifact`'s manifest) | yes, with `DIAGRAM_KIT` set; `--no-render` skips the PNG |

Nothing here is do-not-run. The shared helpers it imports are registered in the library's own `_workspace/`.
