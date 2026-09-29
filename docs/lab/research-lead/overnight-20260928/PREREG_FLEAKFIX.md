# Preregistration: H-FLEAKFIX (F-LEAK transactional repair)

**Status:** FROZEN. This prereg precedes all implementation.
**Date:** 2026-09-29.
**Hypothesis ID:** H-FLEAKFIX.
**Parent finding:** F-LEAK, confirmed in H-STRESS (canonical state NQ4).

## 1. The bug

F-LEAK: when `bridge_learn` fails on a full bridge rule store, the
return -1 path does not release the already stored subset procedures.
Confirmed evidence: H-STRESS event E9 wasted 2 proc slots (12 to 14)
when bridge_learn failed on a full bridge store.

Exact location (identical pattern in 4 files):

```
let s1:i32=proc_store(W, pbase, prog1, nn1);   // consumes proc slot
if(s1>=0){
  let s2:i32=proc_store(W, pbase, prog2, nn2); // consumes proc slot
  if(s2>=0){
    let bs:i32=br_store(W, bbase, p, v, s1, s2); // -1 when bridge full
    if(bs>=0){
      ...
      return 1000+bs;
    }
  }
}
return -1;  // s1 and s2 remain marked used: LEAKED
```

A secondary instance of the same failure class: if the second
`proc_store` returns -1 (proc store full), the first stored slot s1
is also leaked on the failure path.

Files containing the pattern:
1. `bridge_learn.zag` (original H-BRIDGE reference)
2. `stress_learn.zag` (stress harness; where F-LEAK was confirmed)
3. `unified_learn.zag` (live unified learner)
4. `genbias_test.zag` (genbias test copy of the bridge logic)

## 2. The fix (transactional procedure slot allocation)

On the failure path, roll back (free) every subset procedure slot
allocated during the failed bridge attempt, so the attempt is atomic:
either a bridge rule is created, or zero proc slots change state.

```
let s1:i32=proc_store(W, pbase, prog1, nn1);
if(s1>=0){
  let s2:i32=proc_store(W, pbase, prog2, nn2);
  if(s2>=0){
    let bs:i32=br_store(W, bbase, p, v, s1, s2);
    if(bs>=0){
      ...
      return 1000+bs;
    }
    // F-LEAK FIX: bridge rule store full. Roll back both subset
    // procedures. Zero proc slots wasted on the failure path.
    proc_set_used(W, pbase, s2, 0);
    proc_set_used(W, pbase, s1, 0);
  } else {
    // Same failure class: second store failed, first slot stranded.
    // Roll it back.
    proc_set_used(W, pbase, s1, 0);
  }
}
return -1;
```

Freeing is sound: on this path no bridge rule was created, no return
value exposes s1/s2, and nothing else can reference the stranded
slots. `proc_set_used(...,0)` restores the exact pre allocation state
that `proc_store` checks via `proc_used`.

Scope: the identical patch is applied to all 4 files listed above.
No other logic changes. No new allocation policy, no eviction, no
priority scheme. This is a minimal transactional repair, not a memory
manager redesign.

## 3. Frozen kill bars

**K-F1 (leak elimination):** A dedicated F-LEAK attack test fills the
bridge rule store to 4/4 via `br_store`, records the proc used count,
then runs `bridge_learn` on a conditional task that would otherwise
succeed. Required: return is -1 AND proc used count is unchanged
(zero leaked slots). The same test also covers the secondary path:
proc store at 15/16 with a conditional task, verifying s1 is rolled
back when the second store fails.

**K-F2 (no regression, bridge):** The original 7/7 tests in
`bridge_learn.zag` main (Tasks C, A, B) still PASS after the fix.

**K-F3 (no regression, B-A6b):** The 15 distractor B-A6b attack still
succeeds: bridge rule created, 2/16 proc slots used, dispatch
verified.

**K-F4 (determinism):** All test outputs byte identical across 3 runs
(cmp verified).

Verdict rule: H-FLEAKFIX SURVIVES iff K-F1 through K-F4 all PASS.
Any single bar failure KILLS the hypothesis. Bars are frozen; they
will not be weakened, redefined, or retroactively altered.

## 4. Test plan

1. Write `fleaf_test.zag`: standalone reproduction containing the
   bridge machinery plus a main that runs the K-F1 attack (bridge full
   and proc nearly full cases) and the K-F3 B-A6b scenario.
2. Run `fleaf_test.zag` against UNFIXED code: confirm the leak
   reproduces (proc count increases on the failed attempt). This is
   the negative control.
3. Apply the fix to all 4 files.
4. Re run `fleaf_test.zag`: K-F1 must show zero slot change.
5. Run `bridge_learn.zag` main: K-F2 7/7.
6. K-F3 from the same test binary.
7. Each test run 3 times; cmp the raw outputs for K-F4.
8. Commit: this prereg (frozen), the fix, the test, raw outputs,
   and FLEAKFIX_RESULT.md.

## 5. Constraints

Pure Zag. No Python anywhere, including analysis and scratch tooling.
Deterministic: no wall clock, no randomness, no uninitialized reads
in the test paths. Toolchain pinned: znc 2026.07.0-dev.

## 6. What failure looks like

- The attack still leaks slots after the patch (rollback incomplete
  or wrong slots freed).
- Any of the 7/7 bridge tests change behavior (overcorrection:
  freeing slots that a live rule references).
- Nondeterministic output across runs.

## 7. What success does NOT claim

This repair does not claim L3, does not change any learning
mechanism, and does not address NQ5 (single pass discovery copies)
or the remaining FDCR downgrades. It is a bounded memory management
correctness fix: the failure path becomes atomic.
