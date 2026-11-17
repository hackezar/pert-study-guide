# Bailey's PERT Study Guide

Single-page PERT math study guide for Bailey (Jack's girlfriend). Converted on 2026-11-17 from the
Accuplacer guide that was a claude.ai artifact ("Bailey's Study Guide", https://claude.ai/artifact/UBcvVMAbj2LhcCGAmzBXxW).

- Hosting: planned for GitHub Pages at https://hackezar.github.io/pert-study-guide/ (repo hackezar/pert-study-guide,
  serve from `main`). NOT published yet as of 2026-11-17, waiting on Jack's OK for a public repo.
  Once live: push to `main` = update. Bailey's copy updates on her next online visit (sw.js is network-first).
- `index.html` holds everything: lessons, question generators `G.*`, practice engine, profile, lo-fi music.
- `launcher/Bailey PERT Study Guide.html` is the file Jack sends Bailey. It redirects to the live site and hands over
  her old progress from the `bsg3` localStorage key via `#import=` (used only if the site has no progress yet).
  If the hosting URL changes, update `U` in the launcher and resend it.
- PERT practice test: adaptive, 25 questions, estimate = 100 + 16·θ clamped to 50-150. The `DIFF` table gives each
  lesson level a difficulty. Simulated students land within about ±8 of their true score.
- Florida cut scores used: 114 college-ready (MAT 1033), 123 College Algebra (MAC 1105). Colleges vary.
- `tools/convert.py` is a record of the one-time conversion (needs the gitignored original). Edit `index.html` directly now.
