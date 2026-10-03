# Unified Structures: One Workspace for Procedures, Causal Rules, Hypotheses, Plans, and Linguistic Relations

Date: 2026-09-30. Worker: Unified Structure Explorer.
Verdict label: UNIFIED-STRUCTURES-EXPLORATION-COMPLETE.
Status: exploration/prereg level. No implementation. No existing code modified.

Governing ruling: Micah's architecture ruling I (2026-09-30):
proc + causal should become different learned structures executed through
the same substrate, not separate stores connected by a smarter router.
Replacing two handlers with one more abstract handler is not sufficient.
The distinction must emerge from learner structure, not source architecture.

Substrate assumed: CLA-1 (PREREG_CLA1.md, frozen b4f61ff8a).
Nodes are (type_tag, ref[4], payload[4]). The learner assigns type_tag
through use; the core never interprets tags. Edge vocabulary:
DEPENDS-ON, SUPPORTS, CONTRADICTS, REFINES, INSTANCE-OF.
Core primitives: ALLOC, WRITE, LINK, READ, ACTIVATE, DECAY.
One event stream: TEACH, QUERY, ACT, OBSERVE. No task labels.

## Thesis

All five cognitive objects are executable node/edge graphs built from one
fixed tiny cell algebra. They differ not in storage, handlers, or code
path, but in three structural properties:

1. the edge discipline surrounding the graph (what it is linked to),
2. the learner-assigned type-tag convention (first use defines the type),
3. the event-stream context in which the graph is executed
   (QUERY, ACT, or OBSERVE-comparison).

No handler branches on kind. No router classifies input by syntax.
The proc/caus split in the unified learner (separate PBASE/CBASE,
separate handlers, route_line's 5 syntax codes) is replaced by one
learn function, one query function, and one execute primitive.

## 1. The five structures as workspace graphs

### 1a. Procedure

Current form: PBASE entries, e.g. L3B v2's CREATE/CONNECT assembly over
a 205-program menu; learned by handle_proc_learn, queried by
handle_proc_query.

Workspace form: an ordered graph of cell nodes. Each cell node carries a
learner-assigned type_tag naming a cell-algebra operation (see section 2)
and refs to operand cells. SEQ edges order the cells. A procedure root
node is tagged PROC by the learner on first construction and linked to
its cells with CONTAINS edges (a new generic edge kind, or ref slots).

What makes it executable: the generic EXECUTE primitive (section 2)
walks the cell graph from the root, performing each cell's operation.
A procedure is invoked by binding input values to its input cells and
reading the output cell after traversal.

Example sketch (string doubling, in node terms, not code):
root(PROC) -> c1(COPY input to temp), c2(COPY input to out),
c3(APPEND temp to out). The learner authored the cells; the core only
walks.

### 1b. Causal rule

Current form: CBASE entries, e.g. integer-triple rules learned by
handle_caus_learn from iii>ii episodes; queried by handle_caus_query;
revised by handle_caus_revise with history.

Workspace form: the SAME executable cell-graph form as a procedure,
but surrounded by a different edge discipline. The rule root is tagged
CAUS by the learner. It carries SUPPORTS edges to the evidence nodes
(the episodes that corroborated it) and is eligible for CONTRADICTS
edges when observations disagree. The rule's body is a cell graph that
computes a predicted value from bound inputs, exactly like a procedure
body.

What makes it executable: the same EXECUTE primitive, run in a
prediction context. On QUERY the result is returned as an answer.
On OBSERVE the result is compared to the actual outcome; match
strengthens the SUPPORTS edges (utility update), mismatch creates a
CONTRADICTS edge and triggers relearning from fresh evidence
(the C1-style revision loop, no REVISION_MODE).

The structural difference from a procedure: evidence edges.
A procedure has none; it is a capability, justified by successful use.
A causal rule is a claim about the world, justified by SUPPORTS edges
and vulnerable to CONTRADICTS edges. Same graph, different surrounding
structure, different lifecycle.

### 1c. Hypothesis

Current form: L3C v3's cover-set atoms and DISP/TERM rules; HypD v3's
CANDIDATE population.

Workspace form: a hypothesis node tagged HYP by the learner, linked to
atom or component nodes with PART-OF edges and to evidence nodes with
SUPPORTS edges. When the hypothesis is a covering dispatch (L3C style),
its body is again a cell graph: predicate cells feeding a dispatch cell.
When it is a candidate under selection (HypD style), it carries a
utility record and competes via the protection set.

What makes it executable: EXECUTE runs the body to produce a verdict
or a classification. The hypothesis lifecycle (promote on corroboration,
demote on contradiction) is handled by the utility ledger and the
protection set, not by hypothesis-specific code.

The structural difference from a causal rule: a hypothesis is
provisional by convention. The learner tags it HYP rather than CAUS,
and the learner's own promotion process (compose, verify, promote,
per the L3 integration ruling) may retag or relink it as CAUS when
corroboration crosses the learner's own threshold. The promotion
threshold is learner state, not source code.

### 1d. Plan

Current form: none exists. W7 fails because the core stores transition
triples but has no path from triples to CHOICE (W6W7 analysis,
e7bb3d0bc).

Workspace form: a plan root tagged PLAN, linked to a GOAL node with
AIMS-AT, and to a sequence of action cells with SEQ edges. Each action
cell links to an EXPECTED-OUTCOME node with PREDICTS. The action cells
are executable in the same cell algebra; the expected-outcome nodes are
compared against OBSERVE events after acting.

What makes it executable: EXECUTE runs the action sequence through the
generic ACT channel (the learner-state-consulting ACT handler from the
W6W7 analysis). After each ACT, OBSERVE is compared to the PREDICTS
linked outcome; divergence updates utility and may trigger replanning
(rebuild the graph from the updated model).

The structural difference from a procedure: a plan is indexed by a
goal and carries expectations. A procedure maps inputs to outputs; a
plan maps a current state plus a goal to an action sequence with
predicted intermediates. Same cells, same executor, different
surrounding edges (AIMS-AT, PREDICTS) and different invocation context
(ACT rather than QUERY).

### 1e. Linguistic relation

Current form: string-pair associations in procedure invention
(str>str examples); vocabulary triples in the frozen core's fact store.

Workspace form: symbol nodes linked by INSTANCE-OF to category nodes
and by REFINES to more specific forms. A linguistic relation (e.g. a
word-to-meaning mapping, a compositional rule) is a small cell graph
that maps a symbol structure to another symbol structure: BIND cells
attach symbols to roles, COMPOSE cells assemble novel combinations.

What makes it executable: EXECUTE runs the mapping on QUERY (interpret
an utterance) or during TEACH (encode a new utterance into workspace
structure). Compositionality comes from the graph form itself: a novel
combination is a novel graph assembled from familiar cells.

The structural difference from a procedure: the operands are symbols
and the edges carry linguistic relations (INSTANCE-OF hierarchies,
composition links) rather than data flow alone. But the cells and the
executor are identical. A linguistic relation that computes is,
structurally, a procedure over symbols; the learner's tagging and
the query context mark it as linguistic.

## 2. The ONE generic execution operation

The core provides exactly one execution primitive beyond the CLA-1 six:

EXECUTE(root): walk the cell graph reachable from root following the
fixed discipline below, performing each cell's operation, and return
the designated output cell's value.

The fixed discipline (core code, domain-neutral, audited to name no
domain concept):

- Cells are (op_tag, ref[4], payload[2]). op_tag is learner-assigned;
  the core maps a SMALL FIXED SET of op_tags to structural operations:
  COPY (copy value between refs), BIND (attach a value to a named
  role), COMPARE (equality test on opaque values, result to a flag
  cell), BRANCH (follow one of two SEQ edges based on the flag),
  EMIT (place a value on the output channel), LINK-READ (dereference).
- No arithmetic, no string primitives, no domain operations in the
  core. Opaque values only. If the learner needs addition, the
  learner builds it from cells or the cell graph references a
  previously learned structure; the core never knows it is adding.
- Termination: a step budget (learner-visible state, fixed constant
  in core). Exceeding it halts with a distinguished flag. No
  infinite loops can hang the core.
- The dispatch from op_tag to operation is a fixed table in core
  code. The learner cannot add op_tags that name new core
  operations; it can only compose the fixed set. This is the line
  that keeps EXECUTE generic: the operation set is closed and
  domain-neutral, while everything built from it is open and
  learner-owned.

Why this is not "one giant intelligent oracle": the core understands
nothing about procedures, causes, plans, or language. It copies,
compares, branches, and emits opaque values. All intelligence is in
the graphs the learner builds. This is the same relationship as
machine code to programs: fixed tiny instruction set, unbounded
programs.

What the core does NOT provide: no procedure constructor, no causal
induction, no planner, no parser. Construction is the learner's job
(gap G1 in CLA-1; the compose-verify-promote frontier in ruling G).
The core provides the paper; the learner writes on it.

## 3. How the learner distinguishes the five (structure, not source)

Three mechanisms, all in learner-owned state:

(a) Type-tag conventions. The learner assigns tags on first use:
PROC for capability graphs, CAUS for world-claim graphs, HYP for
provisional graphs, PLAN for goal-indexed sequences, LEX for
symbol-mapping graphs. The core never reads tags. If the learner
later uses one tag for two roles and behavior is unchanged, the
distinction was never load-bearing; that is an experimental result,
not a design failure.

(b) Surrounding edge discipline. A graph with SUPPORTS edges to
evidence and exposure to CONTRADICTS is treated by the learner's
own processes as a claim (causal rule or hypothesis). A graph with
AIMS-AT to a goal and PREDICTS to expectations is treated as a plan.
A graph with neither, invoked for its output, is treated as a
procedure. The learner's maintenance processes (utility update,
protection, revision) key off these edges, not off source branches.

(c) Invocation context. The same graph executed on QUERY answers;
executed through ACT acts; executed against OBSERVE predicts.
The event stream (TEACH/QUERY/ACT/OBSERVE) is the context the
driver provides; the learner's dispatch is a learned structure
(goal + hypotheses + expected consequences + uncertainty, per
ruling F), not a source switch.

Falsifiability of the emergence claim: if a future experiment shows
the learner systematically tagging all five identically while
preserving all battery scores, the five-way distinction is proven
to be researcher-imposed, and the design is vindicated in the
strongest form. If instead some battery fails unless two tags are
kept distinct AND the maintenance processes branch on the tags in
learner state (not source), the distinction is real but still
learner-owned, which satisfies the ruling.

## 4. What breaks, what might be lost, and how we detect it

Risk 1: loss of surface-type safety. The router currently guarantees
procedures see strings and causal rules see integer triples. One
substrate accepts mixed content; a malformed invocation becomes a
learner error rather than a routing impossibility.
Detection: mixed-content probe battery. If EXECUTE on mistyped input
halts cleanly with the step-budget flag and the learner records a
CONTRADICTS edge (learning from the error), the risk is managed. If
mistyped invocations corrupt neighboring structures, the cell algebra
needs a value-kind guard (still domain-neutral: opaque kind tags).

Risk 2: state bloat. PBASE/CBASE fixed formats are compact; a generic
node store costs more bytes per entry (refs, tags, edges).
Detection: Micah's tracking metric LEARNER-STATE BYTES. The
unification must reproduce battery scores within a bounded multiple
(suggest: 3x) of the split implementation's state. Above that, the
generality is not paying for itself.

Risk 3: revision semantics. handle_caus_revise keeps history and
supports targeted revision; procedures are replaced wholesale.
One substrate needs one revision operation that preserves both
behaviors: history-linked supersession for claims (old graph kept,
linked by SUPERSEDED, still inspectable) and replacement for
capabilities.
Detection: run the causal-revision battery (K-U series) and the
procedure battery against the unified implementation. Any score
drop on revision-specific probes is a unification failure, not a
tolerable cost.

Risk 4: ambiguity resolution. The router's syntax split made some
inputs unambiguous by construction. One substrate faces genuinely
ambiguous content.
Detection: the intent/ambiguity battery (K-U4a/a2). The unified
design must reproduce withholding-on-ambiguity scores using
substrate-native signals (multiple matching graphs with divergent
outputs), per audit consolidation 3. Failure here means the
router was doing real disambiguation work that the substrate
must relearn, which is fine, but the scores must show it.

Risk 5: the bridge dissolves badly. The bridge's (pos,val)
conditional becomes a predicate subgraph. If predicate subgraphs
cannot express the learned conditions without a dedicated
condition form, we have smuggled the bridge back in as a
cell-algebra extension.
Detection: audit the op_tag table. If any op_tag names a
condition form richer than COMPARE on opaque values, the
unification cheated. The table must stay closed and domain-neutral.

## 5. Falsifiable predictions

### Unification works if ALL of the following hold (U1-U5):

U1 (score parity): one learn function, one query function, one
EXECUTE primitive, zero router codes, zero proc/caus handler split,
zero dedicated bridge functions reproduce the K-U1 through K-U5
unified-learner battery scores exactly.

U2 (state bound): learner-state bytes for the unified implementation
are within 3x of the split implementation on the same batteries.

U3 (boundary crossing): at least one learned structure emerges that
the old architecture could not express: e.g. a causal rule whose
body is reused as a procedure step, or a plan whose action cells
invoke a learned linguistic mapping. The old stores made this
impossible by construction; the workspace must make it routine.

U4 (tag plasticity): the learner's type-tag assignments are
observable in white-box state, and an experiment that merges two
tags (e.g. HYP into CAUS after corroboration) preserves scores,
showing the distinction is conventional, not architectural.

U5 (no new dispatch growth): adding a sixth cognitive object
(e.g. an analogy structure) requires zero new core operations and
zero new op_tags; it is a new tag convention plus new edge
patterns only. If the core must grow per capability, the
unification failed and the treadmill returned in disguise.

### The split is necessary if ANY of the following hold (S1-S3):

S1 (irreducible score gap): some K-U battery score cannot be
reproduced without reintroducing a branch on content kind in the
learn or query path, after good-faith attempts under the unified
design. The branch must be shown load-bearing by ablation
(remove it, score drops; keep everything else, score holds).

S2 (dispatch treadmill): each new capability added to the unified
substrate requires a new op_tag or a new core operation, so the
"closed" cell algebra grows with the capability count. This is
the old subsystem treadmill wearing a workspace costume.

S3 (systematic ambiguity): mixed-content queries produce
ambiguity at rates that no learner-owned disambiguation process
resolves, and scores recover only when syntax-based routing is
restored. This would prove the router was load-bearing
machinery, not merely an admission gate.

## Relation to the other lanes

- CLA-1: this exploration is a detailed sketch of CLA-1 section
  (b)'s claim that "executable programs" live in the workspace as
  node-type conventions. EXECUTE is a candidate seventh primitive
  (or a fixed composition of the six). Whether it belongs in the
  protected core or is itself learner-constructible is open; the
  prereg for implementation must decide and defend the choice.
- LORG: the utility ledger, dependency graph, and protection set
  apply unchanged to executable graphs. A procedure node with
  dependents is preserved by graph position; a hypothesis with
  live SUPPORTS edges resists eviction. Retention and execution
  are orthogonal; both live in the workspace.
- Ruling G (compose-verify-promote): the construction algorithm
  that BUILDS these graphs from experience is the named frontier
  and is deliberately out of scope here. This document specifies
  the representation and execution; G specifies the learning.
- Ruling I: this is the direct answer to the consolidation
  target. Audit consolidations 1 (unify proc/caus) and 2
  (generalize the bridge) both dissolve into this design; the
  bridge's conditional becomes a predicate subgraph, and the
  router's five codes become unnecessary.

## One-System Rule accounting (exploration; no code)

- Cognition source lines added: 0 (design only).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures sketched: executable cell graphs with
  five tag conventions (PROC, CAUS, HYP, PLAN, LEX), CONTAINS and
  AIMS-AT and PREDICTS edge kinds added to the CLA-1 vocabulary,
  all learner-assigned.
- Projected core addition if implemented: one EXECUTE primitive
  with a closed domain-neutral op table (est. small; measured at
  implementation prereg).

## Kill bars (for this exploration)

K1: the design addresses Micah's ruling I directly, sketches all
five structures as workspace graphs, specifies the one execution
operation, states how the learner distinguishes them structurally,
names what breaks with detection methods, and gives falsifiable
predictions U1-U5 and S1-S3.

K2: no implementation exists; no proc/caus code was modified; the
document proposes no per-capability handlers, modes, or bridges.

K3: pure markdown; dash-clean via the shell-only check script;
contaminated paper verified zero-diff; zero Python at every step;
commit confined to the owned path with explicit pathspecs.
