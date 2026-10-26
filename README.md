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
python3 -m http.server 8000   # then open http://localhost:8000
```

## Notes

- The contact form and newsletter are front-end only — connect them to a form service
  (e.g. Formspree, Web3Forms, or a Vercel serverless function) before relying on them.
