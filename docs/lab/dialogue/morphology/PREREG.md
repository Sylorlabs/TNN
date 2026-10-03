# Morphology Crew — Preregistration (FROZEN 2026-09-21)

## Background
The dialogue trial (commit `9263c90ec78d`, baseline 369/370 = 99.7%) had exactly
one miss: **WE-09** turn 1.

- **Query:** `i'm curious about the birth year of the guy who wrote the martian`
- **Expected:** `Andy Weir was born in 1972.`
- **Got:** `Andy Weir wrote The Martian.`
- **Documented root cause:** the keyword core cannot bridge "birth year" → "born".

## Hypotheses under test
- **H1 (morphology gap):** the miss is caused (at least in part) at the
  keyword-extraction/matching stage: `stem_inplace` (frozen suffix-stripper)
  maps "birth"→"birth" and "born"→"born", so the BORN fact scores zero
  keyword overlap with the query.
- **H2 (scoring gap):** even with the bridge, Jaccard may still prefer the
  WROTE fact (2 overlaps: wrote, martian) over the BORN fact (1 overlap:
  birth→born), because the relative clause identifying the referent
  outscores the question focus. The fix must be validated empirically,
  not assumed.
- **H3 (boundary):** the keyword core has a mappable boundary of bridged vs
  unbridged morphological variation (regular suffixes yes; irregular /
  suppletive forms no). The morphology battery maps it.

## Method
1. **Reproduce** WE-09 with a byte-exact Python mirror of the keyword
   pipeline (tokenize → stopwords → `stem_inplace` → keyword sets →
   cross-multiplied Jaccard over all KB facts). Pin the stage of the miss.
2. **Characterize** with a morphology battery: tense variation (run/ran,
   teach/taught, write/wrote/written), noun/verb pairs (birth/born,
   height/high, depth/deep), compounds (birth year, phone number), regular
   forms the stemmer already handles (control). Map bridged vs unbridged.
3. **Fix:** minimal deterministic repair, applied symmetrically at index
   time and query time (both flow through `proc_token` → `stem_inplace`).
   Candidate: irregular-form normalization table inside/after `stem_inplace`.
   If H2 is confirmed (bridge alone insufficient), the minimal scoring-side
   repair is in scope, but it must not change any passing turn's outcome.
4. **Validate:** rebuild `dialogue.zag`, run the FULL dialogue battery
   (`battery.txt`, 370 turns) 5× byte-identical; run the morphology battery.

## Kill bars (frozen)
- **KB-M1 (reproduction):** the Python mirror must reproduce the exact
  observed answer (`Andy Weir wrote The Martian.`) via the documented
  stage, or the mechanism claim is withdrawn.
- **KB-M2 (morphology battery):** ≥95% of morphology probes pass post-fix.
- **KB-M3 (no regressions):** full dialogue battery must score ≥369/370
  post-fix AND WE-09 turn 1 must pass (WEIRD 30/30). Any previously-passing
  turn that newly fails = fix REJECTED; fall back to a narrower repair.
- **KB-M4 (determinism):** 5/5 runs byte-identical (digest match).
- **KB-M5 (symmetry):** the repair must apply identically to KB-install and
  query paths (single code path, no dual dictionaries that can drift).

## What is NOT in scope
- Changing the Jaccard scorer's formula, the gazetteer, or answer templates
  beyond what is needed for KB-M3 (any such change must be justified as
  the minimal repair for WE-09).
- External libraries, statistical models, or non-determinism. Pure Zag.

## Deliverables
- `REPRO.md` — exact mechanism of the WE-09 miss (stage-pinned).
- `MORPH_BATTERY.md` + `morph_battery.txt` — characterization battery.
- `FIX.md` — the repair, with before/after mechanism description.
- `VERDICT.md` — post-fix numbers vs kill bars.
- Patched `dialogue.zag` (in the parent `dialogue/` workdir) + 5 run logs.
- Addendum to `docs/lab/dialogue/VERDICT.md` noting WE-09's resolution.
