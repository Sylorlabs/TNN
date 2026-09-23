# RESULTS — Keyboard-geometry typo inference vs keyboard-blind baseline

Verdict: **PASS**. The keyboard-geometry knowledge beats the keyboard-blind
baseline on top-1 intended-word recovery on all three battery kinds.

## Measured results (frozen battery, N=20,031)

| kind | n | KB top-1 | BL top-1 | Δ (pp) | KB top-3 | BL top-3 |
|---|---|---:|---:|---:|---:|---:|---:|
| S1 (single near-key sub) | 9,398 | **95.02%** | 91.04% | **+3.98** | 99.87% | 99.43% |
| S2 (two adjacent-key subs) | 10,566 | **95.71%** | 71.94% | **+23.77** | 99.91% | 88.29% |
| RW (real-world-style) | 67 | **95.52%** | 92.54% | **+2.99** | 100.00% | 98.51% |
| ALL | 20,031 | **95.39%** | 80.97% | **+14.42** | 99.90% | 93.55% |

Raw counts: KB top-1 19,107 / BL top-1 16,219 (of 20,031).

Kill bar (preregistered): KB top-1 > BL top-1 on EACH of S1, S2, RW —
**met on all three**. The head-to-head isolates exactly the substitution-cost
table (identical DP, identical insertion/deletion/transposition constants,
identical candidate set and tie-breaks), so the gain is the keyboard
geometry, nothing else.

## Where the gain comes from

- **S2 (+23.77pp)** is the big win: with two errors, blind edit distance
  leaves many equidistant candidates and tie-breaks decide; geometry
  disambiguates by physical plausibility.
- **S1 (+3.98pp)**: single-error items are easier for the baseline (fewer
  distance-1 competitors), but geometry still wins.
- **RW (+2.99pp, n=67)**: hand-authored transpositions/doublings/neighbor
  slips — geometry wins on realistic typos too.
- Per-item: geometry improved the rank on **3,553** items and worsened it on
  **281** (12.6:1). The 281 are honest boundary cases where a competing word
  has a cheaper keyboard path (e.g. typed `atter` for `after`); reported, not
  hidden.
- 50 items are "collisions" (the typed string is itself a different list
  word); both methods necessarily miss those, capping achievable top-1 at
  99.75% for both.

## Character-level (diagnostic)

Preregistered metric on S1 (n=9,398): truth-char top-1 **0.00%**, top-3
**43.19%**. The 0% is by construction and was a metric-design weakness in
the prereg: the pressed key itself always ranks first (cost 0 — maybe it
wasn't a typo), so the truth can never be rank 1. The honest reading:
single-key evidence alone cannot beat the null hypothesis "no typo".

Post-hoc supplementary (labeled, not preregistered): excluding the typed key
itself — "given that a typo occurred here, what was the intended letter?" —
top-1 **25.36%**, top-3 **64.00%**. Geometry gives a ranked hypothesis set;
word context resolves the rest (word-level top-1 95%+). This is the intended
use pattern: geometry proposes, context disposes.

## Determinism

`run_battery.zag` executed twice on the frozen `items.txt`
(sha256 c62b4150cd86a9702e3aae6dd4c216ae9af90986272eb0f5a4ec26b38b981ad7):
results byte-identical (`cmp` clean).
Results sha256: d343ab38213d181cd72107dfde83e88bc1928eb82030700ab1e1eb28fa1b94ce.

## Build notes (deviations from prereg, all pre-execution)

1. One bug found and fixed during pre-freeze smoke testing: the truth-index
   search compared the word buffer against item-buffer offsets (would have
   silently mis-ranked); caught by a bounds panic on the 4-item scratch
   battery. Fixed before any frozen-battery execution.
2. Implementation refactor between prereg freeze and battery execution: the
   edit-distance core moved verbatim from `run_battery.zag` into the
   deliberation-facing `typo_infer.zag` (`infer_dist`); the runner now imports
   it. Algorithm unchanged. Proven: the pre-refactor binary and the
   refactored binary produce byte-identical results on the frozen battery
   (runs A and C `cmp` clean), and the 4-item smoke results were identical
   before/after.
3. Prereg-pinned shas verified unchanged at execution: words.txt
   921db28f…, gen_battery.py 42e3a233…, qwerty.zag b9c57a83….

## What this does not claim

- Word plausibility is list membership only; no frequency priors.
- Digits, punctuation, and non-QWERTY layouts are not encoded.
- The 392-word list is small; a production lexicon needs the same trial at
  scale (the inference is O(lexicon) per query — fine, but re-verify).
- Single-character inference is a likelihood ranking, not a verdict.

## Residual boundary

Geometry + word list resolves 95.39% top-1. The remaining misses are
collisions (typed string is a real other word — needs sentence context, not
key geometry) and cheaper-path competitors. Next boundary if wanted:
sentence-context scoring on top of the geometry prior.
