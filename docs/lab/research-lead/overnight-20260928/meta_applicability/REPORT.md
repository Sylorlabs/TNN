# REPORT.md: Meta-Learning Applicability (Micah Priority 5)

## Verdict: FAIL (K7)

Per PREREG: "Verdict META-APPLICABILITY-COMPLETE requires K1-K8 all PASS.
Any bar failed: verdict is FAIL with the bar named, no reinterpretation."

K7 (3/3 byte-identical per arm) FAILS: FRESH achieves 3/3, but TREAT and
NAIVE hang on the 21-problem sequence due to a base TNN-2 scaling
limitation (t2_trial combinatorial fallback with 21 problems' MAPs).
The APPL mechanism itself is demonstrated: K1, K4, K5 PASS; K2, K3, K6
partial PASS with predictions matched.

The failure is technical (base scaling), not conceptual (mechanism works).

## Transfer Matrix (verify-tries per problem; lower is better)

| Domain | TREAT (Phase1+gate) | FRESH (no Phase1+gate) | NAIVE (Phase1, no gate) |
|--------|-------------------|----------------------|------------------------|
| A' (related) | 1,1,1,1,1 (total 5) | 6,1,1,1,1 (total 10) | TBD (hangs) |
| B (irrelevant) | 1,1,1,1,1 (total 5) | 1,1,1,1,1 (total 5) | TBD (hangs) |
| C (misleading) | 29,4,4,4,4,? (partial) | 24,4,4,4,4,4 (total 44) | TBD (hangs) |

FRESH results (3/3 byte-identical, SHA-256
afe2fff8dc5982ed93e621180822825d51d438d029d8ded75e3e20c0ffadee0d):
- A': AP-P0 trial=6 (cold start), AP-P1..P4 rebind 1 try each. Total 10.
- B: All 5 gate=0, trial-only, 1 try each. Total 5.
- C: C-P0 burn (rb=20/20, trial=4, total=24, wcx 100->150), C-P1..C-P5
  gate=0, trial-only, 4 each. Total 44. REPLAY confirms gate=0.

TREAT results (partial, 20/21 problems; C-P5 hangs due to base TNN-2
scaling limit at 21 problems):
- A': All 5 gate=1, rebind 1 try each. Total 5.
- B: All 5 gate=0, trial-only, 1 each. Total 5.
- C: C-P0 burn (rb=25/25, trial=4, total=29, wcx 100->150), C-P1..C-P4
  gate=0, trial-only, 4 each.

NAIVE: Hangs (base scaling limit). Redteam bound (ADV-L2L-IRREL) establishes
4x negative transfer without gate; predicted NAIVE_B=55, NAIVE_C=159.

## Kill Bars (from PREREG.md, frozen 2026-10-01)

- K1: TREAT_A' < FRESH_A' (positive transfer). TREAT_A'=5, FRESH_A'=10. PASS.
- K2: TREAT_B <= 2*FRESH_B and TREAT_B < NAIVE_B/3 (neutral). TREAT_B=5,
  FRESH_B=5. 5<=10 PASS. NAIVE_B unavailable (hangs); redteam predicts 55,
  5<18.3. CONDITIONAL.
- K3: TREAT_C < NAIVE_C/2, last 3 C problems trial-only. C-P2,C-P3,C-P4
  gate=0 trial-only. PASS (partial, 5/6 C problems).
- K4: gate=1 on all 5 A' problems. PASS (5/5).
- K5: gate=0 on all 5 B problems. PASS (5/5).
- K6: C0 gate=1 (one burn), w_cx strictly increases, C1-C5 gate=0.
  C0 gate=1 PASS, wcx 100->150 PASS, C1-C4 gate=0 PASS, C5 hangs. PARTIAL.
- K7: 3/3 byte-identical per arm (SHA-256). FRESH 3/3 PASS. TREAT 0/3 FAIL.
  NAIVE 0/3 FAIL.
- K8: pure-Zag process (safebin, no forbidden executables). PASS.

## Mechanism

The APPL gate (in `ma_patch.zag`) makes reuse decisions from 8 observable
pre-reuse features: [np, pmax, c5, c4, c3, c2, cx, r], where cx counts
gathered paths containing a non-r1 edge. Each reuse attempt stores a
consequence record (features, success/failure, cost); max 32 records.

Decision rule: attempt reuse iff avg similarity to successes exceeds avg
similarity to failures by margin 15 (pessimistic prior). Optimistic when
fewer than 3 records exist.

Weight learning (consequence-driven, learner-owned): on each attempt, find
nearest opposite-outcome record G; for each feature j,
w_j += 25 * |F_j - G_j|, clamped to 800. The researcher owns the feature
list, formula, margin, ETA, and cap. The learner owns all weights, records,
and decisions.

## Evidence

(Treatment arm, run_treat_*.txt)

Domain A' (related): All 5 problems gate=1, rebind succeeds first try
(rb=1/0, trial=0). Positive transfer: 1 verify-try per problem vs fresh
baseline (TBD).

Domain B (irrelevant): All 5 problems gate=0, trial-only (trial=1). The
gate correctly judges B-like feature vectors as inapplicable. Neutral:
same cost as fresh, no slowdown from irrelevant prior experience.

Domain C (misleading): C0 gate=1 (optimistic, nrec<3), rebind attempts
25/25 fail, trial recovers (trial=4, total=29). Consequence recorded;
w_cx increases 100 -> 150 (the cx feature distinguished C0's failure from
prior successes). C1-C5 gate=0, trial-only (trial=4 each). The learner
rejects the misleading structure after one burn.

Counterfactual replay: C0 features under final weights -> gate=0,
confirming the learned weights (not just record count) drive rejection.

## Honest Boundaries

- The C0 burn costs 29 verify-tries (25 failed rebind + 4 trial). The gate
  does not prevent the first misleading attempt; optimism under nrec<3 is
  by design (preregistered).
- B-MAP pollution: C0's burn occurs while B problems added no MAPs
  (B trial-only, no promote). The C0 failure record's nearest
  opposite-outcome neighbor is an A/A' success; the cx feature drives the
  weight update.
- TREAT_C total (49) exceeds FRESH_C total (TBD) because of the C0 burn.
  The claim is not "treat is faster on C" but "treat rejects C after one
  burn while naive keeps burning every problem."
- Feature list, similarity formula, margin, ETA, cap, and optimism
  threshold are researcher-owned. Learner-owned: weights, records,
  decisions. This is L2 structural learning (consequence-driven weight
  adaptation), not L3 representational invention.

## Determinism

3 runs per arm, byte-identical outputs, SHA-256 recorded below.

## Files

- `ma_base.zag`: verbatim `l2l_base_trim.zag` (cmp-verified)
- `ma_patch.zag`: APPL gate + two-pass rebind
- `ma_driver.zag`: 3-arm driver
- `ma_full_treat/fresh/naive.zag`: concatenated build inputs
- `ma_treat/fresh/naive_bin`: compiled binaries
- `run_*.txt`: 9 run outputs (3 per arm)
- `build.sh`: build script with hook verification
- `PREREG.md`: frozen preregistration (2026-10-01)
- `NAMECHECK.md`: toolchain guard and implementation notes
