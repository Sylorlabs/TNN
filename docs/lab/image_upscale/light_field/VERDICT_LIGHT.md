# VERDICT: LIGHT-FIELD (wave-20260927-0221pdt sensory) -- KILL

Date: 2026-09-27. Status: KILLED by frozen bars. No judge brief. No sealed pair.

## Commit order (prereg-first rule satisfied)

1. 4a937d994 PREREG (frozen) -- no implementation
2. c6b8190f3 PREREG amendment 1 (pre-run correction; skycrop 512x184)
3. aa76f9b8d Implementation (azupscale_light.zag, azcrop.zag, azdb.zag)

## Toolchain

Pinned znc SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(verified before use). Pure Zag throughout. No Python anywhere.

## Battery (frozen)

1. Sealed canonical fixture (512x184 GT, 256x92 input; azprep from
   docs/lab/image_adaptivelayers/sealed/original_512.bmp).
2. Skycrop: rows 0..183 of docs/lab/image_upscale/generation/run_sky_1/gt.bmp
   (real photo), 512x184, input 256x92 via azcrop.zag (byte-verified crop rows
   and box filter against the source GT).

## BAR 0 (baseline re-verification): PASS

- Baseline rebuilt from pristine committed source (unmodified; git-clean).
- Two fresh runs byte-identical (deterministic).
- azdb.zag self-test ok; reproduces committed metrics:
  TNN 25.964 dB (frozen 25.96, tol 0.05); bicubic 25.889 dB (frozen 25.89).
- Baseline render SHA-256:
  0126450b6698bf882e94fec74aaff124a47c3f864dab4f8358f77b45cbeebb3f

## Results

| image  | baseline dB | variant dB | delta dB | checker mlv base | checker mlv var |
|--------|-------------|------------|----------|------------------|-----------------|
| sealed | 25.964      | 24.111     | -1.853   | 2328             | 7028            |
| skycrop| 31.563      | 30.885     | -0.678   | 719              | 1869            |

Mean delta: -1.266 dB. Variant deterministic (two fresh reruns byte-identical
on both images). Variant render SHAs:
  sealed: 2cecf9122317f6263e69c092daa9bc3e616b857a73e785577a28c86178b14503
  skycrop: 6a960231638ddd655379770118ccceefb7288b83e5ccb58bcd9a1836a753ec26
Baseline skycrop SHA:
  bd5503b5c0e3d62279c58713c137bacbcade168f863228b74981d977c285e665

Light-field estimates (from observed input only):
  sealed:  qx=(-16,-1,3) qy=(-88,-96,-107)
  skycrop: qx=(-14,-19,-19) qy=(21,17,15)

Label counts identical baseline vs variant on both images (light field changes
no labels, as designed). INVENTED (label 4) count = 0 in all four runs
(unchanged). Damage is concentrated in label 3 (SHAPES), the only label the
mechanism touches: sealed SHAPES odd-pixel SSE (R) 5,597,208 -> 9,935,327;
skycrop 142,840 -> 579,452.

Runtime: baseline 0.579 s, variant 0.563 s (ratio 0.97x; BAR 3 passes).

## Bar verdicts

- BAR 0 (baseline reproduces, deterministic): PASS.
- BAR 1 (mean delta >= 0.00, min >= -0.15, one >= +0.10): FAIL.
  Mean -1.266 dB; sealed -1.853 dB; skycrop -0.678 dB.
- BAR 2 (checkerboard no worse; INVENTED unchanged; LIGHT_FIELD trace line):
  FAIL on checkerboard (2.6x-3x worse on both images). INVENTED unchanged
  (0). Trace line present and deterministic.
- BAR 3 (runtime <= 1.05x): PASS (0.97x).
- Determinism (byte-identical reruns): PASS all four runs.

## Why it failed (mechanistic)

The estimator is sound: it correctly finds the real scene gradients
(sealed has a strong vertical gradient, qy ~= -100; skycrop a mild one).
The construction equation is wrong. Each region's mean is ALREADY the local
illumination estimated from the observed input; the atom deviations are
zero-mean. Adding the ABSOLUTE light field (0 at frame center, +/-q/2 at the
edges, i.e. up to ~50 levels for sealed) on top of the local mean
double-counts the illumination. The correct use of a global field would be
region-relative (field at pixel minus field at region center) or a shrinkage
of the region mean toward the field -- neither is what the frozen Section 3
specified, and the freeze cannot be changed post-hoc. The large absolute
shifts also drive many pixels into 0/255 clipping, which is why the
checkerboard tell (odd/even differences) amplifies 3x even though the field
itself is smooth.

## Red-team review (independent pass, per prereg Section 6)

- Knowledge vs architecture: not confounded. The knowledge (gradient
  estimate) is correct; the architecture (additive absolute re-basing) is
  wrong. The failure is cleanly in the construction equation.
- Metric gaming: none. Metrics got worse; the scorer is independent,
  self-tested, and reproduces the committed baseline to 0.004 dB.
- Local-structure leakage: no. The estimator is a genuine global summary
  (8x8 block medians, half-means). The flaw is double-counting, not leakage.
- Visual artifacts: YES. Side-by-side inspection: the variant shows a visible
  global brightness gradient shift plus amplified blockiness/seams at region
  boundaries. The difference image is dominated by a smooth vertical gradient
  of tens of levels. Human eyes agree with the metrics: clearly worse.
- Free-lunch cost claim: runtime 0.97x holds, but moot -- there is no lunch,
  free or otherwise.

## Verdict

KILL. The LIGHT-FIELD lever as preregistered degrades both images
substantially on every quality axis. The frozen bars worked as designed.
No judge brief is produced (nothing is ready). No sealed pair is fabricated.

## Lesson recorded

A global illumination estimate is only useful as a RELATIVE correction
(within-region variation) or as a shrinkage target for noisy local means --
never as an additive absolute offset on top of an already-correct local mean.
Any future light-field attempt must preregister the region-relative (or
shrinkage) formulation from the start; this round's additive formulation is
dead.
