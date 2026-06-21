#!/usr/bin/env python3
"""
Single-page prototype packager.

For each canonical prototype in ../recreate-*/X.html:
  1. Copy it into prototype/X.html.
  2. Replace the old width=360 viewport meta with width=device-width.
  3. Wire up the inter-screen hrefs.
  4. Inject a small responsive CSS block that centers the 360px phone
     on desktop and fills the viewport on mobile (≤ 480px).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(__file__).resolve().parent

WIRING = [
    ("dashboard.html", ROOT / "recreate-dashboard" / "dashboard.html", [
        ('<a class="nav-item" href="#">\n          <span class="icon">\n            <svg viewBox="0 0 24 24" aria-hidden="true">\n              <rect x="3" y="9" width="18" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/>\n              <path d="M3 13h18M12 9v13" stroke="currentColor" stroke-width="1.6"/>\n              <path d="M12 9c-2 0-3-1-3-3V4h6v2c0 2-1 3-3 3z" fill="currentColor"/>\n            </svg>\n          </span>\n          <span>Rewards</span>',
         '<a class="nav-item" href="reward.html">\n          <span class="icon">\n            <svg viewBox="0 0 24 24" aria-hidden="true">\n              <rect x="3" y="9" width="18" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/>\n              <path d="M3 13h18M12 9v13" stroke="currentColor" stroke-width="1.6"/>\n              <path d="M12 9c-2 0-3-1-3-3V4h6v2c0 2-1 3-3 3z" fill="currentColor"/>\n            </svg>\n          </span>\n          <span>Rewards</span>'),
        ('<div class="fab" role="button" aria-label="Scan QR">',
         '<a class="fab" role="button" aria-label="Scan QR" href="qr-scan.html">'),
        ('<!-- 3 Investment -->\n          <a class="qa-tile" href="#">\n            <span class="icon">\n              <svg viewBox="0 0 32 32" aria-hidden="true">\n                <path d="M16 4C12 8 8 10 8 16a8 8 0 0016 0c0-6-4-8-8-12z" fill="currentColor"/>\n                <text x="16" y="14" text-anchor="middle" font-size="6" fill="#fff" font-family="sans-serif" font-weight="700">Rp</text>\n              </svg>\n            </span>\n            <span class="label">Investment</span>\n          </a>',
         '<!-- 3 Investment -->\n          <a class="qa-tile" href="investment.html">\n            <span class="icon">\n              <svg viewBox="0 0 32 32" aria-hidden="true">\n                <path d="M16 4C12 8 8 10 8 16a8 8 0 0016 0c0-6-4-8-8-12z" fill="currentColor"/>\n                <text x="16" y="14" text-anchor="middle" font-size="6" fill="#fff" font-family="sans-serif" font-weight="700">Rp</text>\n              </svg>\n            </span>\n            <span class="label">Investment</span>\n          </a>'),
    ]),
    ("investment.html", ROOT / "recreate-investment" / "investment.html", [
        ('<a class="toolbar-back" href="#" aria-label="Back">',
         '<a class="toolbar-back" href="dashboard.html" aria-label="Back">'),
    ]),
    ("forex.html", ROOT / "recreate-forex" / "forex.html", [
        ('<a class="toolbar-back" href="#"',
         '<a class="toolbar-back" href="dashboard.html"'),
    ]),
    ("qr-scan.html", ROOT / "recreate-qr" / "qr-scan.html", [
        ('<a href="#" class="close"',
         '<a href="dashboard.html" class="close"'),
    ]),
    ("qr-input.html", ROOT / "recreate-qr" / "qr-input.html", [
        ('<a href="#" class="back"',
         '<a href="qr-scan.html" class="back"'),
    ]),
    ("reward.html", ROOT / "recreate-rewards" / "reward.html", [
        ('<a class="nav-item" href="#" style="text-decoration:none;">\n        <span class="icon">\n          <svg viewBox="0 0 24 24" aria-hidden="true">\n            <path d="M12 3l9 8h-3v9h-5v-6H11v6H6v-9H3z" fill="currentColor"/>\n          </svg>\n        </span>\n        <span>Home</span>',
         '<a class="nav-item" href="dashboard.html" style="text-decoration:none;">\n        <span class="icon">\n          <svg viewBox="0 0 24 24" aria-hidden="true">\n            <path d="M12 3l9 8h-3v9h-5v-6H11v6H6v-9H3z" fill="currentColor"/>\n          </svg>\n        </span>\n        <span>Home</span>'),
        ('<a class="nav-item active" href="#" style="text-decoration:none;">\n        <span class="icon">\n          <svg viewBox="0 0 24 24" aria-hidden="true">\n            <rect x="3" y="9" width="18" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/>\n            <path d="M3 13h18M12 9v13" stroke="currentColor" stroke-width="1.6"/>\n            <path d="M12 9c-2 0-3-1-3-3V4h6v2c0 2-1 3-3 3z" fill="currentColor"/>\n          </svg>\n        </span>\n        <span>Rewards</span>',
         '<a class="nav-item active" href="reward.html" style="text-decoration:none;">\n        <span class="icon">\n          <svg viewBox="0 0 24 24" aria-hidden="true">\n            <rect x="3" y="9" width="18" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/>\n            <path d="M3 13h18M12 9v13" stroke="currentColor" stroke-width="1.6"/>\n            <path d="M12 9c-2 0-3-1-3-3V4h6v2c0 2-1 3-3 3z" fill="currentColor"/>\n          </svg>\n        </span>\n        <span>Rewards</span>'),
        ('<a class="fab" href="#" role="button" aria-label="Scan QR"',
         '<a class="fab" href="qr-scan.html" role="button" aria-label="Scan QR"'),
    ]),
]

VIEWPORT_PATCH = (
    '<meta name="viewport" content="width=360, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
)

RESPONSIVE_CSS = """
  <!-- =========================================================
       HOSTED-PROTOTYPE WRAPPER — added by prototype/wire-links.py
       Desktop: 360px phone centered on a neutral page bg.
       Mobile (≤ 480px): phone fills the screen up to 360px
       and the page scrolls vertically.
       ========================================================= -->
  <style>
    html, body {
      background: #ececec;
      margin: 0;
      padding: 0;
    }
    body {
      width: 360px;
      margin: 0 auto;
      display: block;
    }
    .phone {
      width: 360px;
      height: auto;
      min-height: 800px;
    }
    @media (max-width: 480px) {
      html, body {
        background: #fff;
        margin: 0;
        padding: 0;
      }
      body {
        width: 100vw;
        max-width: 360px;
        margin: 0 auto;
      }
      .phone {
        width: 100%;
        max-width: 360px;
        box-shadow: none;
        border-radius: 0;
      }
    }
  </style>
"""


def main():
    for rel, source, ops in WIRING:
        target = TARGET / rel
        if not source.exists():
            print(f"  SKIP: source {source} not found")
            continue

        # Start fresh from the canonical source.
        src = source.read_text()

        # 1. Viewport patch.
        if VIEWPORT_PATCH[0] in src:
            src = src.replace(VIEWPORT_PATCH[0], VIEWPORT_PATCH[1], 1)

        # 2. Remove any previously-injected responsive block (idempotent re-runs).
        src = re.sub(
            r'\n  <!-- =========================================================\n       HOSTED-PROTOTYPE WRAPPER.*?</style>\n',
            '', src, flags=re.DOTALL)
        src = re.sub(
            r'\n  <!-- =========================================================\n       RESPONSIVE WRAPPER.*?</style>\n',
            '', src, flags=re.DOTALL)

        # 3. Link wiring.
        for match, replacement in ops:
            count = src.count(match)
            if count == 0:
                print(f"  WARN: {rel}: no match for pattern ({len(match)} chars)")
            elif count > 1:
                src = src.replace(match, replacement, 1)
                print(f"  WARN: {rel}: pattern matched {count} times — replaced first only")
            else:
                src = src.replace(match, replacement)

        # 4. Inject responsive CSS before </head>.
        src = src.replace("</head>", RESPONSIVE_CSS + "</head>", 1)

        target.write_text(src)
        print(f"  built {rel}  ({len(src):,} bytes)")

    print("\nDone.")


if __name__ == "__main__":
    main()
