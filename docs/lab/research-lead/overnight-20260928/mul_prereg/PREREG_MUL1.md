# PREREG: MUL-from-ADD Learner Construction Experiment (MUL-1)

Date: 2026-09-30. Worker: MUL Prereg Author.
Status: PREREG-FROZEN (design only; no implementation in this commit).
Lane: Construct-and-apply frontier; Micah's ISA boundary ruling consequence (2).

## Step 0 Name-Check

The standing rules that apply: (1) PURE ZAG ONLY for any computational
research operation; this task is architecture design, pure markdown, no
code written, no computation performed, no Python used for any purpose.
(2) No em dashes in loop documentation: this document uses hyphens only,
verified by shell byte check for E2 80 94. (3) Commits stay local, owned
path only (docs/lab/research-lead/overnight-20260928/mul_prereg/),
explicit pathspecs, git status inspected before committing, the
contaminated paper untouched. (4) Preregistration strictly precedes
implementation: this prereg is frozen alone; no implementation may
reference it until reviewed. (5) Sealed FW1-FW9 files never accessed;
FW3 is the sealed multiplication world and this experiment uses fresh
exemplars only. This paragraph was written before any design work began.

## The standing question

> Why can the existing general architecture not learn this behavior?

The frozen core implements one retrieval operation: exact-key lookup
over stored triples. It has no persistent format for a learner-owned
procedure object and no application step on miss. The CAM-1 mechanism
(371d20743) adds trial-based PROPOSE/VERIFY/PROMOTE/APPLY, but its
P-DEP discovers only fixed templates (z = a, z = a + a, z = a + b).
Multiplication is not a fixed template over the exemplars; it is an
iterated computation. No existing mechanism constructs an iterative
procedure from bare exemplars. That is the gap this experiment tests.

## Mandate

Micah's ISA boundary ruling (0525377f3), consequence (2): do NOT add
MUL to the protected core because FW3 needs multiplication. Test
whether the learner can construct and persist MUL from the generic
computational basis. "That would be very interesting L3-ish evidence."

This prereg freezes the experiment that performs that test. It is
written from the MUL scout specification (8d30083b7), with the scout's
four open questions Q1-Q4 decided below (section 9).

## 1. The construction target

A learner-constructed MUL(x, y) is a PROC graph in the single
workspace, per the unified structures thesis: a root node tagged
PROC by the learner, CONTAINS edges to cell nodes, SEQ ordering
edges, each cell carrying a learner-assigned op_tag and refs to
operand cells. Invocation: caller ALLOCs a frame node, WRITEs
input bindings into its slots, then EXECUTE(root, frame) walks
the graph; output is read from the cell referenced by root ref[0].

The natural naive-loop form (the learner's actual topology may
differ; variance is evidence):

```
frame slots: [x] [y] [result] [i]
c1: MOVE(result <- 0)
c2: MOVE(i <- 0)
c3: BRANCHEQ(i, y, ->c6, ->c4)
c4: MOVE(result <- ADD(result, x))
c5: MOVE(i <- STEP(i)); SEQ back to c3
c6: terminal; root ref[0] -> result slot
```

## 2. The two rungs (frozen)

Rung A (run first): the approved ISA basis. Cell ops from
{MOVE, BRANCHEQ, ADD} plus literal cells (0 and 1). The counter
advances by ADD(i, 1) using a literal 1 cell; termination is
BRANCHEQ(i, y). No SUB, INC, or DEC. The learner must discover
the use of the literal 1 as the step. This rung runs on the
frozen, approved basis.

Rung B (run second, only after Rung A completes): {MOVE,
BRANCHEQ, INC, DEC}. ADD itself is learner-constructed first
(loop: while y != 0: x := INC(x); y := DEC(y)), then MUL is
constructed on top of the learner-built ADD. Two levels of
genuine construction. If Rung A fails for basis reasons rather
than construction reasons, Rung B diagnoses the difference;
the comparison is itself a finding.

Frozen constraint (both rungs): no new arithmetic op may be
added to pass. No MUL, SUB, or loop primitive enters the core.
If the learner cannot express iteration on the frozen basis,
that is a finding about the basis (F-MUL4 territory), not a
license to expand it.

## 3. Experience curriculum (frozen)

Phase 1 (prerequisite): ADD available. On Rung A, ADD is the
approved core primitive and the learner practices on addition
exemplars (10 pairs, sums 3..25). On Rung B, the learner
constructs ADD from INC/DEC first; the construction trace is
recorded. Which rung is running is recorded in the run log.

Phase 2 (experience): N = 12 bare multiplication exemplars,
taught as (x, y) -> product pairs through the standard event
loop. No additive scaffolding is shown. No decomposition.
The pairs:

(2,3)->6, (3,4)->12, (2,5)->10, (4,4)->16, (3,7)->21,
(5,6)->30, (4,9)->36, (7,7)->49, (6,4)->24, (8,3)->24,
(5,8)->40, (9,6)->54

Training products: {6, 10, 12, 16, 21, 24, 30, 36, 40, 49, 54}.

Phase 3 (discovery): multiplication queries arrive. Queries
miss (no MUL structure exists). The MISS_POLICY register
triggers trial-based composition: candidate programs are
assembled from the frozen vocabulary (section 4), EXECUTEd on
the exemplar inputs, scored by CORROBORATE, and the candidate
predicting all 12 exemplars is PROMOTEd as a PROC node.

Phase 4 (verification): held-out probes, administered only
after promotion. The 8 probes:

(6,7)->42, (3,9)->27, (8,8)->64, (7,9)->63,
(4,11)->44, (9,9)->81, (5,12)->60, (11,3)->33

Probe products {27, 33, 42, 44, 60, 63, 64, 81}: none appears
in the training product set in any form. Builders are blind
to these probes until Phase 4 (K2).

Phase 5 (reuse and revision): the transfer task, then the
revision probe (section 6).

Phase 6 (adversary): independent red team attempts F-MUL1
through F-MUL5; at least one post-freeze family
(exponentiation via repeated MUL, or integer division via
repeated subtraction) designed after the mechanism freeze.

Diagnostic control (not part of the L3 claim): the scaffolded
experience arm. The same N pairs taught alongside their
additive decompositions (e.g., (3,4)->12 with 3+3+3+3=12
shown). If the learner succeeds here but fails the bare
arm, the execution path works and the discovery failed;
the claim is not made. This arm is for debugging only.

## 4. Discovery mechanism (frozen)

On QUERY miss for a multiplication probe, the miss policy
proposes candidate programs assembled from this frozen,
domain-neutral vocabulary. These moves describe any loop,
not multiplication; they are the ceiling on researcher
contribution:

- INIT(slot, literal): WRITE a literal (0 or 1) into a frame slot.
- ACCUM(result_slot, src_slot): result = ADD(result, src).
- STEP(counter_slot): counter = ADD(counter, 1) on Rung A;
  INC(counter) on Rung B.
- TEST(c_slot, bound_slot, back_target, exit_target): BRANCHEQ
  between two slots, with a back-edge target and an exit target.
- SEQ(cell_a, cell_b): order two cells.

Search bound (frozen): skeletons up to K = 8 cells. Hole
fillers from {x, y, result, counter, lit0, lit1}. The trial
order is fixed and published in the implementation commit;
it is not part of this prereg, but the oracle audit
(section 7) constrains it.

Each candidate is EXECUTEd on the 12 exemplar inputs.
CORROBORATE (learner-level: EXECUTE, BRANCHEQ against
expected, WRITE outcome) scores it. The first candidate
predicting all 12 exemplars is PROMOTEd as a PROC node.
The full construction trace is recorded: every candidate
tried, every rejection, the promotion event.

What the researcher must NOT supply: a "repeated addition"
schema, a loop-with-accumulator template, or the knowledge
that multiplication is iterated addition. The vocabulary
above names no target regularity. Anything that does is
template contamination (F-MUL2).

## 5. The L3 bar, MUL-specific (frozen)

Criterion 0, applied:

- C0-A (runtime-defined semantics): the MUL procedure's
  cells live in learner-owned workspace state. The source
  contains no multiplication branch, no MUL op_tag in any
  dispatch table, no special case. The audit question
  "where are the semantics of multiplication implemented"
  must be answerable with "in this learner-authored PROC
  graph," pointing at workspace bytes, not source lines.
  Verified by source scan (G1-equivalent).

- C0-B (open structural form): the final graph's exact
  topology (cell count, wiring, rung, efficiency) emerges
  from construction. It is not selected from a finite
  researcher-enumerated family. Falsifier: the learner's
  MUL is always exactly the section-1 sketch down to cell
  count, across runs and seeds.

- C0-C (multiple unforeseen forms): after the mechanism
  freeze, sealed families requiring materially different
  constructed procedures. Phase 6 requires at least one
  adversary-designed post-freeze family (exponentiation
  via repeated MUL is the default; integer division via
  repeated subtraction is the alternate).

- C0-D (cognitive reuse): the constructed MUL improves
  performance beyond the training probes: the Phase 5
  transfer task and the held-out probes. Existence of the
  graph is not enough.

Template-contamination check (frozen procedure): enumerate
every structural commitment the researcher made (the
section-4 vocabulary, K = 8, the frame model, the trial
order). Then verify the learner's MUL contains at least
one structural decision the researcher did not make: the
accumulation order, the counter direction, the termination
form, or an efficiency improvement. If the final graph is
fully determined by researcher choices, the learner
selected, not constructed. F-MUL2.

The 12 criteria, load-bearing notes:

- (5) white-box trace: the construction trace must show
  the assembly moves producing the loop, the failed
  candidates tried and rejected (anti-hardcoding evidence:
  genuine alternatives rejected, per the compose-ops P2
  pattern), and the promotion event.
- (7) ablation: delete only the MUL PROC node and its
  CONTAINS/SEQ edges from the workspace. Multiplication
  queries must then fail (unknown or wrong) while addition
  queries and unrelated fact retrieval are intact. If
  multiplication performance persists, the capability was
  elsewhere (memorized pairs, core smuggling).
- (10) beats memorization: the lookup-table control
  (section 6) trained on identical exemplars must fail
  the held-out probes that MUL passes, by the frozen
  margin.
- (11) red team: independent adversary attempts the
  F-MUL1 through F-MUL5 breaks.
- (12) revisability: the Phase 5 revision probe (zero,
  then negatives). The learner must revise the structure;
  a construction that cannot survive first contact with
  zero is brittle, not intelligent.

## 6. Predictions and falsifiers (frozen)

Predictions (confirm for the claim):

- P-MUL1: after the 12 bare exemplars, the learner PROMOTEs
  a PROC structure that computes x*y correctly on at least
  7 of the 8 held-out probes.
- P-MUL2: white-box: the promoted graph satisfies the
  graph-property checklist (section 8).
- P-MUL3: ablation: removing only the MUL PROC node
  destroys multiplication performance (0/8 probes
  correct) while addition accuracy and unrelated
  retrieval are unchanged from pre-ablation.
- P-MUL4: reuse: the learner invokes the constructed MUL
  as a subroutine in the Phase 5 transfer task with no
  researcher intervention between construction and reuse.
  Transfer task (frozen): fresh context, stored facts
  "rect width 6" and "rect height 7" in a surface encoding
  different from training (named attributes, not pairs),
  query "rect area ?". Pass: correct answer 42, with the
  query-path trace showing EXECUTE of the MUL root.
- P-MUL5: the lookup-table control, trained on the
  identical 12 exemplars, scores at most 2/8 on the
  held-out probes. Margin: MUL leads the control by at
  least 5 probes.

Falsifiers (any one kills or downgrades):

- F-MUL1 (memorization): the promoted structure has no
  back-edge and no accumulation cell; it is a case list.
  Verdict: L0/L1 storage, not construction. Claim dead.
- F-MUL2 (template): the construction trace shows the
  learner selecting among researcher-supplied
  multiplication schemas, the vocabulary names the target
  regularity, or the template-contamination check finds
  zero learner-made structural decisions. Verdict:
  downgrade to L2 at best. Claim dead as L3.
- F-MUL3 (no transfer): the structure works only on the
  training surface encoding; the Phase 5 transfer task
  fails without relearning from scratch. Reuse fails.
  C0-D fails.
- F-MUL4 (core smuggling): any core source change was
  needed to pass (new op, new branch, widened basis).
  The ISA boundary is violated. Reject the
  implementation. The design question (is the basis
  sufficient?) is answered no, which is a finding about
  the basis, not a license to expand it.
- F-MUL5 (oracle search): the oracle audit (section 7)
  shows the search order or the search space did the
  work rather than the learner's corroboration. Reject
  per the audit.

## 7. Oracle audit (frozen)

The program-search policy's biases are the load-bearing
design risk (scout Q1). This audit is frozen:

1. The implementation commit publishes the fixed trial
   order of skeletons.
2. An independent auditor verifies BEFORE Phase 4 results
   are examined: (a) no correct skeleton occupies the
   first trial position; at least 5 incorrect skeletons
   precede the first correct one in the fixed order;
   (b) the search space contains skeletons that are wrong
   in interesting ways, not only the correct skeleton
   plus trivial variants; (c) the construction trace
   records at least 3 genuinely rejected candidates
   (candidates that passed at least one exemplar but not
   all 12).
3. Rerun sensitivity: Phase 3 is rerun with a shuffled
   trial order. The promoted structure must still satisfy
   P-MUL1 (corroboration selects, not position). If the
   shuffled run fails where the fixed run passed, the
   fixed order was load-bearing: F-MUL5 triggers.

F-MUL5 triggers if any of: a correct skeleton is tried
first in the fixed order; the space lacks genuine
alternatives; the trace shows no real rejections; or the
shuffled rerun diverges in correctness from the fixed run
in the direction implicating order.

## 8. Graph-property checklist (frozen; admits efficient forms)

Tier 1 (functional, both forms): the promoted structure
computes x*y correctly on at least 7/8 held-out probes,
plus the scaling probe (13,17)->221. The scaling probe
uses inputs larger than any training input; a case list
cannot pass it. Tier 1 is necessary for any form.

Tier 2 (structural, naive-loop form): the graph contains
(a) a back-edge (some cell's SEQ target is an ancestor),
(b) an accumulation cell (an output-path slot both read
and written across the back-edge), (c) a data-dependent
termination test (a BRANCHEQ whose taken/not-taken path
varies with an input slot), (d) input slots referenced
but never overwritten.

Tier 2' (structural, efficient form): if the learner's
graph fails Tier 2 but passes Tier 1 including the
scaling probe, it is examined as a candidate efficient
form. It passes Tier 2' if white-box inspection shows a
general computation (no case branches on input values,
no lookup structure) that a second auditor confirms is
not a disguised case list. An efficient form passing
Tier 2' is STRONGER evidence than the naive loop
(C0-B: unforeseen form).

P-MUL2 is satisfied by Tier 1 + (Tier 2 or Tier 2').

## 9. Scout open questions, decided

- Q1 (program-search policy): bounded enumerative search
  over the section-4 vocabulary is the primary arm, with
  the frozen bound K = 8 and the section-7 oracle audit.
  The analogy variant (the learner reuses the ADD loop's
  shape one level up: accumulate ADDs the way ADD
  accumulates INCs) is a NAMED SECOND ARM, run as a
  separate experimental condition, not the only path.
  If the primary arm succeeds and the analogy arm shows
  the shape-reuse, that is C0-D satisfied inside the
  experiment itself: the high-value variant. The analogy
  arm may not be run first and its results may not
  substitute for the primary arm.

- Q2 (rung sequencing): Rung A then Rung B, in that
  order. Rung B begins only after Rung A's Phase 4 is
  complete and judged. If the approved ISA basis changes
  under a future ruling, the rung definitions are
  re-frozen by amendment; this prereg does not move
  with the basis.

- Q3 (efficiency frontier): decided by the Tier 2'
  checklist in section 8. The checklist admits
  unforeseen efficient forms without presuming the
  naive shape.

- Q4 (negatives): the initial construction scope is
  non-negative integers. Zero and negatives are the
  DESIGNATED revision probe for criterion (12),
  administered in Phase 5 after transfer. Revision
  probes (frozen): (5,0)->0, (0,7)->0, then
  (3,-4)->-12, (-2,-5)->10. The learner is not required
  to handle these in Phase 4. In Phase 5 it must revise
  the constructed structure (not receive a new
  template). Pass: at least 3/4 revision probes correct
  after the learner's own revision, with the revision
  visible as workspace edits to the PROC graph.

## 10. Controls (frozen)

- C1 lookup-table baseline: the 12 training pairs stored
  as exact-key triples in the frozen core (its native
  capability). Expected: 12/12 on training pairs,
  at most 2/8 on held-out probes. This is the
  memorization ceiling P-MUL5 beats.
- C2 scaffolded-experience control: diagnostic only
  (section 3). Does not contribute to the L3 claim.
- C3 no-construction control: the frozen core without
  CAM-1 on the same 12 exemplars. Expected: fails all
  held-out probes (exact-key lookup cannot generalize).
  Confirms the capability comes from construction, not
  storage.

## 11. Governance and kill bars

- Pure Zag throughout: driver, learner, scorer, analysis.
  No Python at any step. Toolchain guard enforced per
  the ISA ruling's governance section; violations are
  PROCESS-FAIL with clean re-freeze required.
- K1 ordering: this prereg commit strictly precedes any
  implementation commit (verified by git merge-base
  --is-ancestor before results are examined).
- K2 honest recording: exemplars byte-recorded; builders
  blind to held-out probes until Phase 4; FW1-FW9 never
  accessed; the transfer task's surface encoding frozen
  here, not tuned after results.
- K3 purity: the implementation source is scanned for
  forbidden operations (FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE,
  FIND_THRESHOLD, MAKE_CONDITIONAL, MUL, or equivalents)
  before results are examined. Any hit voids the run.
- Determinism: construction and all probes run 3 times;
  byte-identical traces required for the promotion
  claim (the learner may be stochastic in trial order
  only insofar as the section-7 audit permits).
- This prereg is committed alone. Implementation follows
  only after review.

## 12. One-System Rule accounting (prereg)

- Cognition source lines added by this prereg: 0 (design only).
- New hardcoded semantic cases: 0. New modes: 0.
- New bridges: 0. New task-specific handlers: 0.
- Learner-state structures created: 0 (none built).
- Projected implementation bound: the experiment harness
  is learner-generic; the MUL graph, its cells, its frame
  discipline, and its reuse are all learner-state content
  under the frozen ISA. The researcher's frozen
  contribution is the section-4 vocabulary, the K = 8
  bound, and this experiment design, all auditable under
  the section-5 contamination check.

## Verdict labels

- MUL-PREREG-COMPLETE: this commit (design frozen alone).
- MUL1-BUILD-COMPLETE / MUL1-BUILD-FAIL: implementation.
- MUL1-SURVIVES / MUL1-KILLED: after the full 11-step
  pipeline (prereg, implementation, sealed evaluation,
  reproduction, baselines, alternative-explanation
  attack, OOD, ablation, transfer, red team, governance).
  Builders report BUILD-PASS/BUILD-FAIL only.
