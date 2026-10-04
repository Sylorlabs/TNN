# REPORT: xdomain_causal_l2 -- L2 Adaptive Reuse on Causal to Intervention

## Verdict: XDOMAIN-CAUSAL-L2-COMPLETE. All 8 frozen kill bars PASS.

## Mission

Test L2 adaptive reuse on the causal to intervention pair (Micah
priority 4 high-value pair). L1 exact reuse was DEMONSTRATED on this
pair (XDOMAIN-CAUSAL-INTERV-COMPLETE); arithmetic to planning L2 was
DEMONSTRATED (rebind, truncate, specialize). This work requires
ADAPTATION of the causal model itself: a sealed world where the causal
chain is too long for where the needed intervention attaches
(TRUNCATE), and a sealed world where the causal model was learned on
one variable range and the intervention is needed on a different range
(SPECIALIZE the viability threshold).

## Design

Learned causal model X: threshold-gated walk over r=91. From v,
follow causal links while the next node value is strictly greater
than T; T is learned at teach time as the minimum node value over
the training chains (computed as 11, never a source literal).
Intervention procedure Y: first-match lookup over r=92.
Distractors: D1 identity, D2 count of r=91 outgoing.

Sealed World-T: 3-step chain (41,91,42),(42,91,43),(43,91,44);
mid-chain intervention (43,92,105); endpoint intervention
(44,92,106) as distractor. Goal (41,93)->105. Exact reuse walks to
the endpoint and returns the distractor 106. The learner must
TRUNCATE the walk at depth 2 (discovered, not given).

Sealed World-S: 2-step chain (5,91,6),(6,91,7) on a lower value
range; intervention (7,92,112). Goal (5,93)->112. The learned
threshold (11) blocks the walk entirely. The learner must
SPECIALIZE the threshold to 5 (discovered from the sealed world's
node values, not given).

No paired X+Y training. No hint. No task label. No researcher
mapping. No domain-pair template.

## H1 results (cl_h1.zag, typed contracts)

3/3 byte-identical, sha256
`34504d7bd42fc820814108f911736c6b7566a103b970ff31a71b46e04722a179`.

Learned (from probe observations and computed threshold only):
- X: 1->1 (NODE->NODE), thresh=11, X(11)=13. Correct.
- Y: 1->2 (NODE->NUM), Y(13)=101. Correct.
- D1: 1->1. D2: 1->2. Correct.

TREAT-T:
- Phase 1: singles Y(41)=-1, D2(41)=1; pairs (X,Y)->106,
  (X,D2)->0, (D1,Y)->-1, (D1,D2)->1. L1-FAIL.
- Phase 2: SPECIALIZE over {41,42,43,44} all tried and rejected
  (106 or -1); TRUNCATE k=1 -> 42 -> -1 rejected; k=2 -> 43 ->
  Y(43)=105. Exactly 1 success.
- Z-COMP z=10 a=9 b=1. Z-PROV adapt_of=0 op=1 param=2.
- ARM-RESULT PASS.

TREAT-S:
- Phase 1: X(5)=5 (threshold blocks); singles Y(5)=-1, D2(5)=1;
  pairs (X,Y)->-1, (X,D2)->1, (D1,Y)->-1, (D1,D2)->1. L1-FAIL.
- Phase 2: SPECIALIZE T=5 -> 7 -> Y(7)=112. Exactly 1 success;
  T=6,7 rejected; TRUNCATE k=1 rejected (gate still blocks).
- Z-COMP z=5 a=4 b=1. Z-PROV adapt_of=0 op=2 param=5.
- ARM-RESULT PASS.

L1-ONLY-T/S, ABL-X-T/S, ABL-Y-T/S, FRESH-T/S: all fail as expected.
TOTAL 10/10.

## H2 results (cl_h2.zag, value-level composition)

3/3 byte-identical, sha256
`bfe37d69add725e73ebd684e658377c3f3abdb06208a0340a2a9be97236cf771`.

Modes: 1=WALK, 2=INTERVENE (inherited vocabulary, discovered pair,
not given). Stage 2 requires learned Y as capability evidence.

TREAT-T:
- Phase 1: (1,1)->44, (1,2)->106; (2,*) skipped. L1-FAIL.
- Phase 2: SPECIALIZE T=41->106, T=42,43,44->-1, all rejected;
  TRUNCATE k=1->-1 rejected; k=2 -> 43 -> interv(43)=105.
- VC-COMPOSE ok m1=1 m2=2 op=1 param=2. ARM-RESULT PASS.

TREAT-S:
- Phase 1: (1,1)->5, (1,2)->-1. L1-FAIL.
- Phase 2: SPECIALIZE T=5 -> 7 -> interv(7)=112; T=6,7 and
  TRUNCATE k=1 rejected.
- VC-COMPOSE ok m1=1 m2=2 op=2 param=5. ARM-RESULT PASS.

ABL-X (walk capability removed), ABL-Y (lookup capability removed),
FRESH (no behaviors): all fail as expected in both worlds.
TOTAL 10/10.

## Kill bars

- K-CI-1 SEALED-REQUIRES-ADAPTATION: PASS. Z-T needs TRUNCATE
  (endpoint walk yields distractor 106; only depth 2 reaches the
  mid-chain intervention 105). Z-S needs SPECIALIZE (learned
  threshold 11 blocks the new range; only T=5 opens it).
- K-CI-2 L1-NECESSARILY-FAILS: PASS. L1-ONLY fails in both worlds
  for both H1 and H2.
- K-CI-3 CORRECT-OPERATOR-SELECTED: PASS. World-T: single success
  TRUNCATE k=2, all 4 SPECIALIZE candidates tried and rejected.
  World-S: single success SPECIALIZE T=5, TRUNCATE candidate tried
  and rejected. Exactly one success per world per mechanism.
- K-CI-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: PASS. H1 composites
  record adapt_of=X with correct op/param and comp_b=Y; H2 records
  the correct (m1,m2,op,param).
- K-CI-5 ABLATIONS-FAIL: PASS. ABL-X, ABL-Y, FRESH fail in both
  worlds for both mechanisms with l2_on=1.
- K-CI-6 DETERMINISM: PASS. 3/3 byte-identical per binary (sha256
  recorded above and in NAMECHECK.md).
- K-CI-7 PARAMS-DISCOVERED: PASS. Grep audit: 105/112 occur only in
  world-setup facts, harness queries/verdicts, and comments; the
  truncate depth (2) and specialize threshold (5) never appear as
  mechanism literals; the learned threshold (11) is computed by
  chain_nodes_min, never hardcoded.
- K-CI-8 NO-TEMPLATE: PASS. No CAUSAL_TO_INTERVENTION,
  CAUSAL_INTERVENE, or domain-pair literals in mechanism code.

## Why this matters

This is the first L2 result on the causal to intervention pair, and
it exercises two adaptation shapes the L1 work never needed:
structural truncation of a learned causal walk (the chain outruns
the intervention point) and range specialization of a learned
threshold (the model was calibrated on one variable range and must
operate on another). In both cases the operators are generic
machinery, the selection is learner-driven by exhaustive
try-and-validate against the sealed goal, and the parameters are
discovered from the sealed world. The composition is not rebuilt
from scratch: the adapted MAP carries provenance back to the learned
structure.

## Honest boundaries

- Behavior implementations (threshold-gated walk, first-match
  lookup, identity, count) are researcher-authored prior learning;
  under test is learner-driven operator selection and parameter
  discovery, not behavior induction.
- TRUNCATE/SPECIALIZE are generic machinery; choice and parameters
  are learner-driven.
- Expected answers used for verification (H1/H2 lineage standard).
- Fixed operator order (SPECIALIZE before TRUNCATE) is scaffolding;
  selection is proven by exhaustive try-and-reject.
- H2 modes are inherited mechanism vocabulary, not new cognitive
  modes. 0 new modes, 0 bridges, 0 handlers, 0 new semantic cases.
- One domain pair; two adaptation shapes. The novelty under test is
  the operators and their selection, not the pair.

## Architecture accounting

- cl_h1.zag: mechanism follows the xdomain H1 lineage; new is the
  walk behavior and the two generic operators.
- cl_h2.zag: mechanism logic follows the xdomain H2 lineage; new is
  the stage 1 walk with stage-level adaptation.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Frozen TNN-2 untouched (both standalone).

## Toolchain

Safebin PATH throughout. `which python3 python` empty (NAMECHECK
Step 0). Pinned znc 498abcb5, exit 0 both. Zero em/en dashes
byte-verified. Committed locally on tnn-native-lab, nothing pushed.

## Deliverables

- PREREG.md (frozen in commit 912044b54, strictly before
  implementation)
- NAMECHECK.md (Step 0 guard, build record, audit notes)
- REPORT.md (this file)
- cl_h1.zag, cl_h1_bin, cl_h1_compile.txt, cl_h1_run1/2/3.txt
- cl_h2.zag, cl_h2_bin, cl_h2_compile.txt, cl_h2_run1/2/3.txt
