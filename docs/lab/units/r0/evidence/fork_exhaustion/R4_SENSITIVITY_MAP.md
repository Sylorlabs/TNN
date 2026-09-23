# R-4 SENSITIVITY MAP — fork exhaustion (B-T3 dose-curve degradation rule)

Fork-exhaustion crew · Track R0 · 2026-09-21
Harness: `fork_exhaustion.py` (deterministic arithmetic; no RNG). Raw: `r4_raw.json`.

## Grid

- Formulations: F1 drawdown-from-running-max (recommended), F2 adjacent-only,
  F3 cumulative-from-baseline, F4 strict-zero, F5 endpoint-only,
  F6 total-variation-of-drops, F7 recovery-allowed drawdown,
  F8 bleed-flag-hardened (swarm's flag convention as a hard rule)
- Tolerances: {0, 5, 10, 25, 50}/1000; boundary `≤` vs `<`
- 18 curves: 10 inherited (M0, S1, S1b, S2, S3, S3b, S4, S5, S6, S7) + 8 new
  adversarial (A1 double-dip, A2 early-drop-25-flat, A3 mid-dip-25-recovers,
  A4 improve-then-bleed, A5 mid-dip-20-recovers, A6 boundary-30, A7 slow-bleed-30,
  A8 V-shape-deep)

## Map — mismatches vs normative, formulation × tolerance (≤ boundary)

| formulation \ tol | 0 | 5 | 10 | 25 | 50 |
|---|---|---|---|---|---|
| F1 drawdown-running-max | 8 | 7 | 7 | **0** | 8 |
| F2 adjacent-only | 8 | 7 | 9 | 3 | 8 |
| F3 cumulative-baseline | 9 | 8 | 8 | 1 | 8 |
| F4 strict-zero | 8 | 8 | 8 | 8 | 8 |
| F5 endpoint-only | 8 | 8 | 8 | 3 | 8 |
| F6 total-variation | 8 | 7 | 7 | 1 | 8 |
| F7 recovery-allowed | 7 | 7 | 7 | 2 | 8 |
| F8 bleed-flag-hard | 8 | 7 | 7 | 4 | 7 |

**F1 × 25 is the unique zero-mismatch cell in the entire 8×5 grid.**
No other (formulation, tolerance) pair matches every normative judgment.

## Which curves kill which formulation (tol = 25)

| Formulation | Mismatching curves | Diagnosis |
|---|---|---|
| F1 drawdown-running-max | — | matches all 18 |
| F2 adjacent-only | S3b, A4, A7 | Slow-bleed loophole, twice over: any bleed spread ≤25/step passes. A7 (−5/step to −30) is a second independent instance of the S3b flaw. |
| F3 cumulative-baseline | A4 | Improve-then-bleed: baseline 900, ends 910 — cumulative sees "improvement" while 40/1000 was lost from the peak. (Swarm's T1/T2 point, now with a third instance.) |
| F4 strict-zero | S1b, S2, S3, S5, S7, A2, A3, A5 (8) | Fails every transient-recovery and every within-budget loss — mislabels reorganization as degradation. Tolerance column irrelevant by construction. |
| F5 endpoint-only | A1, A4, A8 | Blind to interior damage: any curve that ends near baseline passes regardless of what happened mid-dose. |
| F6 total-variation | S5 | Near-miss fork: accumulates dips, so the ±20 sawtooth (never below 930, ends 930) scores 60 and fails. Punishes oscillation the bar's "no degradation" language tolerates. |
| F7 recovery-allowed | A1, A8 | Forgives any drawdown recovered by a later dose — the double-dip and V-shape pass despite 50/1000 interior damage. The bar polices the dose path, not just the endpoint. |
| F8 bleed-flag-hard | S1b, S3, S7, A2 | Over-strict: hardens the monitor-flag into a fail rule and rejects sub-span losses and boundary-exact bleeds the normative suite passes. The flag stays a flag. |

## Boundary fork

At tol=25 with `<` instead of `≤`: F1 goes from 0 → 4 mismatches
(S3, S7, A2, A3 — every drawdown-exactly-25 curve fails). The `≤` boundary
is forced by the normative boundary cases, consistent with the swarm's
"exactly 25 passes" amendment text.

## Tolerance knife-edges (F1)

| tol | What flips |
|---|---|
| 0 | S2 (1-probe transient) fails — the strict-zero mislabeling |
| 5 | S1b (20), S3 (25), S5 (20), S7 (25) fail — sub-span and boundary losses rejected |
| 10 | same four fail |
| 25 | all pass; S1 (40), S3b (50), S4 (50), A6/A7 (30) fail — the materiality line |
| 50 | S1 (40) passes — a full span loss tolerated; too lax |

The 25/1000 line is the only tolerance that keeps every sub-span/transient/
boundary case passing while failing every span-or-larger loss, across all 18
curves. It coincides with the independently derived materiality quantum
(one average consistent span's occurrence budget; 5 probes).

## Verdict on R-4

**CONFIRM — strengthened.** The swarm tested 4 formulations; the exhaustion
tested 8 (adding endpoint-only, total-variation, recovery-allowed,
bleed-flag-hard) against 18 curves (8 new adversarial). Max drawdown from
running maximum ≤ 25/1000 (≤ boundary) is the UNIQUE zero-mismatch cell in
the full grid. No fork moves the recommendation. The `<` boundary variant is
killed by the boundary cases; strict-zero is killed 8 ways; adjacent-only's
bleed loophole now has three independent instances (S3b, A4, A7).
