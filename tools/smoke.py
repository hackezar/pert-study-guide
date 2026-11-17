"""Headless end-to-end test of the guide. Run: python tools/smoke.py
Builds a test copy with cloud save pointed at a dead address, drives every page and feature in
headless Chrome, and prints a report. Needs Google Chrome installed in the default location."""
import pathlib, subprocess, re, html, tempfile, shutil, sys, os

root = pathlib.Path(__file__).resolve().parent.parent
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
work = pathlib.Path(tempfile.mkdtemp(prefix='pert-smoke-'))
s = (root / 'index.html').read_text(encoding='utf-8')
s = s.replace("const API='https://uyipfjvehybciqmkrjwc", "const API='http://127.0.0.1:9/x")
s = s.replace("const T=$('test-area');let run=null;", "const T=$('test-area');let run=null;window.__R=()=>run;", 1)
s = s.replace("function mount(el,cfg){let it,", "function mount(el,cfg){el.__it=()=>it;let it,", 1)
pre = '<script>window.__err=[];window.onerror=function(m,u,l){__err.push(m+" @"+l)};addEventListener("unhandledrejection",e=>{if(!/fetch|Failed|NetworkError|status/i.test(String(e.reason)))__err.push("rej "+e.reason)});try{localStorage.clear()}catch(e){}</script>'
DRIVER = r'''<script>
const OUT=[],ok=(c,m)=>OUT.push((c?'PASS ':'FAIL ')+m),C=sel=>{const e=document.querySelector(sel);if(!e)throw new Error('missing '+sel);e.click();return e};
const go=k=>{document.querySelector(`a[data-k="${k}"]`)?C(`a[data-k="${k}"]`):show(k,true)};
const wide=()=>document.documentElement.scrollWidth-document.documentElement.clientWidth;
function answer(pr,right){const it=pr.__it(),p=it.p,inp=pr.querySelector('.pr-in input');
  if(inp){inp.value=right?String(p.show||p.ans).replace('−','-'):'987654';pr.querySelector('[data-a=check]').click()}
  else{const ch=[...pr.querySelectorAll('.choice')],i=p.choices.indexOf(p.ans);(right?ch[i]:ch[(i+1)%ch.length]).click()}}
function closePops(){let n=0;while(document.querySelector('.lvlup button')&&n<40){document.querySelector('.lvlup button').click();n++}return n}
async function main(){try{
  await new Promise(r=>setTimeout(r,400));
  ok(document.querySelectorAll('.card[data-k]').length===14,'home shows 14 lesson cards');
  ok(/Bailey/.test(document.getElementById('greet').textContent),'hero greeting: '+document.getElementById('greet').textContent);
  ok(wide()<=1,'home has no sideways scroll ('+wide()+'px)');
  // every lesson: widgets drawn, paging works, practice reaches Proficient
  const keys=[...document.querySelectorAll('.card[data-k]')].map(c=>c.dataset.k);let pages=0;
  for(const k of keys){go(k);const sec=document.getElementById('t-'+k);
    let n=0;while(sec.querySelector('.pager [data-pg="1"]:not([hidden])')&&n<20){sec.querySelector('.pager [data-pg="1"]').click();n++;pages++}
    sec.querySelectorAll('svg[id]').forEach(v=>ok(v.innerHTML.length>50,`lesson ${k}: picture ${v.id} drawn`));
    sec.querySelectorAll('.ex .exbar [data-x=all]').forEach(b=>b.click());
    const pr=sec.querySelector('[data-practice]');pr.querySelector('[data-lv="2"]').click();
    for(let i=0;i<6;i++){answer(pr,true);const nb=pr.querySelector('[data-a=new]');nb.click()}
    closePops();ok(wide()<=1,`lesson ${k}: no sideways scroll`);
  }
  const st=()=>JSON.parse(localStorage.getItem('bsg3'));
  const prof=keys.filter(k=>(st().sk[k]||{}).n>=5).length;ok(prof===14,'all 14 lessons reach Proficient by answering ('+prof+')');
  ok(pages>20,'lesson paging clicked through '+pages+' parts');
  // wrong answers go to the notebook
  go('eq');const pe=document.querySelector('#t-eq [data-practice]');for(let i=0;i<3;i++){answer(pe,false);pe.querySelector('[data-a=new]').click()}
  ok(st().nb.length>=3,'missed problems land in the notebook ('+st().nb.length+')');
  // today's session
  go('today');C('#go-today');let tp=document.getElementById('today-pr');for(let i=0;i<8;i++){answer(tp,true);tp.querySelector('[data-a=new]').click()}
  ok(/Done for today/.test(document.getElementById('today-area').textContent),"today's 8-problem session finishes");closePops();
  // notebook session
  go('nb');C('#nb-go');const np=document.getElementById('nb-pr');let c=0;while(np.isConnected&&np.__it()&&c<10){answer(np,true);np.querySelector('[data-a=new]').click();c++}
  ok(c>0&&st().nb.every(x=>x.ok.length===1),'notebook redo marks each one right today ('+c+' done)');closePops();
  // starting checks
  go('test');for(const g of ['B','P']){C(`[data-c="${g}"]`);let q=0;while(document.querySelector('#test-area [data-q=next]')&&q<40){document.querySelector('#test-area .choice').click();C('[data-q=next]');q++}
    ok(/starting points/.test(document.getElementById('test-area').textContent),'starting check '+g+' finishes');C('[data-q=quit]')}
  // two practice tests
  for(const cut of [0.3,1.4]){C('[data-pt]');for(let n=0;n<25;n++){const r=__R(),x=r.qs[r.i],ch=[...document.querySelectorAll('#test-area .choice')];let i=x.p.choices.indexOf(x.p.ans);if(x.b>cut)i=(i+1)%ch.length;ch[i].click();C('[data-q=next]')}
    const d=document.querySelector('#test-area svg.dial');ok(!!d,'practice test shows the score dial');
    await new Promise(r=>setTimeout(r,1700));ok(document.getElementById('dial-n').textContent==String(st().pert.slice(-1)[0].s),'dial counts up to the saved score '+document.getElementById('dial-n').textContent);
    closePops();C('[data-q=quit]')}
  ok(!!document.querySelector('#test-area svg.chart'),'score chart on the practice test page');
  // speed round, full minute
  go('speed');C('#sp-go');let sp=0;const tm=setInterval(()=>{const i=document.getElementById('sp-in');if(!i)return;const q=document.getElementById('sp-q').textContent;i.value='1';C('#sp-ok');sp++},500);
  await new Promise(r=>setTimeout(r,62000));clearInterval(tm);
  ok(/right/.test(document.getElementById('sp-area').textContent)&&!!document.getElementById('sp-go'),'speed round ends after 60 seconds ('+sp+' answers typed)');closePops();
  go('sheet');ok(document.querySelectorAll('#t-sheet .sheet section').length===15,'formula sheet has 15 boxes');
  go('day');ok(/30 multiple-choice/.test(document.getElementById('t-day').textContent),'test day guide is the PERT version');
  // profile
  closePops();go('me');const me=document.getElementById('me-area');
  ok(me.querySelectorAll('.badge:not(.off)').length>=6,'badges earned: '+me.querySelectorAll('.badge:not(.off)').length);
  ok(me.querySelectorAll('.note-card').length>=4,'notes from Jack unlocked: '+me.querySelectorAll('.note-card').length);
  ok(!!document.getElementById('sync-link'),'cloud save box shows a personal link');
  const sel=document.getElementById('me-goal');sel.value='123';sel.dispatchEvent(new Event('change'));ok(st().target===123,'goal score can be changed to 123');
  const dt=document.getElementById('me-date');dt.value='2026-12-20';dt.dispatchEvent(new Event('change'));ok(st().test==='2026-12-20','test date can be changed');
  // jump menu reaches every page
  const opts=[...document.getElementById('jump').options].map(o=>o.value);let bad=[];for(const v of opts){show(v,true);if(document.getElementById('t-'+v).hidden)bad.push(v)}ok(!bad.length,'jump menu opens all '+opts.length+' pages '+bad);
  // tab bar
  ok(document.querySelectorAll('#tabbar a').length===5,'tab bar has 5 tabs');
  OUT.push('INFO xp '+st().xp+', solved '+st().solved);
}catch(e){OUT.push('FAIL driver: '+e.message+' '+(e.stack||'').split('\n')[1])}
OUT.push((__err.length?'FAIL':'PASS')+' page errors: '+JSON.stringify(__err));
const p=document.createElement('pre');p.id='RESULT';p.textContent=OUT.join('\n');document.body.appendChild(p)}
setTimeout(main,300);
</script>'''
page = work / 'smoke.html'
page.write_text(s.replace('<head>', '<head>' + pre, 1).replace('</body>', DRIVER + '</body>'), encoding='utf-8')
r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', f'--user-data-dir={work/"prof"}', '--window-size=500,1000',
                    '--virtual-time-budget=120000', '--dump-dom', page.as_uri()], capture_output=True, timeout=300)
out = r.stdout.decode('utf-8', 'replace')
m = re.search(r'<pre id="RESULT">(.*?)</pre>', out, re.S)
report = html.unescape(m.group(1)) if m else 'NO RESULT (page hung or crashed)'
sys.stdout.reconfigure(encoding='utf-8')
print(report)
print('\nSUMMARY', report.count('PASS'), 'pass', report.count('FAIL'), 'fail')
shutil.rmtree(work, ignore_errors=True)
