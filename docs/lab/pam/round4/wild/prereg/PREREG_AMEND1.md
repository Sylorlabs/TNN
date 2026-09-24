# PREREG AMENDMENT 1 — frozen-value corrections (WILD-B)

**Date:** 2026-09-24. **Status:** FROZEN — committed before any WILD-B
fixture run, build, or battery. Parent: PREREG_W4/W5/W12/W13 (commit
8fdb5df1). This amendment CORRECTS citations of frozen Round-3 values; it
recalibrates nothing.

## A1. The frozen M1 bar is (ST=0, AT=0, CT=705, MT=3588), not (705,3588,1,1)

The committed preregs PREREG_W5, PREREG_W12, PREREG_W13 (and the D-W4-1
comparator in PREREG_W4) cite the frozen M1 bar as "(705,3588,1,1)". That
citation is wrong. The frozen record (`pam/round3/m1/VERDICT_M1.md`, lines
12/24) is explicit:

- The exact optimum is **(ST=0, AT=0, CT=705, MT=3588)** → 910/1102 = 82.58%.
- The (…,ST=1,AT=1) variant passes only 671/1102 = 60.89% and "would KILL
  under KB-M1".

The program prereg's own citation ("conf≥705 ∧ mrgF≥3588; RK-3 82.58%")
matches (0,0,705,3588): the 82.58% figure holds only with the strong/agree
arms OFF. The debate text's "(705,3588,1,1)" tuple is superseded by the
frozen verdict.

**Correction (applies everywhere the preregs say "(705,3588,1,1)"):** the
frozen M1 bar is **(CT=705, MT=3588, ST=0, AT=0)**, 910/1102 = 82.58%.
Consequences, all verified against the canonical tape on-VM:

- W5 §2/§3: reference recompute = (705,3588,0,0); K3 = 910/1102 = 82.58%
  (unchanged — the prereg already states 910/1102).
- W12 §5: K1 first stage = (705,3588,0,0); K3 = 910/910 admitted = 82.58%
  (unchanged).
- W13 §2/§3: genuine leases cycle through the 910 C rows passing
  (705,3588,0,0) (generator fixed: dropped the s/a arms).
- W4 D-W4-1: comparator = (705,3588,0,0); predicted outcome UNCHANGED
  (12/12 W wrongs admitted under margin-inflation: no strong/agree arms to
  block them).

W4's own STARTING bar is unaffected: PREREG_M1_BAR §7's baseline
(CT=700, MT=0, ST=1, AT=1) is a different frozen object (the pre-optimization
baseline), correctly cited in PREREG_W4.

## A2. W12 budget B corrected to the computed value: B = 20974

PREREG_W12 §3 states B = 24814 = 2× a max per-episode price total of 12407
"computed from the frozen tape". Recomputing honestly with the frozen price
function (§2) over the honest stream gives **max = 10487**, so the correct
2× value is **B = 20974**. The mechanism is unchanged (B ≥ 2× max episode
total ⇒ every episode's candidates fit in-budget ⇒ predicted 0 deferrals, 0
quarantines on the honest stream — re-verified). Only the calibration
constant is corrected to the true computed value.

Both corrections are fidelity-to-frozen-record fixes. No threshold, arm, or
mechanism is altered; no battery has run.
