# Q4 Baseline Comparison Preregistration: F-PARCOND vs Simple Baselines

Date: 2026-09-30. Worker: Q4 Baseline Comparison Worker.
Parent task: promotion pipeline step 5 (simple-baseline comparison) for F-PARCOND.

## Objective

Answer honestly: does the Q4 learner (BUILD-PASS 5f56cc491, 64/64 on
F-PARCOND) beat simple baselines, or is memorization sufficient?

F-PARCOND: D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3). Only bits 0-2
of x matter, so the truth table has 8 combos (each repeated 8x in the
64-case evaluation). On an 8-combo world a lookup table with full
coverage also scores 64/64. This experiment measures exactly where the
learner's edge over simple baselines is real and where it is not.

## Reference numbers (from committed results, not re-measured here)

- Learner Phase 1: 64/64 true accuracy, 7 ops, from 8 biased passive +
  24 uncertainty-sampled adaptive interventions (32 observations).
- Best single-bit observable: 40/64 = 0.625.
- Learner Phase 2 reuse: hit_iv = 0, 64/64. Scratch: hit_iv = 24, 52/64.

## Baselines (all pure Zag, implemented in q4_baseline.zag)

- MEM: lookup table on (x1,x2,x3) combo key. Predict stored y if the
  combo was observed, else the majority class of the evidence.
- 1NN: 1-nearest-neighbor on Hamming distance over bits 0-2 of the
  stored evidence points. Ties broken by lowest evidence index.
- LIN: linear threshold model. Grid search over w1,w2,w3,b in
  {-1,0,1} (81 combos); pick highest evidence accuracy; tie-break by
  fewer nonzero weights, then lexicographic order. Predict 1 iff
  w.x + b > 0.
- RAND: seeded coin flip per test case (expected 32/64).
- MEM-COMP (Phase 2 only): build D table from fam-6 passive samples via
  D = C' XOR x4 per observed (x1,x2,x3) combo; predict
  C' = D_table[x&7] XOR x4; unseen combos fall back to evidence
  majority. This is the "memorize-then-compose" baseline matching the
  learner's reuse condition structurally.

## Experiments

- E1 (matched passive evidence): every baseline gets exactly the 8
  biased passive samples from the identical protocol as the learner
  (passive() copied verbatim, PRNG seed 123456789, first RNG consumer).
  Measure truth-table accuracy over x in 0..63. Also report how many of
  the 8 (x1,x2,x3) combos the 8 passive samples cover.
- E2 (dumb sampler, matched budget): 8 passive + 24 uniform-random
  additional observations (same PRNG stream continued). Measure accuracy
  for MEM, 1NN, LIN. Tests whether a non-adaptive sampler with the same
  32-observation budget reaches 64/64.
- E3 (sample-to-coverage): for MEM under uniform random sampling, draws
  needed until all 8 combos observed, over seeds 1..20. Report mean and
  max. Compare against the learner's 32 observations (coupon-collector
  expectation is about 21.7 for 8 coupons).
- E4 (Phase-2 reuse vs memorize-then-compose): 8 passive fam-6 samples
  (seed 555555555, same as the paper). MEM-COMP accuracy over 64 cases.
  Compare with learner reuse 64/64 hit_iv=0 and scratch 52/64.

## Frozen Kill Bars

### K1: Baselines implemented
MEM, 1NN, LIN, RAND, and MEM-COMP all implemented in pure Zag in
q4_baseline.zag. sealed() and passive() replicated for fam 5/6.

### K2: Experiments measured
E1, E2, E3, E4 all executed. 3/3 byte-identical runs (same md5).
Exit 0, zero stderr on all runs.

### K3: Honest assessment written
Q4BASELINE_RESULT.md states plainly for each comparison whether the
learner beats the baseline, ties it, or loses to it, with the numbers.
No claim that the learner beats memorization on raw accuracy unless the
measurements show it.

### K4: Purity and determinism
Pure Zag at every stage. Zero Python invocations. 3/3 byte-identical.
Zero em dash bytes in committed docs.

## Predictions (recorded before running; may be wrong)

- P1: MEM with full combo coverage scores 64/64, tying the learner on
  raw accuracy. The learner's edge is not raw accuracy.
- P2: With only the 8 biased passive samples, MEM covers roughly 5 of 8
  combos and scores below 64/64; 1NN interpolates some unseen combos;
  LIN scores at most 56/64 (D=1 on {011,101,110} is not linearly
  separable; x1+x2+x3>=2 gets 7/8).
- P3: E3 mean draws to full coverage is under 32, i.e. uniform sampling
  + memorization can be MORE sample-efficient than the learner's 32
  observations on this tiny world.
- P4: MEM-COMP reaches 64/64 on Phase 2 whenever its 8 passive samples
  cover all 8 D-combos, matching learner reuse; the reuse-vs-scratch
  gap (0 vs 24) is a library-vs-no-library gap, reproducible by a lookup
  table, not a learner-specific advantage.

If P1-P4 hold, the honest conclusion is: the learner ties memorization
on prediction, beats linear/single-bit/RAND baselines, and its real
advantages are the compact reusable representation (7 ops, C0-D) rather
than raw predictive accuracy or sample efficiency on this 8-combo world.

## Falsifiers of my predictions

- FP1: MEM with 32 uniform-random observations fails to reach 64/64.
- FP2: LIN exceeds 56/64 on the truth table.
- FP3: E3 mean draws to coverage exceeds 32.

## Verdict Labels

- BASELINE-COMPARED: all kill bars pass; honest assessment delivered.

## Governance

- Prereg committed alone before implementation.
- Owned path: docs/lab/research-lead/overnight-20260928/q4_baseline/ only.
- Pathspec commits. No Python. No em dashes.
