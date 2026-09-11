# git-serious.com

Landing site for [git-serious](https://github.com/unified-systems-com/git-serious-tap).
Built with [Hugo](https://gohugo.io), served by GitHub Pages.

## Local

    brew install hugo
    hugo server          # http://localhost:1313

## Where things live

- `content/_index.md` — all the copy. Structured bits (headline, status, the numbered
  lists, concepts, image captions) are in the front matter; the "Why" prose is the body.
- `layouts/home.html` — the single-page layout. `layouts/_partials/` has head, nav, footer, figure.
- `assets/css/main.css` — the one stylesheet. Palette and grid motif match unified-systems.com.
- `assets/images/shots/` — carousel screenshots, 1600×1100 at 2x. Hugo resizes and converts them to WebP at build. Captions are the `slides` list in `content/_index.md`.
- `static/CNAME` — the custom domain. `static/favicon.svg`.
- `.github/workflows/hugo.yml` — builds and deploys on push to `main`.

## Deploy

1. Push to GitHub. In the repo settings, set **Pages → Source** to **GitHub Actions**.
2. Under **Pages → Custom domain**, enter `git-serious.com` and enable **Enforce HTTPS**
   once the certificate is issued.
3. DNS: `A` records on the apex to GitHub Pages (`185.199.108.153`, `.109.153`, `.110.153`,
   `.111.153`) and a `CNAME` for `www` pointing at `<org>.github.io`.

## Refreshing the screenshots

Run the `site-screenshots` skill (`.claude/skills/site-screenshots/SKILL.md`). It finds a
running git-serious instance, mints a session cookie, captures each route in
`pages.json` with Playwright at 1600×1100 (2x), writes the slide taglines, rebuilds, and
verifies the carousel. Drop-in replacement PNGs go in `assets/images/shots/`.
