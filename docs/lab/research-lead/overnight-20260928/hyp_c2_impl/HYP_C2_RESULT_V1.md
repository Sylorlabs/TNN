# RESULT: Hypothesis C2 on Battery v1 (SUPERSEDED for T1/T4/T5)

Date: 2026-09-30.
C2 prereg: 01336fe83. Implementation: hyp_c2_impl/hyp_c2.zag (v1 version).
Runs: run1.txt, run2.txt, run3.txt (3/3 byte-identical).

## Status: SUPERSEDED for T1/T4/T5 per Battery v2 (611e8fa1f).

Per v2 sec 3.8: "v1 measurements stand as committed. Interpretations of
v1-T1/T4/T5 as conditional discriminators are SUPERSEDED (measurements are
not retracted). v1-T0/T2/T3 interpretations stand."

## v1 Results (3/3 byte-identical)

| Task | Predicted | Observed | Train | Evals | Repairs | Backtracks | Splits |
|------|-----------|----------|-------|-------|---------|------------|--------|
| T0 2x+1 | SOLVE | SOLVE | 9/9 | 229287 | 3 | 1 | 0 |
| T1 abs | SOLVE | SOLVE | 17/17 | 397613 | 3 | 1 | 0 |
| T2 mod3 | SOLVE | SOLVE | 17/17 | 105230 | 1 | 0 | 0 |
| T3 parity | SOLVE | BUDGET | - | 1000020 | 4 | 3 | 0 |
| T4 nabs | SOLVE | BUDGET | - | 1000001 | 8 | 5 | 0 |
| T5 fcomp | SOLVE | BUDGET | - | 1000005 | 11 | 7 | 1 |

## Key finding (triggered v2 redesign)

T1 SOLVED via straight-line repair, NOT via splits as predicted:
  REPAIR [IN0 NEG] c0=1 c1=9
  BACKTRACK [IN0 NEG]
  REPAIR [IN0 IN0 NEG] c0=1 c1=9
  REPAIR [IN0 SUB MOD] c0=9 c1=17
  SOLVE. Program: [IN0 IN0 NEG IN0 SUB MOD] (6 ops).

This program computes |x| using MOD: mod_nonneg(x, -2x) = |x| via the
truncated-division identity. This is "D's MOD trick" (v2 sec 1, Exhibit 1).
The v1 prediction "SOLVE via splits" is not confirmed in mechanism; the
outcome SOLVE is achieved via an arithmetic shortcut the designers did
not anticipate.

This finding, combined with D's independent discovery (e2ee0964e),
triggered the Battery v2 redesign: T1/T4/T5 are COMPROMISED as
conditional discriminators on the full VM. GENEXEC2-P removes the
shortcut class.

## Falsifiers (v1)

- C2-F1: NOT FIRED (T0 SOLVE).
- C2-F2: NOT FIRED (T4 not solved).
- C2-F3: NOT FIRED (max 1 split < 13 episodes).
- C2-F4: NOT FIRED (T0: 1 backtrack).
- **C2-F5: FIRES** (T3/T4/T5 exceed 1M).

## Note

v1 C2 implementation used the 34-symbol full-VM alphabet for all tasks.
v2 implementation (current hyp_c2.zag) uses 29-symbol P-VM alphabet for
T1/T4/T5. The v1 binary is not preserved; v1 results are from run*.txt.

**Builder label: C2-TESTED on v1 (C2-F5 FIRES; T1/T4/T5 SUPERSEDED by v2)**
