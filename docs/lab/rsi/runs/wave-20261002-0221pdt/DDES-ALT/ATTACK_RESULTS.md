# ATTACK RESULTS: DDES-ALT step 6 alternative-explanation attack

Wave: wave-20261002-0221pdt. Lane: DDES-ALT.
Prereg: PREREG_DDES_ALT.md, frozen alone at d64688fa6 before any
implementation. Implementation: ddes_alt.zag (pure Zag), written
after the prereg commit. This doc reports measured numbers only.

## The three BINDING citation caveats (restated verbatim)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline reviewer checks only"

Nothing here removes or weakens them.

## Build and determinism

- znc ddes_alt.zag -o ddes_alt_bin: exit 0, 93-byte stderr (the
  unconditional zagd-availability warning only), binary 55018 bytes.
- 3/3 runs byte-identical, exit 0, zero stderr bytes every run.
  Transcript sha256 (run_alt_1/2/3.txt):
  f9030bb7dadef25201b112d15e7f237ecc724ed7f8788dad6ad2ac4aa494d31f
- Guided plans built across all cells: 26. Baseline candidates
  evaluated: 150.

## H1: clamp-vacuity attack -- verdict: ATTACK-SUCCEEDS

All three frozen sub-bars met.

(a) V_noclamp on fresh sealed P (H0=[(X,Y,0),(X,Z,9)],
H1=[(X,Y,4),(X,Z,9)], t*=0): plan [S,OY], PRED h0=1 h1=0,
EXEC real=0 on cfg0, ELIM h0 with h0 true, CONVERGE claimed on
h1. CELLSUM VERDICT=SILENT-WRONG (ok0=1 ok1=1, true hypothesis
eliminated on cfg0). The clamp is load-bearing on this fresh
world: P is a valid "clamp is the only thing preventing
silent-wrong" case, structurally unlike F/H (decoy rule,
different delays).

(b) V_nomarker vs V_full on P: after removing FLAG lines, every
decision line (TARGET, PLAN, EXEC, PRED, ELIM/SURVIVE,
CONVERGE) is byte-identical across all 3 runs; the only
differences are the CELL variant labels (by construction) and
the FLAG lines themselves. The marker changes no plan, no
prediction, no elimination, no verdict, no record. It is
unconsumed: no branch in the derivation path reads it.

(c) V_full on Q (H0=[(X,Y,1)], H1=[(X,Y,3)], t*=1, clamp provably
the identity): no FLAG line, TARGET V*=2 t*=1, plan [S,W,OY],
PRED h0=1 h1=0, CONVERGE-OK both configs, CELLSUM
VERDICT=CORRECT. Decision-line sequence matches P's modulo the
FLAG line and the t* value: identical plan shape [S,W,OY],
identical convergence pattern. There is no distinct
boundary-reasoning branch in DDES behavior; the only t*=0
deltas are the clamp's own max(t*,1) and the unconsumed marker.

Interpretation: the repair's decision substance is the uniform
clamp alone. DDES performs no reasoning about t*=0 beyond
max(t*,1) plus a print no downstream decision consumes. This
does not dispute that the clamp is load-bearing (cell (a)
re-confirms it on a fresh world); it kills any reading of the
repair as DDES "reasoning about" the boundary. The t*=0
soundness credit narrows to a static floor, mechanically
verified.

## H2: experiment-selection divergence -- verdict: EVIDENCE-HOLDS

The attack hypothesis (guidance adds nothing over unguided
synthesis) FAILS on fresh sealed worlds. Guidance changes which
experiments are built, and it matters.

Per-world measured results (guided V_full vs frozen-spec
baseline, seed 14500418 chained W1,W2,W4,W5,W5p):

- W1 (H0=[(X,Y,0)] H1=[(X,Y,2)]): guided [S,W,OY] CORRECT;
  baseline [S,W,OY] CORRECT (draw 19, 20 evals). Same shape,
  same verdict. Parity point, as predicted.
- W2 (H0=[(X,Y,3)] H1=[(X,Y,5)]): guided [S,W,W,W,OY] CORRECT
  (t*=3 derived); baseline NO-DISCRIMINATING-PLAN, LOUD-FAIL
  (64 evals, zero discriminating). Guidance-exclusive win: the
  t*-derived wait count exceeds the baseline's fixed 0..2 menu.
- W4 (H0=[(X,Y,1),(X,Z,0)] H1=[(X,Y,2),(X,Z,3)]): guided
  [S,W,OZ] CORRECT (frontier picks Z at t*=0 over Y at t*=1);
  baseline [S,W,W,OZ] CORRECT (draw 0, 1 eval). Selection
  divergence with identical verdicts: guided builds the minimal
  1-wait plan, the baseline the first PRNG-ordered
  discriminating shape (2 waits).
- W5 (H0=[(X,Z,4)] H1=[(X,Z,6)]): guided [S,W,W,W,W,OZ]
  CORRECT (t*=4 derived); baseline LOUD-FAIL (64 evals).
  Guidance-exclusive win.
- W5p (H0=[(X,Y,2),(X,Z,0)] H1=[(X,Y,2),(X,Z,2)], Y decoys):
  guided [S,W,OZ] CORRECT; baseline [S,W,OZ] CORRECT (draw 0,
  1 eval). Same shape, same verdict. Parity point with decoys.

Frozen metrics, measured:

- divergence_rate = 1/3 (W4 only; W1 and W5p identical shapes;
  W2/W5 the baseline built no plan).
- guidance_exclusive = 2 (W2, W5).
- baseline_exclusive = 0.
- Baseline totals: correct=3, loud_fail=2, candidates_evaluated=150.

Kill-bar check: guidance_exclusive (2) >= 1, so EVIDENCE-HOLDS.
The frozen bar is met exactly as predicted in the prereg.

Honest reading: the measured guidance contribution is narrow
and mechanical: (i) the wait count derived from the arrival
analysis (t*) lets the guided path build experiments outside
the baseline's fixed menu, and (ii) frontier selection picks
the earliest-discriminating variable with the minimal wait
count. This is bounded L2 machinery. It says nothing about L3,
and it does not touch the binding caveats. The W2/W5 wins come
specifically from t*-derived experiment length, not from any
broader intelligence.

## H3: RT2 loud-failure provenance -- verdict: ATTACK-SUCCEEDS

All frozen sub-bars met, with DDES code unchanged across
RT2a/RT2b/RT2c (only delay tables altered):

- RT2a (frozen contract H0=[(X,Y,1)] H1=[(X,Y,0)], V_full):
  FLAG, plan [S,W,OY], PRED h0=1 h1=1, SURVIVE/SURVIVE,
  CONVERGE-FAIL both configs. CELLSUM VERDICT=LOUD-FAIL.
  Reproduces the frozen RT2 outcome exactly.
- RT2b (widened gap H0=[(X,Y,2)] H1=[(X,Y,0)], V_full): FLAG,
  plan [S,W,OY], PRED h0=0 h1=1, real cfg0=0 cfg1=1,
  CONVERGE-OK both configs. CELLSUM VERDICT=CORRECT. The loud
  failure vanishes when only the delay values change.
- RT2c (same gap of 1 shifted off the boundary H0=[(X,Y,2)]
  H1=[(X,Y,1)], V_full): no FLAG (t*=1), plan [S,W,OY],
  PRED h0=0 h1=1, CONVERGE-OK both configs. CELLSUM
  VERDICT=CORRECT. Moving the distinguishing time off t*=0
  restores discrimination with the gap unchanged.
- RT2d (frozen contract, V_noclamp): plan [S,OY], PRED h0=0
  h1=1; cfg0 real 0: CONVERGE-OK (correct); cfg1 real 0:
  SURVIVE h0, ELIM h1 with h1 true, convergence claimed on h0.
  CELLSUM VERDICT=SILENT-WRONG. Removing the clamp replaces the
  loud failure with silent-wrong on cfg1.

Interpretation: RT2's loud failure appears and disappears
purely with the contract x clamp combination. DDES takes no
boundary-specific detection action: the p0==p1 alarm is a
generic coincidence alarm that fires here only because the
clamp's floor of 1 wait makes the two predictions coincide for
delay values 1 vs 0. The repair's credit narrows to the
mechanical fact that the clamp converts would-be silent-wrong
into loud failure at the boundary (RT2d shows the counterfactual).

## Architecture accounting (ONE-SYSTEM rule)

- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New handlers: 0.
- The three DDES variants are controlled single-line ablations
  of the frozen derivation machinery (FLAG emission suppressed;
  eff_waits replaced by the identity), not new machinery.
- Cognition lines added: 0 (attack harness only; no learner
  state, no new cognitive structures).

## Kill-bar status for this lane

- H1 (clamp-vacuity): ATTACK-SUCCEEDS. Bars (a)+(b)+(c) all met
  on 3/3 byte-identical runs.
- H2 (selection divergence): EVIDENCE-HOLDS. guidance_exclusive
  = 2 >= 1; divergence_rate = 1/3 > 0 with guided strictly more
  efficient (W4) and menu-exceeding (W2, W5).
- H3 (RT2 provenance): ATTACK-SUCCEEDS. RT2b and RT2c both
  CONVERGE-OK with DDES code unchanged; RT2d SILENT-WRONG on
  cfg1.
- Determinism: 3/3 byte-identical transcripts, exit 0, zero
  stderr every run.
- Governance: pure Zag (safebin PATH, `which python3` empty,
  Step 0 recorded before any work); dash scan clean on all lane
  files; prereg committed alone at d64688fa6 before
  implementation; commits lane-scoped with explicit pathspec; no
  push.

## Verdict: BUILD-PASS (attack lane only)

The attack lane built, ran sealed, and reported per-hypothesis
verdicts against the frozen bars. No promotion claim is made.
The steps 4+5 BUILD-PASS is not retroactively altered by these
results; H1/H3 successes narrow the interpretation of the
repair evidence (clamp = static floor doing all
decision-relevant work; RT2 loud failure = contract x clamp
interaction), and H2's failure bounds the guidance credit to
t*-derived experiment construction. All of that is coordinator
business for any citation update.

## Queued next (for the coordinator)

- Step 10 (independent red team) and step 11 (independent
  governance audit) remain open for the DDES line.
- Suggested follow-ups from this lane: (i) whether any frozen
  DDES citation text implies DDES "reasons about" or "detects"
  the t*=0 boundary (H1/H3 say it does neither); (ii) a
  guidance stress set with t* beyond small integers and with
  competing frontiers, to map where t*-derived construction
  keeps its edge (H2).
