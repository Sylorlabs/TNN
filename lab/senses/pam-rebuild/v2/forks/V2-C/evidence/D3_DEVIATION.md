# D3 deviation — CCN-1 detector recall is zero on the R2A battery

**Finding:** The build-time projection ("D3 (CCN-1) 0/100 vs baseline 335",
  PREREG_V2-C_AMEND1.md §4) is not reproduced by the committed binary on the
  frozen battery fixtures. D3 fires zero times across all 340 R2A CCN-1
  fixtures and all 20 harness colorconst-adversarial fixtures.

## Measurements (pure-Zag binary, `stats` mode)

`r2a_colorconst_CCN-1_000.r24` (dmask=4095):
- judgment=DIFFERENT, confidence=850 (wrong-HC; truth=SAME_SURFACE)
- `d3_opp=0` — opposite-cast test (b > 2r ∧ b > 2g) FAILS.
  Panel-1 mean RGB = (0.0, 127.5, 100.1): the 0.55-exposure renders are
  green-heavy, not strictly blue-dominant; `b > 2g` (100.1 > 255.0) is false.
- `d3_corr=3993 < 9500` — the texcorr ≥ 0.95 conjunction ALSO fails on the
  0.55-exposure R2A renders (the death-board median of 0.9989 was measured on
  brighter fixtures and does not transfer).
- `fire=0`, no `kcap` line.

40/40 sampled R2A CCN-1 fixtures (indices 0–39): dmask=0 → all wrong-HC
(conf 756–852); dmask=4095 → zero kcap fires.
Harness colorconst adversarial (20 fixtures): 4 wrong-HC at dmask=0;
dmask=4095 → zero D3 fires (`d3_opp=0`, `d3_corr=9741` passes but the
conjunction still fails).

## Why calibration missed it

`CALIBRATION_C_ZAG.md` D3 was calibrated on:
- 20 NOISE fixtures (0 fires — the safety criterion), and
- the 95 death-board CCN-1 fixtures where texcorr rescued 82/95.

Neither set is the R2A battery's CCN-1 family (340 fixtures, 0.55 exposure,
xblue/xred illuminants with radial-blend textured surfaces). The
"opposite-cast" refinement (b > 2r ∧ b > 2g, added to drive NOISE fires to
zero) is incompatible with the actual fixtures' color distribution, and the
texcorr≥0.95 threshold is incompatible with their exposure level. Recall on
the target family was never measured before the freeze — the 0-FA criterion
was satisfied trivially.

## Consequence

CCN-1 contributes its full 335 wrong-HC to KD-1 (measured, 3 runs
byte-identical). KD-1 = 675 > 537 → FAIL. Per frozen §5 the knowledge
hypothesis DIES by measurement.

No source was modified. This is a measurement finding, not a fix proposal.
Any re-derivation of D3 must be calibrated with measured recall on the
actual R2A CCN-1 fixtures, not on NOISE/death-board surrogates.
