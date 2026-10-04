# Preregistration: H-REVISE4 (Revision Repair v4)

**Date:** 2026-09-29
**Researcher:** H-REVISE4 Researcher (subagent)
**Status:** FROZEN (commit before any implementation file)
**Branch:** tnn-native-lab

## Hypothesis

H-REVISE4: The two H-REVISE3 red-team downgrades (X-RV3-1 scoring
tie gaming, X-RV3-3 silent slot exhaustion) are repairable within the
versioned conditional dispatch architecture: (1) tie-aware diagnosis
that withholds as AMBIGUOUS when the heuristic cannot distinguish
candidates, instead of guessing by position; (2) explicit capacity
policy with a user-visible VS3FULL warning instead of silent drop.

## Background

H-REVISE3 SURVIVES (45/45) on its frozen bars: chained revision
composes, the 'q' gaming fixture is diagnosed correctly, the withhold
path is complete. The independent red team (REVISE3_ADV_RESULT.md)
DOWNGRADED it with two succeeding attacks:

- X-RV3-1: Scored diagnosis gaming. Fixture with hidden true rule
  "IF input[2]=='y' (121) THEN identity ELSE broadcast-last",
  counterexample ("xqy"->"xqy"). P1 discovered is identity [K], whose
  extraction seq [0,1,2] covers all positions. All three discriminating
  candidates (0,120), (1,113), (2,121) score 2 (byte in output +1,
  position in seq +1). Tie-break (strict >, lowest p wins) selects
  incidental (0,120) instead of causal (2,121). Both held-out fail.
  The scored heuristic is bounded, not a causal guarantee.

- X-RV3-3: Slot exhaustion. Five sequential genuine revisions; R5
  returns rc=0, vcount stays 4. Query "vab" falls through to P0 and
  gives wrong answer. The 4-slot limit is disclosed in the prereg, but
  the drop is SILENT: no eviction policy, no user-facing error, no
  store-full signal in the query path.

X-RV3-2 (overlap) was BOUNDARY (stated most-recent-first rule, no kill
criterion). X-RV3-4 (source audit) PASSED: no spoofing. The frozen
K-RV3-1..K-RV3-5 bars were earned and are NOT retroactively altered.

## Repairs (frozen design)

**R1 (X-RV3-1): tie-aware diagnosis with AMBIGUOUS withhold.**
`diagnose_scored` is modified to detect ties at the top score. After
scoring all discriminating candidates, if more than one candidate
achieves the maximal score, the function returns -2 (AMBIGUOUS) instead
of the lowest-position candidate. The caller, on receiving -2, emits
"AMBIGUOUS: top candidates tie at score S; revision withheld (heuristic
cannot distinguish)" and does NOT append a revision. This is honest:
when the available signals cannot distinguish the causal feature from
incidentals, the mechanism withholds rather than guessing. The -1
(no discriminating candidate) path is unchanged.

Rationale: with a single counterexample, the causal feature is
underdetermined when the discovered program reads all tied positions
and the incidental bytes appear in the output. No signal in the
(position, equality) vocabulary distinguishes them. Guessing by
position is arbitrary; withholding is the correct honest behavior.

**R2 (X-RV3-3): explicit capacity policy (REFUSE-WITH-WARNING).**
`vs3_revise` is modified: on a full store (vc>=4), it emits an explicit
warning "VS3FULL: revision refused; store at capacity (4); earlier
revisions intact; queries on the refused condition fall through to P0"
and returns -1 (distinct from 1=appended). The caller, on receiving -1,
emits "REVISE REFUSED (store full, explicit policy)" and does not
modify the store. Documented policy: at most 4 chained revisions; the
5th and beyond are refused with explicit warning, never silently
dropped; earlier revisions are never evicted; queries on refused
conditions use the fallthrough path (P0 or earlier slots).

The 4-slot layout is unchanged (not expanded); the repair is about
explicitness, not capacity. A growable store or eviction policy is
future work, explicitly out of scope.

## Frozen kill bars

**K-RV4-1 (tie gaming addressed):** The X-RV3-1 fixture (hidden truth
(2,121), counterexample ("xqy"->"xqy"), P1=identity) now yields
diagnosis -2 (AMBIGUOUS), NOT (0,120). No wrong revision is appended.
The output contains the AMBIGUOUS line naming the tied candidates.

**K-RV4-2 (capacity explicit):** Five sequential genuine revisions
(R1..R5 as in the X-RV3-3 fixture). R1..R4 append (rc=1). R5 emits the
VS3FULL warning, returns -1, vcount stays 4. Earlier revisions intact
("xab"->"xxx" still PASS). The drop is explicit, not silent.

**K-RV4-3 (no regression):** All 45/45 H-REVISE3 frozen behaviors
preserved. Specifically: Phase C diagnoses (0,120) (unique top score,
no tie); Phase G diagnoses (0,121) (unique); Phase H diagnoses (1,113)
(unique); Phase I diagnoses (2,120) (unique, not -1); Phase E 5/5 PASS;
Phase F UNRESOLVABLE with P0 intact. Rationale: none of the frozen
fixtures produce a top-score tie, so tie-awareness does not change
their outcomes. Verified by re-running the full H-REVISE3 battery.

**K-RV4-4 (determinism):** Three consecutive runs byte-identical
(verified with cmp).

## What is NOT claimed

- The AMBIGUOUS withhold does not identify the causal feature; it
  honestly reports indistinguishability. A future mechanism with a
  richer signal (e.g., multiple counterexamples, interventional data)
  might resolve such ties.
- Capacity remains 4. The repair makes the limit explicit; it does not
  remove it.
- Overlap semantics (most-recent-first) unchanged.
- Condition vocabulary (position, equality) unchanged.

## Pure Zag compliance

Prereg, implementation, compilation, and execution in Zag only. No
Python at any stage. No em dashes in this document.
