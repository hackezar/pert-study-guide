"""One-time patch (2026-11-17): cloud save, notes from Jack, mistake notebook, score chart,
badges + streaks, formula sheet, speed round. Run once from the repo root: python tools/add_features.py"""
import pathlib, sys

p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_text(encoding='utf-8')
if 'pert_save' in s:
    sys.exit('already patched')

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit(f'expected exactly one match ({s.count(old)}): {old[:90]}')
    s = s.replace(old, new)

# ------------------------------------------------------------------ CSS
rep('.confetti{position:fixed', r'''/* streaks, badges, notes, chart, speed round, formula sheet */
.streak{display:inline-flex;align-items:center;gap:4px;font:700 .85rem var(--body);color:var(--c2)}
.badges{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.badge{border:1px solid var(--line);border-radius:10px;padding:10px;display:flex;gap:10px;align-items:center;background:var(--surface)}
.badge i{font-style:normal;font-size:1.6rem;line-height:1}.badge b{display:block;font-size:.9rem}.badge span{font-size:.8rem;color:var(--muted)}
.badge.off{opacity:.45}.badge.off i{filter:grayscale(1)}
.notes{display:flex;flex-direction:column;gap:10px}
.note-card{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:12px 14px}
.note-card p{max-width:none}.note-card small{color:var(--muted);font-size:.8rem}
.letter{font-size:1.05rem;line-height:1.6;max-width:32ch;margin:0 auto}
.chart{display:block;width:100%;max-width:420px;height:auto}
.chart .gl{stroke:var(--line);stroke-width:1}.chart .goal{stroke:var(--c3);stroke-width:2;stroke-dasharray:6 4}
.chart .ln{fill:none;stroke:var(--accent);stroke-width:3;stroke-linejoin:round}.chart .pt{fill:var(--accent);stroke:var(--surface);stroke-width:2}
.chart text{fill:var(--muted);font:500 11px var(--math)}.chart .gt{fill:var(--c3);font-weight:600}.chart .vt{fill:var(--ink);font-weight:600}
.timer{font:700 2.4rem/1 var(--display);text-align:center}.timer.low{color:var(--bad)}
.spq{font:600 1.6rem var(--math);text-align:center;min-height:2.2em;display:flex;align-items:center;justify-content:center}
@keyframes shake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
@media (prefers-reduced-motion:no-preference){.shake{animation:shake .25s}}
.sheet{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.sheet section{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;display:flex;flex-direction:column;gap:6px;break-inside:avoid}
.sheet h3{font-size:1rem;color:var(--accent)}.sheet p,.sheet li{font-size:.92rem}.sheet ul{gap:3px}
.sync{display:flex;flex-direction:column;gap:8px}
.sync input{font:500 .9rem var(--math);padding:8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink);width:100%}
@media print{.top,.nextrow,.pager,.btn,button,.hero,noscript{display:none!important}body{background:#fff;color:#000}.topic{display:none!important}#t-sheet{display:flex!important}.sheet section{border-color:#999}}
.confetti{position:fixed''')

# ------------------------------------------------------------------ HTML: home buttons, new pages
rep('''<div class="row l"><a class="btn ghost" href="#t-test" data-k="test">Practice tests</a><a class="btn ghost" href="#t-day" data-k="day">Test day guide</a></div>''',
    '''<div class="row l" id="home-tools"><a class="btn ghost" href="#t-test" data-k="test">Practice tests</a><a class="btn ghost" href="#t-nb" data-k="nb">Mistake notebook</a><a class="btn ghost" href="#t-speed" data-k="speed">Speed round</a><a class="btn ghost" href="#t-sheet" data-k="sheet">Formula sheet</a><a class="btn ghost" href="#t-day" data-k="day">Test day guide</a></div>''')

SHEET = '''<section class="topic" id="t-nb">
  <div class="block"><span class="kicker">Your redo pile</span><h2>Mistake notebook</h2>
  <p class="lead">Every problem you miss lands here. You get a fresh version of the same kind of problem, and it leaves the notebook once you get it right on two different days. Clearing it is one of the fastest ways to raise a score.</p></div>
  <div id="nb-area" class="part"></div>
</section>

<section class="topic" id="t-speed">
  <div class="block"><span class="kicker">60 seconds</span><h2>Speed round</h2>
  <p class="lead">Quick mental math against the clock: times tables, negatives, fractions, percents and powers. The faster these come, the more brain you have left for the hard questions.</p></div>
  <div id="sp-area"></div>
</section>

<section class="topic" id="t-sheet">
  <div class="block"><span class="kicker">One page</span><h2>Formula sheet</h2>
  <p class="lead">Every rule the PERT math test leans on, in one place. Read it the night before, or print it and stick it on the fridge.</p>
  <div class="row l"><button class="btn ghost" onclick="window.print()">Print this page</button></div></div>
  <div class="sheet">
    <section><h3>Order of operations</h3><p>Parentheses, Exponents, then Multiply and Divide left to right, then Add and Subtract left to right.</p><p class="m">24 ÷ 4 × 2 = 12</p></section>
    <section><h3>Negatives</h3><ul><li>Minus a negative is plus: <span class="m">5 − (−3) = 8</span></li><li>Same signs multiply to positive, different signs to negative</li><li><span class="m">(−2)² = 4</span> but <span class="m">−2² = −4</span></li></ul></section>
    <section><h3>Fractions</h3><ul><li>Add or subtract: match the bottoms first</li><li>Multiply: straight across</li><li>Divide: flip the second, then multiply</li><li>Mixed number: <span class="m">2 1/3 = 7/3</span></li></ul></section>
    <section><h3>Percents</h3><ul><li>part = percent × whole</li><li>Percent change = change ÷ original</li><li>25% off means you pay 75%</li><li><span class="m">1/4 = 0.25 = 25%</span>, <span class="m">1/8 = 12.5%</span></li></ul></section>
    <section><h3>Ratios and proportions</h3><ul><li>Cross-multiply: <span class="m">a/b = c/d</span> means <span class="m">ad = bc</span></li><li>Unit rate: divide to get the amount for one</li><li>Smaller unit, multiply. Bigger unit, divide.</li></ul></section>
    <section><h3>Solving equations</h3><ol><li>Distribute</li><li>Combine like terms</li><li>x terms on one side, numbers on the other</li><li>Divide by the number on x</li></ol><p>Flip an inequality sign when you multiply or divide by a negative.</p></section>
    <section><h3>Lines</h3><ul><li><span class="m">y = mx + b</span>: m is the slope, b is where it crosses the y-axis</li><li>Slope = change in y ÷ change in x</li><li>Parallel: same slope. Perpendicular: flip it and change the sign</li><li>x-intercept: set y = 0</li></ul></section>
    <section><h3>Systems</h3><ul><li>Substitution: plug one equation into the other</li><li>Elimination: add the equations so a letter cancels</li><li>Same slope, different b: no solution</li></ul></section>
    <section><h3>Exponents</h3><ul><li>Multiply: add exponents. Divide: subtract</li><li>Power of a power: multiply</li><li><span class="m">x⁰ = 1</span> and <span class="m">x⁻² = 1/x²</span></li><li><span class="m">√50 = √25 · √2 = 5√2</span></li></ul></section>
    <section><h3>Polynomials and factoring</h3><ul><li>FOIL: First, Outer, Inner, Last</li><li><span class="m">(x + a)² = x² + 2ax + a²</span></li><li><span class="m">x² − a² = (x + a)(x − a)</span></li><li>Trinomial: two numbers that multiply to the last and add to the middle</li><li>Always pull out a common factor first</li></ul></section>
    <section><h3>Quadratics</h3><ul><li>Get 0 on one side, factor, set each part to 0</li><li>x = <span class="fr"><span>−b ± <span class="rt">√<span class="rad">b² − 4ac</span></span></span><span>2a</span></span></li><li><span class="m">b² − 4ac</span> positive: two answers, zero: one, negative: none</li><li>Vertex at <span class="m">x = −b ÷ 2a</span></li></ul></section>
    <section><h3>Radicals and fractions with x</h3><ul><li>Square both sides, then check every answer</li><li>Cancel whole factors only, never single terms</li><li>The bottom of a fraction can never be 0</li><li>No square roots of negatives</li></ul></section>
    <section><h3>Functions</h3><ul><li><span class="m">f(3)</span>: put 3 in for every x</li><li><span class="m">f(g(x))</span>: work inside out</li><li>Inverse: run it backwards</li></ul></section>
    <section><h3>Geometry</h3><ul><li>Rectangle: <span class="m">A = lw</span>, <span class="m">P = 2l + 2w</span></li><li>Triangle: <span class="m">A = ½bh</span>, angles add to 180°</li><li>Circle: <span class="m">A = πr²</span>, <span class="m">C = 2πr</span></li><li>Right triangle: <span class="m">a² + b² = c²</span></li></ul></section>
    <section><h3>Words into math</h3><ul><li>of, times, per: multiply</li><li>less than: subtract, and it flips the order. "5 less than x" is <span class="m">x − 5</span></li><li>is, equals: =</li><li>sum, total: add</li></ul></section>
  </div>
</section>

<section class="topic" id="t-day">'''
rep('<section class="topic" id="t-day">', SHEET)

# ------------------------------------------------------------------ script hooks
rep("const save=()=>{try{localStorage.setItem(LS,JSON.stringify(st))}catch(e){}};",
    "const save=()=>{st.saved=Date.now();try{localStorage.setItem(LS,JSON.stringify(st))}catch(e){}if(typeof cloudSoon==='function')cloudSoon()};")
rep("const ORDER=['home','today',...KEYS,'test','day','me'],PAGE={home:'Home',today:\"Today's session\",test:'Practice tests',day:'Test day guide',me:'Your profile'};",
    "const ORDER=['home','today',...KEYS,'test','nb','speed','sheet','day','me'],PAGE={home:'Home',today:\"Today's session\",test:'Practice tests',nb:'Mistake notebook',speed:'Speed round',sheet:'Formula sheet',day:'Test day guide',me:'Your profile'};")
rep('''<option value="test">Practice tests</option><option value="day">Test day guide</option>''',
    '''<option value="test">Practice tests</option><option value="nb">Mistake notebook${st.nb&&st.nb.length?' ('+st.nb.length+')':''}</option><option value="speed">Speed round</option><option value="sheet">Formula sheet</option><option value="day">Test day guide</option>''')
rep("return`<div class=\"days\">${out.join('')}<span>${n} of the last 7 days</span></div>`}",
    "const sk2=typeof streak==='function'?streak():0;return`<div class=\"days\">${out.join('')}<span>${n} of the last 7 days</span>${sk2>1?`<span class=\"streak\">🔥 ${sk2}-day streak</span>`:''}</div>`}")
rep("""<a class="btn" href="#t-today" data-k="today">Start today's 10 minutes</a>""",
    """<a class="btn" href="#t-today" data-k="today">Start today's 10 minutes</a>${st.nb&&st.nb.length?`<a class="btn ghost" href="#t-nb" data-k="nb">Mistake notebook (${st.nb.length})</a>`:''}""")
rep("if(k==='today'&&!sess)todayIntro();if(k==='me')profile();",
    "if(k==='today'&&!sess)todayIntro();if(k==='me')profile();if(k==='nb'&&!nbRun)nbIntro();if(k==='speed'&&!spRun)spIntro();if(k==='test'&&!run)menu();")
rep("if(res.ok){if(!st.days.includes(t))st.days=[...st.days,t].slice(-60);",
    "if(res.ok){markDay();")
# items remember which generator made them, so misses can go to the notebook
rep("return{key:k,lv:2,p:gen(k,2)[1](),review:true,",
    "const g2=gen(k,2);return{key:k,lv:2,p:g2[1](),gi:G[k].indexOf(g2),review:true,")
rep("const f=gen(key,s.lvl,last);last=f;return{key,lv:s.lvl,p:f[1]()}",
    "const f=gen(key,s.lvl,last);last=f;return{key,lv:s.lvl,p:f[1](),gi:G[key].indexOf(f)}")
rep("return{key:k,lv,p:gen(k,lv)[1](),review:true}",
    "const g3=gen(k,lv);return{key:k,lv,p:g3[1](),gi:G[k].indexOf(g3),review:true}")
rep("function missed(msg){if(!tries){miss++;streak=0}",
    "function missed(msg){if(!tries){miss++;streak=0;if(cfg.nb&&it.nbx){it.nbx.ok=[];save()}else if(it.key)nbAdd(it.key,it.lv,it.gi)}")
rep("const res={ok:true,hints:shown,first:!tries,tries},own=shown<it.p.steps.length;let msg=record(it,res);",
    "const res={ok:true,hints:shown,first:!tries,tries},own=shown<it.p.steps.length;let msg=record(it,res);if(cfg.nb&&it.nbx)msg+=nbHit(it.nbx,res.first&&!shown);")
rep("function pertItem(k,lv){let g=G[k].filter(x=>x[0]===lv&&x[2]!=='err');if(!g.length)g=G[k].filter(x=>x[2]!=='err');return toMC(pick(g)[1]())}",
    "function pertItem(k,lv){let g=G[k].filter(x=>x[0]===lv&&x[2]!=='err');if(!g.length)g=G[k].filter(x=>x[2]!=='err');const f=pick(g);return[toMC(f[1]()),G[k].indexOf(f)]}")
rep("best.p=pertItem(best.k,best.lv);", "[best.p,best.gi]=pertItem(best.k,best.lv);")
rep("h.push({d:today(),s,r:right});",
    "h.push({d:today(),s,r:right,t:Date.now()});markDay();qs.forEach(x=>{if(!good(x))nbAdd(x.k,x.lv,x.gi)});")
rep('''<p class="bigscore">${s}<span class="pr-score"> estimated PERT math score</span></p>''',
    '''<p class="bigscore">${s}<span class="pr-score"> estimated PERT math score</span></p>${h.length>1?chartSVG(h,st.target):''}''')
rep('''${miss?`<h3>Questions you missed</h3>${miss}`:''}</div>`;T.querySelectorAll('ol.hints')''',
    '''${miss?`<h3>Questions you missed</h3><p class="tagline">All of these are now in your <a href="#t-nb" data-k="nb">mistake notebook</a> for a redo on another day.</p>${miss}`:''}</div>`;T.querySelectorAll('ol.hints')''')
rep('''<span>${last?'Latest '+last.s+' · your goal is '+st.target:PN+' questions, no time limit, new questions every time'}</span></button></div></div>''',
    '''<span>${last?'Latest '+last.s+' · your goal is '+st.target:PN+' questions, no time limit, new questions every time'}</span></button></div>${h.length?chartSVG(h,st.target):''}</div>''')
rep("function addXP(n,quiet){if(!n)return;st.xp=(st.xp||0)+n;save();if(!quiet)toast('+'+n+' XP');paintMe();setTimeout(checkLevel,900)}",
    "function addXP(n,quiet){if(!n)return;st.xp=(st.xp||0)+n;save();if(!quiet)toast('+'+n+' XP');paintMe();setTimeout(()=>{checkLevel();checkRewards()},900)}")

# profile: badges, notes, chart, cloud save
rep('''<div class="block"><h3>Your plan</h3>''',
    '''${(st.pert||[]).length?`<div class="block"><h3>Practice test scores</h3>${chartSVG(st.pert,st.target)}</div>`:''}
   <div class="block"><h3>Notes from Jack</h3>${notesHTML()}</div>
   <div class="block"><h3>Badges</h3><p class="tagline">${streak()>1?`<span class="streak">🔥 ${streak()}-day streak</span> · `:''}${BADGES.filter(b=>st.bd&&st.bd[b[0]]).length} of ${BADGES.length} earned</p><div class="badges">${badgesHTML()}</div></div>
   <div class="block"><h3>Your plan</h3>''')
rep('''<div class="block"><h3>Levels</h3>''', '''<div class="block"><h3>Cloud save</h3><div class="sync" id="sync-box">${syncHTML()}</div></div>
   <div class="block"><h3>Levels</h3>''')

FEATURES = r'''/* ================= streaks, badges, notes from Jack, notebook, speed round, cloud save ================= */
function markDay(){const t=today();if(!st.days.includes(t))st.days=[...st.days,t].slice(-400);const h=new Date().getHours();if(h>=22||h<3)st.owl=1;if(h>=4&&h<8)st.early=1}
const dayAdd=(s,n)=>{const d=new Date(s+'T12:00:00');d.setDate(d.getDate()+n);return iso(d)};
function streak(){const set=new Set(st.days);let d=today();if(!set.has(d))d=dayAdd(d,-1);let n=0;while(set.has(d)){n++;d=dayAdd(d,-1)}return n}
const allP=g=>KEYS.filter(k=>GRP[k]===g).every(k=>status(k)>=2);
const pScores=()=>(st.pert||[]).map(x=>x.s);

const BADGES=[
 ['first','🌱','First step','Get your first problem right',()=>st.solved>=1],
 ['st3','🔥','On a roll','Study 3 days in a row',()=>streak()>=3],
 ['st7','⚡','Full week','Study 7 days in a row',()=>streak()>=7],
 ['st14','🌋','Unstoppable','Study 14 days in a row',()=>streak()>=14],
 ['prof','⭐','Got it','Make a lesson Proficient',()=>KEYS.some(k=>status(k)>=2)],
 ['mast','💎','Locked in','Make a lesson Mastered',()=>KEYS.some(k=>status(k)>=3)],
 ['num','🧮','Number pro','Every number skills lesson Proficient',()=>allP('B')],
 ['alg','📐','Algebra pro','Every PERT algebra lesson Proficient',()=>allP('P')],
 ['t1','📝','Test run','Finish a PERT practice test',()=>pScores().length>=1],
 ['up','📈','Climbing','Beat your first practice score by 5 points',()=>{const s=pScores();return s.length>1&&Math.max(...s.slice(1))>=s[0]+5}],
 ['goal','🎯','Goal reached','Reach your goal score on a practice test',()=>pScores().some(x=>x>=st.target)],
 ['p100','💯','Hundred club','Solve 100 problems',()=>st.solved>=100],
 ['p500','🏅','Math machine','Solve 500 problems',()=>st.solved>=500],
 ['nb10','📓','Fixer','Clear 10 problems from the mistake notebook',()=>(st.nbCleared||0)>=10],
 ['sp15','🏎️','Quick hands','Score 15 in a speed round',()=>(st.spBest||0)>=15],
 ['sp25','🚀','Lightning','Score 25 in a speed round',()=>(st.spBest||0)>=25],
 ['owl','🦉','Night owl','Study after 10 pm',()=>!!st.owl],
 ['early','🌅','Early bird','Study before 8 am',()=>!!st.early],
 ['ready','🎓','PERT Ready','Reach the final level',()=>level()===10]];
function badgesHTML(){st.bd=st.bd||{};return BADGES.map(b=>`<div class="badge${st.bd[b[0]]?'':' off'}"><i>${b[1]}</i><div><b>${b[2]}</b><span>${st.bd[b[0]]?'Earned '+fmtDay(st.bd[b[0]]):b[3]}</span></div></div>`).join('')}

/* Notes from Jack: each unlocks once, at a milestone. Edit the words freely. */
const NOTES=[
 ['start','You started!',()=>st.solved>=1,"You started. Honestly that is the hardest part, and you already did it. Proud of you."],
 ['st3','Three days in a row',()=>streak()>=3,"Three days in a row. A little bit every day is exactly how this works. Keep it going."],
 ['prof','Your first lesson',()=>KEYS.some(k=>status(k)>=2),"Your first lesson is Proficient. That one is yours now. On to the next."],
 ['t1','First practice test',()=>pScores().length>=1,"First practice test done. Whatever the number was, it is just the starting line. Now you know exactly what to work on."],
 ['comeback','Welcome back',()=>!!st.cbNow,"Welcome back! Breaks happen to everyone. One short session today is all it takes to get rolling again."],
 ['num','Number skills done',()=>allP('B'),"All the number skills are done. That is the foundation everything else sits on, and yours is solid."],
 ['up','Your score went up',()=>{const s=pScores();return s.length>1&&Math.max(...s.slice(1))>=s[0]+5},"Your practice score went up. That is not luck, that is your work showing. I love seeing it."],
 ['half','Halfway there',()=>{const ks=KEYS.filter(k=>GRP[k]!=='X');return ks.filter(k=>status(k)>=2).length>=Math.ceil(ks.length/2)},"Halfway through the lessons. You are really doing this."],
 ['st7','A whole week',()=>streak()>=7,"A whole week straight. I know it is not always easy to sit down and do math after a long day. You are doing it anyway, and that says a lot about you."],
 ['p100','100 problems',()=>st.solved>=100,"100 problems solved. That is a lot of math. Treat yourself to something good tonight."],
 ['nb10','Ten fixed for good',()=>(st.nbCleared||0)>=10,"Ten mistakes fixed for good. That is literally how scores go up."],
 ['goal','Goal score!',()=>pScores().some(x=>x>=st.target),"You hit your goal score on a practice test! Do it one more time and you will know it was not a fluke."],
 ['alg','Algebra done',()=>allP('P'),"Every algebra lesson is Proficient. That is the whole heart of the test. Seriously impressive."],
 ['ready','PERT Ready',()=>level()===10,"PERT Ready. You put in the work and it shows. Go in calm, take your time on every question, and remember there is no clock. I am so proud of you."],
 ['testday','Test day',()=>today()===st.test,"It is test day! You have prepared for this. Breathe, read each question twice, and trust your work. I cannot wait to hear how it goes."]];
function notesHTML(){st.notes=st.notes||{};const got=NOTES.filter(n=>st.notes[n[0]]),left=NOTES.length-got.length;
  return`<p class="tagline">${got.length?'Tap back through these any time.':'Jack hid notes for you along the way. They unlock as you hit milestones.'}${left?` ${left} still locked.`:''}</p><div class="notes">${got.slice().reverse().map(n=>`<div class="note-card"><small>💌 ${n[1]} · ${fmtDay(st.notes[n[0]])}</small><p>${n[3]}</p><p><b>Jack</b></p></div>`).join('')}</div>`}
function checkRewards(){st.bd=st.bd||{};st.notes=st.notes||{};const t=today();let changed=false;
  BADGES.forEach(b=>{if(!st.bd[b[0]]&&b[4]()){st.bd[b[0]]=t;changed=true;celebrate({icon:b[1],kicker:'Badge earned',title:b[2],text:b[3]+'.',btn:'Nice'})}});
  NOTES.forEach(n=>{if(!st.notes[n[0]]&&n[2]()){st.notes[n[0]]=t;changed=true;celebrate({icon:'💌',kicker:'A note from Jack',title:n[1],text:`<span class="letter">${n[3]}<br><br><b>Jack</b></span>`,btn:'Love it'})}});
  if(changed){save();if(current==='me')profile()}}
(function comeback(){const last=st.days.length?st.days.slice().sort().pop():null;if(last&&dd(last,today())>=3)st.cbNow=1})();

/* score chart: practice test scores over time against the goal line */
function chartSVG(h,goal){const W=420,H=190,L=34,R=14,T=14,B=26,s=h.map(x=>x.s),lo=Math.max(50,Math.floor((Math.min(...s,goal)-8)/10)*10),hi=Math.min(150,Math.ceil((Math.max(...s,goal)+8)/10)*10),
  X=i=>L+(s.length<2?(W-L-R)/2:i*(W-L-R)/(s.length-1)),Y=v=>T+(hi-v)/(hi-lo)*(H-T-B);let g='';
  for(let v=lo;v<=hi;v+=10)g+=`<line class="gl" x1="${L}" x2="${W-R}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${L-6}" y="${Y(v)+4}" text-anchor="end">${v}</text>`;
  g+=`<line class="goal" x1="${L}" x2="${W-R}" y1="${Y(goal)}" y2="${Y(goal)}"/><text class="gt" x="${W-R}" y="${Y(goal)-6}" text-anchor="end">Goal ${goal}</text>`;
  if(s.length>1)g+=`<polyline class="ln" points="${s.map((v,i)=>X(i)+','+Y(v)).join(' ')}"/>`;
  s.forEach((v,i)=>{g+=`<circle class="pt" cx="${X(i)}" cy="${Y(v)}" r="5"/>`;if(i===s.length-1||s.length<=8)g+=`<text class="vt" x="${X(i)}" y="${Y(v)-10}" text-anchor="middle">${v}</text>`});
  g+=`<text x="${L}" y="${H-6}">Test 1</text><text x="${W-R}" y="${H-6}" text-anchor="end">Test ${s.length}</text>`;
  return`<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Practice test scores: ${s.join(', ')}. Goal ${goal}.">${g}</svg>`}

/* mistake notebook: a missed problem type comes back with new numbers until it is right on two different days */
st.nb=st.nb||[];
function nbAdd(k,lv,gi){if(gi==null||gi<0||!G[k]||!G[k][gi])return;const x=st.nb.find(y=>y.k===k&&y.gi===gi);if(x)x.ok=[];else{st.nb.push({k,lv,gi,d:today(),ok:[]});if(st.nb.length>60)st.nb.shift()}save()}
function nbHit(x,clean){if(!clean){x.ok=[];save();return' It stays in the notebook for another try.'}const t=today();if(!x.ok.includes(t))x.ok.push(t);
  if(x.ok.length>=2){st.nb=st.nb.filter(y=>y!==x);st.nbCleared=(st.nbCleared||0)+1;save();return' <b>Out of the notebook for good.</b>'}save();return' Get this kind right again on another day and it leaves the notebook.'}
let nbRun=null;const NA=$('nb-area');
function nbIntro(){nbRun=null;const n=st.nb.length,by={};st.nb.forEach(x=>by[x.k]=(by[x.k]||0)+1);
  NA.innerHTML=!n?`<div class="today"><h3>${st.nbCleared?'Notebook clear':'Nothing here yet'}</h3><p>${st.nbCleared?`You have fixed ${st.nbCleared} ${st.nbCleared===1?'problem':'problems'} for good. Anything you miss from now on shows up here.`:'Problems you miss in lessons, sessions and practice tests will show up here for a redo.'}</p></div>`
   :`<div class="today"><h3>${n} ${n===1?'problem':'problems'} to redo</h3><p>Each comes back with new numbers. Get it right with no hints on two different days and it is gone.${st.nbCleared?` You have cleared ${st.nbCleared} so far.`:''}</p><div class="tbl"><table><tr><th>Lesson</th><th>To redo</th></tr>${Object.keys(by).map(k=>`<tr><td><a href="#t-${k}" data-k="${k}">Lesson ${NUM[k]}: ${NAME[k]}</a></td><td class="m">${by[k]}</td></tr>`).join('')}</table></div><div class="row l"><button class="btn" id="nb-go">Redo ${Math.min(n,10)} now</button></div></div>`;
  const b=$('nb-go');if(b)b.onclick=nbStart}
function nbStart(){const t=today(),q=shuffle(st.nb.filter(x=>!x.ok.includes(t))).slice(0,10);if(!q.length){NA.innerHTML=`<div class="today"><h3>Done for today</h3><p>Everything left in the notebook was already right today. Come back tomorrow to finish them off.</p></div>`;return}
  nbRun=1;NA.innerHTML='<div id="nb-pr"></div>';
  mount($('nb-pr'),{id:'nb',nb:1,title:'Mistake notebook',score:c=>`Problem ${c} of ${q.length}`,last:c=>c>=q.length,
    next:({count})=>{if(count>=q.length)return null;const x=q[count];return{key:x.k,lv:x.lv,gi:x.gi,nbx:x,p:G[x.k][x.gi][1](),review:true,tag:`From Lesson ${NUM[x.k]}, ${NAME[x.k]}.`}},
    done:()=>{nbRun=null;confetti();nbIntro();paint();checkRewards()}})}

/* speed round: 60 seconds of quick mental math */
const SPD=[
 ()=>{const a=R(3,12),b=R(3,12);return[`${a} × ${b}`,a*b]},
 ()=>{const a=R(3,12),b=R(3,12);return[`${a*b} ÷ ${a}`,b]},
 ()=>{const a=R(2,15),b=R(2,15);return[`−${a} + ${b}`,b-a]},
 ()=>{const a=R(2,12),b=R(2,12);return[`${a} − (−${b})`,a+b]},
 ()=>{const a=R(2,9),b=R(2,9);return[`(−${a}) × ${b}`,-a*b]},
 ()=>{const a=R(2,9),b=R(2,9);return[`(−${a})(−${b})`,a*b]},
 ()=>{const p=pick([10,20,25,50,75]),n=pick([20,40,60,80,100,200]);return[`${p}% of ${n}`,p*n/100]},
 ()=>{const[a,b]=pick([[1,2],[1,3],[2,3],[1,4],[3,4],[1,5],[2,5]]),n=b*R(2,9);return[`${a}/${b} of ${n}`,a*n/b]},
 ()=>{const n=R(2,15);return[`${n}²`,n*n]},
 ()=>{const n=R(2,13);return[`√${n*n}`,n]},
 ()=>{const n=R(2,6);return[`2${sup(n)}`,2**n]},
 ()=>{const a=R(2,9),b=R(2,5),c=R(2,5);return[`${a} + ${b} × ${c}`,a+b*c]},
 ()=>{const x=R(-9,12),a=R(2,15);return[`x + ${a} = ${x+a}, so x =`,x]},
 ()=>{const x=R(-9,9)||3,a=R(2,9);return[`${a}x = ${a*x}, so x =`,x]},
 ()=>{const[f,d]=pick([['1/2',.5],['1/4',.25],['3/4',.75],['1/5',.2],['2/5',.4],['1/10',.1],['3/5',.6]]);return[`${f} as a decimal`,d]}];
let spRun=null;const SA=$('sp-area');
function spIntro(){spRun=null;const h=st.spHist||[];
  SA.innerHTML=`<div class="today"><h3>${st.spBest?'Best so far: '+st.spBest:'Ready?'}</h3><p>Answer as many as you can in 60 seconds. Type the answer and press Enter. A miss just moves you on to the next one. Every right answer is worth 2 XP.</p>${h.length?`<p class="tagline">Recent rounds: ${h.slice(-8).join(' → ')}</p>`:''}<div class="row l"><button class="btn" id="sp-go">Start 60 seconds</button></div></div>`;
  $('sp-go').onclick=spStart}
function spStart(){let score=0,left=60,cur,miss=0;spRun=1;
  SA.innerHTML=`<div class="pr"><div class="pr-head"><h3>Speed round</h3><span class="pr-score" id="sp-sc">0 right</span></div><div class="timer" id="sp-t">60</div><div class="spq" id="sp-q"></div><div class="pr-in"><input id="sp-in" type="text" inputmode="decimal" autocomplete="off" aria-label="Your answer" placeholder="Answer"><button class="key" data-a="neg" aria-label="Make negative">±</button><button class="btn" id="sp-ok">Enter</button></div><p class="fb" id="sp-fb" hidden></p></div>`;
  const inp=$('sp-in'),qEl=$('sp-q');
  function nextQ(){cur=pick(SPD)();qEl.innerHTML=`<span class="m">${cur[0]}</span>`;pretty(qEl);inp.value='';inp.focus()}
  function check(){if(!spRun||!inp.value.trim())return;const v=parseNum(inp.value),fb=$('sp-fb');
    if(!isNaN(v)&&same(v,cur[1])){score++;$('sp-sc').textContent=score+' right';fb.hidden=true}else{miss++;fb.hidden=false;fb.className='fb no';fb.textContent=`${cur[0].replace(/, so x =$/,'')}: the answer was ${fmtN(cur[1])}`;anim(qEl,'shake')}nextQ()}
  $('sp-ok').onclick=check;inp.addEventListener('keydown',e=>{if(e.key==='Enter')check()});
  SA.querySelector('[data-a=neg]').onclick=()=>{inp.value=/^[-−]/.test(inp.value)?inp.value.slice(1):'-'+inp.value;inp.focus()};
  nextQ();const tm=setInterval(()=>{if(current!=='speed'){clearInterval(tm);spRun=null;return}left--;const t=$('sp-t');t.textContent=left;t.classList.toggle('low',left<=10);if(left<=0){clearInterval(tm);spEnd(score,miss)}},1000)}
function spEnd(score,miss){spRun=null;const pb=st.spBest||0;st.spHist=[...(st.spHist||[]),score].slice(-20);if(score>pb)st.spBest=score;if(score)markDay();save();if(score)addXP(score*2);if(score>pb&&pb)confetti();
  SA.innerHTML=`<div class="today in"><h3>${score} right${score>pb&&pb?' · new best!':''}</h3><p>${score>pb&&pb?`That beats your old best of ${pb}.`:pb&&score<pb?`Your best is ${pb}. Speed comes from doing a round most days.`:'A round most days makes the basics automatic.'}${miss?` ${miss} missed, and those are worth slowing down for next time.`:''}</p><div class="row l"><button class="btn" id="sp-go">Go again</button><a class="btn ghost" href="#t-home" data-k="home">Home</a></div></div>`;
  $('sp-go').onclick=spStart;checkRewards()}

/* cloud save: progress kept under a private code, merged across devices */
var cloudSoon=null;
(function cloud(){const API='https://uyipfjvehybciqmkrjwc.supabase.co/rest/v1/rpc/',KEY='sb_publishable_AFlm53vsZixo915A_jopzw_PFlephpL',CS='pertSync';
  let c=null;try{c=JSON.parse(localStorage.getItem(CS))}catch(e){}
  const m=/[#&]sync=([A-Za-z0-9-]{12,64})/.exec(location.hash);
  if(m){if(!c||c.code!==m[1])c={code:m[1],ver:0};try{history.replaceState(null,'',location.pathname+location.search)}catch(e){}}
  if(!c){const a='abcdefghjkmnpqrstuvwxyz23456789';let r='';for(let i=0;i<10;i++)r+=a[Math.floor(Math.random()*a.length)];c={code:'pert-'+r,ver:0}}
  const keep=()=>{try{localStorage.setItem(CS,JSON.stringify(c))}catch(e){}};keep();
  let timer=null,busy=false,again=false,last=null,fail=false;
  async function rpc(fn,body){const r=await fetch(API+fn,{method:'POST',headers:{apikey:KEY,'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw new Error(r.status);return r.json()}
  function adopt(remote){const before=JSON.stringify(st);Object.assign(st,mergeSt(st,remote));try{localStorage.setItem(LS,JSON.stringify(st))}catch(e){}return before!==JSON.stringify(st)}
  async function push(){if(busy){again=true;return}busy=true;
    try{for(let i=0;i<3;i++){const r=await rpc('pert_save',{p_code:c.code,p_state:st,p_version:c.ver});if(r.ok){c.ver=r.version;keep();break}c.ver=r.version;keep();if(r.state&&adopt(r.state))refresh()}last=Date.now();fail=false}catch(e){fail=true}
    busy=false;paintSync();if(again){again=false;push()}}
  async function pull(){try{const r=await rpc('pert_get',{p_code:c.code});if(r&&r.state){c.ver=r.version;keep();if(adopt(r.state))refresh()}last=Date.now();fail=false;push()}catch(e){fail=true}paintSync()}
  function refresh(){paint();if(current==='me')profile();if(current==='test'&&!run)menu();if(current==='nb'&&!nbRun)nbIntro()}
  cloudSoon=()=>{clearTimeout(timer);timer=setTimeout(push,3000)};
  window.syncInfo=()=>({code:c.code,last,fail,link:location.origin+location.pathname+'#sync='+c.code});
  window.syncUse=code=>{code=String(code).trim().replace(/^.*#sync=/,'');if(!/^[A-Za-z0-9-]{12,64}$/.test(code))return false;c={code,ver:0};keep();pull();return true};
  pull();document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')pull();else if(timer){clearTimeout(timer);push()}});addEventListener('online',pull)})();
function mergeSt(a,b){const N=(a.saved||0)>=(b.saved||0)?a:b,o=Object.assign({},b,a);
  ['xp','solved','lvlSeen','nbCleared','spBest','owl','early'].forEach(k=>{o[k]=Math.max(+a[k]||0,+b[k]||0)});
  o.days=[...new Set([...(a.days||[]),...(b.days||[])])].sort().slice(-400);
  ['time','goal','met','ex','chk','bd','notes'].forEach(k=>{const r=Object.assign({},b[k]||{});Object.entries(a[k]||{}).forEach(([x,v])=>{r[x]=typeof v==='number'&&typeof r[x]==='number'?Math.max(v,r[x]):(r[x]!=null&&typeof v==='string'&&r[x]<v?r[x]:v)});o[k]=r});
  o.sk=Object.assign({},b.sk||{});Object.entries(a.sk||{}).forEach(([k,s])=>{const r=o.sk[k];o.sk[k]=!r||(s.n+10*s.rv)>=(r.n+10*r.rv)?s:r});
  const seen=new Set();o.pert=[...(b.pert||[]),...(a.pert||[])].filter(x=>{const id=x.t||x.d+'|'+x.s+'|'+x.r;if(seen.has(id))return false;seen.add(id);return true}).sort((x,y)=>(x.t||0)-(y.t||0)).slice(-20);
  ['nb','test','target','vol','start','spHist','cbNow'].forEach(k=>{if(N[k]!==undefined)o[k]=N[k]});
  o.saved=Math.max(a.saved||0,b.saved||0);return o}
function syncHTML(){const i=window.syncInfo?syncInfo():null;if(!i)return'';
  return`<p>Your progress saves to the cloud by itself, so it is safe even if this browser gets cleared. <span class="tagline" id="sync-st">${i.fail?'Offline right now. It will catch up when you are back online.':i.last?'Up to date.':'Connecting…'}</span></p>
   <p><b>Use it on another device too.</b> Open this link on your phone or another computer and the same progress follows you there:</p>
   <input id="sync-link" readonly value="${i.link}" aria-label="Your personal link"><div class="row l"><button class="btn ghost sm" id="sync-copy">Copy my link</button></div>
   <p class="tagline">Keep this link to yourself. Anyone who has it can see and change your progress.</p>`}
function paintSync(){const e=$('sync-st');if(!e)return;const i=syncInfo();e.textContent=i.fail?'Offline right now. It will catch up when you are back online.':'Up to date.'}
document.addEventListener('click',e=>{if(e.target.id==='sync-copy'){const v=$('sync-link');v.select();try{navigator.clipboard.writeText(v.value)}catch(x){document.execCommand('copy')}e.target.textContent='Copied'}});
setTimeout(checkRewards,1500);
'''
rep("show((location.hash||'#home').slice(1).replace(/^t-/,''));", FEATURES + "show((location.hash||'#home').slice(1).replace(/^t-/,''));")

p.write_text(s, encoding='utf-8')
print('patched', len(s))
