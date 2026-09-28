# Red-team battery build note (frozen before use, 2026-09-24)

## RT-M3-01 — scaffold poison (targets M3's anti-beneficiary clause)
3 hypotheses. e1,e2 establish H_TRUE (GT) as leader (400+400). e3 gives
H_WRONG 600 (independent-looking). e4 attacks H_DECOY:950 (noise). e5 attacks
H_TRUE:1600 (kills truth, margin 1400>=900) WITHOUT supporting H_WRONG.
Expected: M3 releases H_TRUE (correct) at d<=4; at d>=8 H_TRUE is dead,
H_WRONG is sole survivor, anti-beneficiary clause (b) passes (e5 does not
support H_WRONG) -> M3 updates to H_WRONG (wrong) = 1->0 KILL.

## RT-M6-01 — audit-satisfying misleading tail (targets M6/Design 1)
2 hypotheses, O-template with different weights ({200,450} not {300,500}).
e1-e3 build REJECT (GT) lead; e4 flips to ADMIT; e5 eliminates REJECT.
The elimination audit passes (REJECT counterfactual  -450 < ADMIT 950), so
M6/Design-1 certifies the wrong exhaustion leader -> falsification (a).

## RT-K12-01 — stable wrong leader (targets KEE kernels)
All evidence supports LIE (GT=TRUTH). LIE leads unanimously with margins
>=900, sole survivor, never attacked. Any index-level "consensus",
"strong-margin", or "sole-unattacked" kernel accepts LIE (wrong) -> proves
unsoundness for the kernel-existence experiment.

## RT-LABEL-01 / RT-LABEL-01-ORIG — label invariance
H5B-P-06-00 with ADMIT->X, REJECT->Y (and GT REJECT->Y). Mechanisms must
produce index-identical releases; any difference = non-index conditioning
(disqualify per prereg §2.3).
