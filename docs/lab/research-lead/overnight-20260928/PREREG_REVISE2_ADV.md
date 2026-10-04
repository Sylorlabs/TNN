# Preregistration: H-REVISE2 Adversary (X-RV1..X-RV4)

**Date:** 2026-09-29
**Researcher:** H-REVISE2 Red Team (subagent)
**Status:** FROZEN (committed before any attack execution)
**Branch:** tnn-native-lab
**Target:** H-REVISE2 SURVIVES (18/18), `revise2.zag`, prereg 3f582bb46,
amendment 66e84347d, result `REVISE2_RESULT.md`

## Mission

Assume the H-REVISE2 claim is false. Attack the versioned conditional
dispatch revision mechanism on four fronts. The mechanism under test is
the verbatim code from `revise2.zag` (program machinery, version store,
diagnosis); only `main()` is replaced by attack scenarios.

## Background facts used to design attacks (from source read, no execution)

- `vs_revise` unconditionally writes vcount=1 and overwrites the single
  condition slot (pos, val) and the P1 program slot. The store layout has
  room for exactly one condition and two programs.
- `diagnose` returns the LOWEST position p where the counterexample byte
  differs from every passing input byte at p. It performs no causal
  analysis; any incidental difference at a lower position wins.
- `diagnose` skips position p entirely if ANY passing input has length
  <= p (the length guard vetoes the position for all inputs).
- `vs_apply` checks exactly one condition: IF input[pos]==val THEN P1
  ELSE P0.

## Attack X-RV1: Chained revision

**Setup.** Phase A: train P0 on ("abc"->"ccc"), ("def"->"fff"),
("ghi"->"iii") (P0 = [N C1 SUB], broadcast-last). Passing set for
diagnosis: ("abc","def","ghi","jkl").
Revision R1: counterexample ("xab"->"xxx"). Expect DETECT, diagnose
(0,120), P1 = [N N SUB] (broadcast-first), versioned IF input[0]==120
THEN P1 ELSE P0. Verify "xab"->"xxx" passes.
Revision R2: new counterexample ("yza"->"aaa"). Under the R1 dispatch,
"yza" routes to P0 (input[0]='y' != 120), P0 predicts "zzz", mismatch,
expect DETECT. Diagnose "yza" against the passing set: expect (0,121).
Discover P2 from {("yza"->"aaa")}. Apply vs_revise with (0,121).
Then verify the R1 case "xab"->"xxx" again.

**Kill criterion.** If after R2 the R1 case "xab"->"xxx" FAILS (routes to
P0 and produces "bbb"), X-RV1 SUCCEEDS: the version store is
single-slot overwrite, not a version memory; the second revision
destroys the first. Verdict impact: H-REVISE2 DOWNGRADED to
"single revision event only; chained revision not supported."

**If the R1 case still passes** (store somehow chains), X-RV1 FAILS.

## Attack X-RV2: Diagnosis gaming (incidental-feature lock-in)

**Setup.** Same P0 and passing set as X-RV1. Hidden true rule (unknown
to the mechanism): broadcast-first iff the input contains 'q', else
broadcast-last. Counterexample ("xqc"->"qqq"): P0 predicts "ccc",
mismatch, expect DETECT. Diagnosis scans positions: p=0, 'x'=120,
differs from all passing bytes at p=0, so it returns (0,120) even
though the causally relevant feature is 'q' at p=1. P1 is discovered
from {("xqc"->"qqq")} (broadcast of position 1). Versioned IF
input[0]==120 THEN P1 ELSE P0. Training and counterexample cases all
pass under this dispatch.
Held-out tests under the true rule:
H1: ("xbc"->"ccc") (no 'q', broadcast-last). Mechanism routes on
input[0]=='x' to P1, predicts not-"ccc".
H2: ("aqc"->"qqq") ('q' present, broadcast-first). Mechanism routes on
input[0]='a' to P0, predicts "ccc".

**Kill criterion.** If either held-out case FAILS, X-RV2 SUCCEEDS: the
diagnosis locked onto the incidental lowest-position feature and the
revision misgeneralizes. Verdict impact: H-REVISE2 DOWNGRADED with the
documented failure class "diagnosis is lowest-position discrimination,
not causal; revision overfits incidental features."

**If both held-out cases pass,** X-RV2 FAILS.

## Attack X-RV3: Spurious UNRESOLVABLE on mixed-length passing inputs

**Setup.** P0 trained on ("abc"->"ccc"), ("def"->"fff"),
("ghi"->"iii"). Diagnosis passing set deliberately mixed-length:
("abc","de","ghi","jkl") where "de"->"ee" is monitor-confirmed passing
under P0 (P0 predicts "ee" correctly). Counterexample ("abx"->"aaa"):
P0 predicts "xxx", mismatch, expect DETECT. Diagnosis: p=0 'a' matches
"abc"[0]; p=1 'b' matches "abc"[1]; p=2: the length guard fires because
"de" has length 2 <= 2, so position 2 is skipped for all inputs;
diagnose returns -1 and the mechanism emits UNRESOLVABLE. But (2,120)
is a valid discriminating feature: no passing input has byte 120 at
position 2 ("abc"[2]='c', "ghi"[2]='i', "jkl"[2]='l', "de" has no
position 2). The attack program independently verifies this.

**Kill criterion.** If diagnose returns -1 (UNRESOLVABLE) while the
attack program confirms a valid discriminating (pos,val) exists
against the passing set, X-RV3 SUCCEEDS: the honest-withhold path
misfires; diagnosis is incomplete on mixed-length inputs. Verdict
impact: H-REVISE2 DOWNGRADED with the documented failure class
"UNRESOLVABLE can fire spuriously when passing inputs have mixed
lengths; one short input vetoes a position for all."

**If diagnose finds (2,120),** X-RV3 FAILS.

## Attack X-RV4: Source audit

**Procedure (no execution).** Grep and read the mechanism code paths:
(a) `diagnose()` must contain no byte-value literals for condition
values (only data-derived values and the 1000 encoding factor);
(b) P1's program bytes ([N N SUB] = [[1,255,255],[1,255,255],[6,0,1]])
must not appear as literals in the revision path; P1 must come only
from `discover()` on the counterexample subset;
(c) the dispatch condition passed to `vs_revise` must come from
`diagnose()` output, not from test-fixture constants;
(d) the picked condition (0,120) must not appear as a literal in any
mechanism function (test data and comments excluded).

**Kill criterion.** If any condition-value literal, P1 byte literal, or
diagnosis-bypassing hardcode is found in mechanism code, X-RV4
SUCCEEDS: the claim is spoofed. Verdict impact: H-REVISE2 KILLED.

**If the audit is clean,** X-RV4 FAILS (attack fails; mechanism passes).

## Verdict mapping

- X-RV4 SUCCEEDS -> H-REVISE2 KILLED (spoofed claim).
- X-RV1, X-RV2, or X-RV3 SUCCEEDS -> H-REVISE2 DOWNGRADED, with each
  successful attack recorded as a documented architectural failure
  class. The frozen K-RV1..K-RV5 bars (single revision event) are not
  retroactively altered; the downgrade adds boundaries the original
  test did not cover.
- All four attacks FAIL -> H-REVISE2 SURVIVES unmodified; the red team
  reports the failed kill attempts as evidence.

## Pure Zag compliance

Attack scenarios are implemented in Zag only, compiled with
znc 2026.07.0-dev. No Python anywhere. No em dashes in documentation.
