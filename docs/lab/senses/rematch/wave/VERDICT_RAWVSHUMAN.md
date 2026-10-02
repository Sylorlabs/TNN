# RAW-VS-HUMAN TEST Wave — Final Verdict Report

**Date:** 2026-09-22  
**Prereg:** `WAVE_RAWVSHUMAN_PREREG.md` (commit `a87ddfd4c41f88710f5e573e9c0283d003360b6d`)  
**Rematch baseline:** commit `1c01a1adcf8dcec824b77f11e83a9c3fe91c2634` (A frozen, not rerun)

## D1 Diagnostic

| Modality | D1 | Gate |
|----------|----|------|
| colordisc | 99.8% (505/506) | PASS |
| pitchdisc | 99.2% (131/132) | PASS |

Scope: color + pitch. See `D1_REPORT.md`.

## Fork B2 — Vocabulary Growth

### Growth (pure-Zag GROW, deterministic)

| Budget | Color cuts | Pitch cuts |
|--------|-----------|------------|
| TRAIN_T1 (n=60/60) | 4: bins 0→400, 1→600, 3→400, 11→800 | 5: bins 12→800, 18→400, 20→200, 23→400, 24→400 |
| TRAIN_T2 (n=600/600) | 0 (no cut cleared 10‰) | 2: bins 25→200, 31→200 |

Grown tables: `b2/grown_T1.zag`, `b2/grown_T2.zag` (SHA-256 below).

### TRAIN fit (k)

| Budget | colordisc | pitchdisc |
|--------|-----------|-----------|
| T1 | k=0, 36/60 | k=0, 54/60 |
| T2 | k=0, 94/600 | k=0, 480/600 |

### TEST-FRESH (seed 20260923)

| Budget | colordisc | colorconst | pitchdisc |
|--------|-----------|------------|-----------|
| B2-T1 | 34/60 = 56.7% | 27/40 = 67.5% | 51/60 = 85.0% |
| B2-T2 | 33/60 = 55.0% | 27/40 = 67.5% | 51/60 = 85.0% |
| Frozen B-T1 | 33/60 = 55.0% | 27/40 = 67.5% | 51/60 = 85.0% |
| Frozen B-T2 | 33/60 = 55.0% | 27/40 = 67.5% | 51/60 = 85.0% |

### Overall (6-task mean; unchanged tasks from frozen B per VERDICT.md)

| | colordisc | colorconst | shapetrans | pitchdisc | timbredisc | motiondir | **Overall** |
|---|---|---|---|---|---|---|---|
| A | 76.7 | 92.5 | 100.0 | 100.0 | 100.0 | 33.3 | **83.8** |
| Frozen B-T1 | 55.0 | 67.5 | 36.7 | 85.0 | 75.0 | 16.7 | **56.0** |
| Frozen B-T2 | 55.0 | 67.5 | 36.7 | 85.0 | 75.0 | 18.3 | **56.2** |
| **B2-T1** | 56.7 | 67.5 | 36.7 | 85.0 | 75.0 | 16.7 | **56.3** |
| **B2-T2** | 55.0 | 67.5 | 36.7 | 85.0 | 75.0 | 18.3 | **56.2** |

### B2 verdicts

- **ALIVE bar:** overall B2−A ≥ +2pp AND B2 ≥60%.
  - T1: 56.3−83.8 = −27.5pp; 56.3 < 60. **DEAD.**
  - T2: 56.2−83.8 = −27.6pp; 56.2 < 60. **DEAD.**
- **Mechanism diagnostic:** overall B2 must beat frozen B by ≥3pp.
  - T1: 56.3−56.0 = +0.3pp. **FAIL.**
  - T2: 56.2−56.2 = +0.0pp. **FAIL.**

## Fork B3 — Fuzzy Membership

### Margin fit (TRAIN; m ∈ {0,100,200,300,500}, tie → smallest m)

| Budget | colordisc | colorconst | pitchdisc |
|--------|-----------|------------|-----------|
| T1 | m=100, 34/60, k=0 | m=0, 35/40, k=0 | m=0, 48/60, k=0 |
| T2 | m=100, 118/600, k=0 | m=0, 298/400, k=0 | m=0, 468/600, k=0 |

m=0 validated byte-for-byte vs frozen B on all 400 round-1 fixtures
(percepts + dists) before any margin was fitted.

### TEST-FRESH

| | colordisc | colorconst | pitchdisc | **Overall** |
|---|---|---|---|---|
| **B3-T1** | 34/60 = 56.7% | 27/40 = 67.5% | 51/60 = 85.0% | **56.3** |
| **B3-T2** | 34/60 = 56.7% | 27/40 = 67.5% | 51/60 = 85.0% | **56.5** |

(Unchanged tasks from frozen B as above.)

### B3 verdicts

- **ALIVE bar:** overall B3−A ≥ +2pp AND B3 ≥60%.
  - T1: 56.3 < 60. **DEAD.**
  - T2: 56.5 < 60. **DEAD.**
- **Mechanism diagnostic:** mean(colordisc, colorconst) must beat frozen B by ≥3pp.
  - T1: (56.7+67.5)/2=62.1 vs (55.0+67.5)/2=61.25 → +0.85pp. **FAIL.**
  - T2: 62.1 vs 61.25 → +0.85pp. **FAIL.**

## Vocabulary sizes

| | Color handles | Pitch handles |
|---|---|---|
| Frozen B | 77 (72 chromatic + 5 achromatic) | 48 |
| B2 | 77 (splits refine distances; no new handle IDs) | 48 |
| B3 | 77 (fuzzy weights; no new handle IDs) | 48 |

Grown cut specifications: B2-T1: 4 color + 5 pitch; B2-T2: 0 color + 2 pitch.

## Ops (TEST-FRESH totals)

| Fork | colordisc (60) | colorconst (40) | pitchdisc (60) |
|---|---|---|---|
| B2 | 491,520 | 512,000 | 86,118,720 |
| B3 | 491,520 | 512,000 | 86,118,720 |

(Per-fixture: colordisc ~8.2k, colorconst ~12.8k, pitchdisc ~1.44M.)

## Determinism

Full pipeline (EMIT → GROW → table) rerun from deleted caches ×2 (TRAIN_T2):

| Run | grown_T2.zag SHA-256 |
|---|---|
| Original | `92c3c844b06d5156debf9ecdbb644120b8ec72747940db4c63877303a420e9c4` |
| Rerun 1 | `92c3c844b06d5156debf9ecdbb644120b8ec72747940db4c63877303a420e9c4` |
| Rerun 2 | `92c3c844b06d5156debf9ecdbb644120b8ec72747940db4c63877303a420e9c4` |

Byte-identical. TEST-FRESH result digests also identical across reruns.

## Mechanical verdicts

- **B2: DEAD.** Fails the ALIVE bar at both budgets (56.3%/56.2% < 60%,
  −27pp vs A). Fails the mechanism diagnostic (+0.3pp/+0.0pp vs +3pp required).
  Vocabulary growth via lightness cuts does not resolve B's color errors;
  pitch cuts give no TEST-FRESH gain.
- **B3: DEAD.** Fails the ALIVE bar at both budgets (56.3%/56.5% < 60%).
  Fails the mechanism diagnostic (+0.85pp vs +3pp required). Fuzzy membership
  helps colordisc on TRAIN (+24 at T2) but the TEST-FRESH gain is +1 fixture
  (+1.7pp), far below the bar.

No rescue language applies. The preregistered bars decide.

## Notes

- T3 (best-effort): not attempted. T1/T2 verdicts are DEAD; the mechanism
  diagnostics show <1pp gains, so T3 cannot change the outcome within the
  24-hour window given pitch GROW's O(n²) scaling.
- TEST-FRESH (seed 20260923) was not contacted before growth/fitting completed.
- A was not rerun (frozen per prereg).
- All mechanisms are pure Zag; Python orchestrated only (as in the rematch).
- Zero randomness in decision paths; deterministic tie-breaks throughout.
