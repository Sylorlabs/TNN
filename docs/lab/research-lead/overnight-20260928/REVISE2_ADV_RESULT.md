# H-REVISE2 Adversary Report: X-RV1..X-RV4

**Date:** 2026-09-29
**Researcher:** H-REVISE2 Red Team (subagent)
**Status:** COMPLETE
**Branch:** tnn-native-lab
**Target:** H-REVISE2 SURVIVES (18/18), `revise2.zag`
**Prereg:** PREREG_REVISE2_ADV.md (1bbadf544, frozen before any attack execution)
**Amendment:** PREREG_REVISE2_ADV_AMEND1.md (corrected X-RV1 R2 fixture;
  transparent setup fix, kill criteria unchanged; frozen before the
  corrected run)
**Attack implementation:** `revise2_adv.zag` (mechanism functions verbatim
  from `revise2.zag`; only `main()` replaced by attack scenarios)
**Raw evidence:** `revise2_adv_raw.txt` (35 lines, md5
  e766d2820e4393784b5d47209fb0e448, byte-identical across two runs)

## Verdict

**H-REVISE2 DOWNGRADED.** Three of four attacks succeed. The frozen
K-RV1..K-RV5 bars are NOT retroactively altered: the single revision
event they tested works as claimed, and the source audit finds no
spoofing. The downgrade bounds the claim: versioned conditional
dispatch revises exactly once, under favorable conditions, and three
architectural failure classes are now demonstrated.

## Attack results

### X-RV1 (chained revision): SUCCEEDS -> failure class F-RV1

R1: ("xab"->"xxx") DETECTed, diagnosed (0,120), P1=[N N SUB] discovered,
versioned IF input[0]==120 THEN P1 ELSE P0, R1 case verified PASS.
R2: ("yzb"->"yyy") genuinely DETECTed under the R1 dispatch (P0 predicts
"bbb"), diagnosed (0,121), P2=[N N SUB] discovered from the new
counterexample subset, `vs_revise` called with (0,121).
Result: the R1 case "xab"->"xxx" now FAILS (predicts "bbb"). The VSTORE
dump shows vcount=1, cond pos=0 val=121: the second `vs_revise`
unconditionally overwrote the single condition slot and the P1 program
slot. The "version store" is a single conditional slot, not a version
memory. A second revision destroys the first.

Amendment note: the first execution used R2 fixture ("yza"->"aaa");
P0 correctly predicted "aaa" (broadcast-last of 'a'), so no DETECT
occurred. The prereg's "P0 predicts zzz" was the adversary's arithmetic
error, recorded transparently in the amendment. The corrected fixture
("yzb"->"yyy") produces a genuine DETECT-to-REVISE event, and the
overwrite finding is unchanged.

### X-RV2 (diagnosis gaming): SUCCEEDS -> failure class F-RV2

Hidden true rule: broadcast input[1] iff the input contains 'q', else
broadcast-last. Counterexample ("xqc"->"qqq") DETECTed. Diagnosis
returned (0,120): the lowest discriminating position, an incidental
feature. The causally relevant feature ('q'=113 at pos 1) was ignored
because position 0 already discriminated. P1=[N C2 SUB] (broadcast
index 1) was discovered and versioned on input[0]==120.
Held-out: ("xbc"->"ccc") FAIL (predicted "bbb"); ("aqc"->"qqq") FAIL
(predicted "ccc"). 0/2. The revision overfits the incidental
lowest-position feature and misgeneralizes in both directions: it
fires P1 on 'x'-initial inputs without 'q', and misses 'q'-inputs
without initial 'x'. Diagnosis is lowest-position discrimination, not
causal diagnosis; the mechanism cannot distinguish incidental from
causally relevant features.

### X-RV3 (spurious UNRESOLVABLE): SUCCEEDS -> failure class F-RV3

Diagnosis passing set ("abc","de","ghi","jkl") with mixed lengths;
"de"->"ee" sanity-confirmed passing under P0. Counterexample
("abx"->"aaa") DETECTed (P0 predicts "xxx"). `diagnose` returned -1:
position 0 and 1 match "abc", and position 2 was skipped because the
length guard vetoes a position when ANY passing input is shorter
("de" has length 2). The mechanism would emit UNRESOLVABLE and withhold
revision. The attack's bounds-respecting reference diagnosis finds
(2,120): no passing input has byte 120 at position 2. The withhold was
spurious; a valid revision existed. One short passing input vetoes a
position for all inputs.

### X-RV4 (source audit): FAILS (attack fails; mechanism passes)

(a) `diagnose()` contains no byte-value literals: the only multi-digit
numeric literal is the 1000 pos/val encoding factor; all compared
values come from the data (`fail[p]`, `D[off+p]`).
(b) P1's exact bytes ([1,255,255],[1,255,255],[6,0,1]) appear nowhere
as a literal; P1 comes only from `discover()` on the counterexample
subset.
(c) The sole `vs_revise` call site passes `(dpos, dval, p1, nn1)`
where (dpos,dval) come from `diagnose()` and p1 from `discover()`.
No diagnosis bypass.
(d) Literal `120` appears only inside `1200*4` (an allocation size);
"xab" appears only as test-fixture data and in comments/emit strings.
No spoofing found. The SURVIVES verdict on the frozen bars was earned.

## What the downgrade means

H-REVISE2's revision works for exactly one revision event, when the
discriminating feature is at the lowest differing position, when
passing inputs share uniform length, and when no second revision is
needed. Outside that envelope, three failure classes apply:

- F-RV1: chained revision impossible; second `vs_revise` overwrites
  the first (single-slot store, not a version memory).
- F-RV2: diagnosis locks onto incidental lowest-position features;
  revision misgeneralizes on held-out inputs.
- F-RV3: UNRESOLVABLE misfires on mixed-length passing sets; the
  length guard is overly conservative.

L3 criterion 12 (revisable after a counterexample) is satisfied only
for the bounded single-event case, not in general. The
REVISE2_RESULT.md claim that "procedure discovery moves from 11/12
toward 12/12" should be read with these bounds: the remaining distance
is not only the generality of the condition vocabulary (already
noted) but also chaining, causal diagnosis, and completeness of the
withhold path.

## Suggested repairs (not implemented; for the builder lane)

- F-RV1: append conditions to a condition list (vcount>1, ordered
  dispatch, most-recent-first or most-specific-first with a stated
  rule).
- F-RV2: diagnosis over ALL discriminating positions with a
  confirmation episode, or a stated lowest-position assumption in the
  claim.
- F-RV3: bounds-respecting diagnosis (short inputs vacuous at missing
  positions, not vetoing).

## Artifacts

- `PREREG_REVISE2_ADV.md` (1bbadf544): frozen attack prereg.
- `PREREG_REVISE2_ADV_AMEND1.md`: frozen fixture correction.
- `revise2_adv.zag`: attack implementation (verbatim mechanism).
- `revise2_adv_raw.txt`: authoritative raw evidence (md5
  e766d2820e4393784b5d47209fb0e448).
- Binary built at /tmp/revise2_adv, not committed per convention.

## Pure Zag compliance

Attack design, implementation, compilation (znc 2026.07.0-dev), and
execution in Zag only. No Python used anywhere. No em dashes in this
document.

## Test accounting note (disclosed)

The first attack execution ran under the original (miscalculated) R2
fixture and is superseded by the corrected run committed here. Both
the flaw and its correction are in the frozen amendment, not hidden.
