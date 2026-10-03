# PREREG.md: XDOMAIN-CAUSAL-L2 -- L2 Adaptive Reuse for Causal to Intervention

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.
This prereg is never edited after freezing. It lives in
`xdomain_causal/l2adapt/` so the C273 battery (parent directory,
commits 2dc11c883 and 664c04d8d) is preserved untouched.

## Hypothesis

H-XDCL2-1: H1 (learned typed contracts) and H2 (value-level function
composition), equipped with the generic L2 REBIND operator from C279
(XDOMAIN-L2), can solve causal to intervention queries when the causal
model is a parameterized structural equation. The intervention
(do-surgery) is expressed as REBINDING the intervened variable's
evidence source from the observed relation to the do-spec relation,
discovered by the learner via a generic candidate scan plus
composition validation. The context variable's binding is held fixed,
which is the L2 analogue of the do-operator's "context held fixed"
principle.

H-XDCL2-2 (control): the same REBIND operator applied to a pure
observational predictor (no equation structure) cannot solve the
surgery cases, because the interventional answer is not reachable by
rebinding the relation of a confounded mapping. This is the C273
diagnosis restated as a predicted control failure, and it localizes
any success to the equation parameterization rather than to REBIND
in general.

Predicted outcome: H1 and H2 both solve all four Z queries in
TREAT-L2, with Z1 and Z4 (do not equal see) solved only via the
rebound X' bound to the do-spec relation; the observational predictor
O rebound to any candidate fails Z1 and Z4; L1 without adaptation
fails Z1 and Z4.

## World design: confounded causal world with a do-spec interface

Variables: A in {1,2} (confounder), C = A (cause), E = A + 2*C
(effect). Units: 501 (A=1, C=1, E=3), 502 (A=2, C=2, E=6). The
confounding is structural: A drives both C and E.

Facts (training, all episodes):
- (501,86,1), (502,86,2): A values, rel 86.
- (501,87,1), (502,87,2): C values, rel 87.
- (501,85,3), (502,85,6): E values, rel 85.
- (501,84,9), (502,84,9): distractor relation, rel 84.
- 30 interference facts (5000+i, 60+(i%10), 6000+i), i in 0..29.

Intervention interface (world facts, the do-spec):
- (93,89,1): query relation 93 means do(C=1).
- (94,89,2): query relation 94 means do(C=2).
Rel 89 is the do-spec relation, keyed by query relation (as in C273
and C275). The do-value is the intervention, not the answer; the
answer E must still be computed through the structural equation.

Intervention queries (each solved in a fresh workspace):
- Z1: s=501, qrel=94, goal=5. do(C=2): E = 1 + 2*2 = 5.
  Observational predictor says 3. do not equal see (surgery).
- Z2: s=501, qrel=93, goal=3. do(C=1): E = 1 + 2*1 = 3.
  do equal see.
- Z3: s=502, qrel=94, goal=6. do(C=2): E = 2 + 2*2 = 6.
  do equal see.
- Z4: s=502, qrel=93, goal=4. do(C=1): E = 2 + 2*1 = 4.
  Observational predictor says 6. do not equal see (surgery).

Oracle (driver-level observability only, not a mechanism): for
(s,qrel), oracle = val(s,86) + 2*val(qrel,89), computed from learner
state. Expected: 5, 3, 6, 4. Proves the world solvable from learner
state; the gap under test is in the mechanisms.

## Learned structures (installed as prior learning)

Behavior implementations are researcher-authored, representing
previously learned structures (same honest boundary as C279). Under
test is whether the LEARNER drives the rebinding, not behavior
induction.

- X (id 0, behav 0): the causal model. X(s) = g(s,in1) + 2*g(s,in2),
  where g(s,r) is the first object of fact (s,r,*), or -999999 when
  missing. in1 and in2 are bindable parameters. Teaching binds in1 to
  the 1st distinct relation observed for the training subject (86)
  and in2 to the 2nd distinct relation (87), via a generic
  bind-to-nth-distinct-relation routine (no literals). X(501)=3,
  X(502)=6. Learned sig NODE to NUM. This X is the structural
  equation E = A + 2*C with rebindable evidence sources.
- Y (id 1, behav 1): the intervention-spec reader. Y(q) = g(q,in1)
  with in1=89 installed as prior learning (Y knows the intervention
  interface; analogous to C279's ALLOC with its fixed divisor).
  Y(93)=1, Y(94)=2. Learned sig NODE to NUM. Y is on the critical
  path: the solver reads the do-value and the do-spec relation
  through Y, never through a literal.
- D (id 2, behav 2): distractor equation. D(s) = 3*g(s,in1), in1
  bound to the 1st distinct relation (86). D(501)=3, D(502)=6. The
  confounded alternative E = 3*A; it matches observation but cannot
  express intervention.
- O (id 3, behav 3): observational predictor (CONTROL). O(s) =
  g(s,in1), in1 bound to the 3rd distinct relation (85). O(501)=3,
  O(502)=6. O is the C273-style observational mapper parameterized
  by relation; rebinding O is the direct transfer of C279's REBIND
  to a non-equation structure.

## L2 mechanism: intervention as evidence-source rebinding

The solver (the "Y must intervene" procedure) handles a query
(s,qrel,goal) as follows. Phase 1 is exact L1 reuse. Phase 2 (l2_on=1)
is the L2 adaptation.

1. Read do_val = Y(qrel) and yrel = Y's bound relation (from Y's
   MAP, not a literal). If Y is absent or do_val is missing, skip to
   Phase 1 with no intervention context (this is what makes ABL-Y and
   NO-DOSPEC fail).
2. Assert the intervention as a unit fact: (s, yrel, do_val). This
   materializes "C is set to do_val for s". The observed C fact
   (s,87,*) remains; the solver does not delete it.
3. Phase 1 (L1): try singles and (H1) type-gated pairs or (H2)
   ordered pairs under the trained bindings. Predicted: fails Z1,
   Z4; solves Z2, Z3 via the observational path (disclosed
   coincidence, same as C273).
4. Phase 2 (L2): scan the generic candidate relations for s
   (distinct r with a fact (s,r,*), first-seen order; now includes
   yrel because of the asserted fact). For X, rebind in2 (the
   intervened variable's evidence source) to each candidate; for D,
   O, Y rebind in1 to each candidate. in1 of X (the context binding)
   is held fixed. Try each rebound MAP as a single and in pairs.
   The first rebound validating to the goal wins.

The do-operator's "sever incoming edges, recompute with context
fixed" is expressed here as: stop reading C from the observed
relation (87) and read it from the set relation (yrel=89), while the
A binding (in1=86) is untouched. No graph is rewritten; the equation
form is unchanged. Only the evidence source binding changes, via the
generic REBIND operator (copy MAP, set param, inherit signature,
record rebound_of).

Candidate order for s=501 (fact insertion order 86, 87, 85, 84, then
the asserted 89): [86, 87, 85, 84, 89]. The genuine do-spec relation
is met LAST, so the learner must reject four wrong bindings first.
X' under in2=86 gives 3, 87 gives 3, 85 gives 7, 84 gives 19, 89 gives
5. Only 89 validates for Z1.

## Arms (per mechanism)

Each Z is solved in a fresh workspace (training facts + interference
+ do-spec world facts; teach; then the query-specific steps).

- TREAT-L2: teach X,Y,D,O; solve Z1..Z4 with l2_on=1.
- L1-ONLY: teach X,Y,D,O; solve Z1..Z4 with l2_on=0. Must fail Z1,
  Z4 (adaptation necessary). Z2, Z3 may solve observationally.
- ABL-X: teach, delete X (id 0); solve Z1 with l2_on=1. Must fail.
- ABL-Y: teach, delete Y (id 1); solve Z1 with l2_on=1. Must fail
  (Y is on the critical path: no do-value, no asserted fact, no 89
  candidate).
- FRESH: facts only (no teach); solve Z1 with l2_on=1. Must fail.
- NO-DOSPEC: teach X,Y,D,O; world WITHOUT the (93,89,*) and
  (94,89,*) do-spec facts; solve Z1 with l2_on=1. Must fail (Y reads
  missing; no 89 candidate). Proves the intervention spec is
  necessary, not just the equation.

## Kill bars (all must pass; verdict requires 9/9)

- K1 H1-L2-SOLVE: TREAT-L2 solves Z1=5 and Z4=4, each via a rebound
  X' with in2=89 (the do-spec relation) and rebound_of=X (id 0).
  Z2=3 and Z3=6 are also solved (binding may be observational;
  disclosed, not counted as intervention evidence).
- K2 H2-L2-SOLVE: same as K1 for H2 (EQN mode rebound with in2=89,
  differing from the trained in2=87).
- K3 L1-NECESSARILY-FAILS: L1-ONLY fails Z1 and Z4 on both H1 and
  H2. (Z2, Z3 solving observationally is expected and disclosed.)
- K4 CAUSAL: ABL-X, ABL-Y, FRESH, and NO-DOSPEC all fail Z1 on both
  H1 and H2 with l2_on=1.
- K5 REBIND-DISCOVERED: grep audit confirms the do-spec relation 89
  appears in the solver only via Y's MAP field (read, never
  written as a literal) and in world-setup add_fact lines and Y's
  installed prior; it never appears as a literal in the rebind
  operator, the candidate scan, or the composition/validation logic.
  The X' binding to 89 is discovered through the generic scan.
- K6 DETERMINISM: 3 full runs per mechanism are byte-identical
  (sha256 recorded in NAMECHECK.md).
- K7 NO-TEMPLATE: grep confirms no L2-specific domain literals in
  the composer/rebind/scan/solver logic: no hardcoded 89 (outside
  world setup and Y's installed prior), no 501/502/5/4/3/6 in logic,
  no X-to-89 mapping. Arm harness query literals (the Z queries
  themselves) are explicitly allowed, as in C279.
- K8 CONTROL-OBS: the observational predictor O, rebound to every
  candidate relation, fails Z1 and Z4 on both mechanisms. C279-style
  relation rebinding on a pure observational mapping does not reach
  the interventional answers (5 and 4 are not values of any
  candidate relation for the query subjects).
- K9 COMPARISON: the REPORT contains an explicit comparison to C275
  sever+recompute on the same Z1..Z4: per-query results,
  representation used (parameterized equation with evidence-source
  rebinding vs explicit causal graph with edge surgery),
  generality scope (structures tested), and a subsumption analysis
  answering whether L2 adaptation subsumes sever+recompute or the
  structure-rewriting dimension is still needed.

## Verdict rule

XDOMAIN-CAUSAL-COMPLETE iff K1-K9 all PASS on the frozen design
above. Per-mechanism adaptive scores are reported (H1: K1,K3-K8 as
they govern H1; H2: K2,K3-K8 as they govern H2; K9 is joint).
COMPLETE marks the battery as executed with exact-line diagnosis,
following the composition_xdomain and xdomain_l2 precedent; it does
not by itself claim generality beyond the tested world.

## Predicted mechanism behavior (frozen)

H1 TREAT-L2, Z1 (s=501, qrel=94, goal=5):
- Setup: do_val=Y(94)=2, yrel=89, assert (501,89,2).
- Phase 1: X(501)=3, Y(501)=2, D(501)=3, O(501)=3; all pairs fail
  (intermediate values 3, 2 are not fact subjects, so second stages
  read missing; type gating additionally prunes). L1-FAIL.
- Phase 2: candidates [86,87,85,84,89]. X rebound in2=86 gives 3,
  87 gives 3, 85 gives 7, 84 gives 19, 89 gives 5. Z-RSINGLE on the
  89 rebound with rebound_of=0. D rebounds give 3,3,9,27,6; O
  rebounds give 1,1,3,9,2; Y rebounds read missing or give 2. None
  validate. Pairs with rebound singles fail on missing second-stage
  reads.
- Z2 (goal 3): Phase 1 X(501)=3 solves observationally (disclosed).
  Z3 (goal 6): Phase 1 X(502)=6 solves observationally. Z4 (goal 4):
  Phase 1 fails; Phase 2 X' in2=89 gives 2+2*1=4.

H2 TREAT-L2 mirrors this with modes: Phase 1 ordered pairs/singles
fail Z1/Z4; Phase 2 EQN-mode in2 rebound to 89 validates 5 and 4.

L1-ONLY: Z1=-2 (fail), Z4=-2 (fail) on both; Z2=3, Z3=6 via
observational singles. ABL-X: D'/O'/Y' rebounds never validate 5;
fail. ABL-Y: no do_val, no assert, 89 never a candidate; fail.
FRESH: no MAPs; fail. NO-DOSPEC: Y(94) missing; fail.

## Honest boundaries

- The do-value is carried by the query relation (93/94) and read
  through Y, the installed intervention-spec reader. This is the
  query interface, not a hint: the mechanism must still discover
  that X's C evidence source must be rebound to Y's relation and
  validate the recomputed E.
- The solver asserts (s, yrel, do_val) to materialize the set value.
  This re-encodes the query; it does not compute the answer. The
  relation used is read from Y's MAP, never a literal.
- Behavior implementations (equation, readers, distractor) are
  researcher-authored prior learning, as in C279. The REBIND
  operator is generic researcher-authored machinery. The binding
  decisions (in2 to 89, not 86/87/85/84; X not D/O) are
  learner-driven through scan plus validation.
- in1 of X (context binding) is held fixed by design; rebinding it
  is not tried. This is the "context held fixed" principle, stated
  here rather than discovered. A fuller L2 would also try in1 and
  must then discriminate the confounded (87,89) binding; that is
  future work.
- Expected answers are used for verification (same methodology as
  C273, C275, C279). Learner-owned verification of counterfactuals
  is future work.
- One causal structure (one confounder, linear equation). The
  comparison to C275 is scoped accordingly; see K9.
- Binary NODE/NUM kinds are syntactic, as in prior batteries.
- No em dashes or en dashes are used in this document (verified).

## Pre-registered comparison framework (for K9)

C275 built sc_do, a bespoke structure-transforming operator: it
reads causal edges (rel 71), structural equations (rel 72), and the
observation mapping from learner state, copies the edge list, severs
incoming edges of the intervened variable, fixes the do-value, and
recomputes in topological order. It solved Z1..Z4 (5,3,6,4) on the
frozen xdomain world and (3,0) on a second generality world
(Q=2*P, R=P+Q), and showed via K5 IRREDUCIBILITY that deleting one
edge plus one term moves the answers while value facts stay
identical, which value chaining cannot express. Its verdict:
do-composition is an irreducibly structural second kind, and
sever+recompute strictly generalizes value chaining.

This battery tests the alternative hypothesis: that the L2
adaptation operators (REBIND), applied to a parameterized causal
equation, achieve the do-computation without a bespoke surgery
operator. The K9 analysis must answer, on the evidence:
(a) per-query: does L2 match sever+recompute's (5,3,6,4);
(b) representation: what must be true of the learned structure for
each approach (parameterized equation with rebindable evidence
sources vs explicit edge/equation graph);
(c) generality: C275 tested two structures with unmodified operator;
this battery tests one; what would a second structure require here;
(d) subsumption: does L2 adaptation subsume sever+recompute (making
the structure-rewriting dimension unnecessary), does
sever+recompute subsume L2, or are they complementary (L2 adapts
parameters of learned structures; sever+recompute rewrites explicit
structure; each covers cases the other does not).
The honest answer may be (d); the prereg does not prejudge it.
