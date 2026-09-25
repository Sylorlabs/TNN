# F23 SELFNORM — Kill-Bar Adjudication

**Mechanism:** F23 SELFNORM (mechanism 23), H5 fork round.
**Date:** 2026-09-25.
**Authority:** `deliberation_depth/monotonicity/training/fork_round/PREREG_FORKROUND.md`
(commit `0566cc81`); ideas file `ideas/native1_forks.md` Fork 4 wins on discrepancies.
**Commit:** `dd7e65a8adcfa01eeaf639c2ac1583d2a4ab59d4` (training evidence);
eval commit pending.

## Frozen mechanism

- `f1' = clamp(1000*f1/max(64,M1),0,1000)`
- `f4' = clamp(1000*f4/max(64,M4a),-1000,1000)`
- `M1` = inclusive trailing max of `f1` (released cells only);
  `M4a` = inclusive trailing max of `|f4|` (released cells only).
- Head: `C=clamp((w1*f1' + w4*f4' + Σother wi*fi)/1000+b,0,1000)`
- Fitted (byte-identical A/B): w=(1256,256,0,0,256,256,0,192), b=192.
- M4 release skeleton preserved exactly (B9: 5240/5240 release+correct identity).

## Fork-specific kill bars (prereg §3 + BUILDLOG interpretations)

| Bar | Criterion | Result | Verdict |
|-----|-----------|--------|---------|
| (a) | Clamp attractor: >50% released cells at conf≡0 or ≡1000 in any leg | **35/37 legs at 100% conf=1000** | **FIRES** |
| (b) | Theater rises vs M4 baseline: F23 V1+V2 > 160 | F23 V1+V2 = 0+0 = 0 | does NOT fire |
| (c) | w1 on f1' ≈ 0 (adjudicated on fitted w1 AND f1' constancy) | w1=1256 numerically, but **f1'≡1000 on 99.98% of released training cells** (4,221/4,222); w1 collinear with bias, unidentifiable; absolute margin signal destroyed | **FIRES** (per preregistered interpretation) |

## Prereg §4 B-metrics (frozen analyzer, 37-leg matrix)

| # | Bar | Threshold | F23 | Verdict |
|---|-----|-----------|-----|---------|
| B1 | 1→0 transitions | = 0 | 0 | PASS |
| B2 | Theater V1=V2=0 | = 0 | V1=0, V2=0 | PASS |
| B3 | G-violations (strict) | = 0 every family | **2 (redteam)** | **FAIL** |
| B4 | meanConfCorrect | ≥ 0.50 | 1.000 | PASS |
| B4b | Honest-family floor | ≥ 0.50 | 1.000 all four | PASS |
| B5 | Separation | ≥ 0.20 | **0.000** (conf=1000 for correct AND wrong) | **FAIL** |
| B6 | Recall vs M4 | ≥ 0.95 | 1.00 (B9 identity) | PASS |
| B7 | Abstention volume | ≤ 0.30 | 0.148 | PASS |
| B8 | G-definedness (amended §4b) | per §4b | **ceiling/P FAILS nonvacuity** (G≡+1.000, not genuine calibration); trap VOID (3 M4-feasible slots < 4); others PASS | **FAIL** |
| B9 | Release+correct identity vs M4 | 100% | 5240/5240 | PASS |
| B12 | G>0 crossings | recorded | admit 0, ceil/D 3, ceil/O 0, ceil/P 6, cost 0, logic 0, redteam 5, revoke 0, trap 3 | recorded |
| B13 | Underconfidence floor G≥−0.100 | ≥ −0.100 | all G ≥ +0.000 | PASS |
| B3pi | Per-item B3 | recorded | (conf constant ⇒ reduces to acc monotonicity; B1=0 ⇒ 0 violations) | recorded |

## Deltas vs NEC m9 (V1=0, V2=0, Gviol=6)

- F23: V1=0 (Δ0), V2=0 (Δ0), Gviol=2 (Δ−4).
- F23 reduces G-violations vs NEC but introduces clamp-attractor pathology.

## Verdict: **KILLED**

F23 SELFNORM is **KILLED** by preregistered kill bars (a) and (c), and
additionally fails B3 (strict), B5, and B8 (ceiling/P nonvacuity).

**Failure mode:** Self-normalization by the trailing max destroys the
absolute `f1` margin signal (`f1'` constant at 1000). The fitted head,
with `w1=1256` on a constant feature, saturates at the `conf=1000` clamp
on 100% of released cells in 35/37 legs. The result is a degenerate
confidence head: zero separation between correct and wrong (B5=0.000),
vacuous G≡+1.000 on ceiling/P, and redteam G-violations.

This confirms the H5 hypothesis: the absolute `f1` margin is load-bearing
for calibration. Normalizing it away — even by a per-item trailing max
that preserves within-item monotonicity — removes the signal the head
needs to distinguish correct from wrong.

**Failure-mode number:** FM-SELFNORM-001 (clamp attractor via destroyed
margin signal).

## Prereg SHA erratum (recorded, not amending)

Fork prereg cites feature-SHA
`4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65e897d`
(actual frozen file:
`4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`;
one hex digit). Extant frozen file used; transcription erratum reported.
