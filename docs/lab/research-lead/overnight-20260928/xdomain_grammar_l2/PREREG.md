# PREREG: xdomain_grammar_l2 -- Level 2 Adaptive Reuse on Grammar to Program

Frozen 2026-10-02, before implementation. Any change requires a new
prereg; this document is never edited after freezing. Committed ALONE
before any implementation file exists.

## Hypothesis

H1 (learned typed contracts) and H2 (value-level function composition),
which drive L1 exact reuse on grammar to construction
(XDOMAIN-GRAMMAR-CONSTRUCT-COMPLETE, the fourth H1/H2 pair), can also
drive L2 ADAPTIVE reuse when a sealed world requires adapting the
grammar's licensed program length itself. Given two generic adaptation
operators (TRUNCATE the licensed length; EXTEND the licensed length),
the LEARNER selects the correct operator per sealed goal and discovers
the correct parameter from the sealed world, with no researcher
supplied mapping and no domain-pair template.

## World design (new sealed worlds; grammar to program)

Relations: r=71 grammar parameter ("rule licenses max program
length"), r=72 distractor parameter, r=93 sealed query.

Training facts (source range):
  (1,71,2): rule 1 licenses max program length 2 (short sentences).
  (2,71,4): rule 2 licenses max program length 4 (long sentences).
  (1,72,7) (2,72,5): distractor hi facts.

Learned structures (installed as prior learning; behavior induction
itself is not under test, per the H1/H2 honest boundaries):

  X (behav 0, PARAM): grammar parameter extraction. X(rule) =
    find_obj(rule,71). X(1)=2, X(2)=4. Learned sig NODE->NODE via the
    kind probe (2 is a fact subject, hence NODE; the contract still
    type-checks because X.out-kind equals Y.in-kind).
  Y (behav 1, EXEC): program executor. Y(L) runs the canonical L-op
    program (L unit ops) and returns its trace encoding, the repunit
    of length L: Y(1)=1, Y(2)=11, Y(3)=111, Y(4)=1111. Returns -1 for
    L<1 or on i32 overflow (generic guard, not domain knowledge).
    Learned sig NODE->NUM via the kind probe (taught on input 2).
  D1 (behav 2): D1(rule) = find_obj(rule,72). D1(1)=7, D1(2)=5.
    Sig NODE->NUM. Distractor.
  D2 (behav 3, identity): D2(v)=v. Sig NODE->NODE. Distractor.

Kinds via probe_kind (H1 lineage): a value that appears as a fact
subject is NODE (1), else NUM (2). Subjects are 1 and 2.

Sealed World-E (extend world):
  No new facts. Sealed goal Z-E: (1,93) -> 1111.
  Requires EXTEND: the grammar was learned on short sentences
  (rule 1 licenses length 2), but the sealed goal needs a longer
  program (length 4). Exact reuse gives X(1)=2, Y(2)=11, which misses.
  EXTEND(X,4) rebinds the licensed length to 4; Y(4)=1111.
  TRUNCATE k=1 gives Y(1)=1, also a miss.

Sealed World-T (truncate world):
  No new facts. Sealed goal Z-T: (2,93) -> 111.
  Requires TRUNCATE: the grammar licenses long programs (rule 2
  licenses length 4), but the sealed goal needs a shorter program
  (length 3). Exact reuse gives X(2)=4, Y(4)=1111, which misses.
  TRUNCATE(X,3) rebinds the licensed length to 3; Y(3)=111.
  EXTEND k=5..8 gives Y(5)=11111 and longer, all misses.
  The goal subject 2 is chosen with target 111 (not 11) so the
  unadapted single Y(2)=11 cannot solve in Phase 1; L1 failure is
  structural, not accidental.

No paired X+Y training. No hint. No task label. No researcher mapping.
No domain-pair template. The extend length (4) and the truncate
length (3) are discovered by the learner from generic candidate
ranges, not from source.

## L2 mechanisms (generic, not domain-specific)

TRUNCATE operator: given a PARAM MAP m with learned length L =
m(s) on the query subject s, and a candidate k with 1 <= k < L,
create m' as a copy of m with the licensed length rebound to k
(sig unchanged, behavior returns k), provenance adapt_of=m,
adapt_op=1, adapt_param=k.

EXTEND operator: given a PARAM MAP m with learned length L and a
candidate k with L < k <= 2*L (generic bound derived from L, no
domain literal), create m' as a copy of m with the licensed length
rebound to k, provenance adapt_of=m, adapt_op=2, adapt_param=k.

Candidate ranges are pure arithmetic on the learned L. No domain
knowledge. The rebound value is learner-discovered by exhaustive
try-and-reject.

Phase 2 tries TRUNCATE first, then EXTEND (fixed order), over all
candidates, retrying typed composition each time, and records every
success; exactly one success per world is required. Selection is
proven by exhaustive try-and-reject, not by order.

Scope (declared): adaptation applies to PARAM (behav 0) MAPs only;
EXEC, D1, D2 MAPs are used as taught. Phase 2 tries adapted MAPs in
pairs only (singles X'(s)=k can never equal a goal: k <= 2*L <= 8
while both goals are >= 111). The adapted PARAM map returns the
rebound length (a rebind for the sealed query); the operator choice
and the parameter value are learner-driven, which is what is under
test.

## Arms (H1, per world W in {E,T})

  TREAT:   teach; solve_z(s, target, l2_on=1). Must SUCCEED with
           exactly one successful adaptation using the correct
           operator and parameter (E: EXTEND k=4, comp_b=Y;
           T: TRUNCATE k=3, comp_b=Y), comp_a a provenanced
           adaptation of X.
  L1-ONLY: teach; solve_z(s, target, l2_on=0). Must FAIL.
  ABL-X:   teach, delete X; solve_z(..., l2_on=1). Must FAIL.
  ABL-Y:   teach, delete Y; solve_z(..., l2_on=1). Must FAIL.
  FRESH:   facts only; solve_z(..., l2_on=1). Must FAIL.

## Arms (H2, per world W in {E,T})

Same five arms with vc_compose_l2. Modes: 1=GRAMMAR (extract licensed
length via r=71, requires X learned as capability evidence),
2=PROGRAM (execute canonical program, requires Y learned as
capability evidence). Inherited H2 mechanism vocabulary, not new
cognitive modes. Stage 1 is the grammar extraction; the adaptation
(op 0=none, 1=TRUNCATE, 2=EXTEND, param) applies to stage 1 as a
rebind of the licensed length; stage 2 is the program executor.
Success record: (m1, m2, op, param); exactly one success required
(E: 1,2,2,4; T: 1,2,1,3).

## Kill bars (frozen)

  K-GP-1 SEALED-REQUIRES-ADAPTATION: Z-E is solvable only via EXTEND
       (the grammar licensed length 2 is too short for the length-4
       program the goal needs) and Z-T only via TRUNCATE (the
       licensed length 4 is too long for the length-3 program the
       goal needs). Established jointly by K-GP-2, K-GP-3, K-GP-4.
  K-GP-2 L1-NECESSARILY-FAILS: L1-ONLY fails in both worlds for both
       H1 and H2 (with l2_on=0). Proves adaptation was necessary.
  K-GP-3 CORRECT-OPERATOR-SELECTED: In World-E the single successful
       adaptation uses EXTEND with k=4 and every TRUNCATE candidate
       is tried and rejected; in World-T the single success uses
       TRUNCATE with k=3 and every EXTEND candidate is tried and
       rejected. Exactly one success per world per mechanism.
  K-GP-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: TREAT arms solve. H1:
       the composite records comp_a = adapted MAP with adapt_of=X,
       the correct adapt_op and adapt_param, and comp_b = Y.
       H2: the composite records the correct (m1, m2, op, param).
  K-GP-5 ABLATIONS-FAIL: ABL-X, ABL-Y, FRESH fail in both worlds for
       both H1 and H2 (with l2_on=1).
  K-GP-6 DETERMINISM: 3 full runs byte-identical per program (sha256
       recorded).
  K-GP-7 PARAMS-DISCOVERED: grep audit confirms the goal values
       (1111, 111) and the discovered parameters (4, 3) appear ONLY
       in world-setup fact lines, arm-harness query literals, and arm
       verdict checks (test oracle), never in the operator,
       candidate-range, or composer logic. The training lengths
       (2, 4) appear only in fact setup and teaching observations.
  K-GP-8 NO-TEMPLATE: grep audit confirms no GRAMMAR_TO_PROGRAM,
       GRAMMAR_PROGRAM, or other domain-pair literals in mechanism
       code (comments declaring their absence are allowed).
  K-GP-9 TOOLCHAIN: safebin active, `which python3 python` empty,
       pure Zag, pinned znc sha256 recorded, zero forbidden
       executable invocations.

## Verdict rule

XDOMAIN-GRAMMAR-L2-COMPLETE iff K-GP-1 through K-GP-9 all PASS.
If any bar fails, the verdict is FAIL with the failing bar named.
H1 and H2 are measured separately; a partial result is reported
honestly.

## Predicted outcome (pre-registered)

H1 World-E: TEACH X id=0 sig=1->1 (X(1)=2); Y id=1 sig=1->2
(Y(2)=11); D1 id=2; D2 id=3. Phase 1: singles Y(1)=1, D1(1)=7;
pairs (X,Y) mid=2 r=11, (X,D1) mid=2 r=5, (D2,Y) mid=1 r=1,
(D2,D1) mid=1 r=7. All miss 1111. Phase 2: TRUNCATE k=1 tried and
rejected (r=1, r=7); EXTEND k=3 rejected (r=111, r=-1); EXTEND k=4
-> mid=4 -> Y(4)=1111 success. Exactly 1 success: op=EXTEND,
param=4, b=Y.
H1 World-T: Phase 1: singles Y(2)=11, D1(2)=5; pairs (X,Y) mid=4
r=1111, (X,D1) mid=4 r=-1, (D2,Y) mid=2 r=11, (D2,D1) mid=2 r=5.
All miss 111. Phase 2: TRUNCATE k=1 -> r=1 rejected, k=2 -> r=11
rejected, k=3 -> mid=3 -> Y(3)=111 success; EXTEND k=5..8 ->
r=11111..11111111 rejected. Exactly 1 success: op=TRUNCATE,
param=3, b=Y.
H2 World-E: Phase 1: (1,1) v1=2 v2=4; (1,2) v1=2 v2=11;
(2,1) v1=1 v2=2; (2,2) v1=1 v2=1. All miss 1111. Phase 2:
TRUNCATE k=1 rejected; EXTEND k=3 -> v2=111 rejected, k=4 ->
v2=1111 success. Exactly 1: (m1=1,m2=2,op=2,param=4).
H2 World-T: Phase 1: (1,1) v1=4 v2=-1; (1,2) v1=4 v2=1111;
(2,1) v1=11 v2=-1; (2,2) v1=11 v2=-1 (overflow guard). All miss
111. Phase 2: TRUNCATE k=1 -> v2=1, k=2 -> v2=11 rejected,
k=3 -> v2=111 success; EXTEND k=5..8 rejected. Exactly 1:
(m1=1,m2=2,op=1,param=3).
All L1-ONLY / ABL-X / ABL-Y / FRESH arms fail in both worlds for
both mechanisms. TOTAL 10/10 per binary.

## Honest boundaries (declared in advance)

- Behavior implementations (grammar parameter extraction, repunit
  program executor, distractor lookup, identity) are
  researcher-authored, representing previously learned structures.
  Under test is whether the LEARNER drives operator selection and
  parameter discovery, not behavior induction.
- The TRUNCATE and EXTEND operators (copy MAP, rebind the licensed
  length, keep signature, record provenance) are generic
  researcher-authored machinery, like the composer. The operator
  choice and parameter values are learner-driven.
- The adapted PARAM map returns the rebound length for the sealed
  query (a rebind, in the lineage of the arithmetic to planning L2
  rebind operator). Input-sensitivity of the rebound map is not
  claimed; the discovery of which bound is.
- Kinds are syntactic (probe_kind); 2 is NODE because it is a fact
  subject. The composition type-checks because X.out-kind equals
  Y.in-kind; no semantic kind claim is made.
- The repunit overflow guard is generic i32 safety, not domain
  knowledge.
- Expected answers used for verification (same as H1/H2 lineage).
  Learner-owned verification is future work.
- The fixed operator try order (TRUNCATE before EXTEND) is arbitrary
  researcher scaffolding; selection is proven by exhaustive
  try-and-reject, not by order.
- H2 modes (GRAMMAR, PROGRAM) are the inherited H2 mechanism
  vocabulary (capability slots), not new cognitive modes.
  0 new modes, 0 bridges, 0 handlers, 0 new semantic cases.
- One domain pair (grammar to program); two adaptation shapes
  (extend, truncate). The novelty under test is the operators and
  their selection, not the pair.
