# PREREG: xdomain_l2 -- Level 2 Adaptive Reuse on Cross-Domain Composition

Frozen 2026-10-02, before implementation. Any change requires a new prereg;
this document is never edited after freezing.

## Hypothesis

H1 (learned typed contracts) and H2 (value-level function composition),
which solve cross-domain composition at Level 1 (exact reuse) on four
domain pairs, can also drive Level 2 adaptive reuse: when X or Y must be
REBOUND (not used unchanged) for Z, the learner discovers the rebinding
from the sealed world guided by typed contracts, without researcher
supplied mapping.

Specific L2 form under test: RELATION REBINDING. X is a parameterized
procedure (SUM over a relation stored in a MAP field). Training binds X
to r=71. The sealed world presents X-relevant facts under r=73 (new
relation). L1 (exact reuse, X bound to 71) necessarily fails. The learner
must create a rebound variant X' (bound to 73) and compose X' with Y.

## World Design

Training facts (r=71, prices):
  (101,71,5) (101,71,3) (101,71,7)
  (102,71,4) (102,71,6)

Sealed facts (subject 103, fresh):
  (103,74,100)   <-- distractor relation, inserted FIRST
  (103,73,6) (103,73,9)
No (103,71,*) facts exist.

Learned structures (behaviors installed as prior learning; behavior
induction itself is not under test, per H1/H2 honest boundaries):

H1 MAPs:
  X (behav 0, SUM): sum of (s,param,v) objects. param=71 from training.
                    X(101)=15, X(102)=10. Learned sig NODE->NUM.
  Y (behav 1, ALLOC): integer division n/5. Y(15)=3, Y(10)=2.
                    Learned sig NUM->NUM.
  D1 (behav 3, MAX): max of (s,param,v) objects. param=71 from training.
                    D1(101)=7, D1(102)=6. Learned sig NODE->NUM.
                    Distractor: rebindable, wrong semantics.
  D2 (behav 2, IDENT): identity. D2(101)=101, D2(102)=102.
                    Learned sig NODE->NODE. Distractor.

H2 modes (capability evidence via has_behav):
  Mode 1 SUM (behav 0): sum of (s,rel,v) objects.
  Mode 2 ALLOC (behav 1): n/5.
  Mode 3 MAX (behav 2): max of (s,rel,v) objects. Distractor.

Sealed goal Z: (103,93)->3.
Requires: rebind X to r=73, X'(103)=15, then Y(15)=3.
The distractor r=74 gives X''(103)=100, Y(100)=20, which must be
rejected by composition validation.

No paired X+Y training. No hint. No task label. No researcher mapping.
No L2-specific domain template. The rebind target (73) is discovered by
scanning the sealed world's facts for the query subject, not from source.

## L2 Mechanism (generic, not domain-specific)

REBIND operator: given MAP m with a bindable parameter (relation field)
and a candidate relation cr from the sealed world, create m' as a copy
of m with param=cr, inheriting m's learned signature, recording
rebound_of=m. Then attempt composition with m' in place of m.

Candidate relations: distinct r such that (s,r,*) is a fact for the
query subject s. Collected by the learner at solve time. Contains no
domain knowledge.

The operator is generic machinery (like the composer itself). The
BINDING (X->73, not X->74, not D1->73) is learner-determined by
type-contract filtering and composition validation against the sealed
goal.

## Arms (H1)

  TREAT-L2: teach X,Y,D1,D2; solve_z(103,3,type_on=1,l2_on=1).
  L1-ONLY:  teach X,Y,D1,D2; solve_z(103,3,type_on=1,l2_on=0). Must FAIL.
  ABL-X:    teach, delete X; solve l2_on=1. Must FAIL.
  ABL-Y:    teach, delete Y; solve l2_on=1. Must FAIL.
  FRESH:    facts only; solve l2_on=1. Must FAIL.

## Arms (H2)

  TREAT-L2: teach; vc_compose_l2(103,93,3,l2_on=1).
  L1-ONLY:  teach; vc_compose_l2(103,93,3,l2_on=0). Must FAIL.
  ABL-X:    teach, delete behav 0; l2_on=1. Must FAIL.
  ABL-Y:    teach, delete behav 1; l2_on=1. Must FAIL.
  FRESH:    facts only; l2_on=1. Must FAIL.

## Kill Bars (frozen)

  K1 H1-L2-SOLVE: TREAT-L2 solves (103,3). Composite Z has comp_a = rebound
       MAP with param=73 and rebound_of=X, comp_b=Y. Correct provenance.
  K2 H2-L2-SOLVE: TREAT-L2 solves (103,3). Composite records
       m1=SUM, rel=73, m2=ALLOC.
  K3 L1-NECESSARILY-FAILS: L1-ONLY fails for both H1 and H2.
       (Proves adaptation was necessary, not just L1 with extra steps.)
  K4 CAUSAL: ABL-X, ABL-Y, FRESH fail for both H1 and H2 (with l2_on=1).
  K5 REBIND-DISCOVERED: grep audit confirms the rebind target 73 appears
       ONLY in add_fact lines (world setup), never in the rebind/scan/
       composer logic. The candidate scan is generic.
  K6 DETERMINISM: 3 full runs byte-identical per program (sha256 recorded).
  K7 NO-TEMPLATE: grep confirms no L2-specific domain literals in the
       composer/rebind logic (no hardcoded X->73, no 103/15/3 in logic).

## Verdict Rule

XDOMAIN-L2-COMPLETE iff K1-K7 all PASS.
If any bar fails, verdict is FAIL with the failing bar named.
H1 and H2 are measured separately; a partial result (one passes, one
fails) is reported honestly.

## Predicted Outcome (pre-registered)

H1: Phase 1 (L1) fails. Phase 2 tries rebind X->74 (validates to 100,
Y(100)=20, rejected), then X->73 (X'=15, Y(15)=3, success). Composite
promoted with rebound provenance. D1 rebind never reached (X succeeds
first, and D1->73 would give 9->1 anyway).

H2: L1 (rel=71) fails all 9 mode pairs. L2 tries rel=74 (all fail),
then rel=73: (SUM,ALLOC) gives 15->3, success.

## Honest Boundaries (declared in advance)

- Behavior implementations (SUM/ALLOC/MAX/IDENT, parameterized) are
  researcher-authored, representing previously learned structures.
  Under test is whether the LEARNER drives the rebinding, not behavior
  induction.
- The REBIND operator (copy MAP, set param, inherit signature) is
  generic researcher-authored machinery, like the composer. The
  binding decision (which MAP, which relation) is learner-driven.
- Expected answers used for verification (same as H1/H2). Learner-owned
  verification is future work.
- Binary NODE/NUM kinds from syntactic probe (same as H1).
- One L2 form (rebinding). Extension, truncation, specialization are
  separate future experiments.
- One domain pair (arithmetic->planning with relation shift).
- The distractor relation r=74 is inserted before r=73 in fact order so
  the candidate scan encounters it first; this tests discrimination,
  not luck. The scan logic itself is order-agnostic.
