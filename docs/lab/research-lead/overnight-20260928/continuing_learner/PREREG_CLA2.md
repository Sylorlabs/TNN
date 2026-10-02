# PREREG: Consolidated Continuing Learner Architecture (CLA-2)

Date: 2026-09-30. Worker: LORG-to-CLA-1 Consolidation Architect.
Status: PREREG-FROZEN (architecture design only; no implementation in this commit).
Verdict label target: LORG-CONSOLIDATION-PREREG-COMPLETE.

## Mandate

Micah's 2026-09-30 consolidation ruling (B + C + E):

- LORG must NOT become a separate permanent memory subsystem.
  Memory, representation, and dependency structure are the same
  substrate problem.
- CLA-1 is the PRIMARY architecture direction.
- Fold the useful LORG ideas into the generic learner-owned
  workspace: utility evidence, dependency links, protection
  relationships, regret/history, as LEARNED STRUCTURAL STATE,
  not a separate memory engine.
- The core eviction mechanism may be generic, but the reason
  something is valuable must be represented by learner-created
  state.
- Q1: test whether the researcher-fixed choice of which
  weights/features change under regret is load-bearing; move
  selection into learner state.
- Q2: no hardcoded exception tables for protection;
  protection must carry opportunity cost/resource pressure.
- Q3: new source lines acceptable only as GENERAL cognitive
  operation, not domain knowledge; long-term target is
  decreasing specialized code.

Source preregs: CLA-1 (`b4f61ff8a`), LORG (`c830c3005`), substrate
scout (`88622725f`). This prereg supersedes CLA-1 section (d) and
the LORG design as a standalone engine. CLA-1 sections (a), (b),
(c), (e), (f) are retained unchanged unless noted. Nothing is
deleted from history: the superseded designs remain committed
and readable.

## The consolidation principle

LORG's diagnosis was correct; its packaging was wrong. The five
root causes (R1-R5), the probation mechanism, the dependency
links, the group shared-fate, and the regret adaptation do not
need a memory engine. They need a workspace that already
expresses all of them as structural conventions.

CLA-1's workspace already has: nodes with learner-assigned type
tags, a typed edge vocabulary (DEPENDS-ON, SUPPORTS, CONTRADICTS,
REFINES, INSTANCE-OF), a utility ledger, a dependency graph, a
protection set, and the DECAY primitive. Every LORG structure
maps onto these without a new format:

- LORG weight vector (6 i32) -> learner-authored evidence edges.
  There is no weight vector in CLA-2. Value is expressed by
  which evidence edges the learner authors, not by researcher
  scalars.
- LORG probation clock -> PROTECTION edges with a decay clock,
  created by the generic teach rule. Probation is protection
  with a clock; clocks are already a generic node property
  served by the DECAY primitive.
- LORG dependency link fields -> DEPENDS-ON edges (already in
  the vocabulary).
- LORG group table -> GROUP nodes with MEMBER edges. Shared
  fate falls out of the aggregation: the group node's evidence
  protects its members.
- LORG eviction ring buffer -> HISTORY nodes in the workspace,
  created from OBSERVE events by the standard event loop.
- LORG regret update rule -> the standard miss-handling rule
  applied to history. Regret is a query miss on a
  recently-evicted key; the generic response (strengthen
  evidence on the retrieval path, extend protection) is the
  same rule that handles any miss. No separate adaptation
  engine.

The result is one format, one event loop, one retention
operation. The LORG line budget (100-130) collapses into the
generic aggregation the event loop already performs.

## Design CLA-2

### (a) Protected core: retained from CLA-1, one addition

CLA-1 section (a) stands: persistent byte-addressable state,
six primitives (ALLOC, WRITE, LINK, READ, ACTIVATE, DECAY), one
generic event stream (TEACH/QUERY/ACT/OBSERVE) with world/task
identity stripped by the driver, no semantic cases, no modes,
no bridges.

Addition (the only core-side retention machinery): the eviction
routine is reduced to three generic steps that read ONLY
learner-authored workspace content:

1. PROTECTION check. Nodes carrying a live learner-authored
   PROTECTION edge are skipped. Protection edges are ordinary
   workspace content with decay clocks; the core does not know
   why a node is protected.
2. Evidence aggregation. bid(node) = fixed linear count over
   the node's learner-authored evidence edges. The core counts;
   it does not weigh. What counts as evidence is whichever
   edges the learner authored.
3. Tie-break. A learner-owned monotonic cursor in learner
   state; non-colliding by construction. Sequential writes
   spread instead of colliding. The cursor rule itself is
   learner-state content, set at bootstrap and revisable.

The core never decides what is worth keeping. It enforces
capacity over learner-justified structure. This is the direct
answer to "the core eviction mechanism may be generic, but the
reason something is valuable should be represented by
learner-created state": the reasons are the evidence edges,
and the core only counts them.

### (b) Workspace: retained from CLA-1, vocabulary extended

CLA-1 section (b) stands: one node store, fixed records
(type_tag, ref[4], payload[4]), learner-assigned tags, one edge
discipline.

The generic edge vocabulary is extended with retention-relevant
types, all domain-free:

- DEPENDS-ON, SUPPORTS, CONTRADICTS, REFINES, INSTANCE-OF
  (retained from CLA-1).
- USE: this node participated in a successful retrieval.
- CONFIRMS: this node was corroborated by an observation.
- SURPRISE: retrieval passed here but found nothing; marks
  load-bearing uncertainty (retained from CLA-1 section d).
- PROTECTION: this node is pinned, with a decay clock and a
  provenance link to the experience that justified the pin.
- MEMBER: this node belongs to a GROUP node (shared fate).
- REGRET: links a miss event to the eviction history that
  caused it.

No edge type names a domain concept (no CAUSE edge, no PLAN
edge, no WORD edge). The source audit (section: Audit) verifies
this. Structure families (fact clusters, hypothesis graphs,
executable programs, episode chains, operator models, history)
remain node-type conventions in the one store.

### (c) Mechanism integration: retained from CLA-1

CLA-1 section (c) stands unchanged: L3C v3's cover composition
as a graph operation, L3B's menu NOT integrated (gap G1), HypD
v3's selection as a learner-owned process over CANDIDATE nodes,
OpScope compressed per C74, C1's teach/query/revise loop as the
event loop, SEM as baseline/control only.

### (d) Retention: the consolidated substrate (SUPERSEDES CLA-1 section d)

The retention policy is fully expressed as workspace structure
plus the three-step core routine. There is no retention module,
no weight vector, no separate update engine.

**How value is represented.** A node's retention bid is the
count of its evidence edges. The learner justifies value by
authoring edges from experience:

- USE and CONFIRMS edges from the generic query/observation
  rules (section f): successful use leaves evidence.
- DEPENDS-ON edges from structure-building processes: a
  hypothesis protects the facts it stands on by graph
  position, because the aggregation counts dependents.
- PROTECTION edges from the teach rule (probation at birth)
  and from learner processes (pins with provenance).
- GROUP nodes with MEMBER edges declare shared fate: the
  group node's own evidence edges raise the effective bid of
  every member, so a structure survives as a unit or not at
  all.
- REGRET edges from miss-handling over history (below).

**How the C75 root causes are addressed (R1-R5 from LORG):**

- R1 (hardcoded importance weights): there are no weights. The
  policy parameters that experience can modify are the
  evidence edges themselves, which are ordinary workspace
  content. The only researcher-fixed choice is the
  aggregation form (linear count), which is content-free.
  Whether that choice is load-bearing is tested by P7.
- R2 (no newness term): the generic teach rule creates a
  PROTECTION edge with a learner-state duration on every new
  node. Newness is protection at birth, not a term in a
  formula.
- R3 (positional tie-break attractor): the learner-owned
  monotonic cursor replaces positional tie-breaking. No
  deterministic positional rule remains.
- R4 (flat representation): DEPENDS-ON edges and GROUP nodes
  give structures shared fate. A tree, a law, or a procedure
  is a connected subgraph, and eviction prices the subgraph,
  not the slot.
- R5 (no learner retention agency): every retention-relevant
  structure (evidence edges, protection pins, groups,
  history) is authored by learner processes or by the
  generic event-loop rules acting on the learner's
  experience. Retention is something the learner does.

**Regret without a weight engine (Q1).** When a query misses
and the missing key is found in the learner-authored HISTORY
(eviction records), the standard miss rule fires: create a
REGRET node linking the miss to the eviction context, and
strengthen the evidence edges on the retrieval path that
would have prevented the eviction. The probation duration
(a learner-state value) is raised by the same generic
strengthen rule, because the duration node sits on that
path. There is no fixed list of "which weights move": what
moves is whatever evidence the learner authored on the path.
The selection of what matters is fully in learner state.

Q1 load-bearing test (frozen, P7): with the authored edge set
held fixed, vary the aggregation form (sum vs max vs
threshold-count). If retention outcomes are invariant, the
linear-count choice is not load-bearing and Q1 is closed. If
outcomes differ materially, per-type contribution amounts must
be promoted into learner state as learner-authored multiplier
edges, and the design is revised under a fresh prereg. The
test decides; the prereg does not assume.

**Protection with opportunity cost (Q2).** No exception tables.
Three pressures, all structural:

1. Capacity pressure: protection edges are workspace nodes
   under the same capacity as everything else. Every pin
   costs a node that could have been knowledge. There is no
   free pin.
2. Rent: PROTECTION edges carry decay clocks served by the
   DECAY primitive. A pin survives only if the learner's
   processes re-confirm it (USE on the protected node
   refreshes the clock). Unused protection rots away.
3. Experienced consequence: a learner that protects
   everything fills its workspace with pins and decaying
   clocks, leaving no room for new evidence. The cost is
   felt as degraded retention, not as a rule violation.

P8 tests this: a probe learner forced to protect on every
teach must score worse on a subsequent retention battery
than the normal learner. If overprotection is costless, Q2
is unanswered and the design fails.

**Source budget (Q3).** The retention machinery is: the
three-step eviction routine (protection check, linear
aggregation, cursor tie-break), the generic teach/query
evidence rules (shared with the event loop), and the
protection clock handling via DECAY. Projected 40-60 new
source lines, below LORG's 100-130, and every line is the
general cognitive operation "retain by learner-authored
evidence", not domain knowledge. No line branches on world
type, relation id, or subject range; the source audit
verifies this. The long-term trajectory (tracked per
generation) must show this number decreasing as more
retention behavior moves into learner-authored structure.

### (e) Experience format: retained from CLA-1

CLA-1 section (e) stands: one append-only log, learner-
extensible kinds, C74 6-i32 episode convention, no task
labels, byte-serializable state, no-reset semantics.

Addition: HISTORY nodes (eviction records, regret records)
are ordinary workspace structures built from OBSERVE events
by the event loop, per the substrate scout's recommendation
that regret/history enter as learned structural state.

### (f) Event loop: retained from CLA-1, evidence rules stated

CLA-1 section (f) stands: one loop (TEACH/QUERY/ACT/OBSERVE)
for all capabilities. The evidence rules are now stated
generically, since they carry the retention policy:

- TEACH: encode the event into nodes; create a PROTECTION
  edge with the learner-state probation duration; link
  INSTANCE-OF/association edges to active related nodes.
- QUERY hit: create USE edges on participating nodes;
  strengthen CONFIRMS where the answer is corroborated.
- QUERY miss: create SURPRISE edges on the retrieval path;
  consult HISTORY; on a regret match, create the REGRET node
  and strengthen the path's evidence (this is the entire
  regret mechanism).
- OBSERVE: compare outcome to expectation; update evidence
  edges; on contradiction, create CONTRADICTS edges and
  retain the contradicted structure as superseded history
  (revision is first-class: the old version is evidence,
  never silently overwritten); refresh protection clocks
  on used nodes (rent paid).

Capabilities differ in the workspace structures they build,
not in the code path that builds them.

### Worked example: W9-class tree preservation (workspace terms)

A fresh W9-class world teaches 28 edge triples forming a
tree. Under CLA-2:

1. Each triple is taught; the teach rule creates a node plus
   a PROTECTION edge with the probation duration. The 28
   triples do not overwrite each other (C75 eliminated by
   the cursor and the protection check).
2. As the learner traverses edges in queries, it authors
   DEPENDS-ON edges (child to parent). The tree is now a
   connected subgraph in the workspace.
3. A learner process creates a GROUP node with MEMBER edges
   to the 28 nodes and authors evidence edges on the group
   node reflecting ongoing use. Shared fate: evicting any
   member must overcome the group's evidence.
4. Under memory pressure, the three-step routine prices the
   subgraph, not the slot. The tree survives as a unit or
   not at all; it cannot be silently hollowed out one edge
   at a time.

No tree-specific code exists anywhere in this sequence. The
same operations preserve a causal law, a procedure's steps,
or a vocabulary.

## One-System Rule accounting (prereg; measured at implementation)

- Cognition source lines added: projected 40-60 (the
  three-step eviction routine, the generic evidence rules,
  protection clock handling via DECAY). Below LORG's
  100-130 estimate. Every line is the general operation
  "retain by learner-authored evidence". Exact count is an
  implementation measurement.
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Per-world-type branches in the retention path: 0
  (verified by the source audit).
- Researcher-fixed weight/adaptation targets: 0 (Q1: no
  weight vector exists; the load-bearing test P7 decides
  whether the aggregation form needs learner-state
  promotion).
- Learner-state structures created: all within the single
  workspace format as edge-type and node-type conventions
  (evidence edges, protection edges with clocks, GROUP
  nodes, HISTORY nodes, REGRET nodes, cursor). Zero new
  state formats.

## Generation tracking

Per the standing rule, every architecture generation tracks:

| Generation | Capabilities passed | Cognition source lines | Semantic cases | Modes | Bridges | Handlers | Learner-state bytes | New learned structures |
|---|---|---|---|---|---|---|---|---|
| Frozen core (97b28e6a6) | 1/9 freeze worlds | baseline (audited at implementation) | 0 | 0 | 0 | 0 | fixed slots | 0 |
| CLA-1 (prereg b4f61ff8a) | projected | projected net-negative vs mechanism sum | 0 | 0 | 0 | 0 | workspace + log | 6 conventions |
| CLA-2 (this prereg) | projected | projected 40-60 retention lines; net-negative vs mechanism sum | 0 | 0 | 0 | 0 | workspace + log (one format) | edge/node conventions only |
| contlearn2 (control) | LEARNER-EXTENDED (179b4a950) | measured at comparison | measured | measured | measured | measured | measured | measured |

The desired trajectory: capabilities up, learner-created
state up, specialized source down, modes/bridges/handlers
at zero.

## Falsifiable predictions

For a future implementation of THIS design, evaluated on
FRESH adversarial worlds (FW1-FW9 are sealed evaluator
assets; the learner is not tuned to them; FW9 is the
designated general-substrate discriminator):

P1 (C75 eliminated): in a fresh sequential-teach stress
(36+ new facts, no intervening probes), all facts taught
within the probation window survive. Zero occurrences of
the OBSERVED-then-EVICT-same-key signature.

P2 (W4-class, fresh): 6/6 pre, 6/6 post, 6/6 revert
(frozen core: 1/6, 2/6, 3/6).

P3 (W5-class, fresh): full targeted and collateral
retention (frozen core: 1/2, 4/6).

P4 (W8-class, fresh): vocabulary recall 4/4 (frozen core:
0/4); novel induction remains a G1 matter.

P5 (W9-class, fresh): edge retention above 20/28 and
20/31 with white-box evidence of a connected DEPENDS-ON
subgraph over the taught tree, verified by traversal
(the honest oracle: a graph property, not a byte
pattern). Frozen core: 0/28, 0/31.

P6 (no single-world overfitting): the SAME implementation
achieves P2-P5 with no per-world tuning and no retention
source edits between worlds. A second round of retention
source edits is a treadmill signal.

P7 (Q1 load-bearing test): with the authored edge set held
fixed, retention outcomes are invariant across aggregation
forms (sum vs max vs threshold-count). If invariant, the
linear-count choice is not load-bearing and Q1 is closed.
If outcomes differ materially, per-type contributions are
promoted to learner state and the design is revised under
a fresh prereg.

P8 (Q2 opportunity cost): a probe learner forced to
protect on every teach scores worse on a subsequent
retention battery than the normal learner, because pins
consume capacity and rent. If overprotection is costless,
Q2 is unanswered.

P9 (Q3 generality): the source audit finds zero branches
on world type, relation id, or subject range in the
retention path; total new retention source is at most the
projected 40-60 lines; and no retention source edit is
needed across the fresh-world battery.

P10 (revision first-class): after a contradiction on a
fresh world, the contradicted structure is retrievable
as superseded history via its CONTRADICTS edges; it was
not silently overwritten.

## Falsification conditions

- F1: the slot-0 attractor (or any positional attractor)
  reappears. REJECT the design.
- F2: P5 fails while P2-P4 pass. The dependency/group
  mechanism is insufficient for structures. NARROW the
  claim to flat knowledge.
- F3: implementation requires any branch on world type,
  relation id range, or subject id range in the retention
  path. REJECT the implementation (not necessarily the
  design).
- F4: removing exactly the evidence edges authored during
  one world restores the C75 ceiling for that world's
  content while leaving other content intact fails, i.e.
  retention persists after edge removal. The core is
  smuggling policy outside learner state. REJECT the
  implementation.
- F5: the store fills with immortal junk across worlds
  (junk count rising without bound). The decay/rent
  mechanism is insufficient. REVISE under a fresh prereg.

## Named gaps (carried forward from CLA-1; not solved here)

G1 (incremental executable construction): the L3B redesign
target and the compose-verify-promote frontier. The
workspace supports executable node structures; the
algorithm is future work under a fresh prereg.

G2 (uncertainty-contingent action): W6/W7. The ACT channel
exists; the mapping from epistemic state to action
selection is future work. The learner-state ACT hypothesis
is approved; no planner or curiosity subsystem is built.

G3 (hierarchical/graph-native traversal): W9. Nodes plus
typed links express hierarchy; traversal and compositional
query machinery is future work.

## Audit requirements (from the substrate scout)

Before any capability claim on an implementation of this
prereg:

1. Source audit: no cell/node kind names a domain concept;
   the executor and the retention routine have zero domain
   semantic cases; the retention path has zero branches on
   world/task identity. The audit is adversarial, not
   self-administered.
2. Honest structural oracle, frozen before the build: what
   counts as new topology or preserved structure is stated
   as a graph property (connectivity, shared fate under
   pressure, reuse on a second probe), never as a byte
   pattern. The C77 lesson stands.
3. Citation check: structures can name and reference other
   structures (GROUP membership, HISTORY links, REGRET
   links); without citation there is no reuse to measure.
4. Post-freeze adversary family: at least one evaluation
   family designed after the freeze (FW9 is designated).

## Relationship to other lanes

- CLA-1 (`b4f61ff8a`): sections (a), (b), (c), (e), (f)
  retained; section (d) SUPERSEDED by this prereg's
  section (d). CLA-1 remains in history as the parent
  design.
- LORG (`c830c3005`): SUPERSEDED as a standalone engine by
  this consolidation. Its diagnosis (R1-R5), rejected
  alternatives, and worked examples are folded in as the
  record above. The prereg remains committed and readable.
- contlearn2: remains the competing control per ruling D.
  Compared against CLA-2 on capability, source delta,
  state formats, handlers/modes/bridges, transfer,
  freeze-challenge performance, and new capability without
  source edits. Converge after discrimination.
- FW1-FW9: sealed evaluator/adversary assets per ruling A.
  Not design hints; no tuning to them.

## What this prereg does NOT authorize

- No implementation in this commit. The implementation
  worker builds only after review.
- No new Zag subsystems, modes, bridges, task-specific
  handlers, or semantic cases may be introduced by the
  implementation. Any such addition fails K2 at review.
- No second memory engine. If the implementation grows a
  separate retention module outside the workspace and the
  three-step routine, it has rebuilt LORG and fails review.
- No per-world retention tuning. P6 and P9 are the guards.

## Kill bars for the implementation (frozen here)

K1: this prereg (frozen alone, before any implementation
commit) completely specifies the architecture: retained
CLA-1 sections, the consolidated retention substrate,
representation, evidence rules, Q1/Q2/Q3 answers,
predictions P1-P10, falsification F1-F5, gaps G1-G3,
audit requirements.

K2: the implementation contains zero task-specific
handlers, zero new hardcoded semantic cases, zero modes,
zero bridges, zero per-world-type branches in the
retention path, and zero researcher-fixed weight or
adaptation targets. Verified by source inspection at
review.

K3: pure Zag plus shell orchestration only (invoke znc,
run binaries, git ops, move/copy files); zero Python and
zero other implementation languages at every step; all
documents dash-clean via the shell-only check_no_dash.sh;
the contaminated paper untouched; commits local with
explicit pathspecs under continuing_learner/ only.
