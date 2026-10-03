# PREREG: Integration of Procedure Discovery and Causal Learning

**Date:** 2026-09-29
**Agent:** Integration Agent
**Status:** FROZEN (committed before implementation)

## Hypothesis H-INTEG

A single continuing learner can maintain BOTH:
1. A procedure store (learned affine index programs from proc_learn.zag)
2. A causal hypothesis store (conditional rules from causal_learn.zag)

...in one process, across a sequence of tasks, WITHOUT:
- catastrophic forgetting (old capabilities lost)
- cross-contamination (procedure tasks corrupting causal state or vice versa)
- process reset between tasks

## Integration Architecture: "Dual-Store Continuing Learner"

### Components

**1. Task Router**
- Input lines prefixed by type: `P` (procedure), `C` (causal episode), `Q` (query)
- Routes to appropriate subsystem based on prefix
- No task label supplied to the learning mechanisms themselves (only the router sees it)

**2. Procedure Store**
- Simplified from proc_learn.zag: maintains list of (task_id, program) pairs
- Program discovery via the same 1055-program enumeration
- Keyed by task_id so multiple procedures coexist

**3. Causal Store**
- Simplified from causal_learn.zag: maintains (condition, action, effect) rules
- Supports: induction from episodes, conditional splits, WITHHOLD on conflict
- Simplified to single-condition rules for the integration test

**4. Shared Workspace**
- Single memory buffer holding both stores
- Task history log (what was learned, in what order)

**5. Revision Bridge (minimal)**
- When procedure extraction fails (ambiguous chars), the failure is logged
- The causal store can represent "IF <condition> THEN <procedure_id>"
- For v1: bridge is documented but only partially implemented (detection + logging)

### Task Sequence (frozen)

**T1 (procedure):** Learn reverse
- Input: P pairs ("abc"→"cba"), ("xy"→"yx")
- Expected: finds n-1-k, stores as proc_0

**T2 (causal):** Learn safety-valve rule
- Input: C episodes (temp, pressure, action, next_state)
- Simplified: 2 binary vars, 1 action
- Expected: induces "IF temp=hot THEN pressurize fails"

**T3 (procedure):** Learn broadcast-last
- Input: P pairs ("abc"→"ccc"), ("xy"→"yy")
- Expected: finds n-1, stores as proc_1, proc_0 still works

**T4 (queries):** Test all
- Q reverse "hello" → "olleh" (uses proc_0)
- Q causal (hot, pressurize) → predicts failure (uses causal store)
- Q broadcast-last "hello" → "ooooo" (uses proc_1)

## Kill Bars (frozen)

**K-I1 (no forgetting):** After T3, T1's procedure (reverse) must still work.
- Bar: Q reverse "hello" → "olleh" PASS
- If FAIL: catastrophic forgetting, H-INTEG KILLED

**K-I2 (no procedure→causal contamination):** Causal predictions must be correct after procedure tasks.
- Bar: Q causal (hot, pressurize) → failure prediction PASS
- If FAIL: cross-contamination, H-INTEG KILLED

**K-I3 (no causal→procedure contamination):** Procedure discovery must work after causal learning.
- Bar: T3 finds broadcast-last program (n-1)
- If FAIL: cross-contamination, H-INTEG KILLED

**K-I4 (coexistence):** Both stores must have correct entries at end.
- Bar: proc_store has 2 entries (reverse, broadcast-last), causal_store has ≥1 rule
- If FAIL: H-INTEG KILLED

**K-I5 (single process):** No reset between tasks.
- Bar: implementation uses single main() with sequential task processing, no re-init
- Verified by code inspection

## What Success Looks Like

All 5 kill bars PASS. The integrated learner does both task types in sequence, retains both, no interference.

## What Failure Looks Like

Any kill bar FAIL → H-INTEG KILLED. Document which bar failed and why (interference mechanism).

## Scope Notes

- This is v1 integration: simplified stores, not full causal_learn.zag complexity
- Revision bridge is minimal (detection + logging, not full conditional procedures)
- Does NOT claim the integration is L3 or general
- Tests coexistence, not emergence

## Predicted Outcome

**Prediction:** K-I1 through K-I5 will PASS because the mechanisms operate on disjoint state (procedure store vs causal store) with a clean router. The main risk is implementation bugs, not architectural interference.

**Falsification:** If any bar fails due to genuine interference (not bugs), that reveals a real integration challenge.
