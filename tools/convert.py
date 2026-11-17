"""Turn the original Accuplacer guide (accuplacer-original.html) into the PERT guide (index.html).

Run from the repo root:  python tools/convert.py
Kept as a record of the conversion. Edit index.html directly from now on.
"""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'tools' / 'accuplacer-original.html').read_text(encoding='utf-8')
L = src.split('\n')

def ln(n):  # 1-indexed original line
    return L[n - 1]

def must(cond, what):
    if not cond:
        sys.exit('convert.py: could not apply: ' + what)

# ---------------------------------------------------------------- script: line-based swaps (bottom up)
check_branch = '\n'.join(L[1293:1296])  # original lines 1294-1296, the starting-check results

NEW_TESTS = r'''const TESTS={B:['Number skills'],P:['PERT algebra']};
const T=$('test-area');let run=null;
/* PERT practice test: adapts like the real one and estimates a 50-150 score.
   Each lesson level has a rough difficulty on one scale; ability is re-estimated after every answer. */
const DIFF={whole:[-2.6,-2.1,-1.6],frac:[-2.2,-1.6,-1.1],dec:[-2.2,-1.6,-1],ratio:[-1.8,-1.2,-.6],expr:[-1.4,-.8,-.2],eq:[-1,-.3,.4],lines:[-.6,.1,.8],sys:[-.4,.3,1],pow:[-.6,.2,1],polyf:[-.3,.5,1.3],quad:[0,.9,1.7],radrat:[.2,1,1.8],fn:[-.5,.4,1.2]};
const PN=25,GRID=Array.from({length:81},(_,i)=>-4+i*.1);
const pOK=(t,b)=>.25+.75/(1+Math.exp(-1.7*(t-b)));
const good=x=>x.pick>=0&&x.p.choices[x.pick]===x.p.ans;
function est(qs){let w=GRID.map(t=>Math.exp(-t*t/3.92));qs.forEach(x=>{if(x.pick==null)return;const ok=good(x);w=w.map((v,i)=>v*(ok?pOK(GRID[i],x.b):1-pOK(GRID[i],x.b)))});
  const s=w.reduce((a,b)=>a+b,0),m=w.reduce((a,v,i)=>a+v*GRID[i],0)/s;return{m,sd:Math.sqrt(w.reduce((a,v,i)=>a+v*(GRID[i]-m)**2,0)/s)}}
const toScore=t=>Math.max(50,Math.min(150,Math.round(100+16*t)));
const BANDS=[[123,'College Algebra range','123 or higher is the usual Florida score for College Algebra (MAC 1105).'],[114,'College-ready','114 to 122 is college-ready in Florida and usually places into Intermediate Algebra (MAT 1033).'],[96,'Just below college-ready','96 to 113 is under the college-ready score of 114. Many colleges place this into a developmental math course.'],[50,'Building the basics','Below 96. Work through the number skills and the first algebra lessons, then test again.']];
const band=s=>BANDS.find(b=>s>=b[0]);
function pertItem(k,lv){let g=G[k].filter(x=>x[0]===lv&&x[2]!=='err');if(!g.length)g=G[k].filter(x=>x[2]!=='err');return toMC(pick(g)[1]())}
function nextPert(){const used={},qs=run.qs;qs.forEach(x=>used[x.k]=(used[x.k]||0)+1);const th=qs.length?est(qs).m:-.6,last=qs.length?qs[qs.length-1].k:null;let best=null,bs=1e9;
  Object.keys(DIFF).forEach(k=>DIFF[k].forEach((b,i)=>{if(k===last)return;const s=Math.abs(b-th)+.45*(used[k]||0)+Math.random()*.35;if(s<bs){bs=s;best={k,lv:i+1,b}}}));
  best.p=pertItem(best.k,best.lv);best.pick=null;qs.push(best)}
function menu(){run=null;const h=st.pert||[],ids=Object.keys(TESTS),last=h[h.length-1];
  T.innerHTML=`<div class="group"><h3>PERT practice test</h3><p>${PN} questions that adapt to you the way the real PERT does: get one right and the next is harder. At the end you get an estimated PERT score on the real 50 to 150 scale.</p><div class="cards"><button class="card" data-pt="1"><em>${h.length?'Your scores: '+h.slice(-6).map(x=>x.s).join(' → '):'Not taken yet'}</em><b>Take a PERT practice test</b><span>${last?'Latest '+last.s+' · your goal is '+st.target:PN+' questions, no time limit, new questions every time'}</span></button></div></div>
   <div class="group"><h3>Starting check</h3><p>Two quick questions per lesson. It sets each lesson to Warm-up or Test level for you. Guessing is fine.</p><div class="cards">${ids.map(id=>{const ks=KEYS.filter(k=>GRP[k]===id);return`<button class="card" data-c="${id}"><em>${st.chk[id]?'Done · take again any time':ks.length*2+' questions'}</em><b>${TESTS[id][0]} starting check</b><span>Lessons ${NUM[ks[0]]} to ${NUM[ks[ks.length-1]]}</span></button>`}).join('')}</div></div>`}
function start(id,mode){const qs=[];
  if(mode==='check'){KEYS.filter(k=>GRP[k]===id).forEach(k=>[1,2].forEach(lv=>qs.push({k,lv,p:toMC(gen(k,lv)[1]()),pick:null})));run={id,mode,qs,i:0}}
  else{run={id:'pert',mode:'pert',qs,i:0};nextPert()}ask()}
function ask(){const{qs,i,mode}=run,x=qs[i],P=mode==='pert',N=P?PN:qs.length;
  T.innerHTML=`<div class="pr"><div class="pr-head"><h3>${P?'PERT practice test':TESTS[run.id][0]+' starting check'}</h3><span class="pr-score">Question ${i+1} of ${N}</span></div><div class="meter"><i style="width:${i/N*100}%"></i></div>
    ${P&&i===0?'<p class="tagline">Like the real PERT: no time limit, no going back, and no answers until the end. Work each one on scratch paper.</p>':''}
    <div class="pr-q in">${x.p.q}</div><div class="choices">${x.p.choices.map((c,j)=>`<button class="choice" data-j="${j}" aria-pressed="${x.pick===j}">${esc(c)}</button>`).join('')}${P?'':`<button class="choice" data-j="-1" aria-pressed="${x.pick===-1}">I have not learned this yet</button>`}</div>
    <div class="row" style="justify-content:space-between"><button class="btn ghost" data-q="quit">Quit</button><button class="btn" data-q="next" ${x.pick==null?'disabled':''}>${i===N-1?'Finish and see my score':P?'Confirm answer':'Next question'}</button></div></div>`;pretty(T)}
function results(){const{qs,id,mode}=run,by={};let right=0;qs.forEach(x=>{const b=by[x.k]=by[x.k]||[0,0];b[1]++;if(good(x)){right++;b[0]++}});
''' + check_branch + r'''
  const e=est(qs),s=toScore(e.m),lo=toScore(e.m-e.sd),hi=toScore(e.m+e.sd),B=band(s),h=st.pert=st.pert||[],pb=h.length?Math.max(...h.map(x=>x.s)):0;h.push({d:today(),s,r:right});if(h.length>12)h.shift();save();addXP(right*5);if(h.length>1&&s>pb)confetti();
  const rows=Object.keys(by).sort((a,b)=>by[a][0]/by[a][1]-by[b][0]/by[b][1]).map(k=>`<tr><td><a href="#t-${k}" data-k="${k}">Lesson ${NUM[k]}: ${NAME[k]}</a></td><td class="m">${by[k][0]} of ${by[k][1]}</td><td>${by[k][0]===by[k][1]?'Solid':by[k][0]/by[k][1]>=.5?'Review':'Study this first'}</td></tr>`).join('');
  const miss=qs.filter(x=>!good(x)).map(x=>`<div class="miss"><div class="pr-q">${x.p.q}</div><p><b class="k2">You chose:</b> <span class="m">${esc(x.p.choices[x.pick])}</span> &nbsp; <b class="k3">Correct:</b> <span class="m">${esc(x.p.ans)}</span></p><ol class="hints">${x.p.steps.map(s=>`<li>${s}</li>`).join('')}</ol></div>`).join('');
  const gap=st.target-s;
  T.innerHTML=`<div class="pr in"><div class="pr-head"><h3>PERT practice test results</h3></div><p class="bigscore">${s}<span class="pr-score"> estimated PERT math score</span></p><div class="meter"><i style="width:${s-50}%"></i></div>
    <p class="tagline">Likely somewhere from ${lo} to ${hi} · ${right} of ${PN} right · your goal is ${st.target}</p>
    <p><b>${B[1]}.</b> ${B[2]}</p>
    ${gap<=0?`<p class="tip"><b>At your goal.</b> ${h.length>1&&h[h.length-2].s>=st.target?'That is two in a row at your goal, which is strong evidence you are ready.':'Do it once more on another day to show it was not luck.'}</p>`:`<p>${gap<=6?'Close to your goal.':'Room to grow before your goal.'} Work on the lessons at the top of the list below, then take another test in a few days.</p>`}
    ${h.length>1?`<p class="tagline">Your scores so far: <b>${h.map(x=>x.s).join(' → ')}</b>${s>pb?' · a new personal best':''}</p>`:''}
    <p class="note" style="text-align:left;margin:0">On an adaptive test the number right matters less than how hard your questions got. This is an estimate from this guide's own questions, not an official score.</p>
    <div class="tbl"><table><tr><th>Lesson</th><th>Right</th><th>What to do</th></tr>${rows}</table></div>
    <div class="row l"><button class="btn" data-pt="1">Take another with new questions</button><button class="btn ghost" data-q="quit">Back</button></div>
    ${miss?`<h3>Questions you missed</h3>${miss}`:''}</div>`;T.querySelectorAll('ol.hints').forEach(work);pretty(T);paint()}
T.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  if(b.dataset.pt)return start(null,'pert');if(b.dataset.c&&b.classList.contains('card'))return start(b.dataset.c,'check');
  if(b.dataset.j!==undefined){run.qs[run.i].pick=+b.dataset.j;T.querySelectorAll('.choice').forEach(c=>c.setAttribute('aria-pressed',c===b));T.querySelector('[data-q=next]').disabled=false}
  if(b.dataset.q==='quit')menu();
  if(b.dataset.q==='next'){const N=run.mode==='pert'?PN:run.qs.length;if(run.i>=N-1)results();else{if(run.mode==='pert')nextPert();run.i++;ask()}window.scrollTo(0,0)}});
menu();'''

NEW_WIDGETS = r'''$('fn-rule').innerHTML=RULES.map((r,i)=>`<option value="${i}">${r[0]}</option>`).join('');
[['ln-m',lineW],['ln-b',lineW],['sy-m',sysW],['sy-b',sysW],['pb-a',parabW],['pb-b',parabW],['pb-c',parabW],['fn-rule',fnW],['fn-x',fnW],['pc-p',pctW],['fb-n',fracW],['fb-d',fracW]].forEach(([id,f])=>$(id).addEventListener('input',f));
[lineW,sysW,parabW,fnW,pctW,fracW].forEach(f=>f());'''

NEW_READY = ln(1397).replace("'Accuplacer Ready'", "'PERT Ready'") + '\n' + r'''const CORE=['B','P'],myKeys=()=>KEYS.filter(k=>CORE.includes(GRP[k]));
function ready(){const rows=CORE.map(id=>{const ks=KEYS.filter(k=>GRP[k]===id),p=ks.filter(k=>status(k)>=2).length;return{id,name:TESTS[id][0],p,n:ks.length,ok:p===ks.length}}),ks=myKeys(),need=Math.ceil(ks.length/2),rv=ks.filter(k=>st.sk[k]&&st.sk[k].rv>=1).length,
    h=st.pert||[],l2=h.slice(-2),tOk=l2.length===2&&l2.every(x=>x.s>=st.target),last=h.length?h[h.length-1].s:0,tf=Math.max(0,Math.min(1,(last-80)/(st.target-80)));
  return{rows,rv,need,h,tOk,all:rows.every(r=>r.ok)&&rv>=need&&tOk,pct:Math.round(100*(rows.reduce((a,r)=>a+r.p/r.n,0)/rows.length*.5+(tOk?1:tf*.9)*.3+Math.min(rv,need)/need*.2))}}'''

NEW_STATE = r'''let st={sk:{},days:[],best:{},hist:{},chk:{},xp:0,solved:0,lvlSeen:1,time:{},goal:{},met:{},ex:{},pert:[],target:114,test:null,start:null};
const inDays=n=>{const d=new Date(Date.now()+n*864e5);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
/* progress handed over by the launcher file (#import=...) is used only when this browser has none yet */
try{const m=/[#&]import=([^&]*)/.exec(location.hash);if(m){let have=null;try{have=localStorage.getItem(LS)}catch(e){}const imp=JSON.parse(decodeURIComponent(m[1]));if(imp&&typeof imp==='object'&&!have)localStorage.setItem(LS,JSON.stringify(imp));history.replaceState(null,'',location.pathname+location.search)}}catch(e){}
try{Object.assign(st,JSON.parse(localStorage.getItem(LS))||{})}catch(e){}
if(st.v!==2){st.v=2;delete st.tests;st.hist={};st.best={};st.pert=st.pert||[];st.target=st.target||114;st.lvlSeen=Math.min(st.lvlSeen||1,9);if(!st.test||st.test<inDays(0))st.test=inDays(28)}
if(!st.test)st.test=inDays(28);'''

swaps = [  # (first, last, new) original 1-indexed inclusive
    (1472, 1472, ln(1472) + "\nif('serviceWorker' in navigator&&location.protocol==='https:')navigator.serviceWorker.register('sw.js').catch(()=>{});"),
    (1397, 1400, NEW_READY),
    (1392, 1395, NEW_WIDGETS),
    (1276, 1311, NEW_TESTS),
    (1138, 1138, NEW_STATE),
]
for a, b, new in swaps:
    L[a - 1:b] = [new]

s = '\n'.join(L)

# ---------------------------------------------------------------- script: string swaps
def rep(old, new, count=1):
    global s
    must(s.count(old) >= 1, old[:70])
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)

rep("return p}])});", "return p},'err'])});")
rep("myTests().forEach(id=>{if((st.best[id]||0)<15)work+=25});", "if(!ready().tOk)work+=50;")
rep("text:'Every lesson for your tests is Proficient, every practice test is 15 or better, and half your lessons held up on a later day.",
    "text:'Every lesson is Proficient, your last two PERT practice tests reached your goal, and half your lessons held up on a later day.")
rep("You reach Accuplacer Ready by proving it: every lesson Proficient, every practice test 15 or better.",
    "You reach PERT Ready by proving it: every lesson Proficient and your last two practice tests at your goal score.")
rep(",T=myTests();", ";")
rep("const rows=rd.rows.map(r=>`<tr><td>${r.ok?'✓':'○'}</td><td><b>${r.name} test</b></td><td>${r.p} of ${r.n} lessons Proficient</td><td>Practice test best: ${r.b||'not taken'}${r.b>=15?'':' (need 15 of 20)'}</td></tr>`).join('');",
    "const rows=rd.rows.map(r=>`<tr><td>${r.ok?'✓':'○'}</td><td><b>${r.name}</b></td><td colspan=\"2\">${r.p} of ${r.n} lessons Proficient</td></tr>`).join('')+`<tr><td>${rd.tOk?'✓':'○'}</td><td><b>Practice tests</b></td><td colspan=\"2\">${rd.h.length?'Latest scores: '+rd.h.slice(-3).map(x=>x.s).join(', '):'Not taken yet'}. Your last two need to reach ${st.target}.</td></tr>`;")
rep("""<span>My tests</span><span class="row l">${['A','Q','F'].map(id=>`<label class="chk"><input type="checkbox" id="me-t${id}" data-tt="${id}" ${T.includes(id)?'checked':''}> ${TESTS[id][0]}</label>`).join('')}</span></div>""",
    """<label for="me-goal">Goal score</label><select id="me-goal"><option value="114"${st.target==114?' selected':''}>114 · college-ready (Intermediate Algebra)</option><option value="123"${st.target==123?' selected':''}>123 · College Algebra</option></select></div>""")
rep(" If your college only gives some of the three tests, untick the others and the goal shrinks to match.",
    " Check your college's placement chart for the score you need, and set it as your goal.")
rep("""$('me-area').querySelectorAll('[data-tt]').forEach(c=>c.onchange=()=>{const v=['A','Q','F'].filter(id=>$('me-t'+id).checked);if(!v.length){c.checked=true;return}st.tests=v;delete st.goal[today()];save();paint();profile();checkLevel()})}""",
    """$('me-goal').onchange=e=>{st.target=+e.target.value;delete st.goal[today()];save();paint();profile();checkLevel()}}""")
s = s.replace('Accuplacer', 'PERT')  # remaining profile wording ("Are you ready for the ...", level name)

# ---------------------------------------------------------------- page: head, home, lessons
rep('</head>', '<meta name="robots" content="noindex"><meta name="theme-color" content="#6b3fd0"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="icon-192.png"></head>')
rep('<title>Bailey’s Study Guide</title>', '<title>Bailey’s PERT Study Guide</title>')
rep('<h1>Bailey’s Study Guide</h1>', '<h1>Bailey’s PERT Study Guide</h1>')
s = re.sub(r'(<div class="hero">\s*<h1>[^<]*</h1>\s*<p>)[^<]*(</p>)',
           r'\1All the math on the PERT, in short lessons you tap through one idea at a time. A practice test that adapts like the real one shows how ready you are, and a daily study goal keeps you on track for test day.\2', s, count=1)

a = s.find('<div class="group"><h3>Arithmetic test</h3>')
b = s.find('<div class="block">\n    <h3>What the four levels mean')
must(a > 0 and b > a, 'home groups')
card = lambda k, g, t, d: f'<a class="card" href="#t-{k}" data-k="{k}" data-g="{g}"><em>Lesson</em><b>{t}</b><span>{d}</span></a>'
groups = '''<div class="group"><h3>Number skills</h3><p>The arithmetic everything else on the PERT is built on. Quick wins if any of it is rusty.</p>
    <div class="cards">
      {}
    </div></div>
  <div class="group"><h3>PERT algebra</h3><p>The heart of the PERT math test: expressions, equations, lines, polynomials and quadratics.</p>
    <div class="cards">
      {}
    </div></div>
  <div class="group"><h3>Extra</h3><p>Geometry turns up now and then, mostly inside word problems. Do it once the algebra feels steady.</p>
    <div class="cards">
      {}
    </div></div>

  '''.format(
    '\n      '.join([card('whole', 'B', 'Whole numbers', 'Order of operations, rounding, word problems'),
                     card('frac', 'B', 'Fractions', 'Simplify, add, subtract, multiply, divide'),
                     card('dec', 'B', 'Decimals &amp; percents', 'Converting, comparing, percent problems'),
                     card('ratio', 'B', 'Ratios &amp; proportions', 'Unit rates, cross-multiplying, changing units')]),
    '\n      '.join([card('expr', 'P', 'Expressions', 'Negatives, like terms, distributing'),
                     card('eq', 'P', 'Equations &amp; inequalities', 'Multi-step solving, formulas, word problems'),
                     card('lines', 'P', 'Lines &amp; graphs', 'Slope, y = mx + b, writing equations'),
                     card('sys', 'P', 'Systems of equations', 'Substitution and elimination'),
                     card('pow', 'P', 'Exponents &amp; roots', 'Rules, radicals, scientific notation'),
                     card('polyf', 'P', 'Polynomials &amp; factoring', 'FOIL, trinomials, difference of squares'),
                     card('quad', 'P', 'Quadratics', 'Factoring, the formula, the vertex'),
                     card('radrat', 'P', 'Radicals &amp; rational expressions', 'Square roots, fractions with x, false answers'),
                     card('fn', 'P', 'Functions', 'Notation, domain and range, inverses')]),
    card('geo', 'X', 'Geometry', 'Area, volume, the Pythagorean theorem'))
s = s[:a] + groups + s[b:]

for k in ['stats', 'data', 'geo2', 'explog', 'trig', 'trig2']:
    s, n = re.subn(r'<section class="topic" id="t-%s">.*?</section>\n*' % k, '', s, flags=re.S)
    must(n == 1, 'remove section ' + k)

order = [('whole', 'Number skills'), ('frac', 'Number skills'), ('dec', 'Number skills'), ('ratio', 'Number skills'),
         ('expr', 'PERT algebra'), ('eq', 'PERT algebra'), ('lines', 'PERT algebra'), ('sys', 'PERT algebra'),
         ('pow', 'PERT algebra'), ('polyf', 'PERT algebra'), ('quad', 'PERT algebra'), ('radrat', 'PERT algebra'),
         ('fn', 'PERT algebra'), ('geo', 'Extra')]
for i, (k, grp) in enumerate(order, 1):
    s, n = re.subn(r'(<section class="topic" id="t-%s">\s*<div class="block"><span class="kicker">)[^<]*(</span>)' % k,
                   r'\g<1>Lesson %d · %s\2' % (i, grp), s, count=1)
    must(n == 1, 'kicker ' + k)
rep('<h2>Radical and rational equations</h2>', '<h2>Radicals and rational expressions</h2>')

# practice-test page intro
s = re.sub(r'(<section class="topic" id="t-test">.*?<p class="lead">).*?(</p>)',
           r'\1Two tools live here. The <b>PERT practice test</b> works like the real one: 25 questions that get harder or easier as you go, ending with an estimated score. The <b>starting check</b> is a few quick questions per lesson that works out where to begin. Neither shows answers until the end, and neither is timed.\2',
           s, count=1, flags=re.S)

# test day guide
DAY = '''<section class="topic" id="t-day">
  <div class="block"><span class="kicker">Before you go</span><h2>Test day guide</h2>
  <p class="lead">Knowing exactly how the PERT works removes most of the surprises. Here is what to expect and how to use it to your advantage.</p></div>
  <div class="block"><h3>How the PERT math test works</h3>
    <ul>
      <li><b>30 multiple-choice questions.</b> 25 count toward your score. The other 5 are trial questions that do not count, and you cannot tell which ones they are, so give every question your best.</li>
      <li><b>No time limit.</b> Take as long as you need. Most people finish the math part in under an hour.</li>
      <li><b>Nobody passes or fails.</b> You get a score from 50 to 150, and it only decides which math class you start in.</li>
      <li><b>It adapts to you.</b> A right answer brings a harder question next, so hard questions mean it is going well.</li>
      <li><b>You cannot skip or go back.</b> Each answer is final once you confirm it.</li>
    </ul></div>
  <div class="block"><h3>What you can and cannot bring</h3>
    <ul>
      <li><b>No calculator of your own.</b> An on-screen calculator pops up on some questions only. Practise without one.</li>
      <li><b>Scratch paper is provided.</b> Use it for every problem. Writing each step down frees your head for the thinking.</li>
      <li><b>Bring a photo ID.</b> Check with the testing center for anything else they need.</li>
    </ul></div>
  <div class="block"><h3>What score do you need?</h3>
    <p>In Florida, <b>114</b> is the college-ready math score and usually places you into Intermediate Algebra (MAT 1033). <b>123 or higher</b> usually places you into College Algebra (MAC 1105). Each college publishes its own placement chart, so ask yours which class you are aiming for, then set that score as your goal on your profile.</p></div>
  <div class="block"><h3>On each question</h3>
    <ol>
      <li><b>Read the last line first.</b> Know what it is asking for before you start calculating.</li>
      <li><b>Work it on paper,</b> then find your answer among the choices.</li>
      <li><b>Stuck? Use the choices.</b> Plug each one into the problem and see which works, or cross out the ones that cannot be right.</li>
      <li><b>Check before you confirm.</b> Re-read the question and look for a sign slip. You cannot come back to it.</li>
      <li><b>Then let it go.</b> One hard question does not decide your placement.</li>
    </ol></div>
  <div class="block"><h3>The week before</h3>
    <ul>
      <li>Do a short session here each day instead of one long cram.</li>
      <li>Spend most of the time on lessons marked Learning or Proficient. Polishing what you half-know pays off more than starting brand-new topics.</li>
      <li>Take a <a href="#t-test" data-k="test">PERT practice test</a> every few days and watch the score move.</li>
      <li>Ask the testing center about its retake rules. They differ from college to college.</li>
    </ul></div>
  <div class="block"><h3>If your heart is racing</h3>
    <p>That is your body sending extra fuel to your brain. It is a sign you are ready, and it does not mean you are about to do badly. If worries are crowding your head on the morning of the test, some people find it helps to spend five minutes writing them down on paper first, to get them out of the way.</p>
    <p class="tip"><b>A plan for getting stuck.</b> Decide now: "If I am stuck for a few minutes, I will try the answer choices, pick the best one, and move on." Having the plan ready means you do not have to make that decision under pressure.</p></div>
</section>'''
s, n = re.subn(r'<section class="topic" id="t-day">.*?</section>', lambda m: DAY, s, count=1, flags=re.S)
must(n == 1, 'test day guide')

for bad in ['QAS', 'AAF', 'Accuplacer', 'accuplacer', 'three tests', 'advanced test']:
    if bad in s:
        for m in re.finditer(re.escape(bad), s):
            print('LEFTOVER', bad, '::', s[max(0, m.start() - 80):m.end() + 80].replace('\n', ' '))

(root / 'index.html').write_text(s, encoding='utf-8')
print('wrote index.html', len(s), 'chars')
