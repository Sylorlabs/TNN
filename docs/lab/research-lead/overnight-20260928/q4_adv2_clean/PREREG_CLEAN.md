# F-RECFOLD Clean Rerun Preregistration (P-CLEAN)

## Status

PREREGISTRATION-CLEAN. This document freezes the K4-clean rerun protocol
for the F-RECFOLD second adversary family (H-NEW-2). Committed before the
clean implementation. This prereg strictly precedes all clean-wave
implementation, build, and evaluation work.

Supersedes: `efbc9ad9e` (v1 prereg; governance-tainted by disclosed Python
use during seed drafting; not adopted for canonical claims).
Design: `808ed196d` (unchanged).
V1 pilot: `3868e3852` (BUILD-FAIL pilot with K4-VIOLATION; substantive
result to verify: Q4 mechanism fails on recursive/repeated forms with
I1 40/64, I2 63/64, I3 32/64 on seed 11).

Zero Python used in writing this prereg. Zero em dash bytes.

## 1. Learner Freeze (L)

L = 5f56cc491 (Q4 F-PARCOND adversary test: BUILD-PASS).

Learner source:
`docs/lab/research-lead/overnight-20260928/q4_parcond/q4_parcond.zag`
(775 lines, committed in 5f56cc491).

The discovery mechanism (beam search, operators, signatures, evidence
collection, intervention selection, scoring, keep criteria) is verified
identical to L via shell diff, excluding only the sealed() world
definitions (fam 7-12 added for F-RECFOLD) and the main() driver. No
learner change is permitted after L.

## 2. Instances (Frozen)

The independent draw (seed 770404483, LCG per design section 5.5) is
complete, verified, and revealed. The mechanism is frozen, so instance
knowledge cannot alter its behavior. No redraw.

- I1 (easy, R1): D = XOR3( AND(X1,X5), AND(X2,X4), AND(X3,X6) ).
  Pairing (1,5)(2,4)(3,6). Motif AND. Top XOR3. Xd=X2. Xj=X3.
  Truth table: 28 rows with D=1.
- I2 (medium, R2): D = AND( AND( AND( AND( AND(X5,X4),X6),X1),X3),X2 ).
  Permutation (5,4,6,1,3,2). Motif AND. Xd=X1. Xj=X2.
  Truth table: 1 row with D=1.
- I3 (hard, R1): D = XOR3( XOR(X1,X2), XOR(X3,X5), XOR(X4,X6) ).
  Pairing (1,2)(3,5)(4,6). Motif XOR. Top XOR3. Xd=X6. Xj=X5.
  Truth table: 32 rows with D=1.

Each canonical form uses 5 operators from {AND, OR, NOT, XOR}. Fairness
gate passes (5 <= 7).

## 3. Evaluation Seeds (Frozen)

Learner RNG seeds: 11, 22, 33, 44, 55 (same set as v1 prereg B1).

3 instances x 5 seeds = 15 Phase-1 evaluations.

## 4. Protocol (Frozen)

Phase 1 (Discovery) per instance per seed, per design section 5.6:

- 8 passive (x,y) samples with selection bias: 6 of 8 satisfy Xd = Y
  for the instance decoy Xd; remaining 2 drawn uniformly.
- Up to 24 adaptive interventions (do-operator: SET any combination of
  Xi to 0/1, then read Y), selected by top-8 beam disagreement on
  unobserved x.
- Beam search: width 32, operators {AND, OR, NOT, XOR}, truth-table
  signatures, simplicity tax (200 * opc subtracted from 10000-scale
  accuracy score), incremental growth trace.
- Keep criteria (all must hold):
  (a) best ev accuracy >= best single-observable ev accuracy + 0.15;
  (b) operator count <= 7;
  (c) minimality: no other beam node within 0.02 ev accuracy with
      fewer operators.
- Report per run: BEST node id, ev_correct/en, true_correct/64,
  bobs_true/64, opc, keep flag, trace_events, node count.

Scope: Phase 1 only (matches v1 pilot scope). Phase 2 (reuse),
A-SCRATCH, and full A-BASE (memorization, 1NN, linear, random) are not
in clean-rerun scope. B3 uses the best-observable baseline
(bobs_true_correct: best single variable true accuracy), as in the v1
pilot.

Budgets are hard caps. Exceeding 24 interventions or 7 operators fires
F-OVERBUDGET.

## 5. Bars (Frozen, unchanged from v1)

### B1: Accuracy
For each of the 3 instances, true accuracy 64/64 on at least 4 of 5
seeds.

### B2: Operator Count and Growth Trace
Kept D <= 7 operators with incremental growth trace (trace_events > 0,
monotonic construction via node_new_op).

### B3: Margin over Baselines
True accuracy margin over best baseline >= 0.15 on hard instance (I3),
>= 0.10 on easy (I1) and medium (I2). Baseline: best single observable
variable true accuracy (bobs_true_correct).

### B4: Structural Audit
Post-reveal structural audit passes on all 3 instances:
- R1 instances: at least 2 motif instances on disjoint variable pairs
  (semantic truth-table match, not syntactic).
- R2 instances: nesting chain of depth at least 2 using the drawn motif.
B4 is evaluated only if B1 passes on an instance; otherwise B4 is
NOT APPLICABLE for that instance (per v1 pilot precedent).

## 6. Falsifiers (Frozen)

### F-SEAL: Information Leak
Not applicable: instances are revealed and the mechanism is frozen.
Sealed parameters cannot alter frozen mechanism behavior.

### F-MEM: Non-discriminative Instance
Memorization baseline reaches 64/64 within budget on an instance ->
VOID the instance. Informational: v1 pilot bobs_true values (36/64,
33/64, 32/64) indicate instances discriminate.

### F-NOREP: Form Not Discovered
64/64 accuracy achieved but structural audit fails -> the C0-C form
claim FAILS for that instance. Accuracy still reported.

### F-OVERBUDGET: Budget Exceeded
Interventions > 24 per phase, or kept D operators > 7 -> FAIL.

### F-PYTHON: Python Use
Any Python invocation in prereg writing, implementation, build, run,
verification, or analysis -> VOID the wave (K3 kill bar).

## 7. Determinism (KB4)

The frozen binary is run 3 times; stdout must be byte-identical across
all 3 runs. Compilation via znc (pure Zag). Zero Python. Zero em dash
bytes in all committed artifacts.

## 8. Verdict

Against the frozen bars, per instance and for the battery:

- F-PYTHON fires, or K1/K2/K3 violated: FREC-CLEAN-VOID.
- B1+B2+B3+B4 pass on all 3 instances: FREC-CLEAN-PASS (overturns the
  v1 pilot finding).
- B1 fails on any instance: FREC-CLEAN-FAIL (verifies the v1 pilot
  substantive finding under K4-clean protocol).

A clean FAIL verifies that the frozen Q4 mechanism does not discover
recursive/repeated forms. It does not close C0-C (a third family remains
future work) and starts no SURVIVES claim (promotion steps 4-11 remain).

## 9. Governance

- This prereg was written without Python (shell, git, and file tools
  only).
- Zero em dash bytes (verified via shell grep before commit).
- Prereg commit strictly precedes the clean implementation (prereg
  commit-order self-check).
- Seed 770404483 with SHA256
  5426835ee69f290cb98f12cbc94e7a03fe6de2ada5de91745259ad4ee20fda02
  is carried over from v1; the value was generated via /dev/urandom
  and hashed with sha256sum (shell only). The v1 Python violation
  concerned a discarded earlier seed, not this value.
- Local commits only on tnn-native-lab; owned path
  `docs/lab/research-lead/overnight-20260928/q4_adv2_clean/` with
  pathspec commits; nothing pushed.
