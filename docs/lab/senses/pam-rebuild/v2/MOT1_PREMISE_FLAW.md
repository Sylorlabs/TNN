# MOT-1 premise flaw: truth label is unobservable from the stimulus

**Date:** 2026-09-23. **Crew:** PAMs v2 gap crew D (calibration claim + benchmark integrity).
**Status:** finding documented; no frozen state modified.

## Claim under test

The autopsy death-board (v2/autopsy/AUTOPSY_DEATHBOARD.md, §R2-10 breakdown)
claims R2A-MOT-1 (327 of R2-10's false installs) is "not a perceptual failure
but a benchmark premise flaw: the generator reverses frames yet labels
pre-reversal direction, so the pixels depict the opposite direction — truth
unobservable from the stimulus."

## Finding: CONFIRMED

**Generator inspection** (`round2/fixtures/gen_r2a.py`, `gen_motiondir_adv`,
R2A-MOT-1 branch, adv idx < 350):

```python
# R2A-MOT-1: constant-velocity motion played backward.
# Truth = true (pre-reversal) direction.
truth = DIR8[rng.int(8)]
frames = _motion_frames(rng, truth, 2, 1.0, rng.int(170))
frames = frames[::-1]  # reversal: fools constant-velocity predictors
...
G.write_truth(p, truth)
```

The 8 frames are rendered with content moving in `truth` (2 px/frame,
photographic window translation), then the frame ORDER is reversed before
writing. The stored `.vid` therefore depicts constant-velocity motion in the
exact OPPOSITE direction, while the `.truth` file records the pre-reversal
direction. Nothing in the stimulus records that a reversal happened; the
reversal is a fact about the generation procedure, not the pixels.

**Pixel measurement** (independent of the generator code): on a 50-fixture
sample (`r2a_motiondir_0000.vid` … `r2a_motiondir_0349.vid`, every 7th), the
apparent motion direction was estimated per fixture by frame-to-frame SSD
shift search over the central 32×32 window (majority vote over 7 frame pairs,
nearest of the 8 direction names):

- apparent direction == OPPOSITE of truth label: **50/50**
- apparent direction == truth label: **0/50**

A perceptual system that correctly estimates motion direction from pixels
will therefore "fail" every MOT-1 fixture by construction. The 327 MOT-1
false installs in R2-10 are not evidence of a perceptual deficit; they are
evidence that the front end reads the pixels honestly.

## Scope and limits

- This does not claim direction estimation is solved: MOT-2 (distractor
  motion) and MOT-3 (camouflage) remain genuine perceptual challenges, and
  the death-board classifies both as KNOWLEDGE (fixable), not premise flaws.
- The "unrecoverable" qualifier is a benchmark-design judgment, per the
  death-board's own caveat: a system with explicit video-reversal knowledge
  could in principle detect a temporal splice, but the truth label
  (pre-reversal direction) remains unobservable from the pixels alone — no
  amount of perceptual improvement on the stimulus can recover it.
- Recommendation: MOT-1 fixtures (`r2a_motiondir_0000.vid` … `r2a_motiondir_0349.vid`)
  should be excluded from direction-accuracy scoring or relabeled to the
  depicted (post-reversal) direction. Either change requires Micah's prereg
  amendment; this document is the evidence, not the change.

## Files

- Measurement script (analysis only): `~/workspace/pamv2_gapD/meas_mot1.py`
  (kept in crew scratch, not committed).
- Generator: `round2/fixtures/gen_r2a.py` (frozen, unmodified).
