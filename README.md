# OCBC NISP — Hosted Prototype

A GitHub-Pages-hostable HTML prototype that stitches the 6 self-contained
screen prototypes under `../recreate-*/` into a single navigable site.

## What's here

```
prototype/
├── index.html                   ← landing page (grid of phone thumbnails)
├── dashboard.html               ← DashboardActivity · HOME tab
├── investment.html              ← DashboardMenuActivity · Investment
├── forex.html                   ← ForexPageActivity · Table + Graph tabs
├── qr-scan.html                 ← VisionScanActivity
├── qr-input.html                ← PurchaseLandingPageActivity · Pay To
├── topup.html                   ← DashboardMenuActivity · Top Up & Pay
├── reward.html                  ← DashboardActivity · Rewards tab
├── thumbs/                ← thumbnails used by the index grid
├── wire-links.py                ← re-builds the 7 pages from canonical sources
└── README.md                    ← this file
```

## How it's built

Each `*.html` (except `index.html`) is a **single-page prototype** — a copy
of the corresponding canonical prototype from `../recreate-*/`, with:

1. The old `width=360, ..., user-scalable=no` viewport meta replaced with
   `width=device-width, initial-scale=1.0`.
2. Inter-screen `href="#"` links rewritten to point to the matching page
   in this folder.
3. A small responsive CSS block injected at the end of `<head>`:
   - **Desktop (> 480px)**: body is 360px wide and centered on a neutral
     page background. The phone has a subtle box-shadow.
   - **Mobile (≤ 480px)**: body fills the viewport. The phone stays at
     360px max-width with the box-shadow removed.

`index.html` is a separate landing page with a grid of phone-shaped
thumbnails linking to the 6 screens.

## Link map (16 wired)

| From | Element | To |
|---|---|---|
| `index` | dashboard thumbnail | `dashboard.html` |
| `index` | investment thumbnail | `investment.html` |
| `index` | forex thumbnail | `forex.html` |
| `index` | qr-scan thumbnail | `qr-scan.html` |
| `index` | qr-input thumbnail | `qr-input.html` |
| `index` | topup thumbnail | `topup.html` |
| `index` | reward thumbnail | `reward.html` |
| `dashboard` | bottom-nav "Rewards" | `reward.html` |
| `dashboard` | bottom-nav QRIS FAB | `qr-scan.html` |
| `dashboard` | "Investment" tile | `investment.html` |
| `dashboard` | "Top Up & Pay" tile | `topup.html` |
| `investment` | toolbar ← back | `dashboard.html` |
| `forex` | toolbar ← back | `dashboard.html` |
| `qr-scan` | × close | `dashboard.html` |
| `qr-input` | toolbar ← back | `qr-scan.html` |
| `reward` | bottom-nav "Home" | `dashboard.html` |
| `reward` | bottom-nav "Rewards" | `reward.html` (self) |
| `reward` | bottom-nav QRIS FAB | `qr-scan.html` |

### No-op links (sub-screens we don't have)

These intentionally stay as `href="#"` because the destination is not
built yet: dashboard "Transfer" / "Top Up & Pay" / "Request Money" /
"e-Commerce" / "All Menus" tiles; reward "See Details" / "See Mission
Now" / "My Orders" / "Poinseru" / "Voyage Miles" / "Refer a friend" /
"Beyond Banking" / "Latest Promos"; qr-scan "Show QR" / "Receive
Transfer" tiles.

## How to host on GitHub Pages

1. `git push` to GitHub.
2. Settings → Pages → branch `main`, root.
3. Visit `https://<user>.github.io/<repo>/recreate/prototype/` (or move
   `prototype/` to the repo root for a cleaner URL).

## Regenerating from canonical sources

```bash
cd prototype
python3 wire-links.py
```

The script is **idempotent**: each run starts fresh from the canonical
sources, applies the link rewrites, and re-injects the responsive CSS.
If a canonical source changes significantly, the script will print
`WARN:` lines for any operation that no longer matches.
