# R2-16 B-holdout design note (frozen before generation)

Date: 2026-09-23. Generator: `src/gen_holdout.py`.
Seed: MASTER=20260923, STREAM_BASE=960 (fresh; no overlap with R2A streams
400/500/700/900). Per-fixture seed =
splitmix64(splitmix64(MASTER ^ stream*0x9E3779B97F4A7C15) ^ index*0xBF58476D1CE4E5B9).
No RNG in any decision path; numpy/PIL only for arithmetic/rendering.

## Allocation (prereg §2.5: 10 families x 1,000)

| # | Family tag   | Task       | Truth | Adversarial mechanism (targets formation, G keeps truth evidence) |
|---|--------------|------------|-------|------------------------------------------------------------------|
| 1 | R2H16-COL-1  | colordisc  | SAME  | Digital x1.3 gain on view B (sensor-processing corruption, not an illuminant change like R2A-COL-2). Formation mean-RGB distance fooled; challenge sees identical spectra. |
| 2 | R2H16-CCN-1  | colorconst | DIFFERENT | Local-patch doppelganger: c2 = c1 with an 8x8 patch replaced by a far color. Both mean quantities blind to the small patch. |
| 3 | R2H16-CCN-2  | colorconst | DIFFERENT | Cross-crop collision: different photo crops whose d65 mean-RGB (challenge) and warm mean-chromaticity (formation) both collide; found by deterministic 1500-crop pool search (thresholds: dRGB<10, dChroma<55, fallback <16/<75). |
| 4 | R2H16-SHP-1  | shapetrans | class | Hollow shapes (thin ring/outline): bbox fill-ratio collapses -> TRIANGLE; G is the clean filled re-render (challenge reports truth). |
| 5 | R2H16-SHP-2  | shapetrans | class | Dual shape: target + separated distractor of another class; formation bbox covers both. G = clean filled target. |
| 6 | R2H16-PTC-1  | pitchdisc  | SAME  | Overmodulated AM (mod index 1.5 @30Hz) on toneB: envelope crosses zero -> extra zero-crossings explode the count ratio. G = clean tones. |
| 7 | R2H16-PTC-2  | pitchdisc  | SAME  | Subharmonic toneB: strong f/2 partial (amp 1.0 vs f0 0.8) perturbs the zero-crossing count phase-dependently. G = clean tones. |
| 8 | R2H16-TMB-1  | timbredisc | class | Formant boost: harmonics k>=4 x3.0 (spectral-envelope shift the centroid formation feels but the (p2,p3) challenge ratios don't). Truth = template class of the unboosted base profile. |
| 9 | R2H16-TMB-2  | timbredisc | class | Vibrato: +-3% @6Hz detunes the exact Goertzel resonators (0.5Hz bins). Truth = base class by construction. |
|10 | R2H16-MOT-1  | motiondir  | dir   | Checkerboard drift: 4px-period checkerboard at 2px/frame; the t->t+2 block-match sees period-ambiguous SAD. G = high-contrast windowed drift (challenge's own clean format). |

## Novelty vs the enumerated R2A 16

- COL-1: gain corruption is new (R2A-COL-2 was illuminant change; COL-3 gray-trap).
- CCN-1: local patch edit is new (R2A-CCN families were illuminant/crop shifts).
- CCN-2: cross-crop collision is new (pairwise search, not a transform).
- SHP-1: hollow/outline is new (R2A-SHP were noise/occlusion/thickness).
- SHP-2: dual-shape distractor is new.
- PTC-1: overmodulated AM is new (R2A-PTC were FM/vibrato/noise).
- PTC-2: subharmonic partial is new.
- TMB-1: formant boost is new (R2A-TMB were noise/harmonic-drop).
- TMB-2: vibrato detune is new.
- MOT-1: periodic-texture drift is new (R2A-MOT were noise/occlusion/speed).

All reuse the frozen R2-7 per-task renderers (`gen_r2a.py`) for byte-exact
F/G span formats; only the adversarial manipulation is new. Family IDs
10-19 (fresh; no collision with R2A 0-9).

## Outputs

- `fixtures_holdout/r2h16_<FAMTAG>_<i>.r2fx` (10,000) + `.truth` (not committed)
- `fixtures_holdout/gen_ledger.jsonl` (id/task/family/truth/sha256)
- `fixtures_holdout/MANIFEST.sha256`
- `evidence/b_holdout.list` (10,000 paths, family-major order)

Note (2026-09-23): the first generation attempt used per-task filenames
(`r2h16_<task>_<i>`), so the two families sharing a task overwrote each
other (6000 files for 10000 ledger entries). Caught by file count before
any run; directory wiped and regenerated with per-family filenames.
No runs were scored on the broken set.
