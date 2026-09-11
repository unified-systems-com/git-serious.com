#!/usr/bin/env python3
"""Capture product screenshots from a running git-serious / TAP instance.

    capture.py --base http://localhost:8040 --session-file /path/skey.txt \
               --pages pages.json --out assets/images/shots

Each page is loaded in headless Chromium with the minted ``sessionid`` cookie,
waited on for networkidle plus a settle period (the graph panels are cytoscape
canvases and need it), the instance badge in the nav is hidden, an optional
scroll pane is positioned on its densest stretch of annotations, and the
viewport is written to ``<out>/<name>.png``. Nothing is clicked; nothing is
written to the instance. Run with the tap-playwright venv python (see SKILL.md).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HIDE_BADGE = r"""(re) => {
  const rx = new RegExp(re); let n = 0;
  for (const el of document.querySelectorAll('nav *, header *')) {
    if (el.children.length === 0 && rx.test(el.textContent.trim())) { el.style.visibility = 'hidden'; n++; }
  }
  return n;
}"""

# Scroll the nearest scrollable ancestor of the matched elements so that the
# viewport-sized window containing the most of them is showing.
SCROLL_DENSE = r"""(sel) => {
  const items = [...document.querySelectorAll(sel)];
  if (!items.length) return {err: 'no matches for ' + sel};
  let c = items[0].parentElement;
  while (c && !(/(auto|scroll)/.test(getComputedStyle(c).overflowY) && c.scrollHeight > c.clientHeight + 50)) c = c.parentElement;
  if (!c) return {err: 'no scroll container'};
  const top = c.getBoundingClientRect().top;
  const ys = items.map(n => n.getBoundingClientRect().top - top + c.scrollTop);
  const H = c.clientHeight; let best = {k: 0, start: 0};
  for (const y of ys) { const k = ys.filter(v => v >= y - 40 && v <= y - 40 + H - 80).length; if (k > best.k) best = {k, start: y - 40}; }
  c.style.scrollBehavior = 'auto'; c.scrollTop = best.start;
  return {matches: ys.length, showing: best.k, scrollTop: c.scrollTop};
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="Instance base URL, e.g. http://localhost:8040")
    ap.add_argument("--session-file", required=True, help="File holding the minted sessionid value")
    ap.add_argument("--pages", required=True, help="JSON list of {name, path, dense?}")
    ap.add_argument("--out", required=True, help="Output directory for <name>.png")
    ap.add_argument("--only", default="", help="Comma-separated page names to capture (default: all)")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1100)
    ap.add_argument("--scale", type=int, default=2, help="Device scale factor (2 = crisp on retina)")
    ap.add_argument("--settle-ms", type=int, default=5000, help="Wait after networkidle for graph panels")
    ap.add_argument("--tz", default="America/Los_Angeles")
    ap.add_argument("--badge-regex", default=r"^\[\s*[\w.-]+\s*\]$", help="Nav text to hide, e.g. the '[ demo-dev ]' instance badge")
    ap.add_argument("--full-page", action="store_true", help="Also write <name>-full.png")
    args = ap.parse_args()

    key = pathlib.Path(args.session_file).read_text().strip()
    pages = json.loads(pathlib.Path(args.pages).read_text())
    if args.only:
        want = set(args.only.split(","))
        pages = [p for p in pages if p["name"] in want]
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    host = args.base.split("//", 1)[-1].split(":")[0].split("/")[0]

    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
            timezone_id=args.tz,
        )
        ctx.add_cookies([{"name": "sessionid", "value": key, "domain": host, "path": "/"}])
        for pg in pages:
            page = ctx.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            ok = False
            for attempt in range(3):  # the dev server occasionally resets a connection mid-run
                try:
                    page.goto(args.base + pg["path"], wait_until="networkidle", timeout=60000)
                    ok = True
                    break
                except Exception as e:  # noqa: BLE001
                    print(f"{pg['name']}: retry {attempt + 1}: {str(e)[:80]}", file=sys.stderr)
                    page.wait_for_timeout(3000)
            if not ok or page.url.startswith("chrome-error"):
                print(f"{pg['name']:16s} FAILED to load", file=sys.stderr)
                failures += 1
                page.close()
                continue
            page.wait_for_timeout(args.settle_ms)
            hidden = page.evaluate(HIDE_BADGE, args.badge_regex)
            dense = page.evaluate(SCROLL_DENSE, pg["dense"]) if pg.get("dense") else None
            if dense:
                page.wait_for_timeout(800)
            page.screenshot(path=str(out / f"{pg['name']}.png"))
            if args.full_page:
                page.screenshot(path=str(out / f"{pg['name']}-full.png"), full_page=True)
            login = "login" in page.url or "Sign in" in page.title()
            print(f"{pg['name']:16s} title={page.title()!r} badge_hidden={hidden} dense={dense} console_errors={len(errors)}"
                  + ("  <-- LOGIN PAGE: session invalid" if login else ""))
            if login:
                failures += 1
            page.close()
        browser.close()
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
