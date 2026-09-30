# ARENA PREREG AMENDMENT A4: Developmental TNN Contestant Entry

Date: 2026-09-30 UTC
Status: FROZEN before any contestant implementation or run.

## Purpose

Enter the ACTUAL developmental TNN (DEVINT1, the 11-stage continuing learner,
BUILD-PASS 4/4, independently reproduced) as a contestant in the CA-2 arena.
This is the first real contestant run. The hand-authored reference contestant
remains infrastructure self-test only.

## Contestant design

The contestant is a new pure-Zag program `devint1_contestant.zag` that:

1. Implements the frozen turn protocol from ARENA_PREREG.md section 5
   (reads turn.json, writes exactly one JSON reply line, maintains persistent
   state in statedir across the 131 process invocations).

2. Uses DEVINT1's actual learning mechanisms as its cognitive core:
   - W buffer (16384 bytes) with lexicon, concepts, rules
   - Incremental lexicon induction from observed strings
   - Concept formation from recurring units
   - Rule learning with support/refutation tracking
   - Contradiction detection and revision

3. Adapts arena exposures to the developmental learner:
   - Entity/attribute/value triples are encoded as raw sequences
   - The learner segments and forms concepts from these sequences
   - Test questions are answered by querying learned concepts/rules
   - No task labels or capability IDs reach the learning mechanisms

4. Does NOT use the reference contestant's hand-authored mechanisms.
   The reference contestant's fact store, causal hypothesis code, and Zem
   templates are NOT copied. Only DEVINT1's developmental mechanisms are used.

## What is NOT claimed

- This does not claim the contestant will score well. DEVINT1 was developed
  for morpheme segmentation, not the arena's 16 capabilities. Low scores on
  language-heavy or procedure-invention capabilities are expected and honest.
- This does not claim L3. The contestant uses DEVINT1's L2 mechanisms.
- The sealed seed is not viewed. No tuning to the seed is performed.

## Cost ledger

The harness meters costs externally per ARENA_PREREG.md section 7.
Additionally, the contestant logs internally (for learning-curve analysis):
- number of lexicon entries over time
- number of concepts over time
- number of active rules over time
- state buffer bytes used

Learning curves are produced at experience counts 1, 2, 5, 10, 25, 50, and
at the final turn, showing per-capability scores and cost metrics.

## BUILD-PASS / BUILD-FAIL for this entry

ARENA-RUN-COMPLETE requires ALL of:
  (a) this amendment committed alone before implementation;
  (b) contestant completes all 131 turns without crashing;
  (c) scorer produces per-capability scores;
  (d) cost ledger is complete;
  (e) learning curves are produced;
  (f) pure Zag, zero Python, zero em dashes;
  (g) sealed seed not viewed or tuned to;
  (h) arena world generation and scoring unmodified.

Otherwise ARENA-BLOCKED with specific blocker documented.

## Governance

- Owned path: docs/lab/research-lead/overnight-20260928/arena_tnn_entry/
- Commits local only. Nothing pushed.
- The arena's world/ directory is read-only for this work.
- If the contestant cannot complete the protocol, report ARENA-BLOCKED
  rather than modifying the arena.
