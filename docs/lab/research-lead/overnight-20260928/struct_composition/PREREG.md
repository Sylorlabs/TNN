# PREREG.md: STRUCT-COMPOSITION -- Structure-Transforming Composition for Causal Intervention

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.
This is the UNFROZEN variant: new prototype mechanism code only; the
substrate base (composition_A/cx_core.zag) is referenced verbatim
(sha256-verified) and read-only, never copied or edited.

## Context

XDOMAIN-CAUSAL (xdomain_causal/REPORT.md, frozen commit 2dc11c883)
showed all four composition mechanisms (A, B, C, XIO) failing exactly
the do-surgery queries (Z1=Z4=-2) while preserving the do==see queries
(Z2=3, Z3=6). Diagnosis: all four implement composition as value
chaining, v2 = stage(m2, stage(m1, s)), a function of the first stage's
output value. Under confounding, the interventional answer is not a
function of the observational output. The do-operator needs
structure-transforming composition: read causal edges, sever incoming
edges of the intervened variable, recompute downstream with context
held fixed.

## Hypothesis

H-SC-1 (surgery): A prototype sever+recompute operator that (1) reads
the causal graph (edge facts) and structural equations (term facts)
from learner state, (2) severs incoming edges of the intervened
variable on a working copy of the graph, (3) fixes the intervened
variable to the do-value, (4) recomputes every other variable in
topological order from the surviving equations with exogenous
variables held at observed values, solves the two surgery cases
(Z1=5, Z4=4) and preserves the two do==see controls (Z2=3, Z3=6) on
the frozen xdomain world.

H-SC-2 (generality): The same operator code, unmodified, solves a
second causal world with different variables, different coefficients,
a different intervention target, and a different topological role for
the intervened variable (intervening on a middle variable Q rather
than C, plus intervening on the root P where surgery is a no-op).

H-SC-3 (irreducibility): With all value facts identical, editing only
the structure (deleting one causal edge and its equation term) changes
the operator's answers. Any composition expressible as value chaining
over the same value facts must give the same answer on both runs,
because its inputs are unchanged; therefore sever+recompute is not
expressible as value chaining over values. Value chaining is the
no-surgery degenerate case of the operator (empty intervention on a
single-edge graph), so the relationship is generalization, not
reduction: the surgery step itself has no value-chaining expression.

## World 1 (frozen xdomain world, reused verbatim)

Variables: A=801, C=802, E=803. Units 501 (A=1), 502 (A=2).
Causal edge facts (rel 71): (801,71,802), (801,71,803), (802,71,803).
Structural equation term facts (rel 72, packed parent*10+coeff):
(802,72,8011) meaning C = 1*A; (803,72,8011) and (803,72,8022)
meaning E = 1*A + 2*C.
Observation mapping (rel 70): (801,70,86), so variable 801's observed
value for a unit is read from fact (unit,86,o).
Unit facts: (501,86,1), (502,86,2).
X facts (rel 81, 3-link chains) and Y facts (rel 88, 2-link chains)
identical to xdomain, for the K1 competence census.
Query specs: (93,68,803) target E, (93,69,8021) do(C=1);
(94,68,803), (94,69,8022) do(C=2). The do-value rides the query
relation, as in xdomain (disclosed interface).
30 interference facts (5000+i, 60+(i%10), 6000+i), as in xdomain.
No comb node.

Predictions, TREAT arm (operator answers, not ev_query):
Z1=(501,94): sever A->C; A=1 observed; C=2 fixed; E=1+2*2=5.
Z2=(501,93): E=1+2*1=3.
Z3=(502,94): E=2+2*2=6.
Z4=(502,93): E=2+2*1=4.

## World 2 (generality world, new)

Variables: P=811, Q=812, R=813. Units 511 (P=1), 512 (P=2).
Edges: (811,71,812), (811,71,813), (812,71,813).
Equations: (812,72,8112) meaning Q = 2*P; (813,72,8111) and
(813,72,8121) meaning R = 1*P + 1*Q.
Observation mapping: (811,70,86). Unit facts: (511,86,1), (512,86,2).
Query specs: (95,68,813), (95,69,8121) do(Q=1);
(96,68,813), (96,69,8110) do(P=0).

Predictions, GEN arm (same operator code, zero edits):
G1=(512,95): sever P->Q; P=2 observed; Q=1 fixed; R=2+1=3.
Observational R for P=2 would be 6, so this is a surgery case in a
new structure with a new intervention target.
G2=(511,96): do(P=0) on the root: no incoming edges, surgery is a
no-op; P=0; Q=2*0=0; R=0+0=0.

## World 3 (degenerate case world, new)

Variables: IN=901, OUT=903. Edge: (901,71,903).
Equation: (903,72,9011) meaning OUT = 1*IN.
Observation mapping: (901,70,86). Unit fact: (521,86,7).
Query spec: (97,68,903) with no rel-69 fact, meaning no intervention.

Prediction, DEGEN arm: answer 7. With an empty intervention the
operator reduces to structure-respecting value propagation, which is
what a single chain stage computes: value chaining is the no-surgery
degenerate case.

## IRRED arm (structure-edit experiment)

Identical value facts to World 1 (same units, same X/Y facts, same
observation facts). Structure edited: edge (801,71,803) and equation
term (803,72,8011) removed, so the structure now says E = 2*C only.
No value fact changes.

Predictions: Z1=(501,94) -> 4 (was 5); Z4=(502,93) -> 2 (was 4).
Any value-chaining composition over the same value facts sees
identical inputs on both runs and must emit identical outputs; the
operator emits different outputs; hence the operator is not
expressible as value chaining over values.

## Ablation arms

ABL-NOEDGE: World 1 minus all rel-71 edge facts -> operator emits
STRUCT-MISSING, -2 on all Z.
ABL-NOEQ: World 1 minus all rel-72 equation facts -> -2 on all Z.
ABL-NOOBS: World 1 minus unit (unit,86,o) facts -> -2 on all Z.
FRESH: interference facts only -> -2 on all Z.
The operator reads structure; it has no hardcoded answers. (The X/Y
MAPs are not inputs to the operator at all, unlike mechanisms A-D;
their competence is measured in K1 only.)

## Kill bars

- K1 COMPETENCE: X1=3 (trial), X2=6 (rebind), Y1=1 (trial), Y2=2
  (rebind) via the base ev_query, same as xdomain K1. PASS iff exact.
- K2 SURGERY: TREAT operator answers exactly (5,3,6,4) on Z1..Z4.
  PASS iff exact.
- K3 ABLATION: ABL-NOEDGE, ABL-NOEQ, ABL-NOOBS, FRESH all give -2 on
  every Z query, with STRUCT-MISSING emitted. PASS iff exact.
- K4 GENERALITY: GEN arm gives exactly (3,0) on G1,G2 with
  unmodified operator code. PASS iff exact.
- K5 IRREDUCIBILITY: IRRED arm gives exactly (4,2) on Z1,Z4 with
  value facts identical to TREAT. PASS iff exact.
- K6 DEGENERATE: DEGEN arm gives exactly 7. PASS iff exact.
- K7 AUDIT: the surgery record for Z1 shows edge (801,71,802)
  severed, topological order [801,802,803], and recompute trace
  A=1, C=2, E=5. PASS iff shown.
- K8 DETERMINISM: 3/3 runs byte-identical (sha256 recorded).
  PASS iff identical.

## Honest boundaries

1. Structural equations are declarative facts in this prototype
   (planted like xdomain's edges); the operator reads them from
   learner state and nothing about A/C/E is hardcoded in it, but
   learning the equations from data is future work.
2. Variable enumeration scans fact ids in the range 800..920; this
   working-memory bound is a disclosed researcher choice.
3. Surgery operates on the operator's working copy of the edge
   list; the workspace facts are not mutated, so repeated queries
   see the intact graph.
4. The do-value rides the query relation (93/94/95/96), the same
   interface as xdomain.
5. Expected answers are used for verification, as in all prior
   composition batteries.

## Standing metrics (to record)

Cognition lines added (new driver only), modes/bridges/handlers/new
core semantic cases (must be 0/0/0/0), researcher-owned vs
learner-owned accounting, capability-source delta.
