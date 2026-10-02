# RESULT: H-CAUSALEXP Experiment CONSTRUCTION (causalexp_construct)

Date: 2026-09-30.
Builder verdict: **BUILD-PASS** (7/7 kill bars).
Prereg: `PREREG_CONSTRUCT.md` (frozen at 46bdd01c5, before implementation).
Source: `cxconstruct.zag` (pure Zag).
Raw: `CXCONSTRUCT_RAW.txt` (md5 a1b01823aabaf688218de185785c2e6b).

## What was built

A learner that CONSTRUCTS discriminating interventions from four generic
primitives (S=set X:=1, W=wait, OY=observe Y, OZ=observe Z). Hypotheses are
delay-rule sets stored as DATA and interpreted by one generic simulator;
there is no per-hypothesis code branch. The learner composes sequences by
iterative deepening (depth 1..5, base-4 counting over primitives), simulates
each candidate under every live hypothesis, and selects the FIRST sequence
(in deterministic lexicographic order) where the predicted outcomes
disagree. The search is pure simulation: zero real-world actions occur
before the selected sequence is executed exactly once against the sealed
true world. No sequence is pre-authored; the sequence space is unbounded
in length.

Four configurations run in one binary:
- Config 0: World A {H1=[(X,Z,2),(Z,Y,0)], H2=[(X,Y,1)]}, true=H1.
- Config 1: World A, true=H2.
- Config 2: World B {H3=[(X,Z,3),(Z,Y,0)], H4=[(X,Y,2)]}, true=H3.
- Config 3: World B, true=H4.

## Kill bars (all pass)

- K-CX1 (no single primitive discriminates): 16 PRIM lines (4 configs x
  4 primitives), all agree=1, zero agree=0. Verified from raw output.
- K-CX2 (World A construction): configs 0 and 1 both construct
  [S,W,OY] (length 3). Exactly one EXEC per config. Config 0:
  real=0, SURVIVE h=0 (H1=true). Config 1: real=1, SURVIVE h=1
  (H2=true).
- K-CX3 (World B, different form): configs 2 and 3 both construct
  [S,W,W,OY] (length 4, different from World A's length 3). Config 2:
  real=0, SURVIVE h=0 (H3=true). Config 3: real=1, SURVIVE h=1
  (H4=true).
- K-CX4 (because, not chance): per config, DEPTH summaries show
  found=0 at every depth below the selected depth (World A: depths 1-2
  zero, found at 3; World B: depths 1-3 zero, found at 4). Each SELECT
  line records the disagreeing predictions (h0pred=0 h1pred=1).
  Exactly one EXEC line per config, and it is the SELECTed sequence.
  By code inspection, world_step is called only in the EXEC block;
  the entire search uses sim_seq (hypothesis simulation).
- K-CX5 (elimination correctness): in all 4 configs the true hypothesis
  SURVIVES and the other is ELIMINATED; the real outcome equals the
  true hypothesis's prediction.
- K-CX6 (determinism): 3 runs, byte-identical (cmp), exit 0, zero
  stderr bytes.
- K-CX7 (purity): pure Zag throughout (znc build; bash/grep/cmp/md5sum
  analysis only). Zero Python invocations. Zero em dash bytes in
  committed docs (byte-verified).

## The "because" evidence

The learner never executes a real-world action until it has a simulated
prediction of disagreement. Concretely: in World A it simulates 2 + 12
= 14 observing sequences at depths 1-2, finds all predictions agreeing,
then at depth 3 finds [S,W,OY] with H1->0 vs H2->1 and stops. It does
not execute any of the 14 non-discriminating sequences. The executed
sequence is the deterministic output of the disagreement criterion,
with the disagreeing predictions recorded in the trace. A random-search
learner would have executed sequences without predicted disagreement;
this learner structurally cannot.

## Honest limitations (per frozen prereg section 8)

- Hypotheses are authored rule-sets. This wave tests experiment
  CONSTRUCTION, not hypothesis invention. Target classification: bounded
  L2 with learner-constructed experiments, not L3.
- The primitive set is authored; the sequences are composed, not listed.
- Worlds are synthetic and tiny.
- Iterative deepening is systematic search over a productive
  (unbounded-length) space guided by predicted disagreement. It is not
  random trial-and-error and not selection from an authored menu.
- Promotion pipeline: this is implementation + sealed evaluation
  (4 configs). Independent reproduction, baselines, adversary, OOD,
  ablation, transfer, red team, and governance audit remain.

## Files

- `PREREG_CONSTRUCT.md` (frozen 46bdd01c5)
- `cxconstruct.zag` (implementation)
- `CXCONSTRUCT_RAW.txt` (raw output, md5
  a1b01823aabaf688218de185785c2e6b)
- `CXCONSTRUCT_RESULT.md` (this file)

Toolchain: znc 2026.07.0-dev (edition 2026). Commits local; nothing pushed.
