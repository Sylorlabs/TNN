# Preregistration: H-REVISE3 (Revision Repair v3)

**Date:** 2026-09-29
**Researcher:** H-REVISE3 Researcher (subagent)
**Status:** FROZEN (commit before any implementation file)
**Branch:** tnn-native-lab

## Hypothesis

H-REVISE3: The three architectural failure classes demonstrated by the
H-REVISE2 red team (F-RV1 chained revision impossible, F-RV2 diagnosis
locks onto incidental features, F-RV3 spurious UNRESOLVABLE on
mixed-length passing sets) are repairable within the versioned
conditional dispatch architecture, without changing the (position,
equality) condition vocabulary or the affine sub-program space.

## Background

H-REVISE2 SURVIVES (18/18) on its frozen bars: single revision event,
lowest discriminating position, uniform-length passing set. The
independent red team (REVISE2_ADV_RESULT.md) DOWNGRADED it with three
succeeding attacks:

- X-RV1 (F-RV1): `vs_revise` unconditionally overwrites a single
  condition slot and program slot. A second revision destroys the first.
  The "version store" is a single conditional slot, not a version memory.
- X-RV2 (F-RV2): diagnosis returns the lowest discriminating position.
  With hidden true rule "broadcast input[1] iff input contains 'q'",
  counterexample ("xqc"->"qqq") is diagnosed as (0,120), ignoring the
  causally relevant 'q' at position 1. Held-out misgeneralizes both ways
  (0/2).
- X-RV3 (F-RV3): the length guard vetoes a position when ANY passing
  input is shorter. With passing set ("abc","de","ghi","jkl"),
  counterexample ("abx"->"aaa") yields -1 (UNRESOLVABLE) although a
  bounds-respecting diagnosis finds (2,120).

X-RV4 (source audit) FAILED: no spoofing. The frozen K-RV1..K-RV5 bars
were earned and are NOT retroactively altered.

## Repairs (frozen design)

**R1 (F-RV1): appendable condition list.** The version store becomes a
condition list with up to 4 revision slots. `vs_revise` APPENDS a new
(slot: cond_pos, cond_val, program); it never overwrites. Dispatch
checks slots most-recent-first (stated rule: the newest revision wins
ties). P0 is slot 0 and is never moved.

**R2 (F-RV2): scored diagnosis over all discriminating positions.**
Diagnosis no longer stops at the lowest discriminating position. It
collects every discriminating (pos,val) and scores each:

- +1 output-relevance: the candidate byte appears in the
  counterexample's expected output.
- +1 program-consistency: the candidate position appears in the
  extraction index sequence of the counterexample (positions the
  discovered program reads).
- Tie-break: lowest position (preserves H-REVISE2 behavior on ties).

The discovery of P1 from the counterexample subset happens BEFORE
final diagnosis, so the program-consistency signal is available. This
is a stated heuristic ranking, not a guaranteed causal identification.
The explicit assumption: the causally relevant feature is among the
discriminating positions, and output-relevance plus program-consistency
is a better selector than position order alone. Conjunctions and
features outside (position, equality) remain out of scope.

**R3 (F-RV3): bounds-respecting length guard.** A passing input shorter
than position p is vacuous at p (skipped), not vetoing. Only passing
inputs with length > p participate in the discrimination test at p.

## Experiment Design

Implementation: `revise3.zag` (pure Zag), self-contained. Mechanism
functions copied from `revise2.zag`; version store, diagnosis, and
`main()` replaced per the frozen repairs above.

Phase A (learn): training ("abc"->"ccc"), ("def"->"fff"),
("ghi"->"iii"). Discover P0. Expect [N C1 SUB] (broadcast-last).

Phase B (monitor): ("jkl"->"lll") matches P0. ("xab"->"xxx") vs P0
prediction "bbb": DETECT.

Phase C (diagnose): scored diagnosis of "xab" against passing set
("abc","def","ghi","jkl"). Only (0,120) discriminates. Expect
(0,120).

Phase D (revise): discover P1 from {("xab"->"xxx")}. Expect
[N N SUB]. Append slot 1: IF input[0]==120 THEN P1. vcount=1.

Phase E (verify): 5/5 on ("abc","def","ghi","jkl","xab").

Phase F (withhold): ("abc"->"aaa") detected; scored diagnosis finds no
discriminating position; UNRESOLVABLE; P0 and version store unchanged.

Phase G (chained, K-RV3-1): R2 counterexample ("yzb"->"yyy"). Under
slot-1 dispatch P0 predicts "bbb": DETECT. Scored diagnosis against
the original passing set: candidates (0,121) and (1,122); (0,121)
scores higher (output-relevance + program-consistency). Discover P2
from {("yzb"->"yyy")}; expect [N N SUB]. Append slot 2:
IF input[0]==121 THEN P2. vcount=2. Verify BOTH ("xab"->"xxx") (via
slot 1) and ("yzb"->"yyy") (via slot 2) PASS.

Phase H ('q' case, K-RV3-2): fresh store VS2 with P0 only.
Counterexample ("xqc"->"qqq"): P0 predicts "ccc": DETECT. Scored
diagnosis: candidates (0,120) score 0 and (1,113) score 2
(output-relevance: 113 in "qqq"; program-consistency: extraction seq
is [1,1,1]). Expect diagnosis (1,113), NOT (0,120). Discover P1;
expect [N C2 SUB] (broadcast index 1). Revise:
IF input[1]==113 THEN P1 ELSE P0. Held-out: ("xbc"->"ccc") PASS
(condition does not fire; P0) and ("aqc"->"qqq") PASS (condition
fires; P1).

Phase I (mixed-length, K-RV3-3): fresh store VS3 with P0 only. Passing
set ("abc","de","ghi","jkl"); "de"->"ee" sanity-confirmed under P0.
Counterexample ("abx"->"aaa"): P0 predicts "xxx": DETECT. Scored
diagnosis must NOT return -1; bounds-respecting scan finds (2,120)
("de" is vacuous at position 2). Discover P1; expect [N N SUB].
Revise: IF input[2]==120 THEN P1 ELSE P0. Verify ("abx"->"aaa") PASS.

## Frozen Kill Bars

K-RV3-1 (chained revision works): after Phase G, vcount=2 and both
("xab"->"xxx") and ("yzb"->"yyy") verify PASS. The R1 case is not
destroyed by R2.

K-RV3-2 (diagnosis handles the 'q' case): Phase H diagnosis returns
(1,113) and both held-out cases ("xbc"->"ccc", ("aqc"->"qqq")) PASS.

K-RV3-3 (UNRESOLVABLE does not misfire): Phase I diagnosis returns
(2,120) (not -1) and ("abx"->"aaa") verifies PASS after revision.

K-RV3-4 (original H-REVISE2 tests preserved): Phase E 5/5 PASS and
Phase F honest withhold (UNRESOLVABLE emitted, P0 intact, version
store unchanged).

K-RV3-5 (determinism): two consecutive runs produce byte-identical raw
output (verified with cmp).

## Failure Modes (honest)

- If Phase H diagnosis returns (0,120) instead of (1,113), K-RV3-2
  FAILS and the scored-diagnosis repair is insufficient; the claim
  drops to "explicitly scoped to positional" per the downgrade.
- If chained verification fails, K-RV3-1 FAILS; the appendable store
  does not compose.
- If any bar fails, H-REVISE3 is KILLED or DOWNGRADED per the evidence.
- The scored diagnosis is a heuristic. A red team may construct a case
  where output-relevance and program-consistency jointly select an
  incidental feature (e.g. the incidental byte also appears in the
  output). Such a finding would bound, not necessarily kill, the
  repair.

## What This Would Show

If all five bars pass: chained revision composes, diagnosis selects
the causally relevant feature on the demonstrated gaming fixture, and
the withhold path is complete (no spurious UNRESOLVABLE). L3 criterion
12 would hold for chained single-condition revisions under the stated
scoring assumption. Classification remains bounded L2+ revision, not
general L3: single (position, equality) conditions, affine
sub-programs, heuristic (not guaranteed) causal diagnosis.

## Pure Zag Compliance

Implementation, compilation, and execution in Zag only. No Python
anywhere. Toolchain: znc 2026.07.0-dev (edition 2026).

## Documentation Style

No em dashes in any loop documentation.
