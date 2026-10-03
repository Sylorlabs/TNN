# PREREG_FC1: learned idempotence constrains planning

Status: FROZEN. Written and committed BEFORE any FC-1 implementation
exists in the repo. This document alone governs the FC-1 verdict.
No em dashes are used in this file.

## Amendment 1 (2026-10-03, before any implementation exists)

Correction to the T2 experimental hand-derivation, caught by
re-tracing before implementation. With beliefs [1,0,0], the DFS
explores the [2,5] subtree fully before trying [2,7] at depth 1,
and that subtree contains a 0-reacher:
[2,5,2,5,2,5,2,7] (length 8; states 15,8,9,8,9,8,9,8,0).
The original prediction ([2,7]) was wrong: [2,7] is enumerated
only after the entire [2,5] subtree. K-FC-3's T2 clause is
therefore property-level (REACH 1, DBL2 0) rather than
exact-plan; the predicted experimental T2 plan is
[2,5,2,5,2,5,2,7]. No other bar changes. The T2 control
prediction ([2,2,2,2,2,2,2,7]) is unaffected: with no pruning,
the all-2 spine dominates early search and [2]^7,7 is reached
before any [2,5]-subtree 0-reacher. Sections 6, 8, 9, 13 are
updated accordingly; the original wrong line is struck through
in place where practical and restated here.

## Amendment 2 (2026-10-03, before any implementation exists)

Clarification of K-FC-6's checker (not a bar change). A program
cannot observe its own repeated executions, so K-FC-6 is
verified by the build harness, not by the program: the harness
builds once, runs the binary three times, and checks
byte-identity (cmp and sha256), exit code 0 on all runs, and
zero FAIL lines in the output. The program emits the K-FC-1
through K-FC-5 lines and the final verdict line; the harness
appends the K-FC-6 verdict to the run log. The bar's content
(byte-identical, exit 0, zero FAIL) is unchanged.

## 0. Lineage

The 2026-10-02 formal_constraints worker (REPORT.md in the parent
lane directory, verdict FORMAL-CONSTRAINTS-COMPLETE) showed a split
result: a learner CAN construct constraint CONTENT from experience
(induced registry clauses from judgments, task-adequate 6/6), but it
did NOT wire that content into generation by itself; the channel,
the ABI, and the composer's consultation of it remained researcher
machinery, and removing the wiring left generation unconstrained
(Arm N 0/6).

FC-1 attacks the next step of the same question with a different
formal property and a design that closes the wiring loophole as far
as generic machinery allows: the consultation rule here is
domain-neutral ("do not take an action your current model says has
no effect in this position"), not a domain bridge, and Phase 3
(revision) tests that behavior tracks the LIVE belief rather than a
frozen researcher rule. If the belief flips on disconfirming
evidence and the constrained behavior flips with it, the constraint
is doing cognitive work as learned knowledge, not as wiring.

## 1. Question

From the constitution: "Formal understanding must constrain
behavior: design tests for errors that should become impossible."
FC-1 tests whether a FORMAL PROPERTY acquired through experience
does real cognitive work. The property is idempotence: op k
satisfies k(k(x)) = k(x). After the learner acquires this property
for k from trials, the error of emitting a plan that applies k
twice in a row (a strictly dominated plan, since the second
application provably adds nothing) becomes IMPOSSIBLE for that
learner. A learner without the property still makes the error.

## 2. The formal property (frozen statement)

Idempotence of a unary operation on states, operationalized
positionally: applying op k immediately after op k never changes
the state. The learner represents this as one bit per op:
SELF_STABLE (1) versus UNKNOWN (0). The bit's MEANING is fixed by
the trial procedure (section 4a) and the prune rule (section 4b);
the bit's VALUE (which op) is learned content.

## 3. World (environment, NOT the learner)

State space: integers 0..15. Three operations with opaque integer
ids 2, 5, 7. The ids are arbitrary and carry no semantic hint.
Physics (three functions; the learner never sees these definitions):

- P_clamp(s) = min(s, 8). Idempotent: P_clamp(P_clamp(s)) =
  P_clamp(s) for all s.
- P_inc(s) = (s+1) mod 16. Not idempotent.
- P_dbl(s) = (2*s) mod 16. Not idempotent
  (e.g. P_dbl(P_dbl(12)) = 0, P_dbl(12) = 8).

Run 1 assignment: op 2 -> P_clamp, op 5 -> P_inc, op 7 -> P_dbl.
Run 2 assignment (permuted): op 2 -> P_inc, op 5 -> P_dbl,
op 7 -> P_clamp.
Phase 3 world change (Run 1 world): op 2 -> P_inc. The formerly
idempotent op becomes non-idempotent. This models a counterexample
world and tests belief revision.

The learner sees only integer ids and may call the world (apply op
to state). It cannot inspect the physics definitions. In the
implementation the physics lives in a marked WORLD section;
learner code only calls w_apply.

## 4. Learner (generic machinery only; no formal rules)

(a) Trial procedure acquire(k). Six trials on the fixed states
[12, 3, 15, 8, 0, 9]. Each trial: s1 = apply(k, s),
s2 = apply(k, s1). If s2 == s1 on ALL six trials, set
belief[k] = SELF_STABLE; else belief[k] = UNKNOWN. This asks a
generic empirical question ("does doing k twice differ from doing
it once?"). The trial count (6), the unanimity rule, and the fixed
trial states are authored machinery. WHICH op satisfies the
criterion is learned content.

(b) Planner. Depth-first search over plan prefixes, max depth 8,
ops tried in fixed numeric order [2, 5, 7]. At each node with a
nonempty prefix, if sim(prefix) == goal, return prefix. Generic
prune rule: when the last op of the prefix is k and
belief[k] == SELF_STABLE, the planner does not extend the prefix
with k. Rationale, stated before execution: "do not take an
action the current model says has no effect in this position."
This rule is domain-neutral decision theory, not a rule about
idempotence: it fires for whatever the belief table contains, and
its content comes only from trials.

(c) Simulation. The planner evaluates prefixes by calling the
world's apply (black box). It holds no symbolic knowledge of op
properties; all symbolic knowledge is the belief table. Both
groups (section 5) share the identical planner and the identical
simulation access; the ONLY difference between groups is the
belief table.

Machinery versus content (frozen):

- Machinery (researcher-authored, domain-neutral): trial loop,
  trial states, unanimity threshold, belief table format, DFS
  planner, fixed op order, max depth, generic no-effect prune,
  black-box simulation.
- Content (learned from experience): which op id is SELF_STABLE;
  the belief revision in Phase 3.

## 5. Groups

- Experimental: runs acquire() on all ops (Phase 1), then plans
  Phase-2 tasks with the resulting beliefs.
- Control: identical planner, acquire() never run, all beliefs
  stay UNKNOWN. This is the learner without the formal property.

## 6. Phases and hand-derived expectations

Phase 1 (Run 1 acquisition). Predicted beliefs: op 2 = 1,
op 5 = 0, op 7 = 0. Derivation: op 2 (clamp) trials:
(12->8->8), (3->3->3), (15->8->8), (8->8->8), (0->0->0),
(9->8->8): every second application is a no-change. op 5 (inc):
first trial (12->13->14) changes. op 7 (dbl): first trial
(12->8->0) changes.

Phase 2 (Run 1 planning). Tasks (frozen): T1 (start 12, goal 9),
T2 (start 15, goal 0), T3 (start 12, goal 8), T4 (start 5, goal 9).
Hand-derived under DFS, max depth 8, op order [2, 5, 7]:

- T1 control: [2] reaches 8; the [2,2] subtree is explored fully
  before [2,5]; the spine [2]^8 all reach 8; [2]^7,5 reaches 9.
  Plan: [2,2,2,2,2,2,2,5]. Contains six (2,2) pairs.
- T1 experimental: [2] reaches 8; op 2 pruned after [2];
  [2,5] reaches 9. Plan: [2,5]. Zero (2,2) pairs.
- T2 control: spine [2]^8 all reach 8; [2]^7,5 reaches 9;
  [2]^7,7 reaches dbl(8) = 0. Plan: [2,2,2,2,2,2,2,7].
  Contains six (2,2) pairs.
- T2 experimental: the [2,5] subtree is explored before [2,7]
  and contains the 0-reacher [2,5,2,5,2,5,2,7] (length 8).
  Predicted plan: [2,5,2,5,2,5,2,7]. Zero (2,2) pairs.
  Property-level bar (REACH 1, DBL2 0); see Amendment 1.
- T3 control and experimental: [2] reaches 8 immediately.
  Plan: [2]. Sanity task: no redundancy is reachable here, so
  both groups are clean.
- T4: control predicted [2,2,2,2,5,5,5,5] (first 9-reacher;
  full derivation in section 9); experimental predicted
  [2,5,2,5,2,5,2,5]. The T4 bars check properties (goal reached,
  (2,2) count), not exact plans, so exact-plan risk is contained.

Run 2 (permuted acquisition only). Assignment: op 2 -> P_inc,
op 5 -> P_dbl, op 7 -> P_clamp. Predicted beliefs: op 2 = 0,
op 5 = 0, op 7 = 1. Derivation: op 7 (clamp) gets the same six
no-change trials as op 2 did in Run 1; op 2 (inc) and op 5 (dbl)
are disconfirmed on trial 1. This proves the property tracks the
FUNCTION, not the id: nothing in the learner is tied to "op 2".

Phase 3 (revision, Run 1 world with op 2 -> P_inc).

- 3a: re-run acquire(2) on the same six trial states. First
  trial (12->13->14) disconfirms. Predicted: belief[2] flips
  1 -> 0. Beliefs for ops 5 and 7 are untouched (0, 0).
- 3b: the experimental learner (revised beliefs [0,0,0]) plans
  T3b (start 12, goal 15) under the new physics. [2] reaches 13;
  [2,2] reaches 14; [2,2,2] reaches 15. Plan: [2,2,2]. The
  redundancy error REAPPEARS once the property is unlearned.
  This is the critical control against "the skip was hardcoded":
  behavior follows the live belief, which follows evidence.

## 7. What "constraining behavior" means observably

The error: a returned plan containing a consecutive double
application (k,k) of the idempotent op. Such a plan is strictly
dominated: deleting one k yields a shorter plan reaching the same
state (by the positional idempotence the learner verified). After
acquiring SELF_STABLE for op 2, the experimental learner's
planner cannot extend a prefix ending in 2 with another 2, so
this error becomes impossible for it: zero (2,2) pairs in every
Phase-2 plan, while every plan still reaches its goal (pruning
never breaks correctness because the pruned action is
model-predicted effectless). The control learner, lacking the
property, emits plans containing (2,2) on T1, T2, and T4.

## 8. Frozen kill bars

K-FC-1 (acquisition, Run 1): emitted beliefs are exactly
[1,0,0] for ops [2,5,7]. PASS iff exact.

K-FC-2 (acquisition, Run 2 permuted): emitted beliefs are
exactly [0,0,1] for ops [2,5,7]. PASS iff exact.

K-FC-3 (constraint, experimental): Phase-2 plans: T1 exactly
[2,5]; T2 reaches its goal and contains zero (2,2) pairs
(predicted [2,5,2,5,2,5,2,7], Amendment 1); T3 exactly [2];
T4 reaches its goal and contains zero (2,2) pairs. PASS iff
all hold.

K-FC-4 (control exhibits the error): Phase-2 plans: T1 exactly
[2,2,2,2,2,2,2,5]; T2 exactly [2,2,2,2,2,2,2,7]; T3 exactly
[2]; T4 reaches its goal and contains at least one (2,2) pair.
PASS iff all hold.

K-FC-5 (revision): Phase 3: belief[2] == 0 after re-acquisition;
experimental T3b plan exactly [2,2,2]. PASS iff both hold.

K-FC-6 (determinism): three consecutive runs byte-identical,
exit code 0, zero FAIL lines. PASS iff all hold.

The program emits one PASS/FAIL line per bar and a final
ALL PASS or SOME FAIL line, and returns exit code 0 iff every
bar passes. Simulation counts (world apply calls during
planning) are emitted as supporting evidence, not as a bar.

## 9. T4 hand derivation (control, Run 1)

DFS order: the [2,2] subtree is fully explored before [2,5];
within it, [2,2,2,2] before [2,2,2,5] before [2,2,2,7]. Start 5.
Along the all-2 spine every state is clamp(5) = 5. First plan
reaching 9: [2,2,2,2,5,5,5,5] (length 8): 2^4 leaves state 5,
then 6, 7, 8, 9. Earlier candidates contain no 9: the [2]^8
through [2]^5 subtrees reach at most 12 via dbl ([2]^7,5 -> 6,
[2]^7,7 -> 10, [2]^6,5 -> 6 with children 6,7,12, [2]^6,7 -> 10
with children 8,11,4, [2]^5,5 -> 6 with children 6,7,12,
[2]^5,7 -> 10 with children 8,11,4); within [2]^4: [2]^4,5 -> 6
(grandchildren reach at most 14, no 9), [2]^4,5,5 -> 7
(children 7,8,14), [2]^4,5,5,5 -> 8 whose child
[2]^4,5,5,5,5] reaches 9 first. Experimental T4: with (2,2)
pruned, the first 9-reacher is predicted
[2,5,2,5,2,5,2,5]: at node [2,5,2,5,2,5] (length 6, state 8),
op 2 is tried before op 5, giving [2,5,2,5,2,5,2] (state 8),
whose expansion yields [2,5,2,5,2,5,2,5] (state 9) before the
[2,5,2,5,2,5,5] sibling is tried. The T4 bars check properties
only.

## 10. Adversarial considerations (frozen)

(a) "The skip is hardcoded for op 2." Refuted by K-FC-2 (the
property is acquired for op 7 under permutation) and K-FC-5
(behavior flips when the evidence flips). No id, and no op
count, is special in the learner.

(b) "The planner's perfect simulation does the work." Both
groups share the identical planner and identical black-box
simulation access. The only difference between groups is the
belief table. Any behavioral difference is therefore caused by
the acquired property.

(c) "The prune rule smuggles idempotence." The rule is stated
without reference to idempotence: skip an action the current
model predicts is effectless in this position. Its idempotence
content comes entirely from the trial procedure's verdicts.
This machinery/content split is the load-bearing assumption
and is open to red-team review.

(d) "Pruning could break correctness." Every experimental plan
must still reach its goal (asserted in K-FC-3). If pruning ever
removed a needed action, K-FC-3 would fail.

(e) "Unanimity on six trials is weak induction." Granted; the
claim is not deductive certainty but that the acquired
inductive property constrains behavior, and that the constraint
is revisable (Phase 3).

## 11. Explicit non-goals

- One formal property (idempotence), one op family. Generality
  across properties (inverses, commutativity, associativity) is
  future work.
- The trial threshold and unanimity rule are authored machinery,
  not learned.
- No L2/L3 classification claim. This is a mechanisms test of
  whether learned knowledge constrains behavior.
- Simulation counts are reported, not barred.

## 12. Execution and governance

- Pure Zag only: no Python anywhere (editing, building,
  running, verifying). Safebin mandatory; Step 0 recorded in
  NAMECHECK.md in this directory.
- This prereg is committed alone BEFORE any FC-1 implementation
  exists in the repo. The prereg commit must strictly precede
  the implementation commit (commit-order self-check).
- Verdict names the exact frozen bars above. No bar may be
  weakened or redefined after results.
- Commits are local; nothing is pushed without Micah's explicit
  approval. Explicit pathspecs only; never broad-stage other
  workers' files. Never commit binaries.
- No em dashes in the prereg, the source, or the result doc.
- Determinism: build once with the pinned safebin znc; run the
  binary three times; outputs byte-identical (cmp + sha256).

## 13. Output format (frozen)

The program writes to stdout (single buffered write):

FC1 IDEMPOTENCE-CONSTRAINS-PLANNING
RUN 1 ACQUIRE
BELIEF 2 <0/1>
BELIEF 5 <0/1>
BELIEF 7 <0/1>
RUN 1 PHASE 2
EXP T1 PLAN <ids> REACH <0/1> DBL2 <n> SIMS <n>
CTL T1 PLAN <ids> REACH <0/1> DBL2 <n> SIMS <n>
EXP T2 ...
CTL T2 ...
EXP T3 ...
CTL T3 ...
EXP T4 ...
CTL T4 ...
RUN 2 ACQUIRE PERMUTED
BELIEF 2 <0/1>
BELIEF 5 <0/1>
BELIEF 7 <0/1>
PHASE 3 REVISION
BELIEF 2 <0/1>
EXP T3B PLAN <ids> REACH <0/1> DBL2 <n> SIMS <n>
BARS
K-FC-1 <PASS/FAIL>
K-FC-2 <PASS/FAIL>
K-FC-3 <PASS/FAIL>
K-FC-4 <PASS/FAIL>
K-FC-5 <PASS/FAIL>
K-FC-6 <PASS/FAIL>
ALL PASS | SOME FAIL

DBL2 counts consecutive (2,2) pairs in the emitted plan. SIMS
counts world apply calls during that planning call. Frozen
predictions: K-FC-1: [1,0,0]. K-FC-2: [0,0,1]. K-FC-3: T1
[2,5], T2 REACH 1 DBL2 0 (predicted plan [2,5,2,5,2,5,2,7]),
T3 [2], T4 REACH 1 DBL2 0. K-FC-4: T1
[2,2,2,2,2,2,2,5], T2 [2,2,2,2,2,2,2,7], T3 [2], T4 REACH 1
DBL2 >= 1. K-FC-5: BELIEF 2 0, T3B [2,2,2].
