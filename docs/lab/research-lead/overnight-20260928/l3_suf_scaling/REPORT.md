# L3-SUF-1-SCALING REPORT

**Worker:** L3-SUF-1-SCALING (subagent, 2026-10-03)
**Status:** Scaling battery complete. All frozen bars evaluated; one soft FAIL (SC-K3 at S3), one sharp boundary found (nent=41).
**Task type:** non-ledger (claim minting paused). Scientific scaling evidence, not a benchmark to pass.

## What was built

- `scale_world.zag`: worker's own scaling world builders (INV = G0-class
  invention, ABS = G-B-class abstain), implementing the frozen WB
  interface. Truth: g0=ORD(perm), g1=PARITY, 2 contexts. U pairs:
  unprobeable, undetermined, anti-tiebreak truth. The adversary's sealed
  worlds and KEY.md were not inspected or linked.
- `scale_main.zag`: driver linking the FROZEN learner sources read-only
  (sha256-verified at build, `build/frozen_src.sha256`) + the frozen
  driver.zag harness (`h_treat_arm`, `h_held_tally`, `h_stakes_shape`).
  One (family, scale) per binary; 12 binaries.
- `build.sh` / `run.sh`: pure-Zag builds (safebin, pinned znc, no
  forbidden interpreter; Step 0 verified), 3x runs with sha256 digests.
- `diag_main.zag`: POST-PREREG diagnostic (not part of the frozen
  battery): for each over-marked determined stakes query, reports the
  consequence-log evidence on that element, separating Case A (R-SUF-1
  defect: TEST-ACCEPTs discarded) from Case B (honest abstention: no
  positive evidence at that element).

Scales: S1 (nent=10, |D|=6, |U|=4) / S2 (20,20,8) / S3 (30,40,12) /
S4 (40,60,16,32) / S4b (41,64,17, boundary probe) / S5 (50,80,20).
N_STAKE=12, budgets frozen (150 setup / 500 escalation / 2000 total).

## Results (3/3 byte-identical every run)

| scale | SC-K1 | SC-K2 (INV) | SC-K3 (ABS) | SC-K4 | notes |
|-------|-------|-------------|-------------|-------|-------|
| S1    | PASS  | PASS (310>127, opf=2, shape=1) | PASS (0 wrong, 7/8, 4/4 abst) | PASS | full probe coverage (242/650 tests) |
| S2    | PASS  | PASS (790>156, opf=2, shape=1) | PASS (0 wrong, 8/8, 4/4 abst) | PASS | probe budget saturated (650) |
| S3    | PASS  | PASS (886>156, opf=2, shape=1) | **FAIL** (ii: cdet=5/8 < 7/8) | PASS | 0 wrong; 3 abstains on off-ctx A pairs |
| S4    | PASS  | PASS (950>156, opf=2, shape=1) | PASS (0 wrong, 8/8, 4/4 abst) | PASS | setup staged=0 (slot-varying eats 150) |
| S4b   | —     | — | — | — | **panic: slice index out of bounds, exit=1** |
| S5    | —     | — | — | — | **panic: slice index out of bounds, exit=1** |

- SC-K5 (sharp boundary): PASS. S4b/S5 abort with the predicted
  slice-bounds panic (3/3 identical); S4 passes. Boundary is exactly
  nent=41, the frozen learner's fixed 40x40 used-pair buffer
  (`usedp[1600]` in `l_probe_phase`, indexed `p1*40+p2`).
- SC-K6 (determinism): PASS everywhere (12/12 runs 3/3 byte-identical,
  panics included).
- SC-K4(i): max 650 total TESTs, far under B_REVISE=2000, at every scale.
- Runtime: 0.2-1.1 s/run, flat across scales (no wall-clock degradation;
  the quadratic record-fill cost is negligible at nent<=40).

## Findings

1. **The sole-survivor rule holds at every runnable scale (SC-K2 PASS
   S1-S4).** SEQ order (first mark strictly after first
   committed-prediction REJECT), >=2 non-marking FORM_TRY FAILs before
   lift, and post-escalation stakes shape (0 REJECTs on determined,
   100% ABSTAIN on U) are all preserved at nent=40. The escalation
   enumeration does real work at scale (op_fail=2 throughout).

2. **The scaling limit is sharp and structural, not gradual: nent=41.**
   The frozen learner's `usedp` buffer overflows at 41 entities; 40
   passes fully. This is a fixed-buffer boundary in the probe phase,
   not a degradation of the mechanism's logic. (The `ents[400]` buffer
   would bind next at nent=101; `l_ekey` requires ids < 1000.)

3. **SC-K3 FAIL at S3 is a bar-calibration finding, not a mechanism
   correctness failure.** Decomposition via the post-prereg diagnostic:
   all 3 over-marked determined queries are Case B (no positive
   evidence discarded: obs=0, test_acc=0 at the queried (s0,x,y); the
   abstains are honest). Root cause: the probe strategy's used-pair set
   is context-blind, so a pair trained at ctx0 is never staged-probed
   at ctx1; slot-varying only tests the form's (fabricated) prediction
   there, and fabrication REJECTs get no flipped-value follow-up.
   Cross-context determined pairs are therefore un-evidenced, and the
   sole-survivor rule correctly abstains. The frozen T2(ii) bar
   (>=7/8) demands tiebreak-luck on such queries at scale; it passes at
   S4 (8/8) by the same luck. Safety invariants (0 wrong predictions,
   100% U-abstention) hold at every scale.

4. **R-SUF-1 Case A fires sporadically at all scales (1 instance each
   at S1/S3/S4 INV; 0 at S2/S4 ABS).** Example (S1 INV q=10, pair
   (601,602)@ctx61): test_acc=2, then one stakes fabrication REJECT ->
   marked UNRESOLVED(3), discarding the ACCEPTs. Safe direction, never
   wrong, but the defect does not attenuate with scale. It is
   pre-existing (found by the adversary), not scale-caused.

5. **Probe starvation is real but handled in the safe direction.**
   S1: full pair-space coverage (242 tests, budget unsaturated). S2+:
   budget saturated (650/650). S4 setup: slot-varying consumes the
   entire 150-probe budget (ntrain=152); staged coverage comes only
   from escalation probe-more. Correctness bars still hold.

## Out of scope (per prereg)

The three cognitive scales (element/form/reuse) were not multiplied:
adding a scale would require redesigning the frozen learner, which this
task forbids. "More probes" was answered as starvation tolerance under
frozen budgets. Transfer/reuse/revision/retirement at scale untested.

## Bar verdicts

- SC-K1 PASS (8/8 runs exit 0, S1-S4)
- SC-K2 PASS (INV S1-S4)
- SC-K3 FAIL at S3 (ABS (ii) 5/8 < 7/8); PASS at S1, S2, S4
- SC-K4 PASS (budget honored; S4 holds under setup probe starvation)
- SC-K5 PASS (boundary sharp at nent=41, as predicted)
- SC-K6 PASS (3/3 byte-identical, all runs)

## Notes for the parent

- The S3 SC-K3 FAIL should not be read as the mechanism breaking at
  nent=30: S4 (nent=40) passes SC-K3 fully, and the S3 shortfall is
  decomposed as honest abstention (Case B), not discarded evidence.
  The actionable items are: (a) the ctx-blind used-pair set in the
  probe strategy (a completeness limitation worth a future hypothesis,
  not a frozen-code fix); (b) the R-SUF-1 rule-(ii) coarseness, which
  persists at scale and is already with the red team for SUF-K10.
- The hard scaling ceiling for any future work on this frozen learner
  is nent=40 (usedp), then nent=100 (ents), then ids<1000 (l_ekey).
- Suggested follow-up (not done here): a scaling bar for T2(ii) that
  counts only pairs the learner could have evidenced (on-ctx or
  staged-probed), separating completeness-luck from marking quality.
