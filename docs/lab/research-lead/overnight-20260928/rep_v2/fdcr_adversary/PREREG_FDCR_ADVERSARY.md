# Preregistration: FDCR Adversarial Red Team (F-A1..F-A6)

**Date:** 2026-09-29 07:30 PDT
**Status:** FROZEN (before attack execution)
**Attacker:** FDCR Adversary (independent subagent)
**Target:** `rep_v2/fdcr_learn.zag` (1,264 lines), claims in RESULTS_REP_V2.md

## Background

The Representation Researcher claims FDCR (Failure-Driven Concept Recruitment)
passes all SEM kill tests: K5 hierarchy 4/4, K2 delayed split 5/5, K4 overlap
2/2, K3 merge 5/5, mini_world 8/8. The prereg (6db93a784) is honest about scope
(representational adequacy, not L3). My job: assume the claim is false, find
the strongest alternative explanation.

## Verified pre-attack

- Prereg 6db93a784 (14:17:41 UTC) precedes implementation commit 17d5de9f7
  (14:24:59 UTC). Commit ORDER is clean.
- Governance flag (not a kill): implementation + fixtures + results + raw
  outputs all landed in ONE commit (17d5de9f7) under a "Bridge prereg" message.
  The results report claims "Implementation and fixtures committed separately
  from this report" which is FACTUALLY FALSE. Hygiene violation, documented.
- All five fixtures reproduce byte-identically from committed source. No
  fabrication.

## Attacks

### F-A1 (Source inspection) -- vocabulary hardcoding

Claim to kill: "No test vocabulary appears in source; implementation is generic."

Method: grep fdcr_learn.zag for all fixture vocabularies (flies, sparrow,
eagle, o3a, o3b, squeezer, vellum, sheet, norpal, glim, glow, ferrum, ironbar)
plus structural hardcoding patterns (expected parent intents, entity-count
assumptions).

KILL BAR: Any fixture vocabulary found in source, OR any logic branch keyed
to fixture-specific structure (e.g., "if 8 entities share a feature").

Preliminary: grep counts all zero. Structural check pending.

### F-A2 (Hierarchy depth) -- 3+ levels

Claim to kill: "FDCR handles hierarchy" (K5 shows 2 levels: parent + children).

Method: Construct a 3-level fixture AFTER this prereg (adversary-designed,
not researcher-designed):
- Level 3 (root): all 12 entities share (alive, yes).
- Level 2: 6 mammals share (fur, yes) + (alive, yes); 6 birds share
  (feathers, yes) + (alive, yes).
- Level 1: within mammals, 3 dogs share (barks, yes); 3 cats share
  (meows, yes). Within birds, 3 sparrows share (size, small); 3 eagles
  share (size, large).
- Probes: query root-level, mid-level, and leaf-level features for held-out
  entities.

KILL BAR: FDCR must form all three levels with correct parent links. If it
collapses to 2 levels, forms spurious levels, or answers leaf probes wrong,
F-A2 KILLS the "handles hierarchy" generalization (K5 result stands as a
2-level special case only).

### F-A3 (Split correctness) -- coherent vs arbitrary split

Claim to kill: "SPLIT produces two coherent concepts" (K2 shows SPLIT fired).

Method: Two-part.
(a) White-box: inspect the K2 concept dump. Verify C1 intent = parent intent
+ (r3,o3a) exactly, C2 = parent intent + (r3,o3b) exactly, parent preserved
with both members. Any deviation (e.g., parent intent mutated, members
misassigned) is a FAIL.
(b) Subtle-evidence test (adversary-designed): distinguishing feature is a
single rare relation among many shared ones (10 shared features, 1
distinguishing). If SPLIT fails to fire or splits on the wrong feature,
F-A3 KILLS.

KILL BAR: (a) dump must match the claimed structure exactly; (b) split must
fire on the single distinguishing feature.

### F-A4 (Overlap vs duplication) -- true overlap

Claim to kill: "Shared concept with distinct children = true overlap"
(K4 shows C2 shared, C0/C1 children).

Method: White-box inspection of K4 concept dump.
- True overlap: ONE concept C2 with members {B1, B2}, intent exactly the
  2 shared features; C0 (B1) and C1 (B2) are children of C2 with parent=2.
- Duplication (kill): TWO separate concepts each containing the shared
  features independently, with no parent link between the shared structure
  and the children; OR C2 exists but B1/B2 are not both members; OR C2
  intent != exactly the 2 shared features.

KILL BAR: Any structural deviation from true overlap as defined above.

### F-A5 (COMPOSE missing) -- boundary of the missing operator

Claim: researcher admits COMPOSE not implemented. This attack measures how
critical the gap is.

Method: Construct a task requiring composition (adversary-designed):
- Concept A: entities with (color, red).
- Concept B: entities with (shape, round).
- Target: entity with both (color, red) AND (shape, round), query a feature
  that is only inferable if the composed concept exists.
- Since COMPOSE is absent, expect FAIL. Document precisely which inference
  fails and why.

KILL BAR: This is a BOUNDARY attack, not a kill of the adequacy claim
(researcher already disclosed it). PASS for the researcher if the failure
mode matches the disclosure (no silent wrong answer; clean WITHHOLD or
documented limitation). FAIL (kill of honesty) if FDCR gives a confidently
wrong answer where composition was needed.

### F-A6 (Scale) -- 20+ entities

Claim to kill: implicit "mechanism scales" (all tests are tiny: 8, 2, 2, 2).

Method: Generate a 24-entity fixture with shell (no Python): 3 groups of 8,
each group shares a group feature, all share a root feature (mirrors K5
structure at 3x scale). Measure: wall-clock time, output concept count,
correctness of root parent formation.

KILL BAR: Any of: crash, hang (>60s), root parent missing, or concept count
exploding superlinearly (>200 concepts for 24 entities suggests
combinatorial blowup). If FORM enumerates all subsets, 24 entities could
produce thousands of concepts.

## Controls

- C-REPRO: all five committed fixtures reproduce byte-identically (done).
- C-GOV: prereg order verified (done, with hygiene flag documented).

## What kills what

- F-A1 kill: hardcoding found -> H-REP adequacy claim KILLED (fraud-adjacent).
- F-A2 kill: hierarchy does not generalize past 2 levels -> "handles
  hierarchy" downgraded to "handles 2-level grouping." K5 stands as
  reported; the generalization dies.
- F-A3 kill: split is arbitrary or misfires -> "contradiction-driven
  revision" downgraded.
- F-A4 kill: overlap is duplication -> "represents overlap" KILLED.
- F-A5: boundary documentation (researcher pre-disclosed; kill only on
  dishonest failure mode).
- F-A6 kill: combinatorial blowup -> "generic mechanism" claim weakened to
  "toy-scale only."

## Frozen

Attacks frozen before execution. Fixture designs for F-A2, F-A3(b), F-A5, F-A6
will be generated with shell after this commit. No Python anywhere.
