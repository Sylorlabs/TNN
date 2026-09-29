# Integration Result: H-INTEG SURVIVES

**Date:** 2026-09-29
**Prereg:** PREREG_INTEGRATION.md (commit 3be18d8ad)
**Implementation:** integ_learn.zag
**Raw output:** INTEG_RAW_OUTPUT.txt
**Verdict:** H-INTEG SURVIVES (5/5)

## What Was Built

**Dual-store continuing learner** in pure Zag (single file, single process):
- **Task router:** P/C/Q line prefixes route to procedure/causal/query handlers
- **Procedure store:** 8 slots, each holds a learned affine index program (1055-program enumeration)
- **Causal store:** 16 rules, each (condition, action, effect) with conflict detection
- **Shared workspace:** Single 64KB buffer, sequential task processing, no re-init

## Task Sequence Executed

**T1:** Learned reverse from ("abc"→"cba"), ("xy"→"yx")
- Found n-1-k, stored at procedure slot 0

**T2:** Learned safety-valve from 4 causal episodes
- R0: IF temp==cold AND pressurize THEN pressure:=high
- R1: IF temp==hot AND pressurize THEN pressure:=low (stays low)

**T3:** Learned broadcast-last from ("abc"→"ccc"), ("xy"→"yy")
- Found n-1, stored at procedure slot 1
- Slot 0 (reverse) undisturbed

**T4:** All queries passed

## Kill Bar Verdicts

| Bar | Test | Result |
|-----|------|--------|
| K-I1 (no forgetting) | Q reverse "hello"→"olleh" after T3 | PASS |
| K-I2 (no proc→causal contamination) | Q causal (hot,low)→low correct | PASS |
| K-I3 (no causal→proc contamination) | T3 finds broadcast-last after T2 | PASS |
| K-I4 (coexistence) | proc=2, causal=2 at end | PASS |
| K-I5 (single process) | Code inspection: single main(), sequential | PASS |

**Result: 5/5 PASS. H-INTEG SURVIVES.**

## Key Finding: No Interference

The two mechanisms coexist cleanly because they operate on **disjoint state**:
- Procedure store: slots 0-7, program bytes
- Causal store: slots 0-15, rule tuples
- Router ensures task types never touch the wrong store

There is no shared representation to corrupt. This is architectural separation, not learned separation.

## Honest Limitations

1. **Simplified stores.** The causal store is a simplified version (single-condition rules, no splits/merges/contests). The full causal_learn.zag machinery was not integrated.

2. **Explicit router.** Task types are marked with P/C/Q prefixes. The learner does not infer task type; the router does. A true continuing learner would need to discover this.

3. **Revision bridge minimal.** The prereg promised detection + logging of procedure failures. The implementation logs failures (returns -1) but does not invoke causal machinery to handle them. The bridge is architectural scaffolding, not functional.

4. **No stress test.** Only 2 procedures and 2 causal rules. Not tested: store overflow, many-task sequences, interleaved tasks.

5. **Disjoint is easy.** The hard integration problem (shared representations, mutual benefit) is not addressed. This proves coexistence, not synergy.

## What This Proves

A single Zag process can maintain multiple learned capabilities across a task sequence without reset, without forgetting, and without interference — when the capabilities use separate state.

## What This Does NOT Prove

- That the mechanisms benefit each other (no synergy demonstrated)
- That the learner can handle unmarked task boundaries
- That revision works across mechanisms (bridge not functional)
- That this scales to dozens of capabilities

## Next Steps

1. **Functional revision bridge:** When procedure extraction fails, invoke causal conditional learning to create "IF <condition> THEN <procedure>" rules.
2. **Learned routing:** Remove P/C/Q prefixes; let the learner infer task type from input structure.
3. **Full causal integration:** Port the split/merge/contest machinery from causal_learn.zag.
4. **Stress test:** 10+ tasks, interleaved, store pressure.

## Classification

**Bounded L2 integration.** Two validated L2 mechanisms coexist in one process. This is infrastructure for a continuing learner, not a cognitive architecture breakthrough. The value is in proving the engineering path, not in claiming intelligence.
