# CALIBRATION_5100.md - F1-BUFFER training calibration (5100-series)

Lane F1-BUFFER, wave wave-20261001-2321pdt. This record covers
calibration ONLY, on the F1-FOLLOWUP Part 2 sealed artifacts, which
are training knowledge for this lane (per the lane task: the
5100-series and the 2301 fixture are training knowledge, not test
data). No fresh fixture was generated and no fresh learner run was
executed in this step. All analysis is pure Zag (dev/bufx,
dev/bufsep), compiled by the pinned znc.

No em-dashes are used in this document.

## Method

For each of the 24 Part 2 seeds (i = 0..23), dev/bufx read the
committed train trace
../F1-FOLLOWUP/runs2/1/s2_<i>_train.trace and reported the
first-trigger buffer: trig (first TRIGGER episode), n (buffer
episodes), S0/S1 (sums of x0/x1 over episodes 0..trig). Labels are
transcribed from F1-FOLLOWUP/SEALED_EVAL_PART2.md section 2:
OVERFIT = seeds 2, 3, 5, 13, 17, 18; CORRECT = all others.
dev/bufsep then reported the best single-threshold separation per
buffer feature (S0, S1, D=|S0-S1|, T=S0+S1, M=min(S0,S1), N, TRIG,
R=D/T) in both directions.

## Calibration table (dev/calib_5100.txt)

SEED 0 CORRECT S0=6 S1=7 N=3 TRIG=2
SEED 1 CORRECT S0=3 S1=3 N=3 TRIG=2
SEED 2 OVERFIT S0=8 S1=4 N=2 TRIG=1
SEED 3 OVERFIT S0=6 S1=5 N=2 TRIG=1
SEED 4 CORRECT S0=3 S1=5 N=2 TRIG=1
SEED 5 OVERFIT S0=6 S1=6 N=2 TRIG=1
SEED 6 CORRECT S0=3 S1=7 N=2 TRIG=1
SEED 7 CORRECT S0=6 S1=3 N=2 TRIG=1
SEED 8 CORRECT S0=3 S1=3 N=2 TRIG=1
SEED 9 CORRECT S0=0 S1=4 N=2 TRIG=1
SEED 10 CORRECT S0=3 S1=5 N=2 TRIG=1
SEED 11 CORRECT S0=5 S1=6 N=2 TRIG=1
SEED 12 CORRECT S0=8 S1=6 N=2 TRIG=1
SEED 13 OVERFIT S0=5 S1=7 N=2 TRIG=1
SEED 14 CORRECT S0=3 S1=3 N=2 TRIG=1
SEED 15 CORRECT S0=5 S1=4 N=2 TRIG=1
SEED 16 CORRECT S0=3 S1=5 N=2 TRIG=1
SEED 17 OVERFIT S0=5 S1=6 N=2 TRIG=1
SEED 18 OVERFIT S0=3 S1=7 N=2 TRIG=1
SEED 19 CORRECT S0=0 S1=7 N=2 TRIG=1
SEED 20 CORRECT S0=3 S1=8 N=2 TRIG=1
SEED 21 CORRECT S0=5 S1=4 N=2 TRIG=1
SEED 22 CORRECT S0=7 S1=4 N=2 TRIG=1
SEED 23 CORRECT S0=5 S1=5 N=2 TRIG=1

## Separation results (dev/bufsep output, misc = misclassified seeds)

SEP S0 ge k=8 misc=6 | le k=0 misc=6
SEP S1 ge k=8 misc=7 | le k=3 misc=6
SEP D ge k=7 misc=7 | le k=0 misc=6
SEP T ge k=12 misc=5 | le k=4 misc=6
SEP M ge k=5 misc=6 | le k=0 misc=6
SEP N ge k=3 misc=8 | le k=2 misc=6
SEP TRIG ge k=2 misc=8 | le k=1 misc=6
SEP R ge k=1/1 misc=8 | le k=0/6 misc=6

Best single-feature rule on training: T >= 12 predicts OVERFIT,
misc = 5/24 (cells ovf_ge=3 cor_ge=2 ovf_lt=3 cor_lt=16).

## Collision proof (ceiling for this feature family)

Two pairs of seeds are identical on EVERY frozen buffer feature
(S0, S1, D, T, M, N, TRIG, R) yet carry opposite labels:

- Seed 6 CORRECT vs seed 18 OVERFIT: both (S0,S1,N,TRIG) = (3,7,2,1).
  Their first two fixture episodes are the same multiset {(1,3),(2,4)}
  in swapped order; their first bursts are identical (2x1, then the
  degenerate 3x1 re-add). They diverge at episode 2+: seed 6 is
  repaired by a later full-buffer trigger (episode 12), seed 18
  stalls. The first-trigger buffer does not determine the outcome.
- Seed 11 CORRECT vs seed 17 OVERFIT: both (5,6,2,1). Same sums,
  different episode distributions ({(1,3),(4,3)} vs {(4,4),(1,2)}),
  different second constructs (complementary 2x1+x0 vs degenerate
  4x1 double-accumulator). Even the greedy second step is not fixed
  by the (S0,S1) sums, only by the full buffer contents.

Therefore NO deterministic rule over the frozen buffer features can
beat misc = 2 on this training series. The error-mass-balance
hypothesis in single-threshold form (R, D) is falsified on training
data (misc 7 to 8).

## Frozen rule chosen for the sealed test

Predict OVERFIT iff T >= 12, where T = S0 + S1 over the
first-trigger buffer. This is the best-calibrated single-feature
rule (misc 5 on training). It is frozen as-is in PREREG_BUFFER.md;
the sealed test on the fresh 8100-series is a genuine out-of-sample
check of whether the best available buffer rule generalizes. The
prereg records the training misc honestly and names
BUFFER-NOT-PREDICTIVE as the reference outcome.
