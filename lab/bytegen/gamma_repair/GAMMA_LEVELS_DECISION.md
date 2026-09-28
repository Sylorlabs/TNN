# Gamma-disease level strategies: empirical decision data (2026-09-24)

Micah's order: test all options, do not pick a strategy, bring data. This document
reports measured waveform evidence for three level strategies plus one
measurement-discovered sub-variant. Analyzer-first: every claim below is a
waveform measurement, not a listening claim. No strategy is recommended here.

## The three strategies (plus one discovered sub-variant)

- **S1 RE-STAGE** — per-file plan-energy scale factors (exact rational constants
  baked into the Zag source), so each battery file peaks at −3 dBFS under gain 1.
- **S2 FIXED MASTERING GAIN** — one constant `G = 23197/104680` applied unchanged
  to every render. Per the task brief, `G` is set so the task-named hottest file
  (`f3mood_scary`, 16.94% railed at gain 1) peaks at exactly −3 dBFS.
- **S2b FIXED MASTERING GAIN (true-peak variant)** — one constant `G = 23197/124074`,
  set from the *true* hottest mix peak. Discovered during measurement: by rail% the
  hottest file is scary, but by pre-clamp mix peak it is happy (124074 > 104680).
  Under S2b every battery file peaks at or below −3 dBFS.
- **S3 REVERT CONTROL** — the OLD output-derived peak normalizer (peak exactly
  24000 per file), confirming the gamma disease returns.

Baselines shown for reference: `NEW_gain1` = the committed gamma repair at gain 1
(unchanged behavior), `S3_revert` = OLD normalized battery.

## Headline measurement table (hifi battery, 44.1 kHz)

Peak and rail% are the strategy's level outcome; RMS dBFS and crest factor (dB)
describe dynamics; the gamma column is the R3 append-loud-frame test
(diffs in PCM window [0,107484)); envelope r is per-frame RMS-envelope
Pearson correlation vs the OLD normalized render (frames of 4410 samples = 0.1 s;
final tail truncated to whole frames identically for all strategies).

| file | strategy | peak (samples) | peak dBFS | rail % | RMS dBFS | crest dB | gamma diffs | env r vs OLD |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| song | NEW_gain1 | 32768 | +0.00 | 5.896 | −6.48 | 6.48 | 0 | 0.9665 |
| song | **S1** | 22764 | −3.16 | 0.000 | −19.76 | 16.60 | 0 | 0.9999 |
| song | **S2** | 26089 | −1.98 | 0.000 | −18.64 | 16.66 | 0 | 1.0000 |
| song | **S2b** | 22011 | −3.46 | 0.000 | −20.12 | 16.66 | 0 | 1.0000 |
| song | **S3** | 24000 | −2.70 | 0.000 | −19.37 | 16.66 | 107428 | 1.0000 |
| happy | NEW_gain1 | 32768 | +0.00 | 4.058 | −7.98 | 7.98 | 0 | 0.9860 |
| happy | **S1** | 22725 | −3.18 | 0.000 | −21.49 | 18.31 | 0 | 1.0000 |
| happy | **S2** | 27494 | −1.52 | 0.000 | −19.88 | 18.36 | 0 | 1.0000 |
| happy | **S2b** | 23197 | −3.00 | 0.000 | −21.36 | 18.36 | 0 | 1.0000 |
| happy | **S3** | 24000 | −2.70 | 0.000 | −21.06 | 18.36 | 107428 | 1.0000 |
| scary | NEW_gain1 | 32768 | +0.00 | 16.936 | −4.38 | 4.38 | 0 | 0.9715 |
| scary | **S1** | 22844 | −3.13 | 0.000 | −15.96 | 12.83 | 0 | 1.0000 |
| scary | **S2** | 23197 | −3.00 | 0.000 | −15.82 | 12.82 | 0 | 1.0000 |
| scary | **S2b** | 19571 | −4.48 | 0.000 | −17.30 | 12.82 | 0 | 1.0000 |
| scary | **S3** | 24000 | −2.70 | 0.000 | −15.52 | 12.82 | 107428 | 1.0000 |
| calm | NEW_gain1 | 27441 | −1.54 | 0.000 | −12.40 | 10.86 | 0 | 1.0000 |
| calm | **S1** | 23120 | −3.03 | 0.000 | −13.88 | 10.85 | 0 | 1.0000 |
| calm | **S2** | 6080 | −14.63 | 0.000 | −25.49 | 10.86 | 0 | 1.0000 |
| calm | **S2b** | 5130 | −16.11 | 0.000 | −26.96 | 10.86 | 0 | 1.0000 |
| calm | **S3** | 24000 | −2.70 | 0.000 | −13.56 | 10.86 | 107428 | 1.0000 |

Notes on the table:

- −3 dBFS = 23197 (32768 × 10^(−3/20) = 23197.97). S1 lands at −3.03…−3.18 dBFS:
  the −0.03…−0.18 dB shortfall is deterministic integer truncation when the
  rational scale factor is applied to plan-energy cells; it is part of the
  measured result, not a failure.
- S2 (task-literal): scary lands at exactly −3.00 dBFS; happy lands at **−1.52 dBFS,
  above the −3 dBFS target** — the "hottest file" named in the brief (scary, by
  rail%) is not the hottest by true mix peak (happy, 124074). 0% rails either way.
- S2b: all four files at or below −3.00 dBFS by construction.
- S3: every file pinned at exactly −2.70 dBFS (= 24000/32768) — the prereg bar value.
- Crest factor is preserved identically by S1/S2/S2b/S3 per file
  (16.6 / 18.3 / 12.8 / 10.9 dB); the gain-1 clipped baseline crushes it
  (6.5 / 8.0 / 4.4 dB). Clipping visibly reshapes the dynamics envelope
  (env r 0.97–0.99 vs OLD); the three strategies restore it (r = 0.9999–1.0000).
- S2/S2b envelope correlation vs OLD is exactly 1.000000: both are a single
  constant multiplied over the mix, exactly like OLD's normalizer, so the
  envelope shape is bit-for-bit proportional.
- No two files share a SHA-256 across the full 20-file set (5 strategies × 4 files).

## What the numbers say about each strategy (neutral trade-offs)

**S1 RE-STAGE.** Every file peaks at −3 dBFS (±0.2 dB), 0% rails, gamma-free
(R3 diffs 0), envelope correlation ≈1 vs OLD. Costs visible in the data: (a) it
equalizes *peaks*, not loudness — calm, the densest file (lowest crest, 10.9 dB),
becomes the loudest by RMS (−13.88 dBFS, louder than scary's −15.96); (b) each new
plan needs its own staging constant derived from a mix-peak measurement —
the constants here were computed offline from measured mix peaks (song 117734,
happy 124074, scary 104680, calm 27441) and baked in as exact rationals
(23197/117734, 23197/124074, 23197/104680, 23197/27441); the emitter itself
measures nothing at render time.

**S2 FIXED MASTERING GAIN (G = 23197/104680).** One constant for all files;
preserves the plans' relative levels exactly (scary loudest, calm quietest —
same ordering as the gain-1 baseline); gamma-free (R3 diffs 0); envelope
correlation exactly 1.000000 vs OLD; 0% rails. Costs visible in the data:
(a) only the task-named file lands at −3.00 dBFS — happy peaks at −1.52 dBFS and
song at −1.98 dBFS, both above the −3 dBFS target; (b) calm drops to −14.63 dBFS
peak / −25.49 dBFS RMS, far below the others (inter-file spread preserved, so the
quietest plan stays quiet).

**S2b FIXED MASTERING GAIN (G = 23197/124074).** Same single-constant machinery as
S2, but the constant is set from the true hottest mix peak (happy, 124074), so all
four files peak at or below −3.00 dBFS (happy exactly −3.00). All other measured
properties match S2: gamma-free, envelope r = 1.000000 vs OLD, 0% rails,
relative levels preserved (calm −16.11 dBFS peak / −26.96 dBFS RMS).

**S3 REVERT CONTROL.** Restores the OLD output-derived normalizer: every file
pinned at exactly −2.70 dBFS (24000), 0% rails, envelope preserved — and the
gamma disease returns exactly as before (R3 append-loud-frame: 107,428 diffs in
PCM window [0,107484) vs 0 for all other strategies). This is the disease-positive
control; it behaves as the repair note predicts.

**Baselines.** NEW_gain1 (the committed repair, unchanged): gamma-free and
deterministic, but 4–17% of samples railed on three of four files, with crest
factors crushed by clipping (6.5/8.0/4.4 dB vs the true 16.6/18.3/12.8 dB).

## Governance flags (need Micah's signature; NOT amended here)

- HIFI-PREREG H3 / MOOD2-RESULTS H3 ("peak exactly 24000", −2.70 dBFS) cannot pass
  under S1 (−3.03…−3.18 dBFS) or S2/S2b (−1.52…−16.11 dBFS). If either strategy is
  chosen, those bars need a signed prereg amendment. S3 keeps them passing.
- REPAIR_NOTE.md says "peak 26056" for f3mood_calm.wav; the waveform's true
  absolute peak is **27441** (min −27441, max +26056) — 26056 is only the positive
  maximum. Flagged as a correction, not silently edited.
- Committed-source closure gap (first class): the committed tree contains
  `docs/lab/imagination/src/field.zag` but not its imported `sin_lut.zag`, and not
  `toolchain/R33_NATIVE_IO_V1.zag` at the expected relative path — a pristine
  isolated checkout cannot build the emitter closure as committed. This test
  rebuilt the committed OLD/NEW `field.zag` blobs with the pinned toolchain plus
  the local `sin_lut.zag` and `R33_NATIVE_IO_V1.zag`; that substitution is part
  of the provenance of every number above.

## Method and reproducibility (how the numbers were produced)

- Pure Zag for all synthesis/instrument code; Python + wave + numpy for analysis only.
- Toolchain pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Committed sources: NEW `88eb0d6b33b6`, OLD parent `094d14d6`, prereg `f472ca9c53b4`
  (extracted from the `tnn-native-lab` branch history).
- True mix peaks (pre-clamp) were measured by a pure-Zag instrument (`f3mixpeak`
  mode, additive to a copy of the NEW source): song 117734, happy 124074,
  scary 104680, calm 27441. Rendered gain-1 absmax (32768 on three files) is the
  clamp rail, NOT the true peak — early provisional factors derived from it were
  discarded before measurement.
- S1 implementation: `f3_s1_scale` multiplies every energy cell of a freshly built
  plan by the exact rational 23197/PEAK (per-file PEAK above) via integer
  multiply-then-divide; the gain-1 hifi emitter is untouched.
- S2/S2b implementation: `f3_emit_wav_hifi_s2` multiplies each signed mix sample
  by the exact rational G = 23197/104680 (S2) or 23197/124074 (S2b) before the
  clamp; plan and base emitter untouched.
- S3: the OLD binary rebuilt from the committed OLD source with only filename
  remapping + the R3 proof scaffold (45 diff lines, all mechanical).
- Zero RNG anywhere; every battery rendered 2× (S2b 2×) with byte-identical SHAs.
- Variant sources and the analysis script are preserved at
  `~/workspace/gamma_work/` (`gen_variants.py`, `measure.py`, `build_s1/`,
  `build_s2/`, `build_s2b/`, `field_oldproof_src.zag`, `build_inst/`).

## Micah's three choices (no recommendation)

1. **S1 RE-STAGE** — per-file constants, every file at −3 dBFS, loudness ordering
   across files changes (calm loudest by RMS), per-plan staging work forever.
2. **S2 FIXED MASTERING GAIN** — one constant, relative levels preserved;
   choose the constant's anchor: **G = 23197/104680** (task-literal; scary at
   −3.00 dBFS, happy at −1.52 dBFS) or **G = 23197/124074** (true hottest peak;
   all files at or below −3.00 dBFS).
3. **S3 REVERT CONTROL** — restore output-derived normalization; gamma disease
   returns (107,428 R3 diffs); prereg H3 bars keep passing unchanged.

Whichever is chosen, HIFI-PREREG H3 / MOOD2-RESULTS H3 need a Micah-signed
amendment unless the choice is S3.
