# Gamma level strategy adoption: S2b fixed mastering gain (2026-09-24)

## Decision

Adopt **S2b FIXED MASTERING GAIN (true-peak variant)**: one constant
`G = 23197/124074` applied unchanged to every render, before the clamp.
Full measurement evidence:
`docs/lab/bytegen/gamma_repair/GAMMA_LEVELS_DECISION.md`.

## Why S2b

1. Gamma-free: 0 diffs on the R3 append-loud-frame test (PCM window
   [0,107484)). The S3 revert control, which restores the OLD normalizer,
   produces 107,428 diffs. The disease does not return under S2b.
2. Honest anchor: the constant is set from the true hottest mix peak
   (happy, 124074 pre-clamp samples; the rail%-named file scary is not the
   hottest by true peak). Every battery file peaks at or below -3 dBFS by
   construction: happy -3.00, song -3.46, scary -4.48, calm -16.11 dBFS.
3. One constant, no per-file knobs: unlike S1 (per-file plan-energy
   constants, which equalize peaks and flip loudness ordering so calm
   becomes loudest by RMS) and unlike S2 (task-literal G = 23197/104680,
   which leaves happy at -1.52 dBFS, above the -3 dBFS target).
4. Dynamics preserved: envelope Pearson r = 1.000000 vs the OLD normalized
   render on every file (a single constant multiplied over the mix is
   bit-for-bit proportional, exactly like OLD's normalizer); per-file
   crest factors preserved (16.6 / 18.3 / 12.8 / 10.9 dB); 0% railed
   samples, vs 4-17% railed on three of four files at gain 1 with crushed
   crest (6.5 / 8.0 / 4.4 dB).
5. Deterministic: pure Zag, zero RNG, every battery rendered 2x with
   byte-identical SHAs.

## Measured evidence (hifi battery, 44.1 kHz, 2x byte-identical)

| strategy | gamma diffs | rails % | peak dBFS (song/happy/scary/calm) |
|---|---:|---:|---|
| NEW_gain1 (committed repair) | 0 | 5.896 / 4.058 / 16.936 / 0.000 | +0.00 / +0.00 / +0.00 / -1.54 |
| S2b (adopted) | 0 | 0.000 | -3.46 / -3.00 / -4.48 / -16.11 |
| S2 (task-literal) | 0 | 0.000 | -1.98 / -1.52 / -3.00 / -14.63 |
| S1 (re-stage) | 0 | 0.000 | -3.16 / -3.18 / -3.13 / -3.03 |
| S3 (OLD normalizer) | 107428 | 0.000 | -2.70 / -2.70 / -2.70 / -2.70 |

-3 dBFS = 23197 samples (32768 x 10^(-3/20) = 23197.97). S3 pins every
file at exactly -2.70 dBFS (= 24000/32768), the prereg bar value.

## What it supersedes

1. The OLD output-derived peak normalizer (peak exactly 24000 per file).
   It is the gamma-disease mechanism: the S3 control reproduces the
   disease exactly (107,428 diffs). Per-output peak normalization is
   retired for all future renders.
2. The "peak exactly 24000" bar (HIFI-PREREG H3 / MOOD2-RESULTS H3,
   -2.70 dBFS). No gamma-free strategy can pass it; it is superseded by
   the fixed mastering gain, pending the signed amendment below.

## Amendment text (NEEDS MICAH'S SIGNATURE, not yet signed)

HIFI-PREREG H3 / MOOD2-RESULTS H3 amendment: the bar "peak exactly
24000" (-2.70 dBFS) is replaced by: each battery file peaks at or below
-3 dBFS under the fixed mastering gain G = 23197/124074; inter-file
relative levels are preserved from the mix with no per-file
normalization; per-output peak normalization is forbidden. The OLD
output-derived peak normalizer is the gamma-disease mechanism and must
not be restored.

Status: strategy adopted by Micah's directive 2026-09-24 ("commit the
good one"). This amendment is drafted only and takes effect when signed.

Signature: _______________  Date: _______________

## Provenance

- Decision evidence: GAMMA_LEVELS_DECISION.md, same directory
  (committed 1d25b755; re-committed here byte-identical).
- Measurement used the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` and the
  committed NEW/OLD sources; known committed-source closure gap
  (missing sin_lut.zag and toolchain/R33_NATIVE_IO_V1.zag at the expected
  relative path) is documented in the decision doc and unchanged by this
  adoption.
