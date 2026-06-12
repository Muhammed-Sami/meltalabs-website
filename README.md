# Melta Labs website (meltalabs.com)

Bilingual (English + Arabic / RTL) company website for **Melta for Information
Technology LLC** (Melta Labs). Static HTML/CSS/vanilla JS — no build step —
hosted on GitHub Pages with the custom domain `meltalabs.com`. The visual system
is a light, enterprise "Trust-First" design intended to read as a legitimate,
established IT company in support of a Dun & Bradstreet (D-U-N-S) registration.

## Structure
```
index.html            EN home            → https://meltalabs.com/
ar/index.html         AR home (RTL)      → https://meltalabs.com/ar/
privacy.html          EN privacy         → https://meltalabs.com/privacy.html
ar/privacy.html       AR privacy (RTL)   → https://meltalabs.com/ar/privacy.html
assets/styles.css     One shared stylesheet (CSS logical properties → serves LTR + RTL)
robots.txt            Allow all, points to sitemap
sitemap.xml           All 4 URLs with hreflang alternates
site.webmanifest      PWA manifest (light theme)
.nojekyll             Disables Jekyll so /assets serves verbatim
CNAME                 meltalabs.com
favicon.svg / favicon.ico / apple-touch-icon.png   Root favicons
assets/*.png          Generated icons + 1200×630 OG card (see below)
assets/gen_assets.py  Regenerates all binary brand assets with Pillow
```

## Bilingual / SEO design
- Separate crawlable URLs per language (`/` and `/ar/`) with reciprocal,
  self-referential **hreflang** (`en` / `ar` / `x-default`) on every page.
- `<html lang dir>` set per page (`en/ltr`, `ar/rtl`); one stylesheet handles
  both directions via CSS logical properties.
- Per-page canonical, unique title + meta description, Open Graph + Twitter card,
  and JSON-LD `@graph` (Organization + WebSite) with a shared `@id` across both
  languages. Arabic copy is human-quality translation; all Latin/numeric runs in
  Arabic text are isolated with `<bdi>`.

## ⚠️ Company facts are LOCKED — keep them byte-identical
The name / address / phone (NAP) below appear across all pages, both JSON-LD
blocks, the footer, the sitemap and the manifest. They **must** stay identical to
each other and to your D-U-N-S application — a single mismatch is the most common
reason a business record fails to verify.

- **Legal name:** Melta for Information Technology LLC (Latin on both languages)
- **Brand:** Melta Labs / ميلتا لابز
- **Email:** accounts@meltalabs.com
- **Phone:** +20 101 532 4571  (`tel:+201015324571`, E.164)
- **Address:** 1 Ahmed Bahgat St., Othman Towers, Tower 7, OC1, Fifth Floor, Maadi, Cairo, Egypt
- **Founded:** 2025
- **Commercial Register №:** 275628  ·  **Tax Registration №:** 769546358  ·  ISIC 6209 (IT services)
- **D-U-N-S №:** 849225135

All of the above are taken from the official Egyptian Commercial Register extract
and Tax Authority taxpayer card — keep them byte-identical to those documents.

## Regenerating brand assets
Icons and the OG card are generated, not hand-edited:
```bash
python3 assets/gen_assets.py     # requires Pillow (pip install pillow)
```

## Local preview
Use a local server so the root-absolute paths (`/assets/...`, `/ar/`) resolve:
```bash
python3 -m http.server 8765      # then open http://localhost:8765/
```

## Deploy (GitHub Pages)
Already linked to the repo's GitHub Pages site with the `meltalabs.com` custom
domain. Pushing to `main` rebuilds automatically. DNS at the registrar:
- Apex `meltalabs.com` → A records `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`
- `www` → CNAME `muhammed-sami.github.io`
- Enable **Enforce HTTPS** in Settings → Pages once the certificate is issued.
