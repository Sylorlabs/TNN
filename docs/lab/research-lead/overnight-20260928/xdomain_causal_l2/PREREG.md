# PREREG: xdomain_causal_l2 -- Level 2 Adaptive Reuse on Causal to Intervention

Frozen 2026-10-02, before implementation. Any change requires a new
prereg; this document is never edited after freezing. Committed ALONE
before any implementation file exists.

## Hypothesis

H1 (learned typed contracts) and H2 (value-level function composition),
which drive L1 exact reuse on causal to intervention
(XDOMAIN-CAUSAL-INTERV-COMPLETE), can also drive L2 ADAPTIVE reuse when
a sealed world requires adapting the causal model itself. Given two
generic adaptation operators (TRUNCATE the causal walk depth;
SPECIALIZE the causal walk viability threshold to a new value range),
the LEARNER selects the correct operator per sealed goal and discovers
the correct parameter from the sealed world, with no researcher
supplied mapping and no domain-pair template.

## World design (new sealed worlds; L1 pair is the base)

Relations: r=91 causal ("causes"), r=92 intervention ("is addressed
by"), r=93 sealed query.

Training facts (source range):
  (11,91,12) (12,91,13): 2-step causal chain, endpoint 13.
  (21,91,22) (22,91,23): 2-step causal chain, endpoint 23.
  (13,92,101): outcome 13 needs intervention 101.
  (23,92,102) (23,92,103): outcome 23 needs 102 (first) or 103.

Learned structures (installed as prior learning; behavior induction
itself is not under test, per the H1/H2 honest boundaries):

  X (behav 0, WALK): threshold-gated causal walk. From v, follow r=91
    while the next node value is strictly greater than T; T is learned
    at teach time as the minimum node value over the training chains
    (computed, equals 11, never a source literal). Return the endpoint.
    Learned sig NODE->NODE via the kind probe.
  Y (behav 1, LOOKUP): find_obj(v,92), first match. Learned sig
    NODE->NUM via the kind probe.
  D1 (behav 2, identity): D1(v)=v. Sig NODE->NODE. Distractor.
  D2 (behav 3, count r=91 outgoing): Sig NODE->NUM. Distractor.

Kinds via probe_kind (H1 lineage): a value that appears as a fact
subject is NODE (1), else NUM (2).

Sealed World-T (truncate world):
  (41,91,42) (42,91,43) (43,91,44): 3-step chain, all values above the
  learned threshold, so the gate is transparent.
  (43,92,105): mid-chain intervention.
  (44,92,106): endpoint intervention (distractor).
Sealed goal Z-T: (41,93) -> 105.
  Requires TRUNCATE: exact X(41)=44 (endpoint walk), Y(44)=106, which
  misses the goal. TRUNCATE(X,2)(41)=43, then Y(43)=105.
  The causal chain is too long for where the needed intervention
  attaches; the walk must be truncated, not rebound.

Sealed World-S (specialize world):
  (5,91,6) (6,91,7): 2-step chain on a LOWER value range than the
  source range; every value is at or below the learned threshold.
  (7,92,112): endpoint intervention.
Sealed goal Z-S: (5,93) -> 112.
  Requires SPECIALIZE: the learned threshold (11) blocks the walk
  (6 > 11 is false), so exact X(5)=5 and Y(5) misses. SPECIALIZE(X,5)
  sets T=5 for the sealed range; the walk goes 5->6->7, Y(7)=112.
  The causal model was learned on one variable range; the intervention
  is needed on a different range, so the threshold must be specialized.

No paired X+Y training. No hint. No task label. No researcher mapping.
No domain-pair template. The truncate depth (2) and the specialize
threshold (5) are discovered by the learner from generic candidate
scans of the sealed world, not from source.

## L2 mechanisms (generic, not domain-specific)

TRUNCATE operator: given a walk MAP m and a candidate depth k with
1 <= k < len (len = r=91 chain length from the query subject), create
m' as a copy of m with a depth cap of k (the threshold gate still
applies), sig unchanged, provenance adapt_of=m, adapt_op=1,
adapt_param=k.

SPECIALIZE operator: given a walk MAP m and a candidate threshold T
from the distinct node values reachable from the query subject over
r=91 (first-seen order), create m' as a copy of m with threshold T,
sig unchanged, provenance adapt_of=m, adapt_op=2, adapt_param=T.

Candidate depths: every integer k in 1..(len-1); generic range, no
domain literals. Candidate thresholds: the generic reachability scan
described above; no domain knowledge.

Phase 2 tries SPECIALIZE first, then TRUNCATE (fixed order), over all
candidates, retrying typed composition each time, and records every
success; exactly one success per world is required. Selection is
proven by exhaustive try-and-reject, not by order.

Scope (declared): adaptation applies to walk (behav 0) MAPs only;
lookup, identity, and count MAPs are used as taught. Phase 2 tries
adapted MAPs in pairs only (singles cannot type-check: NODE output
vs NUM goal).

## Arms (H1, per world W in {T,S})

  TREAT:   teach; solve_z(s, target, l2_on=1). Must SUCCEED with
           exactly one successful adaptation using the correct
           operator and parameter (T: TRUNCATE k=2, comp_b=Y;
           S: SPECIALIZE T=5, comp_b=Y), comp_a a provenanced
           adaptation of X.
  L1-ONLY: teach; solve_z(s, target, l2_on=0). Must FAIL.
  ABL-X:   teach, delete X; solve_z(..., l2_on=1). Must FAIL.
  ABL-Y:   teach, delete Y; solve_z(..., l2_on=1). Must FAIL.
  FRESH:   facts only; solve_z(..., l2_on=1). Must FAIL.

## Arms (H2, per world W in {T,S})

Same five arms with vc_compose_l2. Modes: 1=WALK, 2=INTERVENE
(inherited H2 mechanism vocabulary, not new cognitive modes). Stage 1
is the threshold-gated walk; the adaptation (op 0=none, 1=TRUNCATE,
2=SPECIALIZE, param) applies to the stage 1 walk; stage 2 is the
intervention lookup and requires the learned Y behavior as capability
evidence via has_behav. Success record: (m1, m2, op, param); exactly
one success required (T: 1,2,1,2; S: 1,2,2,5).

## Kill bars (frozen)

  K-CI-1 SEALED-REQUIRES-ADAPTATION: Z-T is solvable only via TRUNCATE
       (the chain is too long for the mid-chain intervention; the
       endpoint walk yields the distractor 106) and Z-S only via
       SPECIALIZE (the learned threshold blocks the new value range).
       Established jointly by K-CI-2, K-CI-3, K-CI-4.
  K-CI-2 L1-NECESSARILY-FAILS: L1-ONLY fails in both worlds for both
       H1 and H2 (with l2_on=0). Proves adaptation was necessary.
  K-CI-3 CORRECT-OPERATOR-SELECTED: In World-T the single successful
       adaptation uses TRUNCATE with k=2 and every SPECIALIZE
       candidate is tried and rejected; in World-S the single success
       uses SPECIALIZE with T=5 and every TRUNCATE candidate is tried
       and rejected. Exactly one success per world per mechanism.
  K-CI-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: TREAT arms solve. H1:
       the composite records comp_a = adapted MAP with adapt_of=X,
       the correct adapt_op and adapt_param, and comp_b = Y.
       H2: the composite records the correct (m1, m2, op, param).
  K-CI-5 ABLATIONS-FAIL: ABL-X, ABL-Y, FRESH fail in both worlds for
       both H1 and H2 (with l2_on=1).
  K-CI-6 DETERMINISM: 3 full runs byte-identical per program (sha256
       recorded).
  K-CI-7 PARAMS-DISCOVERED: grep audit confirms the goal values (105,
       112) and the discovered parameters (2, 5) appear ONLY in
       world-setup fact lines and arm-harness query literals, never
       in the operator, candidate-scan, threshold-learning, or
       composer logic.
  K-CI-8 NO-TEMPLATE: grep audit confirms no CAUSAL_TO_INTERVENTION,
       CAUSAL_INTERVENE, or other domain-pair literals in mechanism
       code (comments declaring their absence are allowed).

## Verdict rule

XDOMAIN-CAUSAL-L2-COMPLETE iff K-CI-1 through K-CI-8 all PASS.
If any bar fails, the verdict is FAIL with the failing bar named.
H1 and H2 are measured separately; a partial result is reported
honestly.

## Predicted outcome (pre-registered)

H1 World-T: Phase 1 fails. Singles: Y(41)=-1, D2(41)=1. Pairs:
(X,Y)->106, (X,D2)->0, (D1,Y)->-1, (D1,D2)->1. Phase 2: SPECIALIZE
over {41,42,43,44} all rejected (106 or -1); TRUNCATE k=1 -> 42 ->
-1 rejected; k=2 -> 43 -> Y(43)=105 success; (X',D2)->1 rejected.
Exactly 1 success: op=TRUNCATE, param=2, b=Y.
H1 World-S: Phase 1 fails. X(5)=5 (threshold blocks). Singles:
Y(5)=-1, D2(5)=1. Pairs: (X,Y)->-1, (X,D2)->1, (D1,Y)->-1,
(D1,D2)->1. Phase 2: SPECIALIZE T=5 -> 7 -> Y(7)=112 success;
T=6,7 -> 5 -> -1 rejected; TRUNCATE k=1 -> 5 (gate still blocks) ->
-1 rejected. Exactly 1 success: op=SPECIALIZE, param=5, b=Y.
H2: same outcomes via stage pairs (T: m1=1,m2=2,op=1,param=2;
S: m1=1,m2=2,op=2,param=5). ABL-X/ABL-Y/FRESH fail everywhere.

## Honest boundaries (declared in advance)

- Behavior implementations (threshold-gated walk, first-match
  lookup, identity, count) are researcher-authored, representing
  previously learned structures. Under test is whether the LEARNER
  drives operator selection and parameter discovery, not behavior
  induction.
- The TRUNCATE and SPECIALIZE operators (copy MAP, set depth cap or
  threshold, keep signature, record provenance) are generic
  researcher-authored machinery, like the composer. The operator
  choice and parameter values are learner-driven.
- The learned threshold (11) is computed as the minimum training
  node value, not a literal; K-CI-7 audits this.
- Expected answers used for verification (same as H1/H2 lineage).
  Learner-owned verification is future work.
- The fixed operator try order (SPECIALIZE before TRUNCATE) is
  arbitrary researcher scaffolding; selection is proven by
  exhaustive try-and-reject, not by order.
- H2 modes (WALK, INTERVENE) are the inherited mechanism vocabulary
  (capability slots from the H2 lineage), not new cognitive modes.
  0 new modes, 0 bridges, 0 handlers, 0 new semantic cases.
- One domain pair (causal to intervention); two adaptation shapes.
  The domain gap is modest by design; the novelty under test is the
  operators and their selection, not the pair.
