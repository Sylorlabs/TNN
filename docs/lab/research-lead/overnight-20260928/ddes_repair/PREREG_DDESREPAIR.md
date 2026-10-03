# PREREG: DDES Repair (t*=0 soundness hole)

Frozen before any implementation. This prereg commits the repair
specification and the repair kill bars. Any amendment must be committed
transparently and re-frozen before implementation; no bar may be altered
after seeing results.

## Target

DDES implementation 56db8d606 (BUILD-PASS, strong L2, NOT L3).
Adversary finding e40bdfc9b: ATTACK-SUCCEEDS via K2 (sealed soundness
world). K1 failed (zero-enumeration claim stands). K3 confirmed the
disclosed L2 ceiling.

## The bug (from the adversary report)

Sealed World F: H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)].
The frontier selects (Y, t*=0). synthesize_plan emits [S,OY] with zero
waits. The analytic predictor (observation of V at end of plan is 1 iff
arrival[V] <= t*) claims H0 predicts 1. But the execution model fires
rules only on W ticks (world_step); the S action sets X but fires no
rules. With zero waits, OY reads pre-propagation state (0). Result:
when truth is h0, DDES eliminates the TRUE hypothesis and converges to
h1. Silent wrong convergence.

None of the frozen K-NX worlds has t*=0, so BUILD-PASS stands against
its frozen bars. This repair blocks promotion until fixed and re-run.

## Repair specification (frozen)

The execution model and the analytic predictor must agree on the
effective wait count. Rules fire only on W ticks, so an observation
must follow at least one W tick to reflect any propagation.

- Add a generic helper eff_waits(t_star) = max(t_star, 1).
- synthesize_plan: wait while cur_t < eff_waits(t_star) (was: cur_t < t_star).
- predict: observation is 1 iff arrival[V*] <= eff_waits(t_star)
  (was: arrival[V*] <= t_star).
- No other logic changes. No new branches on delay values, variable
  ids, or world ids. The clamp is a generic boundary condition on the
  derived target t*, of the same kind as the existing null-schema
  fallback and the n<1 guard in z_alloc.
- On World F this yields plan [S,W,OY]: truth h0 gives real=1
  (0-delay rule fires at tick 1), predictor agrees (0 <= 1), correct
  convergence on both truth configs.

For all frozen K-NX worlds (t* >= 1), eff_waits(t*) = t*, so the
repaired binary must behave identically to 56db8d606 on Worlds A-E.

## Test worlds (frozen)

Worlds A, B, C, D, E exactly as in PREREG_DDES.md (same rule tables,
same configs, same expected plans and convergence).

World F (adversary sealed world, now adopted as regression world):
H0 = [(X,Y,0)]. H1 = [(X,Z,7)]. Both truth configs.
Expected after repair:
- truth h0: PLAN [S,W,OY], EXEC real=1, PRED h0=1 h1=0, CONVERGE-OK.
- truth h1: PLAN [S,W,OY], EXEC real=0, PRED h0=1 h1=0, CONVERGE-OK.

## Repair kill bars (all must pass)

- K-R1 (World F fixed): both truth configs of World F converge
  correctly (the surviving hypothesis matches truth). Kill: either
  config eliminates the true hypothesis or fails to converge.
- K-R2 (no regression): Worlds A-E produce byte-identical cognitive
  output to the frozen 56db8d606 runs (same TARGET, PLAN, EXEC, PRED,
  CONVERGE lines; same SUMMARY ok=9/9; same plans_built=8 for the
  frozen set). plans_built over the full run (A-E plus F) must equal
  10 (exactly 1 per discriminating config; E builds none).
- K-R3 (determinism): 3/3 byte-identical runs, exit 0, zero stderr.
- K-R4 (purity): pure Zag, zero Python at any stage, zero em-dash
  bytes in all committed files.
- K-R5 (no new enumeration): static audit of the repaired synthesis
  path. The repair must not introduce any candidate-generating loop,
  length constant, or comparison between assembled plans. Kill: any
  such construct.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
