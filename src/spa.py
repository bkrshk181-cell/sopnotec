# Builds a single-file version of the whole site (all pages as hash-routed views).
# Usage: python3 spa.py <out.html> <image_dir>
import os, re, sys, base64, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUTFILE, IMGDIR = sys.argv[1], sys.argv[2]
src = open(os.path.join(HERE, "build.py")).read()

# 1) images become tokens; resolved once at the end
src = re.sub(r"def img\(k\):.*?return _c\[k\]", "def img(k):\n    USED.add(k); return f'__IMG_{k}__'", src, flags=re.S)
# 2) pages are collected instead of written
src = re.sub(r"def page\(fname, title, desc, body\):.*?open\(os\.path\.join\(OUT, fname\), \"w\"\)\.write\(doc\)",
             "def page(fname, title, desc, body):\n    PAGES.append((fname[:-5], title, body))", src, flags=re.S)
src = src.replace('print("built", sorted(os.listdir(OUT)))', "")
ns = {"__file__": os.path.join(HERE, "build.py"), "__name__": "spa", "USED": set(), "PAGES": []}
sys.argv = [sys.argv[0], "/tmp/_spa_unused", IMGDIR]
exec(compile(src, "build.py", "exec"), ns)
PAGES, USED = ns["PAGES"], ns["USED"]
SERVICES, PROJECTS = ns["SERVICES"], ns["PROJECTS"]

def fix(h):
    h = re.sub(r'href="/([a-z0-9\-]*)([?#][^"]*)?"', lambda m: f'href="#/{m.group(1) or "index"}{m.group(2) or ""}"', h)
    h = re.sub(r'src="__IMG_([a-z0-9_]+)__"', r'src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" data-img="\1"', h)
    h = re.sub(r"url\('__IMG_([a-z0-9_]+)__'\)", r"var(--i-\1)", h)
    return h

head_html = fix(ns["header"]())
foot_html = fix(ns["footer"]())
imgs = {k: "data:image/webp;base64," + base64.b64encode(open(f"{IMGDIR}/{k}.webp", "rb").read()).decode() for k in sorted(USED)}
img_js = "window.IMG=" + json.dumps(imgs) + ";(function(){var r=document.documentElement.style;for(var k in IMG)r.setProperty('--i-'+k,'url(\"'+IMG[k]+'\")')})();"

views = "".join(f'<div class="view" data-route="{r}" data-title="{ns["e"](t)}">{fix(b)}</div>' for r, t, b in PAGES)

# page index overlay
def link(r, label): return f'<a href="#/{r}">{label}</a>'
groups = [
 ("Main pages", [("index","Home"),("about","About"),("services","Services"),("projects","Projects"),("team","Team"),("contact","Contact"),("privacy-policy","Privacy Policy"),("404","404 page")]),
 ("Service pages", [(f"service-{s['slug']}", s["name"]) for s in SERVICES]),
 ("Case studies", [(f"project-{p['slug']}", p["name"]) for p in PROJECTS]),
]
idx = "".join(f'<div><h5>{g}</h5>{"".join(link(r,l) for r,l in items)}</div>' for g, items in groups)

EXTRA_CSS = """
.view{display:none}.view.on{display:block}
#pgbtn{position:fixed;left:24px;bottom:24px;z-index:70;display:flex;gap:10px;align-items:center;padding:12px 18px;border-radius:999px;border:1px solid var(--line);background:rgba(13,11,41,.9);backdrop-filter:blur(12px);color:#fff;font:600 14px/1 inherit;font-family:inherit;cursor:pointer;box-shadow:0 20px 40px -15px #000;transition:.3s}
#pgbtn:hover{border-color:var(--c2);transform:translateY(-3px)}
#pgbtn b{background:var(--grad);border-radius:999px;padding:4px 9px;font-size:12px}
#pgidx{position:fixed;inset:0;z-index:200;background:rgba(5,4,15,.82);backdrop-filter:blur(14px);display:grid;place-items:center;padding:24px;opacity:0;visibility:hidden;transition:.35s}
#pgidx.show{opacity:1;visibility:visible}
#pgidx .box{width:min(1000px,100%);max-height:90vh;overflow:auto;background:var(--bg2);border:1px solid var(--line);border-radius:28px;padding:36px;transform:translateY(30px) scale(.97);transition:.45s var(--ease)}
#pgidx.show .box{transform:none}
#pgidx .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:26px;gap:20px}
#pgidx .top h3{font-size:26px}
#pgidx .top button{background:none;border:1px solid var(--line);color:#fff;width:42px;height:42px;border-radius:50%;cursor:pointer;font-size:18px}
#pgidx .cols{display:grid;grid-template-columns:1fr 1.3fr 1fr;gap:30px}
#pgidx h5{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--c1);margin-bottom:12px}
#pgidx a{display:block;padding:9px 12px;border-radius:10px;color:#c3c6e6;font-size:15px;transition:.25s}
#pgidx a:hover{background:rgba(91,110,225,.14);color:#fff;transform:translateX(4px)}
#pgidx a.cur{background:rgba(91,110,225,.22);color:#fff}
@media (max-width:760px){#pgidx .cols{grid-template-columns:1fr}#pgbtn span{display:none}}
"""

ROUTER = """
(function(){
const $=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>[...c.querySelectorAll(s)];
$$('img[data-img]').forEach(i=>{i.src=IMG[i.dataset.img]});
const views=$$('.view'),map={};views.forEach(v=>map[v.dataset.route]=v);
const idx=$('#pgidx');
let CUR=(location.hash||'#/index');
function parse(){let h=CUR.replace(/^#\\/?/,'');let anchor='';const ai=h.indexOf('#');if(ai>=0){anchor=h.slice(ai+1);h=h.slice(0,ai)}
  let q='';const qi=h.indexOf('?');if(qi>=0){q=h.slice(qi+1);h=h.slice(0,qi)}return{r:h||'index',q:new URLSearchParams(q),anchor}}
function show(first){const {r,q,anchor}=parse();const v=map[r]||map['404'];
  views.forEach(x=>x.classList.toggle('on',x===v));document.title=v.dataset.title;
  $$('.menu>li>a').forEach(a=>{const t=(a.getAttribute('href')||'').slice(2);a.classList.toggle('on',t===v.dataset.route||(a.dataset.match&&v.dataset.route.startsWith(a.dataset.match)))});
  $$('#pgidx a').forEach(a=>a.classList.toggle('cur',a.getAttribute('href').slice(2)===v.dataset.route));
  const s=q.get('service');if(s&&$('#svcsel',v))$('#svcsel',v).value=s;
  $('nav.main').classList.remove('open');
  const el=anchor&&document.getElementById(anchor);
  if(el)setTimeout(()=>el.scrollIntoView({behavior:first?'auto':'smooth'}),first?0:60);else scrollTo(0,0);
  dispatchEvent(new Event('resize'));dispatchEvent(new Event('scroll'))}
function replayCurtain(){const c=$('#curtain');const n=c.cloneNode(true);n.classList.remove('leave');c.replaceWith(n)}
document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#/"]');if(!a||e.metaKey||e.ctrlKey)return;e.preventDefault();
  idx.classList.remove('show');const target=a.getAttribute('href');
  if(target===CUR){scrollTo({top:0,behavior:'smooth'});return}
  const c=$('#curtain');c.classList.add('leave');setTimeout(()=>go(target,true),520)});
function go(t,push){CUR=t;if(push){try{history.pushState(null,'',t)}catch(_){}}show(false);replayCurtain()}
addEventListener('popstate',()=>{const h=location.hash||'#/index';if(h!==CUR)go(h,false)});
addEventListener('hashchange',()=>{const h=location.hash||'#/index';if(h!==CUR)go(h,false)});
$('#pgbtn').onclick=()=>idx.classList.add('show');
$('#pgidx .top button').onclick=()=>idx.classList.remove('show');
idx.addEventListener('click',e=>{if(e.target===idx)idx.classList.remove('show')});
addEventListener('keydown',e=>{if(e.key==='Escape')idx.classList.remove('show')});
show(true);
})();
"""

doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SopnoTec — IT Solutions &amp; Service Agency</title>
<meta name="description" content="SopnoTec website redesign — every page in a single file.">
<script>{img_js}</script><style>{ns['CSS']}{EXTRA_CSS}</style></head>
<body>{head_html}
<main>{views}</main>
{foot_html}
<button id="pgbtn" aria-label="All pages">☰ <span>All pages</span> <b>{len(PAGES)}</b></button>
<div id="pgidx"><div class="box"><div class="top"><h3>All <span class="grad">pages</span></h3><button aria-label="Close">✕</button></div><div class="cols">{idx}</div></div></div>
<script>{ROUTER}</script>
<script>{ns['JS']}</script></body></html>"""
open(OUTFILE, "w").write(doc)
print("pages", len(PAGES), "images", len(imgs), "bytes", len(doc))
