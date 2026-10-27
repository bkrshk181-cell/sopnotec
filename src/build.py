import base64, os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
IMG = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
CSS = open(os.path.join(HERE, "style.css")).read()
JS = open(os.path.join(HERE, "main.js")).read()
_c = {}
def img(k):
    if k not in _c:
        _c[k] = "data:image/webp;base64," + base64.b64encode(open(f"{IMG}/{k}.webp", "rb").read()).decode()
    return _c[k]
def ic(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24">{ICONS[name]}</svg>'
e = H.escape
ARROW = ic("arrow")
S = {s["slug"]: s for s in SERVICES}
P = {p["slug"]: p for p in PROJECTS}
def nav_name(s): return s.get("nav", s["name"])
def surl(s): return f"/service-{s['slug']}"
def purl(p): return f"/project-{p['slug']}"

# ---------- shared chrome ----------
def header():
    mega = "".join(f'<a href="{surl(s)}"><span class="mi">{ic(s["icon"])}</span><span>{e(nav_name(s))}<small>{e(s["short"][:58])}…</small></span></a>' for s in SERVICES)
    return f'''
<div id="curtain"><img src="{img('logo')}" alt=""></div>
<div id="progress"></div><div id="glow"></div>
<div class="topbar"><div class="wrap">
  <div class="l"><a href="mailto:{SITE['email']}">{ic('mail')} {SITE['email']}</a><a href="tel:{SITE['phone2'][1]}">{ic('phone')} {SITE['phone2'][0]}</a></div>
  <div class="r"><span style="display:inline-flex;gap:8px;align-items:center">{ic('pin')} {SITE['address']}</span><a href="/contact">Help</a><a href="/contact">Support</a><a href="/contact#faq">FAQs</a></div>
</div></div>
<nav class="main"><div class="wrap">
  <a href="/" class="logo"><img src="{img('logo')}" alt="SopnoTec"></a>
  <ul class="menu">
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/services" data-match="service">Services <span class="caret">▼</span></a><div class="mega"><div class="mega-in">{mega}<a class="all" href="/services">View all services {ARROW}</a></div></div></li>
    <li><a href="/projects" data-match="project">Projects</a></li>
    <li><a href="/team">Team</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
  <a href="/contact" class="btn btn-primary cta">Get Started Free {ARROW}</a>
  <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>
</div></nav>'''

def footer():
    fs = "".join(f'<li><a href="{surl(s)}">{e(nav_name(s))}</a></li>' for s in SERVICES[:6])
    return f'''
<div class="fcta"><div class="wrap"><div class="in rv s">
  <div><small>Call to action</small><h3>Ready to collaborate with us?</h3></div>
  <a class="ph" href="tel:{SITE['phone1'][1]}"><span class="ic">{ic('phone')}</span><span><small>Phone</small><b>{SITE['phone1'][0]}</b></span></a>
  <a href="/contact" class="btn">Contact us {ARROW}</a>
</div></div></div>
<footer><div class="wrap">
  <div class="fgrid">
    <div><a href="/" class="logo"><img src="{img('logo')}" alt="SopnoTec"></a>
      <p>Tailored IT solutions, digital innovation and expert support — we help businesses grow across every digital channel.</p>
      <form class="news" action="/api/lead" method="post"><input type="hidden" name="form" value="newsletter"><input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="email" name="email" placeholder="Your email" aria-label="Your email" maxlength="200" required><button>Subscribe</button></form></div>
    <div><h5>Links</h5><ul><li><a href="/">Home</a></li><li><a href="/about">About us</a></li><li><a href="/projects">Our projects</a></li><li><a href="/team">Meet our team</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy-policy">Privacy policy</a></li></ul></div>
    <div><h5>Services</h5><ul>{fs}<li><a href="/services" style="color:var(--c1)">All services →</a></li></ul></div>
    <div><h5>Contact</h5><ul><li><a href="tel:{SITE['phone1'][1]}">{SITE['phone1'][0]} ({SITE['phone1'][2]})</a></li><li><a href="tel:{SITE['phone2'][1]}">{SITE['phone2'][0]} ({SITE['phone2'][2]})</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li><li>{SITE['address']}</li></ul></div>
  </div>
  <div class="huge">SopnoTec</div>
  <div class="copy"><span>© <span id="yr"></span> SopnoTec. All rights reserved.</span><span><a href="/privacy-policy">Privacy Policy</a> · <a href="/privacy-policy">Terms of Condition</a></span></div>
</div></footer>
<button id="totop" aria-label="Back to top"><svg class="ringp" viewBox="0 0 54 54"><circle cx="27" cy="27" r="24" stroke="rgba(255,255,255,.1)"/><circle cx="27" cy="27" r="24" stroke="url(#tg)"/><defs><linearGradient id="tg"><stop offset="0" stop-color="#22c7e0"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs></svg>{ic('arrow')}</button>'''

def page(fname, title, desc, body):
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<style>{CSS}</style></head>
<body>{header()}
<main>{body}</main>
{footer()}
<script>{JS}</script></body></html>'''
    open(os.path.join(OUT, fname), "w").write(doc)

def phero(title_html, sub, crumbs, bg, icon=None):
    cr = '<a href="/">Home</a>' + "".join(f'<span class="sep">/</span>' + (f'<a href="{u}">{e(t)}</a>' if u else f'<span>{e(t)}</span>') for t, u in crumbs)
    big = f'<div class="ico-big">{ic(icon)}</div>' if icon else ""
    return f'''<header class="phero"><div class="bgimg" style="background-image:url('{img(bg)}')"></div><canvas class="net"></canvas>{big}
<div class="wrap"><div class="crumbs rv">{cr}</div><h1 class="rv">{title_html}</h1>{f'<p class="rv">{e(sub)}</p>' if sub else ''}</div></header>'''

# ---------- reusable blocks ----------
def stats_block():
    return '''<section class="tight"><div class="wrap"><div class="stats-box rv s">
<div class="stat"><b class="grad" data-count="5">0</b><span>Glorious years</span></div>
<div class="stat"><b class="grad" data-count="120">0</b><span>Active clients</span></div>
<div class="stat"><b class="grad" data-count="150">0</b><span>Projects completed</span></div>
<div class="stat"><b class="grad" data-count="10">0</b><span>Professional team</span></div>
</div></div></section>'''

def testimonial_block():
    cards = ""
    for i, t in enumerate(TESTIMONIALS):
        roles = " · ".join(e(r) for r in t["roles"][:3])
        cards += f'''<article class="tcard" data-i="{i}"><div class="tq">“</div>
<div class="tbody"><div class="stars">★★★★★</div><blockquote>{e(t['long'])}</blockquote>
<div class="tfoot"><img src="{img(t['img'])}" alt="{e(t['name'])}"><div><b>{e(t['name'])}</b><small>{roles}</small></div>
<div class="tstat"><b class="grad">{e(t['stat'][0])}</b><span>{e(t['stat'][1])}</span></div></div></div></article>'''
    nav = "".join(f'<button data-i="{i}" aria-label="{e(t["name"])}"><img src="{img(t["img"])}" alt=""><i></i></button>' for i, t in enumerate(TESTIMONIALS))
    tiles = ""
    for t in TESTIMONIALS:
        chips = "".join(f"<span>{e(r)}</span>" for r in t["roles"])
        tiles += f'''<div class="ttile" data-tilt><div class="tt-top"><img src="{img(t['img'])}" alt="{e(t['name'])}"><div><b>{e(t['name'])}</b><div class="stars sm">★★★★★</div></div></div>
<p>“{e(t['short'])}”</p><div class="chips">{chips}</div><p class="tbio">{e(t['bio'])}</p></div>'''
    return f'''<section class="testis"><div class="wrap">
<div class="center"><div class="eyebrow rv">Client Testimonials</div><h2 class="rv">What founders &amp; CEOs <span class="grad">say about us.</span></h2>
<p class="sub rv">Visionary CEOs trust us to streamline their workflows — here's what they say about working with our founder, Abu Bakar.</p></div>
<div class="tdeck rv s"><button class="tarrow prev" aria-label="Previous">{ic('arrow')}</button><div class="tstack">{cards}</div><button class="tarrow next" aria-label="Next">{ic('arrow')}</button></div>
<div class="tnav rv">{nav}</div>
<div class="center" style="margin:90px 0 40px"><div class="eyebrow rv">Client Reviews</div><h3 class="rv" style="font-size:clamp(26px,3vw,38px)">Reviews about <span class="grad">our work.</span></h3></div>
<div class="ttiles">{tiles}</div>
</div></section>'''

def cta_block(title="Looking for the best <span class='grad'>IT business solutions?</span>", sub="We're here to help grow your business. We have worked with clients across the globe — let's make yours the next success story."):
    return f'''<section style="padding-top:40px"><div class="wrap"><div class="cta-box rv s">
<div class="eyebrow" style="justify-content:center">Let's get started</div><h2>{title}</h2><p class="sub">{e(sub)}</p>
<div class="row"><a href="/contact" class="btn btn-primary">Get free consultation {ARROW}</a><a href="/services" class="btn btn-ghost">Our services</a></div>
</div></div></section>'''

def why_block():
    rs = "".join(f'<div class="reason rv"><div><h4>{e(a)}</h4><p>{e(b)}</p></div></div>' for a, b in REASONS)
    return f'''<section><div class="wrap why-grid">
<div class="sticky rv l"><div class="eyebrow">6 Reasons</div><h2>Why businesses <span class="grad">choose us.</span></h2>
<p class="sub">A trusted IT solution &amp; service business agency. IT solutions created by top experts, free consultation for any kind of IT solution, and 24/7 support for partners throughout the process.</p>
<div class="mini"><div>{ic('award')}<b>Experienced</b><small>5+ years of experience</small></div><div>{ic('clock')}<b>Active</b><small>Support any time 24/7</small></div><div>{ic('shield')}<b>Professional</b><small>We take our job seriously</small></div></div>
<a href="/contact" class="btn btn-primary" style="margin-top:30px">Contact us {ARROW}</a></div>
<div class="reasons">{rs}</div></div></section>'''

def pillars_block():
    items = [("bulb","bulb","Innovative Solutions","Harness the power of advanced technology tailored to your business needs."),
             ("tima","headset","Excellent Support","Access dedicated assistance and guidance from our skilled professionals."),
             ("ns3","rocket","Strategic Growth","Drive your business forward with data-driven insights and optimized processes.")]
    cards = "".join(f'<div class="pillar"><div class="im"><img src="{img(a)}" alt=""></div><div class="tx"><span class="ic">{ic(b)}</span><h3>{c}</h3><p>{d}</p></div></div>' for a, b, c, d in items)
    return f'<section class="tight"><div class="wrap"><div class="pillars stagger">{cards}</div></div></section>'

def team_cards(full=False):
    out = ""
    for i, m in enumerate(TEAM):
        extra = f'<p class="motto">“{e(m["motto"])}”</p><p class="bio">{e(m["bio"])}</p>' if full else f'<p class="bio">{e(m["bio"][:110])}{"…" if len(m["bio"])>110 else ""}</p>'
        out += f'''<div class="member rv" style="transition-delay:{i*.12}s"><div class="ph"><img src="{img(m['img'])}" alt="{e(m['name'])}"><div class="soc"><span>{ic('share')}</span><span>{ic('mail')}</span><span>{ic('globe')}</span></div></div>
<div class="info"><h3>{e(m['name'])}</h3><span class="role">{e(m['role'])}</span>{extra}</div></div>'''
    return f'<div class="team-grid">{out}</div>'

def proj_cards():
    out = ""
    for i, p in enumerate(PROJECTS):
        tools = "".join(f"<span>{e(t)}</span>" for t in p["tools"][:4])
        out += f'''<a href="{purl(p)}" class="proj rv" data-tilt style="transition-delay:{i*.12}s"><div class="bg" style="background:{p['grad']}"><img src="{img(p['img'])}" alt=""></div>
<span class="tag">{e(p['cat'])}</span><div class="big grad">{p['big']}</div><div class="bigl">{e(p['bigl'])}</div>
<h3>{e(p['name'])}</h3><p>{e(p['summary'])}</p><div class="tools">{tools}</div><span class="more">View case study {ARROW}</span></a>'''
    return f'<div class="proj-grid">{out}</div>'

def svc_img_cards(items):
    out = ""
    for i, s in enumerate(items):
        out += f'''<a href="{surl(s)}" class="svc-img rv" style="transition-delay:{(i%3)*.1}s"><img src="{img(s['card'])}" alt=""><span class="ic">{ic(s['icon'])}</span><span class="num">{SERVICES.index(s)+1:02d}</span>
<h3>{e(s['name'])}</h3><p>{e(s['short'])}</p><span class="more">Explore service {ARROW}</span></a>'''
    return out

def marquee(cls=""):
    items = "".join(f'<a href="{surl(s)}">{e(nav_name(s))}</a>' for s in SERVICES)
    return f'<div class="marquee {cls}"><div class="track">{items}</div></div>'

ORB = f'''<div class="orb rv s"><div class="ring"><i></i></div><div class="ring r2"><i></i></div><div class="ring r3"><i></i></div>
<div class="core"><svg viewBox="0 0 100 100" fill="none"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22c7e0"/><stop offset=".5" stop-color="#5b6ee1"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs><path d="M50 6 88 28v44L50 94 12 72V28z" stroke="url(#lg)" stroke-width="7" stroke-linejoin="round"/><path d="M66 36H40a8 8 0 0 0 0 16h20a8 8 0 0 1 0 16H34" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg></div>
<div class="chip c1"><div class="ic">★</div><div><b data-count="120">0</b><small>Satisfied clients</small></div></div>
<div class="chip c2"><div class="ic">⚡</div><div><b>24/7</b><small>Active support</small></div></div>
<div class="chip c3"><div class="ic">◆</div><div><b data-count="150">0</b><small>Projects completed</small></div></div></div>'''

def about_split(checks, cta=("/services","What we offer")):
    ch = "".join(f"<li>{ic('check')}{e(c)}</li>" for c in checks)
    return f'''<div class="split2">
<div class="collage rv l"><div class="ph p1" data-parallax="-0.05"><img src="{img('about1')}" alt=""></div><div class="ph p2"><img src="{img('about2')}" alt=""></div>
<div class="badge"><div class="spin"><img src="{img('untitled')}" alt=""></div><div class="yrs"><b data-count="5">0</b></div></div></div>
<div class="rv r"><div class="eyebrow">About SopnoTec</div><h2>Where vision meets reality in every <span class="grad">click &amp; keystroke.</span></h2>
<p class="sub">At SopnoTec, we leverage cutting-edge technology and tailored solutions, offering comprehensive IT services, digital innovation, and expert support for unparalleled business growth and success.</p>
<ul class="checks">{ch}</ul><a href="{cta[0]}" class="btn btn-primary">{cta[1]} {ARROW}</a></div></div>'''

# ================= PAGES =================
# HOME
slides = ""
for h, p in HERO_SLIDES:
    slides += f'''<div class="slide"><h1>{e(h)}</h1><p>{e(p)}</p><div class="ctas"><a href="/contact" class="btn btn-primary">Get free consultation {ARROW}</a><a href="/services" class="btn btn-ghost">Explore services</a></div></div>'''
dots = "".join("<button aria-label='slide'><i></i></button>" for _ in HERO_SLIDES)
svc_cards = "".join(f'''<a href="{surl(s)}" class="svc rv" data-tilt style="transition-delay:{(i%3)*.1}s"><span class="num">{i+1:02d}</span><div class="ic">{ic(s['icon'])}</div><h3>{e(s['name'])}</h3><p>{e(s['short'])}</p><span class="more">Learn more {ARROW}</span></a>''' for i, s in enumerate([S[x] for x in HOME_SERVICES]))
home = f'''
<header class="hero"><canvas class="net"></canvas><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
<div class="wrap"><div><div class="pill"><span class="dot"></span> IT Solutions &amp; Service Agency · 24/7 Support</div>
<div class="slides">{slides}</div><div class="dots">{dots}</div></div>{ORB}</div><div class="scrollhint"></div></header>
{marquee()}
<section><div class="wrap">{about_split(["Website development","Internal networking","Free IT consultation","24/7 partner support"], ("/about","More about us"))}</div></section>
{pillars_block()}
<section><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">What We're Offering</div><h2>Services built to<br><span class="grad">scale with you.</span></h2></div>
<div class="rv"><p class="sub">SopnoTec offers tailored IT solutions and comprehensive digital development services, addressing diverse business needs and delivering customized, scalable technology.</p><a href="/services" class="btn btn-ghost" style="margin-top:20px">All 10 services {ARROW}</a></div></div>
<div class="svc-grid">{svc_cards}</div></div></section>
<section class="tight"><div class="wrap"><div class="banner rv s"><div class="bgimg" data-parallax="0.08" style="background-image:url('{img('p5833775')}')"></div>
<div class="eyebrow">Do you need a meeting?</div><h2>We're ready to <span class="grad">develop your business!</span></h2>
<ul class="bullets">{''.join(f"<li>{ic('check')}{t}</li>" for t in ["IT solutions are created by top experts","Receive free consultation for any kind of IT solutions","Support 24/7 for partners during the process"])}</ul>
<a href="/contact" class="btn btn-primary">Book a free consultation {ARROW}</a></div></div></section>
{stats_block()}
<section><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">Our Completed Projects</div><h2>Improve &amp; enhance <span class="grad">our projects.</span></h2></div>
<p class="sub rv">Our diverse portfolio reflects our prowess in exceptional customer service, effective CRM implementations, seamless ticketing solutions, dynamic WordPress development, successful digital marketing campaigns, and more.</p></div>{proj_cards()}</div></section>
{testimonial_block()}
<section style="padding-top:0"><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">Our Expert People</div><h2>Meet our professional <span class="grad">team.</span></h2></div>
<div class="rv"><p class="sub">Experienced &amp; knowledgeable professionals who make our customers pleased with their ability to create the best IT solutions.</p><a href="/team" class="btn btn-ghost" style="margin-top:20px">Meet the team {ARROW}</a></div></div>{team_cards()}</div></section>
{cta_block()}'''
page("index.html", "SopnoTec — IT Solutions & Service Agency", "SopnoTec offers tailored IT solutions, customer support, bookkeeping, CRM and digital marketing services.", home)

# ABOUT
about = f'''{phero("Where vision meets <span class='grad'>reality.</span>", "Cutting-edge technology, tailored solutions and expert support for unparalleled business growth.", [("About", None)], "about3", "users")}
<section><div class="wrap">{about_split(["Best quality support","Money back guarantee","Serve the best","Trusted professionals"], ("/contact","Work with us"))}</div></section>
{marquee("tilt")}
{stats_block()}
{why_block()}
<section class="tight"><div class="wrap"><div class="banner rv s"><div class="bgimg" data-parallax="0.08" style="background-image:url('{img('teamphoto')}')"></div>
<div class="eyebrow">SopnoTec</div><h2>Better IT solutions &amp; services <span class="grad">at your fingertips.</span></h2><p class="sub">From customer service to CRM, bookkeeping, development and marketing — one partner for the whole journey.</p><br><a href="/services" class="btn btn-primary">Explore services {ARROW}</a></div></div></section>
{pillars_block()}
<section><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">Our Expert People</div><h2>Meet our professional <span class="grad">team.</span></h2></div><p class="sub rv">A team of experienced &amp; knowledgeable professionals who create the best IT solutions to improve performance of clients.</p></div>{team_cards()}</div></section>
{testimonial_block()}{cta_block()}'''
page("about.html", "About — SopnoTec", "About SopnoTec, a trusted IT solution and service business agency.", about)

# SERVICES
steps = [("Plan","We study your goals, audience and market to craft a strategy that fits."),("Execute","Launch flawlessly, staying flexible to real-time feedback."),("Analyze","Dig into the data for actionable insights and optimization."),("Deliver","Measure success by tangible outcomes for your business.")]
stp = "".join(f'<div class="step"><div class="n">0{i+1}</div><h4>{a}</h4><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
services = f'''{phero("Unleashing excellence through our <span class='grad'>specialized services.</span>", "Embark on a journey of innovation and success. From customer-centric support to cutting-edge development, we transform your aspirations into tangible achievements.", [("Services", None)], "i102", "layers")}
<section><div class="wrap split2">
<div class="rv l"><div class="eyebrow">What We Offer</div><h2>One partner, <span class="grad">ten specialties.</span></h2>
<ul class="bullets">{''.join(f"<li>{ic('check')}{t}</li>" for t in ["SopnoTec delivers personalized solutions, adapting our expertise to meet the unique demands of your business and industry.","Explore a spectrum of services designed to drive innovation, from customer engagement to web development, optimizing every aspect of your business.","Our services are crafted with a focus on tangible outcomes, ensuring your business not only meets but exceeds its goals and aspirations."])}</ul>
<a href="/about" class="btn btn-ghost">About us {ARROW}</a></div>
<div class="rv r" style="position:relative"><div class="mask" style="border-radius:28px;overflow:hidden;border:1px solid var(--line)"><img src="{img('p7567595')}" alt="" style="width:100%;height:460px;object-fit:cover"></div>
<img src="{img('tech')}" alt="" style="position:absolute;right:-30px;bottom:-40px;width:160px;opacity:.5;animation:spin 30s linear infinite"></div>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="svc-grid">{svc_img_cards(SERVICES)}</div></div></section>
<section class="tight"><div class="wrap center"><div class="eyebrow rv">How we work</div><h2 class="rv" style="margin-bottom:60px">From idea to <span class="grad">results.</span></h2><div class="process stagger">{stp}</div></div></section>
{stats_block()}{testimonial_block()}{cta_block()}'''
page("services.html", "Services — SopnoTec", "Customer service, live chat, bookkeeping, CRM, ticketing, cold calling, marketing and WordPress services.", services)

# SERVICE DETAIL
for idx, s in enumerate(SERVICES):
    ch = "".join(f"<li>{ic('check')}{e(c)}</li>" for c in s["checks"])
    btns = "".join(f'<button class="{"on" if i==0 else ""}"><span class="n">0{i+1}</span>{e(t)}</button>' for i, (t, _) in enumerate(s["features"]))
    panes = "".join(f'<div class="pane{" on" if i==0 else ""}"><div class="ic">{ic(s["icon"])}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, (t, p) in enumerate(s["features"]))
    others = [x for x in SERVICES if x is not s]
    rel = [others[(idx + k) % len(others)] for k in range(3)]
    pr = P[s["project"]]
    prev_s, next_s = SERVICES[idx-1], SERVICES[(idx+1) % len(SERVICES)]
    body = f'''{phero(e(s["name"]), s["tagline"], [("Services","/services"),(s["name"],None)], s["card"], s["icon"])}
<section><div class="wrap split2">
<div class="rv l" style="position:relative"><div class="mask" style="border-radius:28px;overflow:hidden;border:1px solid var(--line)"><img src="{img(s['hero'])}" alt="" style="width:100%;height:520px;object-fit:cover"></div>
<div class="chip" style="left:-20px;bottom:40px"><div class="ic">{ic(s['icon'])}</div><div><b>24/7</b><small>Dedicated support</small></div></div>
<div class="chip" style="right:-10px;top:30px;animation-delay:-2s"><div class="ic">★</div><div><b data-count="120">0</b><small>Happy clients</small></div></div></div>
<div class="rv r"><div class="eyebrow">At SopnoTec get</div><h2>{e(s['headline'])}</h2><p class="sub">{e(s['intro'])}</p><ul class="checks">{ch}</ul>
<a href="/contact?service={s['slug']}" class="btn btn-primary">Contact us {ARROW}</a></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">Uplifting Customer Experiences</div><h2>{e(s['name'])} services <span class="grad">at SopnoTec.</span></h2></div></div>
<div class="ftabs rv"><div class="ftab-list">{btns}</div><div class="ftab-panel">{panes}<div class="bign">{idx+1:02d}</div></div></div></div></section>
{pillars_block()}
{why_block()}
<section class="tight"><div class="wrap"><div class="banner rv s"><div class="bgimg" data-parallax="0.08" style="background-image:url('{img(pr['img'])}')"></div>
<div class="eyebrow">Related case study · {e(pr['cat'])}</div><h2>{e(pr['name'])}: <span class="grad">{pr['big']} {e(pr['bigl'])}</span></h2><p class="sub">{e(pr['summary'])}</p><br><a href="{purl(pr)}" class="btn btn-primary">Read the case study {ARROW}</a></div></div></section>
<section><div class="wrap"><div class="head"><div class="rv"><div class="eyebrow">Explore more</div><h2>Other <span class="grad">services.</span></h2></div><a href="/services" class="btn btn-ghost rv">All services {ARROW}</a></div>
<div class="svc-grid">{svc_img_cards(rel)}</div>
<div class="pager"><a href="{surl(prev_s)}"><small>← Previous service</small><b>{e(prev_s['name'])}</b></a><a class="nx" href="{surl(next_s)}"><small>Next service →</small><b>{e(next_s['name'])}</b></a></div></div></section>
{cta_block()}'''
    page(surl(s)[1:] + ".html", f"{s['name']} — SopnoTec", s["short"], body)

# PROJECTS
projects = f'''{phero("Improve &amp; enhance <span class='grad'>our projects.</span>", "Our portfolio illustrates our commitment to excellence — from customer service and CRM to bookkeeping and digital transformation.", [("Projects", None)], "bgmeet", "rocket")}
<section><div class="wrap">{proj_cards()}</div></section>
{stats_block()}{testimonial_block()}{cta_block("Have a project in mind? <span class='grad'>Let's build it.</span>")}'''
page("projects.html", "Projects — SopnoTec", "Case studies from SopnoTec: bookkeeping support, digital assistant and e-commerce support.", projects)

for idx, p in enumerate(PROJECTS):
    paras = "".join(f'<p class="rv">{e(x)}</p>' for x in p["body"])
    st = "".join(f'<div><b class="grad">{a}</b><span>{e(b)}</span></div>' for a, b in p["stats"])
    svcs = "".join(f'<a class="sl" href="{surl(S[x])}">{e(S[x]["name"])} {ARROW}</a>' for x in p["services"])
    tools = "".join(f"<span>{e(t)}</span>" for t in p["tools"])
    prev_p, next_p = PROJECTS[idx-1], PROJECTS[(idx+1) % len(PROJECTS)]
    body = f'''{phero(e(p['name']), p["summary"], [("Projects","/projects"),(p['name'],None)], p["img"], "rocket")}
<section><div class="wrap pd-grid"><div>
<div class="cover mask"><img src="{img(p['img'])}" alt="" data-parallax="0.06" style="transform:scale(1.15)"></div>
<div class="pd-stats stagger">{st}</div>
<div class="prose"><div class="eyebrow rv">The story</div>{paras}</div>
<div class="pager"><a href="{purl(prev_p)}"><small>← Previous project</small><b>{e(prev_p['name'])}</b></a><a class="nx" href="{purl(next_p)}"><small>Next project →</small><b>{e(next_p['name'])}</b></a></div></div>
<aside class="side rv r"><div class="side-card"><h4>Project info</h4><dl><div><dt>Category</dt><dd>{e(p['cat'])}</dd></div><div><dt>Client</dt><dd>Confidential</dd></div><div><dt>Highlight</dt><dd>{p['big']} {e(p['bigl'])}</dd></div></dl><div class="tools" style="margin-top:20px">{tools}</div></div>
<div class="side-card"><h4>Services used</h4>{svcs}</div>
<div class="side-card" style="background:linear-gradient(135deg,rgba(91,110,225,.25),rgba(139,92,246,.15))"><h4 style="color:#fff">Need something similar?</h4><p style="color:#c3c6e6;margin-bottom:18px">Get a free consultation from our experts.</p><a href="/contact" class="btn btn-primary">Let's talk {ARROW}</a></div></aside>
</div></section>{cta_block()}'''
    page(purl(p)[1:] + ".html", f"{p['name']} — SopnoTec Case Study", p["summary"], body)

# TEAM
team = f'''{phero("Meet our professional <span class='grad'>team.</span>", "Experienced & knowledgeable professionals who make our customers pleased with their ability to create the best IT solutions.", [("Team", None)], "teamphoto", "users")}
<section><div class="wrap">{team_cards(full=True)}</div></section>
<section class="tight"><div class="wrap"><div class="banner rv s"><div class="bgimg" data-parallax="0.08" style="background-image:url('{img('group')}')"></div>
<div class="eyebrow">Our culture</div><h2>We help our clients stand out — <span class="grad">and they help us grow.</span></h2><p class="sub">A 10+ strong team across customer support, accounting, development and marketing, serving clients across the globe.</p><br><a href="/contact" class="btn btn-primary">Work with us {ARROW}</a></div></div></section>
{stats_block()}{cta_block()}'''
page("team.html", "Team — SopnoTec", "Meet the SopnoTec team.", team)

# CONTACT
opts = "".join(f'<option value="{s["slug"]}">{e(s["name"])}</option>' for s in SERVICES)
faqs = [("What services does SopnoTec offer?", "Ten specialties: customer service representatives, live chat support, QuickBooks bookkeeping, CRM setup and customization, ticketing desk creation, cold calling / call support, campaign management, digital marketing, social media &amp; LinkedIn engagement, and WordPress development."),
        ("Is the first consultation free?", "Yes — you can receive a free consultation for any kind of IT solution. Just send us a message or call."),
        ("Do you provide support outside business hours?", "Yes. We provide 24/7 support for partners during the process, and our live chat specialists offer round-the-clock assistance."),
        ("Where are your clients based?", "We have worked with clients across the globe. You can reach us on our Ireland and USA numbers."),
        ("Can you work with the tools we already use?", "Yes. We integrate with your existing CRM, email platforms and business tools — including QuickBooks, Shopify, Zapier, JotForm, Trello and Adobe Sign.")]
fq = "".join(f'<details class="rv"><summary>{q}<span class="pm">+</span></summary><div class="ans">{a}</div></details>' for q, a in faqs)
contact = f'''{phero("Feel free to <span class='grad'>get in touch.</span>", "World class IT solutions partner of choice. Reach us any time — we'd love to hear about your project.", [("Contact", None)], "s_csr", "mail")}
<section><div class="wrap contact-grid">
<div class="rv l"><div class="eyebrow">Contact With Us</div><h2>Let's start a <span class="grad">conversation.</span></h2>
<div class="cinfo">
<a href="tel:{SITE['phone1'][1]}"><span class="ic">{ic('phone')}</span><span><small>Call anytime · {SITE['phone1'][2]}</small><b>{SITE['phone1'][0]}</b></span></a>
<a href="tel:{SITE['phone2'][1]}"><span class="ic">{ic('phone')}</span><span><small>Call anytime · {SITE['phone2'][2]}</small><b>{SITE['phone2'][0]}</b></span></a>
<a href="mailto:{SITE['email']}"><span class="ic">{ic('mail')}</span><span><small>Send email</small><b>{SITE['email']}</b></span></a>
<div class="ci"><span class="ic">{ic('pin')}</span><span><small>Visit</small><b>{SITE['address']}</b></span></div></div></div>
<form class="cf rv r" action="/api/lead" method="post" novalidate><input type="hidden" name="form" value="contact"><div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div><div class="field"><input id="n" name="name" autocomplete="name" maxlength="120" placeholder=" " required><label for="n">Your name</label></div>
<div class="field"><input id="em" name="email" type="email" autocomplete="email" maxlength="200" placeholder=" " required><label for="em">Email address</label></div>
<div class="field"><input id="ph" name="phone" type="tel" autocomplete="tel" maxlength="40" placeholder=" "><label for="ph">Phone</label></div>
<div class="field"><select id="svcsel" name="service" aria-label="Service"><option value="">Choose a service</option>{opts}</select></div>
<div class="field full"><input id="sj" name="subject" maxlength="200" placeholder=" "><label for="sj">Subject</label></div>
<div class="field full"><textarea id="m" name="message" rows="6" maxlength="5000" placeholder=" "></textarea><label for="m">Tell us about your project</label></div>
<button class="btn btn-primary field full" type="submit">Send message {ARROW}</button><div class="sent" role="status" aria-live="polite">Thanks! We'll be in touch shortly.</div></form>
</div></section>
<section class="tight"><div class="wrap"><div class="mapbox rv s"><div class="grid"></div><div class="ping"></div><div class="pinx">{ic('pin')}</div><div class="lbl">{SITE['address']}</div></div></div></section>
<section id="faq"><div class="wrap"><div class="center" style="margin-bottom:50px"><div class="eyebrow rv">FAQ</div><h2 class="rv">Questions, <span class="grad">answered.</span></h2></div><div class="faq">{fq}</div></div></section>'''
page("contact.html", "Contact — SopnoTec", "Contact SopnoTec by phone, email or the contact form.", contact)

# PRIVACY
blks = "".join(f'<div class="blk rv"><div class="n">{i+1:02d}</div><div><h3>{e(t)}</h3><p>{e(x)}</p></div></div>' for i, (t, x) in enumerate(PRIVACY))
page("privacy-policy.html", "Privacy Policy — SopnoTec", "SopnoTec privacy policy.",
     phero("Privacy <span class='grad'>policy.</span>", "How we collect, use and protect your information.", [("Privacy Policy", None)], "i104", "shield") + f'<section><div class="wrap legal">{blks}</div></section>')

# 404
page("404.html", "Page not found — SopnoTec", "Page not found",
     f'<section class="nf"><canvas class="net" style="position:absolute;inset:0"></canvas><div class="wrap" style="position:relative"><div class="big grad"><span>4</span><span>0</span><span>4</span></div><h2 style="margin:10px 0 16px">This page took a coffee break.</h2><p class="sub" style="margin:0 auto 30px">The page you are looking for doesn\'t exist or has been moved.</p><a href="/" class="btn btn-primary">Back to home {ARROW}</a></div></section>')

print("built", sorted(os.listdir(OUT)))
