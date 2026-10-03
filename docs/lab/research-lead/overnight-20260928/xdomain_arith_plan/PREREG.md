# PREREG: xdomain_arith_plan -- Cross-Domain Arithmetic to Planning

Frozen 2026-10-02, before implementation. Any change requires a new prereg;
this document is never edited after freezing.

## Hypothesis
H1's learned typed I/O contracts and H2's value-level function composition
are general cross-domain mechanisms, not chain-count specific. They will
solve an arithmetic-procedure to planning-allocation composition without
modification to the mechanism logic (only new behavior implementations
representing previously learned structures).

## World Design

Subjects: b1=101, b2=102 (basket nodes; appear as fact subjects).
Relation: has_price=71.
Facts (5):
  (101,71,5) (101,71,3) (101,71,7)   -> b1 item prices
  (102,71,4) (102,71,6)              -> b2 item prices

Learned structures (behaviors installed as prior learning; behavior
induction itself is not under test here, per H1/H2 honest boundaries):
  X (behav 0, SUM):   sum of (s,71,v) objects. X(101)=15, X(102)=10.
  Y (behav 1, ALLOC): integer division n/5 (packs affordable).
                      Y(15)=3, Y(10)=2, Y(7)=1.
  D1 (behav 2, MAX):  max of (s,71,v) objects. D1(101)=7, D1(102)=6.
                      Distractor: same signature as X, wrong semantics.
  D2 (behav 3, IDENT): identity. D2(101)=101.
                      Distractor: wrong signature.

Signature learning (H1 mechanism, verbatim logic):
  probe_kind(v) = 1 NODE iff v appears as a fact subject, else 2 NUM.
  Expected learned signatures:
    X: NODE->NUM, Y: NUM->NUM, D1: NODE->NUM, D2: NODE->NODE.

Sealed goal Z: (101,93)->3. Requires X(101)=15 then Y(15)=3.
Reuse goal Z2: (102,93)->2. Requires X(102)=10 then Y(10)=2.

No paired X+Y training. No hint. No task label. No researcher mapping
between arithmetic and planning. No ARITH_TO_PLAN template in source.

## Mechanisms Under Test

M1 (typed contracts, H1 logic): learn signatures from probe observations;
composer admits pair (A,B) iff sig(A).out==sig(B).in with goal-kind
endpoints; promote composite with contract in(A)->out(B).

M2 (value composition, H2 logic): try ordered MAP pairs (a,b);
mid=exec(a,s); r=exec(b,mid); promote on r==target. No type filter.

## Arms
  TREAT-TYPED: teach X,Y,D1,D2; solve_typed(101,3). Then solve_typed(102,2).
  TREAT-VALUE: teach X,Y,D1,D2; solve_value(101,3). Then solve_value(102,2).
  NOTYPE:      teach all; solve_typed with type filter OFF on (101,3).
  NOVC:        teach all; solve_value with pair search disabled (singles only).
  ABL-X:       teach all, delete X; both solvers on (101,3) must fail.
  ABL-Y:       teach all, delete Y; both solvers on (101,3) must fail.
  FRESH:       facts only, no teaching; both solvers on (101,3) must fail.

## Kill Bars (frozen)
  K1 SOLVE: TREAT-TYPED solves (101,3) via composite (X,Y); TREAT-VALUE
            solves (101,3) via ordered pair (X,Y). Both correct provenance.
  K2 CAUSAL: ABL-X fails, ABL-Y fails, FRESH fails, for BOTH solvers.
            (D1 alone must not solve: D1(101)=7 != 3. Verified by design.)
  K3 MECHANISM-CAUSAL:
            (a) NOTYPE solves but with strictly more tries than TREAT-TYPED
                (type filter prunes).
            (b) NOVC fails (pair search is load-bearing for M2).
  K4 LEARNED-NOT-ASSIGNED: audit confirms zero per-MAP signature literals
            in source; signatures only from probe observations.
  K5 DETERMINISM: 3 full runs byte-identical (sha256 recorded).
  K6 NO-TEMPLATE: grep confirms no ARITH_TO_PLAN, no hardcoded (X,Y) pair
            selection, no 101/102/15/3 literals in composer logic.
  K7 REUSE: Z2 (102,2) solved with cost <= TREAT cost (reuse, not rediscovery).

## Verdict Rule
XDOMAIN-ARITH-PLAN-COMPLETE iff K1-K7 all PASS.
If any bar fails, verdict is FAIL with the failing bar named.
A partial result (e.g., M1 passes but M2 fails) is reported honestly;
generality is per-mechanism, not assumed.

## Honest Boundaries (declared in advance)
- Behavior implementations (SUM/ALLOC/MAX/IDENT) are researcher-authored,
  representing previously learned structures. Under test is composition,
  not behavior induction.
- Expected answers used for verification (same as H1/H2). Learner-owned
  verification is future work.
- Binary NODE/NUM kinds from syntactic probe (same as H1).
- Level 1 composition only (exact reuse of X and Y unchanged). Level 2
  (adaptive) and Level 3 (novel intermediate) are future work.
- One domain pair. Generality claim is bounded to: mechanism logic
  unmodified from H1/H2, new structurally-different domains.
