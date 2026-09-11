---
name: site-screenshots
description: Refresh the git-serious.com carousel — capture product screenshots from a running git-serious / TAP instance in headless Chromium with a minted session cookie, write or update the slide taglines in content/_index.md, rebuild, and verify the carousel. Use when the product UI has changed, a new page deserves a slide, or someone asks to "update the screenshots", "add a slide", or "refresh the carousel".
argument-hint: [page names to recapture, or "all"]
---

# Refresh the site screenshots and taglines

The carousel on git-serious.com is eight viewport captures of the running product
plus a title and one or two sentences for each. Everything lives in this repo:

- `assets/images/shots/<name>.png` — the images (1600×1100 viewport at 2x = 3200×2200).
- `content/_index.md` → `slides:` — order, `src`, `title`, `text`, `alt` per slide.
- `.claude/skills/site-screenshots/pages.json` — which product routes map to which names.
- `capture.py`, `verify.py` next to this file — the two scripts.

Hugo resizes to WebP at build, so drop in PNGs and rebuild. Never commit `public/`.

## 1. Find a running instance

The product is auth-walled and the demo grid is live: **screenshots only, click
nothing on the graphs, no writes, no restarts.**

- Ask the session that owns the demo stack (it has been `demo-dev`; use ListAgents,
  then SendMessage) for the base URL and worktree. Or look yourself: TAP instances are
  Docker-published ports that redirect `/` to `/auth/passkey/login/`:
  ```bash
  lsof -nP -iTCP -sTCP:LISTEN | grep com.docke
  curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" http://localhost:8040/
  ```
- The worktree matters because the session-minting script runs inside that stack's
  `web` container. Its `WEB_PORT` is in the worktree's `.env.local`.

## 2. One-time browser setup (idempotent)

```bash
VENV="$HOME/.cache/tap-playwright/venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip playwright
  "$VENV/bin/python" -m playwright install chromium
fi
```

## 3. Mint a session cookie

Humans log in with a passkey; a headless browser cannot. The tap repo's
`drive-browser` skill ships a DEV-ONLY script that creates a real Django session for
the `admin` user (it refuses to run unless `settings.DEBUG` is true). Run it inside
the stack's web container and keep the key in the scratchpad, never in the repo:

```bash
TAP=/Users/george/tap-sessions/demo-dev          # the worktree from step 1
SKEY_FILE="$SCRATCHPAD/skey.txt"
( cd "$TAP" && scripts/dc exec -T web uv run python manage.py shell \
    < .claude/skills/drive-browser/mint_session.py ) | grep SESSIONKEY | cut -d= -f2 > "$SKEY_FILE"
test -s "$SKEY_FILE" && echo minted
```

Mint once per run. If a capture prints `LOGIN PAGE: session invalid`, mint again.

## 4. Capture

```bash
"$VENV/bin/python" .claude/skills/site-screenshots/capture.py \
  --base http://localhost:8040 --session-file "$SKEY_FILE" \
  --pages .claude/skills/site-screenshots/pages.json \
  --out assets/images/shots            # add --only tap-lanes,org to redo a few
```

What the script does, so you can tell when it has not: waits for `networkidle` plus
5 s (cytoscape canvases settle slowly), hides the `[ instance ]` badge in the nav,
scrolls any pane named by a page's `dense` selector to the stretch with the most
annotations (the zizmor workflow page opens on its *first* finding, which shows one
margin note; the dense window shows four), then writes the 1600×1100 viewport. The
dev server sometimes resets a connection mid-run; the script retries three times.

**Look at every PNG with the Read tool.** Check for: a login page, a blank or
half-rendered graph (increase `--settle-ms`), stale data you would not want public,
and that the badge is gone. Recapture the ones that are wrong with `--only`.

Adding a page: append `{name, path}` to `pages.json`, capture it, then add a slide.
Ask the demo owner which routes are worth showing; they know what is new.

## 5. Write the taglines

Each slide in `content/_index.md` has:

```yaml
  - src: images/shots/<name>.png
    title: Four to six words, ending in a period.
    text: One or two sentences. What the reader is looking at and why it matters.
    alt: A plain description of the visible layout for screen readers.
```

Rules, learned the first time round:

- **README voice.** Plain, a little dry, first-person asides allowed. No marketing
  adjectives, no exclamation marks.
- **Describe what is visible.** The title names the view; the text says what it shows
  and what question it answers. Do not describe what a badge colour or number means
  unless the product owner has confirmed it.
- **No numbers that drift.** Finding counts, run counts, dates and version strings
  change daily on the demo grid. Write "every finding", not "155 findings". A stable
  structural count ("twenty-four repositories") is fine if it is really stable.
- **Story order.** One repo → whole org → what moved → findings across the org → one
  file → one finding → workflow anatomy → the plumbing. Zoom out, then drill in, then
  show the machinery underneath. Put a new slide where it fits that arc.
- **Alt text is not the caption.** It describes the picture's layout (tables, graph,
  code pane), not the pitch.
- The first slide is the hero: it is eager-loaded and becomes the `og:image`.

## 6. Build and verify

```bash
hugo --gc --minify
"$VENV/bin/python" .claude/skills/site-screenshots/verify.py --public public --out "$SCRATCHPAD/site-check"
```

`verify.py` fails on console errors, horizontal overflow at 400 px, or a carousel
counter that does not advance. Then look at `site-desktop.png`, `site-phone.png` and
`site-last-slide.png`. Send the desktop render to the user with SendUserFile.

## 7. Ship

Commit the PNGs and `content/_index.md` together with a message that says which
slides changed and why. Pushing `main` deploys through `.github/workflows/hugo.yml`.
