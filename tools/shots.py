"""Screenshots of the main pages with sample progress, light and dark. Run: python tools/shots.py OUTDIR"""
import pathlib, subprocess, sys, tempfile, json
root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
work = pathlib.Path(tempfile.mkdtemp(prefix='pert-shots-'))
s = (root / 'index.html').read_text(encoding='utf-8')
s = s.replace("const API='https://uyipfjvehybciqmkrjwc", "const API='http://127.0.0.1:9/x")
s = s.replace("const T=$('test-area');let run=null;", "const T=$('test-area');let run=null;window.__R=()=>run;", 1)
seed = {"v": 2, "xp": 540, "solved": 120, "days": ["2026-11-15", "2026-11-16", "2026-11-17"],
        "sk": {"whole": {"n": 5, "rv": 2, "lvl": 3}, "frac": {"n": 5, "rv": 1, "lvl": 2}, "dec": {"n": 3, "rv": 0, "lvl": 2}, "eq": {"n": 2, "rv": 0, "lvl": 2}},
        "pert": [{"d": "2026-11-10", "s": 98, "r": 12, "t": 1}, {"d": "2026-11-13", "s": 105, "r": 14, "t": 2}, {"d": "2026-11-16", "s": 112, "r": 15, "t": 3}],
        "nb": [{"k": "eq", "lv": 2, "gi": 1, "ok": [], "at": 1}, {"k": "frac", "lv": 2, "gi": 3, "ok": [], "at": 2}],
        "target": 114, "test": "2026-12-15", "lvlSeen": 4, "spBest": 17, "early": 1, "owl": 1,
        "bd": {k: "2026-11-15" for k in ["first", "st3", "t1", "up", "prof", "mast", "p100", "early", "owl", "sp15"]},
        "notes": {k: "2026-11-15" for k in ["start", "t1", "up", "prof", "st3", "p100", "half", "num"]}}
pre = '<script>localStorage.setItem("bsg3",' + json.dumps(json.dumps(seed)) + ');localStorage.setItem("pertSync",JSON.stringify({code:"pert-sampledemo1",ver:0}))</script>'
CLEAN = 'document.querySelectorAll(".lvlup").forEach(e=>e.remove());'
SHOTS = {
  'home': '',
  'lesson': 'show("quad",true);',
  'practice': 'show("eq",true);const s=document.getElementById("t-eq");for(let i=0;i<9;i++){const b=s.querySelector(".pager [data-pg=\'1\']:not([hidden])");if(b)b.click()}',
  'question': 'show("test",true);document.querySelector("[data-pt]").click();',
  'results': 'show("test",true);document.querySelector("[data-pt]").click();for(let n=0;n<25;n++){const r=__R(),x=r.qs[r.i],ch=[...document.querySelectorAll("#test-area .choice")];let i=x.p.choices.indexOf(x.p.ans);if(x.b>0.9)i=(i+1)%ch.length;ch[i].click();document.querySelector("[data-q=next]").click()}setTimeout(()=>{document.querySelectorAll(".lvlup").forEach(e=>e.remove());window.scrollTo(0,0)},2000);',
  'walk': 'show("test",true);document.querySelector("[data-pt]").click();document.querySelector("[data-q=show]").click();document.querySelector("[data-q=step]")?.click();document.querySelector("[data-q=step]")?.click();document.querySelector("[data-q=step]")?.click();',
  'profile': 'show("me",true);',
  'notebook': 'show("nb",true);',
  'speed': 'show("speed",true);document.getElementById("sp-go").click();',
  'sheet': 'show("sheet",true);',
  'note': 'celebrate({icon:"💌",kicker:"A note from Jack",title:"Three days in a row",text:`<span class="letter">${NOTES[1][3]}<br><br><b>Jack</b></span>`,btn:"Love it"});',
}
for name, js in SHOTS.items():
    clean = '' if name == 'note' else CLEAN
    page = work / f'{name}.html'
    page.write_text(s.replace('<head>', '<head>' + pre, 1).replace('</body>', f'<script>setTimeout(()=>{{{clean}{js}}},2400)</script></body>'), encoding='utf-8')
    for scheme, flag in (('dark', 0), ('light', 1)):
        if scheme == 'light' and name not in ('home', 'results', 'profile', 'practice', 'walk'):
            continue
        size = '1280,900' if name == 'home' and scheme == 'light' else ('500,3000' if name == 'profile' else '500,1050')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', f'--user-data-dir={work/"p"}', '--hide-scrollbars', f'--window-size={size}',
                        f'--blink-settings=preferredColorScheme={flag}', '--virtual-time-budget=9000', f'--screenshot={out/(name+"-"+scheme+".png")}', page.as_uri()],
                       capture_output=True, timeout=120)
print('\n'.join(sorted(p.name for p in out.glob('*.png'))))
