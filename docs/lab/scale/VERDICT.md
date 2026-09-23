# SCALE-UP verdict — 2026-09-21/22

Micah's order: more categories, long-horizon full runs, LLM-scale amounts.
Prereg: `~/workspace/scale/PREREG.md` (frozen before any scale run).

## The ceiling actually reached

**6,585,360 facts** (24 categories × 274,390 per category) — the corpus maximum
(10 Gutenberg texts, 1,332,368 words total). No kill bar tripped at any scale.
Nothing broke. The ceiling is the corpus, not the learner.

Honest scope: this is millions of facts, not billions of tokens. "LLM amounts"
were not reached and are not claimed.

## Scale laws (P=1, eval mode)

| N (facts) | Clean mastery | All-fact mastery | Flaw 96 | Absorption | ops/fact | B/fact | Reps byte-identical |
|---|---|---|---|---|---|---|---|
| 240 | 226/226 = 1.0000 | 0.9417 | 96/96 | 14/14 | 4.004 | 92 | 5/5 |
| 2,400 | 2286/2286 = 1.0000 | 0.9525 | 96/96 | 114/114 | 4.000 | 92 | 5/5 |
| 24,000 | 22841/22841 = 1.0000 | 0.9517 | 96/96 | 1159/1159 | 4.000 | 92 | 5/5 |
| 240,000 | 227965/227965 = 1.0000 | 0.9499 | 96/96 | 12035/12035 | 4.000 | 92 | 3/3 |
| 999,984 | 950214/950214 = 1.0000 | 0.9502 | 96/96 | 49770/49770 | 4.000 | 92 | 1 |
| 3,000,000 | 2850347/2850347 = 1.0000 | 0.9501 | 96/96 | 149653/149653 | 4.000 | 92 | 1 |
| 6,585,360 | 6256828/6256828 = 1.0000 | 0.9501 | 96/96 | 328532/328532 | 4.000 | 92 | 1 |

- Clean mastery excludes the 5% planted falsehoods (trained on supplied false
  values, recalled as supplied — absorption 1.0 at every scale, championship
  convention). All-fact mastery ≈ 0.95 is the falsehood rate arithmetic, not
  a learning deficit.
- Cost is exactly linear: ops/fact = 4.000 at every N ≥ 2,400 (4.004 at N=240:
  one amortized audit entry). Marginal ≈ 4.2 µs/fact user CPU.
- Memory is exactly 92 B/fact at every N (24 slot + 4 index + 64 audit),
  chunked — no slice over 2^25 at any scale.

## Catastrophic forgetting (KB-FORGET): not observed

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** T3 TRIPWIRE —
> "not observed" rests on KB-FORGET (trip iff last-first decile gap >3pp). The
> measured 0.00pp gap stands, but the bar had infinite slack — it would have
> tolerated ~187,700 forgotten early facts before tripping, so the instrument
> could not have detected forgetting below that scale. Proposed replacement
> T3 (trip iff gap >0.5pp) is pending Micah's signature.

Mastery by training decile, first vs last decile:

| N | d=0 (first 10%) | d=9 (last 10%) | gap |
|---|---|---|---|
| 240 | 1.0 | 1.0 | 0 |
| 2,400 | 1.0 | 1.0 | 0 |
| 24,000 | 1.0 | 1.0 | 0 |
| 240,000 | 1.0 (22841/22841) | 1.0 (22775/22775) | 0 |
| 999,984 | 1.0 (95074/95074) | 1.0 (94999/94999) | 0 |
| 3,000,000 | 1.0 (285028/285028) | 1.0 (285139/285139) | 0 |
| 6,585,360 | 1.0 (625741/625741) | 1.0 (625752/625752) | 0 |

All 10 deciles 1.0 at every completed scale. Retention across passes
(P=1/2/3 at 240 and 2,400; P=1/2 at 24,000): 1.0 every pass.

## Kill bars

| Bar | Result |
|---|---|
| KB-SCALING (>2pp mastery drop) | NOT TRIPPED — 0.00pp drop at every scale |
| KB-FORGET (>3pp horizon gap) | NOT TRIPPED — 0.00pp gap at every scale |
| KB-COST (superlinear ops/fact) | NOT TRIPPED — exactly 4.000/fact throughout |
| KB-DETERMINISM | NOT TRIPPED — byte-identical at every rep count run |
| KB-FLAW (<7/8 slices) | NOT TRIPPED — 96/96 at every scale |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** T2/T3
> TRIPWIRES — KB-SCALING and KB-FORGET are non-informative as written.
> "NOT TRIPPED" with 0.00pp measured against trip thresholds of >2pp / >3pp
> means the bars had infinite slack: KB-SCALING tolerates 125,137 wrong facts
> at N=6,585,360 before tripping; KB-FORGET tolerates ~187,700 forgotten early
> facts. The measurements stand; the bars said almost nothing. Proposed
> replacements T2 (trip iff drop >0.25pp) and T3 (trip iff gap >0.5pp) are
> pending Micah's signature.

## What this means

The standing expectation held: **no degradation over long horizons**, tested to
6.58M facts — 27,000× the championship snippet size. The learner's deliberate
per-fact storage scales linearly in time and memory with zero forgetting and
zero nondeterminism. What broke first: nothing in the learner; the run stopped
at the corpus ceiling (every word position of every text used).

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** two instrument
> qualifications on this section. (a) T2 TRIPWIRE — "no degradation over long
> horizons" rests on KB-SCALING (trip iff mastery drops >2pp below S0). The
> measured 0.00pp stands, but the bar had infinite slack: at N=6,585,360 it
> would have tolerated 125,137 wrong facts before tripping, so the instrument
> could not have detected degradation below ~125k wrong facts — the claim's
> strength is limited by the instrument. Proposed replacement T2 (trip iff
> drop >0.25pp) is pending Micah's signature. (b) T3 TRIPWIRE — "zero
> forgetting" rests on KB-FORGET (trip iff last-first decile gap >3pp). The
> measured 0.00pp gap stands, but the bar tolerated ~187,700 forgotten early
> facts before tripping. Proposed replacement T3 (trip iff gap >0.5pp) is
> pending Micah's signature.

## Caveats

- Procedural Gutenberg-derived integer facts, not prose-mediated learning
  (documented tradeoff in corpus/MANIFEST.json). Falsehoods are numeric
  distractors absorbed 1.0 at every scale — the teacher-quality finding
  (consistent lies absorbed) reproduces at 6.5M facts.
- S4 stretch reps are single runs (determinism established 5/5 at S0–S2, 3/3 at S3).
- The flaw battery is the 96-probe 4-family championship battery, sampled per
  the frozen prereg at large N.
- znc 2^25 slice limit respected via chunking throughout (59 slot + 30 audit
  chunks at 240k; more at larger N — exact counts in run logs).

## Lineage

- Corpus crew: texts + FACTSPEC.md + manifests, `~/workspace/scale/corpus/`
  (SHA256SUMS 34/34 OK; 2000/2000 independent-implementation agreement).
- Driver crew: `scale_learner.zag` (pure Zag, zero RNG), reuses the
  class3-standardized learner core; N=240 validated.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
