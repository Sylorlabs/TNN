# FDCR Red-Team Report (F-A1..F-A6)

**Date:** 2026-09-29 07:45 PDT
**Attacker:** FDCR Adversary (independent subagent)
**Target:** `rep_v2/fdcr_learn.zag`, claims in RESULTS_REP_V2.md
**Prereg:** `fdcr_adversary/PREREG_FDCR_ADVERSARY.md` (commit e300bd9cb, frozen before attacks)
**Verdict:** CLAIM SURVIVES with three downgrades. No kill.

## Method

- Recompiled `fdcr_learn.zag` from committed source with znc. All five
  committed fixtures reproduce byte-identically. No fabrication.
- Designed five adversarial fixtures AFTER prereg (shell only, no Python).
- White-box inspection of concept dumps (the `# concepts` sections).

## F-A1 (Source inspection): NO KILL

- Grep for all fixture vocabularies (flies, sparrow, eagle, o3a, o3b,
  squeezer, vellum, sheet, norpal, glim, glow, ferrum, ironbar): all zero.
- No structural hardcoding: no fixture-keyed branches, no magic numbers
  tied to entity counts. The single "expected" string (line 1197) is test
  harness output formatting, not logic.
- Implementation is generic.

## F-A2 (Hierarchy depth, 3 levels): NO KILL, two bugs found

Fixture `atk_fixtures/fa2_3level.txt`: 12 entities, root {alive}, mid
{alive,fur}/{alive,feathers}, leaves (dogs/cats/sparrows/eagles).

Result: three levels form with correct parent links.
- C5 {alive=yes}, 12 members, parent=-1 (root).
- C4 {alive,fur}, 6 members, parent=5; C6 {alive,feathers}, 6 members,
  parent=5 (mid).
- C0..C3 leaves with correct parents.

Bugs found (not kills of the hierarchy claim):
1. **MERGE incompleteness:** C2 {alive,feathers,size=small} parent=5 and C65
   with IDENTICAL intent parent=6 were not unified. Same for C3/C66.
   The prereg's MERGE spec ("if two concepts have identical intents, unify
   them") is violated when duplicates arise under different parents.
2. **Spurious SPLITs:** C7 {alive,size=small} and C8 {alive,size=large}
   created with reason=2 (SPLIT) despite no contradiction in the fixture.
   Same phenomenon as the researcher's disclosed K5 "extra SPLIT children."

## F-A3 (Split correctness): NO KILL on structure; BAR CONFOUND found

(a) White-box K2: dump matches spec exactly. C0 {r1o1,r2o2} preserved with
both members; C1 {+r3o3a} for E1a, C2 {+r3o3b} for E1b, parent=0, reason=2.
Coherent, not arbitrary.

(b) Subtle split (10 shared features, 1 distinguishing `rare`):
SPLIT fired correctly on the single distinguishing feature. Children exact.

(c) **MAJOR BAR-WEAKNESS FINDING:** Every K2-v2 probe queries a TAUGHT fact
(T E1a|r3|o3a etc.). Bug fix #3 (Step-0 direct taught-fact lookup, added
during development with NO prereg amendment) answers all of them without
touching the concept system. The K2-v2 kill bar therefore cannot
discriminate "SPLIT works" from "direct lookup works." The split DID fire
(dump proves it), so the mechanism is sound, but the bar is invalid as a
test of revision. Same confound applies to K5-v2 (4/4 probes taught) and
K4-v2 (2/2 probes taught). Only mini_world's 3 "sib"-marked probes
genuinely exercise concept inference (3/3 pass).

Downgrade: K5-v2/K2-v2/K4-v2 probe scores are CONFOUNDED. Structure
formation is white-box verified; the bars need redesign with held-out
inference probes before they can carry the adequacy claim alone.

## F-A4 (Overlap vs duplication): NO KILL

K4 dump is true overlap, exactly per spec:
- C2 intent exactly {r1=o1, r2=o2}, members {B1, B2}, parent=-1, reason=1.
- C0 (B1 full) and C1 (B2 full), both parent=2.
One shared concept, two members, distinct linked children. Not duplication.

## F-A5 (COMPOSE missing): BOUNDARY CONFIRMED, no kill (pre-disclosed)

FORM produces intersection (shared-subset) parents only. No union operator
exists. My composition fixture could not make composition load-bearing
(the target label was taught, so Step 0 answered it). Precise boundary:
union-intent concepts arise only as leaf/SPLIT artifacts, never by
deliberate composition of two concepts' intents. The researcher's
disclosure was accurate; the failure mode is clean (no confidently wrong
answers observed).

## F-A6 (Scale, 24 entities): NO KILL

Fixture `atk_fixtures/fa6_scale.txt`: 24 entities in 3 groups of 8.
Result: 36 concepts, 0.192s wall clock, exit 0. Root C26 {alive} with all
24 members; group parents C24/C34/C35 correct. No combinatorial blowup.
Bonus: cross-cutting tag groupings (C25..C33) formed correctly, showing
the mechanism finds multiple overlapping structures, not just the
designed one.

## Governance findings

1. Prereg commit order is clean: 6db93a784 (14:17:41 UTC) precedes
   implementation 17d5de9f7 (14:24:59 UTC).
2. **Hygiene violation:** implementation + fixtures + results + raw outputs
   all landed in ONE commit (17d5de9f7) under the message "Bridge prereg
   FROZEN." The results report's claim "Implementation and fixtures
   committed separately from this report" is FACTUALLY FALSE.
3. **Unamended design change:** Step-0 direct lookup (bug fix #3) changed
   what the kill bars measure. The prereg required amendments before
   results are examined; none was filed.

## Overall verdict

**H-REP (representational adequacy) SURVIVES** on structure formation:
hierarchy (2 and 3 levels), contradiction-driven split, and true overlap
all form as specified, verified white-box, no hardcoding, deterministic,
and scaling cleanly to 24 entities.

**Three downgrades applied:**
1. K5-v2/K2-v2/K4-v2 probe bars are CONFOUNDED by Step-0 lookup; they do
   not test concept inference. Adequacy currently rests on white-box
   structure evidence plus mini_world's 3 genuine inference probes.
   Bars must be redesigned with held-out probes.
2. MERGE is incomplete: identical-intent concepts under different parents
   are not unified (C2/C65, C3/C66).
3. SPLIT fires spuriously in some fixtures (C7/C8 here; C3-C6 in K5):
   reason=2 children with no contradiction present.

**Not L3.** The researcher correctly scoped the claim to representational
adequacy. Nothing in this red team upgrades it; the nine-criterion L3
assessment remains untouched.

## Evidence

- `fdcr_adversary/PREREG_FDCR_ADVERSARY.md` (frozen attacks)
- `fdcr_adversary/atk_fixtures/` (5 adversarial fixtures)
- `fdcr_adversary/atk_outputs/` (5 raw execution logs)
- This report.
