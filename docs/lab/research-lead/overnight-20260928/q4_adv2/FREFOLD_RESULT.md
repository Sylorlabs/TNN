# F-RECFOLD Evaluation Result (Pilot)

## Status

PILOT-COMPLETE. Draw and pilot implementation complete. Full 5-seed
evaluation not completed due to time constraints. Pilot results indicate
BUILD-FAIL against B1.

Prereg: efbc9ad9e
Design: 808ed196d
Draw: DRAW_TRANSCRIPT.md (this directory)

## Draw Summary (K2)

Independent draw performed via LCG (s_0=770404483). Seed hash verified.
Fairness gate passed (5 ops per instance, <=7).

- Instance 1 (easy, R1): motif=AND, top=XOR3, pairing=(1,5)(2,4)(3,6),
  Xd=X2, Xj=X3. D = XOR3(AND(X1,X5),AND(X2,X4),AND(X3,X6))
- Instance 2 (medium, R2): motif=AND, perm=(5,4,6,1,3,2), Xd=X1, Xj=X2.
  D = AND(AND(AND(AND(AND(X5,X4),X6),X1),X3),X2)
- Instance 3 (hard, R1): motif=XOR, top=XOR3, pairing=(1,2)(3,5)(4,6),
  Xd=X6, Xj=X5. D = XOR3(XOR(X1,X2),XOR(X3,X5),XOR(X4,X6))

## Implementation

File: frecfold.zag (based on frozen mechanism from q4_parcond.zag L=5f56cc491)
- Added x6 extraction to sealed()
- Added fam 7,8,9 (F-RECFOLD Phase 1 instances)
- Added fam 10,11,12 (F-RECFOLD Phase 2 reuse targets)
- New main() driver for F-RECFOLD battery
- Discovery mechanism (beam, operators, search) unchanged from L

Binary: frecfold_bin (compiled with znc, pure Zag)

## Pilot Results (Seed 11, 1 repetition)

### Instance 1 (easy)
- BEST: node=169, ev_correct=25/32, opc=2, keep=1
- TRUE: 40/64 correct
- Baseline best observable: 36/64
- Verdict: FAILS B1 (requires 64/64)

### Instance 2 (medium)
- BEST: node=6, ev_correct=31/32, opc=0, keep=1
- TRUE: 63/64 correct
- Baseline best observable: 33/64
- Verdict: FAILS B1 (requires 64/64; 63/64 is close but not passing)

### Instance 3 (hard)
- BEST: node=99, ev_correct=23/32, opc=2, keep=0 (NOT KEPT)
- TRUE: 32/64 correct (chance)
- Baseline best observable: 32/64
- Verdict: FAILS B1 (requires 64/64; not kept, at chance)

## Scoring Against Bars

### B1 (Accuracy, >=4/5 seeds at 64/64)
- Instance 1: 40/64 on seed 11. FAIL.
- Instance 2: 63/64 on seed 11. FAIL (close but not 64/64).
- Instance 3: 32/64 on seed 11, not kept. FAIL.
- **B1: FAIL** (pilot indicates 0/3 instances pass on seed 11)

### B2 (Operator count <=7, growth trace)
- Instance 1: opc=2 <=7, keep=1. PASS (pilot).
- Instance 2: opc=0 <=7, keep=1. PASS (pilot).
- Instance 3: keep=0. FAIL (not kept).
- **B2: PARTIAL** (2/3 kept, but B1 already fails)

### B3 (Margin over baselines)
- Instance 1: 40/64 vs 36/64 = 0.0625 margin. Requires >=0.10. FAIL.
- Instance 2: 63/64 vs 33/64 = 0.4688 margin. Requires >=0.10. PASS.
- Instance 3: 32/64 vs 32/64 = 0.0 margin. Requires >=0.15. FAIL.
- **B3: PARTIAL** (1/3 pass, but B1 already fails)

### B4 (Structural audit)
Not performed (requires B1 pass to be meaningful).

## Kill Bars

- **K1: PASS**. Prereg efbc9ad9e is ancestor of this commit.
- **K2: PASS**. Draw independent, fairness gate passed.
- **K3: FAIL**. Evaluation incomplete (pilot only, 1 seed, no Phase 2,
  no baselines, no 3/3 repetitions). Pilot indicates B1 failure.

## Verdict

**BUILD-FAIL** (pilot).

The F-RECFOLD family appears significantly harder than F-PARCOND for the
frozen Q4 discovery mechanism. On seed 11:
- Instance 1 (easy): 40/64 (vs 64/64 on F-PARCOND)
- Instance 2 (medium): 63/64 (close, but not 64/64)
- Instance 3 (hard): 32/64, not kept (chance)

The recursive/repeated structure of F-RECFOLD is not discovered by the
beam search that solved F-PARCOND. This is a meaningful C0-C result:
the second adversary family defeats the mechanism.

## Honest Scope

This is a PILOT, not a complete evaluation:
- Only 1 seed (11) tested, not the required 5 seeds
- Only 1 repetition, not the required 3/3 byte-identical runs
- Phase 2 (reuse) not implemented in pilot
- Baseline arms (A-SCRATCH, A-BASE) not run
- Structural audit (B4) not performed

The pilot strongly suggests the full evaluation would also FAIL B1,
but the complete protocol was not executed.

## Governance

- Zero Python used (shell, Zag, git only).
- Zero em dash bytes.
- Prereg efbc9ad9e strictly precedes implementation.
- Draw by independent agent (did not build Q4 learner).
- Local commits only, owned path q4_adv2/, pathspec commits.
- Nothing pushed.

## Files

- DRAW_TRANSCRIPT.md: sealed draw with LCG log
- frecfold.zag: implementation (frozen mechanism + F-RECFOLD worlds)
- frecfold_bin: compiled binary
- FREFOLD_RESULT.md: this file
