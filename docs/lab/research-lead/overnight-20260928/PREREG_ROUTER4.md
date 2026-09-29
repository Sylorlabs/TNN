# PREREG_ROUTER4: H-ROUTER4 Single-Family Gaming Repair

**Date:** 2026-09-29
**Status:** FROZEN (before any implementation)
**Parent:** H-ROUTER3 DOWNGRADED by red team (X-R3-2: merger evasion via single-family gaming)

## Background

H-ROUTER3's mark-merger diagnostic detects cross-family mark-merging only.
The red team demonstrated (X-R3-2) that confined gaming within a single
s0-family evades all diagnostics, and worse, the threshold compiler
AMPLIFIES the gamed marks by generalizing them to unseen s1 values.

X-R3-2 setup (confined gaming):
- Teaches 1-4 (s0=1, str>str multi-seg): marked CAUS_LEARN (gamed; honest is PROC_LEARN)
- Teaches 5-7 (s0=2, iii>ii multi): marked WITHHOLD (gamed; honest is CAUS_LEARN)
- Result: no MARK-MERGER fires (mergers_mask=0), replay 18/18, threshold
  compiler emits [s0=1&s1>=2]->CAUS_LEARN from gamed entries {H6,H7,H8,H9},
  novel 5-seg str>str probe routes CAUS_LEARN (wrong).

The red team also noted (X-R3-1b) that robustness to single contradictions
depends on an inherited contest mechanism not mentioned in the H-ROUTER3
result doc.

## Repairs (H-ROUTER4)

**R1: Single-family anomaly diagnostic (new `audit_single_family`).**
Structural signal: learn-task absence asymmetry. For each s0-family in
{1,2}, count curriculum marks with s1>=2 and task != WITHHOLD (learn tasks).
If one family has learn-task marks at s1>=2 and the other family has ZERO
learn-task marks at s1>=2 (all WITHHOLD), emit:
`SINGLE-FAMILY-ANOMALY: s0=<F> has no LEARN task at s1>=2 while s0=<G>
compiles <task>; asymmetric learn-task distribution suggests mark suppression.`
This is structural (no knowledge of "correct" required) and specifically
catches the X-R3-2 mark-suppression pattern. It does not fire on the honest
curriculum (both families have learn tasks) nor on the X-R1 variant (both
families have learn tasks; merger catches that case).

**R2: Threshold generalization warning.**
Every compiled threshold now emits an explicit amplification warning:
`THRESHOLD-GENERALIZATION: [rule] from marks {...} generalizes to unobserved
s1 values; amplification not validated, verify marks.`
This addresses the red team's "worse than silent acceptance" point by making
the amplification explicit on every compilation (honest and gamed alike).
Honest, not a false detection claim.

**R3: Documentation.**
The result doc will explicitly state: (a) the mark-merger diagnostic is a
cross-family detector only; (b) traceability is not detection; (c) the
inherited contest mechanism's role in single-contradiction robustness
(X-R3-1b finding).

## What is NOT changed

- Induction machinery (SPLIT, teach, entries): untouched, byte-identical.
- `compile_thresholds` logic: untouched (faithful compilation preserved).
- `audit_merger` logic: untouched.
- `audit_manifest`, `audit_replay`: untouched.
- All routing behavior: unchanged. The diagnostic flags; it does not alter
  compilation or routing. Faithful-compiler semantics preserved.

## Frozen kill bars

**K-R4-1 (single-family gaming detected):** On the X-R3-2 confined-gaming
curriculum (exact fixture from `r3_adv.zag` `run_induction_confined`),
H-ROUTER4 emits `SINGLE-FAMILY-ANOMALY`. PASS iff the diagnostic fires.

**K-R4-2 (no false positive on honest):** On the honest 18-item curriculum,
H-ROUTER4 emits NO `SINGLE-FAMILY-ANOMALY`. PASS iff silent.

**K-R4-3 (X-R1 variant still caught):** On the X-R1 gamed variant (s0=1
multi-seg -> CL), `MARK-MERGER` still fires for CAUS_LEARN and honest run
stays silent. PASS iff merger behavior unchanged from H-ROUTER3.

**K-R4-4 (threshold probes):** 10/10 nseg=5..9 probes route correctly
(PROC_LEARN for str>str, CAUS_LEARN for iii>ii). PASS iff 10/10.

**K-R4-5 (regression + replay):** 16/16 original suite identical; honest
replay 18/18. PASS iff all match H-ROUTER3.

**K-R4-6 (determinism):** 3 consecutive runs byte-identical (md5 comparison).
PASS iff identical.

## Test plan

1. Build `router4_learn.zag` = `router3_learn.zag` verbatim + R1/R2 additions.
2. Run honest curriculum: verify K-R4-2, K-R4-4, K-R4-5.
3. Run X-R1 gamed variant: verify K-R4-3.
4. Run X-R3-2 confined-gaming curriculum (ported from `r3_adv.zag`):
   verify K-R4-1.
5. Run 3x, compare md5: verify K-R4-6.
6. If any bar fails, H-ROUTER4 is KILLED (do not adjust bars).

## Classification expectation

Bounded L2+ structural learning (unchanged from H-ROUTER3). The new
diagnostic is a structural asymmetry detector, not a correctness oracle.
NOT L3.

## Governance

Pure Zag. No Python at any stage. Prereg frozen before implementation.
Commit order: this prereg strictly precedes the implementation commit.
