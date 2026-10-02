# Bridge Result: H-BRIDGE SURVIVES (7/7)

**Date:** 2026-09-29
**Status:** COMPLETE
**Branch:** tnn-native-lab
**Prereg:** PREREG_BRIDGE.md (commit 17d5de9f7, frozen before implementation)
**Implementation:** bridge_learn.zag
**Raw output:** BRIDGE_RAW_OUTPUT.txt (21 lines, byte-identical across runs)

## Verdict

**H-BRIDGE SURVIVES.**

The functional revision bridge works. When procedure discovery fails,
the bridge induces a conditional rule with a data-learned (position,
value) condition, preserves both sub-procedures, and dispatches correctly
at query time.

## Test Summary

### Task C (K-B1 control): simple broadcast-last

- Training: ("abc"->"ccc"), ("def"->"fff")
- Result: direct discovery succeeded, proc slot 0, **0 bridge rules created**.
- K-B1(control) PASS: bridge does not trigger on success.

### Task A: conditional on position 0

- Training: ("abc"->"ccc"), ("def"->"fff") [broadcast-last],
  ("xab"->"xxx"), ("xcd"->"xxx") [broadcast-first]
- Direct discovery failed (contradictory seqs). Bridge triggered.
- Learned: **IF input[0]==120 ('x') THEN proc3 ELSE proc4**
  - proc3 = [C0] (broadcast-first, verified: "abc"->"aaa")
  - proc4 = [N C1 SUB] (broadcast-last, verified: "abc"->"ccc")
- K-B1(trigger) PASS: exactly 1 bridge rule created.
- K-B2(part1) PASS: condition (pos=0, val=120) learned from data.
  Source inspection confirms bridge_learn contains no byte literals
  for condition values; values are read from training inputs at runtime.
- K-B3 PASS: both procedures independently applicable via proc_apply.
- K-B4(part1) PASS: bridge_apply("xqw")->"xxx", bridge_apply("zzz")->"zzz".

### Task B: conditional on position 1, different trigger (generality)

- Training: ("aqb"->"bbb"), ("cqd"->"ddd") [broadcast-last, input[1]=='q'],
  ("azb"->"aaa"), ("czd"->"ccc") [broadcast-first, input[1]!='q']
- Bridge skipped position 0 (splits failed discovery there) and found:
  **IF input[1]==113 ('q') THEN proc5 ELSE proc6**
- K-B2(part2) PASS: different position (1 vs 0) and different trigger
  value (113 vs 120) proves the mechanism generalizes; it is not
  hardcoded to pos=0 or val='x'.
- K-B4(part2) PASS: bridge_apply("aqz")->"zzz" (trigger -> last),
  bridge_apply("azq")->"aaa" (no trigger -> first).

## Kill Bar Assessment

| Bar | Result |
|-----|--------|
| K-B1 (trigger on failure only) | PASS (Task C: 0 rules; Task A: 1 rule) |
| K-B2 (condition learned, not hardcoded) | PASS (no literals; Task B different pos/val) |
| K-B3 (both procedures preserved) | PASS (independent proc_apply verified) |
| K-B4 (correct dispatch) | PASS (4/4 queries) |

**Result: 7/7. H-BRIDGE SURVIVES.**

## What This Proves

The H-REVISE architectural gap is now bridged for the binary-conditional
case. The procedure mechanism alone cannot represent "IF input[0]=='x'
THEN 0 ELSE n-1" (proven impossible in PROC_REVISION_RESULT.md). The
bridge provides:

1. **Failure detection:** bridge_learn detects when direct discovery
   returns -1 (no program fits all examples).
2. **Condition induction:** systematic search over (input position, byte
   value) pairs present in the training data. First working split wins.
3. **Procedure preservation:** both sub-procedures stored in the procedure
   store, independently usable.
4. **Conditional dispatch:** bridge_apply evaluates the learned condition
   at query time.

This is causal-style reasoning (IF condition THEN procedure) applied to
procedure selection. The condition is learned from data, not authored.

## Honest Limitations (per prereg scope notes)

1. **Binary conditions only.** One position, one value, two procedures.
   N-way splits and multi-condition rules are future work.
2. **Simple condition language.** (input[pos] == val) only. No ranges,
   conjunctions, or content patterns.
3. **No recursive bridging.** If subset discovery fails, returns -1.
4. **Short inputs default to ELSE.** Query inputs shorter than cond_pos
   use proc_false. Documented behavior.
5. **First working split wins.** Does not find minimal or canonical
   conditions. For Task A, tried v='a' and v='d' (wasting 2 proc slots)
   before finding v='x'.
6. **Proc slot waste.** Failed split attempts consume procedure slots.
   PROC_MAX increased to 16 to accommodate. A production version should
   use dry-run discovery before storing.

## Classification

**Bounded L2+ with functional revision bridge (binary-conditional).**

The bridge does not make the procedure mechanism L3. It provides a
specific, validated repair for the revision gap in the binary-conditional
case. Criterion 12 (revision) is now PARTIALLY satisfied: the system can
revise via conditional splitting, but cannot do general revision
(specialize, merge, deprecate with provenance).

## Files

- Prereg: PREREG_BRIDGE.md (frozen 17d5de9f7)
- Implementation: bridge_learn.zag
- Raw output: BRIDGE_RAW_OUTPUT.txt (deterministic, byte-identical)

## Pure Zag Compliance

Implementation, compilation, and execution in Zag only. No Python used.
Toolchain: znc 2026.07.0-dev (edition 2026).
