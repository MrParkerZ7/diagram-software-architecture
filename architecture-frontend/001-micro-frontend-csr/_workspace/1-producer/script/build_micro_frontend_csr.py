# -*- coding: utf-8 -*-
"""Builder: slot 001, micro-frontends under client-side rendering (CSR), first load.

Spec: ../analysis/spec_micro-frontend-csr-architecture-drawio/micro-frontend-csr-architecture.md
Data only: every coordinate, style, port, label wrap and slide belongs to the library's shared frame
(<library>/_workspace/1-producer/script/_lib/mfe_frame.py), found by walking up to the `project: library` marker.

Writes the item into the slot's root (../../../micro-frontend-csr-architecture.drawio from here), the one write outside
this workspace, then renders 2-generated/artifact/micro-frontend-csr-architecture.png and runs both gates.

    python build_micro_frontend_csr.py [--no-render] [--no-gates]

Environment (never written into a file): DIAGRAM_KIT = the prompt master's shared/prompts/3-diagram folder.
"""
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "micro-frontend-csr-architecture"


def _front(readme):
    """The front matter of a README marker as a dict (flat `key: value` lines only)."""
    try:
        with open(readme, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    out = {}
    for line in text.split("\n")[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def _up_to(kind):
    """The nearest folder at or above this script whose README.md says `project: <kind>`."""
    d = HERE
    while True:
        if _front(os.path.join(d, "README.md")).get("project") == kind:
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("no README.md with 'project: %s' above this builder" % kind)
        d = parent


if not os.path.isfile(os.path.join(os.environ.get("DIAGRAM_KIT", ""), "text", "gen_text.py")):
    raise SystemExit("DIAGRAM_KIT must point to the prompt master's shared/prompts/3-diagram")
LIBRARY = _up_to("library")
WORKSPACE = _up_to("analyze")                       # this slot's _workspace/
SLOT = os.path.dirname(WORKSPACE)
sys.path.insert(0, os.path.join(LIBRARY, "_workspace", "1-producer", "script", "_lib"))
import mfe_frame  # noqa: E402
import render_png  # noqa: E402

ABBR = "CSR"
FULL_NAME = "client-side rendering (first load)"
STATEMENTS = [
    "In the browser. The CDN sends a nearly empty index.html; the DOM is built by JavaScript after the shell and the "
    "team UIs load.",
    "In the browser, at run time, on the first load: the app shell reads the registry's manifest (an import map or a "
    "Module Federation manifest), loads each team's remote entry from the CDN and mounts it.",
    "Each team deploys its UI on its own, with no rebuild of the shell. But the first paint waits for several bundles, "
    "SEO depends on crawlers running JavaScript, and shared libraries (one React) must stay compatible singleton "
    "versions.",
]
ROWS = [  # (node ids, state) - spec section 3, Node states; each node's caption is its frame-static NAME
    ("B-PAGE B-SHARED B-UI-A B-UI-B B-UI-C", "active"),
    ("B-SHELL", "pivot"),
    ("B-ROUTER B-BUS", "muted"),
    ("E-ROUTER E-CDN", "active"),
    ("E-CACHE", "muted"),
    ("O-COMPOSER O-SRV-A O-SRV-B O-SRV-C", "muted"),
    ("O-BFF K-API-A K-API-B K-API-C", "active"),
    ("K-CMS D-INTEGRATION", "muted"),
    ("D-REGISTRY D-CI-A D-CI-B D-CI-C", "active"),
]
CABLES = [  # (n, from, to, class, label) - spec section 3, Cables
    ("1", "B-PAGE", "E-CDN", "net", "1 · 3 · static files: index.html, import map / manifest, shell, team bundles"),
    ("2", "B-PAGE", "G-SHELL", "page", "2 · the shell boots"),
    ("3", "B-SHELL", "G-REMOTES", "page", "3 · load each remote entry, mount it"),
    ("4", "B-PAGE", "E-ROUTER", "net", "4 · team UIs call the API (JSON)"),
    ("5", "E-ROUTER", "O-BFF", "net", "5 · /api routed to the BFF"),
    ("6", "O-BFF", "G-APIS", "net", "6 · the BFF calls the team APIs"),
    ("-", "G-CI", "E-CDN", "build", "each team uploads its own bundle"),
    ("-", "G-CI", "D-REGISTRY", "build", "publishes the new version"),
    ("-", "D-REGISTRY", "E-CDN", "build", "manifest points at it"),
]
COMPANIONS = ["%03d-micro-frontend-%s/micro-frontend-%s-architecture.drawio" % (i, x, x)
              for i, x in ((2, "spa"), (3, "mpa"), (4, "ssr"), (5, "ssg"), (6, "isr"), (7, "rsc"))]


def main(argv):
    states = {}
    for ids, state in ROWS:
        for cid in ids.split():
            states[cid] = state
    drawio = os.path.join(SLOT, NAME + ".drawio")
    info = mfe_frame.build_page(ABBR, FULL_NAME, STATEMENTS, states, CABLES, COMPANIONS, drawio)
    print("[written] %s.drawio in the slot root: %d cells, %d cables, pivot %s" % (NAME, info["cells"], info["cables"],
                                                                                info["pivot"]))
    rc = 0
    if "--no-gates" not in argv:
        for gate, flags in (("kit_coverage_check.py", ["--architecture"]), ("check_layout.py", [])):
            r = subprocess.run([sys.executable, os.path.join(mfe_frame.KIT, gate)] + flags + [drawio],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            print("$ python %s %s<drawio>  -> exit %d" % (gate, "".join(f + " " for f in flags), r.returncode))
            print("\n".join(l for l in r.stdout.splitlines()[1:] if l.strip()) if gate == "check_layout.py"
                  else r.stdout.strip())
            rc = rc or r.returncode
    if "--no-render" not in argv:
        png = os.path.join(WORKSPACE, "2-generated", "artifact", NAME + ".png")
        render_png.render(drawio, png)
        print("[rendered] 2-generated/artifact/%s.png" % NAME)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
