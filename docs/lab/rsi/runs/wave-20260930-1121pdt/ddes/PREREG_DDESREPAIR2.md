# PREREG: DDES t*=0 Soundness Repair, Wave 2 (R2)

Frozen before any implementation. This prereg commits the repair
specification and the repair kill bars for wave 20260930-1121pdt.
Any amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results.

## Provenance

NEW prereg, written by worker DDES for wave 20260930-1121pdt.
Repair design inherited from PREREG_DDESREPAIR.md @ 0f10fd0f2 and the
prior repair implementation ddesr.zag @ 17c97a2cd (worker of the
overnight 20260928 cycle), extended with an explicit boundary-flag
requirement (K-R2.1) that the prior cycle did not have. This cycle
re-freezes, re-implements, and re-runs the repair because the prior
repair result was logged only inside a paper commit and never entered
the claim ledger as an audited claim, so promotion stayed blocked.
Nothing in this prereg is copied from a tool result; the world tables
are restated from PREREG_DDES.md and PREREG_DDESREPAIR.md.

## Target

DDES lineage at 56db8d606 (BUILD-PASS, strong L2 guided generation,
NOT L3). Adversary finding e40bdfc9b: ATTACK-SUCCEEDS via K2
(sealed soundness world). The frozen K-NX1 through K-NX8 verdicts
stand; none of the frozen K-NX worlds has t*=0.

## The bug (from the adversary report, restated)

Sealed World F: H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)].
The disagreement frontier selects (Y, t*=0). The unrepaired
synthesize_plan emits [S,OY] with zero waits. The execution model
fires rules only on W ticks; the S action sets X but fires no rules.
With zero waits, OY reads pre-propagation state (0). The analytic
predictor (observation of V at end of plan is 1 iff arrival[V] <= t*)
claims H0 predicts 1. When truth is h0, the unrepaired mechanism
eliminates the TRUE hypothesis and converges to h1. That is silent
wrong convergence: the run prints CONVERGE-OK while the surviving
hypothesis is false.

## Repair specification (frozen)

The execution model and the analytic predictor must agree on the
effective wait count. Rules fire only on W ticks, so an observation
must follow at least one W tick to reflect any propagation.

- Add a generic helper eff_waits(t_star) = max(t_star, 1).
- synthesize_plan: wait while cur_t < eff_waits(t_star)
  (was: cur_t < t_star).
- predict: observation is 1 iff arrival[V*] <= eff_waits(t_star)
  (was: arrival[V*] <= t_star).
- Boundary detection and flag: when the derived target satisfies
  t_star == 0, the derivation path must emit the exact trace line
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` before the PLAN line. This is the
  mechanism detecting and flagging the unsound boundary condition
  instead of passing through it silently. The flag is a detection
  marker, not a branch on any delay value, variable id, or world id.
- No other logic changes. The clamp and the flag are generic boundary
  conditions on the derived target t*, of the same kind as the
  existing null-schema fallback and the n<1 guard in z_alloc.
- On World F this yields plan [S,W,OY]: truth h0 gives real=1
  (0-delay rule fires at the first tick), the predictor agrees
  (arrival 0 <= 1), correct convergence on both truth configs, and the
  flag line appears on both configs.

For all frozen K-NX worlds (t* >= 1), eff_waits(t*) = t* and the flag
never fires, so the repaired binary must behave identically to
56db8d606 on Worlds A through E.

## Test worlds (frozen)

Worlds A, B, C, D, E exactly as in PREREG_DDES.md (same rule tables,
same configs, same expected plans and convergence).

World F (adversary sealed soundness world, regression world):
H0 = [(X,Y,0)]. H1 = [(X,Z,7)]. Both truth configs.
Expected after repair:
- truth h0: TARGET V*=2 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OY]; EXEC real=1; PRED h0=1 h1=0;
  SURVIVE h0; ELIM h1; CONVERGE-OK.
- truth h1: TARGET V*=2 t*=0 schema=1; FLAG TSTAR-ZERO-BOUNDARY
  floor=1; PLAN [S,W,OY]; EXEC real=0; PRED h0=1 h1=0;
  ELIM h0; SURVIVE h1; CONVERGE-OK.

## Repair kill bars (all must pass for REPAIR-PASS; builders report BUILD-PASS/BUILD-FAIL only)

- K-R2.1 (t*=0 condition detected and flagged): both World F config
  traces contain the exact line `FLAG TSTAR-ZERO-BOUNDARY floor=1`
  between the TARGET line and the PLAN line. Kill: the flag is absent
  on either config, or appears on any of Worlds A through E.
- K-R2.2 (no silent wrong convergence): both truth configs of World F
  print CONVERGE-OK and the surviving hypothesis matches truth
  (cfg0: SURVIVE h0 and ELIM h1; cfg1: ELIM h0 and SURVIVE h1). The
  emitted plan on both configs is exactly [S,W,OY] (zero-wait plans
  are forbidden at the boundary). Kill: either config eliminates the
  true hypothesis, fails to converge, or emits a plan with zero W
  ticks before the observation.
- K-R2.3 (zero regression): the Worlds A through E output block is
  byte-identical to the frozen reference
  docs/lab/research-lead/overnight-20260928/ddes/DDES_RAW.txt
  (diff of the A-E section empty). The plans_built counter reads 8
  after the E section; the full run (A-E plus F) reads plans_built=10
  and SUMMARY ok=11/11. Kill: any byte difference in the A-E block,
  or a counter mismatch.
- K-R2.4 (determinism): 3/3 runs byte-identical (md5 match), exit 0,
  zero stderr bytes on every run. Kill: any divergence, nonzero
  exit, or any stderr byte.
- K-R2.5 (purity): pure Zag only. Zero Python at any stage
  (implementation, build, run, analysis). Zero em-dash and zero
  en-dash bytes in all committed files (byte-checked with
  check_no_dash.sh). Kill: any Python use or any forbidden byte.
- K-R2.6 (no new enumeration): static audit of the repaired
  synthesis path. The repair must not introduce any
  candidate-generating loop, length constant, or comparison between
  assembled plans. Kill: any such construct.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
