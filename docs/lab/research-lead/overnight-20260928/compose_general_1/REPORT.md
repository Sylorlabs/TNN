# COMPOSE-GENERAL-1 REPORT: Three Competing General Composition Hypotheses for the Diamond/Fan-Out Failure

Date: 2026-10-03. Worker: COMPOSE-GENERAL-1.
Lane: `docs/lab/research-lead/overnight-20260928/compose_general_1/`.
Task type: DESIGN ONLY. No implementation, no runs, no binaries.

## 0. Status: nothing in this report is tested

This report contains zero experimental results. Every mechanism described
below is a reasoned design, not a built system. Every prediction is a
falsifiable claim awaiting a preregistered implementation, not an observed
outcome. No verdict (PASS/FAIL/BUILD-PASS/INFORMATIVE-FAIL) is claimed for
any hypothesis. Section 2 separates, line by line, what is TESTED (prior
lane evidence this design relies on, with ledger citations) from what is
REASONED (everything in Sections 4 through 8, untested by construction).

No toolchain was invoked: there is no code, so there is nothing for the
toolchain guard to cover. A future implementation worker must follow the
standing guard (safebin, pure Zag, NAMECHECK.md Step 0) before building.

## 1. Task and architectural context

Micah's 2026-10-03 clarification overrides prior framing: CROSS-DOMAIN IS
NOT A MODE. The final goal is GENERAL LEARNED-STRUCTURE COMPOSITION, not
"cross-domain composition." The diamond/fan-out failure recorded by
COMPOSE-PAIR6-ADV must trigger competing GENERAL hypotheses, not a diamond
handler. Domain-blindness is required of every mechanism: the standard is
"would the same frozen architecture still know how to learn/use this if
humans had never named the domain or capability?"

This worker's assignment: design three structurally different, general,
domain-blind, falsifiable composition hypotheses that address the diamond
failure generally. Implementation is explicitly out of scope; this report
is the complete deliverable.

## 2. Tested vs reasoned

### 2.1 TESTED (prior lane evidence; relied on, not re-proven)

- T1. U (unified behavior-contract operation: trial space {singles,
  ordered pairs}, 1-in/1-out contracts, predicted outmask/inmask
  handshake) is defeated by fan-out: COMPOSE-PAIR6-ADV, ledger C380,
  INFORMATIVE-FAIL. UNI-D exhausts its trial space on Q1 (ANS=-2,
  TRIES=14, WIDEN=1). The boundary is real, not a teaching artifact.
- T2. A general extension of U's principles solves the diamond with no
  new mechanism: GEN (iterated n-ary application over a value pool;
  the fork emerges because a computed value stays in the pool and is
  consumable by any MAP), same lane, C380, K3/K4/K5 PASS (Q1 ANS=5
  TRIES=8; collapse battery regresses clean; Q2 misleading-teaching
  solved via generalized widening).
- T3. Unmodified frozen GEN covers fan-in, DAG-4, chain-3, and partial
  applicability: ledger C402, GEN-GENERALITY K1-K7 PASS. The diamond
  failure was a trial-space limit, not a shape patch.
- T4. U is retired as a separate mechanism (ledger C413); GEN, LCONT,
  and FC are unified into one 5-operation contract module
  (induct/check/grow/invalidate/revise), ledger C424, SUBSUMES, 7/7
  bars, zero scenario branches. The contract module is the live
  general mechanism for learned-structure (MAP/contract) composition.
- T5. Cycles are handled inside GEN's lineage by sequences plus learned
  halting across five families (fixpoint C414, generalized C420,
  oscillatory C425, convergent C428, feedback C430/C432). This is the
  standing bar any new composition hypothesis must eventually meet or
  explicitly bound.
- T6. Procedure-body composition over learner-owned procedures
  (COGOPS: C417 2-way, C422 3-way, C433 diamond via generic
  multi-source fan-in) is demonstrated but has no subsumption test
  against the contract module (synthesis gap P0). The hypotheses in
  this report compete at the learned-structure level (GEN's level),
  not at the procedure-body level.
- T7. Domain-blindness protocol exists and passed for U-era
  composition: identifier relabel (C398), relation-label relabel
  (C399 second assignment), joint relation+node relabel (C409 second
  assignment), node-id independence (C403 second assignment). The
  blind battery is the template referenced in Section 8.
- T8. Partial applicability via sub-node DAG sharing is demonstrated
  by XP-DAGFAN-4 (branch lane-xdagfan2-20261003, PASS 22/22, 3/3
  byte-identical): a composite's part (t=241) recombines with a
  different partner without reusing the whole parent.
- T9. Frozen GEN has a round cap of 6 and a pool cap of 64
  (PAIR6 PREREG Section 4; REPORT.md open questions note the caps are
  untested boundaries). A chain longer than 6 links exceeds the
  frozen round cap.
- T10. All MAPs in the PAIR6 worlds are pure (REPORT.md boundary B3
  discussion). No tested result covers side-effecting MAPs under any
  composition mechanism.

### 2.2 REASONED (this report; untested by construction)

- R1. The three mechanism designs in Sections 4, 5, 6.
- R2. Every numbered prediction F-A1 through F-C4 and every entry of
  the discrimination matrix in Section 7.
- R3. The domain-blindness arguments in Section 8 (the arguments are
  reasoned from the designs; the blind battery itself is proposed,
  not run).
- R4. The regression-ground and next-step sketches in Sections 9
  and 11.

## 3. The composition arc as read

Pipeline composition was solved by U (5 pairs, C368), then U was
defeated by the diamond: one intermediate feeding two consumers plus
a 2-input join is outside U's {singles, ordered pairs} trial space and
outside its 1-in/1-out execution (C380 INFORMATIVE-FAIL). GEN
generalized the trial space to rounds over a value pool with
observed-kind admission, and the fork emerged with no diamond-specific
code (C380 K3-K5). Frozen GEN then covered fan-in, DAG-4, chain-3,
and partial applicability unchanged (C402), absorbed cycles via
sequences plus learned halting (C414-C432), and was unified with
LCONT and FC into the 5-op contract module (C424). In parallel,
COGOPS demonstrated procedure-body composition including diamond via
generic multi-source fan-in (C433), and XP-DAGFAN-4 demonstrated
sub-node DAG sharing for partial applicability.

The open architectural question this report addresses: GEN is an
existence proof that a general extension covers the diamond, but it
is one point in a space of possible general mechanisms. A forward,
eager, round-based value-graph expansion is not the only general way
to compose learned structures. The three hypotheses below are three
other points in that space, designed to be mutually discriminating:
there exist shared worlds on which they make different, measurable,
preregisterable predictions (Section 7). None contains a diamond
handler, a shape template, a mode, or a domain-specific branch. In
each, the fork (one intermediate, two consumers) emerges from the
general rule, exactly as the task requires.

Frozen reference world used for walk-throughs (from the PAIR6
PREREG, unchanged): X = WALK(91) worker->team NODE->NODE; Y =
COUNT(92) team->pending NODE->NUM; W = COUNT(94) team->completed
NODE->NUM; G = ADD2 (NUM,NUM)->NUM. Q1: s=202, kin={NODE},
kout={NUM}, expected 5, via X(202)=211, Y(211)=3, W(211)=2,
G(3,2)=5.

## 4. Hypothesis A: BACKCHAIN (goal-directed regressive decomposition)

### 4.1 One-line statement

Compose by regressing the goal backward through inverse-applicable
structures: maintain open needs (required kind, derivable from the
input), discharge each need by any structure whose learned output
contract matches, and memoize solved needs so shared sub-derivations
are built and executed once.

### 4.2 General principle

Forward search enumerates what structures CAN do from the input;
backward search enumerates what the goal NEEDS and finds structures
that provide it. The search state is a set of needs, not a pool of
values. A need is the pair (K, s): "a value of kind-set K derivable
from input s." The initial need is (kout, s). This is the classic
regression idea, restricted to learned kind-set contracts and opaque
structure identifiers, with end-to-end verification retained from
U/GEN.

### 4.3 Mechanism sketch (implementable)

State: an open-need stack; a memo table mapping each need to its
lazily-enumerated solution list (each solution: a derivation tree
plus its executed value, or -2 discarded); a tried-set of
(need, producer-id, solution-index) for determinism.

Goal (s, kin, kout):
1. Admit iff kind(s) is compatible with kin (same k_has convention
   as U/GEN; empty = compatible with all). Else ANS=-2.
2. Open need N0 = (kout, s). Push.
3. Repeat: take the deepest open need N = (K, s). Candidate
   producers: MAPs in id order whose outmask is compatible with K.
   Skip (N, producer) already tried. For producer m:
   - 1-input: sub-need (inmask(m), s). 2-input: sub-needs
     (inmask1(m), s) and (inmask2(m), s).
   - A sub-need closes directly by s when kind(s) is compatible
     with its kind (leaf derivation), or by regression through its
     own producers (pushed as a new open need).
   - Loop guard: a sub-need identical to a need already on the open
     stack fails that producer choice immediately (no infinite
     regress). A sub-need with memoized solutions reuses them; when
     the reused solution fails end-to-end downstream, the next
     memoized alternative is drawn (alternatives are enumerated
     lazily, not just the first).
4. When every sub-need of a producer choice is closed, the
   derivation tree is complete: execute it bottom-up exactly once
   and verify end-to-end (value == expected, as in U/GEN).
5. On end-to-end failure, backtrack chronologically to the next
   untried (need, producer, alternative) choice, deterministic in
   id order.
6. When all kind-compatible producers for all open needs are
   exhausted without success: fire ONE admission-relaxed pass
   (producer matching ignores kind compatibility; the WIDEN analog),
   triggered solely by observed exhaustive failure, exactly once.
   Then report ANS=-2 on continued failure.
7. On success, record the whole derivation closure with
   observe/observe2 on actual input/output values (same
   provenance-based recording spirit as GEN): contracts grow from
   the successful composition.

### 4.4 Diamond walk-through (frozen Q1)

Goal (202, {NODE}, {NUM}). N0 = ({NUM}, 202). Producers of {NUM} in
id order: Y, W, G.
- Y: sub-need ({NODE}, 202). Closes by s directly: derivation
  Y(202), executes -2, discarded as a solution (tried, counted).
  Backtrack within the sub-need: producer X for ({NODE}, 202):
  sub-need ({NODE}, 202) for X's input closes by s. Derivation
  Y(X(202)): executes X(202)=211 (memoized as the solution of need
  ({NODE}, 202) via X), Y(211)=3. End-to-end 3 != 5: backtrack.
- W: symmetric: W(202) -2; W(X(202)) = 2 != 5: backtrack. The need
  ({NODE}, 202) solution X(202)=211 is reused from memo, not
  recomputed.
- G (2-input): sub-needs A = ({NUM}, 202), B = ({NUM}, 202).
  Solve A: producers Y, W, G in order. Y(202) -2; Y(X(202)) = 3:
  first solution of need ({NUM}, 202), memoized. Solve B, the SAME
  need: reuse memoized solutions first: Y(X(202)) = 3, giving
  derivation G(3,3) = 6 != 5: backtrack within B to the next
  alternative of need ({NUM}, 202): W(202) -2; W(X(202)) = 2.
  Derivation G(Y(X(202)), W(X(202))) with the shared memoized
  X(202)=211: executes G(3,2) = 5. End-to-end success.
- Recording closure: observe2(G,3,2,5), observe(Y,211,3),
  observe(W,211,2), observe(X,202,211), as in GEN.

The fork emerges from need memoization: the need ({NODE}, 202) is
solved once, and both legs of G consume that one solution. No
diamond-specific code exists anywhere in the sketch.

### 4.5 Generality argument

Chains: a chain is regression depth n; each need has one natural
producer. Fan-in: a 2-input producer creates two sub-needs, as in
the walk-through. DAGs: any shared sub-need is solved once by memo,
regardless of how many parents consume it; 3/5/10+ structure
combinations are deeper/wider need trees, no new rule. N-ary joins:
arity is a per-structure property (as in GEN's class convention);
each input position becomes one sub-need. Multiple outputs: a
structure with a multi-valued output closes several needs at once
(one application, several kind requirements). Partial
applicability: a sub-need's solution is reusable by any later goal
whose needs include it, without reusing the whole parent
derivation (same reuse shape XP-DAGFAN-4 demonstrated for
xhier_compose, here at the need level). Cycles: BOUND (see 4.8).

### 4.6 Structural difference

Versus GEN/contract-module: GEN expands FORWARD and EAGERLY over a
value pool in rounds, executing every admitted application whether
or not it can lead to the goal; BACKCHAIN expands BACKWARD from the
goal and executes only complete candidate derivations, never
speculative intermediate applications. GEN needs round and pool
caps to terminate; BACKCHAIN needs only a depth bound and the
stack-loop guard. Versus Hypothesis B: BACKCHAIN interleaves search
and execution (a derivation is executed as soon as it is complete,
and failure drives backtracking); B separates them into two phases.
Versus Hypothesis C: BACKCHAIN's procedure is fixed and memoryless;
every goal is solved from scratch, and nothing about the search
strategy changes with experience.

### 4.7 Falsifiable predictions

- F-A1 (cap independence, discriminating vs frozen GEN): a 10-link
  linear chain world (fresh relations, all contracts taught).
  Frozen GEN cannot solve it without changing its frozen round cap
  of 6 (T9). BACKCHAIN predicts ANS correct with only a frozen
  depth bound (e.g., 16), no round or pool caps involved.
  Falsified if BACKCHAIN also needs a cap change or fails.
- F-A2 (distractor discipline): diamond world plus D distractor
  MAPs with in{NUM}, out{NODE} and no facts. Each distractor is a
  candidate producer of the ({NODE}, 202) need, but its input need
  ({NUM}, 202) is already on the open stack, so the stack-loop
  guard fails it immediately: predict exactly D wasted tries, one
  per distractor. Frozen GEN predicts ~2D wasted tries (round-2
  applications on the NUM values 3 and 2). Falsified if either
  count differs (exact accounting fixed at preregistration).
- F-A3 (sharing integrity): on frozen Q1, exec_count(X) == 1 over
  the entire BACKCHAIN run (need memoization, never recomputed).
  Falsified if X executes 2 or more times.
- F-A4 (goal-kind gating integrity): Q1 with kout deliberately
  wrong ({NODE} instead of {NUM}): BACKCHAIN must exhaust
  kind-compatible producers, fire WIDEN=1 exactly once, and only
  then solve via the relaxed pass. Falsified if it solves with
  WIDEN=0 (the goal-kind gate was bypassed) or fails to solve.

### 4.8 Honest bounds

BACKCHAIN as sketched covers acyclic composition only. Fixpoint and
feedback cycles (T5) need an explicit iterate-with-halt construct in
the derivation language, which is not designed here; until it is,
cycles are a declared BOUND, and GEN's cycle envelope stands
unmatched. BACKCHAIN's worst case is exponential in producer
fan-out times depth (same as any chronological backtracker); the
stack-loop guard prevents infinite regress but not combinatorial
blowup, so a frozen depth bound and a tried-set cap are required
(the preregistration must freeze them). Side-effecting MAPs are out
of scope (T10): re-execution of a derivation during backtracking
assumes purity.

## 5. Hypothesis B: SUSPEND (two-phase lazy dataflow: assemble, then evaluate)

### 5.1 One-line statement

Separate composition into ASSEMBLY (build a suspended computation
DAG of hash-consed thunks by contract matching, executing nothing)
and EVALUATION (demand the root thunk; thunks evaluate inputs on
demand and memoize by thunk identity), so the composite is a
persistent, inspectable, revisable first-class structure and shared
subcomputations evaluate exactly once.

### 5.2 General principle

A composition can be a THING before it is a RUN. In GEN the
composite exists only implicitly as the successful path through the
value pool; in BACKCHAIN it exists transiently as search state.
SUSPEND reifies it: the assembled DAG persists in learner state
across queries, can be inspected, rebound to new inputs, and revised
by sub-thunk substitution with memo invalidation limited to the
ancestors of the change. Sharing is by thunk identity (pointer
equality after hash-consing), not by value equality (GEN's pool) or
need equality (BACKCHAIN's memo). Evaluation is lazy and
demand-driven: nothing executes until the root is demanded, and then
only the thunks on the demand path execute.

### 5.3 Mechanism sketch (implementable)

State: a thunk table (id -> (map-id, input-thunk-ids, status,
memoized value)); an intern table mapping (map-id, input-thunk-ids)
to the canonical thunk id (hash-consing: syntactically identical
applications are the same thunk); a composite store mapping goal
signatures to root thunk ids (persistent learner state).

Phase 1, ASSEMBLE(goal (s, kin, kout)): purely symbolic, zero
execution. Regress needs exactly as in Hypothesis A Section 4.3,
but instead of executing a completed derivation, intern it as
thunks: leaf const-thunk C(s); app-thunk intern(m, input-ids).
Candidate DAGs are enumerated in a frozen deterministic order
(producer id order, increasing size); the FIRST candidate whose
assembly completes is evaluated. (Stated openly: the assembly
search strategy is regressive like BACKCHAIN; SUSPEND's novel
architectural commitments are the phase split, the persistent
composite, and demand evaluation, and the differential predictions
below test exactly those commitments, not the search order.)

Phase 2, EVALUATE(root): demand-driven with identity memoization.
demand(t): if memo(t) present, return it. If t is on the evaluation
stack, fail the candidate (loop guard; cycles need the iterate
construct, BOUND as in 4.8). Else evaluate input thunks on demand
in input order, apply the MAP once, memoize, return. After
evaluation, verify end-to-end (value == expected). On failure,
return to assembly for the next candidate DAG.

REVISE(path, new-subthunk): replace the thunk at path with a
newly assembled sub-thunk, invalidate memos on the ancestor path
only, re-evaluate on demand. REBIND(new-s): replace the const-thunk
input, clear all memos, re-evaluate: zero assembly.

Success recording: as in GEN/BACKCHAIN, observe/observe2 over the
evaluated applications with actual values.

### 5.4 Diamond walk-through (frozen Q1)

Assembly (no execution): candidates enumerated; early candidates
(Y(C202)), (W(C202)), (Y(X(C202))), (W(X(C202))) assemble and are
evaluated to -2, 3, 2 respectively, failing end-to-end. The
successful candidate: T3 = intern(X, [C202]); T1 = intern(Y, [T3]);
T2 = intern(W, [T3]) (hash-cons: the second X(C202) application
returns the SAME thunk id T3, so T1 and T2 share one node);
T0 = intern(G, [T1, T2]). Evaluation on demand: demand(T0) needs
T1: demand(T1) needs T3: X(202)=211, memo(T3)=211; Y(211)=3,
memo(T1)=3. demand(T2): needs T3: memo hit, no recompute;
W(211)=2, memo(T2)=2. G(3,2)=5. End-to-end success. The DAG
{T0,T1,T2,T3,C202} persists in the composite store.

The fork is thunk identity: two consumers hold the same thunk id,
so one evaluation serves both. No diamond-specific code.

### 5.5 Generality argument

Chains, fan-in, n-ary joins, and DAGs are all DAGs; assembly builds
them by the same rule and hash-consing shares every repeated
sub-application automatically, however many consumers share it
(2, 3, 10+). Multiple outputs: tuple-valued thunks with projection
thunks. Partial applicability: sub-thunks persist across goals, so
a later goal whose assembly needs X(C(s)) reuses thunk T3's shape
(rebound) without rebuilding that sub-DAG; this is XP-DAGFAN-4's
sub-node sharing expressed as thunk reuse. Cycles: BOUND (loop
guard fails them; the iterate construct is future work, as in 4.8).

### 5.6 Structural difference

Versus BACKCHAIN: BACKCHAIN interleaves search and execution and
its derivations are transient; SUSPEND never executes during
assembly, and the composite outlives the query that built it. The
observable consequence is F-B1/F-B2, which BACKCHAIN cannot exhibit
by construction. Versus GEN: GEN executes eagerly in rounds over
concrete values (X runs twice on Q1: round 1 on 202, round 2 on
211); SUSPEND executes lazily on demand (X runs once). Versus
Hypothesis C: SUSPEND's assembly procedure is fixed; the composite
is stored, but the STRATEGY that builds composites never changes.
C stores composites too, but its retrieval/adaptation/reinforcement
loop means its behavior on the tenth goal differs from its behavior
on the first; SUSPEND's does not.

### 5.7 Falsifiable predictions

- F-B1 (zero-assembly reuse, the key architectural
  discriminator): after Q1 success, pose Q1b: same contracts and
  goal shape, new input s=204 with fresh facts X(204)=212,
  Y(212)=2, W(212)=1, G(2,1)=3, expected 3. Predict: assembly steps
  on Q1b = 0 (REBIND only), total MAP executions = 4 (X, Y, W, G
  once each), ANS=3. BACKCHAIN and GEN predict a full re-search
  (tries comparable to Q1). Falsified if any assembly search runs
  on Q1b.
- F-B2 (surgical revision): after Q1 success, retract W's 94-facts
  (W now returns -2 everywhere) and add alternative 1-input MAP V
  (in{1}, out{2}) with V(211)=2. Predict: SUSPEND re-assembles
  ONLY the sub-need ({NUM}, 202) for G's second input, substitutes
  T2' = intern(V, [T3]), invalidates memos on {T2', T0} only, and
  re-evaluates: X and Y execute 0 additional times (memo hits on
  T3, T1). Falsified if X or Y re-execute, or if revision
  re-assembles from the root.
- F-B3 (single evaluation): on frozen Q1, exec_count(X) == 1 and
  total executions on the success path == 4 (X, Y, W, G once
  each). Falsified if any MAP on the success path executes twice.
- F-B4 (phase-separation integrity): instrument the build: zero
  MAP executions occur before the first candidate DAG is fully
  assembled. Falsified if any execution happens during assembly
  (that would be collapse into BACKCHAIN, and the hypothesis's
  central claim would be void).

### 5.8 Honest bounds

SUSPEND's assembly search has the same worst-case branching as
BACKCHAIN's; laziness saves re-execution, not search. It does NOT
predict fewer assembly trials than BACKCHAIN, only fewer
executions and the persistence/revision behaviors. The intern
table is unbounded in the sketch; a frozen implementation must
bound it (preregistration fixes the bound). Cycles are BOUND as in
4.8. Non-pure MAPs break identity memoization outright (a thunk
evaluated once is assumed to return the same value forever);
SUSPEND is undefined for effectful MAPs unless an ordering/purity
discipline is added, which is not designed here. All PAIR6 MAPs
are pure (T10), so the Q1/Q2 worlds are in scope.

## 6. Hypothesis C: LEARN-COMPOSE (learner-owned composition policy)

### 6.1 One-line statement

There is no fixed composition search procedure: the learner keeps a
composition memory of (goal-signature, composite program, outcome
history) entries, retrieves and adapts stored composites for new
goals, and revises them with general operators on failure, so
trials-to-solution DECREASES with compositional experience and
composites transfer across worlds.

### 6.2 General principle

BACKCHAIN, SUSPEND, and GEN are all fixed procedures: the
researcher writes the search, the learner only fills in contracts.
LEARN-COMPOSE moves the composition strategy itself into learner
state. What the learner owns: which composites to try first for
which goal shapes, how to adapt a stored composite to a new
inventory, and what to change when a composite fails. What the
researcher provides: a small frozen set of GENERAL revision
operators defined purely over contracts (append, prepend,
substitute, fork-leg, join-leg, drop-leg), a goal-signature
function over kind sets and contract multisets, and end-to-end
verification. The diamond is then solved the second time cheaply,
not the first time cleverly; the claim is about the learning curve,
transfer, and revision, not about first-encounter efficiency.

The operators, stated to show none is diamond-specific:
- APPEND(m)/PREPEND(m): extend the composite's frontier with a
  contract-compatible structure.
- SUBST(a, b): replace structure a with contract-compatible b.
- FORK(n): share derivation node n's output with a second
  consumer position (general: applies whenever an intermediate's
  kind admits two consumers; the diamond is one instance).
- JOIN(m2): combine two frontier values with 2-input structure m2
  (general: any arity-2 combination).
- DROP(n): remove a leg.
- RETRY-WIDEN: one admission-relaxed re-attempt after exhaustive
  failure (the WIDEN analog).
No operator mentions diamonds, fan-out, chains, or any shape.

### 6.3 Mechanism sketch (implementable)

Learner state (persistent across goals and worlds): composition
memory entries e = (sig, composite, successes, failures,
last-revised), where sig = (kin, kout, contract-sketch), and
contract-sketch = the inventory's multiset of
(arity, inmask-set, outmask-set) triples, sorted (order-invariant,
label-free). A composite = a DAG of (map-id, input positions), i.e.,
a stored program over opaque structure ids.

Per goal (s, kin, kout):
1. Compute sig. Retrieve the entry with the most similar sig
   (frozen similarity: exact match > sketch-subset/superset >
   kind-match-only > none).
2. If none: cold-start = bounded blind search over the operators
   (frozen budget, e.g., 40 tries). Expected to be WORSE than GEN
   on first encounter; this is predicted, not hidden.
3. Adapt: SUBST each stored map-id with an inventory MAP whose
   contracts are compatible (kind-set matching as in U/GEN).
4. Execute the composite; verify end-to-end (value == expected).
5. Success: successes++, grow contracts via observe/observe2 on
   actual values (as in GEN).
6. Failure: apply revision operators in frozen order, bounded
   tries each; execute and verify each revision. On success, store
   as a new (or revised) entry. On exhaustive failure, record
   negative evidence: failures++ on the tried entries; the failing
   composite is marked failed, never persisted as a success.
7. Similarity and operator order are frozen at preregistration;
   the MEMORY (which composites, which revisions worked) is
   learner-owned and grows.

### 6.4 Diamond walk-through (first encounter and second)

First diamond goal ever (cold): sig has no match. Cold search tries
chain composites: [X,Y] executes 3 != 5 (failure recorded);
[X,W] executes 2 != 5 (failure recorded). Revision: FORK on X's
output node (its kind {NODE} admits Y and W as consumers), then
JOIN(G) over the two legs: composite executes G(3,2)=5. Stored
under sig({NODE},{NUM},sketch-with-2input).

Second diamond goal (fresh relations, same shape): sig matches the
stored entry. Adapt by SUBST to the new inventory's MAPs
(contract-compatible). Execute: success in a handful of tries, no
search over chains, no distractor trials. Trials-to-solution drops.

The fork and join are general operators applied by the learner on
the basis of recorded failure, not researcher-supplied
diamond handling.

### 6.5 Generality argument

The composite representation is a DAG, so chains, fan-in, fan-out,
DAGs, n-ary joins, and multi-leg combinations are all expressible;
the operators transform DAGs generally. Partial applicability:
retrieve a stored composite and SUBST/DROP legs to fit the new
goal (this is L2 adaptive reuse: truncate, substitute, specialize
as memory operations). Multi-input/output: composites with several
frontier values. 3/5/10+ structures: larger stored DAGs; the
memory, not the procedure, scales. Cycles: BOUND (the operator set
has no iterate construct; same declared gap as A and B).

### 6.6 Structural difference

Versus BACKCHAIN and SUSPEND: those are fixed procedures whose
behavior on the tenth goal is identical to the first; LEARN-COMPOSE
has no fixed search procedure at all, only retrieval, adaptation,
and reinforcement, so its behavior CHANGES with experience. Versus
GEN: GEN is memoryless forward search; LEARN-COMPOSE's first
encounter is deliberately worse than GEN (cold-start blind search),
and its claim is that the second and third encounters are better.
This inverts the usual evaluation: the hypothesis is confirmed by
a DECREASING trials curve, not by a low absolute trial count. It is
also the only hypothesis of the three that addresses the synthesis
gaps P1 (composite revision: operators revise stored composites)
and the L2 adaptive-reuse frontier directly.

### 6.7 Falsifiable predictions

- F-C1 (learning curve, the central claim): three-goal sequence
  with equal inventory size: diamond world-1 (fresh relations),
  diamond world-2 (fresh relations, same shape), fan-in world-3
  (fresh relations). Predict trials T1 > T2 > T3, strictly
  decreasing. GEN/contract-module predicts flat (T1 approx T2
  approx T3, no memory). Falsified if T3 >= T1.
- F-C2 (revision beats re-search): after diamond success in
  world-1, break W (retract 94-facts) and add V (in{1}, out{2},
  V(211)=2) as in F-B2. Predict LEARN-COMPOSE's SUBST revision
  solves in fewer tries than GEN's from-scratch re-solve on the
  same broken world, and in fewer tries than its own cold T1.
  Falsified otherwise.
- F-C3 (negative evidence is recorded): adversarial goal whose
  sig matches the stored diamond entry but whose semantics differ
  (e.g., the 2-input structure computes SUB: G'(3,2)=1, expected
  1... or expected answer differs from the composite's output).
  Predict: the learner executes the stored composite,
  end-to-end verification FAILS, entry.failures increments, the
  entry is NOT recorded as a success, and a revision is attempted.
  Falsified if the learner reports success without verification
  passing, or reuses the entry without recording the failure
  (silent negative transfer).
- F-C4 (signature blindness): the C398/C399/C409 relabel protocol
  applied to relations, node ids, and kind polarity: retrieval
  decisions and outcomes byte-identical. Falsified by any
  byte difference (the signature smuggled a label).

### 6.8 Honest bounds

LEARN-COMPOSE is an L2 claim, not L3: the revision operators and
the signature function are researcher-provided generic machinery;
what the learner creates is the composite programs and the
retrieval preferences. Cold-start is predicted WORSE than GEN;
any evaluation that only measures first-encounter trials will
(misleadingly) favor GEN, so the preregistration must measure the
curve, not the intercept. The similarity function is a
researcher choice that could smuggle bias; it must be frozen,
simple (kind sets plus contract-sketch multiset, nothing else),
and its exact form committed before any run. Transfer is claimed
across worlds with the same SHAPE; transfer across shapes (diamond
memory helping a cycle goal) is not claimed. As with A and B:
cycles BOUND, purity assumed (T10).

## 7. Discrimination matrix: shared worlds, differential predictions

All five worlds are implementable in pure Zag on the PAIR6-style
substrate. Predictions are preregisterable as stated; exact TRIES
accounting is fixed at preregistration time, but the ORDERINGS and
equalities below are the falsifiable content.

D1 (deep chain): 10-link linear chain, fresh relations, all
contracts taught. Frozen GEN: FAIL (round cap 6, T9). A: PASS, no
cap change (F-A1). B: PASS (assembly depth 10). C: PASS, cold and
slow (worse than A/B on first encounter, predicted).

D2 (re-query, new input): Q1b after Q1 (Section 5.7: s=204,
expected 3). GEN: full re-search, tries approx Q1. A: full
re-search (memoryless). B: 0 assembly steps, 4 executions (F-B1).
C: retrieve plus adapt, a handful of tries (fewer than A/GEN,
more than B's zero).

D3 (broken leg): post-Q1-success, W's facts retracted, V added
(V(211)=2). GEN: from-scratch re-solve. A: full backward
re-search, tries approx Q1. B: localized sub-thunk re-assembly;
X and Y execute 0 additional times (F-B2). C: SUBST revision;
tries fewer than its own T1 and fewer than GEN's re-solve
(F-C2). B vs C discriminator: B's trace shows memo hits on
unchanged thunks; C's trace shows a memory-retrieval plus
operator application.

D4 (three-goal learning sequence): diamond world-1, diamond
world-2 (fresh relations), fan-in world-3; equal inventory size.
GEN: flat trials. A: flat trials. B: flat assembly per new shape
(one assembly each). C: strictly decreasing trials T1 > T2 > T3
(F-C1). This world discriminates C from everything else.

D5 (distractor-heavy diamond): Q1 plus D NUM->NODE distractor
MAPs (in{NUM}, out{NODE}, no facts). GEN: ~2D wasted tries
(round-2 applications on values 3 and 2). A: exactly D wasted
tries, one per distractor, each failed immediately by the
stack-loop guard (F-A2). B: D assembly steps, 0 extra executions
(assembly is symbolic). C (after one success): ~0 distractor
tries (retrieved composite never mentions them); C cold-start on
D5 is predicted bad (stated in 6.8).

Summary of what each world separates:
- D1 separates {A, B, C} from frozen GEN (cap independence).
- D2 separates B (persistent composite, zero re-assembly) from
  A/GEN, and C (retrieval) from A/GEN.
- D3 separates B (surgical, memo-preserving) and C (operator
  revision) from A/GEN (full re-search); B vs C by mechanism
  trace.
- D4 separates C (learning curve) from all fixed procedures.
- D5 separates forward-eager (GEN) from backward (A), symbolic
  assembly (B), and memory retrieval (C) on irrelevant inventory.

No single world favors the same hypothesis on every axis; that is
the point of competing hypotheses.

## 8. Domain-blindness analysis

The standard (Micah 2026-10-03): would the same frozen
architecture still know how to learn/use this if humans had never
named the domain or capability? Dependence on human domain
identity is architectural failure.

- BACKCHAIN: operates on opaque MAP ids, learned kind-set
  contracts (inmask/outmask bitmasks), and the goal triple
  (input value, kin, kout). Relation numbers (91/92/94), node
  ids (202/211), and kind labels (NODE/NUM) never enter any
  decision except as opaque integers compared for equality or
  bitmask intersection. A frozen BACKCHAIN binary given the
  relabeled world must behave identically.
- SUSPEND: identical argument. Thunk interning keys on
  (map-id, input-thunk-ids); evaluation dispatches on map-id;
  contracts are bitmasks. The persisted composite is a DAG over
  opaque ids. Relabeling changes nothing it consults.
- LEARN-COMPOSE: the signature is (kin, kout, contract-sketch),
  where the sketch is a sorted multiset of
  (arity, inmask-set, outmask-set) triples. No relation labels,
  no node ids, no domain names, no capability names appear.
  Similarity is computed over these alone. This is the
  hypothesis most at risk of smuggling (a rich similarity
  function could encode researcher knowledge of the domain),
  which is why F-C4 exists and why the signature function must
  be frozen to kind sets plus the contract multiset, nothing
  else.

Proposed blind battery (for the implementation worker, not run
here): apply the C398/C399/C409/C403 protocol to each
hypothesis's Q1-equivalent world: (i) permute relation numbers,
(ii) permute node ids, (iii) swap kind polarity (NODE<->NUM with
contracts swapped consistently), (iv) joint relabel of all three.
Require byte-identical stdout across all four variants per
hypothesis. Any byte difference is architectural failure of that
hypothesis, not a test artifact.

## 9. Relation to the live mechanisms and regression ground

These hypotheses compete with GEN and its successor the unified
contract module (C424) at the learned-structure composition
level. They do not compete with COGOPS procedure-body composition
(C417/C422/C433); the P0 subsumption question is orthogonal, and
nothing here claims to resolve it.

Any implementation worker taking up one hypothesis must first
reproduce the standing regression ground, unchanged:
- the 5 pipeline pairs (C368 battery),
- diamond Q1 and misleading-teaching Q2 (C380),
- fan-in, DAG-4, chain-3, partial applicability (C402),
- the domain-blindness battery of Section 8.
Only then do the discriminating worlds D1-D5 mean anything.
On cycles, all three hypotheses declare the iterate/halt gap
(4.8, 5.8, 6.8); GEN's five-family cycle envelope (T5) is the bar
they do not yet meet, and the worker must state this as a BOUND,
not silently drop cycle coverage.

Note on the existing synthesis: C402 already showed the diamond
was a trial-space limit with a principled fix (GEN), and C424
unified the mechanism. These hypotheses are therefore NOT
proposed because composition is broken; they are proposed because
Micah's clarification demands competing general hypotheses for
the diamond failure rather than a single anointed mechanism, and
because A, B, and C make different predictions about
cap-independence (D1), persistence (D2), revision cost (D3),
learning curves (D4), and distractor scaling (D5) that GEN's
single point in the space cannot discriminate.

## 10. Honest bounds and non-claims (whole report)

- Nothing here is tested (Section 0, Section 2.2). All
  predictions are reasoned.
- Hypotheses A and B are researcher-implemented fixed
  procedures, exactly like GEN. Only Hypothesis C moves any
  part of the composition strategy into learner-owned state,
  and even C's operators and signature function are
  researcher-provided: C is an L2 adaptive-reuse claim, not L3
  representational invention. None of the three claims
  learner-invented composition machinery.
- None of the three is claimed to subsume the contract module,
  and none is claimed to be compatible with COGOPS; those are
  separate experiments (synthesis P0).
- All three assume pure MAPs (T10) and declare cycles BOUND
  pending an iterate-with-halt construct.
- The walk-throughs use the frozen PAIR6 Q1 world; the
  discriminating worlds D1-D5 are specified but not built.
- No kill bars are frozen here; freezing bars is the
  implementation worker's preregistration step, not this
  design step.

## 11. Proposed next steps (not this task)

For the parent orchestrator's scheduling, in information-gain
order:

1. Preregister and implement Hypothesis B's F-B1/F-B2 on the
   PAIR6 substrate: persistence and surgical revision are the
   sharpest architectural discriminators, and B's predictions
   are the most mechanically checkable (exec counts, assembly
   step counts, memo-invalidation scope).
2. Preregister Hypothesis A's F-A1 (chain-10) against frozen
   GEN: the cheapest build (a regressor plus the existing
   base), directly testing cap-independence.
3. Preregister Hypothesis C's F-C1 (three-goal curve): the only
   test of whether composition strategy can live in learner
   state; needs the composition-memory substrate, the largest
   build of the three.
4. Run the Section 8 blind battery against whichever
   hypothesis is implemented first; blindness is a standing
   requirement, not a follow-up.
5. Revisit the cycle BOUND for the surviving hypothesis(es)
   only after D1-D5 discriminate: do not build the iterate
   construct three times.

## 12. Files and provenance

- This file: REPORT.md (design deliverable; the only file in
  this lane).
- No source, no binaries, no run logs exist for this task.
- Commit: local only, explicit pathspec, never pushed, per the
  lane constraint and the shared-workspace git discipline.
