# Melta Labs website (meltalabs.com)

Static company website for **Melta for Information Technology LLC** (Melta Labs).
Built as plain HTML/CSS — no build step — and hosted on GitHub Pages with the
custom domain `meltalabs.com`.

## Files
- `index.html` — homepage (hero, services, about, contact)
- `privacy.html` — privacy policy
- `CNAME` — custom domain config for GitHub Pages (`meltalabs.com`)

## Company details (already filled in)
The site currently uses these values — keep them **identical** to your
Dun & Bradstreet (D-U-N-S) application; NAP consistency is what gets a
business record verified:

- **Legal name:** Melta for Information Technology LLC (Melta Labs)
- **Email:** accounts@meltalabs.com
- **Phone:** +20 101 532 4571
- **Address:** 1 Ahmed Bahgat St., Othman Towers, Tower 7, OC1, Middle Floor, Cairo, Egypt

They appear in `index.html` (contact section, footer, and JSON-LD block) and in
`privacy.html`. If any of these change, update all of those places together.

## Deploy to GitHub Pages
1. Create a new GitHub repo (public), e.g. `meltalabs-website`.
2. Push these files to the `main` branch.
3. Repo → **Settings → Pages** → Source: `Deploy from a branch` → Branch: `main` / `/ (root)`.
4. Under **Custom domain**, enter `meltalabs.com` and Save (the `CNAME` file already sets this).
5. Enable **Enforce HTTPS** once the certificate is issued.

## DNS (at your domain registrar)
Point `meltalabs.com` at GitHub Pages with these **A records** (apex domain):
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```
And add a `CNAME` record for `www` → `<your-github-username>.github.io`.

DNS changes can take a few minutes to ~24h to propagate.
