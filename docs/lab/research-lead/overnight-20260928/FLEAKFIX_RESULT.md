# H-FLEAKFIX Result: F-LEAK Transactional Repair

**Hypothesis:** H-FLEAKFIX (prereg `f1f59882c`, frozen before implementation).
**Verdict:** SURVIVES. All four frozen kill bars PASS.
**Date:** 2026-09-29.

## The bug

F-LEAK, confirmed in H-STRESS (event E9 wasted 2 proc slots, 12 to 14):
when `bridge_learn` fails on a full bridge rule store, the return -1
path did not release the already stored subset procedures. A second
instance of the same failure class: when the second `proc_store`
fails (proc store full), the first stored slot is stranded.

## The fix

Transactional procedure slot allocation. On the bridge failure path,
every subset procedure slot allocated during the failed attempt is
rolled back via `proc_set_used(...,0)`, restoring the exact pre
allocation state. Either a bridge rule is created, or zero proc slots
change state. No new allocation policy, no eviction, no priority
scheme. Minimal repair.

Applied identically to all 4 files containing the bridge logic:
1. `bridge_learn.zag` (original H-BRIDGE reference)
2. `stress_learn.zag` (stress harness; where F-LEAK was confirmed)
3. `unified_learn.zag` (live unified learner)
4. `genbias_test.zag` (genbias test copy)

Freeing is sound: on the failure path no bridge rule was created, no
return value exposes the stranded slots, and nothing else can
reference them.

## Verification

### Negative control (unfixed code)

`fleaf_test.zag` built from the pre fix `bridge_learn.zag`
(`FLEAKFIX_NEGCONTROL_RAW.txt`):
- K-F1a: bridge-full attack: rc=-1, proc 2->4. **2 slots leaked.**
- K-F1b: proc-nearly-full attack: rc=-1, proc 15->16. **1 slot leaked.**
- K-F3: B-A6b: PASS (already fixed by the earlier B-A6b repair).
- Result: 1/3. The bug reproduces exactly as diagnosed.

### Fixed code (all kill bars)

**K-F1 (leak elimination): PASS.** `FLEAKFIX_RAW.txt`, 3/3:
- K-F1a: bridge-full attack: rc=-1, proc 2->2. Zero slots wasted.
- K-F1b: proc-nearly-full attack: rc=-1, proc 15->15. Zero slots wasted.
- K-F3: B-A6b 15-distractor: bridge rule 0 learned
  (IF input[0]==120 THEN proc0 ELSE proc1), 2/16 proc slots,
  dispatch verified (xqw->xxx, abc->ccc). PASS.

**K-F2 (no regression, bridge): PASS.** `BRIDGE_FLEAKFIX_REGRESS_RAW.txt`:
original 7/7 tests in `bridge_learn.zag` main all PASS on fixed code.
Task C direct, Task A bridge (pos=0,val=120), Task B bridge
(pos=1,val=113), all dispatches correct. H-BRIDGE still SURVIVES.

**K-F3 (no regression, B-A6b): PASS.** Covered in the fixed run above.

**K-F4 (determinism): PASS.** `fleaf_test.zag` output byte identical
across 3 runs (cmp verified). `bridge_learn.zag` main output byte
identical across 3 runs (cmp verified).

### No regression in dependent mechanisms

- `unified_learn.zag`: 9/9 PASS (H-UNIFIED SURVIVES).
- `stress_learn.zag`: 17/17 PASS (H-STRESS SURVIVES).
- `genbias_test.zag`: 6/6 PASS (H-GENBIAS SURVIVES).

## Classification

Bounded memory management correctness fix. The bridge failure path
is now atomic. This does not claim L3, does not change any learning
mechanism, and does not address NQ5 (single pass discovery copies) or
the remaining FDCR downgrades.

## Commits

- Prereg: `f1f59882c` (frozen before implementation).
- This result: fix in 4 files, `fleaf_test.zag`, raw outputs, this doc.

## Raw evidence

- `FLEAKFIX_NEGCONTROL_RAW.txt`: leak reproduces on unfixed code.
- `FLEAKFIX_RAW.txt`: 3/3 PASS on fixed code (representative of 3
  byte-identical runs).
- `BRIDGE_FLEAKFIX_REGRESS_RAW.txt`: 7/7 bridge regression PASS.
- `fleaf_test.zag`: the attack test source.

Pure Zag. No Python. Toolchain: znc 2026.07.0-dev.
