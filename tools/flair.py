"""One-time patch (2026-11-17): sunset hero with waves, lesson icons, emoji bursts, score dial."""
import pathlib, sys
p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_text(encoding='utf-8')
if 'function dialSVG' in s:
    sys.exit('already patched')

def rep(o, n):
    global s
    if s.count(o) != 1:
        sys.exit(f'miss({s.count(o)}) ' + o[:80])
    s = s.replace(o, n)

wave = 'M0 45' + ''.join(f' Q{180+720*i} 12 {360+720*i} 45 T{720+720*i} 45' for i in range(4)) + ' V90 H0Z'

CSS = r'''/* ---------- flair: sunset hero with rolling waves, lesson icons, emoji bursts, score dial ---------- */
.hero{position:relative;overflow:hidden;isolation:isolate;border-bottom:0;padding-block:30px 118px;color:#fff;
  background:linear-gradient(180deg,#1d1147 0%,#4b2aa8 30%,#9d4edd 52%,#ff7a59 76%,#ffc861 100%)!important;background-size:auto!important}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background-image:radial-gradient(1.5px 1.5px at 12% 18%,#fff 50%,transparent 51%),radial-gradient(1px 1px at 32% 8%,#fff 50%,transparent 51%),radial-gradient(1.5px 1.5px at 58% 22%,#fff 50%,transparent 51%),radial-gradient(1px 1px at 78% 12%,#fff 50%,transparent 51%),radial-gradient(1px 1px at 90% 30%,#fff 50%,transparent 51%),radial-gradient(1px 1px at 45% 34%,#fff 50%,transparent 51%);opacity:.7}
.hero h1{color:#fff;background:none;-webkit-background-clip:border-box;background-clip:border-box;text-shadow:0 2px 18px rgba(40,10,80,.45);font-size:clamp(2.1rem,7vw,3.1rem)}
.hero p{color:rgba(255,255,255,.92);text-shadow:0 1px 8px rgba(40,10,80,.35)}
.greet{font:600 .95rem var(--body)!important;color:#ffe7b0!important;letter-spacing:.02em;margin:0 0 6px!important}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chips span{font:600 .82rem var(--body);background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);padding:5px 11px;border-radius:999px;color:#fff}
.sun{position:absolute;z-index:-1;right:9%;bottom:44px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 50% 45%,#fff7d1,#ffd36b 55%,#ff9a5a);box-shadow:0 0 70px 26px rgba(255,190,100,.42)}
.waves{position:absolute;left:0;right:0;bottom:-1px;height:92px;z-index:-1;overflow:hidden}
.waves svg{position:absolute;bottom:0;left:0;width:200%}
.waves .w1{fill:#2bb5a8;opacity:.55;height:92px}.waves .w2{fill:#1b7fa6;opacity:.75;height:68px}.waves .w3{fill:var(--bg);height:40px}
@media (prefers-reduced-motion:no-preference){
  .waves .w1{animation:roll 16s linear infinite}.waves .w2{animation:roll 11s linear infinite reverse}.waves .w3{animation:roll 8s linear infinite}
  .sun{animation:sunbob 7s ease-in-out infinite}}
@keyframes roll{to{transform:translateX(-50%)}}
@keyframes sunbob{50%{transform:translateY(6px)}}
.card{position:relative;overflow:hidden}
.card[data-ic]::after{content:attr(data-ic);position:absolute;top:10px;right:12px;font-size:1.45rem;transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.card:hover::after{transform:rotate(-10deg) scale(1.15)}
.card.s3{background:linear-gradient(160deg,color-mix(in srgb,var(--good) 10%,var(--surface)),var(--surface) 70%)}
.group>h3{display:flex;align-items:center;gap:8px;font-size:1.25rem}
.pop-emoji{position:fixed;z-index:9;pointer-events:none;font-size:1.7rem;animation:floatup 1.1s cubic-bezier(.2,.8,.2,1) both}
@keyframes floatup{0%{opacity:0;transform:translate(0,0) scale(.4)}20%{opacity:1;transform:translate(calc(var(--dx)*.3),-20px) scale(1.1)}100%{opacity:0;transform:translate(var(--dx),-110px) scale(.9) rotate(var(--r))}}
.dial{display:block;width:100%;max-width:320px;margin:4px auto 0}
.dial .lbl{fill:var(--muted);font:600 11px var(--math)}.dial .big{fill:var(--ink);font:700 46px var(--display)}
'''
rep('.confetti{position:fixed', CSS + '.confetti{position:fixed')

rep('<div class="hero">\n    <h1>', f'''<div class="hero"><div class="sun" aria-hidden="true"></div>
    <div class="waves" aria-hidden="true"><svg class="w1" viewBox="0 0 2880 90" preserveAspectRatio="none"><path d="{wave}"/></svg><svg class="w2" viewBox="0 0 2880 90" preserveAspectRatio="none"><path d="{wave}"/></svg><svg class="w3" viewBox="0 0 2880 90" preserveAspectRatio="none"><path d="{wave}"/></svg></div>
    <p class="greet" id="greet"></p>
    <h1>''')
rep('keeps you on track for test day.</p>\n  </div>', 'keeps you on track for test day.</p>\n    <div class="chips" id="chips"></div>\n  </div>')
rep("H.insertAdjacentHTML('afterbegin',goalHTML());paintMe();", "H.insertAdjacentHTML('afterbegin',goalHTML());paintMe();paintHero();")

FL = r'''/* ---------- flair helpers ---------- */
const ICON={whole:'🔢',frac:'🍕',dec:'💯',ratio:'⚖️',expr:'✏️',eq:'🟰',lines:'📈',sys:'🔀',pow:'⚡',polyf:'🧩',quad:'🏹',radrat:'🌀',fn:'⚙️',geo:'📐'};
document.querySelectorAll('.card[data-k]').forEach(c=>{if(ICON[c.dataset.k])c.dataset.ic=ICON[c.dataset.k]});
const GH={'Number skills':'🐚','PERT algebra':'🌊','Extra':'🏝️'};document.querySelectorAll('#t-home .group>h3').forEach(h=>{const e=GH[h.textContent.trim()];if(e)h.insertAdjacentHTML('afterbegin',`<span aria-hidden="true">${e}</span>`)});
function paintHero(){const g=$('greet'),c=$('chips');if(!g)return;const h=new Date().getHours(),sk=streak(),l=level(),L=LEVELS[l-1],ps=(st.pert||[]).map(x=>x.s),left=dd(today(),st.test);
  g.textContent=(h<5?'Up late, Bailey':h<12?'Good morning, Bailey':h<17?'Good afternoon, Bailey':'Good evening, Bailey')+' 🌺';
  c.innerHTML=`<span>${L[1]} Level ${l} · ${L[2]}</span>${sk>1?`<span>🔥 ${sk}-day streak</span>`:''}${ps.length?`<span>📝 Best ${Math.max(...ps)}</span>`:''}${left>0?`<span>🗓️ ${left} ${left===1?'day':'days'} to go</span>`:left===0?'<span>🎓 Test day!</span>':''}`}
const EMO=['🌺','🐠','🐢','🌊','⭐','✨','🐬','🌴'];
function burst(el,n){if(calm||!el)return;const r=el.getBoundingClientRect();for(let i=0;i<(n||6);i++){const e=document.createElement('span');e.className='pop-emoji';e.textContent=pick(EMO);e.style.cssText=`left:${r.left+r.width*(.2+Math.random()*.6)}px;top:${r.top}px;--dx:${R(-70,70)}px;--r:${R(-40,40)}deg;animation-delay:${i*40}ms`;document.body.appendChild(e);setTimeout(()=>e.remove(),1500)}}
function dialSVG(sc,goal){const cx=160,cy=150,r=118,ang=v=>Math.PI*(1-(v-50)/100),P=(v,rr)=>[cx+rr*Math.cos(ang(v)),cy-rr*Math.sin(ang(v))],arc=(a,b,col)=>{const[x1,y1]=P(a,r),[x2,y2]=P(b,r);return`<path d="M${x1} ${y1}A${r} ${r} 0 0 1 ${x2} ${y2}" fill="none" stroke="${col}" stroke-width="18"/>`};
  const[gx1,gy1]=P(goal,r-14),[gx2,gy2]=P(goal,r+14),[gl,gt]=P(goal,r+26);
  return`<svg class="dial" viewBox="0 -12 320 200" role="img" aria-label="Estimated score ${sc} on a scale from 50 to 150, goal ${goal}">${arc(50,95.5,'var(--bad)')}${arc(96,113.5,'var(--hi)')}${arc(114,122.5,'var(--good)')}${arc(123,150,'var(--c4)')}
   <line x1="${gx1}" y1="${gy1}" x2="${gx2}" y2="${gy2}" stroke="var(--ink)" stroke-width="3"/><text class="lbl" x="${gl}" y="${gt}" text-anchor="middle">goal ${goal}</text>
   <g id="needle" style="transform-origin:${cx}px ${cy}px;transform:rotate(${(sc-50)/100*180-90}deg)"><line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy-r+26}" stroke="var(--ink)" stroke-width="4" stroke-linecap="round"/></g><circle cx="${cx}" cy="${cy}" r="9" fill="var(--ink)"/>
   <text class="lbl" x="${cx-r}" y="${cy+22}" text-anchor="middle">50</text><text class="lbl" x="${cx+r}" y="${cy+22}" text-anchor="middle">150</text>
   <text class="big" x="${cx}" y="${cy-30}" text-anchor="middle" id="dial-n">${sc}</text></svg>`}
function countUp(el,to){if(!el||calm)return;const t0=performance.now();(function f(t){const p=Math.min(1,(t-t0)/1400),e=1-Math.pow(1-p,3);el.textContent=Math.round(50+(to-50)*e);if(p<1)requestAnimationFrame(f);else el.textContent=to})(t0);
  const n=$('needle');if(n){const end=n.style.transform;n.style.transform='rotate(-90deg)';void n.getBoundingClientRect();n.style.transition='transform 1.4s cubic-bezier(.2,.8,.2,1)';n.style.transform=end}}
'''
rep("/* ================= streaks, badges", FL + "/* ================= streaks, badges")
rep("const b=q('[data-a=new]');b.className='btn';", "burst(q('.fb'),own&&!tries?7:4);const b=q('[data-a=new]');b.className='btn';")
rep("c.appendChild(s)}document.body.appendChild(c);",
    "if(i%4===0){s.textContent=pick(['🌺','🐠','🐢','🌊','⭐','🐬']);s.style.background='none';s.style.width='auto';s.style.height='auto';s.style.fontSize='22px'}c.appendChild(s)}document.body.appendChild(c);")
rep('''<p class="bigscore">${s}<span class="pr-score"> estimated PERT math score</span></p>${h.length>1?chartSVG(h,st.target):''}<div class="meter"><i style="width:${s-50}%"></i></div>''',
    '''${dialSVG(s,st.target)}<p class="note">estimated PERT math score</p>${h.length>1?chartSVG(h,st.target):''}''')
rep("T.querySelectorAll('ol.hints').forEach(work);pretty(T);paint()}",
    "T.querySelectorAll('ol.hints').forEach(work);pretty(T);paint();countUp($('dial-n'),s);if(s>=st.target)setTimeout(()=>confetti(90),900)}")
rep('''<text class="gt" x="${W-R}" y="${Y(goal)-6}" text-anchor="end">Goal ${goal}</text>''',
    '''<text class="gt" x="${L+6}" y="${Y(goal)-6}">Goal ${goal}</text>''')
p.write_text(s, encoding='utf-8')
print('ok')
