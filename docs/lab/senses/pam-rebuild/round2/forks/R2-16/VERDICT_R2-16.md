# VERDICT_R2-16.md — FINAL

## Fork ID
R2-16 (FS-A-REDESIGNED)

## Status
**DEAD** — Multiple prereg bars fail. Recall 77.6% (<80%) is independently fatal.

## Prereg
- Frozen: `4601db7f3182181f525c5791339207243727caa2` (2026-09-23, verified via GitHub API)
- This completion: all previously-unmeasured components now measured.

## Mechanism (frozen; untouched by completion crew)
Pure Zag (`src/r216.zag`), six task formation+challenge pairs, INSTALL iff
challenge outcome == formation claim. Python only for glue (drivers, scorers,
fixture generators). Zero RNG in decision paths.

## Measured bars (prereg §5)

| # | Bar | Measured | Threshold | Verdict |
|---|-----|----------|-----------|---------|
| 1a | Enumerated FI, overall UCB | 64/10000 = 0.64%, UCB 0.816% | ≤1% | **PASS** |
| 1b | Enumerated FI, per-family UCB ≤2% | 5 families fail (see below) | all ≤2% | **FAIL** |
| 2 | Recall (controls) | 1552/2000 = 77.6% | ≥80% | **FAIL** (fatal) |
| 3a | Ablation FI ≥2× full | 1244 vs 64 = 19.4× | ≥2× | **PASS** |
| 3b | Ablation holdout-gap widening | 396 < 1180 | holdout_gap ≥ adv_gap | **FAIL** |
| 4a | Holdout per-family UCB ≤2% | 4 families fail (see below) | all ≤2% | **FAIL** |
| 4b | Holdout pooled UCB | 1572/10000 = 15.72%, UCB 16.45% | ≤1% | **FAIL** |
| 5 | Overstrict | 26/2000 = 1.3% | ≤5% | **PASS** |
| 6 | Determinism (×2 byte-identical, chains) | b_adv, b_ctrl, b_holdout all PASS | pass | **PASS** |

ALIVE requires all; any fail = DEAD. **Verdict: DEAD.**

### Bar 1b detail (enumerated per-family, 95% Wilson UCB)
- motiondir f1: 7/504, UCB 2.84% — FAIL
- motiondir f2: 2/116, UCB 6.07% — FAIL
- motiondir f3: 0/10, UCB 27.75% — FAIL (mathematically impossible; see defect note)
- timbredisc f1: 33/500, UCB 9.12% — FAIL
- timbredisc f3: 19/190, UCB 15.09% — FAIL
- All other 12 families: PASS.

Note: fresh measurement gives 64 FI (builder reported 61; +3 on motiondir
f1/f2). Fixtures verified against `b_adv.manifest` SHAs; the 3 extra FI
manually confirmed by direct binary run. Reporting the fresh number.

### Bar 4 detail (holdout, 10 novel families × 1000, post-freeze)
- R2H16-COL-1 (gain-shift SAME): 0/1000, UCB 0.38% — PASS
- R2H16-CCN-1 (local-patch doppelganger): 982/1000 = 98.2%, UCB 98.86% — FAIL
- R2H16-CCN-2 (cross-crop collision): 323/1000 = 32.3%, UCB 35.26% — FAIL
- R2H16-SHP-1 (hollow shapes): 0/1000 — PASS
- R2H16-SHP-2 (dual shape): 0/1000 — PASS
- R2H16-PTC-1 (overmodulated AM): 4/1000, UCB 1.02% — PASS
- R2H16-PTC-2 (subharmonic): 1/1000, UCB 0.56% — PASS
- R2H16-TMB-1 (formant boost): 72/1000 = 7.2%, UCB 8.97% — FAIL
- R2H16-TMB-2 (vibrato): 3/1000, UCB 0.88% — PASS
- R2H16-MOT-1 (checkerboard drift): 187/1000 = 18.7%, UCB 21.23% — FAIL
- Pooled: 1572/10000, UCB 16.45% — FAIL (≤1%).

The colorconst mechanism is fundamentally broken against local changes:
an 8×8 patch replacement (0.7% of pixels) defeats both formation and
challenge (98.2% FI). Mean-RGB cannot see it.

### Bar 3 detail (ablation)
Implemented as deterministic post-hoc glue (`src/score_ablation.py`); the
frozen Zag binary has no bank mode and the mechanism was not touched.
1-NN on formation confidence vs frozen bank (first 20 TRUE + 20 FALSE
exemplars per task in battery order; ties → FALSE).
- B-adv: abl FI 1244/10000 (12.44%) vs full 64/10000 (0.64%) → 19.4×. PASS.
- Holdout: abl FI 1968/10000 vs full 1572/10000.
- Gap: (1968−1572)=396 ≥ (1244−64)=1180? No. FAIL.

### Bar 6 detail (determinism)
- b_adv union ×2: byte-identical (ledger f99a8295…, stdout 3f1c4fba…), chain OK.
- b_ctrl union ×2: byte-identical (ledger 1e7f8022…, stdout bad91f30…), chain OK.
- b_holdout union ×2: byte-identical (ledger 57c22583…, stdout 33931626…), chain OK.

## Achievements
1. Shapetrans central-moment challenge: 0 FI on enumerated (was 53 in R2-14);
   0 FI on both holdout shape families.
2. Overall enumerated FI UCB 0.816% passes the ≤1% bar.
3. Overstrictness eliminated: 1.3% (was 96.5% in R2-14 with margins).
4. Determinism: all batteries byte-identical ×2 with verified hash chains.
5. Ablation confirms the G-challenge carries the load (19.4× FI without it).

## Failures
1. **Recall 77.6% < 80%** — fatal. The truth-quantity challenges withhold
   too many correct formations (colorconst 54.0% recall is the main drag).
2. **Per-family FI bars** — timbredisc f1/f3 and motiondir f1/f2 fail on
   enumerated; the frozen swapped timbredisc mapping's root cause (Goertzel
   bias) was never resolved.
3. **Holdout catastrophe** — colorconst local-patch: 98.2% FI. The
   mean-RGB quantity is blind to local edits; both formation and challenge
   fail together.
4. **Ablation gap** — the holdout gap does not widen (396 < 1180).

## Prereg defects (noted, not amended post-results)
1. Per-family Wilson UCB ≤2% is mathematically impossible for n≲200 even
   with zero errors (motiondir f2 n=116: UCB₀=3.21%; f3 n=10: UCB₀=27.75%).
   Scored honestly as FAIL.
2. §2 describes CH-CCN-2 (pixel-L1) but the frozen built mechanism retains
   CH-CCN-1 (mean-RGB) per the builder's investigation. Documented; mechanism
   not altered.
3. `abl_bank` was specified but never implemented in the frozen Zag; the
   completion measured it as post-hoc glue with fully disclosed semantics.

## Commits
- Prereg: `4601db7f3182181f525c5791339207243727caa2`
- Sources + builder results (pre-completion): `26fd4bb68863c7709d9d40da964b08762a5cab6b`
- Completion evidence + verdict: (this commit)

## Recommendation
Do not revive. The colorconst quantity (mean-RGB) is structurally
inadequate; the recall ceiling (~80.3% per prereg §7) was not reached;
and the timbredisc mapping anomaly remains unexplained. A successor fork
would need a spatially-sensitive colorconst quantity and a white-box
fix for the Goertzel bias.
