# CORE FREEZE CHALLENGE: FAILURE CAUSE TRACES, CLUSTERS, AND GENERAL SUBSTRATE PROPOSALS

Date: 2026-09-30. Worker: freeze_analysis lane, wave-20260930-1421pdt.
Status: FREEZE-FAILURE-ANALYSIS-COMPLETE. Design and paper work only. No source modified.
Scope: the completed Core Freeze run (FREEZE-RUN-COMPLETE, 1/9 WORLD-PASS W1 only,
confirmed by the pure-Zag rescore with zero discrepancies; governance audit PASSED).

## Method and sources

Each failed world (W2-W9) is traced to its architectural cause in the frozen core
from primary evidence: the frozen source
`docs/lab/research-lead/overnight-20260928/core_freeze/stage0/world_learn.zag`
(read-only inspection; line numbers cited), `REGIONS.md`, `INTERFACE.md` (via the
design documents), the sealed world designs
(worlds_prefreeze/DESIGN_WORLDS_PREFREEZE.md and worlds_adversary/DESIGN_WORLDS_ADVERSARY.md),
`run_phase/RUN_RESULTS.md`, and the pure-Zag `freeze_rescore/RESCORE_REPORT.md`.

A prior worker's `freeze_cluster/CLUSTER_ANALYSIS.md` (CLUSTER-ANALYSIS-COMPLETE)
exists and was read as reference. This analysis is independently re-derived from
the primary sources, and it goes beyond that document in the one dimension the
prior document explicitly declined: general substrate change proposals with
expected worlds-fixed counts and architecture-accounting impact, per Micah's
2026-09-30 directive (the 1/9 result is evidence about what the frozen core is
missing, not nine requests for nine patches; the store/eviction failure must not
become another cache-policy version treadmill).

Conventions: all proposals obey the One-System Rule (capability from EXPERIENCE
leading to NEW LEARNED STATE/STRUCTURE, never from new Zag subsystems, modes,
bridges, or handlers) and the PROTECTED CORE ISA ruling (core is a small frozen
domain-neutral computational basis: ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ,
ADD, BRANCH, APPLY/EXECUTE, generic state/register operations; no core operation
may encode a target-domain regularity detector). Architecture accounting uses the
2026-09-30 baseline convention: cognition lines count only learn/retrieve/infer/
retain/plan functions; every proposal reports cognition lines added, new semantic
cases, new modes, new bridges, new handlers (all must be zero), and the
learner-state structures the learner would create by experience.

## Per-world cause traces (W2-W9)

### W2: new procedures. Observed 0/8 (all -2). Primary cause: no induction machinery reachable through the generic interface.

The eight execution probes query novel-instance keys (8004, 8005 with relations
801-804) that were never observed. `query()` (world_learn.zag lines 111-121) is
exact (subject, relation) key lookup and returns the -2 not-found sentinel on a
miss; there is no other retrieval path in the challenge driver. Answering a novel
instance requires constructing a general rule (the invariant 4-step operation
sequence) from the three demonstrations and applying it to new keys. No such
construction machinery exists anywhere in the challenge path: the DDES
hypothesis-ledger slice at W[16384..32768) is never written by the generic world
driver, and REGIONS.md documents why ("there are no generic causal event verbs
yet, and adding them would be cognitive machinery, not plumbing"). The only
hypothesis machinery in the binary lives in the legacy P1-P11 driver, which the
source comments mark as not called by the frozen world driver (lines 889-893).
Secondary confound: the 15 demonstration teaches churned one low-index slot
(S1->S2 learner state delta: 7 bytes), so the training data was destroyed as
well; but the root cause is independent of storage, because even perfectly
stored demonstrations could not yield procedure behavior through exact lookup.

### W3: causal laws. Observed 0/10 (all -2). Primary cause: same as W2 (no induction machinery); surface differs, missing operation is identical.

The ten held-out probes query sum keys (pair, 600) that were never observed.
Same exact-key `query()` path, same -2. Predicting a held-out sum requires
constructing the addition hypothesis from the eight interventions and applying
it to fresh pairs: induction from examples to an executable general rule, which
is structurally the same missing operation as W2's procedure abstraction (one
learns a step sequence, the other a value mapping; both need construct-then-apply).
The REGIONS.md admission applies with full force here: there are no generic
causal event verbs, so causal learning is structurally excluded from the
challenge path, not merely unexercised. The 44 intervention teaches show the
same eviction churn (S2->S3 delta: 9 bytes), a confound, not the root cause.

### W4: law changes/reversions. Observed 1/6 pre, 2/6 post, 3/6 revert. Primary cause: state-management pathology in evict_c/learn, two defects.

Defect 1 (tie-break collapse): `evict_c()` (lines 55-69) selects the
lowest-importance valid slot and replaces it only on strictly lower importance
(`if(imp<bestk)`), so ties always resolve to the lowest source index. When the
36-slot store is full of importance-1 entries, every eviction returns the same
low-index slot; the newly taught fact lands there at importance 1 and is
immediately the next eviction victim. The six sequential law teaches collapsed
onto 1-2 surviving keys (the binary output shows the alternating
OBSERVED/EVICT signature on the just-taught key).

Defect 2 (revision actively deprotects): in `learn()`'s revision branch (lines
77-87), a changed observation on an existing key increments BOTH the
contradictions counter AND the wrong counter. `importance_c()` (lines 48-54)
computes 10*(correct-wrong) + 5*dependents - 8*contradictions + 1, so a revised
key with one correct probe, one revision: importance = 10*(1-1) + 0 - 8*1 + 1 =
-7, below every fresh importance-1 slot. The newly learned law value becomes
the single most evictable entry in the store. The revision path conflates
"this belief was corrected" with "this belief was wrong" and punishes the
correction. Consequence: the world tested the eviction pathology, not reversion;
the superseded-field versioning machinery (fields 24, 36) existed but its keys
never stabilized enough to be meaningfully exercised.

### W5: contradictions. Observed 1/2 targeted, 4/6 collateral. Primary cause: cascade from W4's state-management failure.

W5's design contradicts beliefs established in W4 (keys 9601-9602, relation 610).
Those keys never stabilized (see W4), so the contradiction targets were absent;
the 1/2 and 4/6 scores are eviction noise, not belief-revision measurements.
One step removed from Defect 1 and Defect 2 above: no independent structural
cause. Note the design-level reinforcement of Defect 2: a contradiction is
precisely the signal that the world changed, yet the substrate files it as
`wrong`, the same counter as a probe mismatch.

### W6: active inquiry. Observed treatment 1/5 (0/3 vault), control 0/5. Two separable causes.

Cause (a), measurement confound: the reveal triple (22001, 22101, 7) was taught
in phase B and evicted in the same phase output (per C1, the treatment outcome
is CONFOUNDED by the Cluster A pathology, not a clean inquiry measure).

Cause (b), structural and independent of storage: ACT never consults learner
state. The world driver emits the constant `CHOICE 0` unconditionally
(process_line ACT branch; documented as explicit placeholder at lines
1238-1241: "the current substrate has no generic action-selection machinery").
The binary's only action signal is emitted wherever the world file places an
ACT line: the decoy ACT (before any uncertainty signal could exist) and the
post-diagnostic ACT fire identically, so the action is a function of file
position, not epistemic state. A one-element constant action set cannot encode
selection among inquiries. This would persist with perfect storage: it is the
adversary's B4 attribution argument, confirmed in the outputs, and it is the
measured form of protocol prediction 8.4.

### W7: planning. Observed 0/4 (24 CHOICE 0 lines). Primary cause: same as W6 cause (b): no action-selection machinery.

ACT emits the fixed default without reading W (lines 1232-1241). The goal state
9704 is unreachable under all-zero acts per the frozen grader. This failure is
more primitive than procedure learning: even with perfect procedures, a
constant action cannot execute a plan. W7 shares its root cause with the W6
attribution failure: no decision machinery maps internal state to action.

### W8: synthetic language. Observed 0/9 (0/5 novel, 0/4 recall). Two separable causes.

Cause (a): the four recall probes failed because the training triples were
evicted (RUN_RESULTS revises the pre-run 4/4 recall prediction on this basis):
Cluster A confound, not a storage-success case.

Cause (b): the five novel probes require inducing the compositional mapping
(m = 100*v + 10*o + d) from the five training utterances and applying it to
unseen token combinations. The induction half is the Cluster B gap (same
missing construct-from-examples machinery as W2/W3); the application half is a
composition gap (computing over stored token facts rather than one exact-key
lookup). Novel meaning keys were never observed, so all five probes hit the -2
path deterministically.

### W9: new representational structure. Observed 0/28 tree A, 0/31 tree B; 27 of 28 edges evicted. Two separable causes.

Cause (a), measurement confound per C1: 27 of 28 taught edge triples were
evicted (only the last-taught edge survived in S9), so the B3 white-box test
for a new structural topology was not clean.

Cause (b), structural: depth and grandparent probes require multi-hop traversal
of the taught edges. `query()` performs single exact-key lookup. A two-hop
machinery function `twohop()` exists in the source (lines 127-138) but is
called only by `legacy_p1_p11()` (lines 1020-1024), which is dead code in the
challenge path: the generic driver routes events into `learn()` and `query()`
only. So composition-over-content exists as unreachable legacy code, and there
is no generic structural workspace in W: the only state formats are
researcher-fixed (44-byte fact slots; the never-written DDES ledger slice).
This is the measured form of protocol prediction 8.2.

## Clusters (shared architectural causes)

### Cluster A: retention policy is researcher-fixed and self-defeating (W4 primary; W5 cascade; W6/W8/W9 measurement confounds; W2/W3 training churn)

Shared cause: the frozen store's retention policy. Three source-level defects
compose it: (1) `evict_c` resolves importance ties by lowest source index,
collapsing sequential teaches onto one slot when the store fills with
importance-1 entries; (2) `importance_c` punishes revision (a corrected belief
drops to -7, the most evictable entry in the store); (3) the dependents term
(+5*d) is dead through the generic interface (only the unreachable `twohop()`
increments it), so the policy cannot recognize facts that other structures
depend on, and the `last_used` field the store already tracks is never
consulted by eviction. Nothing in the policy is learner-assigned or revisable
by experience; the fixed researcher counters decide what survives.

Falsifiable prediction: with a stable multi-slot store, W4's six teaches occupy
six slots (S3->S4 delta grows from 36 bytes toward ~200), W5's contradiction
targets answer from storage, W6 treatment scores 3/3 on vault probes by direct
recall, W8 recall is 4/4, and W9 retains 27+/28 edges in S9. This cluster is
the top priority: a substrate that cannot stably hold six new facts in sequence
cannot accumulate experience at all, and every other cluster's clean
measurement depends on it (W4's reversion test, W9's B3 white-box test).

### Cluster B: no induction machinery: construct-from-examples to an executable general rule (W2, W3, W8-novel-induction)

Shared cause: the core stores facts and retrieves by exact key; it never
constructs a generalizable rule from demonstrations and never applies one to
novel inputs. W2 needs procedure abstraction (invariant step sequence from
three demonstrations); W3 needs causal-law hypothesis construction (addition
from eight interventions); W8-novel needs grammar induction (m = 100*v + 10*o
+ d from five utterances). The surface differs; the missing operation is
identical: trial construction of an executable mapping from examples,
persistence of the winner, application to novel inputs. The REGIONS.md
admission (no generic causal event verbs; hypothesis ledger unreachable) is the
structural form of this gap.

Falsifiable prediction: with construct-and-apply induction machinery, W2's
novel-instance probes and W3's held-out sums return computed values instead of
-2 while exact-key behavior (W1) is unchanged. Scope guard: this is the hard
L3 frontier problem; it must never be addressed by researcher-authored semantic
cases (FIND_THRESHOLD-style ops), which the standing rules forbid as recreating
the treadmill at the L3 frontier, and which the ISA ruling forbids as protected
core operations.

### Cluster C: no composition machinery: compute over stored content (W1 two-hop probes, W9 traversal, W8-novel-application)

Shared cause: the only retrieval mode is single exact-key lookup. The core
cannot chain relations (W1's two two-hop probes, documented -2 inside the
passing world), compose stored elements into novel structures (W8 novel
utterances), or traverse graph structure (W9 depth/grandparent). Distinct from
Cluster B: B is induction (deriving a rule from examples); C is combination
(chaining stored facts). A system could compose without inducing (fixed
composition over learned facts) or induce single-step rules without composing.
Cleanly testable only after Cluster A is fixed (W9's edges must survive).

Falsifiable prediction: with composition machinery, W1's two-hop probes return
chained values (12/12), W8's novel utterances are answered by combining taught
words, and W9's probes return correct multi-hop results given stable edges.

### Cluster D: no contingent action: ACT never reads learner state (W6 attribution, W7)

Shared cause: the action channel is unconditional plumbing. No byte of the
32768-byte persistent state influences the emitted choice, so action cannot be
a function of epistemic state (W6: uncertainty before vs. after the diagnostic)
or goal state (W7: 24 identical choices toward an unreachable goal). W6's
inquiry failure is separable from its eviction confound (Cluster A): even with
perfect memory, the inquiry action would not be learner-determined. W7's
failure is more primitive than procedure learning and independent of W2.

Falsifiable prediction: with contingent-action machinery, CHOICE varies with
internal state: W6 emits different actions at the decoy ACT (no uncertainty
yet) versus the post-diagnostic ACT, and W7 emits non-constant action
sequences directed at the goal.

## The deeper unity (noted, not collapsed)

All four clusters share one root characterization: the frozen core is a passive
exact-key associative store with no computation over stored content (B, C), no
learner-owned retention policy (A), and no action contingency (D). They are
kept as four clusters because each has a distinct falsifiable prediction and a
distinct general substrate change. No repair should fix one cluster while
leaving the core passive in the other three dimensions.

## General substrate proposals (design only; no implementation)

Each proposal is a general change, preregistrable against the falsifiable
predictions above, consistent with the One-System Rule and the ISA ruling. For
each: the change, why it is general (not a one-world patch), expected
worlds-fixed count, and architecture accounting (cognition lines added, new
semantic cases, modes, bridges, handlers: all zero; plus the learner-state
structures the learner would create by experience).

### Proposal A (Cluster A): learner-owned retention: policy as data, keep-worth assigned by experience

The question Micah posed: "What general learner-owned memory representation and
policy would let one frozen learner preserve newly useful knowledge,
dependencies, hypotheses and structures without task-specific storage logic?"
Answer, in two parts.

Representation: one learner-owned graph in persistent W. Facts, constructed
hypotheses, procedures, plans, and traversal traces are all nodes in the same
node/edge substrate (this converges with the approved architecture direction:
procedures and causal rules as the SAME executable graph type, not separate
engines). Dependencies are learner-written LINK edges from a composite
structure to its premise slots, using the generic ISA LINK operation. No
task-specific storage formats: one node type, one edge type, created by the
learner's own writes.

Policy: keep-worth values are learner-written fields on nodes, updated by the
learner from its own experience (successful probe reuse, service as a premise
of a kept structure, recent revision, being linked from a surviving
structure). The core's eviction routine becomes a generic selector that reads
these learner-owned values with ISA-allowed operations only
(READ, COMPARE/EQ, BRANCH, ADD for accounting): the source never encodes what
is important, it only enforces uniform accounting (one protection currency,
one selection routine). The three source defects are repaired structurally,
not by tie-break tweaking:

1. Tie collapse: ties are broken by learner-owned recency (a sequence the
learner maintains, e.g. a recency chain via LINKs or a learner-written order
counter), never by lowest source index. The pathology disappears because the
ordering is the learner's own, and sequential teaches naturally spread.
2. Revision punishment: the "corrected belief" signal (the versioning trace,
already present as the superseded field) is separated from the "wrong probe"
signal. Revision recency raises keep-worth (actively maintained beliefs are
protected); probe mismatch lowers it. The current conflation (learn()
increments both wrong and contradictions on a changed observation) is the
specific defect to remove.
3. Dead dependents: the dependency field becomes learner-writable through a
generic domain-neutral primitive (a LINK/DEPEND operation exposed by the
driver, not a causal semantic case). When the learner constructs a composite
structure from premises, it records the dependency; eviction respects
learner-written dependency counts. The field already exists (slot offset 20);
it is dead only because nothing reachable writes it.

Why general: the policy contains no fact domain, no task identity, no
benchmark-shaped constants. It protects whatever the learner's own activity
marks as load-bearing: new facts, revised laws, hypotheses under test,
procedures under construction, plans. The store/eviction failure does not
become a cache-policy treadmill because there is no researcher policy left to
version: the researcher ships the accounting machinery once, and all future
retention behavior is learner state.

Expected worlds fixed: 2 direct passes recovered plus 3 measurements
de-confounded. W4 and W5 were both predicted PASS pre-run on the existing
overwrite/versioning machinery (W4: 6/6 pre, post, revert; W5: 2/2 targeted,
6/6 collateral); the pathology destroyed the measurement, not the machinery,
so stable storage restores both passes. W6 treatment (reveal triple survives:
clean inquiry measurement), W8 recall (4/4), and W9 edges (27+/28 retained:
clean B3 white-box test) become measurable. Structural failures in W2, W3,
W6-attribution, W7, W8-novel, W9-traversal remain and are addressed by
Proposals B-D.

Architecture accounting: cognition lines added 0 (the evict/importance
functions are repurposed to read learner-owned values; no new
learn/retrieve/infer/retain/plan functions, net line count falls or holds).
New semantic cases 0. New modes 0. New bridges 0. New task-specific handlers
0. Learner-state structures created by experience: keep-worth fields on nodes,
learner recency ordering, dependency LINK edges from composite structures to
premise slots.

### Proposal B (Cluster B): trial-based construct-and-apply induction over the generic basis

The general change: the frozen core gains no regularity detectors (the ISA
ruling forbids FIND_POLYNOMIAL_ORDER, BUILD_CAUSAL_RULE, LEARN_PROCEDURE and
their equivalents as protected operations). Instead the learner drives a
generic construction loop built only from allowed ISA operations: propose
candidate executable graphs assembled from the generic basis (ALLOC a trial
structure, LINK its parts, APPLY/EXECUTE it against experience), compare trial
outputs to observations (COMPARE/EQ, BRANCH on mismatch), keep the candidates
that predict, persist the winners as executable graph structures in learner
state. The intelligence (which trials to try, when a candidate earns
persistence) is learner-owned policy built from experience; the core supplies
only the trial machinery. This is the direction already approved and landed as
CAM-1 (trial-based P-DEP: finite-difference regularity detection removed from
core intelligence, replaced by trial/compositional discovery using
learner-created structures).

Why general: one induction substrate covers procedures (W2: step sequences
from demonstrations), causal laws (W3: value mappings from interventions),
and grammar induction (W8-novel: the compositional meaning function from
utterances), because all three are the same operation (construct an executable
mapping from examples, persist it, apply to novel inputs). It fixes three
worlds with one mechanism and adds no benchmark-shaped semantic case.

Expected worlds fixed: 3 (W2, W3, W8-novel become pass-capable; W8 also needs
Proposal A for its recall sub-score and Proposal C for application, noted
below).

Architecture accounting: cognition lines added 0 in the protected core beyond
the already-approved generic basis (ALLOC, READ, WRITE, LINK, COPY,
COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE are the frozen ISA class; the trial
loop is learner-driven use of that basis, consistent with the CAM-1 landing).
New semantic cases 0. New modes 0. New bridges 0. New task-specific handlers
0. Learner-state structures created by experience: executable graphs
(procedures and causal rules as the same graph type), trial records, winner
annotations.

### Proposal C (Cluster C): composition as execution of learner-constructed traversal graphs (converges with B)

The general change is not a second mechanism but the same executable-graph
substrate applied to combination: a two-hop probe (7005, 599, 21) is answered
by executing a learner-constructed chain (7005,501)->7006 then (7006,502)->21;
a W9 depth probe by executing a learner-constructed traversal over taught
edges; a W8 novel utterance by executing the induced meaning function over
taught token facts. The missing piece the alignment synthesis names is the
plan/graph constructor; building it once serves induction (B), composition
(C), and eventually planning (D). This is the architectural compression win:
Proposals B and C are one substrate change, not two, fixing five worlds
together (W1, W2, W3, W8, W9).

Why general: no per-relation chaining operator, no graph-traversal semantic
case, no utterance decoder. The core provides APPLY/EXECUTE over
learner-constructed graphs; the learner constructs the chains, traversals, and
decoders from experience. Query remains exact-key lookup at the base; anything
multi-step is an executed learner structure.

Expected worlds fixed: primary credit 2 (W1 completes to 12/12 inside its
pass; W9 traversal probes become pass-capable given Proposal A for stable
edges), assists W8-novel application (shared with B). Combined with B, the
converged substrate addresses 5 worlds (W1, W2, W3, W8, W9).

Architecture accounting: cognition lines added 0 (same substrate as B; no new
functions). New semantic cases 0. New modes 0. New bridges 0. New task-specific
handlers 0. Learner-state structures created by experience: traversal chains
and composition graphs (same executable graph type as B).

### Proposal D (Cluster D): contingent action as a generic read of learner-owned policy state

The general change: ACT stops being unconditional plumbing and becomes a
generic read protocol over a learner-owned action-selection structure (this is
the direction already approved and landed as ACT: learner-state-driven generic
action selection, POLICY_ROOT as node 0, signed evidence bids, a fixed read
protocol). The core contributes only the read machinery (READ the policy
structure, BRANCH on its output); the policy itself (what to choose given
epistemic state or goal state) is learner-created state built from
experience. No INQUIRY_MODE, no PLAN_MODE, no task handlers: the One-System
Rule forbids mode smells, and the fix is one generic action channel whose
content is learner-authored.

Why general: the same channel serves epistemic actions (W6: choose an inquiry
when uncertainty is high, verified by the -2 versus confabulation distinction
the adversary identified as the genuinely learner-contingent gate) and
goal-directed actions (W7: choose acts from the transition model and goal held
in learner state, composed via the Proposal B/C graph substrate). Agency is
one mechanism, not an inquiry module plus a planner.

Expected worlds fixed: 2 (W6 B4 attribution becomes satisfiable: action is a
function of epistemic state; W7 becomes pass-capable given B/C for plan
construction).

Architecture accounting: cognition lines added 0 (consistent with the ACT
landing under the amended ISA package; the read protocol is generic
machinery). New semantic cases 0. New modes 0. New bridges 0. New
task-specific handlers 0. Learner-state structures created by experience:
policy graph rooted at POLICY_ROOT, evidence bids, goal representations.

## Combined projection and honest caveats

If all four proposals land in one continuing learner under the frozen-core
discipline: W1 12/12 (full pass), W2 pass, W3 pass, W4 pass, W5 pass, W6
pass-capable (clean storage plus attributable inquiry), W7 pass-capable, W8
pass-capable, W9 pass-capable: 9/9 pass-capable in principle, up from 1/9.
Caveats, stated plainly: these are design projections, not measured results;
"pass-capable" means the identified architectural cause is removed, not that a
re-run would pass (fresh adversarial worlds may expose new causes, which is
the point of the challenge); W9's B3 white-box bar additionally requires the
new topology to be genuinely learner-constructed, which is the L3 bar, not a
storage bar. No proposal weakens any frozen kill bar to force a pass.

Total architecture accounting across all four proposals: cognition lines added
0, new semantic cases 0, new modes 0, new bridges 0, new task-specific
handlers 0. All new capability comes from learner-created persistent
structures (keep-worth fields, recency ordering, dependency links, executable
graphs for procedures/rules/traversals, policy graphs with evidence bids).
Capability-source delta stays zero by construction.

## Explicitly rejected one-world repairs

Per the directive, repairs that fix only one world are rejected unless they
reveal a general mechanism. Each of the following was considered and rejected:

1. Changing the evict_c tie-breaker from lowest-index to random or
highest-index: a tie-break tweak, not a policy. It would spread W4's teaches
but leave revision punished, dependents dead, and keep-worth researcher-fixed:
the next world with a different pressure shape re-breaks it. This is the
cache-policy treadmill the directive forbids. Rejected in favor of Proposal A.
2. Adding a MUL (or ADD, or threshold) semantic case so W3/W8 pass: directly
forbidden by the ISA ruling (no core operation may encode a target-domain
regularity detector; the basis is never grown one benchmark at a time; MUL
must be learner-constructed from ADD if at all). Rejected in favor of
Proposal B.
3. Adding a two-hop query operator or a tree-traversal handler so W1/W9
pass: researcher-authored semantic cases recreating the treadmill at the
representation frontier (the exact failure mode of REPEXPAND-1/H-PROCLANG1,
downgraded to L2+). Rejected in favor of Proposals B/C (learner-constructed
traversal graphs).
4. Adding an INQUIRY_MODE or PLAN_MODE, or a W6/W7-specific action handler:
architectural smells under the One-System Rule (CAUSAL_MODE/REVISION_MODE/
LANGUAGE_MODE/MEMORY_MODE/PROCEDURE_MODE are named smells; three custom
bridges trigger ARCHITECTURE REVIEW). Rejected in favor of Proposal D (one
generic action channel, learner-authored policy).
5. Precomputing depth/grandparent triples for W9, or widening the fact store
to 72 slots so evictions stop: capacity or precomputation shoehorns. The
adversary's B4 kills the precomputation (no transfer to fresh ids without the
general procedure), and a bigger store only postpones the pathology. Rejected.

## Recommended next step (for the coordinator)

1. The frozen core analyzed here (freeze 87ac95d08) predates the CLA-2, CAM-1
(trial-based P-DEP), and ACT landings at tip d5984f313, which already move in
the directions of Proposals B and D. The natural next step is a re-freeze of
the integrated core, then a fresh Core Freeze battery on new sealed
adversarial worlds (the FW1-FW9 sealed pure-Zag evaluator assets), per Micah's
rerun philosophy: the same frozen-core discipline on fresh adversarial
worlds, not re-validation against the old W1-W9.
2. Proposals A and C remain the unlanded work: A is the top priority (every
other cluster's clean measurement depends on stable retention, and the
continuing-learner program cannot proceed on a substrate that cannot hold six
new facts); B/C convergence on one executable-graph substrate is the
architectural compression bet to preregister before building.
3. The W6 B4 protocol-interpretation call (adversary FAIL reading vs.
literalist PASS reading) remains banked for the research director; Proposal D
makes the distinction measurable in future runs (action contingent on
epistemic state or not), which dissolves the ambiguity rather than deciding
it by fiat.

## Process notes

- Step 0 toolchain guard: see NAMECHECK.md in this directory. `which python3`
returned /usr/bin/python3 (system runtime binary, not safely removable);
never invoked. No PROCESS-FAIL condition triggered.
- Git read-only throughout: no commits, no pushes, no branch switches.
- Sources were read, never modified. Design/paper work only.
- Dash check: this document uses colons and parentheses only; no em-dashes.
