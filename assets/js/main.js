(function(){
const $=(s,c=document)=>c.querySelector(s),$$=(s,c=document)=>[...c.querySelectorAll(s)];
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;

// page-leave transition for internal links
const cur=$('#curtain');
document.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const h=a.getAttribute('href');
  if(!h||h.startsWith('#')||h.startsWith('mailto:')||h.startsWith('tel:')||a.target==='_blank'||/^https?:/.test(h)||e.metaKey||e.ctrlKey||RM)return;
  e.preventDefault();cur.classList.add('leave');setTimeout(()=>location.href=h,520)});
addEventListener('pageshow',e=>{if(e.persisted)cur.classList.remove('leave')});

// reveal + counters
function count(el){if(el._d)return;el._d=1;const end=+el.dataset.count,suf=el.dataset.suffix??'+',d=1800,st=performance.now();
  (function f(n){const p=Math.min((n-st)/d,1),v=Math.round(end*(1-Math.pow(1-p,4)));el.textContent=v+suf;if(p<1)requestAnimationFrame(f)})(st)}
function reveal(t){if(t._rv)return;t._rv=1;
  if(t.classList.contains('ttiles')){[...t.querySelectorAll('.ttile')].forEach((x,i)=>setTimeout(()=>x.classList.add('in'),i*220));return}
  t.classList.add('in');
  if(t.classList.contains('stagger'))[...t.children].forEach((c,i)=>c.style.transitionDelay=(i*.09)+'s');
  if(t.dataset.count)count(t);$$('[data-count]',t).forEach(count)}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){reveal(e.target);io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});
const RVSEL='.rv,.stagger,[data-count],.mask,.ttiles';
// .mask uses clip-path (invisible to IntersectionObserver) – handled by the geometric sweep below
$$('.rv,.stagger,[data-count],.ttiles').forEach(el=>io.observe(el));
// geometric fallback: reveals anything on screen even if IntersectionObserver is throttled (hidden tabs, iframes, view switches)
function sweep(){const H=innerHeight;$$(RVSEL).forEach(el=>{if(el._rv)return;const r=el.getBoundingClientRect();if((r.width||r.height)&&r.top<H*0.94&&r.bottom>0)reveal(el)})}
window.__sweep=sweep;let sq=0;function qs(){if(!sq){sq=1;requestAnimationFrame(()=>{sq=0;sweep()})}}
addEventListener('scroll',qs,{passive:true});addEventListener('resize',qs);setTimeout(sweep,60);setInterval(sweep,700);

// nav / progress / parallax / to-top
const nav=$('nav.main'),pr=$('#progress'),tt=$('#totop'),par=$$('[data-parallax]'),ringc=$('#totop .ringp circle:last-child');
const C=2*Math.PI*24;if(ringc){ringc.style.strokeDasharray=C}
function onScroll(){const y=scrollY,h=document.documentElement.scrollHeight-innerHeight,p=h>0?y/h:0;
  nav.classList.toggle('scrolled',y>60);pr.style.width=p*100+'%';tt.classList.toggle('show',y>600);if(ringc)ringc.style.strokeDashoffset=C*(1-p);
  par.forEach(el=>{const r=el.getBoundingClientRect();el.style.transform=`translateY(${(r.top+r.height/2-innerHeight/2)*el.dataset.parallax}px)`})}
addEventListener('scroll',onScroll,{passive:true});onScroll();
tt.onclick=()=>scrollTo({top:0,behavior:'smooth'});
$('.burger').onclick=()=>nav.classList.toggle('open');

// active link
const here=location.pathname.split('/').pop()||'index.html';
$$('.menu>li>a').forEach(a=>{const h=a.getAttribute('href');if(h===here||(a.dataset.match&&here.startsWith(a.dataset.match)))a.classList.add('on')});

// cursor glow + spotlight/tilt
const gl=$('#glow');
if(!RM&&matchMedia('(pointer:fine)').matches){
  addEventListener('pointermove',e=>{gl.style.left=e.clientX+'px';gl.style.top=e.clientY+'px'});
  document.addEventListener('pointermove',e=>{const c=e.target.closest('[data-tilt]');if(!c)return;const r=c.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;
    c.style.setProperty('--mx',x+'px');c.style.setProperty('--my',y+'px');
    c.style.transform=`perspective(900px) rotateX(${(y/r.height-.5)*-7}deg) rotateY(${(x/r.width-.5)*7}deg) translateY(-6px)`});
  document.addEventListener('pointerout',e=>{const c=e.target.closest('[data-tilt]');if(c&&!c.contains(e.relatedTarget))c.style.transform=''});
  $$('.btn').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.translate=`${(e.clientX-r.left-r.width/2)*.15}px ${(e.clientY-r.top-r.height/2)*.25}px`});b.addEventListener('pointerleave',()=>b.style.translate='')});
} else gl.style.display='none';

// marquee duplicate
$$('.track').forEach(t=>t.innerHTML+=t.innerHTML);

// hero slider
const slides=$$('.slide'),dots=$$('.dots button');let si=0,timer;
function go(n){if(n===si&&slides[si].classList.contains('on'))return;slides[si].classList.remove('on');slides[si].classList.add('out');const old=si;setTimeout(()=>slides[old].classList.remove('out'),700);
  si=(n+slides.length)%slides.length;setTimeout(()=>slides[si].classList.add('on'),250);
  dots.forEach((d,i)=>{d.classList.remove('on');void d.offsetWidth;if(i===si)d.classList.add('on')});clearTimeout(timer);timer=setTimeout(()=>go(si+1),6000)}
if(slides.length){slides.forEach(s=>$$('h1',s).forEach(h=>{h.innerHTML=h.textContent.trim().split(/\s+/).map((w,i)=>`<span class="w"><span style="transition-delay:${i*.07}s">${w}</span></span>`).join(' ')}));
  dots.forEach((d,i)=>d.onclick=()=>go(i));slides[0].classList.add('on');dots[0]&&dots[0].classList.add('on');timer=setTimeout(()=>go(1),6000)}

// feature tabs
$$('.ftabs').forEach(w=>{const bs=$$('.ftab-list button',w),ps=$$('.pane',w);let k=0,t;
  function sh(i){k=i;bs.forEach((b,j)=>{b.classList.remove('on');void b.offsetWidth;b.classList.toggle('on',j===i)});ps.forEach((p,j)=>p.classList.toggle('on',j===i));clearTimeout(t);t=setTimeout(()=>sh((k+1)%bs.length),7000)}
  bs.forEach((b,i)=>b.onclick=()=>sh(i));const o=new IntersectionObserver(es=>{if(es[0].isIntersecting){sh(0);o.disconnect()}});o.observe(w)});

// forms
$$('form.cf').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();$('.sent',f).style.display='block';f.reset()}));
$$('.news').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const b=$('button',f);b.textContent='Subscribed ✓';f.reset()}));
const q=new URLSearchParams(location.search).get('service');if(q&&$('#svcsel'))$('#svcsel').value=q;
$$('#yr').forEach(y=>y.textContent=new Date().getFullYear());

// network canvas
$$('canvas.net').forEach(c=>{const x=c.getContext('2d');let W,H,pts=[],m={x:-999,y:-999};const dp=Math.min(devicePixelRatio||1,2);
  function rs(){W=c.width=c.offsetWidth*dp;H=c.height=c.offsetHeight*dp;const n=Math.min(90,Math.floor(W*H/(26000*dp)));pts=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.4*dp,vy:(Math.random()-.5)*.4*dp}))}
  rs();addEventListener('resize',rs);
  c.parentElement.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();m.x=(e.clientX-r.left)*dp;m.y=(e.clientY-r.top)*dp});
  const D=140*dp;let vis=true;new IntersectionObserver(es=>vis=es[0].isIntersecting).observe(c);
  (function loop(){if(vis&&!RM){x.clearRect(0,0,W,H);
    for(const p of pts){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;const dx=p.x-m.x,dy=p.y-m.y,dd=Math.hypot(dx,dy);if(dd<160*dp&&dd>0){p.x+=dx/dd*1.2;p.y+=dy/dd*1.2}}
    for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){const a=pts[i],b=pts[j],d=Math.hypot(a.x-b.x,a.y-b.y);if(d<D){x.strokeStyle=`rgba(129,140,248,${(1-d/D)*.35})`;x.lineWidth=dp;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}}
    for(const p of pts){x.fillStyle='rgba(34,199,224,.8)';x.beginPath();x.arc(p.x,p.y,1.6*dp,0,7);x.fill()}}
    requestAnimationFrame(loop)})()});
})();
// testimonial deck + sliding tiles
(function(){
const $$=(s,c=document)=>[...c.querySelectorAll(s)];
$$('.tdeck').forEach(deck=>{const sec=deck.closest('section');const cards=$$('.tcard',deck),nav=$$('.tnav button',sec),stack=deck.querySelector('.tstack');let cur=0,t,busy=false;const n=cards.length;
  function layout(){cards.forEach((c,i)=>c.dataset.pos=(i-cur+n)%n);nav.forEach((b,i)=>b.classList.toggle('on',i===cur));
    const h=Math.max(...cards.map(c=>c.offsetHeight));if(h)stack.style.height=(h+100)+'px'}
  function go(k,rev){if(busy||k===cur)return;busy=true;const old=cards[cur];old.classList.add('leave');if(rev)old.classList.add('rev');
    setTimeout(()=>{cur=(k+n)%n;layout();setTimeout(()=>{old.classList.remove('leave','rev');busy=false},60)},420);clearTimeout(t);t=setTimeout(()=>go(cur+1),7000)}
  deck.querySelector('.next').onclick=()=>go(cur+1);deck.querySelector('.prev').onclick=()=>go(cur-1,true);
  nav.forEach((b,i)=>b.onclick=()=>go(i,i<cur));
  let x0=null;stack.addEventListener('pointerdown',e=>x0=e.clientX);stack.addEventListener('pointerup',e=>{if(x0!==null&&Math.abs(e.clientX-x0)>50)go(cur+(e.clientX<x0?1:-1),e.clientX>x0);x0=null});
  layout();addEventListener('resize',layout);
  new IntersectionObserver((es,o)=>{if(es[0].isIntersecting){layout();t=setTimeout(()=>go(cur+1),7000);o.disconnect()}}).observe(deck)});

})();
