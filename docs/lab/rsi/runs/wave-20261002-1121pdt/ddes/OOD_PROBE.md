# ADVERSARY OOD PROBE: t*=0 repair on structurally novel worlds

Wave: wave-20261002-1121pdt. Lane: DDES. Queue item 5(c).
Prereg: PREREG_DDES_RT10.md, frozen alone at dd5d92f63 before any
implementation. Same binary and transcripts as REDTEAM_STEP10.md
(ddes_rt.zag, ddes_rt_bin; 3/3 byte-identical, sha256
a8b1ce04009698b0f6c698937c6a502cc5f47ed6b16d814050430f451ce2a780;
exit 0; zero stderr). Mechanism byte-identical to the frozen
repair ddesr2.zag at b42b10db5.

Probe question: the repair's development worlds are Worlds A-E
(single-hop X to V, positive delays, t* in {1,2,3,4}) and World F
(single 0-delay rule X to Y). Do the repair's boundary behaviors
(the clamp floor, the TSTAR-ZERO-BOUNDARY flag, correct
convergence) hold on worlds structurally unlike all of them?

Binding caveats (restated; they bind every citation): (1) "a menu of
size 2 reproduces the sealed phase-2 outputs"; (2) "World G is
signature-identical to F by prereg design"; (3) "the
derivation-to-record binding is enforced by offline reviewer checks
only". Ceiling: bounded L2, NOT L3. Honest bound (cf. REDTEAM_SELF
R1): probe designer and prediction author share a head; the
predictions were frozen before implementation, were falsifiable and
specific, and the battery includes structural dimensions the
mechanism's development never exercised.

## Probe worlds (all designed post-repair, frozen before running)

P1: t*=0 discriminating on Z, not Y. H0=[(X,Z,0)] vs H1=[(X,Z,4)].
  (All repair-family worlds discriminate on Y, or on Z only with
  positive delays.)
P2: t*=0 with coexisting 0-delay and positive-delay rules from X.
  H0=[(X,Y,0),(X,Z,2)] vs H1=[(X,Y,5),(X,Z,2)]. (F had one rule.)
P3: t*=0 with INF arrival on the observed variable under H0;
  frontier picks Z while Y agrees at 0. H0=[(X,Y,0)] vs
  H1=[(X,Z,0),(Z,Y,0)]. (Tests INF handling at the boundary.)
P4: t*=0 competing frontiers (Z and Y both disagree at t*=0;
  tie-break picks lowest id, Z). H0=[(X,Z,0),(X,Y,3)] vs
  H1=[(X,Z,5),(X,Y,0)]. (No repair-family world has two t*=0
  frontiers.)

## Measured numbers (decision lines vs frozen rows)

- P1: TARGET V*=1 t*=0 schema=1, FLAG, PLAN [S,W,OZ] both configs;
  cfg0 real=1 PRED 1/0 SURVIVE h0 ELIM h1 CONVERGE-OK; cfg1 real=0
  PRED 1/0 ELIM h0 SURVIVE h1 CONVERGE-OK. 2/2 cells match.
- P2: TARGET V*=2 t*=0 schema=1, FLAG, PLAN [S,W,OY] both configs;
  cfg0 real=1 PRED 1/0 SURVIVE h0 CONVERGE-OK; cfg1 real=0 PRED 1/0
  ELIM h0 SURVIVE h1 CONVERGE-OK. 2/2 cells match.
- P3: TARGET V*=1 t*=0 schema=1, FLAG, PLAN [S,W,OZ] both configs;
  cfg0 real=0 PRED 0/1 SURVIVE h0 ELIM h1 CONVERGE-OK; cfg1 real=1
  PRED 0/1 ELIM h0 SURVIVE h1 CONVERGE-OK. 2/2 cells match.
- P4: TARGET V*=1 t*=0 schema=1, FLAG, PLAN [S,W,OZ] both configs;
  cfg0 real=1 PRED 1/0 SURVIVE h0 CONVERGE-OK; cfg1 real=0 PRED 1/0
  ELIM h0 SURVIVE h1 CONVERGE-OK. 2/2 cells match.

Aggregate: 8/8 cells match frozen prediction rows exactly.
FLAG TSTAR-ZERO-BOUNDARY floor=1 present on all 8 cells, between
TARGET and PLAN. Zero SILENT-WRONG cells. Zero CONVERGE-FAIL
cells (all four worlds discriminate cleanly under the clamp).

Kill-bar check: OOD-K1 (8/8 exact row match) HOLD. OOD-K2 (flag on
all 8 cells) HOLD. Determinism and purity shared with the red-team
battery (RT-K5, RT-K6) HOLD.

## Verdict: OOD PROBE PASS

The repair's boundary behavior generalizes to the four
structurally novel t*=0 families: Z-target discrimination,
coexisting delay magnitudes, INF arrivals at the boundary, and
competing t*=0 frontiers with tie-break. Combined with the
step-10 battery: 14/14 t*=0 cells across RT1-RT3 and P1-P4 behave
exactly as the soundness argument predicts (12 correct
convergences, 2 honest loud failures on the RT2 negative control),
with the flag firing on every t*=0 cell and none elsewhere.

What this does NOT show: the probe stays inside the 3-variable
rule-delay domain (the assessment's step-7 "broader OOD suite"
item remains open), and it does not touch the RT4 bound
(predictor/execution tick-semantics mismatch at t*>=1), which is
queued as the next hypothesis.

## Architecture accounting (ONE-SYSTEM rule)

- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New handlers: 0. Cognition lines added: 0 (test harness only).
