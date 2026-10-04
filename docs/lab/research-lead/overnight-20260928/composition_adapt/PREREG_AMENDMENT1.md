# PREREG AMENDMENT 1: EXTEND-ONE battery

Transparent amendment, frozen before the re-run. It corrects two
things found in the first implementation run; it weakens nothing.
All kill bars are evaluated against PREREG.md as amended here, on a
fresh rebuild and rerun. First run: ad_run1.txt (sha256
2f974614491ed918aef055da1a809e46c1f358ddb980c7bcdd2bed61e93b9c3e);
this amendment is written after that run and before the re-run.

## 1. Operator bug fix (not a bar change)

adapt_extend promoted adapted MAPs via promote_graph, whose
ev_teach_in side effect taught a derived fact (e.g. (101,71,105) in
A4-L1-ABL-Y). That fact gave the generic trial a shortcut path
(t2_trial assembled [101,105,106,107] and verified 107), so ABL-Y
answered 107 instead of the frozen -2.

Root cause: every other promote_graph caller passes a VERIFIED QUERY
ANSWER (trial, rebind, and compose all verify against expected before
promoting). An adapted MAP is scaffolding built mid-query, not a
query answer, so teaching a fact for it broke the standing invariant
"facts are taught only for verified query answers".

Fix: adapted MAPs are promoted with adapt_promote, which writes the
identical MAP node/edge layout (tag 20, fields, DEP edges to
licensing facts, self edges) but teaches no fact. The adapted
structure remains fully visible to the DFS as a live MAP. No kill
bar changes; A4-ABL-Y is re-run against the frozen -2 bar.

## 2. Corrected provenance expectation (bar correction, not weakening)

The frozen PREREG predicted A1/A2's second DFS segment would be
MAP_Y (assertion p4: MAP_Z LINK14 to MAP_Y) and asserted no LINK14
from MAP_Z to MAP_X (p5). The first run showed segments
[adapted, MAP_X]: the UNCHANGED unified DFS selects MAP_X for
segment 2 via A's plen-contract fallback (cx_contract plen-4 matches
the real r2 path 105->106->107->108; the tie with MAP_Y is broken by
lower MAP id). This is pre-existing unified behavior, orthogonal to
the operator, and the composition is genuine (full chain verified
108 against expected). The L2 claim never depended on segment 2's
identity; the prereg's prediction about the third-party DFS
tie-break was simply wrong.

Corrected bars: K1/K2 require p1 (ans=108), p2 (adapted MAP with
type-16 edge to MAP_X), p3 (MAP_Z LINK14 to the adapted MAP), p6
(adapted relseq [1,1,1,1] for A1, [1,1,1,2] for A2). Assertions p4
and p5 are dropped. The observed segment-2 selection (MAP_X via
contract fallback) is recorded as a finding, not a bar.

## Restated kill bars

- K1: A1: ans=108; adapted MAP a with type-16 edge a->MAP_X; MAP_Z
  LINK14 to a; relseq(a)=[1,1,1,1].
- K2: A2: ans=108; adapted MAP a with type-16 edge a->MAP_X; MAP_Z
  LINK14 to a; relseq(a)=[1,1,1,2].
- K3: A3 ans=-2 and zero adapted MAPs created. Unchanged.
- K4: A4 all six L1 arms pass. Unchanged.
- K5: 3/3 byte-identical runs; sha256 recorded. Unchanged.
- K6: zero em/en dashes in all deliverables (byte-verified).
  Unchanged.
- K7: un_patch.zag verbatim; cc_base.zag untouched. Unchanged.

Verdict COMPOSITION-ADAPT-COMPLETE iff K1-K7 all pass under this
amended prereg.
