# PREREG: xdomain_l2_ts -- Level 2 TRUNCATE and SPECIALIZE Adaptation

Frozen 2026-10-02, before implementation. Any change requires a new prereg;
this document is never edited after freezing.

## Hypothesis

H1 (learned typed contracts) and H2 (value-level function composition),
which drive L2 adaptive reuse via REBIND on arithmetic to planning
(XDOMAIN-L2-COMPLETE), can also drive two DIFFERENT L2 adaptation shapes
on a NEW sealed world: TRUNCATE (X produces a longer structure than the
downstream contract accepts) and SPECIALIZE (X is too general for what the
downstream computation needs). Given both operators as generic machinery,
the LEARNER selects the correct operator per sealed goal and discovers the
correct parameter from the sealed world, with no researcher supplied
mapping and no domain-pair template.

## World Design (new sealed world, different from the rebind world)

Relation 61 throughout (no relation shift; the adaptation under test is
not rebinding). Two sealed subjects, two sealed goals.

Training facts (relation 61, sensor sweeps of 5 readings):
  (101,61,2) (101,61,4) (101,61,6) (101,61,8) (101,61,10)
  (102,61,1) (102,61,3) (102,61,5) (102,61,7) (102,61,9)
  (201,61,2) (201,61,4) (201,61,6)
  (202,61,1) (202,61,3) (202,61,5)

Sealed facts, World-T (truncate world), fresh subject 103:
  (103,61,3) (103,61,1) (103,61,4) (103,61,1) (103,61,5)

Sealed facts, World-S (specialize world), fresh subject 104:
  (104,61,2) (104,61,7) (104,61,3) (104,61,8) (104,61,4)

Learned structures (behaviors installed as prior learning; behavior
induction itself is not under test, per the H1/H2 honest boundaries):

  X (behav 0, SWEEP): collect readings of (s,param,v) in first-seen
    order, hardware cap 5. Learned sig NODE->SEQ5 (both training sweeps
    yield length 5).
  Y1 (behav 1, PLAN3): sum of exactly 3 readings (3-phase plan total).
    Learned sig SEQ3->NUM (taught on the two 3-reading sweeps of 201, 202).
  D (behav 2, RISK3): product of exactly 3 readings (3-factor risk).
    Learned sig SEQ3->NUM. Semantic distractor: same contract as Y1,
    wrong semantics.
  Y2 (behav 3, TOTAL): sum of all readings, any length. Learned sig
    SEQANY->NUM (taught on a 3-sweep and a 5-sweep; varying observed
    length generalizes the input contract).

Kinds: 1=NODE, 2=NUM, 10+k=SEQk (fixed length k), 20=SEQANY.
Contract compatibility: exact match, or SEQANY on either side against a
fixed SEQk on the other (optimistic; runtime length checks still apply).
Signature learning rule (declared): consistent observed length L across
teaching observations gives SEQ L; varying observed lengths give SEQANY;
subject-kind inputs give NODE via the syntactic probe.

Sealed goal Z-T: (103,93)->8.
  Requires TRUNCATE: X(103) yields 5 readings [3,1,4,1,5] (SEQ5), but Y1
  demands SEQ3. TRUNCATE(X,3)(103) = [3,1,4], then PLAN3 = 8.
  X is too long; exact L1 reuse is blocked by the contract.
Sealed goal Z-S: (104,94)->15.
  Requires SPECIALIZE: X(104) yields [2,7,3,8,4]; TOTAL gives 24, not 15.
  X is too general (unfiltered sweep). SPECIALIZE(X,7)(104) keeps readings
  >= 7, i.e. [7,8], then TOTAL = 15.
  X is too general; exact L1 reuse validates the contract but not the goal.

No paired X+Y training. No hint. No task label. No researcher mapping.
No L2-specific domain template. The truncate length (3) and the specialize
threshold (7) are discovered by the learner from generic candidate scans
of the sealed world, not from source.

## L2 Mechanisms (generic, not domain-specific)

TRUNCATE operator: given a sequence-producing MAP m and a candidate length
k shorter than m's observed output length on the query subject, create m'
as a copy of m that keeps only the first k elements, with sig_out = SEQk
and truncate_of = m provenance.

SPECIALIZE operator: given a sequence-producing MAP m and a candidate
threshold T from the distinct observed values of the query subject, create
m' as a copy of m that keeps only elements >= T, with sig_out = SEQANY
(length not known until runtime) and specialize_of = m provenance.

Candidate lengths: every k in 1..(len-1) where len is the observed sweep
length on the query subject (generic integer range, no domain literals).
Candidate thresholds: distinct values v with a fact (s,61,v) for the query
subject s, first-seen order (generic scan, no domain knowledge).

The operators are generic machinery (like the composer). The SELECTION
(TRUNCATE for Z-T, SPECIALIZE for Z-S) and the PARAMETERS (k=3, T=7) are
learner-determined by exhaustive try-and-validate against the sealed goal.
Phase 2 tries SPECIALIZE first, then TRUNCATE (fixed order), over all
candidates, and records every success; exactly one success per world is
required.

Scope (declared): adaptation applies to stage-1 (X-like) MAPs only;
stage-2 MAPs are used as taught. Phase 2 tries adapted MAPs in pairs only
(singles cannot type-check: SEQ output vs NUM goal).

## Arms (H1, per world W in {T,S})

  TREAT:   teach; solve_z(s, target, type_on=1, l2_on=1). Must SUCCEED
           with exactly one successful adaptation using the correct
           operator and parameter (T: TRUNCATE k=3, comp_b=Y1;
           S: SPECIALIZE T=7, comp_b=Y2), comp_a a provenanced
           adaptation of X.
  L1-ONLY: teach; solve_z(..., l2_on=0). Must FAIL.
  ABL-X:   teach, delete X; solve l2_on=1. Must FAIL.
  ABL-Y:   teach, delete Y; solve l2_on=1. Must FAIL.
  FRESH:   facts only; solve l2_on=1. Must FAIL.

## Arms (H2, per world W in {T,S})

Same five arms with vc_compose_l2. Modes: World-T uses 1=SWEEP, 2=PLAN3,
3=RISK3; World-S uses 1=SWEEP, 4=TOTAL. Stage 1 writes the shared
sequence buffer; stage 2 reads it (value passing between stages).
Capability evidence via has_behav, as in the H2 lineage. Success record:
(m1, m2, op, param); exactly one success required
(T: op=TRUNCATE, param=3, m1=1, m2=2; S: op=SPECIALIZE, param=7, m1=1,
m2=4).

## Kill Bars (frozen)

  K-TS-1 SEALED-REQUIRES-ADAPT: Z-T is solvable only via TRUNCATE (X too
       long: SEQ5 output against a SEQ3 contract) and Z-S only via
       SPECIALIZE (X too general: unfiltered sweep). Established jointly
       by K-TS-2, K-TS-3, K-TS-4.
  K-TS-2 L1-NECESSARILY-FAILS: L1-ONLY fails in both worlds for both H1
       and H2 (with l2_on=0). Proves adaptation was necessary.
  K-TS-3 CORRECT-OPERATOR-SELECTED: In World-T the single successful
       adaptation uses TRUNCATE with k=3 and every SPECIALIZE candidate
       is tried and rejected; in World-S the single success uses
       SPECIALIZE with T=7 and every TRUNCATE candidate is tried and
       rejected. Exactly one success per world per mechanism.
  K-TS-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: TREAT arms solve. H1: the
       composite records comp_a = adapted MAP with adapt_of=X, the
       correct adapt_op and adapt_param, and comp_b = the correct Y
       (World-T: Y1; World-S: Y2). H2: the composite records the correct
       (m1, m2, op, param).
  K-TS-5 CAUSAL: ABL-X, ABL-Y, FRESH fail in both worlds for both H1 and
       H2 (with l2_on=1).
  K-TS-6 DETERMINISM: 3 full runs byte-identical per program (sha256
       recorded).
  K-TS-7 PARAMS-DISCOVERED: grep audit confirms the goal values (8, 15)
       and the discovered parameters (3, 7) appear ONLY in add_fact
       world-setup lines and arm-harness query literals, never in the
       operator, candidate-scan, or composer logic.

## Verdict Rule

XDOMAIN-L2-TS-COMPLETE iff K-TS-1 through K-TS-7 all PASS.
If any bar fails, verdict is FAIL with the failing bar named.
H1 and H2 are measured separately; a partial result (one passes, one
fails) is reported honestly.

## Predicted Outcome (pre-registered)

H1 World-T: Phase 1 fails (no pair type-checks: SEQ5 vs SEQ3). Phase 2:
SPECIALIZE over {3,1,4,5} all fail (12/60 on T=3; length rejects on
T=1,4,5); TRUNCATE over {1,2,3,4}: k=3 gives [3,1,4], PLAN3 = 8, success
(RISK3 gives 12, rejected); k=1,2,4 length-rejected. Exactly 1 success:
op=TRUNCATE, k=3, b=Y1.
H1 World-S: Phase 1: (SWEEP,TOTAL) gives 24, rejected. Phase 2:
SPECIALIZE over {2,7,3,8,4}: T=7 gives [7,8], TOTAL = 15, success; others
give 24/22/19/8, rejected. TRUNCATE over {1,2,3,4} gives 2/9/12/20,
rejected. Exactly 1 success: op=SPECIALIZE, T=7, b=Y2.
H2: same outcomes via stage pairs (T: m1=1,m2=2,op=TRUNCATE,param=3;
S: m1=1,m2=4,op=SPECIALIZE,param=7).

## Honest Boundaries (declared in advance)

- Behavior implementations (SWEEP/PLAN3/RISK3/TOTAL) are
  researcher-authored, representing previously learned structures.
  Under test is whether the LEARNER drives operator selection, not
  behavior induction.
- The TRUNCATE and SPECIALIZE operators (copy MAP, set length/threshold,
  adjust contract, record provenance) are generic researcher-authored
  machinery, like the composer. The operator choice and parameter values
  are learner-driven.
- Expected answers used for verification (same as H1/H2 lineage).
  Learner-owned verification is future work.
- Sequence kinds from observed lengths (same spirit as H1's syntactic
  probe); the consistent/varying length rule is declared above.
- One domain pair (sensing/aggregation to planning); two adaptation
  shapes. The domain gap is modest by design; the novelty under test is
  the operators and their selection, not the pair.
- H2 "modes" are the inherited mechanism vocabulary (capability slots
  from the H2 lineage), not new cognitive modes. 0 new modes, 0 bridges,
  0 handlers, 0 new semantic cases.
- The fixed operator try order (SPECIALIZE before TRUNCATE) is arbitrary
  researcher scaffolding; selection is proven by exhaustive
  try-and-reject, not by order.
