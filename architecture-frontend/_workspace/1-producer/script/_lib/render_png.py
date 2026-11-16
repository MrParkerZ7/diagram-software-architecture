# -*- coding: utf-8 -*-
"""Render a one-page .drawio to a PNG with headless Chrome (or Edge) and the local draw.io viewer.

A shared helper under _lib/, never run on its own: a slot's builder calls render(drawio_path, png_path).
Everything machine-specific is found at run time, never written into a file:
  * the viewer: DRAWIO_VIEWER_JS, else the newest
    <home>/.vscode/extensions/hediet.vscode-drawio-*/drawio/src/main/webapp/js/viewer.min.js
  * the browser: CHROME_PATH, else Google\\Chrome\\Application\\chrome.exe and then
    Microsoft\\Edge\\Application\\msedge.exe under %ProgramFiles%, %ProgramFiles(x86)% and %LOCALAPPDATA%, else
    chrome / msedge / chromium on the absolute PATH entries only.
The page is drawn at zoom 1 with no fit, screenshotted, and cropped with Pillow to the drawn content plus 20 px.
"""
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

MARGIN = 20


class RenderError(SystemExit):
    pass


def _version_key(path):
    m = re.search(r"hediet\.vscode-drawio-(\d+(?:\.\d+)*)", path.replace("\\", "/"))
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


def find_viewer():
    v = os.environ.get("DRAWIO_VIEWER_JS")
    if v:
        if os.path.isfile(v):
            return v
        raise RenderError("render_png: DRAWIO_VIEWER_JS is set but names no file")
    pat = os.path.join(os.path.expanduser("~"), ".vscode", "extensions", "hediet.vscode-drawio-*", "drawio", "src",
                       "main", "webapp", "js", "viewer.min.js")
    found = sorted(glob.glob(pat), key=_version_key, reverse=True)
    if found:
        return found[0]
    raise RenderError("render_png: no draw.io viewer - set DRAWIO_VIEWER_JS, or install the hediet.vscode-drawio "
                      "extension (looked for <home>/.vscode/extensions/hediet.vscode-drawio-*/.../js/viewer.min.js)")


def find_browser():
    c = os.environ.get("CHROME_PATH")
    if c:
        if os.path.isfile(c):
            return c
        raise RenderError("render_png: CHROME_PATH is set but names no file")
    roots = [os.environ.get(k) for k in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
    for rel in (os.path.join("Google", "Chrome", "Application", "chrome.exe"),
                os.path.join("Microsoft", "Edge", "Application", "msedge.exe")):
        for r in roots:
            if r and os.path.isfile(os.path.join(r, rel)):
                return os.path.join(r, rel)
    names = ("chrome.exe", "msedge.exe", "google-chrome", "chromium", "chromium-browser", "msedge")
    for d in os.environ.get("PATH", "").split(os.pathsep):
        if not d or not os.path.isabs(d):
            continue                                   # an empty or relative entry would search the current folder
        for n in names:
            p = os.path.join(d, n)
            if os.path.isfile(p):
                return p
    raise RenderError("render_png: no browser - set CHROME_PATH (looked under %ProgramFiles%, %ProgramFiles(x86)% "
                      "and %LOCALAPPDATA% for Chrome and Edge, then on the absolute PATH entries)")


def _page_size(xml):
    m = re.search(r'pageWidth="(\d+)"\s+pageHeight="(\d+)"', xml)
    return (int(m.group(1)), int(m.group(2))) if m else (3000, 2000)


def render(drawio_path, png_path):
    """Draw `drawio_path` (one page) and write the cropped PNG to `png_path`. Returns png_path."""
    from PIL import Image, ImageChops
    xml = open(drawio_path, "rb").read().decode("utf-8")
    pw, ph = _page_size(xml)
    viewer, browser = find_viewer(), find_browser()
    webapp = os.path.dirname(os.path.dirname(os.path.abspath(viewer)))
    cfg = {"toolbar": "", "nav": False, "resize": True, "lightbox": False, "border": 10, "fit": False, "zoom": 1,
           "xml": xml}
    div = '<div class="mxgraph" data-mxgraph="%s"></div>' % html.escape(json.dumps(cfg), quote=True)
    work = tempfile.mkdtemp(prefix="mfe-render-")
    try:
        page = ('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;'
                'background:#FFFFFF}</style></head><body>%s<script>window.IMAGE_PATH=%s;window.DRAWIO_BASE_URL=%s;'
                '</script><script src="%s"></script></body></html>'
                % (div, json.dumps(_uri(os.path.join(webapp, "img"))), json.dumps(_uri(webapp)), _uri(viewer)))
        hp = os.path.join(work, "page.html")
        with open(hp, "wb") as f:
            f.write(page.encode("utf-8"))
        shot = os.path.join(work, "shot.png")
        args = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars",
                "--allow-file-access-from-files", "--user-data-dir=%s" % os.path.join(work, "profile"),
                "--window-size=%d,%d" % (pw + 100, ph + 100), "--virtual-time-budget=15000",
                "--screenshot=%s" % shot, _uri(hp)]
        try:
            subprocess.run(args, capture_output=True, timeout=180)
        except (OSError, subprocess.SubprocessError) as e:
            raise RenderError("render_png: the browser could not run (%s)" % type(e).__name__)
        if not os.path.isfile(shot):
            raise RenderError("render_png: the browser wrote no screenshot")
        img = Image.open(shot).convert("RGB")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        box = ImageChops.difference(img, bg).getbbox()
        if not box:
            raise RenderError("render_png: the viewer drew nothing")
        x0, y0, x1, y1 = box
        crop = img.crop((max(0, x0 - MARGIN), max(0, y0 - MARGIN), min(img.width, x1 + MARGIN),
                         min(img.height, y1 + MARGIN)))
        os.makedirs(os.path.dirname(os.path.abspath(png_path)), exist_ok=True)
        crop.save(png_path, "PNG", optimize=True)
        return png_path
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _uri(path):
    import pathlib
    return pathlib.Path(os.path.abspath(path)).as_uri()
