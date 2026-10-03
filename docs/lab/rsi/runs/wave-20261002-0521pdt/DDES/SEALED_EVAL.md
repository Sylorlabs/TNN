# SEALED EVAL: DDES step 7 (OOD test)

Wave: wave-20261002-0521pdt. Lane: DDES.
Prereg: PREREG_DDES78.md, frozen alone at ac7cc6856 before any
implementation. Implementation: ddes_78.zag (pure Zag), written
after the prereg commit. This doc reports measured numbers only,
for the V_full rows (step 7). Step 8 rows are in ABLATION.md.

## The three BINDING citation caveats (restated verbatim)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline
reviewer checks only"

Nothing here removes or weakens them. Ceiling: bounded L2 with
persistence. NOT L3.

## Build and determinism

- znc ddes_78.zag -o ddes_78_bin: exit 0, 93-byte stderr (the
  unconditional zagd-availability warning only), binary 37236 bytes.
- 3/3 runs byte-identical, exit 0, zero stderr bytes every run.
  Transcript sha256 (run_78_1/2/3.txt):
  f7a7ec52bd642604c9ffc3619a72836674de4bc8a4e0d11b5895306c56dda074
- 60 guided plans built across the full matrix (5 variants x
  6 worlds x 2 configs). Zero randomness anywhere.

## Step 7 results: V_full on the six sealed OOD worlds

Decision lines (TARGET, FLAG, PLAN, EXEC, PRED, ELIM/SURVIVE,
CONVERGE, CELLSUM) checked against the frozen prediction rows:

- O1 (two-hop chain): TARGET V*=1 t*=5 schema=1, no FLAG,
  PLAN [S,W,W,W,W,W,OZ]; cfg0 real=1 PRED 1/0 SURVIVE/ELIM
  CONVERGE-OK; cfg1 real=0 PRED 1/0 ELIM/SURVIVE CONVERGE-OK;
  CELLSUM VERDICT=CORRECT. Row matches exactly.
- O2 (t*=12 horizon): TARGET V*=2 t*=12 schema=1, no FLAG,
  PLAN [S,12xW,OY]; cfg0 real=1 / cfg1 real=0, PRED 1/0 both,
  correct eliminations, CONVERGE-OK both;
  CELLSUM VERDICT=CORRECT. Row matches exactly.
- O3 (competing frontiers): TARGET V*=2 t*=0 schema=1,
  FLAG TSTAR-ZERO-BOUNDARY floor=1, PLAN [S,W,OY];
  cfg0 real=1 / cfg1 real=0, PRED 1/0 both, CONVERGE-OK both;
  CELLSUM VERDICT=CORRECT. Row matches exactly.
- O4 (chain + decoy): TARGET V*=1 t*=3 schema=1, no FLAG,
  PLAN [S,W,W,W,OZ]; cfg0 real=1 / cfg1 real=0, PRED 1/0 both,
  CONVERGE-OK both; CELLSUM VERDICT=CORRECT. Row matches exactly.
- O5 (fan-in): TARGET V*=1 t*=1 schema=1, no FLAG,
  PLAN [S,W,OZ]; cfg0 real=1 / cfg1 real=0, PRED 1/0 both,
  CONVERGE-OK both; CELLSUM VERDICT=CORRECT. Row matches exactly.
- O6 (chain-shaped boundary, negative control):
  TARGET V*=1 t*=0 schema=1, FLAG TSTAR-ZERO-BOUNDARY floor=1,
  PLAN [S,W,OZ]; cfg0 real=1 PRED 1/1 SURVIVE/SURVIVE
  CONVERGE-FAIL; cfg1 real=0 PRED 1/1 ELIM/ELIM CONVERGE-FAIL;
  CELLSUM VERDICT=LOUD-FAIL. Row matches exactly: the predicted
  honest loud failure (clamp floor makes both predictions
  coincide), not silent-wrong.

Kill-bar check (frozen): (7a) 3/3 byte-identical, exit 0, zero
stderr: HOLD. (7b) all six decision-line rows match the prereg
prediction table exactly: HOLD. (7c) zero SILENT-WRONG CELLSUMs
across 6 worlds x 2 configs: HOLD.

## Verdict: BUILD-PASS (step 7)

The t*-derived plan construction generalizes, on this sealed
set, to two-hop chains, t*=12 horizons, decoy rules, competing
frontiers, and fan-in convergence, with the boundary world
failing loudly as predicted rather than silently. This is
bounded L2 guided generation on structurally new rule shapes;
it says nothing about L3 and does not touch the binding
caveats.

## Architecture accounting (ONE-SYSTEM rule)

- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New handlers: 0.
- Cognition lines added: 0 (evaluator harness only; no learner
  state, no new cognitive structures).
