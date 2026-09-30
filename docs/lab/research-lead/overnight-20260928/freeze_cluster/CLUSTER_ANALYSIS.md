# Core Freeze Challenge: Failure Cluster Analysis

Date: 2026-09-30. Worker: Freeze Failure Cluster Analyst.
Verdict label: CLUSTER-ANALYSIS-COMPLETE.
Status: analysis only; no implementation proposed.

Source: Core Freeze Challenge run phase (97b28e6a6, FREEZE-RUN-COMPLETE),
RUN_RESULTS.md, per-world battery outputs, governance audit (cee63d75a).
Learner profile: 1/9 WORLD-PASS (W1 only).

## Method

For each failing world (W2-W9), the primary architectural cause was
identified from the run outputs (not just the summary table). Failures
were then clustered by shared missing or broken mechanism. Each cluster
carries a falsifiable prediction: what would change if the shared cause
were fixed. Micah's directive governs the framing: the 1/9 result is
evidence about what the frozen core is missing, not nine requests for
nine patches. Repairs that fix only one world are rejected unless they
reveal a general mechanism.

## Per-world primary causes

### W2 procedures: FAIL 0/8 (all -2)

Run evidence: battery/W2.out shows all 8 probes returning
`ANSWER 8004 801 -2` through `ANSWER 8005 804 -2`. The novel-instance
keys (8004, 8005 with relations 801-804) were never observed during
training. The 15 training teaches churned a single low-index slot
(S1->S2 learner state delta: 7 bytes; W2.out shows the
OBSERVED/EVICT alternating signature).

Primary cause: the frozen core has no procedure-abstraction machinery.
Its only retrieval mode is exact (subject, relation) key lookup. W2
requires deriving a procedure from demonstrations and applying it to
novel instances. Even with perfect storage, novel keys return -2
because there is no rule to apply. The eviction churn is a confound,
not the root cause: it destroyed the training data, but the training
data could not have produced procedure behavior through exact lookup
regardless.

### W3 causal laws: FAIL 0/10 (all -2)

Run evidence: battery/W3.out shows held-out probes returning -2; the
44 training teaches show the OBSERVED/EVICT alternating signature
(S2->S3 delta: 9 bytes). The predicted failure (researcher menus,
construction-vs-selection boundary) is confirmed.

Primary cause: identical in structure to W2. W3 requires constructing
a causal hypothesis (a sum law) from demonstrations and applying it to
held-out inputs. The core stores facts; it does not construct
functions. Novel keys return -2. The eviction churn is again a
confound, not the root cause.

### W4 law change/revert: FAIL (1/6 pre, 2/6 post, 3/6 revert)

Run evidence: battery/W4.out shows the C75 signature verbatim:
```
OBSERVED 9601 610 10
EVICT 9601 610
OBSERVED 9602 610 20
EVICT 9602 610
```
The 6 sequential teaches collapsed to 1-2 surviving keys.

Primary cause: the eviction tie-breaker pathology (C75). The
prediction assumed 6 teaches would occupy 6 slots. The world did not
test reversion; it tested the eviction pathology. No conclusion about
revision machinery can be drawn from this world. This is a pure
state-management failure.

### W5 contradictions: FAIL (1/2 targeted, 4/6 collateral)

Run evidence: RUN_RESULTS.md documents the cascade: W4's keys never
stabilized, so W5's contradiction targets were absent. The 1/2 and 4/6
reflect eviction noise, not belief revision.

Primary cause: cascade from the W4 eviction failure. The world could
not test contradiction handling because its targets did not exist in
stable storage. Pure state-management failure, one step removed.

### W6 active inquiry: FAIL (treatment 1/5, 0/3 vault; control 0/5)

Run evidence (two separable causes):

(a) Eviction confound: battery/W6phaseB.out shows the reveal triple
taught (`OBSERVED 22001 22101 7`) followed by `EVICT 22001 22101` in
the same phase output. Only 1/5 treatment probes correct. Per C1, the
treatment measurement is confounded.

(b) Action-attribution failure (independent of storage):
battery/W6phaseA.out shows the full phase:
```
OBSERVED 23001 23101 5
EVICT 23001 23101
OBSERVED 23002 23101 6
EVICT 23002 23101
OBSERVED 23001 23102 23002
CHOICE 0
ANSWER 22001 22101 -2
EVICT 23001 23102
OBSERVED 23003 23101 7
CHOICE 0
```
The binary's only action signal is the constant CHOICE 0, emitted
wherever the world file places an ACT line. The decoy ACT fires before
any uncertainty signal could exist; the post-diagnostic ACT fires
identically. A one-element constant action set cannot encode selection
among inquiries. The action is a function of file position, not
epistemic state. This is the adversary's structural argument, confirmed
by the outputs. It would persist with perfect storage.

Primary causes: (a) eviction pathology (measurement confound);
(b) missing contingent-action machinery (structural failure).

### W7 planning: FAIL 0/4 (all CHOICE 0)

Run evidence: battery/W7.out contains 24 CHOICE lines, all
`CHOICE 0` (verified: `grep CHOICE W7.out | sort | uniq -c` gives
24 CHOICE 0). No action-selection machinery exists; the goal is
unreachable under all-zero acts per the frozen grader.

Primary cause: missing action-selection machinery. The learner cannot
select actions toward goals. This is more primitive than procedure
learning: even with perfect procedures, constant CHOICE 0 cannot
execute a plan.

### W8 synthetic language: FAIL 0/9 (0/5 novel, 0/4 recall)

Run evidence: battery/W8.out shows all 9 probes returning -2
(e.g., `ANSWER 9901 704 -2` through `ANSWER 9910 704 -2`). The 4
recall probes failed because training triples were evicted (RUN_RESULTS
revises the 4/4 recall prediction on this basis). The 5 novel probes
require composing known words into novel utterances.

Primary causes: (a) eviction pathology for the recall sub-score;
(b) missing compositional machinery for the novel sub-score. The core
cannot combine stored elements into novel structures.

### W9 representational structure: FAIL (0/28 tree A, 0/31 tree B)

Run evidence: battery/W9treeA.out shows all probes returning -2
(e.g., `ANSWER 20001 21007 -2`). RUN_RESULTS documents that 27 of 28
edge triples were evicted (only the last-taught edge survived in S9).
Per C1, the white-box B3 test is confounded.

Primary causes: (a) eviction pathology (measurement confound, destroys
the B3 test); (b) missing traversal/composition machinery. Even with
stable edges, the probes require multi-hop relation traversal, which
single exact-key lookup cannot perform.

## Clusters

### Cluster A: state-management pathology (the eviction tie-breaker)

Worlds: W4 (primary), W5 (cascade), W6-treatment (confound),
W8-recall (confound), W9 (confound). Partial churn confound on W2/W3
training data.

Shared mechanism broken: the frozen store's retention policy.
evict_c() breaks lowest-importance ties by lowest index; when the
36-slot store fills with importance-1 entries, sequential teaches
overwrite the same slot. The substrate cannot stably hold 6 sequential
new facts (C75). Importance is a fixed researcher-defined counter
(correct/wrong/dependents/contradictions); nothing in the policy is
learner-assigned or revisable by experience.

Would fixing it plausibly fix multiple worlds: yes, five. W4 becomes a
clean reversion test (6 teaches occupy 6 slots). W5's contradiction
targets exist. W6's reveal triple survives (treatment measurement
becomes clean). W8 recall returns to the predicted 4/4. W9's edges
survive for a clean B3 white-box test. It would not fix W2, W3, W7,
W6-inquiry-attribution, W8-novel, or W9-traversal, which fail for
independent structural reasons.

Falsifiable prediction: with a stable multi-slot store, W4's 6 teaches
produce 6 surviving keys (S3->S4 delta grows from 36 bytes toward ~200);
W5's contradiction targets answer from storage; W6 treatment scores
3/3 on vault probes by direct recall; W8 recall is 4/4; W9 retains
27+/28 edges in S9.

On Micah's directive: this must NOT become a cache-policy version
treadmill. The general question is what learner-owned memory
representation and policy would let one frozen learner preserve newly
useful knowledge, dependencies, hypotheses, and structures without
task-specific storage logic. The properties a general fix needs (not a
code proposal): (1) retention importance assigned and updated by the
learner from its own experience (probe success, reuse, contradiction
involvement), not only by fixed researcher counters; (2) eviction
sensitive to the role a fact plays in the learner's knowledge
(dependencies it supports, hypotheses it constrains), not just
recency or frequency; (3) the policy itself held in learner-owned
state, revisable by experience rather than frozen at compile time.
Anything less is another tie-break tweak.

### Cluster B: no hypothesis and rule construction machinery

Worlds: W2, W3.

Shared mechanism missing: the ability to construct a generalizable
rule from demonstrations and apply it to novel inputs. The core's only
retrieval mode is exact (subject, relation) key lookup. W2 needs
procedure abstraction from demonstrations; W3 needs causal-law
hypothesis construction from examples. The surface differs
(procedures vs. sums) but the missing operation is identical:
induction from examples to an executable general rule.

Would fixing it plausibly fix multiple worlds: yes, both. A general
rule-construction substrate addresses procedures and causal laws
together because they are the same underlying failure.

Falsifiable prediction: with rule-construction machinery, W2's
novel-instance probes and W3's held-out sums return computed values
instead of -2, while exact-key behavior (W1) is unchanged.

Note on scope: this is the hard L3 problem (procedure and
representation invention). It must not be addressed by adding
researcher-authored semantic cases, which the standing rules forbid
as recreating the treadmill at the L3 frontier.

### Cluster C: no compositional and combinatorial machinery

Worlds: W1 (2 two-hop probes, documented boundary inside the pass),
W8-novel (0/5), W9-traversal (0/28 and 0/31 absent the eviction
confound).

Shared mechanism missing: the ability to combine stored facts.
The core performs single exact-key lookups; it cannot chain relations
(two-hop), compose words into novel utterances, or traverse graph
structure. W1's 10/12 pass with the 2 two-hop failures documents this
boundary inside a passing world: single-hop exact recall works,
composition does not.

Would fixing it plausibly fix multiple worlds: yes, three. W1 goes
12/12; W8 novel probes compose from known vocabulary; W9 traversal
probes resolve multi-hop queries.

Falsifiable prediction: with composition machinery, W1's two-hop
probes return chained values; W8's novel utterances are answered by
combining taught words; W9's probes return correct multi-hop results
given stable edges (requires Cluster A fixed first for a clean test).

Relation to Cluster B: distinct. Cluster B is induction (deriving a
rule from examples). Cluster C is combination (chaining stored facts).
A system could compose without inducing (fixed composition operators
over learned facts) or induce without composing (single-step rules).
They are separate missing mechanisms that happen to share the same
root symptom: the core is a passive store with no computation over
stored content.

### Cluster D: no agentic action machinery

Worlds: W6-inquiry-attribution, W7.

Shared mechanism missing: the learner cannot take actions contingent
on its internal state. CHOICE is the constant 0 regardless of
epistemic state (W6: uncertainty before vs. after diagnostics) or goal
state (W7: 24 identical CHOICE 0 lines toward an unreachable goal).
W6 needs epistemic-state-contingent inquiry selection; W7 needs
goal-directed action sequences. Both are the same underlying gap:
no decision machinery mapping internal state to action.

Would fixing it plausibly fix multiple worlds: yes, both. Contingent
action selection makes W6's inquiry learner-determined (B4 attribution
satisfiable) and gives W7 the action sequences planning requires.

Falsifiable prediction: with contingent-action machinery, CHOICE
varies with internal state: W6 emits different actions at the decoy
ACT (no uncertainty yet) vs. the post-diagnostic ACT (uncertainty
resolved or identified); W7 emits non-zero action sequences directed
at the goal.

Note: W7 additionally needs Cluster B/C machinery for full planning
(chaining actions into procedures, composing subgoals), but its
observed 0/4 is an action-selection failure at a more primitive level
than procedure learning.

## Answers to the specific questions

1. Are W2 (procedures) and W3 (causal laws) the same underlying
failure? Yes. Both require constructing a generalizable rule from
demonstrations and applying it to novel inputs, and both fail because
the core's only mode is exact-key lookup. The surface differs; the
missing mechanism (Cluster B) is identical. They should be addressed
together, never as two patches.

2. Does W7 (planning) depend on W2? No, not for its observed failure.
W7 fails at action selection (constant CHOICE 0), which is more
primitive than procedure learning. Full planning would eventually need
W2's machinery (chaining actions into procedures) and Cluster C's
(subgoal composition), but the observed 0/4 is a Cluster D failure,
independent of W2.

3. Is W6's inquiry failure separable from its eviction confound? Yes.
The eviction confound (reveal triple evicted; treatment 1/5) affects
the numeric measurement. The B4 attribution failure (CHOICE 0
constant; action not contingent on uncertainty) is structural and
independent of storage. Even with perfect memory, the inquiry action
would not be learner-determined. These are two distinct causes in two
different clusters (A and D).

## Ranking

Ranked by (i) worlds covered, (ii) fundamentality, (iii) addressability
by a general substrate change rather than per-world patches.

1. Cluster A (state management): covers 5 worlds (W4, W5, W6, W8,
W9) plus churn confounds on W2/W3. Most fundamental to the
continuing-learner program: a substrate that cannot stably hold 6 new
facts cannot accumulate experience at all, and every other cluster's
clean measurement depends on it (W9's B3 test, W4's reversion test).
Most directly addressable by a general substrate change, with the
explicit warning that it must be a learner-owned memory policy, not
another tie-break tweak. This is the top priority.

2. Cluster B (rule construction): covers 2 worlds (W2, W3).
Fundamental to the general-architecture claim: without it the system
cannot learn procedures or causal laws, only memorize facts. This is
the L3 frontier problem; addressable only by general induction
machinery, never by researcher-authored semantic cases.

3. Cluster C (composition): covers 3 worlds partially (W1's 2 probes,
W8-novel, W9-traversal). Fundamental: without it the system cannot
combine what it knows. Cleanly testable only after Cluster A is fixed
(W9). General multi-hop and combinatorial machinery addresses all
three together.

4. Cluster D (action): covers 2 worlds (W6-inquiry, W7). Fundamental
to agency but downstream of the others for the continuing-learner
program: action selection matters once there is knowledge worth acting
on. Note the interface caveat from the adversary's analysis: the
freeze interface's action channel is narrow, so part of this cluster
may be a measurement-interface limitation as well as a core
limitation; the constant CHOICE is nonetheless a core property.

## The deeper unity (noted, not collapsed)

All four clusters share one root characterization: the frozen core is
a passive exact-key associative store with no computation over stored
content, no learner-owned retention policy, and no action contingency.
Cluster A is retention, Cluster B is induction, Cluster C is
composition, Cluster D is agency. They are kept as four clusters
because each has a distinct falsifiable prediction and a distinct
general substrate change; collapsing them into "the core does nothing"
would lose the actionable structure. But no repair should be designed
that fixes one cluster while leaving the core passive in the other
three dimensions: the One-System Rule rewards fewer special
mechanisms, and the target is one general cognitive substrate whose
capabilities increasingly come from learner-created state.

## What this analysis does not do

This is analysis, not implementation. No code changes are proposed.
The clusters are handed to the designers with falsifiable predictions
so that proposed substrate changes can be preregistered against them.
Per Micah's directive, any proposed repair that fixes only one
freeze-challenge world is rejected unless it reveals a general
mechanism; the rerun philosophy is the same frozen-core discipline on
fresh adversarial worlds, not patches validated against the old ones.
