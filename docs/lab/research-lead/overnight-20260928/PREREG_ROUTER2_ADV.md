# PREREG_ROUTER2_ADV: Adversary Preregistration Against H-ROUTER2

**Status:** FROZEN. No edits after this commit except an explicit amendment
record. Execution must strictly follow this document.

**Date:** 2026-09-29
**Target:** H-ROUTER2 SURVIVES (commit `313b840ed`). Claim: routing predicates
are LEARNED from an 18-item marked curriculum via causal SPLIT machinery, not
authored. 16/16 suite + novel, 4/4 withhold, deterministic.
**Adversary stance:** Assume the claim is false. Attack it.

## Attack X-R1: Curriculum gaming (wrong but consistent marks)

**Method:** Build a variant curriculum where str>str multi-segment items
(features s0=1, s1 in {2,3,4}) are marked CAUS_LEARN (12) instead of
PROC_LEARN (11), keeping everything else identical and consistent (no two
items share features with different marks). Run the learner.

**Kill criterion:** If the learner induces s0=1 -> CAUS_LEARN rules with no
inconsistency flag, no abstention, and no diagnostic distinguishing this run
from the honest run, then the routing "knowledge" is fully determined by
researcher-supplied marks. H-ROUTER2 is DOWNGRADED from "learner induces the
routing policy" to "learner reformats researcher-supplied routing decisions
into white-box entries." The policy content never left the researcher.
(Supervised fidelity is not policy invention.)

**Pass criterion (claim survives):** The learner flags the curriculum as
suspicious, abstains, or emits a diagnostic distinguishing mark-driven
memorization from genuine induction. (Not expected; recorded for honesty.)

## Attack X-R2: Feature-extractor boundary collisions

**Method:** Craft boundary strings and verify the authored feature extractors
produce the documented feature values, then check routing:
(a) `ab>ba>cd` (two `>` in one segment): expect s0=3 (mixed), route WITHHOLD.
(b) `a1>b2` (alphanumeric sides): expect s0=1 (non-numeric includes
alphanumeric), check route.
(c) `1,2,3>4,5` with trailing spaces / ` 1,0,0 ` (whitespace): check s2
classification and route.
(d) `AB>BA;CD>DC` (uppercase): expect s0=1, s1=2, route PROC_LEARN.
(e) `ab>ba;` (trailing empty segment): check nseg counting and route.

**Kill criterion:** If any boundary string produces features the prereg does
not document AND the learner routes it CONFIDENTLY (non-WITHHOLD) to a task
code, then the authored extractors create silent misrouting surface the
"learned" claim does not cover. H-ROUTER2 is DOWNGRADED: routing correctness
depends on undocumented extractor behavior, not on learned predicates.

**Pass criterion:** All boundary strings either map to documented features or
route WITHHOLD.

## Attack X-R3: Threshold divergence from H-ROUTER

**Method:** The H-ROUTER2 hypothesis states the induced predicates match "the
authored H-ROUTER decisions." H-ROUTER's authored predicate is "if 2+ segs,
str>str then PROC_LEARN" (a threshold). H-ROUTER2 induces per-value rules
(s1=2, s1=3, s1=4 -> PL) and WITHHOLDS on nseg=5 (K-R2C explicitly requires
WITHHOLD on `(1,5,0)`).
Run H-ROUTER's authored logic (from `route_learn.zag`) and H-ROUTER2's
induced rules on str>str inputs with nseg = 5, 6, 7, 8, 9. Compare.

**Kill criterion:** If H-ROUTER routes nseg>=5 str>str to PROC_LEARN while
H-ROUTER2 WITHHOLDS on all of them, then the induced policy DIVERGES from the
authored H-ROUTER decisions on a principled input class. The hypothesis
sentence "matching the authored H-ROUTER decisions" is FALSE outside the
curriculum range. H-ROUTER2 is DOWNGRADED to "learns a per-value
approximation of the routing policy that withholds outside the curriculum
range; does not recover the threshold."

**Pass criterion:** The policies agree on all tested nseg values (would
require the learner to have generalized the threshold, contradicting the
documented boundary; not expected).

## Attack X-R4: Source audit for hardcoded rules

**Method:** Grep `router2_learn.zag` for:
(a) task-code literals (10, 11, 12, 13, 14) outside the `TC_*()` definitions,
the `teach()` curriculum calls, and the `check_route()` test expectations;
(b) feature-value literals (s0=1, s1=2, etc.) in any routing decision logic
outside the generic SPLIT machinery and the test driver;
(c) any conditional whose branches return different task codes based on
feature values (i.e., an authored routing predicate hiding in the
implementation).

**Kill criterion:** If any routing decision logic contains hardcoded
feature-to-task mappings (e.g., `if s0==1 && s1>=2 return TC_PL()` or a
lookup table from features to task codes used at route time), then the "11
induced rules" did not all come from SPLIT machinery. H-ROUTER2 is KILLED.

**Pass criterion:** The only feature-to-task mappings at route time flow
through the generic `predict()` over SPLIT-induced hypothesis entries.

## Verdict rule

- X-R4 kill => H-ROUTER2 KILLED.
- Any of X-R1, X-R2, X-R3 meeting kill criterion => H-ROUTER2 DOWNGRADED
  (survives in narrowed form; the specific narrowing is documented).
- All four attacks failing to meet kill criteria => H-ROUTER2 SURVIVES
  unmodified.

## Scope notes

- Pure Zag. No Python anywhere, including verification and analysis.
- No em dashes in loop documentation.
- The adversary does not modify `router2_learn.zag`. Attack harnesses are
  separate files (`router2_adv*.zag`) or shell-driven reruns of the existing
  binary where the binary already exposes the needed behavior.
- Commit order: this prereg strictly before any attack execution commit.
