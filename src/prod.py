# Production build: static multi-page site with shared CSS/JS and real image files.
# Usage (from the repo root):  python3 src/prod.py
#   reads  src/*.py, src/style.css, src/main.js, assets/img/*.webp
#   writes ./*.html, sitemap.xml, robots.txt, assets/css/style.css, assets/js/main.js
import os, re, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
IMGDIR = os.path.join(ROOT, "assets", "img")
src = open(os.path.join(HERE, "build.py")).read()

HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#07061a">
<meta property="og:type" content="website"><meta property="og:site_name" content="SopnoTec">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{site}/assets/img/og-image.jpg">
<link rel="canonical" href="{canon}">{robots}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css">
<script src="/assets/js/main.js" defer></script></head>
<body>'''
PAGE_FN = """def page(fname, title, desc, body):
    path = '/' if fname == 'index.html' else '/' + fname[:-5]
    PAGES.append((fname, path))
    doc = PROD_HEAD.format(title=e(title), desc=e(desc), site=SITE['url'], canon=SITE['url'] + path,
                           robots='\\n<meta name="robots" content="noindex">' if fname == '404.html' else '') + header() + '\\n<main>' + body + '</main>\\n' + footer() + '\\n</body></html>\\n'
    doc = re.sub(r'<img (?![^>]*alt="SopnoTec")', '<img loading="lazy" decoding="async" ', doc)
    open(os.path.join(OUT, fname), 'w').write(doc)"""
src = re.sub(r"def page\(fname, title, desc, body\):.*?open\(os\.path\.join\(OUT, fname\), \"w\"\)\.write\(doc\)", lambda m: PAGE_FN, src, flags=re.S)
src = re.sub(r"def img\(k\):.*?return _c\[k\]", lambda m: "def img(k):\n    assert os.path.exists(f'{IMG}/{k}.webp'), k\n    return f'/assets/img/{k}.webp'", src, flags=re.S)
src = src.replace('print("built", sorted(os.listdir(OUT)))', "")
PAGES = []
ns = {"__file__": os.path.join(HERE, "build.py"), "__name__": "prod", "PROD_HEAD": HEAD, "re": re, "PAGES": PAGES}
sys.argv = [sys.argv[0], ROOT, IMGDIR]
exec(compile(src, "build.py", "exec"), ns)

os.makedirs(os.path.join(ROOT, "assets", "css"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "assets", "js"), exist_ok=True)
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(ROOT, "assets", "css", "style.css"))
shutil.copy(os.path.join(HERE, "main.js"), os.path.join(ROOT, "assets", "js", "main.js"))
# sitemap.xml + robots.txt (404 excluded)
import datetime
SITE_URL = ns["SITE"]["url"]
today = datetime.date.today().isoformat()
def prio(path):
    if path == "/": return "1.0"
    if path in ("/services", "/contact"): return "0.9"
    if path.startswith(("/service-", "/project-")) or path in ("/about", "/projects", "/team"): return "0.8"
    return "0.3"
urls = "".join(f"  <url><loc>{SITE_URL}{path}</loc><lastmod>{today}</lastmod><priority>{prio(path)}</priority></url>\n"
               for fname, path in PAGES if fname != "404.html")
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("production build written to", ROOT, "-", len(PAGES), "pages, sitemap.xml, robots.txt")
