# MUL-from-ADD Construction Scout

Date: 2026-09-30. Worker: MUL-from-ADD Construction Scout.
Verdict label: MUL-SCOUT-COMPLETE.
Status: scout/specification level. No implementation. Analysis only.

## Mandate

Micah's ISA boundary ruling (0525377f3): do NOT add MUL to the protected
core because FW3 needs multiplication. Test whether the learner can
construct and persist MUL from the generic computational basis. "That
would be very interesting L3-ish evidence."

The EXECUTE placement analysis (1fc77503b) adds: the {INC, DEC} rung
beats {ADD}, because MUL-from-ADD needs a decrementable counter anyway,
and INC/DEC forces the learner to construct ADD itself, which is the
L3-flavored outcome the program wants.

This scout specifies what that construction would look like, what
experience it needs, how discovery could work under the trial-based
(no finite-difference) constraint, what counts as genuine construction
under the L3 criteria, and the falsifiable predictions for the
experiment.

## 1. The construction target: MUL as a workspace structure

Per the unified structures thesis (4ab7d3890), a procedure is an
executable node/edge graph in the single workspace:

- A root node, tagged PROC by the learner on first construction
  (the core never interprets tags).
- CONTAINS edges (or ref slots) from the root to cell nodes.
- SEQ edges ordering the cells.
- Each cell carries a learner-assigned op_tag naming a cell-algebra
  operation and refs to operand cells.
- Invocation: the caller ALLOCs a frame node, WRITEs input bindings
  into its slots (six-primitive work), then EXECUTE(root, frame)
  walks the graph; the output is read from the cell referenced by
  root ref[0]. Frame-slot indirection replaces any HOLE sentinel
  (per the EXECUTE placement, section 3).

A learner-constructed MUL(x, y) is a PROC graph with this shape
(one natural form; the learner's actual topology may differ, and
that variance is evidence, see section 5):

```
frame slots: [x] [y] [result] [i]
cells:
  c1: MOVE(result <- 0)          ; initialize accumulator
  c2: MOVE(i <- 0)               ; initialize counter
  c3: BRANCHEQ(i, y, ->c6, ->c4) ; termination test
  c4: MOVE(result <- ADD(result, x))  ; accumulate
  c5: MOVE(i <- ADD(i, 1))       ; advance counter; SEQ back to c3
  c6: (terminal)                 ; output via root ref[0] -> result slot
```

Graph properties that make this MUL and not a lookup table:

- It contains a back-edge (c5 SEQ to c3): the structure iterates.
- It contains an accumulation cell (c4): the output slot is both
  read and written across iterations.
- It contains a data-dependent termination test (c3): the trip
  count varies with the input y.
- Input slots x and y are referenced but never overwritten:
  the procedure is a pure function of its inputs.

These are checkable as graph properties on the white-box state,
never as byte patterns. Any correct reusable construction counts,
including forms the researcher did not sketch. A more efficient
learner-invented form (doubling, Egyptian/peasant multiplication,
or anything the scout author did not think of) is STRONGER
evidence, because a template would produce the naive loop.

## 2. The basis question: two rungs

The ISA boundary ruling approves ADD as a core primitive. The
EXECUTE placement recommends the {INC, DEC} rung. The scout
specifies the construction on both, because they are different
strengths of evidence.

Rung A (approved ISA basis): {MOVE, BRANCHEQ, ADD, EQ-as-part-of-
BRANCHEQ} plus literal cells. The loop above is expressible:
the counter advances by ADD(i, 1) using a literal 1 cell, and
terminates on BRANCHEQ(i, y). No SUB, INC, or DEC is needed.
The learner must discover the use of the literal 1 as the step.
This is the experiment to run first, because the basis is frozen
and approved.

Rung B (deeper L3 test): {MOVE, BRANCHEQ, INC, DEC}. Here ADD
itself is learner-constructed first (loop: while y != 0:
x := INC(x); y := DEC(y)), and MUL is constructed on top of the
learner-built ADD. Two levels of genuine construction. This is
the stronger experiment and the one the placement doc calls
"the L3-flavored outcome." It should follow Rung A, not replace
it: if Rung A fails for basis reasons rather than construction
reasons, Rung B diagnoses the difference.

Frozen constraint (both rungs): no new arithmetic op may be
added to pass the experiment. If the learner cannot express
iteration on the frozen basis, that is a finding about the
basis (F-B territory), not a license to add MUL, SUB, or a
loop primitive. The ruling is explicit: freeze the basis
deliberately; do not grow it one benchmark at a time.

## 3. Required experience

Two experience designs, in order of increasing evidential strength.
The experiment should run the strong one; the weak one is a
diagnostic control.

Weak (scaffolded): paired demonstrations showing the additive
decomposition, e.g. (3, 4) -> 12 alongside 3+3+3+3 = 12.
The alignment hands the learner the key insight. If the learner
succeeds here but not on the strong design, the construction
was scaffolded, not discovered. Useful for debugging the
execution path, not for the L3 claim.

Strong (bare exemplars): multiplication pairs only, e.g.
(3,4)->12, (2,5)->10, (4,3)->12, (5,5)->25, with held-out
probes such as (6,7)->42 and (3,9)->27. No additive
decomposition is shown. The learner must discover that
iterated accumulation reproduces the outputs.

The natural curriculum, and the scout's recommended staging:

- Phase 1: the learner constructs ADD (Rung B) or practices
  with ADD as given (Rung A), on addition exemplars.
- Phase 2: multiplication exemplars arrive. Queries miss
  (no MUL structure exists). The miss policy triggers
  trial-based composition (section 4).
- Phase 3: held-out probes test the promoted structure.
- Phase 4 (transfer): the constructed MUL is invoked as a
  subroutine in a novel problem (e.g., area computations,
  or a compound expression), without researcher intervention.

The Phase 1 to Phase 2 transition is where the most interesting
evidence can appear: if the learner reuses the ADD loop's shape
(one level up: accumulate ADDs the way ADD accumulates INCs),
that is compositional reuse of a learner-built structure, which
is C0-D (cognitive reuse) satisfied inside the experiment itself.

## 4. Discovery: trial-based composition

The ISA ruling removed finite-difference regularity detection
from core intelligence. Discovery must be trial/compositional
using learner-created structures. The scout specifies the
mechanism at the level the CAM-1 PROPOSE step would need:

On QUERY miss for a multiplication probe, the miss policy
(INCOMPAT-2's MISS_POLICY register, approved in the coordinator
package) proposes candidate programs. Candidates are assembled
from a generic assembly vocabulary, not from a multiplication
schema. The vocabulary:

- initialize: WRITE a literal (0 or 1) into a frame slot.
- accumulate: ADD a slot into the result slot.
- step: advance a counter slot (ADD(i,1) on Rung A; INC on Rung B).
- test: BRANCHEQ between two slots, with a back-edge target.
- sequence: SEQ-link cells in an order.

These moves are domain-neutral: initialize/step/test/sequence
describe any loop, not multiplication. Composing them into the
MUL graph is the construction. The search is bounded: skeletons
up to K cells, hole fillers from {x, y, result, counter,
literals}. Each candidate is EXECUTEd on the exemplar inputs;
CORROBORATE (learner-level: EXECUTE, BRANCHEQ against expected,
WRITE outcome) scores it; the candidate predicting all
exemplars is PROMOTEd as a PROC node.

Honest difficulty statement: the program-search policy (which
skeletons to try, in what order) is itself an open frontier,
the "plan constructor" gap named by the composition scout.
The MUL experiment does not need to solve program search in
general; it needs a bounded, generic, domain-neutral search
whose biases are stated up front and audited (the oracle test:
randomize the trial order; if capability survives, the search
was the oracle). The scout banks this as the load-bearing
design question for the experiment prereg author.

What the researcher must NOT supply: a "repeated addition"
schema, a loop-with-accumulator template, or the knowledge
that multiplication is iterated addition. The assembly moves
above are the ceiling on researcher contribution. Anything
that names the target regularity is template contamination
(section 5, F-MUL2).

## 5. What counts as genuine construction: the L3 bar

Micah's Criterion 0, applied to MUL:

- C0-A (runtime-defined semantics): the MUL procedure's cells
  live in learner-owned workspace state. The source contains
  no multiplication branch, no MUL op_tag in any dispatch
  table, no special case. The audit question "where are the
  semantics of multiplication implemented" must be answerable
  with "in this learner-authored PROC graph," pointing at
  workspace bytes, not source lines.
- C0-B (open structural form): the final graph's exact
  topology (cell count, wiring, which rung, which efficiency)
  emerges from the construction process. It is not selected
  from a finite researcher-enumerated family. Falsifier: the
  learner's MUL is always exactly the researcher's sketch
  (section 1) down to cell count, across runs and seeds.
- C0-C (multiple unforeseen forms): after the mechanism is
  frozen, expose it to sealed families requiring materially
  different constructed procedures (exponentiation via
  repeated MUL is the natural next rung; integer division
  via repeated subtraction another). At least one family
  designed by an independent adversary after freeze.
- C0-D (cognitive reuse): the constructed MUL improves
  performance on something beyond the training probes:
  held-out pairs, subroutine use in a compound task, or
  transfer across a changed surface encoding. Existence
  of the graph is not enough.

The 12 criteria, MUL-specific notes on the load-bearing ones:

- (5) white-box trace: the construction trace must show the
  assembly moves producing the loop, the failed candidates
  tried and rejected (anti-hardcoding evidence: ADD selected
  among genuinely tried alternatives, per the compose-ops
  P2 pattern), and the promotion event.
- (7) ablation: delete the MUL PROC node (only it) from the
  workspace; multiplication queries must fail while addition
  and unrelated capabilities are intact. If performance
  persists, the capability was elsewhere (memorized pairs,
  core smuggling).
- (10) beats memorization: a lookup-table control trained
  on the same exemplars must fail the held-out probes that
  MUL passes. The held-out set must include pairs whose
  products never appeared in training in any form.
- (11) red team: an independent adversary tries the
  template-contamination and core-smuggling breaks below.
- (12) revisability: present a counterexample the initial
  construction mishandles (zero: MUL(x, 0); or negatives).
  The learner must revise the structure, not require a new
  template. A construction that cannot survive first
  contact with zero is brittle, not intelligent.

Template-contamination check (the sharpest anti-spoof):
enumerate every structural commitment the researcher made
(the assembly vocabulary, the search bound, the frame
model). Then verify the learner's MUL contains at least
one structural decision the researcher did not make: the
choice of accumulation order, the counter direction, the
termination form, or an efficiency improvement. If the
final graph is fully determined by researcher choices,
the learner selected, not constructed.

## 6. Falsifiable predictions

Predictions (the experiment should confirm):

- P-MUL1: after N bare multiplication exemplars (N fixed in
  the prereg), the learner PROMOTEs a PROC structure that
  computes x*y correctly on all held-out probes.
- P-MUL2: white-box: the promoted graph contains a back-edge
  (iteration), an accumulation cell, and a data-dependent
  termination test, verified as graph properties.
- P-MUL3: ablation: removing only the MUL PROC node destroys
  multiplication performance; all other capabilities intact.
- P-MUL4: reuse: the learner invokes the constructed MUL as
  a subroutine in a novel compound task with no researcher
  intervention between construction and reuse.
- P-MUL5: the lookup-table control, trained on identical
  exemplars, fails held-out probes that MUL passes, by a
  margin fixed in the prereg.

Falsifiers (any one kills or downgrades the claim):

- F-MUL1 (memorization): the promoted structure has no
  back-edge and no accumulation cell; it is a case list.
  Verdict: L0/L1 storage, not construction. Claim dead.
- F-MUL2 (template): the construction trace shows the
  learner selecting among researcher-supplied
  multiplication schemas, or the assembly vocabulary names
  the target regularity. Verdict: downgrade to L2 at best.
- F-MUL3 (no transfer): the structure works only on the
  training surface encoding; a changed encoding (e.g.,
  swapped input slots, different literal layout) breaks
  it without relearning from scratch. Reuse fails.
- F-MUL4 (core smuggling): any core source change was
  needed (new op, new branch, widened basis). The ISA
  boundary is violated. Reject the implementation; the
  design question (is the basis sufficient?) is answered
  no, which is itself a finding, not a license to expand.
- F-MUL5 (oracle search): randomizing the trial order and
  the candidate-generation seed leaves capability
  unchanged. The search, not the learner, did the work.
  Reject per the oracle audit.

## 7. Experiment specification (for the prereg author)

Phases:

1. Prereg: freeze N (exemplar count), the held-out probe
   set, the lookup control, the graph-property checklist
   (back-edge, accumulation, termination), the ablation
   protocol, the transfer task, and the revision probe
   (zero/negatives). Freeze the assembly vocabulary and
   the search bound. Name the oracle audit.
2. Phase 1 (prerequisite): ADD available (given on Rung A,
   learner-constructed on Rung B). Record which.
3. Phase 2 (experience): teach N bare multiplication
   exemplars through the standard event loop. No additive
   scaffolding.
4. Phase 3 (discovery): multiplication queries; misses
   trigger trial-based composition under MISS_POLICY;
   candidates EXECUTEd and corroborated; promotion on
   full exemplar prediction.
5. Phase 4 (verification): held-out probes; white-box
   graph-property check; ablation; lookup-control
   comparison; oracle audit (seed randomization).
6. Phase 5 (reuse and revision): subroutine transfer task;
   zero/negative revision probe.
7. Phase 6 (adversary): independent red team attempts
   F-MUL1 through F-MUL5 breaks; at least one
   post-freeze family (exponentiation or division).

Controls:

- Lookup-table baseline (memorization ceiling).
- Scaffolded-experience control (diagnostic: does the
  execution path work when the insight is given?).
- A no-construction control: the frozen core without
  CAM-1/CAM-1-equivalent on the same exemplars (should
  fail: exact-key lookup cannot generalize).

Governance:

- Pure Zag throughout. No Python at any step.
- Prereg strictly precedes implementation.
- Sealed FW1-FW9 never accessed (FW3 is the sealed
  multiplication world; this experiment uses fresh
  exemplars, never the sealed set).
- Builders blind to held-out probes until Phase 4.

## 8. Open questions (banked, not decided here)

- Q1: the program-search policy. Bounded enumerative
  search over assembly moves is the scout's default, but
  its biases need stating and auditing. A smarter
  constructor (analogy from the ADD loop's shape) is the
  high-value variant and should be a named arm of the
  experiment, not the only path.
- Q2: Rung A vs Rung B sequencing. The scout recommends
  A then B, but if the approved ISA basis changes per
  Amendments A-C, the rung definitions move with it.
- Q3: the efficiency frontier. If the learner invents a
  sublinear multiplication, the graph-property checklist
  (section 1) needs generalizing: the check is "computes
  the product reusably," not "has exactly this loop
  shape." The prereg author must write the checklist to
  admit unforeseen efficient forms, or C0-B is tested
  against a checklist that presumes the naive shape.
- Q4: negative numbers. Whether the initial construction
  should handle them, or whether they are the designated
  revision probe, is a prereg decision with consequences
  for criterion (12).

## One-System Rule accounting (scout only)

- Cognition source lines added: 0.
- New hardcoded semantic cases: 0. New modes: 0.
- New bridges: 0. New task-specific handlers: 0.
- Learner-state structures created: 0 (none built).
- This document specifies a construction the learner
  would own entirely: the MUL graph, its cells, its
  frame discipline, and its reuse are all learner-state
  content under the frozen ISA. The researcher's
  contribution is bounded to the assembly vocabulary
  and the experiment design, both stated above and
  both auditable for template contamination.
