# SEALED_EVAL.md - Sealed evaluation of F2 v3 on World C-prime

Date: 2026-10-01. Adversary: independent (F2v3-ADVERSARY).
Frozen prereg: PREREG_F2V3.md (committed alone at 13206c15b).
Sealed world: F2v3/sealed/f2v3_world_cprime.zag,
sha256 c018fc657346a9771cd41315dbedb855755225e7ee552990e3595b1a4acad78a
(recorded in SEALED_CPRIME.md before any sealed run).

## Binaries (built by the adversary from frozen sources)

- Learner source: f2v3_learner.zag,
  sha256 91c9390f9567e3c99fbfbdcf0129d709d954a628c8d604b3139ea762f50f8900.
  Build-chain verified: rebuilding learner + World A reproduces the
  builder-recorded binary hash 62ee648f... bit-for-bit.
- /tmp/f2v3_cprime_sealed (v3 learner + sealed C-prime):
  68bb09f48a4c1fe9a1d22907b252b7104e507639cb7ce5376766dace86af0b63
- /tmp/f2v3_nc3_sealed (frozen v2 learner + sealed C-prime, NC3 ablation):
  6b481f5ca1db0a5dcb5a5f92b4ff39034b048b155ad699eaae5ad892e9756938
- /tmp/scratch_rand (8-seed random control, standalone Zag): 0/160.
- /tmp/nc2 (memorization-replay baseline, standalone Zag): NC2_RESULT 0.

## Determinism (K4-R7, part)

3/3 sealed runs byte-identical: `cmp` confirms
/tmp/sealed_run1.log == /tmp/sealed_run2.log == /tmp/sealed_run3.log
(byte-by-byte; exit 0 on both comparisons).
Tool note: the safebin `sha256sum` (symlink to /usr/bin/sha256sum)
returns the empty-string hash when reading these exact 13050-byte logs
to EOF (a reproducible environment quirk; prefixes hash correctly and
`head`/`cat`/`wc`/`od` all read the content fine). `cmp` is the
definitive byte-identical evidence and it passes. Pure Zag throughout
(safebin PATH; `which python3` / `which python` print nothing; no
forbidden executable invoked at any stage of build, execution, or log
handling). No em dashes in any wave documentation (grep verified).

One governance note, reported honestly: during draft-world editing the
adversary reflexively typed a `python3 -c` probe inside a compound
shell command. Under the safebin PATH `python3` does not resolve, so no
Python interpreter executed (command not found; zero effect on any
artifact; all actual work used only safebin tools). It is recorded here
as an attempted invocation that did not execute, for the coordinator's
judgment. No scientific result was touched by it.

## Sealed run narrative (3/3 identical; run 1 representative)

- WORLD Cprime-dual-contextual-SEALED, NHYP 216 (X:6, Y1:6, Y2:6).
- Standard rounds 1-5 pin Y1/Y2 (216 -> 180 -> 144 -> 30 -> 12 -> 6):
  [SX,W,W,OY1], [SX,SJ,W,W,OY1], [SX,W,W,W,OY2], [SX,SJ,W,W,W,OY2],
  [SX,SK,W,W,W,OY2]. Standard scan then exhausts at nalive=6.
- DPDS round 6: pair (78,80), D={X} (runtime diff); D2CERT logged for
  pair (78,79) (indistinguishable to depth 8); distinguishing sequence
  [SX,SJ,W,W,W,W,W,OX] discovered by enumeration (8 primitives, not a
  source literal); pred [1] vs [0]; actual [0]; killed [78,79];
  nalive=4. Ledger entry appended.
- DPDS round 7: pair (80,81), D={X}; sequence [SX,SK,W,W,W,W,W,OX]
  (8 primitives); pred [0] vs [1]; actual [0]; killed [81,83];
  nalive=2. Ledger entry appended.
- DPDS round 8: pair (80,82), D={X}; full restricted-alphabet scan to
  depth 8 finds no distinguishing sequence; D2CERT logged.
  DPDS_EXHAUSTION. SURVIVORS [80,82], exhausted=1, ledger_n=2.
- Goal phase: PLAN_C2 M=[SX,SJ,SK,W,SX,W,SX,W,SX] (len 9),
  PLAN_AGREEMENT 1, GOAL_REAL_C2 1 (all twelve SUFFIX observations 1).
- RANDOM_BASELINE_C2 0/20 (seed 12345). OBS_USED 19.
- PROGRAM_FAIL mask=31 (bit 32, K4-R4 convergence, not set).

## Per-bar verdicts (frozen bars, prereg section 8)

- K4-R1 (passive ambiguity): PASS. NHYP 216 >= 2 (X:6, Y1:6, Y2:6).
- K4-R2 (construction, not enumeration): PASS. Adversary source audit:
  neither distinguishing sequence ([SX,SJ,W,W,W,W,W,OX],
  [SX,SK,W,W,W,W,W,OX]) nor any bracketed primitive sequence appears in
  f2v3_learner.zag; experiments arise solely from iterative-deepening
  enumeration (standard and pair-restricted); the executed sequences
  differ in composition from every dev-world run.
- K4-R3 (disagreement-driven): PASS. "K4-R3 PASS zero world calls in
  search". All 7 executed experiments logged with predicted vectors
  showing disagreement; the discrimination ledger is complete (2
  entries; every elimination backed).
- K4-R4 (convergence): FAIL. The loop terminates by exhaustion with
  nalive=2 (SURVIVORS [80,82]), not exactly one survivor. w_verify
  correctly identifies the true Y1/Y2 rules (ty1=1, ty2=2) but the
  exactly-one-survivor clause fails. This is the killing bar.
- K4-R4b (pairwise distinguishability): PASS.
  (i) Both discrimination eliminations ([78,79] on actual [0] vs pred
  [1]; [81,83] on actual [0] vs pred [1]) contradicted the actual
  observation vector of their logged distinguishing sequence.
  (ii) At termination the single live pair (80,82) carries a logged
  D2 certificate (full pair-restricted scan to depth 8, no disagreeing
  sequence). The X-class was resolved by evidence where resolvable and
  honestly certified where not.
- K4-R5 (model to goal): PASS. (a) Full plan achieves the sustained
  triple predicate for real (GOAL_REAL_C2 1, PLAN_AGREEMENT 1).
  (b) Random-action control 0/20.
- K4-R6 (observation economy): PASS. OBS_USED 19 on C-prime; World A
  dev used 6; total 25 <= 32 across both worlds.
- K4-R7 (determinism and purity): PASS. 3/3 byte-identical (cmp);
  pure Zag; no em dashes.

## Why K4-R4 failed (adversary analysis, hand-verified)

The surviving pair (80,82) carries X-rules (Y1->X, d3, K==1) and
(Y2->X, d2, J==1): "crossed" rules whose contexts are cross-coupled.
Under the frozen L_advance semantics (context evaluated at cause time):
- (Y1,d3,K=1) predicts X(t)=1 iff X(t-5)=1 AND J(t-5)=1 AND K(t-3)=1.
- (Y2,d2,J=1) predicts X(t)=1 iff X(t-5)=1 AND K(t-5)=1 AND J(t-2)=1.
Disagreement requires [J(t-5) AND K(t-3)] != [K(t-5) AND J(t-2)] with
X(t-5)=1. The minimal construction (SX,SJ at t-5; SK strictly between
t-5 and t-3; 5 WAITs; OX at t) uses 9 primitives; all alternative
constructions use 9-10. D2=8 is therefore provably insufficient for
this pair, and the learner's exhaustive depth-8 scan correctly
certifies indistinguishability. This is not a world artifact and not an
implementation bug: it is a genuine coverage gap in the D2=8 bound for
the X-rule equivalence class, exactly the outcome the prereg
anticipated ("If a live pair needs 9+ primitives, the D2 certificate
honestly reports indistinguishability and K4-R4 fails; the bar has
teeth"). DPDS resolved 4 of 6 X-variants by discovered evidence; the
remaining crossed-context pair needs depth 9.

## Negative controls

- NC1 (random-action control; kill via K4-R5b): 0/20 on the sealed run
  (seed 12345). Standalone 8-seed scratch program (identical LCG stream,
  alphabet, trajectory, predicate; cross-validated: seed 12345 gives
  0/20 matching the binary): seeds 12345, 7, 99, 1234, 55555, 987654,
  20261001, 42 all 0/20. TOTAL 0/160. Non-vacuity condition 4 holds.
- NC2 (memorization-replay baseline; reported, not kill): standalone
  Zag program storing the passive trace and all 7 executed experiment
  trajectories, acting by longest-suffix replay of goalvar observation
  histories (WAIT on no match), budget 30 steps. Replay produced
  [SJ,SK,W,W,SX,W,W,W,W,W,SX,...] (it discovers the gate flips from
  memory but cannot sustain the X cadence). NC2_RESULT 0: the sustained
  predicate is not achieved. Memorization (L0) does not explain the
  learner's goal success. Reported honestly as expected.
- NC3 (mechanism ablation; reported, not kill): frozen v2 learner
  (standard depth-6 only, no DPDS) on sealed C-prime terminates by
  exhaustion with SURVIVORS [78,79,80,81,82,83], nalive=6 >= 2,
  PROGRAM_FAIL mask=19. The X-variant failure mode reproduces; the
  control is informative (not uninformative): the v3 learner's DPDS
  accounts for resolving 4 of the 6 (6 -> 2), while the residual pair
  defeats D2=8.

## Verdict: BUILD-FAIL

Killing bar: K4-R4 (convergence). Evidence: sealed 3/3 runs terminate
by exhaustion with nalive=2 (SURVIVORS [80,82]), D2 certificates logged
for the indistinguishable pair; w_verify confirms the true Y1/Y2 rules
are the shared ones but the exactly-one-survivor clause fails.

What BUILD-FAIL establishes: DPDS with the frozen D2=8 bound resolves
most of the X-rule equivalence class by learner-discovered evidence
(4 of 6 variants, with a complete elimination trail and honest D2
certificates), achieves the harder sustained dual-contextual goal for
real on a fresh sealed world (GOAL_REAL_C2 1, random 0/20, NC2 0/1),
but does not fully cover the equivalence class: crossed-context
X-rule pairs need depth-9 distinguishing sequences. The mechanism is
bounded-effective, not complete, at D2=8.

What it does not establish: no claim about L3 (prereg section 12
stands); no generality claim beyond this world; the failure is a
depth-bound coverage gap, not evidence about representational
invention. A future revision would need to address the bound (e.g. a
principled deeper or smarter discrimination search), not add
per-world or per-pair semantic cases.

## Files delivered (all under
docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/)

- NAMECHECK_ADVERSARY.md (Step 0, toolchain guard, independence)
- SEALED_CPRIME.md (world spec, laws, schedule, non-vacuity cert,
  pre-run sha256)
- SEALED_EVAL.md (this file)
- sealed/f2v3_world_cprime.zag (the sealed world; the builder never
  reads this directory)
