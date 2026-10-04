# ADDENDUM A1 to PREREG ST-1 - measurement-point clarification for KB2

Wave: wave-20260925-0521pdt. Date: 2026-09-25 05:55 PDT.
Parent prereg: PREREG_ST1_AUD.md, commit d7c5253ad (prereg-only,
committed alone before any ST-1 code). This addendum is committed
before any implementation commit. It clarifies a measurement point;
it does not weaken, narrow, or re-interpret any bar to force a pass.

## The issue

KB2 as frozen reads: |10*log10(E_st / E_dry)| <= 0.5 dB. Read
literally on the final WAV files, this bar is confounded: the frozen
mono writer peak-normalizes by the dry Q24 peak while the frozen
stereo writer peak-normalizes by the stereo Q24 peak. The loudest
score elements (white bed, hum, breath, wind, all center-panned at
gL=gR=0.7071) make the stereo peak about 0.707x the dry peak, so a
WAV-level energy ratio would read about +3 dB even with a perfect
positioning stage. That +3 dB is presentation normalization, not the
mechanism under test. KB2's stated intent ("energy preserved: the
piece is the same piece, only positioned") is about the positioning
stage.

## The clarification (not a weakening)

KB2 is measured at the positioning stage: pre-normalization Q24
accumulator mean-squares, which the ST-1 binary reports exactly in
its trace. The numeric bar is unchanged: the ratio
(MS_L + MS_R) / MS_dry must lie in [0.8913, 1.1220] (the exact
f64 bounds for +/-0.5 dB), where MS_dry is the sum of per-stem
mean-squares (integer-exact: each stem sample squares to at most
2^48 and the 926100-sample sum stays below 2^53) and MS_L, MS_R are
the accumulator mean-squares. The verifier parses these from the
trace FIELD line and checks the ratio; the computation is exact to
f64 rounding (relative error about 1e-13, far below the bar).

## Sanctioned additive trace fields (diagnostic only)

The prereg froze trace decision lines (element, stem index, pan,
gL, gR). This addendum sanctions two additive diagnostic fields,
which change no mechanism and no frozen constant:
- each STEM line gains e_raw=<i64>, the stem's Q24 mean-square
  (integer-exact per above);
- a final FIELD line: FIELD ms_dry=<i64> ms_L=<i64> ms_R=<i64>.
KB6 and KB7 remain measured on the final WAV files (they
characterize the delivered artifact: mono compatibility and crest
character as Micah would hear them). All other bars are unchanged.
