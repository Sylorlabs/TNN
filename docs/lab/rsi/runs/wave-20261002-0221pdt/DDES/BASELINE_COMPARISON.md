# BASELINE COMPARISON: unguided random experiment synthesis vs DDES V2 guided derivation

Wave: wave-20261002-0221pdt. Lane: DDES.
Baseline spec frozen in PREREG_DDES_REPRO.md (committed alone at
7dc99b131 before the baseline was written). This doc reports the
measured numbers for pipeline step 5.

## The three BINDING citation caveats (restated verbatim)

(1) "a menu of size 2 reproduces the sealed phase-2 outputs"
(2) "World G is signature-identical to F by prereg design"
(3) "the derivation-to-record binding is enforced by offline reviewer checks only"

Nothing in this comparison removes or weakens them; the
self-red-team section below addresses them directly.

## Baseline specification (as frozen)

- ddes_randbase.zag, pure Zag, xorshift32 PRNG seed 14500418
  (0x00DD4242), fully deterministic, no wall-clock seed.
- Worlds: the six phase-A derivation worlds from the frozen
  1721pdt plan (F, A, H, K, RT1, RT2), same rule definitions.
- Candidate space: [S] + w waits (w in 0..2) + one observation
  op (OX, OY, OZ); 9 shapes; B=64 draws with replacement per
  world, first discriminating candidate selected (predictions
  under h0 vs h1 differ), else NO-DISCRIMINATING-PLAN.
- Simulator semantics: rule (src,dst,delay) fires at the first W
  tick t with t >= delay while src is active; same-tick fixpoint
  chaining; S stimulates X at t=0; observation reads current
  variable state.
- Verdict per world: CORRECT (true hypothesis survives and false
  eliminated on both configs), SILENT-WRONG, LOUD-FAIL.
- Scope: proposal guidance only. The baseline does not exercise
  record persistence, the class-stamp gate, or phase-B reuse.

## Simulator validation (mechanical, 7/7)

The baseline simulator reproduces every frozen EXEC real value
from RESULT_DDES_V2_STEPS7_11.md:

- F [S,W,OY]: cfg0=1, cfg1=0 (frozen: 1, 0)
- A [S,W,OY]: cfg0=0, cfg1=1 (frozen: 0, 1)
- H [S,W,OZ]: cfg0=1, cfg1=0 (frozen: 1, 0)
- RT1 [S,W,OZ]: cfg0=1 (frozen: 1)

Same simulation semantics as the guided path's EXEC ground
truth. The comparison is about how experiments are proposed,
not about how they are simulated.

## Per-world results

Baseline run transcript sha256 (3/3 byte-identical, exit 0,
zero stderr):
672a32f6f3d114a55c530e5cb265c6e6a04a85b78be723a3275e776e5cebb736

- F: baseline CORRECT (PLAN [S,W,W,OY], draw 8, 9 evals).
  Guided: CORRECT ([S,W,OY]). Match.
- A: baseline CORRECT (PLAN [S,W,W,OZ], draw 4, 5 evals).
  Guided: CORRECT ([S,W,OY]). Match.
- H: baseline CORRECT (PLAN [S,W,W,OZ], draw 12, 13 evals).
  Guided: CORRECT ([S,W,OZ]). Match.
- K: baseline LOUD-FAIL (64 evals, zero discriminating
  candidates; identical hypotheses). Guided: LOUD-FAIL
  (NO-DISCRIMINATING-PLAN). Match.
- RT1: baseline CORRECT (PLAN [S,W,W,OY], draw 0, 1 eval).
  Guided: CORRECT ([S,W,OZ]). Match.
- RT2: baseline LOUD-FAIL (64 evals, zero discriminating
  candidates; the delay-1 vs delay-0 hypotheses are
  indistinguishable under these observations at every wait
  count). Guided: LOUD-FAIL (CONVERGE-FAIL via p0==p1 alarm).
  Match.

SUMMARY: baseline correct=4, loud_fail=2,
candidates_evaluated=156. Guided: 4 correct, 2 loud fails,
plans_built=10. Per-world verdicts identical on all 6 worlds.

## Cost fields

- baseline binary_bytes=17091 (guided ddesv2_s7_bin=75589)
- baseline wall_ms: 2, 2, 2 (guided: 9, 10, 24 per frozen record)
- baseline candidates_evaluated=156 (cap 64/world; early stop on
  first discriminating candidate)
- guided plans_built=10
- baseline source: ddes_randbase.zag, new file, pure Zag, no
  derivation machinery, no records, no phase-B, no guards

## Interpretation (honest)

On these six sealed worlds, unguided random proposal with a
strictly larger evaluation budget (156 candidate simulations vs
10 guided syntheses) matches the guided derivation on every
world, including the two loud-failure worlds. The guided
derivation's proposal-quality advantage is therefore NOT
demonstrated on this world set: the worlds are easy enough
that random search finds discriminating plans within a few
draws (RT1 on draw 0, A on draw 4, F on draw 8, H on draw 12).

This does not overturn the frozen BUILD-PASS, which rests on
different evidence: the t*=0 soundness repair (pre-repair
control exhibits silent-wrong; no-clamp ablation re-opens it;
both reproduced byte-identically here), the persistence
records carried through the disconnect (R_F, R_H with the
adversary-chosen V*=1 value), the class-stamp gate (J loud
CLASS-MISMATCH), and the OOD loud failures (K, J). The
baseline tests none of those; it isolates proposal guidance,
and on proposal guidance alone the guided path shows no
measured edge on this set. The "strong L2 guided generation"
credit should be read with that bound: guided, yes; uniquely
necessary for these worlds, no.

A further honest note: the baseline's evaluator IS its
simulator, so by construction it cannot exhibit the
silent-wrong hole class (no gap between prediction and
execution). The t*=0 hole was specific to DDES's architecture
(deriving a target t* and planning at raw t* with a separate
analytic predictor). The baseline comparison therefore cannot
and does not speak to the value of the clamp/flag repair; the
ablations do.

## Self-red-team on the binding caveats

1. Does the eff_waits clamp make the reproduction result
   vacuous? No. The no-clamp ablation (reproduced
   byte-identically, transcript hash match) re-opens
   silent-wrong convergence on F with the FLAG still present,
   so the clamp is load-bearing for soundness, not decorative.
   The clamp does not trivialize the worlds: K, RT2, and J
   still fail loudly under it, and RT2's hypotheses are
   genuinely indistinguishable under the validated simulation
   semantics (the baseline, which has no clamp, also fails
   loudly there). Caveat (1) (menu of size 2) still bounds
   what phase-2 outputs can show; the reproduction does not
   touch it.
2. Is the baseline fair (not deliberately crippled)? Yes.
   Strictly larger candidate budget (156 actual evaluations vs
   10 guided syntheses, cap 64/world vs 1/world), identical
   validated simulation semantics (7/7 frozen EXEC values),
   deterministic seeded PRNG, full 9-shape candidate space,
   first-discriminating selection, and complete per-world
   reporting including the two worlds where it matches the
   guided loud failures. A crippled baseline would have been
   given fewer evaluations or a weaker simulator; this one
   was given more of both.
3. Does the reproduction strengthen or weaken caveat (3)
   (derivation-to-record binding enforced offline only)?
   Neither. The reproduction re-runs the same binding
   mechanism and re-verifies it the same offline way (exact
   trace-line checks against the frozen record). It does not
   make the binding self-enforcing, and this doc does not
   claim otherwise.

## Kill-bar status for this lane

- R-R1 (source pins): PASS. All five extracted sources
  sha256-match the prereg pins before building.
- R-R2 (byte-identical rebuild): PASS. All five rebuilt
  binaries sha256-match the committed _bin blobs at 947675258.
- R-R3 (sealed 9/9 re-pass): PASS. All five rebuilt run
  transcripts sha256-match the frozen values; K-R1 through
  K-R9 re-verified line by line from the rebuilt transcripts
  (8 FLAG lines, 0 zero-wait plans; pre-repair silent-wrong on
  F; K loud non-convergence; J CLASS-MISMATCH + CONVERGE-FAIL
  with 0 EXEC lines and no RECORD-LOAD; no-clamp re-opens the
  hole; no-guard 1 ABL-PROBE with SCAFFOLD-CALLS 0;
  zeroed-record 5 phase-B CLASS-MISMATCH + 5 CONVERGE-FAIL
  with 0 phase-B EXEC; R_H byte-exact on sealed I; RT1 2/2
  correct; RT2 2/2 loud CONVERGE-FAIL).
- R-R4 (baseline comparison): PASS. Baseline implements the
  frozen spec exactly (seed, B=64, 9 shapes, simulator
  validated 7/7); per-world verdicts and cost fields reported
  above; transcript 3/3 byte-identical.
- R-R5 (determinism): PASS. 5 rebuilt binaries x 3 runs
  byte-identical with exit 0 and zero stderr; baseline 3/3
  byte-identical with exit 0 and zero stderr.

## Verdict: BUILD-PASS (reproduction step)

Pipeline steps 4 (independent reproduction from committed
source) and 5 (simple-baseline comparison) are complete. All
five frozen kill bars R-R1 through R-R5 pass. The frozen DDES
V2 BUILD-PASS is reproduced, not promoted: no SURVIVES claim.
Ceiling remains bounded L2 with persistence; C0-A through C0-D
still fail; the three binding caveats above still bind every
citation of the BUILD-PASS.

## Queued next

Step 6 (alternative-explanation attack on the rebuilt evidence
set, incorporating the baseline finding that proposal
guidance shows no measured edge on the six sealed worlds);
step 10 (independent red team); step 11 (independent
governance audit). The f461e812d mass deletion of the
committed DDESv2 lane (sources recoverable only from the
947675258 blobs; working-copy dir untracked) is a provenance
fragility the coordinator should address before further
lanes cite these artifacts.
