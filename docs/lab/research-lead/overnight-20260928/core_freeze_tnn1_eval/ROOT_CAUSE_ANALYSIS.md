# CORE-FREEZE-TNN1 Root-Cause Analysis

Date: 2026-10-01. Worker: CORE-FREEZE-TNN1 Root-Cause Analyst (subagent).
Governing directive: cluster failures into shared architectural causes,
not per-world patches (Micah, 2026-09-30).

## Method

This is analysis only. No source edits, no builds, no sealed-asset access
beyond the committed evaluation record. All architectural claims are
grounded in the frozen TNN-1 source as preserved verbatim in
`core_freeze_tnn1_shim/freeze_shim.zag` (lines 1-1093, 1095-1328 =
frozen TNN-1 `d3895083c9f8`, confirmed by SHIM_REPORT.md section 5)
and in the committed per-world transcripts in `runs/`.

## Score recap

FW SCORE 4/9 (FW1, FW2, FW4, FW5 pass). OLD-WORLD 4/9 (up from 1/9).
Failures: FW3/W3 arithmetic, FW7/W7 planning, FW8/W8 novel utterance,
FW9/W9 relational DAG, FW6/W6 active inquiry (degenerate constant).

## What passes, and why it matters

FW1/FW2 (associative recall) pass through `activate`: exact-key
retrieval of taught facts. FW4 (law change/revert) passes through
`contradict_map` + `map_standing`: contradiction adds a CON edge and
demotes standing, so the revised fact wins. FW5 (targeted update)
passes the same way: `ev_observe` on a conflicting fact contradicts
the old node and teaches the new one, with no collateral damage.

The pattern: TNN-1 is a competent RETRIEVAL and STANDING machine.
It stores, retrieves, contradicts, and demotes. Every failure below
is a failure of GENERATION: the learner cannot construct a novel
executable structure at runtime, on either the query path or the
act path.

## Per-cluster architectural diagnosis

### Cluster 1: FW3/W3 arithmetic (0/10 both)

Transcript: multiplication facts observed (2*3=6, 2*4=8, 3*3=9, ...);
every probe query answered `ANSWER <s> 32500 -2`.

Trace through `ev_query` (frozen source line 648): exact hit fails
(no stored fact for the probe key), so the miss policy `mp_run`
(line 586) builds candidate plans from exactly three fixed templates
(`plan_c2`, `plan_it`, `plan_g` at lines 331-358) plus
compose-by-cloning (`plan_ext`, `plan_c2c`). These templates express
lookup, single accumulation, and chained lookup. None can express
"multiply the two operands." The P-INV fallback (`bootstrap_miss`,
line 625) requires all recent observations to agree on one value;
multiplication examples disagree, so it returns -2. Result: -2 on
all 10 probes.

The standing question: why can the existing general architecture not
learn this behavior? Because the miss path has no procedure
constructor. The approved EXECUTE 4-op ISA (`execute`, tags 101-104,
frozen source line 195) is present but unreachable from the cognition
path: its only callers are test functions `t_c6`/`t_c7` (lines
800-812). The query path's plans run through a DIFFERENT executor
(`exec_plan`, line 427) over a different step vocabulary (kinds 1-6:
READ/MOVE/BEQ/INC/EMIT/APPLY). So the architecture contains a frozen
domain-neutral ISA and a separate fixed-template plan vocabulary that
never meet. MUL Rung B (commit `a2223cc11`) proved the learner CAN
construct ADD then MUL-from-ADD through CALL in the 4-op ISA, but
that trial harness lives in a standalone experiment, never integrated
into TNN-1's miss path. The knowledge of how to build executable
structure exists in the lab but not in the learner.

### Cluster 2: FW7/W7 planning (0/4 both)

Transcript: transition facts observed (state->prev/next edges), then
`CHOICE 0` emitted on every ACT event, 21 times in FW7. The grader
records 0 visited goals.

Two stacked architectural failures:

(a) The action channel is dead. `ev_act` (line 691) iterates edges
of POLICY_ROOT (`ng(W,0,20)`); if `pr<2` it returns 0 immediately.
Candidates must be learner-created nodes linked to POLICY_ROOT with
a role field matching the ACT context stack (`ctx_push(W,-3)` at
line 692, role check at lines 701-704). In the frozen cognition
path, NOTHING creates guides or links them to POLICY_ROOT:
`pol_set` and the guide builder `r_mk_guide` are called only from
test functions (lines 822-1325, all `t_*`/`r_*` test scope).
Therefore POLICY_ROOT is always empty in every world, and `ev_act`
always returns its hardcoded 0 fallback. The "CHOICE 0" in the
transcripts is not a choice among alternatives; it is the
no-candidate fallback.

(b) Even with a live channel, nothing converts transition facts into
an action sequence. Planning requires constructing a multi-step
executable structure (walk from state to goal) and emitting its steps
as actions. The plan constructor (cluster 1) builds query-answer
plans, never action plans, and there is no plan-to-action emission
path.

The standing question: why can the existing general architecture not
learn this behavior? Because action in TNN-1 is selection-only over
learner-built guides, and the guide-construction pipeline exists
only as test scaffolding. Experience has no path from observation
to guide creation. The FW6 responder contract even keys on this:
it releases the next phase when it sees the diagnostic miss line
followed by "CHOICE 0", because the adversary knew the constant was
structurally guaranteed.

### Cluster 3: FW8/W8 novel utterance (0/5 novel both, retention 4/4)

Transcript: seen utterances recalled exactly (4/4 retention); every
novel combination answered -2.

Same miss path as cluster 1, same verdict: the three fixed templates
cannot compose parts into the required novel form, P-INV cannot fire
on disagreeing examples, and there is no general composer. Retention
passes because `activate` is exact-key retrieval; novelty fails
because novelty needs construction and the constructor vocabulary is
frozen at three shapes.

The standing question gets the same answer as cluster 1: the
architecture retrieves stored wholes but cannot assemble new wholes
from learned parts at runtime.

### Cluster 4: FW9/W9 relational DAG (FW: 5/30, 9/30; W: 14/28, 14/26)

Transcript: DAG edges observed (child->parent); multi-hop queries
answered -2 almost uniformly (one depth-1 query answered 1 in FW9a,
a few in FW9b).

Variable-depth traversal requires a learner-assembled LOOP over
edges: follow parent pointers until a condition holds. The plan
vocabulary's only loop-capable template, `plan_it` (lines 352-359),
is a fixed iteration shape (read slot, branch-on-miss, increment,
re-read the SAME key) that cannot traverse a DAG. The 4-op ISA,
which CAN express traversal loops (BRANCHEQ + MOVE over learner
state), is unreachable from the cognition path (cluster 1).
`mp_compose` extends plans by cloning steps, not by closing loops
over relations.

The standing question: same answer again. The learner cannot
assemble a novel iterative structure from experience. Fixed
templates cover fixed-depth composition (which is why some 1-hop
queries answered); anything needing a runtime-built loop fails.

### Cluster 5: FW6/W6 active inquiry (degenerate constant action)

Transcript (treatment arm): phase B1 emits the diagnostic miss
(`ANSWER 35002 35502 -2`) then `CHOICE 0`; phase B2 answers known
facts correctly (recall works) with no inquiry behavior. Report:
B1 3/3 and B2 0/3 numerically met, B4 FAIL; all CHOICE lines
constant "CHOICE 0" (5/5). Adversary reading: WORLD-FAIL.

Mechanism of the degenerate constant (the precise architectural
trace): an inquiry world needs the miss (-2) to become an inquiry
act. In frozen TNN-1, a miss produces NO persistent state: `ev_query`
returns -2 without creating a UNCERTAINTY node and without creating
any guide. The clean inquiry mechanism (12 admissions -> 12
UNCERTAINTY nodes -> 12 guides, commit `18ed3331c`) exists only in
the standalone inquiry build and in test scaffolding (`r_mk_uncert`,
line 1113, and S8 test stage, line 1013); it is absent from the
frozen cognition path. With no uncertainty node and no guides,
`ev_act` hits the `pr<2` fallback and returns 0. The degenerate
constant is therefore not a policy choice or a tuning artifact; it
is the only output the architecture can produce, by construction,
whenever inquiry is required.

The standing question: why can the existing general architecture not
learn this behavior? Because the miss-to-inquiry pipeline was
validated as a mechanism but never integrated as architecture. The
frozen learner has a miss detector (-2) and an action selector
(`ev_act`), but no learner-state link between them.

## Pointed questions from the tasking

### Is the FW6 degenerate the same root cause as the FW8 novel-utterance failure?

Same family, different proximate mechanism. Both are failures of
generative output: the architecture treats output as selection among
stored structures rather than construction of new executable
structure. But:

- FW8: a constructor EXISTS on the query path (3 templates); its
  vocabulary is too weak for the required composition.
- FW6: NO constructor exists on the act path; the guide pipeline
  (uncertainty -> guide -> POLICY_ROOT -> ev_act selection) is
  test-only scaffolding.

They should not be merged into one fix. FW8 needs a stronger runtime
constructor on the query path. FW6 needs the miss-to-guide pipeline
moved from test scaffolding into the cognition path. A single
"output constructor" concept covers both only if it is built once
and shared by both paths (see Change 1 + Change 2 below, which are
designed to converge on one executable graph type per Micah's
doctrine).

### Is the FW3 arithmetic failure the same root cause as MUL Rung B's 0/4 revision failure?

No, but they are adjacent stages of one lifecycle gap. FW3 fails at
CONSTRUCTION: the learner never builds MUL at all. MUL Rung B
(standalone) succeeded at construction (primitive basis ->
learner-built ADD -> learner-built MUL via CALL) and failed at
REVISION: 0/4 on restructuring the loop after counterexamples.
The shared architectural cause is that the executable-structure
lifecycle is one-shot everywhere it exists: TNN-1's query path has
neither construction nor revision of executable graphs; the MUL
harness has construction but no counterexample-driven restructure
operator (`contradict_map` demotes MAP standing only; nothing
rewrites an executable graph). Shipping construction without
revision would move the FW3 failure to the MUL Rung B failure
inside the continuing learner. The next generation needs both
together. This is the explicit connection to Micah's high-priority
direction: generic revision of learner-created executable
structures is not a follow-up to construction; it is half of the
same change.

### Do FW7 planning and FW9 relational DAG share a cause?

Yes, in large part. Both require the learner to assemble a novel
multi-step iterative structure at runtime: FW9 a traversal loop
over relations, FW7 an action sequence over transitions. Both hit
the same wall: fixed templates cannot close novel loops, and the
4-op ISA loop machinery is dead code. FW7 additionally needs the
act channel (cluster 2a), which is the FW6 fix. So FW7 = (FW9's
constructor gap) + (FW6's action-channel gap).

## Shared-cause clustering: the minimal change set

Three architectural changes address all five clusters. Each fixes
more than one world; none is a per-world patch; none adds opcodes
(ISA stays frozen per Micah's ruling); none adds modes, bridges, or
handlers (one-system rule).

### Change 1: One executable graph type, constructed at runtime, executed by EXECUTE

Problem addressed: the query path's plan vocabulary (step kinds 1-6
via `exec_plan`) and the approved 4-op ISA (`execute`) are two
separate graph types, and the ISA one is dead in the cognition path.

Change: make the miss path construct learner-authored executable
graphs IN THE FROZEN 4-OP ISA and run them through the existing
`execute` entry point. Concretely, integrate the MUL Rung B trial
machinery (propose graph -> execute on training cases -> verify on
held-out -> promote on pass) into `mp_run` as the general miss
policy, replacing the fixed three templates as the primary
constructor (templates may remain as seed heuristics, not as the
ceiling). This is Micah's stated doctrine: procedure and plan
converge on the same executable graph type.

Worlds fixed: FW3 (construct MUL/ADD from the ISA basis at query
time), FW8 (construct compositional utterance programs), FW9
(construct traversal loops), and half of FW7 (construct the
action-step sequence as an executable graph).

Why the architecture cannot do this today: the trial harness that
proved the capability was never given a home inside the learner.
The miss path predates it and was never rewired.

### Change 2: Close the miss-to-act loop in learner state

Problem addressed: `ev_act` is selection-only over guides, guides
are test-built, misses create no uncertainty state.

Change: integrate the validated clean inquiry mechanism into the
frozen cognition path as ordinary learner state operations, not as a
mode: on miss (-2), create an UNCERTAINTY node linked to the miss
context (this is the "uncertainty originates from learner state"
requirement); the miss policy creates a guide node (inquiry action
candidate) linked to POLICY_ROOT with a role matching the ACT
context, exactly as the test scaffolding does today but driven by
experience. No new modes, no handlers: uncertainty nodes and guides
are node/edge types the core already supports.

Worlds fixed: FW6 (miss becomes a contingent inquiry act instead of
constant CHOICE 0), and the other half of FW7 (the action channel
becomes live, so Change 1's constructed action sequences can be
emitted as actions rather than answers).

Why the architecture cannot do this today: the guide pipeline was
built as test scaffolding around a selection protocol, never as a
learning pathway. The selection protocol itself is sound (bid,
directional eviction, supersession all passed ACT remediation);
what is missing is the learner-state source of candidates.

### Change 3: Generic revision of learner-created executable structures

Problem addressed: construction without revision repeats the MUL
Rung B 0/4 wall inside the continuing learner.

Change: a counterexample-driven restructure operator over
executable graphs. When a promoted executable structure fails on a
new case, the learner must be able to modify the graph (retarget a
branch, adjust a loop bound, insert/remove a step) and re-verify,
rather than only demoting its standing. Demotion (`contradict_map`)
is the correct response for a wrong FACT; revision is the correct
response for a wrong PROCEDURE. These are different operations and
the architecture currently has only the first.

Worlds fixed: none directly on the current battery (no world tests
revision of a constructed procedure yet), which is precisely why it
must be built alongside Change 1 rather than after the next
failure. It resolves the MUL Rung B BUILD-PASS ceiling (0/4
revision) and future-proofs every world Change 1 fixes: the first
constructed MUL that meets a zero or negative case will need
restructuring, not just demotion.

Explicit link to Micah's high-priority direction: this IS the
generic revision of learner-created executable structures he
named as the post-freeze priority. The freeze evidence sharpens
it: revision must operate on the same executable graph type that
Change 1 constructs, or the architecture splits into a constructor
that builds and a reviser that cannot touch what was built.

## Coverage matrix

| Change | FW3 | FW7 | FW8 | FW9 | FW6 | MUL Rung B 0/4 |
|---|---|---|---|---|---|---|
| 1: runtime ISA construction | fixes | half | fixes | fixes | - | subsumes construction |
| 2: miss-to-act loop | - | half | - | - | fixes | - |
| 3: generic revision | future-proofs | future-proofs | future-proofs | future-proofs | - | fixes |

No change fixes only one world. Change 1 + Change 2 together are
necessary and jointly sufficient for FW7. Change 3 has no current
battery bar but is the load-bearing half of Change 1.

## What the NEXT GENERATION should build (architectural, not per-world)

1. A single executable graph type in the frozen 4-op ISA, used by
   both the query miss policy and procedure learning. Retire the
   parallel step-kind 1-6 plan vocabulary (or reimplement it as
   sugar over the ISA); two graph types is one too many.
2. The MUL Rung B trial loop (propose/execute/verify/promote) as
   the general miss policy inside the continuing learner, with no
   per-task harness.
3. Miss -> UNCERTAINTY node -> guide -> POLICY_ROOT as the ordinary
   cognition-path consequence of a miss, using only existing node
   and edge types. The inquiry build (commit `18ed3331c`) is the
   reference implementation to integrate, not to re-derive.
4. A revision operator over executable graphs, tested by the same
   0/4 counterexample battery that MUL Rung B failed, before any new
   capability claim.
5. Do NOT add MUL, DIV, traversal, or inquiry opcodes to the ISA.
   Do NOT add an inquiry mode or a planning module. Every one of
   these would be a per-world patch wearing architecture clothes.

## Deliberately deprioritized

- The two documented EXECUTE deviations (literal budget, absent
  kind guard): recorded deviations, not placement falsifiers, not
  failure causes. The budget literal appears in BOTH executors
  (`execute` line 197 and `exec_plan` line 429); making it
  learner-visible is hygiene for the next generation, not a
  capability fix. No world failed because of it.
- FW4-style standing/demotion tuning: FW4 and FW5 already pass;
  the demotion machinery is not a failure cause.
- Compressing the 1328-line architecture below the 1200-line
  ceiling before the next capability test: Micah ruled capability
  and compression are separate axes. Measure first; compress after
  capability is demonstrated.

## Verdict

ROOT-CAUSE-ANALYSIS-COMPLETE. Five clusters reduce to three shared
architectural gaps: (1) no runtime constructor for executable
structure in the frozen ISA, with the capable trial machinery
stranded outside the learner; (2) no learner-state path from miss
to action candidate, with the guide pipeline stranded in test
scaffolding; (3) no revision operator for learner-built executable
graphs, with demotion-only semantics inherited from fact learning.
The next generation is three changes, not five patches.
