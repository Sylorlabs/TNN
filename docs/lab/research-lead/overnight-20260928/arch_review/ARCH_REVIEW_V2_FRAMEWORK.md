# Architecture Review V2: Prepared Framework (Not Conducted)

Date: 2026-09-30.
Status: PREPARED. This document specifies the review procedure, the trigger
evaluation, the decision criteria, and candidate alternative representations.
It conducts no review and issues no verdict. The review opens only when a
trigger condition fires, evaluated after C2 results and the battery redesign
both land.

## 1. Authority and lineage

- First architecture review: `18be93c3e` (2026-09-30). Concluded the
  representation (linear (op, arg) programs over the frozen GENEXEC2 VM, with
  CALL for fragments) is expressively adequate for the task battery; every
  observed failure was a failure to FIND a program, never a failure to EXPRESS
  one; the defect localized to discovery machinery (score-ranked retention of
  partial programs). Stated falsifier: if every hypothesis fails T0 through T5
  on the frozen VM within the frozen cost budget, the assessment is overturned
  and a VM-level review replaces further discovery work.
- Discovery battery prereg: `425f7276d`. Freezes the GENEXEC2 interpreter
  exactly as committed in `8d5f58b89`, the op set, the task episodes, the
  1M-evaluation budget, and the confirmation rule (outcome without the
  predicted mechanism trace is UNCONFIRMED).
- Discovery comparator: `2e2419a79`. Operationalized the three trigger
  conditions T-A, T-B, T-C and the sequencing guard. Recorded D's MOD-trick
  finding: T1 no longer discriminates conditional from straight-line
  machinery, so the v1 battery does not measure what it claims.
- Frontier H-NEW-6 (valley-depth characterization battery, `1d72eac51`):
  provides the parameterized depth 1..k measurement the trigger needs.
- This framework: the prepared procedure for the VM-level review that the
  first review's falsifier names.

## 2. Trigger conditions (frozen, from 2e2419a79 section 5)

T-A (mechanism convergence): on the redesigned battery, B, C2, and D all
fail at the same valley depth k*, and k* moves with the budget. Concretely,
doubling the budget from 1M to 2M evaluations doubles the crossable valley
depth. Interpretation: the three mechanisms are budget-bound variants of one
search process, not distinct discovery capabilities.

T-B (C2 falsification): C2 fires C2-F1 (T0 fail), C2-F4 (T0 needs more than
6 backtracks), or C2-F3 (degenerate splits). Interpretation: the non-myopic
repair lineage is exhausted. Greedy repair (C1) was falsified; non-myopic
repair (C2) would then be falsified; the counterexample-driven growth idea
has no live variant left.

T-C (battery exhaustion): the redesigned battery shows that every valley
deeper than depth d* (for small d*, e.g. 2) is unsolvable by all three
mechanisms within 10x budget, and the failures are all budget-shaped.
Interpretation: the representation is the binding constraint, not any
mechanism's search policy.

Evaluation rule: any one condition opens the review. The trigger is evaluated
by a worker that (a) runs the H-NEW-6 valley battery for B, C2, D at fixed
budget on the redesigned tasks, (b) checks budget-scaling of k*, (c) reports
which conditions hold. The trigger evaluation itself is preregistered before
running: frozen valley parameterization, frozen budget levels, frozen
pass/fail criteria per depth.

## 3. Sequencing guards

1. Do not open the review on C2's raw T0-T5 outcomes alone. D's MOD-trick
   finding means the v1 battery does not measure what it claims; the
   redesigned battery (tasks provably requiring conditional structure) must
   be committed first.
2. The battery redesign must be committed before trigger evaluation begins.
3. C2's mechanism-trace requirement stands through the trigger evaluation:
   outcome match without the predicted trace is UNCONFIRMED per the battery
   confirmation rule and does not feed the trigger. In particular, a C2 T1
   solve via straight-line MOD-trick repair is UNCONFIRMED against the
   frozen "SOLVE via splits" prediction, and a C2 T4 straight-line solve is
   UNCONFIRMED against "nested splits, 0 CALLs".
4. B and D both violated K4 (disclosed Python use); neither implementation's
   logic may be adopted without a clean rerun. The trigger evaluation uses
   their committed traces as evidence about task structure, not as adoptable
   mechanisms. If clean reruns are required for trigger validity, the review
   preparer must say so explicitly before the trigger worker launches.

## 4. Review process (K1)

Phase R0 (trigger verification): an independent check that the trigger
evaluation was preregistered, that the redesigned battery carries a
discrimination proof per task (each task provably requires the structural
capability it claims to test; no MOD-trick-class degenerate solution
exists), and that mechanism traces rather than bare outcomes fed the
trigger verdict.

Phase R1 (failure taxonomy): for each (mechanism, task, depth) failure,
classify the failure mode using committed traces: budget exhaustion,
backtrack exhaustion at BMAX, kink-routing misfire, archive saturation,
degenerate split, or representation-shaped (failure signature identical
across mechanisms). This taxonomy is the evidence base for Phase R2.

Phase R2 (the representation question): apply the three operational tests
in section 5. Each test is reported separately with its evidence.

Phase R3 (decision): emit exactly one verdict from section 6, with a
committed decision record naming the evidence for each test. A verdict of
REPRESENTATION-WRONG must name the failing sense and authorize exactly one
new representation track with its own preregistered battery.

Phase R4 (governance): the decision record is committed before any new work
is authorized. Any new representation track requires a fresh preregistration
(frozen interpreter or construction substrate, frozen battery with
discrimination proofs, frozen falsifiers) before any implementation. The
review may not authorize a C3, D2, B2, or any variant that keeps linear
(op, arg) GENEXEC2 programs as the program form.

Roles: the review is conducted by a worker with no authorship of the B, C2,
or D implementations (independence bar). The review reads committed traces
only and writes no implementation code.

## 5. What "the representation is wrong" means (K2)

Three distinct senses, each with an operational test. The review must run
all three and report each separately. Conflating them is the failure mode
this section exists to prevent.

Sense 1: EXPRESSIVENESS. The representation cannot express some program the
battery requires.
Test: for each redesigned-battery task, exhibit a GENEXEC2 program meeting
SOLVE or prove none exists. If any required program is unexpressible,
Sense 1 holds. Prior evidence: the first review found all v1 T0-T5
expressible; the redesigned battery must re-establish this from scratch,
because new tasks may not inherit the old verdict.

Sense 2: DISCOVERABILITY. The representation makes required programs
undiscoverable by any mechanism within budget, though they are expressible.
Test: T-C is the operational form. If all mechanisms fail at the same
shallow depth with budget-shaped failures on tasks with known expressible
solutions, Sense 2 holds. The cross-mechanism signature distinguishes this
from mechanism defects: mechanism defects have characteristic signatures
(B: kink-routing misfires on the trace; C2: backtrack exhaustion at BMAX=6;
D: archive saturation with thousands of elites and no niche improvement).
Representation-shaped failures look the same across all three mechanisms:
smooth degradation with budget, no mechanism-specific signature.

Sense 3: DISCRIMINATION. The representation admits degenerate solutions that
satisfy the formal SOLVE criteria without demonstrating the capability
under test.
Test: D's MOD trick is the exemplar: [IN0 PUSH:-2 IN0 MUL MOD NEG NEG]
computes |x| exactly via truncated division, satisfying T1's formal
criterion while using no conditional machinery. For each task, the review
asks whether a formally correct solution exists that bypasses the intended
structural requirement (conditional computation, composition, reuse). If
such degenerate solutions exist and are reachable within budget, the battery
measures search luck rather than the capability, and the representation
plus the SOLVE definition is wrong in Sense 3 even if Senses 1 and 2 pass.
Remedy may be battery redesign rather than representation change; the
review must state explicitly which one the evidence supports.

Verdict rule: the representation is WRONG if any sense holds and the defect
is attributed to the representation rather than the battery protocol. If
Sense 3 holds but the defect is in the SOLVE definition, the episode
encoding, or the task design, the verdict is BATTERY-WRONG (section 6):
redesign the battery, keep the representation. A Sense 3 finding must not
be used as a pretext for representation change when a protocol fix
suffices.

## 6. Decision outputs

The review must emit exactly one of the following, with evidence cited per
test from section 5:

- REPRESENTATION-OK: all three senses pass on the redesigned battery. The
  defect remains in discovery machinery. Authorize continued mechanism work
  with a named next hypothesis, its frozen falsifiers, and its prereg.
- BATTERY-WRONG: a Sense 3 defect is attributed to the protocol (SOLVE
  definition, episode encoding, or task design). Authorize battery redesign
  v2 with per-task discrimination proofs. The representation is retained.
  No new representation track is authorized.
- REPRESENTATION-WRONG (Sense N): name the failing sense (1 or 2; Sense 3
  attributed to the representation itself, not the protocol). Authorize
  exactly one alternative-representation track selected from section 7 (or a
  new alternative with written justification for why no listed alternative
  fits). The new track receives a fresh preregistered battery with
  discrimination proofs before any implementation.

Forbidden in all cases: spawning C3, D2, B2, or any variant that keeps
linear (op, arg) GENEXEC2 programs as the program form. Per the standing
architecture-review trigger, the review must examine whether the program
representation, the episode encoding, or the train/hidden protocol is the
defect, and may not answer a representation question with another search
policy over the same representation.

## 7. Alternative representations to consider (K3)

Each alternative names the defect sense it addresses and the constraint it
must satisfy. Constraint for all: C0-A. The source must contain only
generic execution and construction machinery; the semantics of any
learner-created structure must live in learner-created persistent state,
with no dedicated semantic case written before training. An alternative
that entrenches researcher-authored form fails the purpose of the review
even if it improves benchmark scores.

1. Named-variable register programs. Replace the anonymous stack with a
   small set of named registers. Addresses Sense 2: stack shuffling
   (DUP, SWAP, OVER) inflates program length and creates spurious valleys,
   because every data movement is a search step. A register form shortens
   the distance between semantically adjacent programs.

2. Expression trees with first-class conditionals. Replace linear op
   sequences with tree-structured expressions where IF with branches is a
   node type, not a jump-offset trick (JZ/JMP with numeric targets).
   Addresses Sense 3: conditional structure is currently encoded as
   control flow with fragile offsets, and the MOD trick shows arithmetic
   can masquerade as conditionals. First-class conditionals make the
   structural distinction the battery needs directly representable and
   directly checkable in traces.

3. Dataflow graphs with learner-defined node types. Programs as directed
   graphs; node types drawn from a learner-extensible set rather than a
   frozen opcode list. Addresses Sense 2 and the C0 direction: a fixed
   linear topology plus a fixed opcode set may be the discoverability
   bottleneck. Connects to the OP-RECRUIT v2 track: recruited operators
   become graph node types with learner-defined semantics in persistent
   state, which is the C0-A direction (runtime-defined semantics).

4. Typed programs with signatures. Each program carries an input/output
   type signature; construction is type-directed and ill-typed candidates
   are never generated. Addresses Sense 2: much of the 1M-evaluation
   budget is spent on type-incoherent candidates (stack underflows are
   silent no-ops producing junk that still costs a full evaluation).
   Types prune the search space by construction rather than by
   evaluation.

5. Richer episode encoding. Keep a stack VM but change what an episode is:
   currently integer inputs with top-of-stack integer output. Alternatives
   include multi-value outputs, structured inputs, or behavioral episodes
   (input/output traces over several steps). Addresses Sense 3: the
   discrimination failure may come from the impoverished episode encoding
   admitting degenerate solutions, not from the VM. This alternative keeps
   the interpreter and changes the protocol.

6. Program sketches with typed holes. The learner proposes partial
   programs with typed holes; a filler mechanism completes them.
   Addresses Sense 2: valley-crossing may require committing to a
   structural skeleton before the details are known. Sketches make
   partial commitment first-class instead of requiring every prefix to be
   a complete executable program, which is what forces greedy mechanisms
   through unevaluated valleys.

7. Rewriting systems (equational programs). Programs as sets of rewrite
   rules rather than instruction sequences. Addresses Sense 2: the linear
   instruction form forces an execution order on what may be naturally
   unordered structure; rewrite rules separate what is computed from the
   order of computation, which may shorten the search distance to
   compositional targets like T4 and T5.

For each alternative the review, if it selects one, must also state: the
discrimination argument (which battery tasks would separate it from
GENEXEC2 and why), the C0 assessment (does it move toward runtime-defined
semantics per C0-A and open structural form per C0-B, or entrench
researcher-authored form), and the cost (new interpreter or substrate,
new battery with discrimination proofs, estimated implementation budget).

## 8. Inputs the review requires

- Committed mechanism traces for B, C2, D on the redesigned battery
  (traces, not bare outcomes; the confirmation rule applies).
- The battery redesign document with per-task discrimination proofs
  (for each task: the structural capability claimed, and a proof or
  exhaustive argument that no degenerate solution of the MOD-trick class
  exists).
- The H-NEW-6 valley-depth measurements: max crossable depth per
  mechanism at fixed budget, plus budget-scaling data for k*.
- The first architecture review (`18be93c3e`) and the discovery
  comparator (`2e2419a79`) as prior art.
- C0 status (`5891940d6`): the review's representation verdict feeds the
  C0-B (open structural form) assessment. A representation change toward
  learner-extensible form is C0-relevant; a change that merely swaps one
  fixed form for another is not.

## 9. Honest scope

This framework prepares a review; it conducts none and prejudges nothing.
The triggers may never fire. If C2 succeeds with mechanism-confirmed
traces on the redesigned battery, the review does not open and the lineage
continues under the existing battery. If the review opens and returns
REPRESENTATION-OK or BATTERY-WRONG, no representation track is authorized.
The framework's value is procedural: if the review opens, it is
preregistered in procedure rather than improvised under disappointment,
with the forbidden move (another search policy over the same
representation) named in advance so it cannot be taken by default.
