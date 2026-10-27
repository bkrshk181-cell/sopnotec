# SopnoTec — website

Static, multi-page website for **SopnoTec** (IT solutions & service agency). Plain HTML/CSS/JS — no framework, no build step needed to deploy.

## Structure

```
index.html, about.html, services.html, projects.html, team.html, contact.html,
privacy-policy.html, 404.html
service-*.html        10 service detail pages
project-*.html        3 case-study pages
assets/css/style.css  all styles
assets/js/main.js     animations, sliders, tabs, forms
assets/img/           images (webp), favicon, social share image
src/                  page generator (content lives in src/data.py)
docs/CONTENT.md       all site copy in one readable file
vercel.json           Vercel config (caching + security headers)
```

## Deploy on Vercel

1. Import this repo in Vercel → **Framework Preset: Other**.
2. Leave **Build Command** and **Output Directory** empty (root is served as-is).
3. Deploy. Every push to `main` redeploys automatically.

## Editing content

All text, services, projects, team and testimonials live in `src/data.py`.
After editing, regenerate the HTML pages (Python 3.8+, no packages required):

```bash
python3 src/prod.py
```

Then commit and push. Styles: `src/style.css`; scripts: `src/main.js` (copied into `assets/` by the build).

Optional single-file preview of the whole site:

```bash
python3 src/spa.py preview.html assets/img
```

## Preview locally

```bash
npx vercel dev               # clean URLs + /api/lead, like production
python3 -m http.server 8000   # quick look only: open http://localhost:8000/index.html
```

## URLs, sitemap & robots

- Clean URLs: pages are served as `/about`, `/services`, `/service-crm-setup-and-customization`, etc.
  (`cleanUrls` in `vercel.json`). Old `*.html` links 308-redirect to the clean version.
- Internal links and assets use root-relative paths (`/about`, `/assets/...`); each page has a
  canonical URL based on `SITE['url']` in `src/data.py`.
- `python3 src/prod.py` regenerates `sitemap.xml` and `robots.txt` along with the pages — don't edit them by hand.

## Notes

- **Lead emails:** the contact form and newsletter post to `/api/lead` (Vercel serverless
  function in `api/lead.js`), which emails every submission to the SopnoTec inbox through
  Hostinger SMTP (`smtp.hostinger.com:465`, SSL). Reply-To is set to the visitor, so hitting
  Reply answers them directly. A hidden honeypot field and a minimum fill time filter bots.
- Set these in **Vercel → Project → Settings → Environment Variables** (see `.env.example`),
  then redeploy: `SMTP_USER`, `SMTP_PASS`, and optionally `LEAD_TO`, `SMTP_HOST`, `SMTP_PORT`.
  Never commit the password.
- `python3 -m http.server` previews the pages but not `/api/lead`; use `vercel dev` to test the form locally.
