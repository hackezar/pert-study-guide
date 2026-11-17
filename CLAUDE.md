# Bailey's PERT Study Guide

Single-page PERT math study guide for Bailey (Jack's girlfriend; math section only). Converted on 2026-11-17 from
the Accuplacer guide that was a claude.ai artifact ("Bailey's Study Guide", https://claude.ai/artifact/UBcvVMAbj2LhcCGAmzBXxW).

- Live: https://hackezar.github.io/pert-study-guide/ (GitHub Pages from `main`, public repo hackezar/pert-study-guide,
  noindex). Push to `main` = update; Pages takes about a minute. sw.js is network-first, so she gets updates on her
  next online visit. Bump the cache name in sw.js when adding new files.
- Bailey's personal link is the site URL plus `#sync=<her code>`. The code is private: keep it out of this public
  repo (it's in Claude's memory file bailey-pert-guide.md). The page remembers the code after the first visit.
- Cloud save: Supabase project uyipfjvehybciqmkrjwc (same one Two Tides uses), schema `pertguide.progress`, reached
  only through RPCs `pert_get(code)` and `pert_save(code,state,version)` (version check, conflict returns server
  copy). The page merges both copies with `mergeSt` (counters take max, lists union, notebook union with `nbGone`
  tombstones, settings by `setAt`). Test codes `pert-smoketest-*` get deleted after tests.
- `index.html` holds everything: lessons, question generators `G.*`, practice engine, adaptive PERT practice test
  (`DIFF`, `est`, score = 100 + 16·θ clamped 50-150), notebook, speed round, badges `BADGES`, notes from Jack
  `NOTES` (written by Claude in Jack's voice; Jack may want to edit them), cloud sync, lo-fi music.
- Florida cut scores used: 114 college-ready (MAT 1033), 123 College Algebra (MAC 1105). Colleges vary.
- Tests: `python tools/smoke.py` (43 end-to-end checks in headless Chrome, cloud disabled) and
  `python tools/shots.py OUTDIR` (light/dark screenshots). Headless screenshots freeze requestAnimationFrame, so
  the dial count-up shows its first frame there; smoke.py checks the real value.
- `tools/convert.py`, `add_features.py`, `flair.py` are one-time patch records; edit `index.html` directly now.
