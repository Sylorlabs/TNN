# GENEXEC2 Evidence (2026-09-30)

## Build
- Toolchain: znc 2026.07.0-dev (edition 2026)
- Binary: /tmp/genexec2_bin (85475 bytes)
- Pure Zag: yes. No Python used.
- Em-dash bytes in source: 0.

## Determinism
Three runs, byte-identical:
- cksum: 970587458 493 (all three)
- diff run1 vs run2: identical
- diff run2 vs run3: identical

## Raw Output (run1, representative)
```
GENEXEC2
TASK 0 phase=1 exact=0 len=1 prog=[PUSH:1]
TASK 1 phase=3 exact=1 len=8 prog=[IN0 PUSH:-1 GT JZ:6 IN0 JMP:8 IN0 NEG]
  probe x=0 k=-1 cmp=GT
  PROMOTE FRAG0
  HELDOUT 8/8
TASK 2 phase=1 exact=0 len=1 prog=[PUSH:0]
TASK 3 phase=1 exact=0 len=1 prog=[PUSH:1]
TASK 4 phase=1 exact=0 len=3 prog=[IN0 PUSH:2 MOD]
TASK 5 phase=1 exact=0 len=1 prog=[PUSH:2]
NLIB 1
T4_CALLS_TO_FRAG1 0
T5_CALLS_TO_FRAG1 0
ABLATION
ABL_TASK 4 exact=0 score=6/13 len=3
ABL_TASK 5 exact=0 score=3/13 len=1
DONE
```

## Kill Bar Verdicts

### K-A (source audit)
- Source contains generic VM (ops 0-20) and generic learner (beam, probe, promote).
- No dedicated semantic cases for ABS, PARITY, etc.
- Learner state: FRAG0 (T1 solution) stored as instruction bytes in lib_buf.
- VERDICT: PASS (architecture is generic; semantics reside in learner-created bytes).

### K-B (T1 conditional assembly)
- T1 solved via P3 (phase=3), program len=8.
- P1 max length is 12. 8 is NOT > 12.
- Trace shows probe (x>-1) and assembled branches.
- VERDICT: FAIL (program length 8 does not exceed P1 max 12).

### K-C (T1-T5 solved)
- T0: exact=0 FAIL
- T1: exact=1 PASS
- T2: exact=0 FAIL
- T3: exact=0 FAIL
- T4: exact=0 FAIL
- T5: exact=0 FAIL
- VERDICT: FAIL (only 1/6 tasks solved).

### K-D1 (reuse constructed)
- T4 CALLs to FRAG1 (ABS): 0 (FRAG1 does not exist; only FRAG0 exists)
- T5 CALLs to FRAG1: 0
- VERDICT: FAIL.

### K-D2 (ablation)
- With CALL disabled, T4 score 6/13, T5 score 3/13.
- But T4/T5 were not solved with CALL enabled either, so ablation is moot.
- VERDICT: FAIL (no advantage to destroy).

### K-P1 (persistence)
- FRAG0 is T1's solution bytes, stored in library.
- T4/T5 do not CALL it.
- VERDICT: FAIL (no reuse demonstrated).

## Summary
BUILD-FAIL. The P1 beam search systematically fails to find simple
arithmetic programs (2x+1, x mod 3, parity) due to sparse-reward
pruning of solution prefixes. P3 succeeds on T1 (|x|) by decomposing
into easy subset problems, but P1/P2 do not solve T0, T2-T5. Only 1 of
6 tasks solved; no reuse demonstrated.

C0-C remains partial (and in this run, largely unmet) pending a
working P1 search mechanism.
