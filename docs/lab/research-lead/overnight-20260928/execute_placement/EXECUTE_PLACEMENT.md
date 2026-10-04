# EXECUTE Placement Resolution

Date: 2026-09-30. Worker: EXECUTE Placement Resolver.
Verdict label: EXECUTE-PLACEMENT-RESOLVED.
Status: analysis only; recommendation to Micah for approval before any core change.
No implementation in this commit.

## Sources

- UNIFIED_STRUCTURES.md (commit 4ab7d3890): specifies EXECUTE(root) as a
  core graph-walker over COPY, BIND, COMPARE, BRANCH, EMIT, LINK-READ.
  Flags placement as undecided: seventh primitive or learner-constructible
  from the six.
- PREREG_CLA2.md (commit 24351fd31): six primitives retained
  (ALLOC, WRITE, LINK, READ, ACTIVATE, DECAY). No execution primitive.
- COMPOSE_OPS_SPEC.md (commit 881b17638): proposes four new ops
  (COPY, APPLY, CORROBORATE, PROMOTE) with APPLY as the traversal/binding/
  basis-execution atom. APPLY overlaps EXECUTE.

Micah's lens governs: prefer the design that explains more cognition
with fewer researcher-authored mechanisms. A seventh primitive is a
cost. It is justified only if the fixed point it provides cannot live
in learner state.

## 1. The attempted construction: EXECUTE from the six primitives

The honest attempt was made before concluding. A learner-authored
EXECUTE would look like this:

- Execution context as workspace nodes: a PC cell (current cell id),
  a flag cell, a frame node with binding slots, a step-counter cell.
  All representable with ALLOC/WRITE/LINK. No problem here.
- Traversal via READ (fetch cell contents) and ACTIVATE (neighbor
  sets). Structurally feasible.
- Value movement via WRITE. Structural duplication via ALLOC/WRITE/
  LINK rebuild (compose-ops Q2 already notes this as slower but
  sufficient). Dereference via double READ. All feasible.

What breaks is the dispatch step. Advancing one cell requires mapping
the cell's op symbol to an action: "this tag means copy," "this tag
means branch." Three variants were considered; all fail honestly:

(a) Multi-event stepping. The event loop checks a well-known run-queue
location each event; if a frame is PENDING, it performs one cell-op.
The op_tag to action mapping still has to be frozen code, now inside
the event-loop rule instead of a primitive. Same researcher-authored
content, worse locality: auditing "the executor" means auditing
event-loop branches. Plus new protocol states for pending execution
across events, which are modes in disguise, plus N events per
execution instead of one. Strictly worse on every axis of Micah's
lens. It relocates the fixed point; it does not remove it.

(b) Dispatch table in learner state. The learner authors a table
mapping op_tag to handler subgraph. To execute a cell: look up its
tag, get the handler subgraph, execute the handler subgraph.
"Execute the handler subgraph" requires interpreting its cells,
which requires the mapping, which is the table. Infinite regress.
The regress bottoms out only where some layer maps symbols to
actions directly, in code. That layer is researcher-authored frozen
code by definition, because the learner authors state, not code.

(c) Pure structural dataflow (cells fire when inputs are ready, no
program counter). Requires the core to detect readiness and schedule
firing. A scheduler is more machinery than a program-counter loop,
not less. Rejected.

The regress argument is the load-bearing claim: the interpretation
fixed point cannot be learner-owned. Therefore some seventh
primitive-equivalent is unavoidable. The "learner-constructible"
option collapses into "dispatch hidden in event-loop code," which is
more machinery by honest accounting, not less.

The real decision is therefore not whether but how much: what is the
minimal fixed point.

## 2. Deriving the minimal fixed point

Starting from the union of requirements (UNIFIED_STRUCTURES 6-op
table; COMPOSE_OPS APPLY/COPY/CORROBORATE), each entry was tested
for reduction:

- BIND: is WRITE of a value into a slot. A usage pattern, not an op.
  Dropped.
- EMIT: is WRITE to a designated output cell, or the convention that
  the caller READs the output cell after the run. Dropped as an op.
- LINK-READ (dereference): is READ of a ref field followed by READ of
  the target. The core already resolves refs during traversal.
  Dropped as an op.
- COPY (structural duplication): the learner builds a DUP procedure
  once, from the six primitives at construction time, then EXECUTEs
  it. A library procedure, not a core op. Dropped from the table.
  (Construction is not execution; no circularity.)
- COMPARE/EQ: byte equality with the result affecting control flow.
  The one value-level predicate. Kept, but fused with BRANCH (below).
- BRANCH: data-dependent control flow. Unavoidable: predication
  (execute both arms, select by flag) still needs a flag-gated move,
  which is BRANCH in disguise. Some op must read a runtime value and
  affect control. Kept, fused with COMPARE.

Fusion: separate TEST (set flag) and BRANCH (read flag) needs a flag
register in the execution context. A fused BRANCHEQ(a, b, t, f)
(compare bytes, jump) needs no flag register: simpler context
(current cell, frame, step counter). One dispatch entry instead of
two. Recommended as primary; the split form is the fallback if
flag-reuse proves load-bearing (F-J).

Arithmetic: the hard entry. Three rungs were considered:

- Rung 0 (no arithmetic): numbers as learner-built structures
  (Peano chains), arithmetic as learner-built procedures over
  MOVE/BRANCHEQ. Fails at the payload boundary: W3 teaches integer
  i32 payloads, and with only equality and branching the learner
  cannot convert a payload integer into any structured representation
  (no successor operation on the payload encoding). Memorizing sums
  is L1 lookup and fails held-out probes by design. Rung 0 is
  refuted for payload-carrying worlds. The alternative of having the
  frozen teach rule convert payloads to Peano chains would hide
  integer semantics in the teach path, which is less auditable than
  an explicit op-table entry. Rejected.
- Rung 1 (INC, DEC): successor and predecessor on integer payloads.
  ADD is learner-constructed (loop: while y != 0: x := INC(x);
  y := DEC(y)). SUB likewise. MUL is learner-constructed from ADD
  (nested loops; needs slot copying via MOVE, which is why MOVE is
  load-bearing). This rung makes W3's "discover addition" literally
  the construction of the ADD procedure: the learner invents
  addition. That is the L3-flavored outcome the program wants.
  INC/DEC is infrastructure (the numeric analogue of MOVE), not
  domain knowledge: no fact about sums lives in the core.
- Rung 2 (ADD as a single-step op, per COMPOSE_OPS): strictly more
  researcher-authored capability than rung 1, and still insufficient
  alone: MUL-from-ADD needs iteration, iteration needs a
  decrementable counter, so rung 2 silently needs DEC anyway.
  COMPOSE_OPS F6 (FW3 via learner-composed MUL-from-ADD) is
  unachievable on {EQ, ADD} without it. Rung 2 is dominated.

Recommendation: rung 1. The table is {MOVE, BRANCHEQ, INC, DEC}:
four ops. Operands are frame slots or literal cells (refs resolve
structurally). INC/DEC on non-integer payloads FAIL cleanly (a
value-kind guard, domain-neutral like the kind-guard contemplated
in UNIFIED_STRUCTURES Risk 1; the source audit verifies no semantic
cases).

Execution context: {current: node id, frame: node id, steps: int}.
No flag register (fused branch). Fixed loop: while steps < BUDGET,
READ current cell, dispatch over the 4-op table, unknown op_tag
means FAIL (closed table), advance along SEQ edges, halt on a cell
with no SEQ edge. Output: the cell referenced by root ref[0]
(resolves to a frame slot or literal cell). BUDGET is a frozen
constant, learner-visible (READable); F-F governs whether it is
load-bearing.

## 3. Frame indirection replaces the HOLE sentinel

COMPOSE_OPS specifies HOLE as a core-defined sentinel payload that
APPLY fills from bindings. The frame model makes the sentinel
unnecessary:

- The caller (query rule, miss policy, ACT handler) ALLOCs a frame
  node and WRITEs bindings into its slots. All six-primitive work.
- Procedure cells reference frame slots instead of containing HOLE
  markers. A "variable" is a ref pointing into the frame: structural,
  no reserved value.
- The learner's generalization step (COPY exemplar, mark varying
  positions) WRITEs frame-slot refs over varying positions. The mark
  is the frame-slot ref itself.

This dissolves COMPOSE_OPS Q3 (sentinel collision): there is no
reserved payload value. Binding is WRITE, not a traversal pre-pass.
Falsifiable: F-H.

## 4. APPLY and EXECUTE are the same operation

APPLY(structure, bindings) as specified: traverse, fill HOLEs,
execute basis ops, return value or clean failure. Under the frame
model this is exactly EXECUTE(root=structure, frame=bindings):
traversal is the walk, HOLE-fill is frame-slot indirection,
basis execution is the 4-op dispatch, clean failure is the
FAIL/unknown-tag/budget path. APPLY is EXECUTE's calling
convention, not a separate operation.

Disposition of the COMPOSE_OPS four (mapping to one primitive):

- COPY: learner library procedure (section 2). Dropped from core.
- APPLY: unified into EXECUTE. Not a separate op.
- CORROBORATE: EXECUTE plus BRANCHEQ(result, expected) plus WRITE
  of an outcome record. Three extra cells in the trial graph at
  learner level; no core op. (Single-case by design is preserved:
  the learner sequences cases through its policy loop.)
- PROMOTE: retention-lane operation, unchanged. It marks; EXECUTE
  never marks.

Net effect: COMPOSE_OPS' four new ops plus basis collapse to one
primitive with a 4-entry dispatch. UNIFIED_STRUCTURES' 6-op table
collapses to 4 ops. This is the architectural compression ruling H
asks for: two overlapping executor proposals with one shared deeper
mechanism.

## 5. ACT-channel interaction

Plans execute action cells through the ACT channel (ruling F:
ACT consults learner state; UNIFIED_STRUCTURES 1d: observe between
actions). Two designs:

- Yield/resume: EXECUTE suspends mid-run at an ACT-cell, the event
  loop performs ACT, then resumes. Requires continuation machinery
  in the core.
- Terminal ACT-cells with chained invocation: an ACT-cell has no SEQ
  edge, so EXECUTE halts and returns the action descriptor as its
  value. The learner-state ACT handler performs ACT, processes the
  OBSERVE event, and re-invokes EXECUTE with the updated frame for
  the next step.

Chained invocation is recommended: no yield machinery, and the
round trip matches the plan lifecycle (act, observe, compare to
PREDICTS, continue or replan) which needs event-loop involvement
between actions anyway. Falsifiable: F-I.

Nested invocation (a procedure calling a procedure): handled by
construction-time inlining (the learner splices callee cells into
the caller graph with remapped frame slots, using COPY plus WRITE;
all six-primitive work). Run time stays single-frame. True
re-entrant recursion would need a bounded frame stack; deferred to
F-G. The W2/W3 traces do not need it.

Mid-execution retrieval (a procedure doing its own lookup): the
caller performs retrieval via the six primitives and WRITEs inputs
into the frame before invoking EXECUTE. Separation: retrieval is
caller work, computation is EXECUTE work. ACTIVATE-as-an-EXECUTE-op
was considered and rejected as extra machinery; F-G covers the case
where caller-side retrieval proves insufficient.

## 6. Recommendation

Add ONE primitive to the protected core:

EXECUTE(root, frame) -> value | FAIL

- Fixed loop over a closed 4-op dispatch table: MOVE(dst, src),
  BRANCHEQ(a, b, t, f), INC(slot), DEC(slot).
- Operands resolve to frame slots or literal cells, structurally.
- Execution context {current, frame, steps}; step budget BUDGET
  (frozen constant, learner-visible); unknown op_tag and
  non-integer INC/DEC operand FAIL cleanly; halt on terminal cell;
  output via root ref[0].
- Frame allocated and bound by the caller with the six primitives.
  No HOLE sentinel. No arithmetic beyond INC/DEC. No yield/resume.
  ACT-cells are terminal; plans chain invocations.
- Source audit line: the table names no domain concept; zero
  branches on world/task identity; the integer guard is a
  value-kind check only.

This serves both lanes: it is the executor UNIFIED_STRUCTURES
specifies and the APPLY atom COMPOSE_OPS specifies, unified.
The seventh primitive is justified by the regress argument
(section 1): the interpretation fixed point cannot live in
learner state, and hiding it in event-loop code is more
machinery by honest accounting, not less.

## 7. Falsifiable criteria

- F-A (table minimality): a red team exhibits W2-class and
  W3-class execution traces on a 3-op table (e.g., MOVE subsumed
  by frame aliasing, or BRANCHEQ weakened). Then narrow to 3.
- F-B (arithmetic rung): W3-class ADD proves unconstructible
  from {INC, DEC} within BUDGET for the integer ranges the
  worlds require, and no learner-invented representation closes
  the gap. Then promote one rung (bounded ADD op) under a fresh
  prereg; the promotion is recorded as a cost against the
  trajectory, not a win.
- F-C (placement): a red team demonstrates op_tag to action
  mapping genuinely resident in learner-revisable state with no
  regress (the construction section 1 claims is impossible).
  Then remove the primitive.
- F-D (APPLY distinctness): a required calling pattern from the
  compose-verify-promote frontier proves inexpressible via frame
  indirection without new core machinery. Then split APPLY out.
- F-E (oracle audit): COMPOSE_OPS O1-O3 applied to this spec.
  If capability survives randomization of the learner's
  construction choices (which positions get frame refs, trial
  order, promotion threshold), the primitive is the oracle.
  Reject it.
- F-F (budget): the BUDGET value proves load-bearing per
  capability (different budgets, different capability sets,
  budget tuned per world). Then the budget moves to learner
  state or the design fails review.
- F-G (re-entrancy): a required capability needs nested
  invocation that construction-time inlining cannot express.
  Then add a bounded frame stack under a fresh prereg.
- F-H (frame vs HOLE): frame-slot indirection proves unworkable
  in the W2/W3 construction traces (e.g., the exemplar policy
  cannot express "varying position" without a sentinel). Then
  adopt the HOLE sentinel under a fresh prereg.
- F-I (ACT chaining): interleaved act-observe-act proves
  inexpressible via chained EXECUTE invocation (the frame
  cannot carry the continuation). Then add yield/resume under
  a fresh prereg.
- F-J (fused vs split branch): flag-reuse across multiple
  branches proves load-bearing in a real trace. Then split
  TEST/BRANCH.

Retained from the source docs and still binding: COMPOSE_OPS
O1-O3, P1-P5, F1-F7 (with F6 re-read against rung 1: FW3 must be
reachable via learner-composed MUL from learner-composed ADD
from INC/DEC, or the rung is falsified per F-B);
UNIFIED_STRUCTURES U1-U5 (score parity, state bound, boundary
crossing, tag plasticity, no dispatch growth) and S1-S3 (split
necessary conditions).

## 8. Prereg-level amendments

These amendments are specified here for Micah's approval. They
authorize no implementation; the implementation prereg follows
approval.

Amendment A (to PREREG_CLA2 section (a), Protected core):
Add a seventh primitive with the exact spec in section 6 above:
EXECUTE(root, frame) -> value | FAIL; closed dispatch over
{MOVE, BRANCHEQ, INC, DEC}; operands resolve to frame slots or
literal cells; execution context {current, frame, steps}; frozen
learner-visible BUDGET; clean FAIL on unknown op_tag,
non-integer INC/DEC operand, or budget exhaustion; halt on
terminal cell; output via root ref[0]. The frame is caller-
allocated with the six primitives. Rationale: the regress
argument (section 1). Audit requirement: the dispatch table
names no domain concept; zero branches on world/task identity.

Amendment B (to COMPOSE_OPS_SPEC sections 2.2, 2.3, and 8):
APPLY is struck as a separate operation and re-specified as the
calling convention of EXECUTE (root plus frame bindings).
COPY is struck from the core op set; re-specified as a learner
library procedure built from the six primitives at construction
time. CORROBORATE is struck from the core op set; re-specified
as learner-level composition (EXECUTE, then BRANCHEQ against
expected, then WRITE of the outcome record). The HOLE sentinel
(2.3) is struck; replaced by frame-slot indirection (section 3
above). PROMOTE is retained unchanged in the retention lane.
All oracle tests (O1-O3), predictions (P1-P5), and falsification
conditions (F1-F7) are retained and now apply to EXECUTE, with
F6 re-read per section 7.

Amendment C (to UNIFIED_STRUCTURES section 2, The ONE generic
execution operation): the op table {COPY, BIND, COMPARE, BRANCH,
EMIT, LINK-READ} is replaced by {MOVE, BRANCHEQ, INC, DEC} per
the reduction in section 2 above. BIND, EMIT, and LINK-READ
become documented usage conventions over WRITE/READ. COPY
becomes a learner library procedure. The machine-code analogy
is retained with a 4-instruction ISA. Risk 5's audit line
(no op_tag richer than the table) now guards 4 entries.

## One-System Rule accounting (analysis only)

- Cognition source lines added: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New task-specific handlers: 0.
- Proposed new core surface: 1 primitive, 4-entry closed dispatch
  (projected small; measured at the implementation prereg).
- Learner-state structures created: 0.
- Net architectural effect if approved: two executor proposals
  (UNIFIED_STRUCTURES EXECUTE, COMPOSE_OPS APPLY/COPY/CORROBORATE)
  merge into one primitive; the learner's construction burden
  grows (frame refs, inlining, learner-built ADD/MUL, learner-
  level CORROBORATE) while fixed core machinery shrinks to the
  provable minimum.

## Kill bars (this analysis)

K1: the analysis addresses the open placement question from the
three cited commits, attempts the learner-side construction and
names exactly what breaks (the regress argument), derives the
minimal fixed point entry by entry, resolves the EXECUTE/APPLY
overlap, and specifies the decision as prereg amendments A-C
with falsifiable criteria F-A through F-J.

K2: no implementation exists or is proposed beyond the single
justified primitive; no per-capability handlers, modes, or
bridges are introduced; the recommendation reduces net proposed
core surface (4 proposed ops collapse to 1).

K3: pure markdown; dash-clean via the shell-only check script;
contaminated paper verified zero-diff before and after; zero
Python at every step; commit confined to the owned path with
explicit pathspecs.
