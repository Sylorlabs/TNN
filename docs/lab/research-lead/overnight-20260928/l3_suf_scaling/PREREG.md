# PREREG: L3-SUF-1-SCALING (resolution-records mechanism under scale)

Status: PREREG-FROZEN 2026-10-03, before any scaling implementation exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md under l3_suf_scaling/.

Worker: L3-SUF-1-SCALING (subagent, 2026-10-03). This is a non-ledger task
(claim minting paused). It does NOT modify the frozen builder code, the
builder's src/, or the adversary's sealed worlds.

## 1. Objective

Test whether the L3-SUF-1 resolution-records mechanism (sole-survivor rule
at element/form/reuse scales, per-element marking, frozen escalation
order) keeps working as world size and evidence volume grow, and locate
the scale at which it breaks.

Baseline (established): worlds with |D| = 6 disagreeing pairs, |U| = 4
undetermined pairs, nent = 10 entities, 150-probe budget, N_STAKE = 12.
This study scales |D|, |U|, entity count, and training/probe volume.
Probe budgets (150 setup / 500 escalation probe-more / 2000 total) and
N_STAKE = 12 stay frozen: the question is whether correctness degrades
gracefully (safe-direction ABSTAIN) under probe starvation, not whether
bigger budgets fix bigger worlds.

Out of scope (stated, not silently dropped): the three cognitive scales
(element/form/reuse) are frozen learner machinery; adding a fourth scale
would require redesigning the frozen learner, which this task forbids.
"More probes" is answered as probe-starvation tolerance under the frozen
budgets, not as a budget increase.

## 2. Scales (frozen)

One fresh learner per (family, scale); KB starts wiped. N_STAKE = 12.
Entity ids are sequential (< 1000, per the frozen l_ekey bound); context
ids 61/62. Truth: g0 = ORD(perm), g1 = PARITY (context-gated, worker's
own design; not the sealed worlds).

| scale | nent | \|D\| | \|U\| | \|A\| | ntrain |
|-------|------|------|------|------|--------|
| S1    | 10   | 6    | 4    | 8    | 20     |
| S2    | 20   | 20   | 8    | 16   | 56     |
| S3    | 30   | 40   | 12   | 24   | 104    |
| S4    | 40   | 60   | 16   | 32   | 152    |
| S4b   | 41   | 64   | 17   | 34   | 162    |
| S5    | 50   | 80   | 20   | 40   | 200    |

Families (worker's own world builders, same frozen WB interface):
- INV (G0-class invention): D trained at both contexts; A trained at one
  random context; U withheld from training, unprobeable, undetermined,
  anti-tiebreak truth at both contexts. Stakes (12): 3 U heldout
  (det=1), 3 D trained (det=0, held=1), 3 A trained (det=0, held=1),
  1 U extra (det=1, held=0), 2 untrained agreeing (det=0, held=0).
- ABS (G-B-class abstain): same truth/training shape. Stakes (12):
  4 U (det=1, held=1), 4 D trained (det=0, held=1), 4 A trained
  (det=0, held=1).

Predicted structural boundary (from frozen-learner source inspection,
recorded before running): l_probe_phase's used-pair set is a fixed
40x40 buffer (usedp[1600], indexed p1*40+p2). nent > 40 overflows it.
S4b/S5 are expected NOT to complete. The experiment verifies the
boundary is real and sharp (S4 passes, S4b fails).

## 3. Kill bars (frozen; this is a discrimination instrument, not a
benchmark to pass: a FAIL at some scale is the intended signal)

- SC-K1 (no crash, S1-S4): all 8 runs (INV+ABS x S1-S4) exit 0 with no
  runtime panic.
- SC-K2 (sole-survivor works at scale, INV, every scale S1-S4):
  (i) first_unres_mark > first_creject (SEQ order: marking follows
  committed-prediction REJECTs); (ii) op_fail >= 2 (>= 2 non-marking
  FORM_TRY FAILs before lift adoption); (iii) post-escalation stakes
  shape: 0 REJECTs on determined queries AND 100% ABSTAIN on U queries.
- SC-K3 (marking correct at scale, ABS, every scale S1-S4):
  (i) 0 wrong predictions on heldout; (ii) >= ceil(5*D_det/6) correct on
  determined heldout (D_det = 8, so >= 7); (iii) 100% ABSTAIN on
  undetermined heldout; (iv) surgical precision: among stakes-queried
  determined pairs, fraction with final record mask == UNRESOLVED <= 0.5
  (bounds the known safe-direction over-marking; > 0.5 is smearing).
- SC-K4 (graceful degradation): (i) total TESTs <= 2000 on every run
  (B_REVISE honored); (ii) at S3/S4, where the 150-probe setup budget is
  exhausted by slot-varying alone (staged coverage ~= 0), SC-K2 and
  SC-K3 still hold: degradation is safe-direction (ABSTAIN), never
  confident-wrong. Reported per scale (informational): probes used,
  staged coverage, runtime.
- SC-K5 (sharp boundary): S4b (nent=41) and S5 (nent=50) do NOT complete
  (nonzero exit / runtime panic consistent with the source-identified
  usedp overflow), while S4 (nent=40) passes SC-K1. If S4b/S5
  unexpectedly complete, SC-K5 FAILs as stated and the true boundary is
  recorded instead.
- SC-K6 (determinism): 3/3 byte-identical stdout per run; sha256
  digests recorded.

## 4. Falsifiers

F-SCALE-CRASH -> SC-K1. F-SCALE-SOLE -> SC-K2. F-SCALE-MARK -> SC-K3.
F-SCALE-BUDGET -> SC-K4. F-SCALE-BOUNDARY -> SC-K5.

## 5. VOID (terminal)

Any edit to the frozen builder src/ or adversary sealed worlds; any
forbidden-interpreter invocation (pure Zag, safebin mandatory); any 3/3
divergence; any inspection of the adversary's sealed KEY.md by this
worker (scaling worlds are the worker's own design; no key needed).

## 6. Known boundaries (honest)

- The frozen learner carries fixed buffers (usedp 40x40, ents 100,
  guard-reexpand aug 512 quads, 16KB form). This study does not change
  them; it maps where they bind.
- Only two world families (invention, abstain). Transfer/reuse,
  revision, and retirement at scale are not tested here.
- A FAIL of SC-K2/SC-K3 at some scale S is evidence about that scale,
  not a verdict on the L3 claim (already adjudicated through SUF-K12
  governance); it is reported as the scaling envelope of the mechanism.
