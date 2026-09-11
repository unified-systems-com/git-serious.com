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

They come from a running git-serious instance, captured with Playwright at a 1600×1100
viewport, device scale 2, after `networkidle` plus five seconds for the graph panels to
settle. Auth is a minted `sessionid` cookie (see the tap repo's `drive-browser` skill).
Drop new PNGs into `assets/images/shots/` with the same names and rebuild.
