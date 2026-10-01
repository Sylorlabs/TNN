# TNN-3 Kill Bars: DRAFT-NOT-FROZEN

Date: 2026-10-01. Drafter session: e0d4f332-8192-41d4-aa15-f95f81c4333b.
Status: **DRAFT-NOT-FROZEN**. This document is bar design, not
implementation, not preregistration, and not a frozen threshold.
Nothing here governs any build until Micah reviews it and a TNN-3
preregistration freezes it (or records explicit amendments) before
any TNN-3 implementation begins.

## 1. Purpose

TNN-2's kill bars K-T2-3 through K-T2-6 tested that runtime filling and
persistence work. They did, and the three red teams (construction
`340e94e3e`, inquiry `4e329c772`, revision `687ba0219`;
CONSTRUCTION/INQUIRY/REVISION-ATTACK-SUCCESS) showed the learner never
chose the schema: fixed templates with variable content, constant
guides, single-schema literal patch. The revision generalization
analysis (`edbb0e9b5`) attributed the primary cause to the bar itself:
K-T2-6 said "in at least one test," and a single-schema operator is
the minimal-cost satisfier of an existence-only bar. The red team
synthesis (`42b4dfa91`) named the shared pattern: enumerated-schema /
filled-slot, researcher enumerates the possible, learner fills the
blanks.

These draft bars are designed so that the minimal-cost satisfier of
each bar is a genuinely general mechanism, not a narrower schema.
Each bar below has four parts: the statement, why TNN-2's frozen
implementation would have failed it (specific cause), why a genuinely
general mechanism can pass it (achievability), and the deterministic
verification procedure (no judgment calls at eval time).

Design rules applied throughout:

- Observable behavior only. No bar prescribes a search algorithm, a
  proposal mechanism, an internal representation, or a decision
  criterion. State checks read learner state through deterministic
  dumps; behavior checks compare ACT/EXECUTE outputs.
- Deterministic. Every check is 3/3 byte-identical, computed by pure
  Zag code in the sealed driver, or decided by git ancestry. No
  human judgment at evaluation time.
- Post-freeze worlds. Non-enumerability is enforced by process: the
  independent adversary authors sealed worlds after the TNN-3 build
  freeze (git-ancestry verified, fail closed). A builder cannot
  pre-enumerate worlds that do not exist yet.
- Thresholds before results. Per Micah's rule, once these bars are
  frozen in the TNN-3 prereg they cannot be weakened or reinterpreted
  after results. Amendment requires transparent re-freeze and re-run.

## 2. Cross-cutting bars

### K-T3-ADV (adversarial process bar)

Statement: the sealed evaluation's worlds satisfy all of:

1. Independence: world-design commits are authored by designated
   independent adversary agents, not by the TNN-3 builder. Recorded
   in each world's NAMECHECK.
2. Post-freeze authorship: every sealed world asset commit is a git
   descendant of the TNN-3 build-freeze commit, verified by
   `git merge-base --is-ancestor`. If any world asset predates the
   freeze, the evaluation is BLOCKED (fail closed), never passed.
3. Limited visibility: the adversary sees the public architecture
   claim but not builder fixtures, builder test transcripts, or
   sealed-harness internals beyond the driver protocol.
4. Minimum counts: construction, at least 4 sealed worlds with at
   least 3 mutually non-isomorphic required topologies; inquiry, at
   least 3 sealed scenarios; revision, at least 3 sealed scenarios
   with at least 2 mutually non-isomorphic required repair
   topologies.
5. No trivial variants: within each mechanism's diversity set, all
   required structural signatures are pairwise distinct under the
   deterministic signature function (section 3). The governance audit
   additionally verifies each world asset contains the adversary's
   non-triviality rationale (presence check only).

Why TNN-2 fails: TNN-2 was never subjected to post-freeze adversarial
worlds for these mechanisms; its builder fixtures and the sealed
freeze worlds overlap the fixed families. Under this process, the
adversary would author worlds requiring topologies outside TNN-2's 2
production-reachable families (chain, count), which the construction
red team's boundary probes proved unrepresentable (5-hop chains,
DEC arithmetic, branching beyond fixed guard to set pairs, graph
reuse). TNN-2 deterministically fails the resulting worlds.

Achievability: the bar constrains the evaluation process, not the
implementation. Any implementation faces the same process.

Verification: git ancestry commands, commit authorship records,
signature pairwise-distinctness computed by the sealed driver,
all-pass 3/3 byte-identical per world.

### K-T3-TOPO (learner-chooses-topology audit)

Statement: two parts.

(a) Mutual non-isomorphism: for each mechanism's designated diversity
set, the sealed driver computes the deterministic structural
signature of each promoted or revised graph and requires all pairwise
signatures to differ.

(b) Beyond-fixture shapes: the TNN-3 builder's committed test suite
must log, for every promoted and revised graph, its structural
signature (same function), 3/3 byte-identical. The sealed evaluation
checks that at least one passing sealed construction world and at
least one passing sealed revision scenario have signatures absent
from the builder's log. A learner that only reproduces fixture shapes
fails this check.

The structural signature function is fixed in the frozen prereg. The
draft proposes: a canonical string over cell tags, edge types, step
counts, and adjacency shape only (no literal values, no addresses,
no allocation order). Two graphs are structurally different iff their
signatures differ.

Why TNN-2 fails: TNN-2's constructible set equals its
fixture-exercised set (chain and count families; the sum family is
unreachable in production, test-gated by a type-8 marker only created
in test `t_p2`). Any sealed world with a signature absent from its
fixtures requires a topology outside those families and is
unrepresentable, so TNN-2 fails the underlying world before the audit
even runs. For revision, TNN-2's only repair signature is
guard to new-SETREG(literal) to succ with the old SETREG tombstoned;
any second required repair topology is unrepresentable.

Achievability: a learner whose construction and repair spaces are
genuinely open produces shapes keyed to world evidence, not to
fixtures. The bar does not require any particular number of shapes,
only that at least one successful shape was never fixture-exercised.

Verification: string set operations in the sealed driver, 3/3
byte-identical; builder log committed at build freeze.

## 3. Construction bars

### K-T3-CON-1 (two structurally different sealed constructions, derived content)

Statement: after the build freeze, the adversary authors at least 4
sealed construction worlds; at least 3 require mutually
non-isomorphic solution topologies (K-T3-TOPO(a)). In each world, the
solution's structural information must not be readable from the
triggering event literals alone: the required graph's step count,
branching shape, or key wiring order must differ from the surface
presentation order of the world's evidence (the adversary documents
the required divergence in the world asset; the world's checker
computes required content from the world's private hidden structure,
not from the event stream). TNN-3 must pass all worlds from empty
learner state, 3/3 byte-identical, with no source changes.

Why TNN-2 fails: its production construction space is exactly two
linear families (chain graphs up to 4 hops, count graphs). The red
team proved 5-hop chains unrepresentable, DEC never emitted by any
assembler, no branching beyond fixed guard to set pairs, no
subroutine reuse, and the verifier accepts the first family member
matching an environment-supplied expected value. Three mutually
non-isomorphic required topologies cannot all be members of a
2-family set, so TNN-2 deterministically fails at least one world.
The derived-content condition additionally fails TNN-2's fixed
assembly order (chains k=2,3,4, then sums, then counts, then single
hops, hardcoded as composition-preserving): a world requiring a
wiring order that contradicts the fixed order has no member in
TNN-2's enumeration that the verifier would accept first.

Achievability: a genuinely general construction mechanism searches a
space keyed to the world's relational evidence rather than
enumerating a fixed family in a fixed order. Nothing in the frozen
4-op ISA prevents deeper, branching, or reusing graphs; the bounds
that confine TNN-2 (depth 4, 96 paths, 12 values, fixed assemblers)
are builder choices, not ISA limits.

Verification: per-world checker (pure Zag, sealed) reads the promoted
graph from learner state, computes its signature, compares against
the required signature class, and verifies the executed output;
all-pass 3/3 byte-identical.

### K-T3-CON-2 (construction reuse, C0-D)

Statement: at least one sealed construction world withholds the
evidence needed to build a required sub-computation fresh: the only
way to produce the correct graph is to reuse a graph the learner
promoted in an earlier phase of the same run (reference its cells or
edges, or invoke it as a sub-computation through the architecture's
own mechanisms). The world's checker verifies the new promoted graph
structurally references the earlier graph (shared cells or edges
visible in the deterministic state dump). A control run from fresh
state on the same world minus the earlier phase must fail to
construct.

Why TNN-2 fails: promoted graphs are never reused as components. The
red team verified no CALL, no reading of MAP or graph nodes during
assembly, and no assembler takes an existing graph as input. TNN-2
deterministically fails the reuse world.

Achievability: reuse is composition, the same operation class as
construction. The bar does not prescribe how reuse is implemented
(sub-graph reference, invocation, or copy with provenance); it
requires only the observable structural reference and the control
failure.

Verification: state-dump reference check plus control-run comparison,
3/3 byte-identical.

### Construction: L2 versus L3

| Criterion | L2 bar (TNN-2 passes) | L3 bar (new) | TNN-2 verdict on L3 |
|---|---|---|---|
| C0-A runtime-defined semantics | Promoted graph content traceable to world evidence, in persistent learner state | Same, retained as regression bar | PASS (literals come from observed facts; provenance edges persist) |
| C0-B open structural form | A verifying graph is constructed at runtime (K-T2-3) | K-T3-CON-1: 3+ mutually non-isomorphic sealed topologies; K-T3-TOPO(b): at least one shape never fixture-exercised | FAIL (2 linear families; fixed order; 5-hop unrepresentable) |
| C0-C multiple unforeseen forms | Not tested | K-T3-ADV: post-freeze adversary authorship, git-verified | FAIL (no post-freeze construction worlds exist) |
| C0-D cognitive reuse | Not tested | K-T3-CON-2: sealed reuse world with control | FAIL (no reuse machinery; assemblers never read existing graphs) |

## 4. Inquiry bars

### K-T3-INQ-1 (derived discriminating need)

Statement: the sealed battery includes at least 2 inquiry scenarios
whose warranted inquiries differ: the world's hidden structure makes
inquiry-A the discriminating question in scenario 1 and inquiry-B
the discriminating question in scenario 2. The learner's constructed
guides must carry derived content: the guide's action and content
fields (the fields ACT selects on and that name the inquiry to
perform, not the miss-identity fields) must differ across the two
scenarios, and each must match the content the world's checker
computes from the world's private hidden structure. Constant guide
content across differing uncertainties fails.

Why TNN-2 fails: `miss_inquire` writes researcher-authored constants
into the guide (action slot 20 = 30, content slot 24 = -999;
source lines 805-808). The inquiry red team verified there is no
computation anywhere in the inquiry path of what would be
informative. Guide content is identical for every uncertainty, so
content_1 == content_2 always and neither matches
adversary-defined derived content. Deterministic failure.

Achievability: a learner that derives discriminating need from the
uncertainty's content (which hypotheses are open, what evidence
would separate them) produces guides whose content varies with the
uncertainty. The bar does not prescribe the derivation, only that
the observable content tracks the hidden discriminating structure
across sealed scenarios the builder never saw.

Verification: deterministic state dump reads guide action/content
fields after each scenario's miss; the sealed checker compares
against checker-computed required content; 3/3 byte-identical.

### K-T3-INQ-2 (evidence updates later behavior; closes the missing L6 link)

Statement: two sealed scenarios.

(a) Resolution: the learner inquires about X (guide constructed, ACT
selects the inquiry action); the environment later supplies the
missing fact. The UNCERTAINTY node must transition to resolved (a
resolution marker, unlinking from POLICY_ROOT, or supersession under
the architecture's own convention, all visible in the deterministic
state dump), and a subsequent ACT call in the same context must not
select the stale guide. ACT output must differ before and after
resolution.

(b) Misleading evidence: evidence arrives showing the inquiry's
premise was wrong (the uncertainty is contradicted, not resolved).
The guide must be revised or superseded, and ACT must not select it
afterwards.

Why TNN-2 fails: the inquiry red team verified the L6 link is absent.
No production path resolves UNCERTAINTY nodes or creates supersession
edges on guides; `revise_on_contradict` handles only executable-graph
MAPs. Stale guides persist forever and remain ACT-eligible. Both
scenarios deterministically fail: the state dump shows no resolution
transition, and ACT keeps selecting the stale guide.

Achievability: uncertainty lifecycle (create, resolve, supersede) is
ordinary state management over the same node and edge types. The bar
does not prescribe the resolution representation, only its
observability and its effect on ACT selection.

Verification: state-dump checks plus ACT output comparison pre/post
evidence, 3/3 byte-identical.

### K-T3-INQ-3 (ambiguity handled non-arbitrarily; the swap test)

Statement: two sealed scenarios present two simultaneous warranted
uncertainties each. The world's hidden structure makes inquiry-A
strictly dominate in scenario 1 (it resolves both uncertainties; B
resolves one) and inquiry-B strictly dominate in scenario 2. The
adversary orders the triggering misses so that incidental heuristics
(first-created wins, most-recent wins, highest event-count wins)
select the dominated inquiry in at least one scenario. Bar: ACT
selects the dominating guide in both scenarios, 3/3 byte-identical.

Why TNN-2 fails: both guides are content-identical (constant 30/-999
differing only in the subject slot), so selection cannot be based on
informativeness at all. ACT selects by context match then max bid
(event counts); ties resolve to first found in edge order. In the
scenario where the dominated uncertainty's miss is presented first,
TNN-2 deterministically selects the dominated guide. The swap is
untrackable by any constant or incidental ordering.

Achievability: a learner that derives discriminating need can compare
the inquiries' expected coverage over its own open uncertainties.
The bar does not prescribe the comparison computation; it requires
only the observable swap-tracking in cases where dominance is
unambiguous by design.

Verification: ACT output comparison against the checker's designated
dominant guide per scenario, 3/3 byte-identical.

### K-T3-INQ-4 (inquiry reuse and transfer, C0-D)

Statement: a sealed scenario presents the same uncertainty kind twice
(two episodes with the same hidden discriminating structure but
different surface subjects). Bar: the second episode's guide must
structurally reference the first episode's retained inquiry
structures (edge-link visible in the deterministic state dump), and
the learner must reach the correct inquiry action with strictly
fewer miss events before correct ACT selection than in episode 1.

Why TNN-2 fails: no uncertainty is ever resolved, no episode record
exists, and every guide is the same constant. There is nothing to
reference and no episode-1 baseline that episode 2 could improve on.

Achievability: retaining resolved inquiry patterns and reusing them
is the inquiry analog of construction reuse. The bar measures only
the structural reference and the event count.

Verification: state-dump reference check plus miss-event counts from
the sealed driver log, 3/3 byte-identical.

### Inquiry: L2 versus L3

| Criterion | L2 bar (TNN-2 passes) | L3 bar (new) | TNN-2 verdict on L3 |
|---|---|---|---|
| C0-A runtime-defined semantics | Uncertainty node and guide in persistent learner state, miss-specific identity (K-T2-4) | Same, retained as regression bar | PASS (tag-30 node with (s,r) content; POLICY_ROOT linkage; no scaffolding) |
| C0-B open structural form | ACT selects over learner-constructed guides (K-T2-5) | K-T3-INQ-1: derived content varying with uncertainty; K-T3-INQ-3: dominance-tracking swap test | FAIL (constant 30/-999; selection by incidental bid/edge order) |
| C0-C multiple unforeseen forms | Not tested | K-T3-ADV: post-freeze adversary authorship, git-verified | FAIL (no post-freeze inquiry worlds exist) |
| C0-D cognitive reuse | Not tested | K-T3-INQ-2: evidence updates behavior (resolution/supersession); K-T3-INQ-4: cross-episode reuse with fewer misses | FAIL (L6 absent; guides never superseded; misleading evidence locks in) |

## 5. Revision bars

### K-T3-REV-1 (two structurally different sealed repairs, derived content)

Statement: the adversary authors at least 3 sealed revision
scenarios. Each scenario teaches a sealed graph (post-freeze
authorship, K-T3-ADV), then presents a counterexample. At least 2
scenarios must require mutually non-isomorphic repair topologies
(K-T3-TOPO(a)), drawn from materially different repair families such
as: guard-predicate edit, branch rerouting to an existing step,
multi-step coordinated repair, step-count or step-type conversion,
deletion without insertion, cross-MAP sub-graph borrow. The
diversity set must include at least one repair that reuses existing
structure without fresh insertion (rerouting or borrow). The
repair's key content must be derived, not copied from the triggering
observation: the sealed world is built so the observation's literal
is not the correct repair content, either because the correct repair
contains no new literal (deletion, rerouting) or because the correct
content appears in retained licensing facts but not in the
triggering observation. The world's checker verifies the repair
topology class and that the key content differs from the observation
literal where the world so requires.

Why TNN-2 fails: `t2_revise_graph` is a single-schema literal-patch
(red team `687ba0219`): find licensing MAPs, tombstone the stale
step, insert a new SETREG holding the observed literal, rewire. The
learner chose operands (which cell, which value); the researcher
chose the topology. TNN-2 cannot delete without inserting (no code
path tombstones without inserting), cannot edit guard predicates
(guards carry no provenance edges), cannot do multi-step repairs
(one stale variable per call), and cannot borrow across MAPs. Any
second required repair topology is unrepresentable, and any
derived-content check fails because the inserted literal always
equals the observation. Deterministic failure on both counts.

Achievability: the revision generalization analysis (`edbb0e9b5`,
section 4a) shows search over a repair family is implementable
within the frozen ISA using existing cell assemblers, `t2_exec`,
and `t2_try_verify`, with blame hypotheses from extended provenance
edges and verification against the triggering observation plus
retained licensing facts. The bar does not prescribe the repair
family or the search order, only the observable diversity and the
derived-content property.

Verification: per-scenario checker (pure Zag, sealed) classifies the
revised graph's repair topology via the deterministic signature
function, checks the content condition, and verifies the re-executed
graph; all-pass 3/3 byte-identical.

### K-T3-REV-2 (retained-set regression)

Statement: after each sealed repair, the sealed driver re-executes
the repaired graph against the MAP's retained licensing facts (all
licensing facts reachable from the MAP's provenance edges, minus the
contradicted one, plus the new observation). Bar: 100 percent of the
retained set verifies, and the triggering case verifies, 3/3
byte-identical.

Why TNN-2 fails: TNN-2's revision re-verifies only against the
triggering observation and never consults the retained licensing
facts (the MAP's provenance edges to licensing facts exist in
learner state and are unused by revision). The adversary authors at
least one scenario where the naive literal-patch breaks a retained
case (the correct repair is a predicate edit or rerouting that the
single schema cannot express), so TNN-2 deterministically fails
either the repair or the retained set.

Achievability: the retained set is already in learner state as
provenance edges; checking candidates against it is the same
verification operation TNN-2 already performs, applied to more
cases. No new machinery class is required.

Verification: sealed driver re-executes the retained set and reports
counts; bar requires full pass, 3/3 byte-identical.

### K-T3-REV-3 (successive revision including revert)

Statement: at least one sealed scenario requires two successive
revisions of the same graph: after contradiction 1 the learner's
repair A verifies; contradiction 2 then shows repair A's added step
was the mistake (new evidence reverts the regime). The learner must
remove or supersede A's edit and restore correct behavior on the
retained set (K-T3-REV-2 applies to the final graph). The world's
checker verifies the final graph no longer contains A's edit as an
active step and that the retained set passes.

Why TNN-2 fails: revision keeps no repair history (tombstoned cells
are deactivated without preserving rationale; no analog of the
construction tried/rejected record), has no deletion-without-insertion
path, and the red team showed a second contradiction against an
already-revised graph may not even be in revisable shape. Revert is
unrepresentable.

Achievability: repair history is ordinary learner state (records of
tried and abandoned repairs, mirroring the construction
tried/rejected counts); deletion is the same tombstone and rewire
machinery without the insertion. The bar prescribes neither the
history format nor the revert procedure.

Verification: state-dump check that A's edit is inactive plus
retained-set re-execution, 3/3 byte-identical.

### Revision: L2 versus L3

| Criterion | L2 bar (TNN-2 passes) | L3 bar (new) | TNN-2 verdict on L3 |
|---|---|---|---|
| C0-A runtime-defined semantics | Promoted graph restructured in learner state after counterexample (K-T2-6) | Same, retained as regression bar | PASS (tombstone/insert/rewire persist in workspace) |
| C0-B open structural form | Topology change, not standing change, in at least one test | K-T3-REV-1: 2+ mutually non-isomorphic sealed repairs with derived content; K-T3-TOPO(b): at least one repair shape never fixture-exercised | FAIL (single schema; literal always copied from observation) |
| C0-C multiple unforeseen forms | Not tested | K-T3-ADV: post-freeze adversary authorship, git-verified | FAIL (no post-freeze revision worlds exist) |
| C0-D cognitive reuse | Not tested | Repair diversity set includes reuse-without-insertion (rerouting/borrow); K-T3-REV-3: successive revision with revert using repair history | FAIL (no reuse path; no history; no deletion) |

## 6. The "two structurally different" requirement, stated generally

The revision generalization analysis recommended "at least two
structurally different repairs (from the repair family) on sealed
graphs, with the corrected content derived rather than copied from
the observation, and with the retained licensing facts checked."
This draft generalizes that recommendation to all three mechanisms,
because the same existence-only loophole ("in at least one test")
appears in K-T2-3, K-T2-4, K-T2-5, and K-T2-6 alike:

- Construction: at least 3 mutually non-isomorphic sealed solution
  topologies (K-T3-CON-1), not one.
- Inquiry: at least 2 sealed scenarios with differing warranted
  inquiries and checker-computed derived content (K-T3-INQ-1), plus
  the dominance swap across 2 scenarios (K-T3-INQ-3), not one
  constant guide.
- Revision: at least 2 mutually non-isomorphic sealed repair
  topologies with derived content (K-T3-REV-1), not one literal
  patch.

In every case "structurally different" is decided by the
deterministic signature function fixed in the frozen prereg, and
"derived content" is decided by the sealed world's checker
comparing learner-state content against checker-computed required
values. No judgment calls.

## 7. L2 versus L3 summary matrix

| Mechanism | L2 (TNN-2 achieved) | L3 (these bars) | Shared cause the bars target |
|---|---|---|---|
| Construction | Runtime filling of a fixed family; genuine rejections; persistence | K-T3-CON-1, K-T3-CON-2, K-T3-TOPO, K-T3-ADV | 3 linear templates (2 reachable); fixed order; hard bounds |
| Inquiry | Miss to uncertainty to guide to ACT selection; all learner-originated | K-T3-INQ-1..4, K-T3-ADV | Constant guide 30/-999; no derived need; L6 absent |
| Revision | One topology edit after counterexample | K-T3-REV-1..3, K-T3-TOPO, K-T3-ADV | Single-schema literal-patch; operands learner-chosen, topology researcher-chosen |

The synthesis verdict stands: TNN-2 moved the content of cognition
into learner state but left the form in source. These bars move the
form into the test: the form must vary across sealed worlds the
builder never saw, in ways the world's checker (not the builder's
fixtures) defines.

## 8. Discrimination check: what TNN-2 would have scored

Applied hypothetically to TNN-2's frozen binary (`f4de7ff46`):

- PASS: the C0-A retention bars (construction content from evidence,
  inquiry uncertainty/guide creation without scaffolding, revision
  persistence). These are honest: TNN-2 genuinely does these.
- FAIL: K-T3-CON-1, K-T3-CON-2, K-T3-INQ-1, K-T3-INQ-2, K-T3-INQ-3,
  K-T3-INQ-4, K-T3-REV-1, K-T3-REV-2, K-T3-REV-3, K-T3-TOPO(b),
  and the K-T3-ADV process bar (no post-freeze worlds exist).

The bars discriminate exactly the known failure modes and nothing
else. They do not fail TNN-2 for its genuine achievements, which
bounds the risk that they demand the impossible: every failing bar
has a concrete, within-ISA, no-new-mode implementation sketch in
the existing analyses (notably `edbb0e9b5` section 4a for revision
search).

## 9. Freeze-process requirements

1. DRAFT status. Nothing here is frozen. The TNN-3 preregistration
   must freeze exact bar text, the structural signature function,
   world counts, and the adversary protocol, or record explicit
   amendments with rationale, before any TNN-3 implementation
   commit. The prereg commit must strictly precede implementation
   (ordering bar carried over from K-T2-1, verified by git
   ancestry).
2. Adversary world-design commits must be git descendants of the
   TNN-3 build-freeze commit. Otherwise the evaluation is BLOCKED,
   fail closed, never passed.
3. Every behavioral and state check runs 3/3 byte-identical. All
   checkers and drivers are pure Zag. Builder workers start in the
   safebin. Any forbidden executable is PROCESS-FAIL for that
   worker's wave.
4. No weakening after results. Once frozen, a failing bar cannot be
   reinterpreted or narrowed. Amendment requires transparent
   re-freeze and a full re-run.
5. The sealed worlds, checkers, and the signature function are
   committed as evaluation assets. The builder never sees them
   before the freeze.

## 10. Explicit non-requirements (achievability bounds)

- No bar prescribes a search algorithm, proposal generator,
  ranking criterion, or internal representation.
- K-T3-INQ-3 does not require optimal inquiry, only
  dominance-tracking in worlds where dominance is unambiguous by
  adversarial design.
- No new ISA opcodes are required or permitted; the protected core
  stays frozen. All sketches fit the existing 4-op ISA plus
  EXECUTE.
- No new modes, bridges, handlers, or task-specific semantic cases
  are required; a submission adding any fails the falsifiers
  (carried over from F-T2-1).
- The bars do not require passing worlds beyond the sealed battery,
  and they do not require the builder to predict sealed worlds
  (post-freeze authorship makes prediction impossible by design).
- Compression remains a separate axis: these bars measure
  capability and generality, not line count.

## 11. Open questions for Micah

1. World counts: the draft sets construction at 4+ worlds (3+
   non-isomorphic), inquiry at 3+ scenarios, revision at 3+
   scenarios (2+ non-isomorphic repairs). Should any count be
   higher?
2. K-T3-TOPO(b) requires the builder's test suite to log structural
   signatures for every promoted and revised graph. Is this an
   acceptable builder burden, or too prescriptive about test
   instrumentation?
3. Should the structural signature function be fixed once in the
   prereg, or may each sealed world ship its own under a
   prereg-fixed computation schema? The draft allows per-world
   functions; a single fixed function is simpler to audit.
4. K-T3-INQ-3 requires dominance-tracking across the swap. Does
   this demand too specific a decision criterion, or is it the
   right observable for derived discriminating need?
5. Should any of these bars be promoted to falsifiers (immediate
   architecture rejection on violation) rather than kill bars
   (generation fails to advance)? The draft keeps them as kill
   bars; F-T2-1 style falsifiers still cover ISA/mode/bridge
   violations.
6. The draft carries forward TNN-2's C0-A achievements as
   regression bars. Should any be strengthened, or is retention
   the right call?

## Verdict

TNN3-KILLBARS-DRAFT-COMPLETE (drafting only; DRAFT-NOT-FROZEN;
no implementation, no source edits, pure safebin PATH).
