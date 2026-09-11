#!/usr/bin/env python3
"""Render the built site and exercise the carousel.

    verify.py --public public --out /tmp/site-check

Serves ``public/`` on a local port, screenshots the page at desktop and phone
widths, clicks through the carousel, and fails on console errors, horizontal
overflow, or a counter that does not advance. Look at the PNGs afterwards.
"""
from __future__ import annotations

import argparse
import http.server
import pathlib
import socketserver
import threading

from playwright.sync_api import sync_playwright


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--public", default="public")
    ap.add_argument("--out", required=True)
    ap.add_argument("--port", type=int, default=8137)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_):  # keep the report readable
            pass

    handler = lambda *x, **k: Quiet(*x, directory=a.public, **k)  # noqa: E731
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", a.port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h in (("desktop", 1440, 1500), ("phone", 400, 1400)):
            ctx = b.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            errs: list[str] = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.goto(f"http://127.0.0.1:{a.port}/", wait_until="networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=str(out / f"site-{name}.png"))
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > w:
                print(f"{name}: horizontal overflow {sw}px > {w}px"); bad += 1
            if w > 1000:
                def arrived(idx: int) -> None:  # wait until the track has scrolled to slide idx
                    page.wait_for_function(
                        """i => { const t = document.querySelector('.track');
                                  const s = t.querySelectorAll('.slide')[i];
                                  return Math.abs(t.scrollLeft - s.offsetLeft) < 2; }""",
                        arg=idx, timeout=8000)
                    page.wait_for_timeout(300)  # let the IntersectionObserver update the counter
                before = page.text_content(".count")
                page.click(".controls .next"); arrived(1)
                page.click(".controls .next"); arrived(2)
                after = page.text_content(".count")
                n = page.locator(".dots button").count()
                page.click(f".dots li:nth-child({n}) button"); arrived(n - 1)
                last = page.text_content(".count")
                page.screenshot(path=str(out / "site-last-slide.png"))
                print(f"carousel: {before.strip()} -> {after.strip()} -> {last.strip()} ({n} slides)")
                if after.strip() != f"03 / {n:02d}" or last.strip() != f"{n:02d} / {n:02d}":
                    print("carousel counter did not track the scroll"); bad += 1
            if errs:
                print(f"{name}: console errors: {errs}"); bad += 1
            ctx.close()
        b.close()
    srv.shutdown()
    print("OK" if not bad else f"{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
