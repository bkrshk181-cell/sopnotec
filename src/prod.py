# Production build: static multi-page site with shared CSS/JS and real image files.
# Usage (from the repo root):  python3 src/prod.py
#   reads  src/*.py, src/style.css, src/main.js, assets/img/*.webp
#   writes ./*.html, assets/css/style.css, assets/js/main.js
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
<meta property="og:image" content="assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script></head>
<body>'''
PAGE_FN = """def page(fname, title, desc, body):
    doc = PROD_HEAD.format(title=e(title), desc=e(desc)) + header() + '\\n<main>' + body + '</main>\\n' + footer() + '\\n</body></html>\\n'
    doc = re.sub(r'<img (?![^>]*alt="SopnoTec")', '<img loading="lazy" decoding="async" ', doc)
    open(os.path.join(OUT, fname), 'w').write(doc)"""
src = re.sub(r"def page\(fname, title, desc, body\):.*?open\(os\.path\.join\(OUT, fname\), \"w\"\)\.write\(doc\)", lambda m: PAGE_FN, src, flags=re.S)
src = re.sub(r"def img\(k\):.*?return _c\[k\]", lambda m: "def img(k):\n    assert os.path.exists(f'{IMG}/{k}.webp'), k\n    return f'assets/img/{k}.webp'", src, flags=re.S)
src = src.replace('print("built", sorted(os.listdir(OUT)))', "")
ns = {"__file__": os.path.join(HERE, "build.py"), "__name__": "prod", "PROD_HEAD": HEAD, "re": re}
sys.argv = [sys.argv[0], ROOT, IMGDIR]
exec(compile(src, "build.py", "exec"), ns)

os.makedirs(os.path.join(ROOT, "assets", "css"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "assets", "js"), exist_ok=True)
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(ROOT, "assets", "css", "style.css"))
shutil.copy(os.path.join(HERE, "main.js"), os.path.join(ROOT, "assets", "js", "main.js"))
print("production build written to", ROOT)
