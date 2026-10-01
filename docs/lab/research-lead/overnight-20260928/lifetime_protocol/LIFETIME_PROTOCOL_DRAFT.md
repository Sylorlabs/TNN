# LIFETIME EVALUATION PROTOCOL (DRAFT-NOT-FROZEN)

Date: 2026-10-01. Designer: Lifetime Evaluation Protocol Designer (subagent).
Status: DRAFT. Not frozen. For Micah's review. No implementation exists.

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

### WORLD A: foundation chains (the baseline skill)

- Subjects: 1..10.
- Teach: 2-hop and 3-hop chain facts, enough for the trial loop to
  assemble and promote chain MAPs. Include redundant licensing facts
  so provenance is nontrivial.
- Tests: can the learner acquire a verified executable procedure and
  answer held-out chain queries.
- Sealed probes: 10 chain queries on subjects 1..10, (subject,
  relation) pairs never taught.
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
- Sealed probes: 10 B-chain queries, held out.
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
- Tests: does revision correct A's answers without destroying B's
  capability (no collateral damage), and does the MAP-level white
  box show in-place revision with provenance retargeting.
- Sealed probes: 10 probes (5 revised-A queries with corrected
  answers, 5 B queries that must be unchanged).
- Criterion: 10/10 (5 correct-after-revision, 5 unchanged).
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
- Sealed probes: 10 count/sum queries, held out.
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
  A probes (retention check).
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
- FORGET(world, node, reason): every compression or retirement of a
  structure the learner (not the budget) initiated, if the
  architecture supports learner-initiated forgetting.

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

### 7.7 Memory under long interference

Definition: behavior as the node budget fills across the lifetime.
Measure: node count at each world boundary; probe scores vs budget
fraction; which origin_worlds suffer EVICT events first.
Log signature: EVICT lines with origin_world; retention sweep
scores per world.
Control: none needed; this is a characterization measure, but
report the budget fraction at which each world's score degrades.
The 1024-node budget finding (transfer analysis) predicts
degradation; the protocol quantifies where.

### 7.8 Whether learning itself improves

Definition: the learner's learning procedure changes with
experience (not just its knowledge).
For frozen TNN-2: the trial loop order is fixed, so this measure
is expected to be zero. The protocol records it as zero rather
than omitting it.
For H3-lite builds: POLICY events changing trial order, guide
defaults, or repair dispatch across the lifetime count here.
Measure: POLICY event count with behavioral consequence (a later
QPATH or E() change attributable to the policy change).
Control: frozen TNN-2 lifetime (zero expected) vs H3-lite
lifetime.
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
  the degradation point beyond it.
- K-LT-3 (cross-domain executable reuse): >= 1 L2 event
  (X-origin MAP executed in Y != X, correct result). Prediction
  for frozen TNN-2: FAIL (subject-bound graphs; transfer analysis
  proved the block architecturally). A FAIL here is a clean
  diagnostic, not a surprise; it scopes the TNN-3 requirement.
- K-LT-4 (revision safety): post-C B probes >= 9/10 AND revised-A
  probes 5/5 correct AND unrevised-A probes 5/5 unchanged.
  Prediction: PASS (revision is provenance-scoped).
- K-LT-5 (learning improves): R = E_life(A)/E_life(A') > 1.15
  with E_iso(A) == E_iso(A') (difficulty control). Prediction for
  frozen TNN-2: FAIL (fixed trial order; nothing to improve
  with). This bar is the H3-lite/TNN-3 diagnostic: it passes
  only if policy learning exists and works.

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
   (TEACH/PROMOTE/EXEC/REVISE node ids). No log signature, no
   claim.
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

## 13. Honest TNN-2 capability assessment (predicted)

What frozen TNN-2 can show in this protocol:

- Fact accumulation across worlds (L1 events): YES, by design
  of world B. This is L0/L1 learning, useful infrastructure.
- Revision without collateral damage (K-LT-4): YES, expected.
- Retention within budget (K-LT-2): YES, expected.
- Same-(subject, relation) MAP reuse (7.5): YES, given the
  reuse-path fix is in the tested build. Without the fix,
  expect zero (the shadow-fact finding).
- Cross-domain procedure invocation (K-LT-3): NO. Architecturally
  blocked: literals baked into graphs, no CALL opcode, assemblers
  never reference stored MAPs. The protocol will record zero
  L2 events; that zero is the evidence.
- Learning-rate improvement (K-LT-5): NO. Fixed trial order,
  fixed dispatch. E_life(A') should equal E_iso(A').

The protocol is designed so TNN-2's predicted FAILs (K-LT-3,
K-LT-5) are as informative as its predicted PASSes. They mark
the exact architectural boundary the next design must cross.

## 14. What TNN-3 would need (implied requirements)

For K-LT-3 to pass, a future architecture needs at least one of:

- Subject-parameterized graphs (literals as frame-bound
  variables, not baked constants), or
- A CALL/apply opcode letting the trial loop or query path
  invoke stored roots with new bindings, or
- An adaptation operator (L3) that rewrites an X-origin graph
  for Y's subjects with a white-box trace.

For K-LT-5 to pass, it needs learner-writable learning policy
(the H3-lite direction): trial order, guide selection, or
repair dispatch that changes with experience and measurably
reduces E().

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
- That passing K-LT-1/K-LT-2/K-LT-4 is "basically" transfer in
  the strong sense; it is fact-level and retention-level
  transfer, reported exactly as such.

The protocol measures specific, named phenomena. It does not
certify architectures.

## 16. Preregistration freeze requirements

Before any lifetime implementation:

1. This document frozen by Micah (DRAFT -> FROZEN commit).
2. World teach streams and sealed probe sets generated, hashed,
   and sealed. The designer of the worlds must not be the
   implementer of the driver (adversarial separation; the H2
   precedent applies).
3. Instrumentation field order frozen (Section 6).
4. k (probe schedule), E() rules, and bar thresholds frozen
   (Sections 9, 11).
5. Named evaluator with no access to world contents beyond
   hashes until the freeze commit.
6. Freeze commit strictly precedes the first teach event.
7. The subject build (frozen TNN-2 binary or named variant)
   recorded by hash; the reuse-path variant question (test the
   frozen build, the fixed variant, or both) decided and
   recorded before freezing.

Amendments after freezing follow the standing rule: transparent,
dated, committed alone before the changed code runs. Bars are
never weakened to force a pass.

## 17. Relation to existing evaluations

- Core Freeze (FW1-FW9): targeted repair battery for frozen
  mechanisms. Isolation-style. Complementary, not replaced.
- GW1-GW8: generality worlds, isolation-style. Complementary.
- H2 (K-H2-1..4, frozen): learner-internal criterion traps.
  H2's withhold/lie/criterion probes can be embedded as a world
  in a future lifetime sequence; for now H2 runs standalone
  per Micah's ordering (H2 before H1 widening).
- H3-lite: the policy-learning diagnostic. Its POLICY events
  are the log signature for measure 7.8. A lifetime run of an
  H3-lite build is the natural K-LT-5 test.
- Lifetime race (RACE_PREREG.md): TNN vs LLM contest framing
  with stages A-L. This protocol is the single-architecture
  continuity evaluation; the race is the competitive
  evaluation. Both can share world-design discipline but their
  claims differ.

## 18. Standing architectural metric (this design)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: world sequence, teach
  streams, probe sets, bar thresholds, instrumentation spec
  (all frozen pre-evaluation; this is the researcher's
  legitimate role: designing the test, not the cognition).
- LEARNER-OWNED STRUCTURAL DECISIONS: every MAP, fact,
  revision, eviction, and policy change during the lifetime
  (to be counted from logs when run).
- SOURCE-ENUMERABLE FORMS: all world content (researcher
  designed; SUF out of scope by Section 15).
- SUF DECISIONS: 0 in this protocol (not a SUF test).
- LEARNER-INTERNAL CRITERIA: measured by K-H2 under its own
  prereg; this protocol consumes H2's result, does not re-test it.
- REUSE EVENTS: measure 7.5 (to be counted).
- REVISION EVENTS: measure 7.6 (to be counted).
- COGNITION LINES: 0 (design only; no source changes).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

No benchmark score appears in this protocol as a substitute for
these fields. The measures are the score.

---

End of draft. Awaiting Micah's review and freeze decision.
