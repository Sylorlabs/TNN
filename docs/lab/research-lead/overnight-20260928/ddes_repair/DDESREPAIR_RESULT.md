# DDES Repair Result: t*=0 soundness hole fixed

## Prereg

Commit `0f10fd0f2` (file `ddes_repair/PREREG_DDESREPAIR.md`). Committed
alone; implementation is a strict descendant (verified via
git merge-base --is-ancestor before this report).

Target: DDES 56db8d606 (BUILD-PASS, strong L2). Adversary finding
e40bdfc9b: ATTACK-SUCCEEDS via K2 (sealed World F caused silent wrong
convergence at t*=0).

## The repair (frozen in prereg, implemented verbatim)

The execution model fires rules only on W ticks; S sets X but fires no
rules. Added generic helper `eff_waits(t_star) = max(t_star, 1)`:

- `synthesize_plan`: waits while `cur_t < eff_waits(t_star)`
  (was `cur_t < t_star`).
- `predict`: observation is 1 iff `arrival[V*] <= eff_waits(t_star)`
  (was `arrival[V*] <= t_star`).

No other logic changed. The clamp is a generic boundary condition on
the derived target t*, not a branch on any delay value, variable id,
or world id. For all frozen K-NX worlds (t* >= 1),
eff_waits(t*) = t*, so behavior there is unchanged by construction.

File: `ddes_repair/ddesr.zag` (pure Zag). Binary: `ddes_repair/ddesr_bin`.
World F (adversary sealed world) adopted as a regression world in main.

## Test results (3/3 byte-identical, md5 fca91df99502c54625665dc32da0df93)

Exit 0 on all runs. 0 bytes stderr on all runs.

World A cfg0: TARGET (Y,1) PLAN [S,W,OY] EXEC real=0 PRED 0/1 CONVERGE-OK
World A cfg1: TARGET (Y,1) PLAN [S,W,OY] EXEC real=1 PRED 0/1 CONVERGE-OK
World B cfg0: TARGET (Y,2) PLAN [S,W,W,OY] EXEC real=0 PRED 0/1 CONVERGE-OK
World B cfg1: TARGET (Y,2) PLAN [S,W,W,OY] EXEC real=1 PRED 0/1 CONVERGE-OK
World C cfg0: TARGET (Y,4) PLAN [S,W,W,W,W,OY] EXEC real=0 CONVERGE-OK
World C cfg1: TARGET (Y,4) PLAN [S,W,W,W,W,OY] EXEC real=1 CONVERGE-OK
World D cfg0: TARGET (Z,2) PLAN [S,W,W,OZ] EXEC real=1 CONVERGE-OK
World D cfg1: TARGET (Z,2) PLAN [S,W,W,OZ] EXEC real=0 CONVERGE-OK
World E: NO-DISCRIMINATING-PLAN, 0 executions, E-EMPTY-OK
World F cfg0 (truth h0): TARGET (Y,0) PLAN [S,W,OY] EXEC real=1
  PRED h0=1 h1=0, SURVIVE h0, ELIM h1, CONVERGE-OK
World F cfg1 (truth h1): TARGET (Y,0) PLAN [S,W,OY] EXEC real=0
  PRED h0=1 h1=0, ELIM h0, SURVIVE h1, CONVERGE-OK

SUMMARY: ok=11/11, plans_built=10 (exactly 1 per discriminating config).

Before the repair, World F cfg0 eliminated the TRUE hypothesis h0
(silent wrong convergence). After the repair, the true hypothesis
survives on both configs.

## Kill bar verdicts

- K-R1 (World F fixed): PASS. Both truth configs converge correctly;
  the surviving hypothesis matches truth in each case.
- K-R2 (no regression): PASS. The Worlds A-E output block is
  byte-identical to the frozen 56db8d606 runs (diff of the A-E block
  against ddes/DDES_RAW.txt: empty). Same TARGET, PLAN, EXEC, PRED,
  CONVERGE lines. Frozen-set counter reaches exactly 8 before F;
  full-run plans_built=10 (8 frozen + 2 for F).
- K-R3 (determinism): PASS. 3/3 byte-identical, exit 0, zero stderr.
- K-R4 (purity): PASS. Pure Zag. No Python used at any stage. Zero
  em-dash bytes in all committed files (byte-checked).
- K-R5 (no new enumeration): PASS. Static audit of the repaired path:
  eff_waits is a single clamp; synthesize_plan still assembles exactly
  one plan with no candidate list; predict still reads one arrival
  value. No candidate-generating loop, no length constant, no
  comparison between assembled plans. plans_built=10 over 11 configs
  confirms one-shot derivation is preserved.

## Classification

Unchanged: strong L2 (guided generation), NOT L3. The repair does not
alter authorship: guidance remains researcher-written (disclosed), the
plan remains a deterministic function of the hypothesis pair.

## REPAIR-PASS

The t*=0 soundness hole is closed. The derivation is now sound at the
t*=0 boundary: synthesis and prediction use the same effective wait
count, and the observation reflects at least one propagation round.
Promotion unblocked on the K2 vector; the adversary's other findings
(K1 stands, K3 confirms L2 ceiling) are unaffected.
