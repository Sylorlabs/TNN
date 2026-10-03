# PREREG: DEVINT-CLA2 - Developmental Integration on the Consolidated Workspace

**Experiment ID:** DEVINT-CLA2
**Worker:** DEVINT-CLA2 Prereg Author (subagent da206bbb-9b8c-46fa-8981-c8557500919e)
**Date (UTC):** 2026-09-30
**Status:** FROZEN. Committed alone before any implementation, build, or run.
**Verdict label target:** DEVINT-CLA2-PREREG-COMPLETE.

## 1. Mission and central question

DEVINT1 and DEVINT2 each demonstrated a full developmental sequence
(vocabulary, concepts, rules, contradiction, correction, inquiry, eviction,
interference, delayed reuse) in one persistent process on the OLD
fragmented substrate (separate rule stores, twin-store comparisons).
Both achieved BUILD-PASS.

CLA-2 dissolves those separate stores into ONE workspace with edge-type
conventions (commit `e639904f2`). Consolidation is only a win if
capability is preserved while mechanism count drops.

**Central question:** Does the CLA-2 unified workspace support the full
developmental sequence in one persistent process with no reset, no task
labels supplied to cognition, and no recompilation?

A pass validates the entire consolidation direction. A fail localizes
exactly which developmental demand the unified workspace cannot meet,
which is itself high-value: it tells us what the separate stores were
actually buying. This is the win-big/lose-informative symmetry that
ranked this frontier first by information gain.

Per the standing pipeline, the builder reports BUILD-PASS or BUILD-FAIL
only. No SURVIVES claim and no L3 claim is made here.

## 2. The CLA-2 substrate (frozen, as implemented)

The implementation under test is `cla2_build/cla2.zag` (commit
`e639904f2`), which implements the amended CLA-2:

- **7 core primitives:** ALLOC, READ, WRITE, LINK, ACTIVATE, DECAY,
  EXECUTE. EXECUTE(root, frame) dispatches over the closed 4-op ISA
  {MOVE, BRANCHEQ, INC, DEC}. No regularity detectors in core (frozen
  ISA boundary ruling).
- **Workspace:** one node store, fixed records (type_tag, ref[4],
  payload[4]), learner-assigned tags, one edge discipline.
- **Edge vocabulary:** DEPENDS-ON, SUPPORTS, CONTRADICTS, REFINES,
  INSTANCE-OF, USE, CONFIRMS, SURPRISE, PROTECTION, MEMBER, REGRET.
  No edge type names a domain concept.
- **Registers:** POLICY_ROOT (node 0), MISS_POLICY (node 1), 4-event
  context ring. Signed evidence bid: SUPPORTS/CONFIRMS/USE +1,
  CONTRADICTS -1.
- **Retention:** three-step routine (protection check, linear evidence
  aggregation, learner-owned cursor tie-break). GROUP nodes with MEMBER
  edges declare shared fate.
- **Miss handling:** exact-key, then SURPRISE, then MISS_POLICY,
  then HISTORY/REGRET, else -2.

The DEVINT-CLA2 implementation extends this substrate with the
developmental harness. The harness is experimenter infrastructure
(feed schedule, stage checks); it is NOT claimed as learned.

## 3. Domain (shared with DEVINT1 for direct comparability)

True morphemes (length 3, lowercase letters), unknown to the learner:

- M0 = "bik", M1 = "gup", M2 = "zol", M3 = "tav"

Raw episodes are concatenations of morphemes with no boundaries and no
labels, e.g. "bikgupzol". Character noise is injected in later stages
(frozen below). Using the identical domain as DEVINT1 makes the
shared-vs-new check separation (section 7) a direct regression
comparison: same inputs, new substrate.

## 4. Workspace-native mechanism mapping (frozen)

Every mechanism that DEVINT1/2 implemented with separate stores is
re-expressed here as workspace structure. This mapping is part of the
frozen prereg; the implementation may not invent parallel stores.

| DEVINT1/2 mechanism | CLA-2 workspace expression |
|---|---|
| Concept table | GROUP nodes with MEMBER edges to segment nodes; concept identity is group membership, not a table row |
| Relation bigrams | DEPENDS-ON edges between GROUP nodes with count in payload |
| Causal rule (PROVISIONAL/ACTIVE/ROLLED_BACK) | Executable graph node (EXECUTE-compatible) with SUPPORTS edges from evidence; state in payload; CONTRADICTS edges to superseded versions (revision is first-class, never silent overwrite) |
| Procedure pairing table | Executable graph (MAP/COPY ops) with SUPPORTS edges from training examples |
| Contradiction event | CONTRADICTS edge authored from OBSERVE; contradicted structure retained as superseded history |
| Inquiry | UNCERTAINTY node (SURPRISE edges on retrieval path) driving ACT via POLICY_ROOT; the 5-step ACT protocol selects the inquiry act |
| Eviction policy | Three-step retention routine over evidence bids; GROUP shared fate prices subgraphs |
| Twin-store control | REPLACED by workspace self-consistency checks (section 7); the old twin was a control for implementation bugs, the new control is 3/3 byte-identical determinism plus stage-by-stage baseline comparison |
| History/regret | HISTORY nodes and REGRET edges in the workspace, built from OBSERVE events by the event loop |

## 5. Frozen developmental sequence (11 stages)

The eleven stages are the experimenter's feed schedule. The learner
receives NO task-ID input and NO per-stage mode flag. Stage boundaries
exist only in the experiment log, verified by state-continuity checks.

- **S1 raw exposure:** 12 raw episodes (morpheme concatenations, lengths
  2..4 morphemes), no labels. Check: 12 fed; workspace non-empty.
- **S2 segmentation:** lexicon from substring statistics over S1 corpus;
  segment 6 new episodes. Check: 6/6 segmentations match DEVINT1's
  expected outputs exactly (zol|gup|bik, tav|zol|tav, gup|bik|zol,
  bik|tav, zol|gup, tav|gup|zol).
- **S3 concepts:** segments recurring at least twice become GROUP
  nodes with MEMBER edges. Check: 4 GROUP nodes; member patterns
  cover exactly {bik, gup, zol, tav}; zero spurious groups.
- **S4 relations:** GROUP bigrams counted over S1+S2 sequences as
  DEPENDS-ON edges. Check: 12 bigram edges (same count as DEVINT1).
- **S5 causal hypotheses:** induce "G_i predicts G_j next" as
  executable graphs with SUPPORTS edges; ACTIVE at support >= 3
  with zero refutes. Check: at least 4 ACTIVE rules (DEVINT1
  achieved bik->gup, gup->zol, gup->bik, zol->tav).
- **S6 procedures:** substitution procedure as executable graph.
  Pairing (frozen, hidden): M0<->M2, M1<->M3 (bik<->zol, gup<->tav).
  Check: 5/5 correct on held-out examples. Record examples-to-criterion.
- **S7 contradiction:** 4 episodes contradicting one ACTIVE rule;
  2 episodes violating a concept boundary. Check: >= 1 CONTRADICTS
  edge authored on a rule; >= 1 boundary-violation event logged.
- **S8 inquiry:** competing rules trigger UNCERTAINTY; ACT selects
  the inquiry act via POLICY_ROOT; world supplies the discriminating
  episode. Check: INQUIRY-equivalent act emitted (workspace-visible
  UNCERTAINTY node with ACT selection trace); discriminating episode
  consumed; exactly one rule survives as ACTIVE.
- **S9 revision:** contradiction protocol applied; SPLIT attempted on
  the boundary-violated concept (one GROUP replaced by two whose
  concatenation equals it, both recurring afterward). Check: >= 1
  demotion or rollback (CONTRADICTS edge with superseded history
  retrievable); accuracy on contradictory contexts measured
  before/after.
- **S10 memory management:** inject 20 distractor episodes (random
  morpheme orders plus 4 novel distractors "wex", "qiv") to exceed
  capacity; eviction via the three-step retention routine. Check:
  eviction occurs (>= 1 node evicted); post-eviction next-concept
  prediction accuracy on 10 held-out episodes measured; high-bid
  structures (signed bid >= 2) survive at higher rate than low-bid
  structures.
- **S11 delayed reuse and interference:** 6 delayed episodes reusing
  original morphemes in novel orders, interleaved with distractor
  probes. Check: (a) concept recognition: fraction of segments
  mapping to pre-S10 GROUP nodes >= 15/17; (b) procedure reuse:
  S6 pairing applied to a novel sequence, 3/3 correct; (c) no
  catastrophic interference: S5 ACTIVE rules still queryable.

## 6. Frozen synergy metrics (workspace-native)

DEVINT1's four synergy metrics used treatment/control twins. On the
single workspace, each is re-expressed as a workspace-native comparison.
All four are computed with exact integers.

- **M1 concepts -> procedure learning.** Run S6 procedure induction
  twice within the same process: once with GROUP-node concept
  vocabulary visible to the induction, once with GROUP nodes masked
  (segments only, same examples, same ops). Metric: examples-to-
  criterion n_visible vs n_masked. Synergy iff n_visible < n_masked.
  This tests whether the GROUP-node representation (not just the
  segments) carries the learning advantage.
- **M2 causal knowledge -> retention decisions.** After S10 eviction,
  partition surviving vs evicted nodes by signed evidence bid.
  Metric: fraction of nodes with bid >= 2 surviving vs fraction with
  bid <= 0 surviving. Synergy (retention is evidence-driven, not
  positional) iff high-bid survival rate exceeds low-bid survival
  rate by >= 40 points. Also verify zero positional-attractor
  signature (F1).
- **M3 contradiction -> representational refinement.** Count SPLIT
  refinements (one GROUP replaced by two, each recurring >= 2
  afterward). Metric: refinement count and accuracy on contradictory
  contexts before vs after S9. Descriptive; reported with exact
  integers.
- **M4 segmentation -> concept induction.** Episodes until the true
  4-morpheme inventory is fully covered as GROUP nodes, and spurious
  group count at that point. Shared check: DEVINT1 reached full
  coverage at k=5 with 0 spurious; DEVINT-CLA2 must match or the
  delta is reported as a consolidation cost.

## 7. Shared-vs-new check separation (frozen)

**Shared checks (regression against DEVINT1 baseline):** S2
segmentation outputs (6/6 exact), S3 inventory (4 concepts, 0
spurious), S4 bigram count (12), S5 ACTIVE count (>= 4), S6
criterion (5/5), S7 event counts (>= 4 contradictions, >= 2
boundary violations), S9 revision (>= 1 demotion/rollback),
S11 recognition (>= 15/17) and procedure reuse (3/3). A pass
may not hide a regression behind new checks: every shared check
is reported individually.

**New checks (workspace-native, no DEVINT1 baseline):** GROUP
nodes with MEMBER edges exist (white-box graph property);
rules are EXECUTE-compatible graphs (not table rows);
CONTRADICTS edges link live rules to retrievable superseded
history; UNCERTAINTY node with ACT selection trace at S8;
eviction follows the three-step routine (protection check,
bid aggregation, cursor tie-break) verified by bid-vs-survival
correlation (M2); no positional attractor (F1).

## 8. Frozen kill bars B1-B5

- **B1 persistence:** one compilation; all 11 stages in one process;
  STATE-CONT emitted after every stage with non-decreasing GROUP,
  rule-graph, and segment counts except where the frozen
  revision/eviction semantics explicitly remove entries; no boundary
  shows all tables empty after having been non-empty. Any
  unexplained emptying is a reset and VOIDS the run.
- **B2 stage function:** every stage check in section 5 passes with
  the exact numbers frozen there.
- **B3 blindness:** no stage labels, task IDs, mode flags, or domain
  identifiers reach cognition. Verified by source inspection: the
  harness feed path carries only episode bytes; the learner entry
  points (TEACH/QUERY/ACT/OBSERVE) take no stage parameter.
- **B4 interference:** S10 distractors include 4 novel morphemes;
  S11 interleaves distractor probes; post-interference S5 rules
  remain queryable and S11 recognition meets its bar. Clean
  selection under interference with recovery, no catastrophic
  forgetting of the original inventory.
- **B5 delayed reuse:** S11 reuses pre-S10 GROUP nodes and the S6
  procedure with zero re-teaching between S10 and S11. Any
  re-teaching of S1-S6 content in S11 VOIDS the reuse check.

**Determinism:** 3/3 runs byte-identical (raw output cmp clean),
exit 0, zero stderr bytes.

**BUILD-PASS iff B1 and B2 and B3 and B4 and B5 and determinism.**
Otherwise BUILD-FAIL. Negative synergy deltas do NOT fail the
build; they are reported honestly as data.

## 9. Falsification conditions

- **F1:** any positional attractor reappears (eviction or retrieval
  correlating with slot address rather than evidence bid). REJECT
  the implementation.
- **F2:** S5/S6 pass but S7/S9 fail: CONTRADICTS edges do not carry
  the revision semantics the old rollback had. NARROW the claim:
  the workspace stores contradictions but cannot revise on them.
- **F3:** S8 fails: UNCERTAINTY structures do not drive ACT
  selection. The inquiry half of the developmental sequence is
  absent on this substrate.
- **F4:** S10 eviction occurs but M2 shows no bid-vs-survival
  correlation: the three-step routine is not the actual retention
  decider. REJECT the implementation (core smuggling).
- **F5:** implementation requires any branch on stage identity,
  domain concept, or morpheme identity in the learner path.
  REJECT the implementation (not necessarily the design).

## 10. What failure would teach (localization table)

Each stage failure localizes a precise, falsifiable claim about
what the unified workspace cannot express. This is the most
valuable possible output of a fail.

| Failing stage | Localization: what consolidation cost |
|---|---|
| S2/S3 | Segmentation-to-concept pipeline broken in workspace terms; GROUP-node formation does not preserve the induction the table did |
| S4 | DEPENDS-ON edges do not carry bigram statistics the relation table did |
| S5 | Rule induction as executable graphs fails; the graph form loses something the rule record had (support/refute bookkeeping) |
| S6 | Executable procedure graphs do not support the pairing induction the table did |
| S7 | OBSERVE-to-CONTRADICTS path broken; contradiction not representable as edges |
| S8 | UNCERTAINTY-to-ACT path broken; the 5-step protocol cannot select inquiry from epistemic state |
| S9 | CONTRADICTS edges lack revision semantics; superseded history not retrievable or not constraining |
| S10 | Three-step retention misprices structures; evidence bids do not protect what the old policies did |
| S11 | Long-term persistence broken; GROUP/procedure structures decay or are unreachable after pressure |

## 11. Governance

- Pure Zag only: implementation, build, runs, and all analysis
  (grep/cmp/md5/diff via shell only). No Python anywhere
  including scratch. The worker-startup toolchain guard applies;
  Step 0 recorded in NAMECHECK.md.
- No em dashes in any documentation (byte-verified before commit).
- Owned paths only: `docs/lab/research-lead/overnight-20260928/devint_cla2_prereg/`
  for this prereg. The implementation worker will own a separate
  `devint_cla2_build/` path.
- This prereg is committed ALONE before any implementation.
  The implementation commit must be a strict descendant.
- Do NOT access sealed FW1-FW9 files. Builders stay blind.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: never
  edited, never cited as evidence. Zero-diff verified at commit.
- The builder reports BUILD-PASS or BUILD-FAIL only. No
  promotion to SURVIVES/BOUNDED/DOWNGRADED/KILLED; those require
  the full 11-step frontier pipeline including independent red team.
- The harness stage sequencing and feed schedule are authored
  infrastructure, not claimed as learned. The claims under test
  are workspace expressiveness, revision locality, retention
  policy, and developmental persistence only.
- Scope limits disclosed: morpheme domain shared with DEVINT1
  (comparability is the point); exact-match retrieval baseline;
  synthetic world.

## 12. Dependencies and ordering

- Requires CLA-2 implementation complete: satisfied (commit
  `e639904f2`, CLA2-BUILD-COMPLETE, 15/15 self-tests).
- Requires the C1 Zag-driver pattern for clean reruns: satisfied
  (commit `323f2afaa`, C1-REFREEZE-CLEAN).
- Should run after the COMP-1 composition implementation lands,
  since S8 inquiry and multi-fact queries benefit from plan
  execution. If COMP-1 is not yet implemented, S8 uses the
  5-step ACT protocol directly and the prereg stands unchanged.
- The MUL-from-ADD experiment (scouted) is independent; no
  ordering constraint.
