# SENSORY_PREP.md - verdict recording template for the SENSORY verdict

Wave: wave-20261001-2321pdt. Lane: SENSORY.
Prep lane: SENSORY-PREP (replacement worker). Prepared 2026-10-02 ~00:45 PDT.
The SENSORY lane is rendering the H2v1 FSDF candidate; its verdict is expected
in ~45-60 min. This file lets the coordinator record the verdict quickly when
it lands. No outcome is predicted here.

## 1. The candidate: H2v1 FORWARD-SCATTER DECK FIELD (FSDF)

Tag [NEW]. A deck-scale sun-anchored angular luminance field applied as a
radiance multiplier on H1-family alpha clouds, replacing the baseline's flat
sunAmt color mix inside the thin-cirrus block of b_sky (the `if (dy > 0.02)`
block, nothing else).

Physical basis: forward scattering brightens clouds toward the sun; the
anti-solar deck dims. The field is computed per pixel from the ray and the
frozen T1 sun:

- samt = b_sunamt(dx, dz), per-pixel sun amount from the frozen sun azimuth
  (horizontal projection of the T1 sun vector (-0.617, 0.191, -0.764))
- fwd = b_ss((samt - 0.65) / 0.10)      (forward lobe, toward the sun)
- anti = b_ss((0.70 - samt) / 0.10)     (anti-solar wing, away)
- field = 1.0 + 0.10 * fwd - 0.50 * anti

Density and alpha are lane-standard infrastructure, unchanged from H1v2:
h1_dens (seeds 601/602), cov = b_ss((den - 0.52) / 0.14), a = cov * hf clamped
to 1.0. Cloud color channels are b_mix(lo, hi, sunAmt) multiplied by the field,
then alpha-blended into the ray.

This is a new mechanism, not a retune: it abandons H1v2's per-blob light logic
entirely (no density gradients, no march, no per-blob terms) and operates at
deck scale, the scale the bar measures. Zero new fbm octave-evals per sky
pixel (free-lunch cost class; H1v2 added 26).

Frozen design-calculator predictions at (0.10, 0.50): KB3 sunmean 3.94,
antimean -5.85, diff 9.80; KB4 variance 196.13; KB7 |fsmean| 0.57, bigfrac
0.2013; KB11 max|dL| 48.46; KB2 0.2916; KB10 range 0.60, argmax x = 320.
All bars predicted PASS with margin on geometry; the bars decide on real
renders.

Baseline: r11_alien.zag byte copy with only the @import line repointed at the
vendored IO substrate; 1024x1024 reference size; determinism gate of two
byte-identical baseline renders matching the 1721pdt baseline sha
72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b.

## 2. Frozen kill bars KB1-KB11 (from PREREG_SENSORY_H2V1.md)

- KB1-DET: 3 renders of the H2v1 variant at 1024, sha256 identical across all
  3. Else FAIL.
- KB2-COVERAGE: fraction of kept SKYWIN with cloud alpha a > 0.15 (a
  recomputed by the verifier from the frozen H2v1 alpha math) in [0.08, 0.60].
  Expected 0.2916 (H1v2-measured).
- KB3-LIGHTLOGIC: mean(dL over SUNHALF kept) - mean(dL over ANTISUN kept)
  >= 6.0, AND mean(dL over SUNHALF kept) >= 3.0. Same bar as H1v2, unchanged
  strictness.
- KB4-STRUCTURE: variance of dL over SKYWIN kept >= 40.0.
- KB5-NONREG-TERRAIN: mean |dL| over TERRAIN kept <= 1.0.
- KB6-NONREG-MOON: mean |dL| over MOON kept <= 1.0.
- KB7-SKYCALM: |mean(dL) over FULLSKY kept| <= 5.0, and fraction of FULLSKY
  kept with |dL| > 12 <= 0.35.
- KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio variant/baseline
  over ACU <= 1.15.
- KB9-COST: variant 1024 wall time <= 2.0x baseline 1024 wall time
  (matched-contention pairing rule, same as H1v2), and extra fbm
  octave-evals per sky pixel reported (expected 0).
- KB10-ANCFIELD (replaces KB10-ALIGN for the new mechanism): the verifier
  recomputes per kept SKYWIN pixel samt = b_sunamt(rdx, rdz) and the frozen
  field. Clause A: the kept pixel maximizing field has x < 512 (bright lobe
  on the sun side). Clause B: max(field) - min(field) over kept SKYWIN >=
  0.40. Else FAIL.
- KB11-DROPOUT: fraction of kept FULLSKY with |dL| > 60 equals 0.0. Any hard
  blowout or dropout fails. Additionally the verdict worker must document a
  knowledge-vs-architecture investigation of the renders for dropout,
  flicker, banding, or weirdness before any verdict, per the standing
  red-team rule.
- VKB-EYE: a sealed blind A/B pair (baseline vs H2v1 variant, 1024 PNG) is
  prepared for Micah ONLY if every frozen bar passes. Randomized, mapping
  sealed in SEALED_MAPPING. He is the judge. Nothing is adopted on metrics
  alone: a passing candidate is READY-FOR-JUDGE only.

Point sets (all at 1024x1024): SKYWIN 48 points kept >= 36; SUNHALF/ANTISUN
split at x = 510, each >= 12; TERRAIN 64 kept >= 56; MOON 16 kept >= 12;
FULLSKY 144 kept >= 100; ACU from kept SKYWIN. Luma L = (299R + 587G +
114B) / 1000 on final BMP bytes; dL = L_variant - L_baseline. Geometric
validator keep-count asserts run FIRST on the rebuilt baseline; any failure
DISCARDS the candidate (prereg-spec defect; G1-v1 precedent).

## 3. What H2v1 replaces: H1v2 BUILD-FAIL

H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK (wave-20261001-2021pdt) was BUILD-FAIL
on two frozen bars:

- KB3-LIGHTLOGIC FAIL: sun mean +0.64 vs >= 3.0; diff +0.72 vs >= 6.0.
  Mechanism-level negative result: per-blob contrast (KB4 variance 89.58)
  averaged to near zero within each screen half; the frozen bar measures a
  systematic half-level shift, which per-blob light logic cannot move.
- KB9-COST FAIL: 2.36x vs <= 2.0x; +26 fbm octave-evals per sky pixel that
  the prereg prediction missed.

KB1/2/4/5/6/7/8/10/11 passed; KB11 = 0, no artifacts. Full record:
docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/IMPLEMENTATION.md.

Standing owner rule carried into this wave: stop micro-tweaks; hunt a BIGGER
realism lever. H2v1 answers the diagnosed failure by moving the effect to deck
scale, at zero new fbm cost.

## 4. Verdict recording template

Fill when the SENSORY lane verdict lands. Do not alter frozen bars.

- Candidate: H2v1 FORWARD-SCATTER DECK FIELD (FSDF)
- Governing prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY/PREREG_SENSORY_H2V1.md
  (frozen 2026-10-01 23:55 PDT)
- Verdict: BUILD-PASS / BUILD-FAIL   (circle one; KB11 + red-team doc required first)
- Per-bar results:

| Bar | Frozen bar | Measured | PASS/FAIL |
|-----|-----------|----------|-----------|
| KB1-DET | 3/3 renders sha256-identical | sha(s): ____ | |
| KB2-COVERAGE | coverage in [0.08, 0.60] (exp 0.2916) | ____ | |
| KB3-LIGHTLOGIC | sunmean >= 3.0 AND (sun - anti) >= 6.0 (pred 3.94 / 9.80) | sun ____ anti ____ diff ____ | |
| KB4-STRUCTURE | var(dL, SKYWIN) >= 40.0 (pred 196.13) | ____ | |
| KB5-NONREG-TERRAIN | mean \|dL\| <= 1.0 | ____ | |
| KB6-NONREG-MOON | mean \|dL\| <= 1.0 | ____ | |
| KB7-SKYCALM | \|fsmean\| <= 5.0 AND bigfrac <= 0.35 (pred 0.57 / 0.2013) | fsmean ____ bigfrac ____ | |
| KB8-ANTIGRAIN | acutance ratio <= 1.15 | ____ | |
| KB9-COST | wall <= 2.0x baseline (exp 0 new fbm evals) | ____x, fbm/px ____ | |
| KB10-ANCFIELD | argmax-field x < 512 AND field range >= 0.40 (pred x=320 / 0.60) | x ____ range ____ | |
| KB11-DROPOUT | frac(\|dL\|>60) == 0.0 | ____ | |

- Red-team investigation documented (KB11 companion): YES / NO (required before any verdict)
- Baseline gate evidence: one-line diff verified / 2 baseline renders byte-identical /
  baseline sha matches 72e665...1ab8b / keep-count asserts pass
- Verdict line: ________________________________________
- Failed bars: ________________________________________
- If PASS: blind A/B pair prepared for Micah (SEALED_MAPPING), verdict = READY-FOR-JUDGE
  (nothing adopted on metrics alone)
- Provenance header for JUDGE_BRIEF.md: RENDER_SHA ____, FIRST_RENDERED_WAVE
  wave-20261001-2321pdt, COMPONENT_LINEAGE (see prereg)

Coordinator notes: record the verdict verbatim from the SENSORY lane's
IMPLEMENTATION.md / verdict file; do not re-run renders here.
