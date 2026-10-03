# Beam Architecture Review: Three Failed Generations

Date: 2026-09-30. Worker: Beam Architecture Reviewer.
Status: REVIEW ONLY. No implementation. No code written or modified.
No runs executed. Zero Python at every stage.

## 0. Standing rules name-check

1. Pure Zag only. This review is prose; no Python at any stage.
2. Byte checks via worker_snippets/check_no_dash.sh (shell only).
3. No em dashes in loop documentation.

## 1. Lineage under review

Three beam generations plus one diagnostic, all targeting R3 Arm 2
compositional reuse. Target E = OR(AND(D,Y4), AND(NOT(D),Y5)), 4 ops.

| Generation | Change | Result commit | Arm 2 A2-REUSE true/64 |
|---|---|---|---|
| Frozen baseline (023b4f84a) | n/a | R3-FAIL | 53 |
| Design 1 (27a8fd108) | niching + tax annealing + diverse IV | a2f95ef5d BEAM-FAIL, F-DIVERSE-FAIL | 50 |
| Unified U1-U7 (1f303396b) | species Pareto, two-phase tax, diverse IV, ties, novelty floor | fc03664f2 BEAM-UNIFIED-FAIL, F-DIVERSE-FAIL + F-NODOM + F-BLOAT | 52 |
| G0 diagnostic (446233dd5 design) | instrumented copy of failing unified beam | 2faf4196d G0-MERGED | n/a |
| G2 (d4485706f prereg) | refutation-seeking IV policy | c0babffab G2-FAIL, F-DIVERSE-FAIL | 49 |

Trajectory: 53 -> 50 -> 52 -> 49. Flat to negative across three
repair generations.

Purity note: Design 1 (a2f95ef5d) carries a disclosed K4 incident
(no-op python3 after scored runs); its numbers stand as
deterministic negative evidence, not K4-clean. Unified (fc03664f2),
G0 (2faf4196d), and G2 (c0babffab) are K4-clean.

## 2. What the evidence establishes

Finding 1: the bottleneck is generation of behaviorally good
candidates, not retention or selection. G0 (prereg eb0ff7fdf) found
exactly 4 Q-signature candidates across 25 rounds, all in round 2,
with evidence accuracies 1, 1, 1, 9 of 64. The generator proposes
E-shaped structure once, briefly, and never with behavioral
accuracy. PROPOSED_Q=4, MERGED_Q=4, RETAINED_Q=0, PRUNED_Q=0.

Finding 2: retention repair does not move Arm 2. Design 1 added
niching; unified added Pareto retention, two-phase tax, and a
novelty floor. Arm 2 stayed at 50 to 52 against the 53 baseline.

Finding 3: selection repair does not move Arm 2. Design 1 added
diverse IVs; unified kept them; G2 added refutation-seeking IVs.
Arm 2 went 52 -> 49 under G2, worse than baseline.

Finding 4: the merge rule is not the binding constraint. G0
resolved branch (b) structurally, but the merged candidates had
near-zero accuracy. G2 pre-registered alternative explanation A1
("merged, then would have lost anyway") with two kill conditions;
condition (b) failed definitively (no Arm 2 improvement), so A1
SURVIVES. A merge-rule fix (G1) would protect candidates that lose
on accuracy regardless.

Finding 5: the scoring landscape selects against the truth.
Post-mortem Cause 4 (47d5c0137): at full fit, the 3-op overfitter
outscores the true 4-op E under the tax by design. Escape requires
refuting evidence. Three generations of IV policy work have not
produced it.

## 3. Is the current representation itself wrong?

Decompose into three levels.

Level 1: program representation (trees over AND, OR, XOR, NOT).
Expressively adequate. E is a 4-op tree inside the alphabet. Not
wrong in the expressiveness sense.

Level 2: search representation (pairwise combination generator plus
evidence-fit scoring plus opc tax). This is where the failure
lives. E requires a coordinated two-round composition: AND(D,Y4)
and AND(NOT(D),Y5) must both be proposed in some round, both
survive retention, then be OR-combined in a later round. Each
intermediate alone has poor evidence accuracy, so the scorer gives
it no value and retention drops it. The search has no representation
of partial compositional progress. No gradient points toward E.

Level 3: the conditional-structure hypothesis. Semantically, E is a
conditional: if D then Y4 else Y5. The tree prior makes this a 4-op
coordinated discovery with unrewarded intermediates. A
representation with conditionals as first-class primitives would
make it a one-step composition. The tree-of-Boolean-ops prior puts
the conditional form at very low proposal probability. This is a
representation-level mismatch between the target class
(dispatched/conditional structure) and the search prior, not an
expressiveness gap.

Answer: the program representation is adequate, but the search
representation is structurally mismatched to compositional targets
with unrewarded intermediates. Three generations of downstream
repair confirm the bottleneck is not where the repairs were
applied. In the sense the architecture-review rule intends, yes:
the representation of the search (levels 2 and 3) is itself wrong
for this target class, and further retention/selection tweaks are
not justified.

## 4. Untested branches

G1 (merge-rule fix, branch-(b)-gated in BEAM_NEXT_DESIGN.md section
4): never built. A1's survival removes its premise. Building it now
would be a fourth adjacent tweak against the evidence. Do not build.

G3 (compositional generation moves: splice, library-embed):
permitted by the design's honest fallback clause, never built. It is
the last untried search-level direction. Caveat: splice assembles
subexpressions of existing beam members, but G0 shows the beam never
holds behaviorally good compositional intermediates, so splice has
little to assemble. Expected value is low, but it honestly exhausts
the search level. Any G3 prereg must carry the F-CASE hard kill
(target-shaped moves kill on the spot) and A1's kill conditions.

Representation-level alternative (conditional primitives or
equivalent): a new mechanism, not a beam tweak. Requires its own
preregistration, its own falsifiers including F-CASE against
target-shaped primitives, and must respect the pure-Zag red line.
For now it would be a bounded-L2 search-architecture experiment;
no L3 or Criterion 0 claim attaches.

## 5. Recommendation

Primary: pivot to representation-level investigation. Open a new
design lane for conditional-first program search (or equivalent)
with a fresh preregistration. Do not continue the beam
retention/selection lineage.

Secondary (optional, parent's call): run G3 as a single terminal
search-level experiment with A1's kill conditions carried forward,
to exhaust the search level honestly. If G3 fails, close the beam
lineage for compositional targets.

Do not: build G1, any further retention/selection variant, or a G4.
The three-generation rule has fired; the evidence says the repairs
are at the wrong level.

Lane disposition: the beam lane stays open for R1-style
evidence-fit and FREC-style tasks where it has not been killed, but
the R3 Arm 2 compositional target is closed to further beam-tweak
generations pending the representation pivot.

## 6. Kill bars

- K1 (review complete): PASS. This document.
- K2 (all generations analyzed): PASS. Sections 1 and 2 cover
  Design 1, unified, G0, and G2 with committed hashes.
- K3 (no implementation): PASS. Prose only. No .zag written or
  modified, no binaries built, no runs executed.

## 7. Governance notes

- Zero Python at every stage of this review.
- The contaminated research paper was not touched.
- No other worker's files were touched. This commit contains only
  this review document under beam_review/.
- Commits local only, explicit pathspec, nothing pushed.

BEAM-REVIEW-COMPLETE.
