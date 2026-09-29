# Preregistration: Functional Revision Bridge (H-BRIDGE)

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation)
**Branch:** tnn-native-lab
**Builds on:** integ_learn.zag (commit 492f5b01d), PROC_REVISION_RESULT.md (H-REVISE KILLED)

## Background

The procedure mechanism (1055-program affine index search) cannot revise.
H-REVISE was KILLED with a mathematical impossibility proof: no function
P(k,n)->index can satisfy contradictory requirements for identical (k,n)
inputs. The five revision capabilities (detection, diagnosis, conditional
representation, revision operators, procedure memory) are all absent.

The causal mechanism learns conditional rules (IF condition THEN effect)
and revises via contests. Integration v1 coexists both in one process
but the revision bridge is "scaffolding only, not functional."

## Hypothesis H-BRIDGE

When procedure discovery fails on a training set, a functional bridge can:

1. Detect the failure (extraction VACUOUS or no program fits all examples).
2. Invoke condition induction: search over (input position, byte value)
   pairs to find a split where each subset independently discovers a
   procedure.
3. Store a bridge rule: IF input[pos]==val THEN proc_A ELSE proc_B.
4. At query time, evaluate the condition and dispatch to the correct
   procedure.

The condition is LEARNED via search, not hardcoded. The bridge_learn
function contains no byte literals for condition values; it discovers
(pos, val) from the training data.

## Test Design

### Task A (conditional on position 0)

Training pairs:
- ("abc" -> "ccc")   [broadcast-last]
- ("def" -> "fff")   [broadcast-last]
- ("xab" -> "xxx")   [broadcast-first, trigger]
- ("xcd" -> "xxx")   [broadcast-first, trigger]

Expected: direct discovery fails (contradictory seqs [2,2,2] vs [0,0,0]).
Bridge searches positions and values, finds (pos=0, val='x'):
- Subset input[0]=='x': [("xab"->"xxx"),("xcd"->"xxx")] -> [C0]
- Subset input[0]!='x': [("abc"->"ccc"),("def"->"fff")] -> [N C1 SUB]

### Task B (conditional on position 1, different trigger)

Training pairs:
- ("aqb" -> "bbb")   [broadcast-last, input[1]=='q']
- ("cqd" -> "ddd")   [broadcast-last, input[1]=='q']
- ("azb" -> "aaa")   [broadcast-first, input[1]!='q']
- ("czd" -> "ccc")   [broadcast-first, input[1]!='q']

Expected: bridge finds (pos=1, val='q'). This proves the algorithm
generalizes beyond position 0 and beyond the 'x' trigger. If the
implementation hardcoded pos=0 or val='x', Task B fails.

### Task C (K-B1 control: no bridge needed)

Training pairs:
- ("abc" -> "ccc")
- ("def" -> "fff")

Expected: direct discovery succeeds ([N C1 SUB]). Bridge is NOT
triggered. Zero bridge rules created.

## Kill Bars (frozen)

**K-B1: Bridge triggers on failure only.**
- Task C: bridge_learn returns procedure slot (>=0, <1000), bridge rule
  count remains 0. If a bridge rule is created for Task C, K-B1 FAILS.
- Task A: bridge_learn returns bridge slot (>=1000), exactly 1 bridge
  rule created. If no bridge rule, K-B1 FAILS.

**K-B2: Condition is learned, not hardcoded.**
- The bridge_learn function source contains no byte literal equal to
  the trigger value used in Task A, and no literal position constant
  used as the condition position. Verified by source inspection.
- Task B must also succeed with a DIFFERENT position (1) and DIFFERENT
  trigger value ('q'). If Task B fails while Task A succeeds, the
  condition mechanism is fixture-specific and K-B2 FAILS.

**K-B3: Both procedures preserved.**
- After Task A bridge learning, proc_apply on the stored broadcast-last
  slot correctly maps "zzz" -> "zzz", and proc_apply on the stored
  broadcast-first slot correctly maps "zzz" -> "zzz" (first char).
  If either slot was overwritten or corrupted, K-B3 FAILS.

**K-B4: Correct procedure selected at query.**
- bridge_apply("xqw") == "xxx" (trigger -> broadcast-first)
- bridge_apply("zzz") == "zzz" (no trigger -> broadcast-last)
- Task B: bridge_apply("aqz") == "zzz" (trigger 'q' at pos 1 ->
  broadcast-last); bridge_apply("azq") == "aaa" (no trigger ->
  broadcast-first)
- 4/4 required. Each failure kills K-B4.

## What Counts as Success

H-BRIDGE SURVIVES iff K-B1 through K-B4 all PASS.

## What Counts as Failure

- Bridge does not trigger on Task A (returns -1): H-BRIDGE KILLED.
- Condition hardcoded (Task B fails): H-BRIDGE KILLED.
- Wrong dispatch at query: H-BRIDGE KILLED.

## Honest Scope Notes (pre-registered)

1. The bridge handles binary conditions (one position, one value,
   two procedures). N-way splits and multi-condition rules are out
   of scope for v1.
2. The condition language is (input[pos] == val). Richer conditions
   (ranges, conjunctions, content patterns) are future work.
3. If subset discovery fails, the bridge returns -1 (no recursive
   bridging in v1).
4. Query inputs shorter than cond_pos default to the ELSE procedure.
   Documented, not fixed in v1.
5. The bridge picks the FIRST working (pos, val) in search order.
   It does not find minimal or canonical conditions.

## Pure Zag Compliance

Prereg, implementation, compilation, and execution in Zag only.
No Python in any loop artifact. Toolchain: znc 2026.07.0-dev.

## Commit Order

1. This prereg (frozen).
2. Implementation (bridge_learn.zag).
3. Results.
