# H-REVISE4 Result: Tie-Aware Diagnosis and Explicit Capacity

**Date:** 2026-09-29
**Status:** COMPLETE
**Researcher:** H-REVISE4 Researcher (subagent)
**Branch:** tnn-native-lab
**Prereg:** PREREG_REVISE4.md (926618d69, frozen before implementation)
**Implementation:** revise4.zag (pure Zag, self-contained)
**Raw output:** revise4_raw.txt (md5 93332f90fc365426e51e39bce617b4bc, byte-identical across 3 runs)

## Verdict

**H-REVISE4 SURVIVES (52/52).** Both H-REVISE3 red-team downgrades are
repaired within the versioned conditional dispatch architecture.

## What was repaired

**R1 (X-RV3-1 tie gaming): tie-aware diagnosis with AMBIGUOUS withhold.**
`diagnose_scored` now tracks how many candidates achieve the maximal
score. If more than one candidate ties at the top, the function returns
-2 (AMBIGUOUS) and emits "AMBIGUOUS: N candidates tie at score S;
revision withheld (heuristic cannot distinguish)". The caller does NOT
append a revision. This is honest: when the available signals cannot
distinguish the causal feature from incidentals, the mechanism withholds
rather than guessing by position.

Rationale: with a single counterexample, the causal feature is
underdetermined when the discovered program reads all tied positions
(e.g., identity) and the incidental bytes appear in the output. No
signal in the (position, equality) vocabulary distinguishes them.
Guessing by lowest position is arbitrary; withholding is correct.

**R2 (X-RV3-3 silent drop): explicit capacity policy
(REFUSE-WITH-WARNING).** `vs3_revise` on a full store (vc>=4) now emits
"VS3FULL: revision refused; store at capacity (4); earlier revisions
intact; queries on refused condition fall through to P0" and returns -1
(distinct from 1=appended). Callers handle -1 explicitly with "REVISE
REFUSED (store full, explicit VS3FULL policy)". Documented policy: at
most 4 chained revisions; the 5th and beyond are refused with explicit
warning, never silently dropped; earlier revisions are never evicted.

The 4-slot layout is unchanged. The repair is about explicitness, not
capacity.

## Test trace (from revise4_raw.txt)

Phases A-I: identical to H-REVISE3 (45/45 preserved).

- Phase J (K-RV4-1): X-RV3-1 fixture. Hidden truth "IF input[2]=='y'
  THEN identity ELSE broadcast-last". Counterexample ("xqy"->"xqy")
  detected (P0 predicts "yyy"). Diagnosis: (0,120) score 2, (1,113)
  score 2, (2,121) score 2. AMBIGUOUS: 3 candidates tie at score 2.
  Returns -2. No revision appended (vcount still 0). K-RV4-1 PASS.

- Phase K (K-RV4-2): X-RV3-3 fixture. Five sequential revisions.
  R1..R4 append (vcount=4). R5: VS3FULL warning emitted, returns -1,
  vcount stays 4. Earlier revision intact ("xab"->"xxx" still PASS).
  K-RV4-2 PASS.

- Result: 52/52. H-REVISE4 SURVIVES.

## Kill bar assessment

**K-RV4-1 (tie gaming addressed): PASS.** The X-RV3-1 fixture yields
diagnosis -2 (AMBIGUOUS), NOT (0,120). Output contains "AMBIGUOUS: 3
candidates tie at score 2". No wrong revision appended (vcount=0).

**K-RV4-2 (capacity explicit): PASS.** R1..R4 append (rc=1, vcount=4).
R5 emits VS3FULL warning, returns -1, vcount stays 4. Earlier revisions
intact. The refusal is explicit, not silent.

**K-RV4-3 (no regression): PASS.** All 45/45 H-REVISE3 frozen behaviors
preserved: Phase C (0,120) unique top; Phase G (0,121) unique; Phase H
(1,113) unique; Phase I (2,120) unique (not -1, not AMBIGUOUS); Phase E
5/5 PASS; Phase F UNRESOLVABLE (-1, not -2) with P0 intact. None of the
frozen fixtures produce a top-score tie.

**K-RV4-4 (determinism): PASS.** Three consecutive runs byte-identical
(md5 93332f90fc365426e51e39bce617b4bc, verified with cmp).

## Relation to H-REVISE3

H-REVISE3's SURVIVES verdict on its frozen bars stands; the red-team
downgrade bounded the scored heuristic and the capacity handling.
H-REVISE4 removes both bounds: ties now withhold honestly instead of
guessing, and capacity refusal is explicit instead of silent. The
scored diagnosis is now tie-aware; the version store has an explicit
refusal policy.

## Classification

Bounded L2+ revision (chained single-condition revisions; affine
sub-programs; tie-aware heuristic diagnosis; explicit capacity policy).
Not general L3: condition vocabulary remains (position, equality);
conjunctions untested; AMBIGUOUS withhold reports indistinguishability
but does not resolve it; capacity remains 4.

## Boundaries and honest limits

- AMBIGUOUS does not identify the causal feature; it honestly reports
  that the heuristic cannot distinguish. A future mechanism with richer
  signals (multiple counterexamples, interventional data) might resolve
  such ties.
- Capacity remains 4. The repair makes the limit explicit; it does not
  remove it. A growable store or eviction policy is future work.
- Overlap semantics (most-recent-first) unchanged.
- The tie threshold is exact equality of integer scores. Near-ties
  (differing by 1) still resolve by lowest position.

## Pure Zag compliance

Implementation, compilation (znc 2026.07.0-dev), and execution in Zag
only. No Python used anywhere. No em dashes in this document.
