# PREREG: XDOMAIN-CAUSAL-ADAPT -- causal model to intervention with required adaptation

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/xdomain_causal_adapt/` only.
Worker: Cross-Domain Adaptive Composition worker (subagent, 2026-10-02).
Parent mandate: cross-domain moves from exact black-box reuse toward
adaptive heterogeneous composition; high-value test is
causal-to-intervention REQUIRING adaptation.

## 1. What is being tested

Whether a causal model X learned in one context can be ADAPTED (not
copied) to choose an intervention in a context with different variable
names, different arity, and partial observability. The load-bearing
question: is adaptation REQUIRED (does literal reuse fail?) and does
the adapted structure WORK (optimal intervention) and OUTPERFORM both
direct copy and learning from scratch? Both pass and fail outcomes are
publishable: a fail on K4 localizes exactly where the adaptation
advantage does and does not live.

What is NOT tested: exact reuse (done elsewhere); learning the causal
model itself as a novelty claim (discovery is deliberately generic);
multi-step plans; stochastic worlds.

## 2. Frozen worlds

### 2a. Source world S (observational learning context)

Variables: a, b, c (indices 0,1,2). All observed.
Structural equations: b = 2a ; c = a + b.
Observational data (free, 4 rows), a in {1,2,3,4}:
  (a,b,c) = (1,2,3), (2,4,6), (3,6,9), (4,8,12).
One structural probe is allowed in S (part of learning X, before any
target contact): set b=5 (a ambient 1) -> observed row (1,5,6).
This probe falsifies the observationally-tied MUL(3) model of c
(6 != 3*1) while ADD(a,b) survives (6 = 1+5).

Frozen X (what the learner must recover exactly):
  edges: b: parents=[a], form MUL, k=2
         c: parents=[a,b], form ADD
         a: no parents (root)
  roles: a=root, b=mid, c=leaf
  source policy schema (demonstrated in S): intervene on ROOT at max
  value. S intervention truth at value 10: set a -> c=30 ;
  set b -> c=11 (a ambient 1). So ROOT (a) is optimal in S.

### 2b. Target world T (intervention context)

Observed variables: p, q, r, d, s (indices 0..4). NO name overlap
with S. Hidden variable: h (partial observability; never observed,
never intervenable).
Structural equations: q = 2p ; h = p + q (hidden) ; r = h ;
d = r + 1 (readout with offset) ; s = r + d (downstream extra).
Arity differs from S: 5 observed + 1 hidden vs 3.
Free observational data (4 rows), p in {1,2,3,4}:
  p=1: (q,h,r,d,s) = (2,3,3,4,7)
  p=2: (4,6,6,7,13)
  p=3: (6,9,9,10,19)
  p=4: (8,12,12,13,25)
Ambient row (p=1): r = 3.

Probe API (the ONLY target contact besides the 4 free rows):
set one observed candidate variable to value 6, read all observed.
Probe budget B = 2 for EVERY learner (adapted and from-scratch alike).
Frozen probe outcomes at value 6:
  probe p=6 -> (6,12,18,19,37): delta_r/delta_p = 15/5 = 3
  probe q=6 -> (1,6,7,8,15):  delta_r/delta_q = 4/4 = 1
  probe d=6 -> (1,2,3,6,9):   delta_r = 0 (d is causally inert for r)

Intervention task: ONE intervention, one variable from the candidate
set {p, q, d} (s excluded: observationally downstream of the target r;
d included as the distractor), value fixed at 10, maximize r.
Frozen intervention truth at value 10:
  set p=10 -> r=30 ; set q=10 -> r=11 ; set d=10 -> r=3.
Optimal = 30 (set p). The harness exhaustively verifies the optimum
over {p,q,d} at value 10; the optimum is part of the frozen truth.

## 3. Frozen learners

### L_adapt (has X; the adaptation under test)

1. Observational form-match on T's 4 free rows using X's edge-form
   inventory {MUL(k) exact, ADD exact}: q=2p matches b's MUL(2) form;
   r=p+q matches c's ADD form; p has no parents (root, like a);
   d=r+1 matches NO X form (non-role); s=r+d is ADD but has the
   c-analog r as a parent, so s is downstream-extra, not a role.
   Role candidacy scores (computed, order-invariant): p=2 (root),
   q=1 (mid), r=1 (leaf-cand), d=0, s=0.
2. X-driven probe selection (B=2): probe 1 = highest score (p:
   confirm X's predicted root total-effect 2+1=3 per unit, the
   quantity the transferred policy needs); probe 2 = lowest score
   among intervention candidates (d: test X's risky prediction that
   the non-role variable is causally inert for r).
3. Full discovery on 4 obs rows + 2 probe rows; re-verify role map.
   Expected final map: {a->p, b->q, c->r}; d non-role (no equation);
   s downstream of r. The adapted model posits r's parents = {p,q}
   directly (it does NOT recover hidden h; the model is
   interventionally correct on {p,q,d} without it).
4. Transferred policy schema "set ROOT to max", interface re-bound
   through the role map (ROOT->p): set p=10.
   Predicted intervention outcomes: p: 30 (measured total 3/unit:
   3+3*9); q: 11 (transferred ADD form: r = p_ambient + q = 1+10);
   d: 3 (measured inert). All three must match truth.

Adaptation ops exercised: specialize (bind roles a->p,b->q,c->r),
extend (classify target-only extras d/s/h: non-role, downstream,
hidden-acknowledged), interface-adapt (policy schema re-bound
ROOT->p; extras excluded from the policy interface).

### L_copy (direct copy; has X)

X's source policy "set a to 10" applied LITERALLY in T. Variable 'a'
has no binding in T's namespace (bind fails -> -1) so the
intervention is void. Expected outcome: r stays 3 (ambient);
inapplicable flag = 1. This is the REQUIRED-adaptation bar: verbatim
reuse cannot even execute.

### L_scratch (no X; the ablation / from-scratch baseline)

Identical discovery code, identical 4 free rows, identical B=2 probe
budget. Probe selection (preregistered generic, X-free rule): probe
the first two candidates in presentation order. Planning
(preregistered generic, X-free rule): linear-extrapolate r at value
10 from (ambient, probe) per probed candidate
(pred = r_amb + slope*(10 - v_amb), v_amb: p=1,q=2,d=3);
unprobed candidates assumed at ambient r=3; intervene on argmax
predicted r; ties broken by presentation order.
Metric: mean outcome over ALL 6 presentation orders of {p,q,d}.
Frozen scratch outcomes by order:
  [p,q,d]: probe p,q -> pred 30,11 -> pick p -> 30
  [p,d,q]: probe p,d -> pred 30,3  -> pick p -> 30
  [q,p,d]: probe q,p -> pred 11,30 -> pick p -> 30
  [q,d,p]: probe q,d -> pred 11,3  -> pick q -> 11
  [d,p,q]: probe d,p -> pred 3,30  -> pick p -> 30
  [d,q,p]: probe d,q -> pred 3,11  -> pick q -> 11
  sum = 142, n = 6, mean = 142/6 = 23.67, min = 11.
Mechanism of the gap: X converts order-sensitive blind probing into
order-invariant directed probing (X-driven candidacy scores do not
depend on presentation order). No strawman: scratch is a real
zero-prior algorithm (local-linear extrapolation) with a neutral
probe rule.

K7 lesion: L_scratch IS L_adapt with X removed (single code path,
has_x flag = 0 -> order-based probing + extrapolation planner). The
ablation is structural, not just numerical.

## 4. Frozen kill bars

K1 X-LEARNED-INDEPENDENTLY: discovered edges exactly
  b:(parents=[a],MUL,k=2), c:(parents=[a,b],ADD), a:parentless;
  roles (a=root,b=mid,c=leaf); discovery used S data only
  (4 obs rows + 1 S-probe on b); source demo set a=10 -> c=30;
  S-optimality: 30 > 11 (a beats b). PASS iff all hold.

K2 COPY-FAILS (adaptation REQUIRED): bind('a') in T -> unbound;
  inapplicable=1; outcome r=3 = ambient < optimal 30.
  PASS iff outcome==3 and inapplicable==1 and 3 < 30.

K3 ADAPTATION-WORKS: role map exactly {a->p, b->q, c->r};
  d classified non-role, s downstream of r; probe1 = p, measured
  total-effect 3 == X-predicted (2+1); probe2 = d, delta_r == 0;
  policy sets p=10 -> r=30 == harness-verified optimal 30;
  predicted outcomes (p:30, q:11, d:3) all == truth.
  PASS iff all hold.

K4 ADAPTED-OUTPERFORMS: adapted mean 30 > copy 3; adapted mean 30 >
  scratch mean 142/6 (integer check 30*6=180 > 142); adapted
  min-over-orders 30 > scratch min 11. PASS iff all hold.

K5 NO-PAIR-TEMPLATE: adaptation code is generic over (X, probe-API):
  no branches on T variable identities/names, no S/T-pair
  special-casing (researcher code-inspection audit, recorded in
  REPORT); X trained on S only; T contact = 4 obs rows + 2 probes,
  identical budget to scratch (binary emits both counts).
  No paired (S,T) training rows anywhere. PASS iff audit clean and
  budgets equal.

K6 DETERMINISTIC-3x3: sha256(stdout) identical across 3 runs.
  PASS iff all three equal. (No RNG anywhere; fixed probe value 6;
  explicit order enumeration.)

K7 ABLATION-OF-X: lesion has_x=0 (exactly X removed, same code path):
  scratch mean 142/6 < adapted mean 30; scratch min 11 < adapted
  min 30. The full adapted-vs-scratch gap is attributable to X.
  PASS iff both hold and the lesion is exactly X-removal.

Discovery tie-break (preregistered, fixed, generic, applied
identically in S and T and by scratch): when MUL(k) and ADD both fit
all rows, prefer ADD (preserve observed mediators; do not
marginalize an observed variable out of the structure). Expected
tie-break triggers: S: 0 (the b-probe falsifies MUL(3) for c);
T final discovery: 1 (r: MUL(3) on p vs ADD(p,q); ADD kept).
The binary counts and emits triggers; K1/K3 check the expected
counts (0 and 1).

## 5. Verdict rule

BUILD-PASS iff K1..K7 all PASS. Any bar FAIL -> BUILD-FAIL with the
failed bars named and the mechanism localized. A K4 fail with K1-K3
passing localizes the adaptation advantage to shift-robustness and
sample efficiency rather than final-outcome dominance, and that
localization IS the reportable result.
