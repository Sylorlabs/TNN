# H-REVISE3 Result: Repaired Versioned Conditional Dispatch

**Date:** 2026-09-29
**Status:** COMPLETE
**Researcher:** H-REVISE3 Researcher (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_REVISE3.md (54790d0d2, frozen before implementation)
**Implementation:** revise3.zag (pure Zag, self-contained)
**Raw output:** revise3_raw.txt (75 lines, md5
98b49676e97465be61911b0c5c57833c, byte-identical across two runs)

## Verdict

**H-REVISE3 SURVIVES (45/45).** All three red-team failure classes are
repaired within the versioned conditional dispatch architecture.

## What was repaired

**F-RV1 (chained revision):** the version store is now an appendable
condition list (up to 4 revision slots). `vs_revise` appends a new
(cond_pos, cond_val, program) slot and never overwrites. Dispatch checks
slots most-recent-first (stated rule: the newest revision wins on
overlap). P0 is slot 0 and is never moved.

**F-RV2 (diagnosis gaming):** diagnosis now collects every
discriminating position and scores each candidate:

- +1 output-relevance: the candidate byte appears in the
  counterexample's expected output.
- +1 program-consistency: the candidate position appears in the
  extraction index sequence (positions the discovered program reads).
- Tie-break: lowest position (preserves H-REVISE2 behavior on ties).

P1 is discovered from the counterexample subset BEFORE final diagnosis
so the consistency signal is available. This is a stated heuristic
ranking, not guaranteed causal identification. The explicit assumption:
the causally relevant feature is among the discriminating positions.

**F-RV3 (spurious UNRESOLVABLE):** the length guard is now
bounds-respecting. A passing input shorter than position p is vacuous
at p (skipped), not vetoing. Only passing inputs with length > p
participate in the discrimination test at p.

## Test trace (from revise3_raw.txt)

- Phase A: P0 = [[1,255,255],[3,255,255],[6,0,1]] = [N C1 SUB]
  (broadcast-last), from ("abc"->"ccc"), ("def"->"fff"), ("ghi"->"iii").
- Phase B: ("jkl"->"lll") matches. ("xab"->"xxx") vs "bbb": DETECT.
- Phase C: scored diagnosis of "xab": candidates (0,120) score 2,
  (1,97) score 0, (2,98) score 0. BEST (0,120).
- Phase D: P1 = [[1,255,255],[1,255,255],[6,0,1]] = [N N SUB]. Appended
  slot1: IF input[0]==120 THEN P1 ELSE P0. vcount=1.
- Phase E: 5/5 VERIFY PASS.
- Phase F: ("abc"->"aaa") detected; no discriminating position;
  UNRESOLVABLE; P0 intact; vcount still 1.
- Phase G (chained): ("yzb"->"yyy") detected under slot-1 dispatch.
  Candidates (0,121) score 2, (1,122) score 0, (2,98) score 0. BEST
  (0,121). P2 = [N N SUB]. Appended slot2: IF input[0]==121 THEN P2.
  vcount=2. CHAIN VERIFY xab->xxx PASS (R1 survives). CHAIN VERIFY
  yzb->yyy PASS (R2 works).
- Phase H ('q' case, fresh store): ("xqc"->"qqq") detected. Candidates
  (0,120) score 0, (1,113) score 2 (113 in "qqq"; extraction seq
  [1,1,1]). BEST (1,113): the causally relevant feature, not the
  incidental lowest position. PQ = [[1,255,255],[4,255,255],[6,0,1]] =
  [N C2 SUB] (broadcast index 1). Revised: IF input[1]==113 THEN PQ
  ELSE P0. Held-out ("xbc"->"ccc") PASS and ("aqc"->"qqq") PASS.
- Phase I (mixed-length, fresh store): passing ("abc","de","ghi","jkl").
  ("abx"->"aaa") detected. Bounds-respecting diagnosis finds (2,120)
  ("de" vacuous at position 2); NOT -1. Revised:
  IF input[2]==120 THEN PM ELSE P0. VERIFY abx->aaa PASS.

## Kill bar assessment

**K-RV3-1 (chained revision works): PASS.** vcount=2; both
("xab"->"xxx") and ("yzb"->"yyy") verify PASS after R2. R1 not
destroyed.

**K-RV3-2 (diagnosis handles the 'q' case): PASS.** Diagnosis returns
(1,113), not (0,120). Held-out 2/2 PASS. The red-team gaming fixture
is now handled correctly.

**K-RV3-3 (UNRESOLVABLE does not misfire): PASS.** Diagnosis returns
(2,120), not -1, on the mixed-length passing set. Revision proceeds;
("abx"->"aaa") verifies PASS.

**K-RV3-4 (original H-REVISE2 tests preserved): PASS.** Phase E 5/5
PASS; Phase F UNRESOLVABLE emitted with P0 intact and version store
unchanged.

**K-RV3-5 (determinism): PASS.** Two consecutive runs byte-identical
(md5 98b49676e97465be61911b0c5c57833c, verified with cmp).

## Relation to H-REVISE2

H-REVISE2's SURVIVES verdict on its frozen bars stands; the red-team
downgrade bounded it to single-event revision under favorable
conditions. H-REVISE3 removes the three demonstrated bounds: chaining
now composes, the gaming fixture is diagnosed correctly, and the
withhold path is complete. The scored diagnosis is strictly more
informative than lowest-position (it reduces to lowest-position on
score ties).

## Classification

Bounded L2+ revision (chained single-condition revisions; affine
sub-programs; heuristic scored diagnosis). L3 criterion 12 now holds
for chained revisions under the stated scoring assumption, not only
the single-event case. Not general L3: condition vocabulary remains
(position, equality); conjunctions, ranges, and inequalities untested;
the diagnosis heuristic is not a causal guarantee.

## Boundaries and honest limits

- The scored diagnosis can still select an incidental feature if the
  incidental byte also appears in the output and at a program-read
  position. A red team may construct such a fixture; it would bound,
  not necessarily kill, the repair.
- Conjunctions ("input[0]=='x' AND input[1]=='q'") are outside the
  single-condition vocabulary.
- Most-recent-first dispatch is a stated rule; overlapping conditions
  from genuinely conflicting revisions resolve to the newest, which may
  not be the intended semantics in all cases.
- Max 4 revision slots in the current store layout.

## Pure Zag compliance

Implementation, compilation (znc 2026.07.0-dev), and execution in Zag
only. No Python used anywhere. No em dashes in this document.

## Test accounting note (disclosed)

The first run scored 44/45 due to a test-harness accounting omission:
the Phase C "diagnosis succeeded" event incremented ntest but not
npass (the unconditional npass after the dr<0 early-return, present in
revise2.zag, was dropped in the rewrite). The mechanism behaved
correctly in that run (diagnosis found (0,120) as shown in the trace).
The harness was fixed (one line: `npass_total=npass_total+1;`), the
source recompiled, and the committed raw output is the corrected
45/45 run. The pre-fix 44/45 raw output is preserved as
revise3_raw_prefix.txt. The fix touched only test accounting, not the
mechanism. This mirrors the accounting note disclosed in
REVISE2_RESULT.md.
