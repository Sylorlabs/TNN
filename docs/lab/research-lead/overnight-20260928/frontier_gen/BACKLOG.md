# N1 Frontier Backlog (Living Document)

Maintained by N1, the Autonomous Frontier Generator. Seeded 2026-09-30.
This document is updated as research evolves. It is not a task list to
finish and stop; it is the queue that must never empty.

## Standing questions

1. Why would a rational user still choose an LLM instead of TNN today?
2. What important cognitive structure is still authored by researchers
   rather than TNN?

## Scoring rubric

Each question is scored 1 to 5 on seven dimensions. Total is out of 35.

- IMP: importance to general intelligence
- INF: expected information gain
- NOV: novelty relative to existing experiments
- FAL: ability to falsify a central TNN hypothesis
- L3P: potential for L3 evidence
- CMP: competitive relevance against LLMs
- INT: integration leverage toward one continuing learner

## Backlog

### Q1: Prediction-error program synthesis (invert the substrate, do not search it)

Problem: GENEXEC2 P1 beam search fails because sparse exact-match scoring
prunes solution prefixes before full programs are reached. Every fix so far
tunes the search; none questions the search.
Hypothesis: program search does not need a program-space fitness signal.
Learn an approximate forward model of the VM (predict stack effects from
op sequences on sample inputs), then synthesize by inverting the model:
given target behavior, solve for the op sequence in behavior space and
decode to program space.
Why existing TNN fails: all current synthesis searches program space
directly with task scores; nothing models the substrate itself.
Falsification: if model inversion cannot beat beam search on T0-T5 with
equal compute, the forward model adds no leverage and search-space design
is the real bottleneck.
Scores: IMP 4, INF 4, NOV 5, FAL 3, L3P 4, CMP 2, INT 2. Total 24.

### Q2: Compression-driven program invention (MDL, not search)

Problem: same P1 failure as Q1, approached from the opposite direction.
Hypothesis: treat a program as a compressed description of I/O pairs.
The learner already stores fragments; score candidate programs by
description length (program bytes plus residual errors) instead of by
task accuracy. Invention becomes compression, and the P7 persistence
policy ("schemas amortize") becomes the invention criterion: persist a
program only if it compresses.
Why existing TNN fails: invention and persistence are separate lanes;
nothing connects "what to invent" to "what is worth keeping."
Falsification: if MDL-ranked programs do not transfer better than
accuracy-ranked programs on held-out tasks, compression is not the
missing signal.
Scores: IMP 4, INF 4, NOV 5, FAL 4, L3P 5, CMP 2, INT 4. Total 28.

### Q3: Runtime operator recruitment (new opcodes as learner-created data)

Problem: Criterion C0-A demands that new semantics live in learner state
as data, with no dedicated source case. GENEXEC2 has the VM but no path
for the learner to extend the opcode set.
Hypothesis: give the learner an ALLOCATE_OP primitive whose operand is a
frozen subgraph of a solved program. The new opcode's semantics is the
subgraph bytes, stored in learner state, executed by the generic
interpreter. Then test C0-D: recruited operators must reduce examples or
search on later tasks.
Why existing TNN fails: the library stores fragments but cannot call
them as first-class ops with recruited semantics; CALL targets are still
researcher-shaped.
Falsification: preregister tasks where recruitment should help; if
recruited ops never beat inline code on cost, recruitment is ceremony.
Scores: IMP 5, INF 5, NOV 4, FAL 5, L3P 5, CMP 3, INT 3. Total 30.

### Q4: Learner-constructed explanatory variables (causal Stage 2)

Problem: DDES is Stage 1: authored hypothesis language plus guided
synthesis. F2's contextual law used a researcher-supplied K variable.
The deeper question from the mandate is unanswered: can the learner
construct the variables it needs to explain observations?
Hypothesis: worlds where the true cause is a hidden function of
observables (for example, cause = parity of two observables, or a
threshold on an unobserved accumulator the learner must posit). The
learner must propose a derived variable, test it by intervention, and
keep it only if it predicts better than observable-only hypotheses.
Why existing TNN fails: every causal lane starts from researcher-given
variables; variable invention has zero coverage.
Falsification: if the learner cannot beat an observable-only baseline
on hidden-variable worlds, variable construction is beyond the current
substrate and the substrate must change.
Scores: IMP 5, INF 5, NOV 4, FAL 5, L3P 4, CMP 3, INT 4. Total 30.

### Q5: DDES architecture review (is the representation wrong?)

Problem: DDESRT2 broke 4-variable generality: `obs = 4 - v_star` bakes a
3-variable assumption into "generic" synthesis. Repair history: t*=0
clamp, depth test, now a formula fix pending. Two repairs on
synthesize_plan plus one pending break is the treadmill pattern forming.
Hypothesis: analytic derivation from Bellman-Ford arrivals is the wrong
representation for experiment design; it keeps needing researcher patches
at each boundary (t*=0, depth, variable count).
Replacement candidates: (a) learner-grown observation table mapping
variable ids to observation actions, extended when new variables appear;
(b) plan synthesis as search in action space guided by the arrival
analysis, not a closed-form formula; (c) meta-learned designer: a policy
mapping hypothesis-difference vectors to plans, trained across worlds.
Why this matters: without the review, the lane becomes DDES v3, v4, v5.
Falsification: implement (a); if it handles 3-var, 4-var, and t*=0 with
no researcher formula edits, the formula representation was the problem.
Scores: IMP 4, INF 5, NOV 3, FAL 5, L3P 3, CMP 2, INT 4. Total 26.
Status: WATCH. Trigger the full review if the formula fix becomes repair
3 on the same function without new capability.

### Q6: Grounding-first segmentation (semantics before statistics)

Problem: DEVANG2 failed on design: bigram DP with zero counts defaults to
single segments. SEGREDESIGN tries TP-threshold, which is still
distributional statistics over the same impoverished signal.
Hypothesis: propose boundaries where grounding confidence changes. A
candidate segment is kept if it predicts observations or action outcomes
better than its parts; segmentation is validated by predictive utility,
not by transitional probability. Statistics-first and grounding-first
make different predictions on ambiguous forms resolved through grounding.
Why existing TNN fails: nine segmentation generations never used meaning
as the segmentation signal.
Falsification: on ambiguous forms where TP and grounding disagree, if
grounding-first does not segment better, meaning is not a usable early
signal and the failure is elsewhere (representation or memory).
Scores: IMP 4, INF 4, NOV 5, FAL 4, L3P 3, CMP 3, INT 3. Total 26.

### Q7: Shared causal substrate (not a port)

Problem: Integration Step B is blocked: the validated causal learner has
3 variables, episodes, entities, contests, and an 8940-byte workspace;
unified_learn has 2 variables and flat rules. A port would be a redesign.
Hypothesis: stop porting. Design the minimal shared causal substrate both
need: a variable-arity causal store with intervention records, from
which the 2-variable learner and the 3-variable learner are both
degenerate cases. The substrate is new architecture, not a merge.
Why existing TNN fails: every integration attempt moves bytes between
incompatible assumptions instead of redesigning the assumption.
Falsification: if no single substrate expresses both learners without
special cases, the two architectures are genuinely incompatible and one
must be retired by explicit supersession.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 2, CMP 2, INT 5. Total 24.

### Q8: Shared persistent state format (the bytes of one learner)

Problem: Integration Step D runs DEVINT1 then DEVINT2 sequentially in one
binary with separate state. That is composition, not one continuing
learner.
Hypothesis: specify the actual persistent byte layout that fact memory,
concept store, causal records, and procedure fragments all read and
write: one address space, one provenance log, one allocator. Then move
one mechanism at a time onto it. Incompatible assumptions found during
the move are architectural evidence, not bugs.
Why existing TNN fails: no two mechanisms share state; "integration" so
far means sequential execution.
Falsification: if the unified layout cannot express causal episodes and
lexicon entries without ballooning or special zones, a single flat store
is the wrong idea and the learner needs typed regions with a common
provenance protocol instead.
Scores: IMP 5, INF 4, NOV 3, FAL 4, L3P 3, CMP 2, INT 5. Total 26.

### Q9: Hypothesis-scale belief revision (the machine-native rematch)

Problem: SQLite killed the query-side machine-native claim. The
uncontested ground is revision: thousands of competing learned
hypotheses, each with exact provenance, re-ranked in milliseconds as
evidence arrives.
Hypothesis: maintain 10,000 competing hypotheses with per-hypothesis
evidence logs; measure revision latency and provenance exactness against
a SQLite baseline and a conventional algorithm on the same workload.
TNN wins only if revision is faster or more exact, not on queries.
Why existing TNN fails: no current mechanism maintains hypothesis
populations at scale; belief is single-hypothesis plus elimination.
Falsification: if SQLite matches revision latency, the machine-native
claim is dead on this axis too and the search moves on.
Scores: IMP 4, INF 4, NOV 4, FAL 4, L3P 2, CMP 4, INT 2. Total 24.

### Q10: P7 cross-world transfer (schemas amortize across worlds)

Problem: arena transfer (C12) is zero; F2 persists nothing across worlds.
The P7 policy was validated on synthetic threshold tasks only.
Hypothesis: run P7 across worlds with shared latent structure but
different surface variables. The policy should persist the re-fittable
schema, the gate should accept same-family worlds and reject others,
and refit cost should beat fresh learning. This is the transfer test the
"schemas amortize; instances do not" principle predicts.
Why existing TNN fails: transfer has never been tested with a
persistence policy in the loop; it is asserted, not measured.
Falsification: if gated schema reuse does not beat fresh learning on
total cost, the principle does not survive contact with real transfer.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 3, CMP 3, INT 5. Total 26.

### Q11: Autonomous goal execution (hundreds of actions, no resets)

Problem: the largest LLM-competitive gap with zero TNN coverage is
autonomous problem solving: goal plus unknown mechanics, no solution
sequence supplied.
Hypothesis: a sealed environment with unknown mechanics; the learner
must observe, hypothesize, experiment, plan, act, fail, revise, and
continue for hundreds of actions with no reset. Then a second
environment with related latent structure measures transfer.
Why existing TNN fails: every current lane is single-task with a fixed
protocol; nothing runs an open-ended act-learn loop.
Falsification: preregister a random-action baseline and a scripted-plan
baseline; if the learner does not beat both on goal achievement per
action, the loop is not doing cognitive work.
Scores: IMP 5, INF 5, NOV 4, FAL 4, L3P 3, CMP 5, INT 3. Total 29.

### Q12: Sealed benchmark readiness (convert PENDING into runnable)

Problem: the LLM baseline is PENDING with no credential, and waiting
stalls competitive evaluation.
Hypothesis: build everything that does not need the key now: the sealed
world suite, the scorer, the cost-accounting harness, the fair-access
protocol (memory and tools the LLM may use, priced). When a credential
arrives the run is mechanical. Also specify the no-key fallback: which
claims can be settled with local deterministic harnesses alone.
Why this matters: PENDING without a ready protocol decays into never.
Falsification: none needed; this is infrastructure. Kill it if the
protocol cannot be written without assuming a specific LLM's behavior.
Scores: IMP 3, INF 3, NOV 2, FAL 2, L3P 1, CMP 5, INT 2. Total 18.

### Q13: Learning when NOT to transfer (distrust as a cognitive structure)

Problem: P7's gate rejects different-family tasks, but the learner has no
explicit representation of distrust; every new task is approached as
potentially transferable.
Hypothesis: maintain a per-schema distrust prior updated by surprise
(large prediction error on gate-accepted tasks). Test on adversarial
families designed to punish transfer: near-family tasks with flipped
labels, where the schema looks applicable but is wrong.
Why existing TNN fails: meta-learning coverage is "when to transfer";
"when to refuse" has no mechanism.
Falsification: if a distrust prior does not reduce negative-transfer
cost versus the plain gate, distrust adds no value over rejection.
Scores: IMP 4, INF 4, NOV 4, FAL 4, L3P 2, CMP 3, INT 3. Total 24.

### Q14: The ignorance policy (one root cause for many failures)

Problem: white-box failure mining across lanes shows a pattern. F1 beam
search prunes prefixes with no evidence. DEVANG2 DP defaults to single
segments with zero counts. DDES's predictor assumed propagation semantics
it never verified. Each failure is "default behavior under zero
evidence" chosen by the researcher, invisible to the learner.
Hypothesis: make the ignorance policy explicit, auditable, and
learner-visible: a declared component stating what the system does with
no data (priors, defaults, tie-breaks). Then test whether varying only
the ignorance policy changes outcomes across lanes.
Why existing TNN fails: defaults are scattered through code; no lane
can answer "what do you assume when you know nothing."
Falsification: if swapping ignorance policies does not move F1 or
DEVANG2 results, the failures are not default-driven and the hypothesis
dies.
Scores: IMP 4, INF 5, NOV 5, FAL 4, L3P 3, CMP 2, INT 3. Total 26.

### Q15: Researcher-intelligence audit (the roadmap generator)

Problem: every frontier mechanism carries unlisted researcher
intelligence: representation, primitives, search strategy, objective,
candidate family, tie-breaks, thresholds, task boundaries, labels.
Hypothesis: systematically list these for DDES, F2, GENEXEC2, and
DEVANG, then rank which transfers to learner control would yield the
most information per implementation cost. The output is an architecture
roadmap ordered by expected L3 leverage, not another mechanism.
Why existing TNN fails: researcher authority is discussed per-lane but
never inventoried in one place; the next transfer target is chosen by
feel.
Falsification: if the audit cannot rank transfers (all look equal), the
dimensions are wrong and need re-derivation.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 3, CMP 2, INT 5. Total 25.

### Q16: Surprise test for the P7 policy

Problem: P7 was validated on cooperative synthetic tasks. Policies that
pass cooperative tests often fail adversarial ones.
Hypothesis: adversarial families: schemas that are valid but useless
(persist cost, no saving), instances disguised as schemas, and
tasks where the gate passes but refit is worse than fresh learning.
The policy must refuse or retire in each case.
Why existing TNN fails: no lane surprise-tests its own persistence
policy; P7's generality is asserted from 8 tasks.
Falsification: if P7 persists useless schemas or loses to fresh
learning on gate-passed tasks, the policy needs the tolerance-band
redesign its own design notes already predict.
Scores: IMP 3, INF 4, NOV 3, FAL 4, L3P 2, CMP 2, INT 2. Total 20.

### Q17: Arena gain audit (label every point 0.573 to 0.779)

Problem: the arena score rose 0.573 to 0.779 across composition,
conflict, inquiry, and causal additions. Per the arena improvement rule,
gains must be labeled BUGFIX, GENERIC-CAPABILITY, or ARENA-ADAPTER, and
only generic capability counts as research progress.
Hypothesis: audit each gain. The causal gain (C9) is suspect: the
contestant parses the `discrim|` question format because causal order is
unlearnable from the observations by permutation symmetry. That is
arguably ARENA-ADAPTER, not causal cognition.
Why this matters: if most gains are adapters, the competitive narrative
is inflated and research should stop chasing arena points.
Falsification: if the audit finds the gains are mostly generic, the
arena program is healthier than suspected.
Scores: IMP 3, INF 5, NOV 3, FAL 5, L3P 1, CMP 4, INT 2. Total 23.

### Q18: Priced post-deployment learning benchmark

Problem: competitive evaluation has no cost model both systems will
actually run.
Hypothesis: define the benchmark, not the run: thirteen priced tasks
(new fact learning, correction, delayed retention, contradiction,
paraphrase, composition, new vocabulary, causal learning, active
inquiry, procedure learning, representation invention, transfer,
autonomous execution), each with a scoring rule and a cost ledger
(examples, actions, compute, state bytes). Publish the harness so an
LLM run later is plug-and-play.
Why existing TNN fails: cost curves cover TNN internals only; there is
no shared ledger.
Falsification: if a task cannot be priced without favoring one
architecture, drop it rather than bend the ledger.
Scores: IMP 3, INF 3, NOV 2, FAL 2, L3P 1, CMP 5, INT 3. Total 19.

## Ranking (by total)

1. Q3 runtime operator recruitment: 30
2. Q4 learner-constructed explanatory variables: 30
3. Q11 autonomous goal execution: 29
4. Q2 compression-driven program invention: 28
5. Q5 DDES architecture review: 26
6. Q6 grounding-first segmentation: 26
7. Q8 shared persistent state format: 26
8. Q10 P7 cross-world transfer: 26
9. Q14 the ignorance policy: 26
10. Q15 researcher-intelligence audit: 25
11. Q1 prediction-error program synthesis: 24
12. Q7 shared causal substrate: 24
13. Q9 hypothesis-scale belief revision: 24
14. Q13 learning when NOT to transfer: 24
15. Q17 arena gain audit: 23
16. Q16 P7 surprise test: 20
17. Q18 priced post-deployment benchmark: 19
18. Q12 sealed benchmark readiness: 18

Backlog count: 18. Above the 15 minimum.

## Treadmill detector findings

Lineages scanned 2026-09-30:

- DDES (build, t*=0 repair, depth test, RT2 4-var break): one repair plus
  one pending break on synthesize_plan. Pattern forming, not yet three
  consecutive repairs. Verdict: WATCH. Q5 is the pre-armed review.
- FDCR unified1 through unified8: eight generations, each repairing
  adversary-found double-count and edge issues, adding fields (lifetime
  lists in verified-free regions), representation unchanged. Matches the
  treadmill pattern: 3+ consecutive generations repairing neighboring
  edge cases with no new capability. Verdict: TRIGGER ARCHITECTURE
  REVIEW. Question: is the flat concept store with counters the wrong
  representation? The kill battery already showed flat Jaccard clustering
  cannot do hierarchy, split, overlap, or composition. Three replacement
  hypotheses required before FDCR unified9: (a) hierarchical concept
  store with parent pointers and split operation; (b) graded membership
  with per-concept evidence vectors instead of binary counters;
  (c) concept algebra with explicit compose and divide operators as
  learner-invoked primitives.
- revise2 through revise11: ten generations, ended by impossibility
  proof. Historical treadmill example. Recorded so the pattern is
  recognized faster next time.
- seg1 through seg9 plus DEVANG1/2: nine generations. DEVANG2 proved the
  failure is design (bigram DP), not implementation. SEGREDESIGN tries
  TP-threshold, which is adjacent (still distributional). Verdict:
  WATCH. If TP-threshold fails, trigger review with Q6
  (grounding-first) as the replacement family.
- unified_learn 1 through 9: infrastructure treadmill, lane frozen.
  Noted only.

## Top unsolved problem: L3 executable semantics

Three structurally different replacement hypotheses (per the competing
architectures rule). These are not v3 to v4 to v5; they differ in what
the learner grows, compresses, or inverts.

- H1: Executable graph growth. The learner grows a persistent graph of
  operations; new nodes are new semantics; the generic interpreter walks
  the graph. Variable-sized by construction (C0-B), semantics in
  learner-created edges (C0-A). Discriminating test: freeze, then seal a
  family requiring a form the graph has never grown (for example,
  recursion); the learner must grow it without researcher graph
  operators beyond allocate-node and connect-node.
- H2: Compression-recruited operators. New operators are recruited only
  when they compress the description of solved tasks; a recruited
  operator's semantics is the frozen subgraph it abbreviates. Reuse is
  measured by compression gain, which doubles as the C0-D metric.
  Discriminating test: tasks where the compressible regularity is
  hidden across task boundaries; recruitment must find it anyway.
- H3: Demonstration inversion. Learn a forward model of the substrate,
  then synthesize programs by inverting the model: search happens in
  behavior space, decoding to program space only at the end. No
  program-space fitness function exists to prune prefixes, which
  sidesteps the P1 failure mode structurally rather than by tuning.
  Discriminating test: T0-T5 with the forward model trained only on
  random programs, never on task solutions.

Kill rule: a hypothesis dies if its discriminating test fails twice
under independent preregistration, or if its implementation requires a
new dedicated semantic case in source (C0-A violation).

## Launch queue (recommended, in rank order)

1. Q3: runtime operator recruitment. Needs a builder with prereg before
   implementation. Highest L3 leverage.
2. Q4: learner-constructed explanatory variables. Needs a builder plus an
   independent world designer (sealed hidden-variable worlds).
3. Q11: autonomous goal execution. Needs a builder plus an environment
   designer; longest-running worker, start early.
4. Q17: arena gain audit. Cheap, high falsification value; an auditor
   can do it without new code.
5. Q15: researcher-intelligence audit. Produces the ranked roadmap that
   re-prioritizes this backlog.

## Update log

- 2026-09-30: backlog seeded with 18 questions. Treadmill review
  triggered for FDCR unified lineage. DDES and segmentation lanes on
  watch. Top problem: L3 executable semantics with H1/H2/H3.
