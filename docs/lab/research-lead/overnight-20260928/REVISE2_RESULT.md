# H-REVISE2 Result: Versioned Conditional Dispatch Revision

**Date:** 2026-09-29
**Status:** COMPLETE
**Researcher:** Procedure Revision v2 Researcher (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_REVISE2.md (3f582bb46, frozen before implementation)
**Amendment:** PREREG_REVISE2_AMEND1.md (66e84347d, frozen before implementation;
  corrected P1 expectation from [C0] to [N N SUB] per the frozen N-first
  enumeration order; no kill bar impact)
**Implementation:** revise2.zag (pure Zag, self-contained)
**Raw output:** revise2_raw.txt (35 lines, byte-identical across two runs)

## Verdict

**H-REVISE2 SURVIVES (18/18).**

## What was built

A continuing procedure learner with a monitor/diagnose/version loop,
implemented in self-contained pure Zag:

1. **Monitor.** The discovered program P0 stays deployed. Every new
   observation is checked against P0's prediction. Mismatch raises a
   DETECT event autonomously. No human trigger.
2. **Diagnose.** On detection, the learner scans input positions for the
   lowest position where the counterexample's byte differs from every
   passing input's byte at that position. Values come from the data; the
   code contains no byte literals for condition values.
3. **Versioned revision.** P0 is preserved. P1 is discovered from the
   counterexample subset with the same N-first discovery. The version
   store holds both programs plus a dispatch condition:
   IF input[pos]==val THEN P1 ELSE P0. Revised signature is
   (k,n,input)->index, not P(k,n)->index.
4. **Honest withhold.** If no discriminating feature exists (same input,
   contradictory output), the learner emits UNRESOLVABLE, leaves P0 and
   the version store untouched.

## Test trace (from revise2_raw.txt)

- Phase A: P0 = [[1,255,255],[3,255,255],[6,0,1]] = [N C1 SUB] (n-1,
  broadcast-last), learned from ("abc"->"ccc"), ("def"->"fff"),
  ("ghi"->"iii").
- Phase B1: ("jkl"->"lll") matches P0. No revision.
- Phase B2: ("xab"->"xxx") vs P0 prediction "bbb". DETECT (autonomous).
- Phase C: DIAGNOSE pos=0 val=120 ('x'; no passing input has 120 at
  position 0).
- Phase D: P1 = [[1,255,255],[1,255,255],[6,0,1]] = [N N SUB] (constant 0),
  discovered from {("xab"->"xxx")}. Versioned: IF input[0]==120 THEN P1
  ELSE P0. P0 preserved.
- Phase E: 5/5 VERIFY PASS (abc, def, ghi, jkl, xab).
- Phase F: ("abc"->"aaa") detected (predicted "ccc"); no discriminating
  feature ("abc" is itself a training input); UNRESOLVABLE emitted; P0
  still maps "abc"->"ccc"; version store unchanged.

## Kill bar assessment

**K-RV1 (revision works): PASS.** Versioned dispatch produces the expected
output on all five Phase E cases: 5/5 VERIFY PASS in the raw output.

**K-RV2 (proof sidestepped): PASS.** The stored artifact is two distinct
programs ([N C1 SUB] vs [N N SUB], different bytes) plus a condition
record (pos=0, val=120), shown in the VSTORE dump. It is not a single
affine P(k,n)->index. The H-REVISE impossibility proof (no single P(k,n)
satisfies P(k,3)=2 and P(k,3)=0) cannot apply because no such single
function is claimed; P0 and P1 operate on disjoint input domains selected
by content.

**K-RV3 (white-box trace): PASS.** The raw output contains, in order: LEARN
P0 with encoding, MONITOR B1, DETECT B2 with the failing pair and the
wrong prediction, DIAGNOSE with (pos=0, val=120), LEARN P1 with encoding,
REVISE with the dispatch rule, the full VSTORE dump, five VERIFY lines,
and the Phase F DETECT / UNRESOLVABLE / WITHHOLD lines.

**K-RV4 (determinism): PASS.** Two consecutive runs produce byte-identical
raw output (verified with cmp).

**K-RV5 (honest withhold): PASS.** On the unresolvable counterexample the
raw output contains UNRESOLVABLE, the version store dump is unchanged
(vcount=1, same cond), and P0 still maps "abc"->"ccc".

## Relation to H-REVISE (killed)

H-REVISE remains killed and its proof stands: the one-shot batch-search
architecture cannot revise. H-REVISE2 does not overturn that verdict; it
demonstrates a different architecture (continuing learner with
monitor/diagnose/version) that was not tested by H-REVISE. The five
capabilities H-REVISE found absent are now present in bounded form:
detection (monitor loop), diagnosis (content-feature scan), conditional
representation (versioned dispatch), revision operator (version/specialize),
procedure memory (version store).

## Relation to the Bridge (H-BRIDGE)

The Bridge triggers when direct discovery FAILS on the full training set
at learning time. H-REVISE2 triggers when discovery SUCCEEDED, a program
is deployed, and a LATER counterexample contradicts it at use time.
Complementary, not redundant: fallback at learning time vs self-correction
at use time.

## Classification

Bounded L2+ revision (single binary content condition; affine
sub-programs; position/equality vocabulary only). This satisfies L3
criterion 12 (revisable after a counterexample) for the bounded case
tested. It does not claim general revision: multi-condition, relational,
or non-affine revisions are untested. Procedure discovery as a whole moves
from 11/12 toward 12/12 on the tested revision scenario; the remaining
distance to full L3 is the generality of the revision, not its existence.

## Boundaries

- Condition vocabulary is (position, equality) only, inherited from the
  Bridge's split search. Ranges, conjunctions, inequalities untested.
- One revision event tested. Chained revisions (P2, P3, ...) untested.
- The monitor checks only exact output match; graded or partial mismatch
  untested.
- Diagnosis picks the lowest discriminating position; ties beyond position
  order untested.

## Pure Zag compliance

Implementation, compilation (znc 2026.07.0-dev), and execution in Zag only.
No Python used anywhere.

## Test accounting note (disclosed)

The first run scored 17/18 due to a test-harness accounting omission: the
Phase F DETECT event incremented ntest but not npass. The mechanism
behaved correctly in that run (detection occurred and was emitted). The
harness was fixed (one line), the source recompiled, and the committed raw
output is the corrected 18/18 run. Both the pre-fix and post-fix sources
are in git history; the fix touched only test accounting, not the
mechanism.
