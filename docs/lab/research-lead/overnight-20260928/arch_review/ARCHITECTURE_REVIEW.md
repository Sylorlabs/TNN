# ARCHITECTURE REVIEW: Program Discovery for the Frozen GENEXEC2 VM

Date: 2026-09-30.
Status: FINAL. Preregistered criteria: e1dc515a7 (committed before this document).
Wave: documents only. No implementation is authorized.

## 0. The trigger question

Is the current representation itself wrong?

Assessment: no. The representation (linear (op, arg) programs over
the frozen GENEXEC2 VM, with CALL for fragments) is expressively
adequate for the 7 task battery. Evidence: P3 assembled a correct
conditional for T1 (|x|) from separately synthesized parts; T4 and T5
have known CALL based solutions ([IN0, CALL ABS, PUSH 2, SUB, CALL ABS]
and the ADD composition). Every observed failure across both failed
generations was a failure to FIND a program, never a failure to
EXPRESS one. The defect localizes to discovery machinery.

What both failed generations shared: a population of candidate
programs grown by appending ops, retained by ranking on a scalar
output score (GENEXEC2: exact count then MAE; P1 redesign: behavioral
dedup then score ordered CAP eviction). Both pruned the same
deceptive prefixes. The shared defect is score ranked retention of
partial programs, not the VM and not linear programs as such.

Falsifier for this assessment: if every hypothesis below fails tasks
T0 through T5 on the frozen VM within the frozen cost budget, the
assessment is overturned and a VM level review replaces further
discovery work.

None of the hypotheses below is a beam variant. Per prereg bar R5, a
beam variant means: a population of candidate programs grown by
appending ops, retained by ranking on a scalar output score, with a
fixed width or CAP. Larger beams, reweighted scores, and task specific
prefix protection were considered and are explicitly excluded.

## 1. Hypothesis A: residual driven construction (first principles)

Core mechanism: maintain a single growing program P and an explicit
residual object R. For each train episode (x, t), the residual is
r = t minus top of stack after running P on x. Initialize P as empty
(output defined as 0), so R starts as the target itself. At each step,
consider appending each op in deterministic order and choose the op
that best simplifies R under a generic complexity measure. The
primary simplification signal is R becoming constant across episodes
(a constant residual dictates PUSH c followed by the combining op);
the secondary signal is reduction in the number of distinct residual
values or in residual range. Append the chosen op, recompute R,
repeat. Terminate with success when R is identically zero; terminate
with failure (and report R for diagnosis) when no op simplifies R.

How it differs from beam search: there is no population, no scalar
ranking, no width. A single trajectory is driven by an explicit
residual object. The question at each step is "what transformation
remains unexplained" rather than "which partial program scores
highest." The deceptive prefix is never scored as a candidate: after
[IN0, PUSH 2, MUL] the residual on 2x+1 is the constant 1, which
directly dictates PUSH 1, ADD. Score based retention cannot prune a
stepping stone that is never subjected to retention.

Predictions on the battery:
- 2x+1: SOLVE. Predicted program [IN0, PUSH 2, MUL, PUSH 1, ADD],
  found via the constant residual signal.
- mod3: SOLVE. [IN0, PUSH 3, MOD] drives R to zero.
- parity: SOLVE. Residual defined over the joint input (a, b);
  [IN0, IN1, ADD, PUSH 2, MOD] drives R to zero.
- abs: FAIL standalone. No arithmetic op sequence makes R constant
  or zero; the kink keeps R structured. A reports failure with a
  sign partitioned residual, which diagnoses where a split would go,
  but A alone does not split.
- nested abs: FAIL standalone. Fragment composition: FAIL standalone.
- adversary function: SOLVE if and only if the sealed function's
  residual decomposes through constant seeking steps; FAIL
  otherwise. This conditional prediction is staked before T6 is
  designed.

Falsification:
- F1: A fails 2x+1 or mod3. Both have clean constant seeking
  residual decompositions; failure means the residual complexity
  driver is inadequate. A is falsified.
- F2: the construction trace shows multiple candidate programs
  ranked by a residual score. That is a beam search with a renamed
  score; A collapses into the banned class and is rejected as
  genuinely different.
- F3: A solves abs straight line. Either the op alphabet secretly
  expresses abs without comparison (a VM or task design flaw) or
  conditional machinery was smuggled in. The standalone prediction
  is falsified and the anomaly is investigated before any claim.

## 2. Hypothesis B: semantic fragment induction (first principles)

Core mechanism: three parts. (i) A base constructor that finds
straight line programs (any adequate discoverer; B's novelty is not
the base). (ii) An inducer: from construction traces, extract
recurring subcomputations as named fragments. A fragment carries a
semantic signature: its behavior on a fixed probe input set. Fragments
are induced from sub task structure (for example the branch bodies of
an assembled conditional, or a residual pattern solved the same way
across many episodes), never by promoting whole task solutions
verbatim. The library is indexed by behavior, with behavioral dedup of
the index. (iii) A composer: on a new task, match substructure of the
task (its residual profile or regional structure) against fragment
semantic signatures by behavioral similarity, retrieve matches, and
compose them with CALL. Fragment proposal is by semantic match, not by
enumerating CALL ops in a scored population.

How it differs from beam search and from GENEXEC2 P2: GENEXEC2
promotes whole task solutions and beam searches over ops plus CALL.
B induces sub task fragments from traces and retrieves by behavioral
match to task substructure. There is no population ranked by output
score anywhere in the induction or composition loop.

Predictions on the battery:
- 2x+1: SOLVE via the base constructor. No fragment needed.
- mod3: SOLVE, and a periodic fold fragment is induced.
- parity: SOLVE, and a parity fragment is induced.
- abs: SOLVE. Conditional assembly induces the ABS fragment with
  the semantic signature "folds negatives to positives" on the
  probe set.
- nested abs: SOLVE via composition. The task's kink at zero
  subpattern semantically matches the ABS signature, so ABS is
  retrieved twice: predicted program contains at least 2 CALLs to
  ABS, and the trace shows retrieval events before each CALL.
- fragment composition: SOLVE via composition with at least 2
  CALLs to ABS and retrieval events in the trace.
- adversary function: SOLVE if and only if T6 decomposes into
  subpatterns matching induced fragment signatures; FAIL if T6
  requires a genuinely novel primitive. This is the sharpest C0-C
  prediction in the review.

Falsification:
- F1: nested abs or fragment composition is solved but the trace
  shows no semantic retrieval events, or retrieval precision is at
  chance. The composition claim is falsified.
- F2: induced fragments are byte identical whole task solutions
  reused verbatim, with no substructure extraction step in the
  trace. B collapses to GENEXEC2 P2 and is falsified as genuinely
  different.
- F3: the library accumulates near duplicate fragments with no
  behavioral dedup of the index. The semantic indexing claim is
  falsified; the mechanism is memoization, not induction.

## 3. Hypothesis C: counterexample driven structural growth (first principles)

Core mechanism: state is a program P (initially minimal, e.g.
[PUSH 0]) plus a counterexample set. Loop: evaluate P on all train
episodes; if all pass, done. Otherwise take a failing episode e and
attempt repair: search single op appends in deterministic op order
for one that fixes e while breaking no currently passing episode
(verified by re evaluation). If a repair is found, append it; the
growth step is justified by e. If no repair exists, split: choose a
probe from the frozen generic probe family (the same family as
GENEXEC2 P3: [IN0/IN1, PUSH k, LT/GT/EQ], k in -4..4) that separates
failing from passing episodes, then recursively grow each branch on
its own episode subset. Splits nest. The program is a decision tree
of straight line segments grown monotonically, each step justified
by a specific counterexample.

How it differs from beam search: no population, no scalar ranking.
The driver is the counterexample set, and the operators are repair
and split, not generate and rank. How it differs from GENEXEC2 P3:
P3 is one shot post hoc single probe assembly after P1 fails; C
interleaves repair and splitting throughout construction, and splits
nest, producing multi kink conditionals P3 cannot assemble.

Predictions on the battery:
- 2x+1: SOLVE via a short repair chain, each append justified by a
  failing episode.
- mod3: SOLVE. Periodic counterexamples force the MOD repair.
- parity: SOLVE via repair.
- abs: SOLVE via split. Linear repair cannot fix x<0 and x>0
  failures simultaneously (any append fixing one side breaks
  passing episodes on the other, failing the repair check), so the
  mechanism splits on [IN0, PUSH 0, LT] and repairs each branch
  separately. Predicted program has 2 regions and zero CALLs.
- nested abs: SOLVE via nested splits. Three regions (x<-2,
  -2..2, x>2) demand two nested splits. KEY DISCRIMINATOR against
  B: C's program contains conditionals and ZERO CALLs to ABS, while
  B's contains at least 2 CALLs. Same predicted outcome,
  different predicted mechanism; the traces decide.
- fragment composition: SOLVE via splits (regions x<0, 0..2, x>2).
- adversary function: SOLVE if and only if T6 is piecewise with
  repairable regions; the split count in the trace should track
  the true region count.

Falsification:
- F1: C fails 2x+1. The repair operator is inadequate; C is
  falsified.
- F2: C's nested abs trace shows fragment CALLs instead of nested
  splits (or B's trace shows splits instead of CALLs). The
  mechanism claim is falsified. This is why traces are mandatory,
  not just outcomes.
- F3: split count grows with episode count rather than with true
  regions (split count far exceeds true regions on T6). The
  "split only where counterexamples demand" discipline is
  falsified; the mechanism is overfitting, not structural growth.
- F4: the repair step maintains a ranked population of candidate
  repairs. That is beam search inside the repair operator; C is
  rejected as genuinely different.

## 4. Hypothesis D: diversity search baseline, MAP-Elites (conventional control)

Core mechanism: the standard quality diversity baseline from the
evolutionary computation literature. An archive is indexed by a
behavioral descriptor (discretized output vector on the train
episodes). Candidates are generated by mutating archive members
(append, replace, or delete a single op, in deterministic order). A
candidate is retained if its niche is empty or its exact match score
beats the niche elite. Fixed evaluation budget. Retention is per
niche; there is no global top K ranking.

How it differs from beam search: retention is per behavioral niche
rather than global score rank, so behaviorally diverse stepping
stones survive regardless of score. It is still a generate and test
population method, which is why it serves as the conventional
control rather than a first principles TNN hypothesis. Its job is to
show what diversity alone buys on the straight line tasks, isolating
the value added by A, B, and C.

Predictions on the battery:
- 2x+1: SOLVE. The deceptive prefix [IN0, PUSH 2, MUL, PUSH 1]
  occupies its own niche and survives independent of its poor
  score; mutation then appends ADD. This directly tests the P1
  redesign postmortem claim.
- mod3: SOLVE. parity: SOLVE.
- abs: FAIL. The control has no conditional machinery and the P1
  op alphabet has no comparison; this matches the straight line
  limit and isolates the discovery question.
- nested abs: FAIL. fragment composition: FAIL. No fragments, no
  splits.
- adversary function: SOLVE if and only if T6 is straight line
  synthesizable within budget.

Control validity conditions (falsifiers of the control, not of a theory):
- F1: D fails 2x+1. The control is misconfigured (descriptor too
  coarse or too fine, mutation inadequate, budget too small). It
  must be fixed before serving as a baseline.
- F2: D solves nested abs or fragment composition. Either the tasks
  are straight line solvable after all (a task design flaw, to be
  checked by inspecting the found program) or conditional or
  fragment machinery leaked into the control. Invalidate and fix.
- D failing abs, nested abs, and fragment composition is predicted
  control behavior, not a falsifier.

## 5. Discrimination matrix (predicted outcomes)

Task              | A residual | B fragments | C cex growth | D MAP-Elites
2x+1              | SOLVE      | SOLVE       | SOLVE        | SOLVE
abs               | FAIL       | SOLVE       | SOLVE        | FAIL
mod3              | SOLVE      | SOLVE       | SOLVE        | SOLVE
parity            | SOLVE      | SOLVE       | SOLVE        | SOLVE
nested abs        | FAIL       | SOLVE       | SOLVE        | FAIL
fragment comp.    | FAIL       | SOLVE       | SOLVE        | FAIL
adversary (sealed)| conditional| conditional | conditional  | conditional

Mechanism level discrimination where outcomes coincide:
- nested abs and fragment composition: B predicts CALLs plus
  retrieval events; C predicts nested splits and zero CALLs.
- abs: A predicts a diagnosed failure with a sign partitioned
  residual; D predicts plain failure; B and C predict success by
  different mechanisms (induced fragment vs. split).
- adversary: each hypothesis staked a conditional prediction
  before T6 was designed; the adversary's choice decides.

## 6. Minimal discriminating battery design

Frozen substrate: the GENEXEC2 interpreter exactly as committed in
8d5f58b89 (op set, PUSH range -9..9, DIV and MOD edge semantics,
CALL/RET, top of stack result). No VM edits during hypothesis
evaluation. Each hypothesis is new construction machinery over this
frozen VM.

Tasks (frozen episodes, fixed order, persistent hypothesis state
carried across tasks and recorded):
1. 2x+1: x in 0..8. Adequacy gate and historical failure point.
   Discriminates working from broken base discovery; falsifies any
   hypothesis outright on failure (except D, where failure
   invalidates the control instead).
2. abs: x in -8..8 train, x in -12..12 held out. Conditional
   structure with one kink. Discriminates {B, C} from {A, D};
   separates fragment induction from splitting at the mechanism
   level.
3. mod3: x in 0..16. Periodic structure. Tests non monotonic
   discovery and gives B a periodic fragment induction target.
4. parity: a,b in 0..4, target (a+b) even. Relational two input
   structure. Guards against single input overfitting; every
   hypothesis must handle joint inputs.
5. nested abs: x in -6..6, target ||x|-2|. Repeated application
   structure. THE key discriminator: B must show CALLs and
   retrieval events, C must show nested splits and zero CALLs,
   A and D must fail.
6. fragment composition: x in -4..8, target |x|+|x-2|.
   Hierarchical composition. Second B vs C mechanism data point
   and a reuse test.
7. adversary function: sealed, designed by the independent
   adversary after mechanism freeze, requiring a materially
   different structure from tasks 1..6. The C0-C test. Each
   hypothesis's conditional prediction above is staked before the
   design.

Minimality: remove task 1 and the adequacy gate is lost; remove
task 2 and no task separates conditional handling; remove task 3
and periodic structure goes untested; remove task 4 and multi
input handling is unchecked; remove task 5 and B vs C are
mechanistically indistinguishable; remove task 6 and reuse has a
single data point; remove task 7 and C0-C is untested. Every task
separates at least one hypothesis pair.

Protocol:
- Determinism: 3 byte identical runs per (hypothesis, task).
- Reporting per (hypothesis, task): exact match count, found
  structure dump, construction trace with mechanism mandatory
  events (A: residual values per step; B: induction and retrieval
  events with semantic signatures; C: repair and split events with
  justifying counterexamples; D: niche insertions), candidate
  evaluation count and wall clock, persistent state diff across
  the task sequence.
- Confirmation rule (prereg section 3): a prediction is confirmed
  only if the outcome matches AND the trace shows the predicted
  mechanism. Outcome without mechanism does not confirm.
- Cost budget: 1,000,000 program evaluations per task or 300
  seconds wall clock, whichever is reached first. Frozen at the
  battery prereg, before any hypothesis implementation.
- The battery design in this document is a design. Its freeze,
  with concrete budgets and the sealed T6, happens in a subsequent
  battery prereg before any hypothesis is implemented.

## 7. What this review does not do

No hypothesis is implemented here. No beam variant is repaired or
reweighted. No task specific prefix protection is introduced. The
next waves are: battery prereg (freeze budgets and protocol),
adversary T6 design (sealed), then hypothesis implementation
selection. Each of those waves carries its own prereg.
