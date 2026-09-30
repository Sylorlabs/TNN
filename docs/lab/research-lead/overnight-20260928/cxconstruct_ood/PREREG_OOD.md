# PREREG: OOD Test for H-CAUSALEXP-CONSTRUCT (Step 7 of promotion pipeline)

Date: 2026-09-30. Worker: OOD Test Worker.
Status: FROZEN. Committed before any implementation.

## Target

H-CAUSALEXP-CONSTRUCT, BUILD-PASS (7/7), result commit `48f2adc15`.
A2 alternative-explanation attack (step 6) downgraded it to bounded L2:
systematic exhaustive search over a researcher-bounded space
(1364 sequences, depth cap MAXD=5, fixed 4 primitives, delay-rule hypotheses).

This prereg defines four out-of-distribution test families. The frozen
learner is the committed `cxconstruct.zag` logic: 3 variables (X,Z,Y),
4 actions (S=0,W=1,OY=2,OZ=3), MAXD=5, hypotheses as delay-rule data,
first-disagreement selection in lexicographic order S<W<OY<OZ.

## K-OOD0: Reimplementation fidelity (gate)

I will independently reimplement the frozen learner in pure Zag from the
committed source semantics. It must reproduce the builder's committed
`CXCONSTRUCT_RAW.txt` exactly on all 4 configs:

- World A: SELECT seq=[S,W,OY] h0pred=0 h1pred=1; checked counts 2,12,3.
- World B: SELECT seq=[S,W,W,OY] h0pred=0 h1pred=1; checked counts 2,12,56,15.

If any SELECT output or checked count differs, HALT. The harness is wrong,
not the learner. No OOD verdict may be drawn from an unfaithful
reimplementation.

## OOD-1: Deeper worlds (depth boundary)

Worlds (delay rules, same 3-variable substrate):

- D1: H5=[(X,Z,5),(Z,Y,0)], H6=[(X,Y,4)]. True minimal depth: 6.
- D2: H7=[(X,Z,6),(Z,Y,0)], H8=[(X,Y,5)]. True minimal depth: 7.
- D3: H9=[(X,Z,7),(Z,Y,0)], H10=[(X,Y,6)]. True minimal depth: 8.

True minimal depths will be confirmed by an extended-depth exhaustive
search in a clearly labeled measurement harness (not the frozen learner).

Kill bar K-OOD1:
- OOD-1 = PASS if the frozen learner (MAXD=5, no source edits) emits a
  discriminating experiment for at least one of D1/D2/D3.
- OOD-1 = FAIL if it emits NO-DISCRIMINATING-SEQUENCE on all three.

A FAIL confirms the depth cap is load-bearing and maps the exact boundary
(required depth >= 6 defeats the frozen learner).

## OOD-2: Fifth primitive (action-set boundary)

World V uses a 4th variable V (V=3) and a 5th action OV=4 (observe V).
Hypotheses: H31=[(X,V,1)], H32=[(X,V,3)]. V affects no other variable.

Ground truth (extended harness with 4 variables and 5 actions):
- [S,W,W,OV] (depth 4): H31 predicts V=1 (2>=1); H32 predicts V=0 (2<3).
  Discriminates. The world is solvable in principle.

Kill bar K-OOD2:
- Count discriminating sequences in the frozen 4-action menu
  ({S,W,OY,OZ}, depths 1-5) under the extended simulator: call it n4.
- OOD-2 = PASS if n4 >= 1.
- OOD-2 = FAIL if n4 == 0.

A FAIL shows the fixed 4-action set is a hard boundary: V is unobservable
through Y/Z, so the frozen menu is blind by construction. The structural
fact (state layout hardcodes 3 variables; action dispatch hardcodes 0-3)
will also be documented from source audit.

## OOD-3: Inhibition law (hypothesis-space boundary)

True law (sealed world): Y = NOT X. Y defaults to 1; setting X:=1 forces
Y:=0. Z is always 0. This law is non-monotonic and inexpressible as delay
rules (the delay-rule simulator only turns variables on, never off).

Hypotheses (delay rules): H25=[(X,Y,1)], H26=[(X,Y,3)].
Both are false. The truth lies outside the hypothesis class.

Procedure: run the frozen learner end to end (construct, execute against
the sealed inhibition world, eliminate). Record the survivor set.

Kill bar K-OOD3:
- OOD-3 = PASS if the learner ends with zero survivors, or emits any
  explicit signal that the truth lies outside its hypothesis space.
- OOD-3 = FAIL if the learner ends with exactly one surviving hypothesis.

A FAIL demonstrates silent false convergence: the mechanism cannot
represent inhibition, cannot invent a new hypothesis form, and reports
success anyway. The survivor will additionally be checked against the
true law on a held-out experiment ([S,W,W,W,OY]: true Y=0) to confirm it
is false as a general law.

## OOD-4: Scale (combinatorial wall)

Measure checked(d) = number of depth-d sequences with >=1 observe action,
for d = 1..10, in a measurement harness (enumeration only).

Kill bar K-OOD4:
- OOD-4 = PASS if checked(d+1)/checked(d) < 2.0 for all d in 1..9
  (sub-exponential growth, implying pruning or guidance).
- OOD-4 = FAIL if the ratio is within [3.5, 4.5] for all d in 1..9
  (unpruned 4^d enumeration).

A FAIL maps the combinatorial wall: with no pruning, depth 10 requires
~1M simulations per hypothesis pair. Wall-clock time per depth will also
be reported.

## Overall verdict

- OOD-PASS: all four of OOD-1..4 PASS.
- OOD-PARTIAL: 1 to 3 of OOD-1..4 PASS.
- OOD-FAIL: 0 of OOD-1..4 PASS.

Prediction (not a bar): OOD-FAIL or OOD-PARTIAL. The A2 findings imply
the depth cap (OOD-1), action set (OOD-2), and hypothesis class (OOD-3)
are researcher-fixed boundaries, and the enumeration is unpruned (OOD-4).

## Rules

Pure Zag only. No Python at any stage, including scratch, editing,
verification, and measurement. No em dashes in any file. Commits local
only, owned path `docs/lab/research-lead/overnight-20260928/cxconstruct_ood/`
only. This prereg is committed alone before any `.zag` is written.
