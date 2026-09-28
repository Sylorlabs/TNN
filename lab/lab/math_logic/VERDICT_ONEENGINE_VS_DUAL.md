# VERDICT: ONE ENGINE vs DUAL ENGINE (2026-09-25)

## Head-to-head winner: DUAL (2 bars to 1)

Micah's ONE ENGINE bet is **FALSIFIED** on the measured kill bars.

## Kill bar results

| Bar | Battery | ONE | DUAL | Threshold | Verdict |
|-----|---------|-----|------|-----------|---------|
| KB1 interleaved | B3 (10) | 10/10 | 10/10 | ONE ≥7/10 pairwise wins | **FAIL** (0/10 wins) |
| KB2 DUAL | 20 pairs | — | 20/20 conf 1000>0 | ≥18/20 | **PASS** |
| KB2 ONE | 20 pairs | 20/20 conf 1>0, 0=0 | — | all pairs | **PASS** |
| KB3 transfer | B4 (15) | 15/15 | 15/15 | ONE≥10/15 AND DUAL≤6/15 | **FAIL** (DUAL 15/15) |
| KB4 audit | — | — | — | alpha>0.8, ONE mean ≥1.0 above | **VOID** (no 3 independent graders) |
| KB5 false rules | B5 (60) | 60 incorrect | 0 incorrect | ≥50% more → fragile/gullible | **FAIL for ONE** (ONE fragile) |
| KB6 scaling | B6 (50-step) | 52 derivs, 1.4s | 52 derivs, 3.5s | DUAL ≤1/10 ONE | **FAIL** (52 > 5.2) |

**Bars won:** ONE=1 (KB2-ONE), DUAL=2 (KB2-DUAL, KB5). VOID=1 (KB4).

## Fable predictions vs measured

- Fable P1 (ONE wins interleaved): **DID NOT HOLD**. Both 10/10.
- Fable P3 (ONE wins transfer, DUAL fragile): **DID NOT HOLD**. Both 15/15.
- Fable P6 (DUAL efficiency ≤1/10): **DID NOT HOLD**. Both 52 derivations.
- Unpredicted finding: DUAL's R (real H5) is MORE robust to false-rule
  contradiction than ONE. ONE withholds on all 60 B5 problems (sound but
  fragile); DUAL derives correctly via evidence weighing (0 incorrect).

## Determinism

- 3x external byte-identical reruns confirmed.
- ONE: SHA fefb19ca24e1f1debf92be1637a3a98d4b98c3e81993fa29bbd7a0cf0d8823e6
- DUAL: SHA c45564c60f0b797ce34fe43fd5494f041a369a5ef5ddecbd3d214af6a5a9103e
- Zero RNG in both. Pinned toolchain abed8aa1.

## Commits

- Schemas: a8a04d760e2561a40f3805e934d1d873802a6fee
- ONE source: e8823a512b77843e27e8c424f34ea97ecea41e96
- DUAL source: 9b5de653a7cf56cb8e096f09894fa35b5c8ee5e2
- B2/B3/B4 + sealed: 57a2c1d7da750a93296e7a0e91cbc3a608f112b5
- Evidence + ONE fix: 487f05f0b4fef2086f54cdf2b802ab182b925018

## Frozen docs verified

- PREREG_ONEENGINE_VS_DUAL.md @ b5136fdb: byte-match ✓
- FABLE_ARCHITECTURE.md @ ae99d2bb: byte-match ✓
- EFFORT_AUDIT.md @ bf6dc320 (full bf6dc320238187b1dbfd087e5fe3e0cac138aa14): byte-match ✓

## Limitations

- B1 (P01-P22 natural language): not directly runnable on formal engines.
  P01 smoke used formal analog (≤3-step MP).
- KB4 VOID: subagent cannot spawn 3 independent grader subagents.
- B2/B3/B4 authored as formal .form (not natural language).
- CEREMONY DEFECT #1: S_PBC hash 17 chars in COMMIT_SCHEMAS.md (spurious
  leading zero); engine asserts true FNV-1a-64 369efe53016bbe1a.
