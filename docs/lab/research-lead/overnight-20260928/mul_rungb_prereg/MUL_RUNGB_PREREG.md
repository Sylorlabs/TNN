# PREREG: MUL-from-ADD Rung B - Two-Level Learner Construction (MUL-1B)

Date: 2026-09-30. Worker: MUL Rung B Prereg Prep.
Status: PREREG-DRAFT (design only; no implementation in this commit).
Lane: Construct-and-apply frontier; Micah's ISA boundary ruling consequence (2).

## Step 0 Name-Check

The standing rules that apply: (1) PURE ZAG ONLY for any computational
research operation; this task is architecture design, pure markdown, no
code written, no computation performed, no Python used for any purpose.
(2) No em dashes in loop documentation: this document uses hyphens only.
(3) Commits stay local, owned path only
(docs/lab/research-lead/overnight-20260928/mul_rungb_prereg/),
explicit pathspecs, git status inspected before committing, the
contaminated paper untouched. (4) Preregistration strictly precedes
implementation: this prereg is frozen alone; no Rung B implementation
may reference it until reviewed (K1). (5) Sealed FW1-FW9 files never
accessed; FW3 is the sealed multiplication world and this experiment
uses fresh exemplars only. This paragraph was written before any design
work began.

## Parent prereg and Rung A outcome

Parent: `docs/lab/research-lead/overnight-20260928/mul_prereg/PREREG_MUL1.md`
@ `222899314`. Rung A build: `fbf14f73a` (MUL-BUILD-COMPLETE). Rung A
red team: `44f22979b` (MUL-REDTEAM-COMPLETE, 6/6 ATTACK-PASS).

Rung A result, adopted as the baseline: the learner promoted a 4-cell
PROC `[ACCUM_RX STEP_C TEST_CY GOTO(0)]` after 4,297 rejected candidates,
computing X*Y by repeated core-ADD. Six learner-made structural
decisions. 8/8 held-out probes plus scaling (13,17)->221. Ablation of
the PROC destroys multiplication while core ADD survives. Transfer
(rect area 6x7=42) passes. Lookup control 0/8. 3/3 byte-identical.

Rung A red-team boundary (adopted): negative Y would not terminate the
loop. Out of Rung A scope; Phase 5 revision probes deferred.

## The standing question for Rung B

> Why can the existing general architecture not learn this behavior?

Rung A showed the learner can construct a one-level procedure from a
basis that includes core ADD. Rung B asks whether the learner can
construct TWO levels: first ADD itself from {MOVE, BRANCHEQ, INC, DEC},
then MUL on top of the learner-built ADD, with the MUL genuinely
invoking the learner's ADD as a subroutine. No existing mechanism
performs learner-level procedure composition: a constructed procedure
calling another constructed procedure. That is the gap this rung tests.

## Mandate

Parent prereg section 2 (frozen): Rung B runs {MOVE, BRANCHEQ, INC, DEC}.
ADD itself is learner-constructed first (loop: while y != 0: x := INC(x);
y := DEC(y)), then MUL is constructed on top of the learner-built ADD.
Two levels of genuine construction. Per parent Q2 sequencing, Rung B
begins only after Rung A's Phase 4 is complete and judged. That
condition is satisfied: Rung A Phase 4 judged BUILD-PASS and red-teamed.

ISA basis check: {MOVE, BRANCHEQ, INC, DEC} maps to the approved ISA
classes (generic state/register ops, BRANCH/COMPARE-EQ, basic
arithmetic). The ISA ruling (0525377f3) consequence (3) accepts SUB as
ISA-level arithmetic with the same freeze; INC/DEC are the same class.
No basis change is requested or needed.

## 1. The two construction targets

Target 1: learner-constructed ADD(x, y), a PROC graph in the single
workspace, per the unified structures thesis. The naive form (the
learner's actual topology may differ; variance is evidence):

```
frame slots: [x] [y] [r]
c1: MOVE(r <- x)
c2: BRANCHEQ(y, 0, ->c5, ->c3)
c3: MOVE(r <- INC(r))
c4: MOVE(y <- DEC(y)); SEQ back to c2
c5: terminal; root ref[0] -> r slot
```

Note the structural difference from Rung A's MUL: the y input is
consumed (destroyed) by the loop. The learner must discover destructive
counter update, a pattern not exercised in Rung A (where x and y were
preserved). This is a genuine new discovery demand, not a re-run.

Target 2: learner-constructed MUL(x, y) that invokes the learner-built
ADD as a subroutine. The naive form:

```
frame slots: [x] [y] [r] [i]
c1: BRANCHEQ(i, y, ->exit, ->body)
c2 (body): CALL(learner_ADD_root, args=[r, x], out=r)
c3: MOVE(i <- INC(i)); SEQ back to c1
```

The MUL's correctness must DEPEND on the learner-built ADD. If the
learner instead re-discovers repeated INC (flat re-derivation), that is
one level, not two: F-MULB3 downgrade territory, not the claim.

## 2. Frozen vocabulary, both phases (researcher ceiling)

Phase 3a (ADD construction) vocabulary, domain-neutral, names no
target regularity:

- INIT(slot, literal): WRITE a literal (0 or 1) into a frame slot.
- COPY(dst, src): MOVE a slot value.
- STEP_INC(slot): slot <- INC(slot).
- STEP_DEC(slot): slot <- DEC(slot).
- TEST(slot, literal, back_target, exit_target): BRANCHEQ between a
  slot and a literal, with a back-edge target and an exit target.
- SEQ(cell_a, cell_b): order two cells.

No core ADD in the Phase 3a search or execution path. This is the
load-bearing purity requirement (K3): the Rung B implementation must
provably exclude the core ADD primitive from the ADD-construction
phase. The only addition available is the one the learner builds.

Phase 3b (MUL construction) vocabulary: the Phase 3a vocabulary plus
one generic composition move:

- CALL(proc_root, arg_slots, out_slot): EXECUTE a learner-owned PROC
  root with the given argument slots, writing the result to out_slot.

CALL is domain-neutral: it names no target procedure and no target
regularity. It is the generic procedure-invocation primitive the
unified structures thesis requires (procedure and causal rule as the
same executable graph type). At MUL-construction time the only PROC in
the workspace is the learner-built ADD, so CALL in practice invokes
ADD; the learner's discovery is the argument wiring, the loop shape,
and the decision to delegate at all.

Search bounds (frozen): ADD skeletons up to K_ADD = 8 cells; MUL
skeletons up to K_MUL = 8 cells. Hole fillers from {x, y, r, i,
lit0, lit1}. Same bound as Rung A for comparability. The trial order
is fixed and published in the implementation commit; the section-7
oracle audit constrains it.

What the researcher must NOT supply: a "destructive counter" schema,
an "ADD-then-MUL" curriculum hint beyond the phase order, the
knowledge that MUL should call ADD, or argument wirings. The phase
order (ADD first, then MUL) is the curriculum; the composition
discovery is the learner's. Anything that wires the CALL for the
learner is template contamination (F-MULB2).

## 3. Experience curriculum (frozen)

Phase 1 (prerequisite): the learner practices on the Rung B basis
(INIT/COPY/STEP_INC/STEP_DEC/TEST/SEQ moves) with no arithmetic goal.
Which rung is running is recorded in the run log.

Phase 2a (ADD experience): N_ADD = 10 bare addition exemplars, taught
as (x, y) -> sum pairs through the standard event loop. The pairs
(frozen):

(1,2)->3, (2,3)->5, (3,5)->8, (4,6)->10, (5,7)->12,
(6,8)->14, (7,9)->16, (8,10)->18, (9,12)->21, (11,14)->25

Training sums: {3, 5, 8, 10, 12, 14, 16, 18, 21, 25}.

Phase 3a (ADD discovery): addition queries arrive and miss. The
MISS_POLICY triggers trial-based composition over the Phase 3a
vocabulary. Candidates are EXECUTEd on the 10 exemplar inputs, scored
by CORROBORATE; the first candidate predicting all 10 is PROMOTEd as
the ADD PROC node. Full construction trace recorded.

Phase 4a (ADD verification): held-out addition probes, administered
only after ADD promotion. The 8 probes (frozen):

(4,5)->9, (6,7)->13, (8,9)->17, (9,10)->19,
(10,12)->22, (11,13)->24, (13,15)->28, (15,17)->32

Probe sums {9, 13, 17, 19, 22, 24, 28, 32}: none appears in the
training sum set. Plus the ADD scaling probe (47,53)->100 (inputs
larger than any training input).

Phase 2b (MUL experience): the identical 12 bare multiplication
exemplars as Rung A (frozen, byte-identical list from the parent
prereg section 3). No additive scaffolding shown.

Phase 3b (MUL discovery): multiplication queries miss. Trial-based
composition over the Phase 3b vocabulary (including CALL). The first
candidate predicting all 12 exemplars is PROMOTEd as the MUL PROC node.
Full construction trace recorded.

Phase 4b (MUL verification): the identical 8 held-out probes plus the
scaling probe (13,17)->221 from Rung A (frozen, byte-identical).
Comparability with Rung A is the point: same probes, different
dependency structure.

Phase 5 (reuse and revision): the transfer task, then the revision
probes (section 6).

Phase 6 (adversary): independent red team attempts F-MULB1 through
F-MULB5; at least one post-freeze family (exponentiation via repeated
MUL would exercise THREE levels: EXP calls MUL calls ADD; integer
division via repeated subtraction is the alternate) designed after the
mechanism freeze.

Diagnostic control (not part of the claim): the single-level arm. The
learner is given the Rung B basis {MOVE, BRANCHEQ, INC, DEC} plus CALL
but WITHOUT the ADD-first phase; it must construct MUL in one search.
If it succeeds as easily as the two-level arm, the ADD-first
curriculum is scaffolding, not load-bearing. If the two-level arm
succeeds where the single-level fails, the decomposition does work.
This arm is for debugging the curriculum claim only.

## 4. The L3 bar, Rung B-specific (frozen)

Criterion 0, applied to both levels:

- C0-A (runtime-defined semantics): both the ADD and MUL procedures'
  cells live in learner-owned workspace state. The source contains no
  addition branch and no multiplication branch, no ADD or MUL op_tag in
  any dispatch table, no special case. The audit question "where are
  the semantics of addition and multiplication implemented" must be
  answerable with "in these two learner-authored PROC graphs," pointing
  at workspace bytes, not source lines. Verified by source scan.
  Additionally: the MUL graph must contain a CALL cell referencing the
  learner-ADD root node address (white-box, section 8).

- C0-B (open structural form): each graph's exact topology emerges from
  construction. Neither is selected from a finite researcher-enumerated
  family. Falsifier: the learner's ADD is always the section-1 sketch
  down to cell count across runs, or the MUL's CALL wiring is always
  identical with no variance in loop shape.

- C0-C (multiple unforeseen forms): after the mechanism freeze, sealed
  families requiring materially different constructed procedures.
  Phase 6 requires at least one adversary-designed post-freeze family.

- C0-D (cognitive reuse): the constructed MUL improves performance
  beyond training: the Phase 5 transfer task and held-out probes. The
  constructed ADD is reused by the MUL: reuse inside the experiment
  itself, the high-value variant of the parent Q1 analogy arm. The
  analogy arm is no longer a separate condition; on Rung B it IS the
  rung.

Template-contamination check (frozen procedure): enumerate every
structural commitment the researcher made (the section-2 vocabularies,
K_ADD/K_MUL = 8, the frame model, the phase order, the trial order).
Then verify each promoted graph contains at least one structural
decision the researcher did not make: for ADD, the counter direction,
the initialization form, the termination literal; for MUL, the CALL
argument wiring, the loop shape around the CALL, whether INITs are
kept or dropped (cf. Rung A's zero-init discovery). If either final
graph is fully determined by researcher choices, the learner selected,
not constructed. F-MULB2.

The 12 criteria, Rung B load-bearing notes:

- (5) white-box trace: both construction traces must show the assembly
  moves producing the loops, failed candidates tried and rejected
  (genuine alternatives rejected at BOTH levels), and both promotion
  events. The MUL trace must show the CALL cell's target resolving to
  the learner-ADD root.
- (7) ablation, two-level (section 8): ablate only the learner-ADD PROC
  -> direct ADD queries fail AND MUL queries fail (dependency proven).
  Ablate only the learner-MUL PROC -> ADD queries intact, MUL fails
  (level separation proven). If MUL survives ADD ablation, the MUL was
  not using the learner's ADD: F-MULB1.
- (10) beats memorization: the lookup-table control (section 9),
  trained on identical exemplars, must fail the held-out probes at
  both levels by the frozen margin.
- (11) red team: independent adversary attempts F-MULB1 through
  F-MULB5.
- (12) revisability: the Phase 5 revision probes (zero, then
  negatives). With DEC available, sign-handling revision is genuinely
  in reach on Rung B; this is part of the rung's diagnostic value
  over Rung A. The learner must revise its own structures.

## 5. Predictions and falsifiers (frozen)

Predictions (confirm for the claim):

- P-MULB1: after the 10 bare addition exemplars, the learner PROMOTEs
  an ADD PROC that computes x+y correctly on at least 7 of the 8
  held-out addition probes plus the ADD scaling probe (47,53)->100.
- P-MULB2: the promoted ADD graph satisfies the graph-property
  checklist (section 8): back-edge, destructive counter update,
  data-dependent termination on the y slot, no case branches.
- P-MULB3: after the 12 bare multiplication exemplars, the learner
  PROMOTEs a MUL PROC containing a CALL cell targeting the
  learner-ADD root, computing x*y correctly on at least 7 of the 8
  held-out probes plus (13,17)->221.
- P-MULB4: two-level ablation (section 8): (a) ablate learner-ADD
  only -> ADD probes 0/8 and MUL probes 0/8; (b) restore, ablate
  learner-MUL only -> ADD probes at pre-ablation accuracy, MUL
  probes 0/8. Unrelated fact retrieval unchanged throughout.
- P-MULB5: reuse: the learner invokes the constructed MUL as a
  subroutine in the Phase 5 transfer task with no researcher
  intervention between construction and reuse. Transfer task
  (frozen, identical surface to Rung A for comparability): fresh
  context, stored facts "rect width 6" and "rect height 7" in named
  attributes, query "rect area ?". Pass: correct answer 42, with the
  query-path trace showing EXECUTE of the MUL root AND nested
  EXECUTE of the learner-ADD root inside the MUL's loop.
- P-MULB6: the lookup-table control scores at most 2/8 on held-out
  probes at each level. Margin: each constructed level leads its
  control by at least 5 probes.

Falsifiers (any one kills or downgrades):

- F-MULB1 (core-ADD smuggling): the MUL's computation does not depend
  on the learner-built ADD. Detected by (a) source scan finding core
  ADD in the Phase 3a/3b search or execution path (K3), or (b) the
  P-MULB4(a) ablation: MUL survives learner-ADD ablation. Verdict:
  the two-level claim is dead; the ISA boundary is violated. Reject
  the implementation.
- F-MULB2 (template): the construction traces show the learner
  selecting among researcher-supplied addition/multiplication schemas,
  the vocabulary names the target regularity, the CALL wiring is
  researcher-determined, or the template-contamination check finds
  zero learner-made structural decisions at either level. Verdict:
  downgrade to L2 at best. Claim dead as L3.
- F-MULB3 (flat re-derivation): the MUL contains no CALL cell, or its
  CALL targets nothing, or it re-discovers repeated INC without
  delegating to the ADD PROC. Verdict: one level demonstrated, not
  two. The composition claim is dead; the construction result stands
  as a Rung A replication on a weaker basis (still a finding about
  the basis, not the claim).
- F-MULB4 (memorization): either promoted structure has no back-edge
  and no accumulation/counter cell; it is a case list. The ADD
  scaling probe (47,53)->100 and MUL scaling probe (13,17)->221 rule
  out case lists at each level. Verdict: L0/L1 storage. Claim dead.
- F-MULB5 (oracle search): the oracle audit (section 7) shows the
  search order or space did the work at either level rather than the
  learner's corroboration. Reject per the audit.

## 6. Revision probes: the negative-Y boundary (frozen, in scope)

Rung A's documented boundary (negative Y does not terminate) is IN
SCOPE for Rung B revision, not construction. Rationale: with DEC
available, sign-handling is genuinely in reach; whether the learner
revises toward it is diagnostic of the construction's revisability
(criterion 12), which Rung A could not test.

Initial construction scope (Phase 4a/4b): non-negative integers, same
as Rung A. The learner is not required to handle zero or negatives
at promotion.

Phase 5 revision probes (frozen, identical to parent Q4): (5,0)->0,
(0,7)->0, then (3,-4)->-12, (-2,-5)->10. Administered after transfer.
The learner must revise its own structures (workspace edits to the
PROC graphs visible in the trace); it must not receive a new template.
Pass: at least 3/4 revision probes correct after the learner's own
revision.

Note on the ADD loop under negatives: the naive ADD form (while y !=
0: r := INC(r); y := DEC(y)) terminates for y >= 0 and diverges for
y < 0. A learner that revises toward sign handling must restructure
the termination or the stepping. The revision trace is itself
evidence for criterion (12); a learner that cannot revise is brittle
in exactly the way Rung A's boundary suggested.

## 7. Oracle audit (frozen, both phases)

Applied independently to Phase 3a and Phase 3b:

1. The implementation commit publishes the fixed trial order of
   skeletons for each phase.
2. An independent auditor verifies BEFORE Phase 4 results are
   examined: (a) no correct skeleton occupies the first trial
   position in either phase; at least 5 incorrect skeletons precede
   the first correct one in each fixed order; (b) each search space
   contains skeletons that are wrong in interesting ways, not only
   the correct skeleton plus trivial variants; (c) each construction
   trace records at least 3 genuinely rejected candidates
   (candidates that passed at least one exemplar but not all).
3. Rerun sensitivity: each phase is rerun with a shuffled trial
   order. The promoted structures must still satisfy P-MULB1 and
   P-MULB3 respectively (corroboration selects, not position). If a
   shuffled run fails where the fixed run passed, the fixed order
   was load-bearing: F-MULB5 triggers for that phase.

F-MULB5 triggers if any of: a correct skeleton is tried first in a
fixed order; a space lacks genuine alternatives; a trace shows no
real rejections; or a shuffled rerun diverges in correctness from
the fixed run in the direction implicating order.

## 8. Graph-property checklist and two-level ablation (frozen)

Tier 1 (functional, each level): the promoted structure computes
correctly on at least 7/8 held-out probes plus its scaling probe.
Necessary for any form, at each level.

Tier 2-ADD (structural): the ADD graph contains (a) a back-edge (some
cell's SEQ target is an ancestor), (b) a destructive counter update
(the y slot is both read and written across the back-edge via DEC),
(c) a data-dependent termination test (a BRANCHEQ on the y slot whose
taken/not-taken path varies with input), (d) no case branches on
input values, no lookup structure.

Tier 2-MUL (structural): the MUL graph contains (a) a back-edge,
(b) a CALL cell whose target resolves to the learner-ADD root node
address (verified by workspace inspection, not by the builder's
description), (c) a data-dependent termination test on the loop
counter, (d) the accumulation path goes through the CALL cell's
output (the result slot is written by CALL, not by a direct INC/ADD).

Two-level ablation procedure (frozen): (a) invalidate only the
learner-ADD PROC root and its cells; run ADD probes and MUL probes
via the workspace executor; record. (b) Restore from the promotion
snapshot; invalidate only the learner-MUL PROC root and its cells;
run both probe sets; record. (c) Verify unrelated fact nodes intact
throughout. P-MULB4 bars: (a) must yield 0/8 on both sets (dependency);
(b) must yield pre-ablation ADD accuracy and 0/8 MUL (separation).

## 9. Controls (frozen)

- C1 Rung A comparison: the Rung A MUL (core-ADD based) and the Rung
  B MUL (learner-ADD based) run the identical 8 held-out probes plus
  scaling. Expected: equal probe scores; the difference is
  architectural (dependency structure), not behavioral. If Rung B
  scores strictly worse, the weaker basis costs capability: a finding
  about the basis.
- C2 lookup-table baselines: the 10 addition pairs and 12
  multiplication pairs stored as exact-key triples in the frozen core
  (its native capability). Expected: full marks on training pairs, at
  most 2/8 on each held-out probe set. These are the memorization
  ceilings P-MULB6 beats.
- C3 single-level diagnostic arm: the Rung B basis plus CALL, without
  the ADD-first phase (section 3). Diagnostic only; does not
  contribute to the claim. If the single-level arm succeeds as easily
  as the two-level arm, the curriculum is scaffolding. If only the
  two-level arm succeeds, the decomposition is load-bearing.
- C4 no-construction control: the frozen core without CAM-1 on the
  same exemplars. Expected: fails all held-out probes at both levels.
  Confirms the capabilities come from construction, not storage.

## 10. Governance and kill bars

- Pure Zag throughout: driver, learner, scorer, analysis. No Python
  at any step. Toolchain guard enforced per the ISA ruling's
  governance section; violations are PROCESS-FAIL with clean
  re-freeze required.
- K1 ordering: THIS prereg commit strictly precedes any Rung B
  implementation commit (verified by git merge-base --is-ancestor
  before results are examined). No Rung B implementation may begin
  until this prereg is reviewed.
- K2 honest recording: exemplars byte-recorded; builders blind to
  held-out probes until Phase 4a/4b; FW1-FW9 never accessed; the
  transfer task's surface encoding frozen here, not tuned after
  results.
- K3 purity: the implementation source is scanned for forbidden
  operations (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION,
  BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL, MUL, or equivalents) AND for core-ADD in the
  Phase 3a search/execution path, before results are examined. Any
  hit voids the run. The Rung B builder must demonstrate the
  exclusion structurally (e.g., the Rung B binary links no core-ADD
  symbol in the construction path), not by assertion.
- K4 EXECUTE-boundary inheritance: Rung B's nested invocation relies
  on the EXECUTE arrangement whose exact placement (amendments A-C)
  is pending Micah's ruling. This prereg is frozen against the
  current implementation arrangement. If the ruling changes the
  boundary, this prereg is re-frozen by amendment; it does not move
  with the boundary.
- Determinism: both constructions and all probes run 3 times;
  byte-identical traces required for the promotion claims (the
  learner may be stochastic in trial order only insofar as the
  section-7 audit permits).
- This prereg is committed alone. Implementation follows only after
  review.

## 11. One-System Rule accounting (prereg)

- Cognition source lines added by this prereg: 0 (design only).
- New hardcoded semantic cases: 0. New modes: 0.
- New bridges: 0. New task-specific handlers: 0.
- Learner-state structures created: 0 (none built).
- Projected implementation bound: the experiment harness is
  learner-generic; the ADD graph, the MUL graph, their cells, the
  CALL wiring, and their reuse are all learner-state content under
  the frozen ISA. The researcher's frozen contribution is the
  section-2 vocabularies, the K_ADD/K_MUL = 8 bounds, the phase
  order, and this experiment design, all auditable under the
  section-4 contamination check. The CALL move is a generic
  composition primitive, not a multiplication provision.

## Verdict labels

- MUL-RUNGB-PREREG-DRAFTED: this commit (design frozen alone).
- MUL1B-BUILD-COMPLETE / MUL1B-BUILD-FAIL: implementation.
- MUL1B-SURVIVES / MUL1B-KILLED: after the full 11-step pipeline
  (prereg, implementation, sealed evaluation, reproduction,
  baselines, alternative-explanation attack, OOD, ablation,
  transfer, red team, governance). Builders report BUILD-PASS /
  BUILD-FAIL only.
