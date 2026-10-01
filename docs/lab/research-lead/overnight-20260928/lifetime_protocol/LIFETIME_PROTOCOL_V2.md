# LIFETIME EVALUATION PROTOCOL (V2, DRAFT-NOT-FROZEN)

Date: 2026-10-01. Updater: Lifetime Protocol Updater (subagent).
Status: DRAFT. Not frozen. For Micah's review. No implementation exists.
Supersedes: `LIFETIME_PROTOCOL_DRAFT.md` (v1, commit 9474bc232), which is
left untouched in this directory for the review trail.

## 0. Changelog: v1 to v2

Seven analyses completed after v1 was written. Each change below names
its source. Unchanged sections are carried forward verbatim; changed
sections are marked [v2].

1. **K-LT-5 refined with the operational learning-to-learn definition**
   (source: `l2l_analysis/L2L_ANALYSIS.md`, commit 106ee6698). Four
   observables in priority order; minimal measurable unit specified;
   weak vs strong K-LT-5 distinguished; H3-lite honestly calibrated
   (weak should pass via Node 1, strong should fail without conditional
   policies); the uncertainty-dedup gap named as residual. L2L2 cited
   as the reference implementation with corrected status (see item 8).
   Affects: Sections 7.8, 11 (K-LT-5), 13, 14.

2. **New white-box event types** (sources: eviction corruption 986c52fdc,
   theater audit e0423538a, decline signal 9e0ae81d1, goal origination
   3bf4d7bb4). CORRUPTION (silent structural destruction, driver-detected);
   ZOMBIE as a retention-sweep state classification; THEATER_GUARD
   (protocol-level exclusion of T1-T6 from learner-owned counts);
   DECLINE (withhold vs guess, defined for future builds; frozen TNN-2
   expected to log zero genuine declines); GOAL_* reserved but marked
   NOT-APPLICABLE for frozen TNN-2. Affects: Section 6.

3. **Honest TNN-2 predictions updated** (sources: state dynamics
   ee238d8d4, forgetting 2726baf74, eviction corruption 986c52fdc,
   verification criterion c2a48bee6). K-LT-2 gains the corruption caveat
   (beyond budget, structures are corrupted first, not cleanly evicted).
   K-LT-4 gains the V2-hole caveat (revision acceptance never checks
   `out == new_o`; a wrong-but-running repair would be accepted). New
   baseline dynamics diagnostic: per-experience cost constancy check
   ("write-mostly, not living" profile). Affects: Sections 7.7, 11, 13.

4. **World-design rule from the H2 void** (source: `h2_eval/H2_EVAL_REPORT.md`,
   commit 72173fe11, H2-EVAL-VOID). If a teach stream contains direct
   facts for a probe (s,r), `activate` succeeds and the trial never runs.
   Each lifetime probe must now declare whether the trial is expected to
   run; world-design validation check added. Affects: Section 4 (new 4.1).

5. **Theater guard** (source: theater audit e0423538a). The six theater
   instances (T1 MISS_POLICY, T2 P-INV threshold, T3 trial stats, T4 event
   log, T5 UNCERTAINTY fields, T6 eviction history) are excluded from
   learner-owned state in every measure. The POLICY event type is
   restricted to nodes with both production read and write paths.
   Affects: Sections 6, 7.8, 18.

6. **Spontaneity caveat** (source: goal origination 3bf4d7bb4). TNN-2 is
   purely reactive (no self-invocation, R2 gap). "Spontaneous" in this
   protocol means not-harness-labeled (no task labels per Micah's
   clarification), not self-initiated. The stronger reading is marked
   as requiring future architecture. Affects: Section 8.

7. **Fossil inversion in the interference measure** (source: forgetting
   2726baf74). Memory-under-interference now distinguishes four
   end-states: live, deleted, fossil (accidental), zombie (corrupted).
   Fossil and zombie counts are reported diagnostics. Retirement
   (excluded from lookup, low cost, recoverable) does not exist in
   frozen TNN-2; per Section 7.7 it would become a fifth end-state
   only if a future build implements it. Affects: Section 7.7.

8. **L2L2 reference status corrected** (sources: `l2l2_audit/` commit
   af9a9765a; `l2l2_repair/` prereg amendment 0872a412d, implementation
   a530028ea, REPAIR-PASS). The original L2L2 ablation claim (P3) was not
   performed as specified; the repair ran mode 2 properly (B_ABL=13,
   3/3 byte-identical) and closed P3 under the amended prereg. L2L2 may
   now be cited as ablation-verified, referencing the repair, not the
   original misdescribed result. The original BUILD-PASS (5/5) verdict
   is not retroactively validated. Affects: Sections 7.8, 11 (K-LT-5).

9. **New Section 19: decisions requiring Micah.** Banked explicitly:
   H2 repair path, H3-lite vs lifetime ordering, which build(s) to run,
   protocol freeze decision.

10. **CORRUPTION detector algorithm specified** (source:
    `corruption_detector/CORRUPTION_DETECTOR.md`, commit ff2d1e1ef).
    Changelog item 2 defined the CORRUPTION event type; this update
    specifies the driver-side detection algorithm: two-pass MAP
    field-20 root validator, valid-root set {101,102,103,104} grounded
    in `t2_exec` semantics, canonical snapshot format with SHA-256,
    classification taxonomy (BOOTSTRAP, Z_RANGE, FOSSIL, VALID,
    ZOMBIE, Z_SHARED, Z_HIJACKED), onset-only transition rule,
    world-granular attribution caveat, EVICT vs CORRUPTION
    distinction, shared-root landmine rule for future revision
    machinery, and three recommended extensions (guard field-12
    target, literal-operand field 8, policy-anchor liveness).
    Affects: Sections 5 (step 4a), 6 (new 6.2), 7.7, 18.

11. **QA corrections** (source: `protocol_qa/PROTOCOL_QA.md`, report
    a125a1984). Changelog item 7 now names the four Section 7.7
    end-states (live, deleted, fossil, zombie) instead of the stale
    "retired (future)"; the P4 profile referenced in K-LT-2 is
    defined in-document with its source (`tnn2_transfer/
    TRANSFER_ANALYSIS.md` P4 result); "H1 widening" in Section 17
    is defined in-document with its source (`tnn3_roadmap/
    TNN3_ROADMAP.md` section 2). Affects: Sections 0, 11, 17.

## 1. Purpose

This protocol operationalizes Micah's 2026-10-01 architecture
clarification: TNN is a continuous adaptive learner. "Freeze" means freeze
researcher-authored architecture and source for controlled scientific
evaluation. It does not mean freeze the learner.

The scientific ideal under test:

FROZEN RESEARCHER CODE + CONTINUOUSLY CHANGING LEARNER STATE.

That is stronger evidence than continually editing source code.

This protocol is the primary long-term AGI evaluation track. It sits
alongside (not replacing) isolated reset-based tests, which remain
useful for causal attribution. Where a fresh start is needed, it is
reported separately as an isolation test. The lifetime track is the
primary measure of whether one frozen architecture accumulates a
richer, more interconnected internal world over experience.

[v2] The state-dynamics profile (ee238d8d4) sharpens what "continuously
changing" must mean to count as evidence: TNN-2's state changes
continuously (427 nodes over ~260 experiences) but with exactly constant
per-experience cost, zero reuse, and duplicated structures on repeated
experiences. The protocol therefore instruments not just that state
changes, but whether the change is adaptive: the per-experience cost
constancy check (Section 7.8, new diagnostic DYN-1) is a standing
requirement. Stasis of the learning process itself, under changing
state, is reported as a finding, not a pass.

## 2. What "freeze" means in this protocol

FROZEN (researcher-owned, fixed before the lifetime begins):

- TNN source code (the frozen build under test).
- Protected ISA (the 4-op basis: MOVE, BRANCHEQ, INC, DEC).
- Compiler (pinned znc).
- Evaluator protocol (this document, once frozen): world sequence,
  teach streams, probe sets, scoring rules, instrumentation spec.
- World contents: teach events and sealed probes are fixed in advance.
  The learner never sees probes during teaching.

NOT FROZEN (learner-owned, free to change throughout the lifetime):

- Learner state (workspace W in full).
- Memory growth (new nodes up to the architecture's budget).
- Structural creation (new MAPs, facts, edges, hypotheses).
- Revision (contradiction-driven updates, in place or copy-and-commit
  per the approved substrate experiment).
- Policy learning (H3-lite policy nodes, if that build is the subject).
- Representation formation (any learner-created structure).
- Retention priorities, action policies, forgetting and compression.

[v2] Theater guard: the NOT-FROZEN list does not include the six
theater instances (T1-T6, Section 6.1). A node with no production read
path, or no exercised production write path, is not learner-owned state
for any measure in this protocol, regardless of where it lives in the
workspace.

A lifetime run that shows no learner-state change is a failed run of
the protocol, not a passing run of the architecture. The protocol
instruments state change; stasis is evidence against plasticity.

## 3. Two-track reporting structure

Every lifetime claim is reported on two tracks.

### 3.1 ISOLATION TRACK (causal attribution)

Five separate learners, each starting from a blank workspace. Learner
i receives only world i's teach stream (i in {A, B, C, D, A'}), then
answers world i's sealed probes. No cross-world state.

Purpose: what does world X teach a naive learner, and how many
teaching events does it take. This is the control condition for every
lifetime comparison. It also detects worlds that are trivially easy
or impossibly hard independent of history.

### 3.2 LIFETIME TRACK (the primary evaluation)

One learner. Worlds arrive sequentially: A, then B, then C, then D,
then A'. No process reset. No learner-state reset. No task labels.
No recompilation. The teach stream is one continuous sequence; the
learner is never told which world it is in.

Purpose: measure whether earlier experience changes how later
experience is learned, retained, revised, and reused.

### 3.3 Comparison discipline

For each world X, report the paired triple:

- E_iso(X): teaching events to criterion, isolation learner.
- E_life(X): teaching events to criterion, lifetime learner at the
  point X arrives in the sequence.
- Probe scores for both on X's sealed probes.

Transfer is the difference. No lifetime number is interpretable
without its isolation control.

### 3.4 Determinism

Three byte-identical runs per track per world (same rule as the
frozen evaluations: K-FZ2-4, FW, GW). A measure that is not stable
across three runs is reported as unstable, not as a result.

## 4. World sequence

Five worlds. Each world has a teach stream (ordered teaching events)
and a sealed probe set (held-out queries never taught in any world).
Worlds are materially different in subject domain and relation use.
They are not variants of FW1-FW9.

Subject pools are disjoint across worlds except where cross-world
links are explicitly designed (world B). Relation vocabulary is the
frozen TNN-2 set (chain, count, sum families). No new relations are
introduced by the researcher mid-lifetime; that would be a source
change, not learner growth.

### 4.1 [v2] World-design validation: the trial-must-run rule

Source: H2 void (72173fe11). The H2 trap worlds included direct OBSERVE
facts for the query (subject, relation). In `ev_query`, `activate`
finds those facts and returns immediately; the trial (`t2_trial`) never
executes. All H2 probes, including unmasked controls, returned direct
facts (wrong answers). The discrimination gap was zero. The evaluation
was void.

Rule: for every probe in every world, the world designer must declare
TRIAL-EXPECTED (the trial must run for this probe) or LOOKUP-EXPECTED
(direct fact retrieval is the intended path). If TRIAL-EXPECTED, the
world-design validator must confirm that the teach stream contains no
direct fact for the probe's (s, r) that `activate` would find first.
This check is performed on the sealed teach stream by hash-verified
validator code before the freeze, without revealing probe answers.

A world that violates this rule for a TRIAL-EXPECTED probe is rejected
at design review, not patched after the run. The H2 precedent (design
defect discovered only at evaluation) must not repeat.

### WORLD A: foundation chains (the baseline skill)

- Subjects: 1..10.
- Teach: 2-hop and 3-hop chain facts, enough for the trial loop to
  assemble and promote chain MAPs. Include redundant licensing facts
  so provenance is nontrivial.
- Tests: can the learner acquire a verified executable procedure and
  answer held-out chain queries.
- Sealed probes: 10 chain queries on subjects 1..10, (subject,
  relation) pairs never taught. TRIAL-EXPECTED.
- Criterion: 10/10 probes correct.
- Records the baseline E(A): examples to first criterion.

### WORLD B: dependent domain (forward transfer probe)

- Subjects: 11..20.
- Design: B's chains are built so that their premises include facts
  about A's subjects. Concretely, some B-chain links pass through
  subjects 1..10 (cross-subject edges taught as ordinary facts in
  B's teach stream, referencing A's entities). B cannot be solved
  from B's novel facts alone; the trial loop must recruit A's facts
  as licensing premises.
- Tests: does A's knowledge reduce B's learning cost (forward
  transfer at the fact level), and does the white-box log show A's
  facts in B's MAP provenance.
- Sealed probes: 10 B-chain queries, held out. TRIAL-EXPECTED.
- Criterion: 10/10 probes correct.
- Key comparison: E_life(B) vs E_iso(B). The isolation learner must
  be taught A's referenced facts inside B's stream (same byte
  content the lifetime learner already holds), so the difference
  isolates retention and recruitment, not missing information.

### WORLD C: contradiction and revision (revision safety probe)

- Subjects: 1..10 (A's domain) plus 2..3 bridging subjects.
- Design: a subset of A's licensing facts is contradicted by new
  observations (same protocol as the FW revision worlds: observe,
  contradict, revise). The contradictions target A's facts that are
  NOT premises of B's MAPs (revision must be surgical) plus one
  fact that IS shared (revision must propagate correctly).
- [v2] V2-hole trap (source: verification criterion c2a48bee6):
  at least one contradiction in world C must be paired with a probe
  that detects wrong-but-running repair acceptance. `t2_revise_graph`
  accepts any repair with `out != -999999` and never checks
  `out == new_o`. World C includes one contradiction whose correct
  repair the trial cannot produce by literal patch alone; if the
  learner's revision is accepted anyway, the probe records a
  V2-HOLE event. This tests whether the revision path has any
  correctness check beyond successful execution.
- Tests: does revision correct A's answers without destroying B's
  capability (no collateral damage), and does the MAP-level white
  box show in-place revision with provenance retargeting.
- Sealed probes: 10 probes (5 revised-A queries with corrected
  answers, 5 B queries that must be unchanged), plus the V2-hole
  trap probe. TRIAL-EXPECTED for the revised-A probes.
- Criterion: 10/10 (5 correct-after-revision, 5 unchanged); V2-hole
  trap reported separately.
- Key comparison: B-probe retention, lifetime vs a control that
  skips world C.

### WORLD D: novel composition (cross-domain procedure probe)

- Subjects: 21..30.
- Design: a new relation family (count/sum) on fresh subjects, but
  the underlying regularity has the same abstract shape as A's
  chains (iterated binary combination with a literal guard). A
  learner that could recognize procedure shape across domains
  would adapt A's MAPs. TNN-2's graphs are subject-bound (literals
  baked in; transfer analysis 2026-10-01), so the honest
  expectation is rebuild, not reuse. The world is designed to make
  that expectation falsifiable: if any MAP from A is executed
  during D, the white-box log will show it.
- Tests: the boundary between fact-level reuse (possible) and
  procedure-level reuse (architecturally blocked in TNN-2).
- Sealed probes: 10 count/sum queries, held out. TRIAL-EXPECTED.
- Criterion: 10/10 probes correct.
- Key comparison: E_life(D) vs E_iso(D), plus the cross-domain
  execution event count (expected zero for frozen TNN-2).

### WORLD A': return (backward transfer and retention probe)

- Subjects: 101..110 (fresh; A-like in structure, new in surface).
- Design: same chain structure as world A, all-new subjects. No
  fact overlap with A. This isolates procedure-shape transfer
  from fact retention.
- Tests: (a) retention: original A probes (subjects 1..10) still
  answerable after the interference of B, C, D; (b) learning-rate
  transfer: does the lifetime learner reach criterion on A' in
  fewer events than a naive learner.
- Sealed probes: 10 A'-queries (new subjects) plus the 10 original
  A probes (retention check). TRIAL-EXPECTED for A' probes.
- Criterion: 10/10 on A' probes; retention reported separately.
- Key comparisons: E_life(A') vs E_iso(A'); retention score vs
  the 1024-node budget state at A' arrival.

## 5. Lifetime procedure (normative)

1. Build the frozen subject binary once. Record source, binary, and
   protocol hashes.
2. Initialize one workspace W (blank).
3. Stream worlds in order A, B, C, D, A'. The driver feeds teach
   events; the learner may query, act, and revise at any time per
   its own cognition. The driver never labels the world.
4. After each world's teach stream, run that world's sealed probes
   (read-only; probes never enter learner state as teaches).
5. Continue streaming. No resets between worlds.
6. At the end, run all five probe sets once more (final retention
   sweep) on the same unbroken learner state.
7. Repeat steps 2-6 two more times (three runs total). All
   white-box logs must be byte-identical across runs or the
   instability is reported.

Isolation procedure: same, but five learners, each receiving exactly
one world's teach stream from a blank workspace, then that world's
probes. Steps 6-7 apply per learner.

[v2] Step 4a (new): at each world boundary, the driver takes a
white-box snapshot and runs the corruption detector (Section 6.2,
CORRUPTION events) and the theater guard (Section 6.1). Snapshot
hashes are committed to the run log. This makes silent structural
destruction visible even though the learner itself cannot detect it.

## 6. White-box instrumentation spec

The driver (researcher-side harness; cognition untouched) logs the
following event stream. Every event carries: run id, track
(isolation/lifetime), world id at event time, learner clock
(event sequence number), and node ids. This is the evidentiary
basis for every transfer claim. A claim without a log signature is
not a finding.

- TEACH(world, s, r, v, node): every fact teach with its node id.
- PROMOTE(world, map, s, r, root, prov[] ): every graph promotion:
  MAP node id, subject, relation, graph root cell, list of
  licensing fact node ids (the ET_DEP provenance edges).
- EXEC(world, map, query, result): every execution of a stored MAP
  outside the trial loop that built it (the reuse-path query
  behavior). Includes which query triggered it.
- QPATH(world, query, path): for every probe: fact_hit, map_exec,
  trial, or miss. Which node served the answer.
- REVISE(world, map, old_ans, new_ans, trigger): every revision:
  which MAP, answer before/after, the contradicting fact node.
  Records whether the MAP node id was preserved (in-place) or
  replaced (copy-and-commit, per the approved substrate).
- EVICT(node, type, origin_world): every node eviction under memory
  pressure: what was lost and which world created it.
- POLICY(world, node, field, old, new): every write to a learner
  policy node (H3-lite), with the triggering experience id.
  [v2] Restricted: only nodes with both a production read path and
  an exercised production write path qualify. Theater nodes (T1-T6)
  are excluded by the theater guard (Section 6.1).
- FORGET(world, node, reason): every compression or retirement of a
  structure the learner (not the budget) initiated, if the
  architecture supports learner-initiated forgetting.

### 6.1 [v2] New event types

- CORRUPTION(world, map, field, expected_type, actual_type): silent
  structural destruction detected by driver snapshot comparison.
  Source: eviction corruption analysis (986c52fdc). MAP roots are
  stored as field-20 integers, not edges; `evict_node` cleans edges
  but cannot see field-based references, so evicted graph cells
  leave surviving MAPs pointing at wrong node types (zombie MAPs).
  The learner cannot detect its own corruption; the driver must,
  by comparing MAP root fields against node types at each world
  boundary snapshot (detection algorithm: Section 6.2). Each
  corruption is a distinct event from EVICT: EVICT is clean
  removal, CORRUPTION is silent invalidation of a surviving
  structure.
- ZOMBIE-STATE(world, map, status): retention-sweep classification.
  At the final sweep, every MAP is classified: LIVE (root valid,
  executable), FOSSIL (root cells evicted, MAP inert but occupying
  budget; the forgetting-analysis inversion of retirement), ZOMBIE
  (root field points to a wrong-typed node; corrupted), DELETED
  (evicted cleanly). Fossil and zombie counts are reported
  diagnostics, not just node counts.
- THEATER_GUARD(world, node, class): protocol-level assertion, run
  at each world boundary. For each of the six theater instances
  (T1 MISS_POLICY node, T2 P-INV threshold, T3 trial stats, T4 event
  log, T5 UNCERTAINTY fields, T6 eviction history), the driver
  verifies the classification still holds (no production read path
  has appeared for write-only nodes; no write path has appeared
  for read-only nodes). If a future build gives a theater node a
  genuine read path, the guard reports the reclassification and the
  node becomes eligible for learner-owned counts. Until then, no
  measure in this protocol may cite T1-T6 as learner-owned state.
- DECLINE(world, query, outcome): records withhold-vs-guess behavior.
  Source: decline-signal analysis (9e0ae81d1). Frozen TNN-2 has no
  "should I answer" gate; the -2 return is pipeline exhaust (five
  distinct situations overloaded on one sentinel), not a cognitive
  choice. For frozen TNN-2, the driver logs every -2 with its
  producing path (disambiguated by driver instrumentation), and the
  expected count of genuine declines is zero. The event type is
  defined so future builds with a real withhold criterion can be
  measured on the same log schema.
- GOAL_* (reserved, NOT-APPLICABLE for frozen TNN-2): GOAL_FORM,
  GOAL_PURSUE, GOAL_SATISFY, GOAL_ABANDON. Source: goal origination
  (3bf4d7bb4). TNN-2 is purely reactive: all four event handlers
  have zero internal callers, there is no learner tick, no goal
  representation exists in production. These event types are
  specified here so the schema is stable when a future build
  implements R1-R6; for frozen TNN-2 they are defined but never
  fire, and the protocol reports their absence as a finding about
  the architecture, not a gap in the instrumentation.

### 6.2 [v2] Corruption detector (driver-side)

Source: `corruption_detector/CORRUPTION_DETECTOR.md` (commit
ff2d1e1ef). Driver-side (researcher harness), read-only,
deterministic. Same workspace state always yields the same
classification. The learner cannot detect its own corruption; this
detector makes silent structural destruction visible.

1. **When it runs.** At each world boundary per Section 5 step 4a
   (after the teach stream completes, before the next world's
   stream begins) and at the final retention sweep. Attribution
   caveat: CORRUPTION events are emitted at boundary processing
   time, but the corruption occurred at some unknown point during
   the preceding world's stream. The `world` field names the world
   whose stream just completed. This is world-granular
   attribution, not event-granular; measures must not treat a
   CORRUPTION event as timestamped to the boundary tick.

2. **Snapshot format.** For every live (field 36 == 1) tag-20
   node, one canonical line:

   ```
   MAP <id> <root> <root_tag_or_dead> <promo_index>
   ```

   where `<root>` is the field-20 value, `<root_tag_or_dead>` is
   the node tag at root if the root node is live and else the
   literal token `dead`, and `<promo_index>` is field 24 (the
   promotion nonce). Lines sorted by id, joined with `\n`, hashed
   with SHA-256; the hash is committed to the run log at each
   boundary. MAP identity across snapshots is keyed by
   `(id, promo_index)` because `alloc_node` reuses slots.

3. **Valid-root set.** {101, 102, 103, 104} (SETREG,
   guard/BRANCHEQ, INC, DEC), grounded in `t2_exec` semantics
   (any other tag returns -999999), not convention.

4. **Pass 1: per-MAP root validity.** For each live tag-20 MAP
   with root = field20(m): root == 0 -> BOOTSTRAP (degenerate;
   no event); root < 2 or root >= 1024 -> Z_RANGE (emit);
   root node dead -> FOSSIL (emit; dangling root, MAP shell
   survives at bid 2 with zero function); root live with tag in
   {101,102,103,104} -> VALID (proceed to pass 2); root live with
   any other tag -> ZOMBIE (emit; observed: tag-30 UNCERTAINTY
   node, tag-902 literal cell).

5. **Pass 2: shared and hijacked roots (VALID MAPs only).** A
   pass-1-failed MAP is excluded as host and as victim. Build the
   SEQ successor index in one edge pass over live type-12 edges.
   For each VALID MAP, walk its graph: start at root; at a
   tag-102 guard follow field 12 (matching the executor);
   otherwise follow the SEQ successor; bound the walk at 80
   steps. Z_SHARED: two live MAPs name the same root id (emit
   for each MAP involved). Z_HIJACKED: MAP B's root is visited
   during MAP A's graph walk, A != B (emit for B). A MAP passing
   both passes is LIVE.

6. **Transition and dedup rule.** The driver keeps a table of
   last-known status keyed by MAP identity `(id, promo_index)`.
   A CORRUPTION event is emitted only on transition into
   {FOSSIL, ZOMBIE, Z_SHARED, Z_HIJACKED} (from LIVE or from a
   newly seen MAP). A MAP that remains corrupt across consecutive
   boundaries is not re-emitted; its ongoing presence is visible
   in the per-boundary ZOMBIE-STATE counts. If a node id is
   reused by a new MAP (promo_index differs), the old entry is
   retired and the new MAP is evaluated fresh. CORRUPTION events
   count corruption onsets; ZOMBIE-STATE counts report
   prevalence.

7. **Event format.** `CORRUPTION <world> <map> <field>
   <expected_type> <actual_type>`, fixed field order, one event
   per line (Section 6.1 signature). `<field>`: 20 for the core
   check, 12 for the guard-target extension. `<expected_type>`:
   for field 20 the literal string
   `graph-cell(101|102|103|104)`; for field 12
   `setreg-cell(101)`. `<actual_type>`: one of `tag-<n>` (the
   occupying node's tag, e.g. `tag-30`, `tag-902`), `dead`
   (FOSSIL), `range` (Z_RANGE), `shared-root` (Z_SHARED),
   `hijacked` (Z_HIJACKED).

8. **EVICT vs CORRUPTION.** EVICT is clean removal of a node
   (slot freed, edges severed, budget recovered). CORRUPTION is
   the silent invalidation of a surviving structure (the MAP
   shell persists, occupies budget, and points at garbage or at
   another structure's cells). A single eviction can cause zero
   EVICT-adjacent harm to MAPs while causing one or more
   CORRUPTION events.

9. **Shared-root landmine.** Each Z_SHARED MAP looks healthy in
   isolation (both roots are live graph cells of valid tags).
   `t2_revise_graph` on one silently rewires the other's cells
   with no REVISE event for the victim, because the writes pass
   through the shared root. Rule for future builds: any revision
   or execution machinery must consult the detector's
   shared-root table before touching a MAP's graph, and a
   Z_SHARED flag on a MAP must block unattributed in-place
   revision of its cells.

10. **Recommended extensions (not required for compliance).**
    (a) Guard branch-target check: during the pass-2 walk, for
    each tag-102 guard cell verify field 12 names a live tag-101
    cell; emit `CORRUPTION <world> <map> 12 setreg-cell(101)
    <actual>`. (b) Literal-operand check: for each tag-101
    SETREG and tag-102 guard, if field 8 names a node id in the
    `res_op` range, verify it is a live tag-902 node; a reused
    slot means the cell silently reads a wrong literal value.
    (c) Policy-anchor liveness: exactly one tag-2 node should
    exist and be live; otherwise emit a CORRUPTION-class driver
    alert.

11. **Driver cost.** O(boundaries), not O(events): pass 1 scans
    up to 1024 nodes filtering live tag-20; pass 2 is one edge
    pass (4096 slots) plus at most one bounded 80-step walk per
    VALID MAP. Negligible next to per-event scan costs.

12. **Non-claims.** The detector does not prevent corruption and
    does not repair it; it makes silent destruction visible. A
    zero CORRUPTION count at a boundary is evidence of no
    detected corruption, not proof of none: the core check
    covers MAP roots only, and interior guard-target and
    literal-operand corruption require the extensions. Counts
    are workload- and pressure-dependent diagnostics, not
    constants: 0% at 520/1024 nodes, 3.8% at 1022/1024 under
    chain-promotion churn, 20% observed in the more diverse W
    cumulative state. The detector reads frozen-state layout
    (tags, field numbers); any build that changes the MAP layout
    or graph cell tags must update this spec before its lifetime
    runs.

13. **Retention-sweep mapping.** At the final retention sweep the
    per-MAP status maps onto the Section 7.7 end-states: LIVE
    -> LIVE; ZOMBIE, Z_SHARED, Z_HIJACKED -> ZOMBIE; FOSSIL ->
    FOSSIL; MAP node itself evicted -> DELETED (visible via
    EVICT lines, not via this detector).

Log format is line-oriented text, one event per line, fields in
fixed order (same discipline as the H2 SIG log format). The exact
field order is frozen with the protocol.

## 7. The eight required measures, operationalized

Micah's eight measures, each with a definition, a log signature,
and an isolation control.

### 7.1 Forward transfer

Definition: learning X improves the rate or asymptote of learning
Y (Y later in the sequence).
Measure: transfer ratio T(X->Y) = E_iso(Y) / E_life(Y).
Log signature: facts or MAPs with origin_world = X appearing in
the provenance (prov[]) of MAPs promoted during Y, or EXEC events
of X-origin MAPs during Y.
Control: E_iso(Y) from the isolation track.
Bar direction: T > 1 is positive transfer.

### 7.2 Backward transfer

Definition: learning Y later improves (or does not degrade)
performance on X (X earlier).
Measure: probe score on X's sealed probes at final retention
sweep, minus probe score on X immediately after X's teach stream.
Log signature: REVISE or PROMOTE events during Y that touch
X-origin structures, followed by improved X QPATH results.
Control: isolation learner's X score (no later worlds).
Bar direction: non-negative delta passes retention; positive
delta is backward transfer proper.

### 7.3 Spontaneous cross-domain connections

Definition: white-box events in which a structure created for one
world participates in cognition for another, without researcher
scaffolding connecting them.
Three levels, reported separately (Section 8):
L1 fact reuse, L2 procedure invocation, L3 procedure adaptation.
Log signature: per level (Section 8).
Control: isolation learners cannot show cross-world events by
construction; the control is the zero baseline plus the
falsifiability of the signature (the log would show the event if
it happened).

### 7.4 Reduced examples-to-criterion over time

Definition: E_life trends downward across the sequence for
structurally similar worlds (A vs A').
Measure: E_life(A) vs E_life(A'). Ratio R = E_life(A)/E_life(A').
Control: E_iso(A) vs E_iso(A') (should be equal; if not, the
worlds differ in difficulty and the comparison is void).
Bar direction: R > 1 means the lifetime learner got faster.

### 7.5 Reuse of old executable structures

Definition: count of EXEC events (stored MAP executed for a later
query) across the lifetime.
Log signature: EXEC lines with origin_world earlier than
event world.
Control: isolation track EXEC count per world (same-world reuse
only).
Note: the reuse-path fix (MAP-first query) is prerequisite
infrastructure. Without it, this measure is trivially zero and
the protocol reports that instead of a finding.

### 7.6 Revision without destroying useful prior structure

Definition: after world C's contradictions, unrelated capabilities
(B probes, unrevised A probes) are intact.
Measure: retention probe scores post-C vs pre-C.
Log signature: REVISE events scoped to contradicted provenance;
EVICT/absent for unrelated MAPs; QPATH on B probes unchanged.
Control: isolation B learner (never sees C).
This is the K-LT-4 kill bar.

[v2] V2-hole reporting: the world-C trap probe (Section 4) records
whether an accepted revision was actually correct. If REVISE fires
and the trap probe later fails, the revision was accepted without
a correctness check (the c2a48bee6 finding: `t2_revise_graph` never
verifies `out == new_o`). Revision safety then has two sub-verdicts:
surgical (no collateral damage) and correct (repair matches the
observation). Frozen TNN-2 is predicted to pass surgical and fail
correct on the trap.

### 7.7 [v2] Memory under long interference

Definition: behavior as the node budget fills across the lifetime.
Measure: node count at each world boundary; probe scores vs budget
fraction; which origin_worlds suffer EVICT events first.
Log signature: EVICT lines with origin_world; CORRUPTION lines;
ZOMBIE-STATE classifications; retention sweep scores per world.
Control: none needed; this is a characterization measure, but
report the budget fraction at which each world's score degrades.

Four end-states are distinguished at each snapshot (source:
forgetting analysis 2726baf74, eviction corruption 986c52fdc):

- LIVE: structure intact and functional.
- DELETED: cleanly evicted; budget recovered.
- FOSSIL: the accidental anti-retirement. MAP shell survives (bid 2)
  while its graph cells (bid 0) and licensing facts are evicted.
  Full retention cost, zero recoverable function, no path back to
  utility. Fossils are the guaranteed output of fixed per-node bids
  under pressure whenever a structure's parts carry heterogeneous
  fixed bids.
- ZOMBIE: MAP shell survives but its field-20 root now points to a
  wrong-typed node (a literal cell, another MAP's cell). Silently
  corrupted, undetectable by the learner, a landmine for any future
  machinery that executes or revises it. Per the detector (Section
  6.2), Z_SHARED (two MAPs sharing one root) and Z_HIJACKED (one
  MAP's root absorbed into another's graph) are classified ZOMBIE
  at the retention sweep, even though each shared root is
  individually a live graph cell.

The 1024-node budget finding predicts degradation; the protocol
quantifies where, and in which end-state. The honest TNN-2
prediction is refined: under pressure, executable structures do not
just die first; they are corrupted first (field-reference
invalidation) while their MAP shells survive as zombies. Clean
deletion is the rare case.

Retirement (excluded from lookup, low cost, recoverable at bounded
cost) does not exist in frozen TNN-2. If a future build implements
it, RETIRED becomes a fifth end-state with its own log signature.

### 7.8 [v2] Whether learning itself improves

Definition: the learner's learning procedure changes with
experience (not just its knowledge).

Operational definition (source: L2L analysis 106ee6698):
learning-to-learn is present when experience with task A measurably
reduces the cost of learning task B, where the reduction is causally
traced to learner-state changes from A (not to B being easier).

Four observables, in priority order:

1. **Reduced examples-to-criterion** (primary metric). R =
   E_life(A)/E_life(A') with the E_iso difficulty control. This is
   the K-LT-5 bar.
2. **Faster trial convergence.** Fewer assembler families attempted
   before a successful verification on later uncertainties of the
   same type. Measurable in transcripts: count of trial-verify
   calls per miss. Frozen TNN-2: fixed order, no change expected.
3. **Cheaper repeated ignorance.** The second miss on an identical
   (s,r) key costs less than the first. Currently both cost exactly
   +14 nodes / +6 edges (state dynamics, phases B and G); phase G
   created 6 more UNCERTAINTY nodes for keys that already had them.
   Any reduction is learning. This is the highest-impact single
   gap (uncertainty dedup).
4. **Better inquiry on second similar uncertainty.** Fewer
   miss-observe-act cycles to resolve the second uncertainty of a
   previously seen type.

Minimal measurable unit: one (family A, family B) pair with same
structural form, different surface parameters, a fresh-B difficulty
control (B solved with no retained state takes the same examples
as A solved fresh), and a causal ablation (removing the specific
retained state from A returns B to A-speed). The L2L2 experiment is
the reference implementation: family A (offset 3) took 13 examples;
family B (offset 7) with retained state took 10; family B fresh took
13; ablation (form_known forced 0) returned B to 13. Transfer of 3
examples, causally traced to retained `form_known` state. Citation
status: the original L2L2 P3 ablation was not performed as specified
(audit af9a9765a); the repair (0872a412d, a530028ea) ran mode 2
properly (B_ABL=13, 3/3 byte-identical) and closed P3 under the
amended prereg. L2L2 may be cited as ablation-verified referencing
the repair, not the original result. The original BUILD-PASS (5/5)
verdict is not retroactively validated.

What does NOT count: B solved faster because B is easier (fails the
difficulty control); researcher source changes between A and B (that
is researcher learning); memorizing A's answers and regurgitating on
B (storage, L0); trying fewer families because the researcher removed
families (envelope change).

Weak vs strong K-LT-5:

- **Weak** (same relation, biased world): a global trial-order
  policy (H3-lite Node 1) should pass. If the lifetime rewards one
  family consistently, the order flips and E(B) < E(A). The 1.15
  ratio is achievable when the skipped families are expensive.
- **Strong** (different relation, same structural type): requires
  conditional policies indexed by structural features of the
  uncertainty, not a single global order. H3-lite as drafted should
  fail strong K-LT-5. The dedup gap additionally bounds even weak
  K-LT-5: the per-miss floor stays high because identical misses
  still cost full price under H3-lite.

For frozen TNN-2: the trial loop order is fixed, so observables 1-4
are all expected to be zero. The protocol records zero rather than
omitting the measure.

For H3-lite builds: POLICY events changing trial order, guide
defaults, or repair dispatch across the lifetime count here.
Measure: POLICY event count with behavioral consequence (a later
QPATH or E() change attributable to the policy change). Theater
guard applies: only policy nodes with both production read and
write paths are eligible (T1 MISS_POLICY and T2 P-INV threshold
are excluded).

**New standing diagnostic DYN-1 (per-experience cost constancy).**
Source: state dynamics (ee238d8d4). At each world boundary, the
driver computes per-experience state deltas (nodes and edges added
per teach, per miss, per query-hit) and tests whether they are
constant across the lifetime. Exactly constant per-experience cost
across hundreds of experiences, with duplicated structures on
repeated experiences, is the "write-mostly, not living" signature:
the letter of continuously changing state without adaptive
cognition. DYN-1 is reported for every lifetime run on every
build; it is a characterization diagnostic, not a kill bar.

This is the K-LT-5 kill bar and the H3-lite diagnostic readout.

## 8. Cross-domain connection detection (three levels)

A "connection" is only counted with a white-box signature. Verbal
stories about what the learner "must have" done are not findings.

- LEVEL 1, fact reuse: a fact node with origin_world X appears in
  the prov[] list of a MAP promoted during world Y (X != Y), and
  ablating that fact (a counterfactual re-run with the fact
  withheld) increases E(Y) or breaks Y probes. Without the
  ablation, it is correlation, reported as such.
- LEVEL 2, procedure invocation: an EXEC event for a MAP with
  origin_world X occurring during world Y (X != Y) with a correct
  result. This is the reuse-path behavior across a domain
  boundary. For frozen TNN-2 this is architecturally blocked
  (subject-bound literals); the protocol expects zero and treats
  any nonzero as a major finding requiring re-verification.
- LEVEL 3, procedure adaptation: a MAP with origin_world X is
  revised or copied during world Y and the adapted structure
  serves Y queries. Signature: REVISE or PROMOTE during Y whose
  provenance includes an X-origin MAP node (not just X-origin
  facts). Requires the copy-and-commit substrate or equivalent;
  in-place aliasing (the 8b58c4104 bug class) must be excluded
  by node-id accounting.

Micah's examples map to levels: arithmetic structure to planning
is L2/L3; causal abstraction to language is L1/L2; procedure
shape to unfamiliar domain is L2/L3; old hypothesis meeting new
evidence is L1 plus REVISE; useless memory becoming important is
L1 (a fact with no prior prov[] appearances gaining one).

### 8.1 [v2] Spontaneity caveat

Source: goal origination (3bf4d7bb4). TNN-2 is purely reactive:
all four event handlers have zero internal callers, there is no
learner tick, and no goal representation exists in production.
Every connection in a frozen TNN-2 lifetime is therefore caused by
a harness event in the same tick.

"Spontaneous" in this protocol is defined as the weaker reading:
not-harness-labeled. Per Micah's clarification, the driver never
labels the world, never names the connection, and never tells the
learner which prior knowledge to recruit (control 7 in Section 12).
A connection formed under those conditions counts as spontaneous
at L1/L2/L3.

The stronger reading (self-initiated: the learner forms the
connection between events, from accumulated state, without a
harness trigger) requires the R2 self-invocation machinery, which
does not exist in frozen TNN-2. The protocol does not test the
stronger reading on frozen TNN-2; it marks it as requiring future
architecture. If a future build implements goal machinery, the
GOAL_* events (Section 6.1) become the signature for strong
spontaneity.

## 9. Examples-to-criterion (E), precisely

E(X) for a learner on world X: the number of teach events fed
before the learner first scores 10/10 on X's sealed probes when
probed. Probing schedule: after every k teach events (k frozen in
the protocol; k=5 suggested), run the 10 probes read-only. The
first schedule point with 10/10 sets E(X). If criterion is never
reached within the teach stream, E(X) = INCOMPLETE (reported, not
zero; ratios involving INCOMPLETE are void).

Teach streams are fixed length and fixed order per world (frozen).
The isolation and lifetime tracks receive byte-identical teach
content for world X; the lifetime learner additionally holds
prior state. This makes E_iso(X) vs E_life(X) a clean comparison.

[v2] The trial-must-run rule (Section 4.1) applies to the probing
schedule: a TRIAL-EXPECTED probe that is answered via fact_hit
because the teach stream leaked a direct (s,r) fact does not
measure what the world was designed to measure. If more than 2 of
10 probes in a TRIAL-EXPECTED set resolve via fact_hit, the world
fails design validation and E(X) is VOID for that world (the H2
precedent: all probes returned direct facts, discrimination zero).

## 10. Forward vs backward transfer, distinguished

Forward (X->Y, Y later): measured by E() ratios and L1/L2/L3
events during Y with X-origin signatures. Claimed only when the
isolation control shows the lifetime learner needed fewer events
AND the log shows X-origin structures participating.

Backward (Y improves X, Y later): measured by X probe deltas
(post-Y minus post-X) at the final retention sweep. Claimed only
when the delta is positive and the log shows a Y-world event
(revision, new fact, policy change) causally touching X
structures. Mere non-degradation is retention (7.2), not backward
transfer.

## 11. Kill bars (falsifiable)

All bars are evaluated on the lifetime track against isolation
controls, 3/3 byte-identical runs. A bar is PASS/FAIL/VOID
(VOID if a control is broken, e.g. E_iso INCOMPLETE).

- K-LT-1 (forward transfer, fact level): T(A->B) >= 1.25 AND at
  least one L1 event with ablation confirmation. Honest
  prediction for frozen TNN-2: PASS (B is designed to depend on
  A's facts; this bar tests the machinery, not a miracle).
- K-LT-2 (retention under interference): final retention sweep:
  A-origin probes >= 9/10 and B probes >= 9/10 while node budget
  fraction < 0.9. Prediction: PASS within budget; characterizes
  the degradation point beyond it. [v2] Beyond-budget behavior is
  now characterized by end-state (Section 7.7), not just score:
  report fossil and zombie counts alongside probe scores. The
  prediction beyond budget is corruption-first (zombie MAPs),
  then fossilization, then catastrophic answer loss (per the P4
  profile: executable structures die first, MAPs fossilize,
  learned answers are catastrophically forgotten; source:
  `tnn2_transfer/TRANSFER_ANALYSIS.md` P4 result; and the
  eviction-corruption refinement 986c52fdc).
- K-LT-3 (cross-domain executable reuse): >= 1 L2 event
  (X-origin MAP executed in Y != X, correct result). Prediction
  for frozen TNN-2: FAIL (subject-bound graphs; transfer analysis
  proved the block architecturally). A FAIL here is a clean
  diagnostic, not a surprise; it scopes the TNN-3 requirement.
- K-LT-4 (revision safety): post-C B probes >= 9/10 AND revised-A
  probes 5/5 correct AND unrevised-A probes 5/5 unchanged.
  Prediction: PASS on surgical safety (revision is
  provenance-scoped). [v2] The V2-hole trap probe is reported
  separately: predicted FAIL on correctness (a wrong-but-running
  repair is accepted, since `t2_revise_graph` never checks
  `out == new_o`). K-LT-4 therefore has two sub-verdicts:
  K-LT-4a (surgical, predicted PASS) and K-LT-4b (correct,
  predicted FAIL for frozen TNN-2).
- K-LT-5 (learning improves): [v2] split per the L2L operational
  definition.
  - K-LT-5w (weak): R = E_life(A)/E_life(A') > 1.15 with
    E_iso(A) == E_iso(A') (difficulty control). Prediction for
    frozen TNN-2: FAIL (fixed trial order; nothing to improve
    with). Prediction for H3-lite: PASS expected if the world is
    family-biased (Node 1 flips the global order), bounded by the
    dedup residual (identical misses still cost full price).
  - K-LT-5s (strong): cross-relation transfer of learning rate:
    experience with relation R1 reduces E on relation R2 of the
    same structural type, with fresh-R2 and ablation controls.
    Prediction for frozen TNN-2: FAIL. Prediction for H3-lite as
    drafted: FAIL (global order carries no conditional structure;
    Rank 3 gap). Passing K-LT-5s requires conditional policies
    (L2L requirement 3) or strategy invention (requirement 5).
  - The DYN-1 diagnostic (per-experience cost constancy) is
    reported alongside both sub-bars. Exactly constant costs with
    duplicated structures is the predicted frozen TNN-2 profile.

Bars are kill bars for the claim "the lifetime learner shows
[phenomenon]", not for the architecture. Failing K-LT-3 does not
kill TNN-2; it kills the claim that TNN-2 does cross-domain
procedure reuse, which nobody should claim.

## 12. Transfer vs contamination controls

Micah's ruling: cross-domain connection formation is a FEATURE,
not contamination. Rigor still requires distinguishing genuine
transfer from leakage. Controls:

1. Sealed probes: no probe (subject, relation) pair is taught in
   any world's teach stream. A probe answered correctly must come
   from generalization, not memorization.
2. Byte-identical teach content: isolation and lifetime tracks get
   the same world-X bytes; only prior state differs.
3. White-box necessity: every transfer claim cites log lines
   (TEACH/PROMOTE/EXEC/REVISE/CORRUPTION node ids). No log
   signature, no claim.
4. Ablation for L1: re-run world Y with the X-origin fact
   withheld (single-fact ablation); if E(Y) is unchanged, the L1
   event was incidental, not causal.
5. Negative results are first-class: worlds with zero cross
   events are reported as zero, not omitted. A lifetime with
   T = 1.0 everywhere is a finding (no transfer), not a void.
6. Difficulty control: E_iso(A) vs E_iso(A') must match within
   20% or the R ratio is VOID (worlds mismatched).
7. No researcher cross-links: the protocol forbids teach events
   that name the connection (e.g. "use A's method for B"). World
   B's cross-subject facts are ordinary facts; the learner must
   recruit them unprompted.
8. [v2] Trial-must-run validation: per Section 4.1 and Section 9,
   TRIAL-EXPECTED probes that resolve via fact_hit do not count
   toward transfer measures; a world with >2/10 such probes is
   VOID (H2 precedent).
9. [v2] Theater exclusion: no transfer, reuse, revision, or
   policy claim may cite T1-T6 nodes as participating learner
   state. The THEATER_GUARD log (Section 6.1) is part of the
   evidence package for every run.

## 13. Honest TNN-2 capability assessment (predicted)

What frozen TNN-2 can show in this protocol:

- Fact accumulation across worlds (L1 events): YES, by design
  of world B. This is L0/L1 learning, useful infrastructure.
- Revision without collateral damage (K-LT-4a): YES, expected.
- Revision correctness (K-LT-4b): NO, expected. The V2 hole
  (c2a48bee6): any repair that runs is accepted; the trap probe
  should expose this.
- Retention within budget (K-LT-2): YES, expected.
- Retention under pressure: NO, in the specific refined sense.
  Predicted profile: executable structures corrupted first
  (zombie MAPs via field-reference invalidation), MAP shells
  fossilize (bid 2 outlives bid-0 cells), learned answers
  catastrophically forgotten after 12 idle events (PRO clock
  expiry), trial garbage consumed first. The fossil is the
  inversion of retirement: full cost, zero function, no recovery.
- Same-(subject, relation) MAP reuse (7.5): YES, given the
  reuse-path fix is in the tested build. Without the fix,
  expect zero (the shadow-fact finding).
- Cross-domain procedure invocation (K-LT-3): NO. Architecturally
  blocked: literals baked into graphs, no CALL opcode, assemblers
  never reference stored MAPs. The protocol will record zero
  L2 events; that zero is the evidence.
- Learning-rate improvement (K-LT-5w): NO for frozen TNN-2.
  Fixed trial order, fixed dispatch, no uncertainty dedup.
  E_life(A') should equal E_iso(A'). DYN-1 expected to show
  exactly constant per-experience costs ("write-mostly, not
  living": 427 nodes over ~260 experiences, +14/+6 per identical
  miss, duplicated UNCERTAINTY nodes for known keys).
- Learning-rate improvement (K-LT-5s): NO for frozen TNN-2 and
  NO for H3-lite as drafted (no conditional policies).
- Genuine decline/withhold: NO. The -2 is pipeline exhaust, not
  a choice; the DECLINE log should show zero genuine declines.
- Goal-directed behavior: NO. Purely reactive; GOAL_* events
  defined but never fire.

The protocol is designed so TNN-2's predicted FAILs (K-LT-3,
K-LT-4b, K-LT-5w, K-LT-5s) are as informative as its predicted
PASSes. They mark the exact architectural boundary the next design
must cross.

## 14. What TNN-3 would need (implied requirements)

For K-LT-3 to pass, a future architecture needs at least one of:

- Subject-parameterized graphs (literals as frame-bound
  variables, not baked constants), or
- A CALL/apply opcode letting the trial loop or query path
  invoke stored roots with new bindings, or
- An adaptation operator (L3) that rewrites an X-origin graph
  for Y's subjects with a white-box trace.

For K-LT-5w to pass, it needs learner-writable learning policy
(the H3-lite direction): trial order, guide selection, or
repair dispatch that changes with experience and measurably
reduces E(). Plus uncertainty dedup (the Rank 1 gap H3-lite does
not address): the per-miss floor stays high without it.

For K-LT-5s to pass, it needs conditional policies indexed by
structural features of the uncertainty (L2L requirement 3), not
a single global order.

For K-LT-4b to pass, the revision path needs a correctness check
beyond successful execution (close the V2 hole: verify
`out == new_o`, or a learner-owned equivalent).

For memory under interference to improve, it needs
structure-level retention (bids reflecting per-structure utility,
not fixed per-node constants), dependency-aware eviction, and
retirement as a genuine third state instead of the accidental
fossil (forgetting requirements R1-R6).

Neither is claimed here. This section is a requirements sketch
for the design workers, not a result.

## 15. Non-claims

This protocol does NOT establish, and no result under it shall be
cited as establishing:

- L3 (representational invention) or any part of Criterion 0.
- SUF (source-underdetermined form); all world structures here
  are researcher-designed, so SUF is out of scope by construction.
- Learner-authored procedures (the assemblers are fixed; only
  their products and the learner's recruitment of them vary).
- General intelligence, AGI, or superiority over any baseline.
- That passing K-LT-1/K-LT-2/K-LT-4a is "basically" transfer in
  the strong sense; it is fact-level and retention-level
  transfer, reported exactly as such.
- [v2] That passing K-LT-5w is learning-to-learn in the strong
  sense; it is policy selection over researcher-enumerated
  alternatives (6 trial orders), bounded by the SUF disclaimer
  in the L2L analysis. K-LT-5s is the strong form.

The protocol measures specific, named phenomena. It does not
certify architectures.

## 16. Preregistration freeze requirements

Before any lifetime implementation:

1. This document frozen by Micah (DRAFT -> FROZEN commit).
2. World teach streams and sealed probe sets generated, hashed,
   and sealed. The designer of the worlds must not be the
   implementer of the driver (adversarial separation; the H2
   precedent applies).
3. Instrumentation field order frozen (Section 6, including the
   v2 event types and the THEATER_GUARD procedure).
4. k (probe schedule), E() rules, and bar thresholds frozen
   (Sections 9, 11).
5. Named evaluator with no access to world contents beyond
   hashes until the freeze commit.
6. Freeze commit strictly precedes the first teach event.
7. The subject build (frozen TNN-2 binary or named variant)
   recorded by hash; the reuse-path variant question (test the
   frozen build, the fixed variant, or both) decided and
   recorded before freezing.
8. [v2] World-design validation (Section 4.1) run and passed:
   TRIAL-EXPECTED probes confirmed trial-reachable on the sealed
   teach streams; THEATER_GUARD baseline classifications recorded.

Amendments after freezing follow the standing rule: transparent,
dated, committed alone before the changed code runs. Bars are
never weakened to force a pass.

## 17. Relation to existing evaluations

- Core Freeze (FW1-FW9): targeted repair battery for frozen
  mechanisms. Isolation-style. Complementary, not replaced.
- GW1-GW8: generality worlds, isolation-style. Complementary.
- H2 (K-H2-1..4, frozen): learner-internal criterion traps.
  [v2] H2 is currently VOID (72173fe11): t2_sig calibration
  failed AND the trial never ran on any probe (direct facts
  answered everything). Until the t2_sig repair and world
  redesign are decided by Micah (Section 19), this protocol
  consumes no H2 result. H2's withhold/lie/criterion probes can
  be embedded as a world in a future lifetime sequence once
  H2 is re-frozen; for now H2 runs standalone per Micah's
  ordering (H2 before H1 widening; H1 is the hypothesis that
  each mechanism's output space is enumerated in source, so
  "H1 widening" means opening the constructor beyond the
  enumerated space; source: `tnn3_roadmap/TNN3_ROADMAP.md`
  section 2).
- H3-lite: the policy-learning diagnostic. Its POLICY events
  are the log signature for measure 7.8. A lifetime run of an
  H3-lite build is the natural K-LT-5w test. [v2] Honest
  calibration: H3-lite addresses policy revisability (L2L
  requirement 2) but not uncertainty dedup (requirement 1),
  conditional policies (requirement 3), or strategy invention
  (requirement 5). If K-H3 passes but K-LT-5w underperforms,
  the residual is dedup plus the global-order limit, not
  policy revisability.
- Lifetime race (RACE_PREREG.md): TNN vs LLM contest framing
  with stages A-L. This protocol is the single-architecture
  continuity evaluation; the race is the competitive
  evaluation. Both can share world-design discipline but their
  claims differ.

## 18. Standing architectural metric (this design)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: world sequence, teach
  streams, probe sets, bar thresholds, instrumentation spec,
  world-design validation rule, theater guard classifications
  (all frozen pre-evaluation; this is the researcher's
  legitimate role: designing the test, not the cognition).
- LEARNER-OWNED STRUCTURAL DECISIONS: every MAP, fact,
  revision, eviction, and policy change during the lifetime
  (to be counted from logs when run). Theater nodes (T1-T6)
  excluded by guard.
- SOURCE-ENUMERABLE FORMS: all world content (researcher
  designed; SUF out of scope by Section 15).
- SUF DECISIONS: 0 in this protocol (not a SUF test).
- LEARNER-INTERNAL CRITERIA: measured by K-H2 under its own
  prereg; this protocol consumes H2's result, does not re-test it.
  [v2] H2 is VOID; no H2 result is consumed until re-frozen.
- REUSE EVENTS: measure 7.5 (to be counted).
- REVISION EVENTS: measure 7.6 (to be counted), with the V2-hole
  correctness sub-verdict.
- CORRUPTION EVENTS: new category (Section 6.1), to be counted
  from driver snapshots per the detector algorithm (Section 6.2).
  Not revisions; not clean evictions.
- COGNITION LINES: 0 (design only; no source changes).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

No benchmark score appears in this protocol as a substitute for
these fields. The measures are the score.

## 19. [v2] Decisions requiring Micah (explicitly banked)

This draft cannot be frozen until Micah rules on the following.
They are recorded here rather than decided, per the escalation
boundary (protected-core changes, irreversible commitments,
experimentally indiscriminable decisions come to him).

**D1. H2 repair path.** H2 is VOID on two independent grounds:
(a) t2_sig records literals for tags 101/102 while the prereg
requires literals excluded (implementation diverged from spec);
(b) the trap worlds include direct facts for the query (s,r), so
`activate` answers and the trial never runs (world-design defect).
Options: (i) evaluator-side corrected signature plus prereg
amendment re-freezing it (signature is measurement infrastructure;
the spec was correct), (ii) new build (breaks the freeze).
Separately, the H2 worlds need redesign (no direct facts for
TRIAL-EXPECTED probes), which is a new design plus freeze cycle,
not a patch. Until D1 is resolved, Section 17 consumes no H2
result.

**D2. H3-lite vs lifetime ordering.** The plan was "begin H3-lite
unless H2 invalidates its assumptions." H2 voided: it neither
invalidated nor validated anything. Micah's call is needed before
starting the frozen H3-lite diagnostic. This affects whether the
first lifetime runs use the frozen TNN-2 build, an H3-lite build,
or both (and in which order).

**D3. Which build(s) to run.** Candidates: (a) frozen TNN-2 build
f4de7ff46 as-is; (b) the reuse-path variant (MAP-first query,
unfrozen); (c) the barrier-break variant (visibility, unfrozen);
(d) H3-lite (pending D2). The protocol supports all four; the
choice changes which measures are informative (e.g. 7.5 is
trivially zero on (a)). Micah decides the run matrix before the
freeze in Section 16.

**D4. Protocol freeze decision.** This v2 draft is DRAFT-NOT-FROZEN.
Freezing requires D1-D3 plus Micah's review of the v2 changes
(especially the new event types, the K-LT-5 split, and the
theater guard). The freeze commit must strictly precede world
generation (Section 16, item 6).

**D5. Weak vs strong K-LT-5 as the headline bar.** V2 splits K-LT-5
into weak (policy selection, achievable by H3-lite) and strong
(conditional policies, requiring future architecture). Micah should
confirm which sub-bar is the headline claim for the first lifetime
runs, so the run matrix (D3) and the world bias design match the
claim. A family-biased world makes K-LT-5w passable; an unbiased
world makes it a fairer test but harder.

---

End of v2 draft. Awaiting Micah's review and freeze decision.
