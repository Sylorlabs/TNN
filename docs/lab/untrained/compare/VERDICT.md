# VERDICT — Workstream B: Untrained Structural Analysis of Novel Inputs

Date: 2026-09-26. Analyzer: `tnn/uanalyze.zag` (pure Zag, zero RNG, deterministic).
Human descriptions sealed 2026-09-26 17:27 UTC, BEFORE any TNN run on novel inputs.
Analyzer source frozen AFTER final bugfix (SHA in `tnn/FROZEN_SHA256.txt`).
Every input run TWICE; all outputs byte-identical across runs.

## Inputs (all novel; novelty audit in §5)

| ID | Source | Analyzed form | Duration/size |
|----|--------|---------------|---------------|
| A1 | archive.org `ThunderStorm_943` (30 s excerpt @422 s) | 16 kHz mono WAV | 30.0 s |
| A2 | archive.org "133 Authentic Sound Effects" (bell buoy) | 16 kHz mono WAV | 55.8 s |
| A3 | archive.org "133 Authentic Sound Effects" (crickets) | 16 kHz mono WAV | 43.2 s |
| I1 | Wikimedia Commons "Ice Crystals on Window Pane" | 480x320 PPM | 5472x3648 orig |
| I2 | Wikimedia Commons "Longsheng Rice Terraces November 2017 021" | 480x343 PPM | 5600x4000 orig |
| V1 | Wikimedia Commons "Ocean surface waves 09.ogv" | 22 PPM frames @2fps | 11.04 s |

## Aggregate result

| Verdict | Count |
|---------|-------|
| MATCH | 10 |
| MISS (withheld / not captured) | 20 |
| WEAK MISS (coarse but not false) | 3 |
| PARTIAL | 3 |
| **HALLUCINATION (false positive)** | **5** |

**The bar FAILS: 5 hallucinations.** Per the order, false positives are worse than
withholding, and any hallucination fails the bar.

## Hallucinations (5)

| # | Input | False claim | Mechanism |
|---|-------|-------------|-----------|
| H1 | A1 thunderstorm | "RHYTHM amplitude repeats on a cycle of about 0.100 seconds" | Envelope autocorr over lags 2-10 picks lag 2 (short-term correlation) on aperiodic thunder; no 10 Hz structure exists. |
| H2 | A2 bell buoy | "RHYTHM amplitude repeats on a cycle of about 0.100 seconds" | Same lag-2 artifact; no 10 Hz AM in the recording. |
| H3 | A3 crickets | "179 distinct transient events" + "tonal bed with irregular transient events over it" | The chirp AM pulses that the (correct) rhythm detector finds at 3.3 Hz are double-counted by the onset detector as a SECOND, separate transient layer. No separate transient layer exists. |
| H4 | I1 frost | "TEXTURE mostly smooth surfaces, little fine detail" | Texture measured on 80x45 downscale; fine dendritic crystal detail averages away into smooth cells. |
| H5 | I2 terraces | "TEXTURE mostly smooth surfaces, little fine detail" | Same downscale cause; terrace detail lost. |

## Per-input summaries

### A1 thunderstorm — 5 MATCH / 1 MISS(+1 weak) / 1 HALLUCINATION
Matched: continuous noise bed, no pitch (correctly withheld), irregular onsets,
large dynamics (dyn_ratio 5379 after min_es fix), burst-over-bed layers (coarse).
Missed: the TWO-burst grouping (102 shredded 20 ms triggers, no grouping);
low-frequency dominance understated (band_low 0.513 vs 0.55 sentence threshold).
Hallucinated: 100 ms rhythm (H1).

### A2 bell buoy — 0 MATCH / 5 MISS / 2 PARTIAL / 1 WEAK MISS / 1 HALLUCINATION
Partially matched: "no glide" (strike-group ~10 s period missed — 0.5 s
env-autocorr maxlag cannot see it). Missed: ~10 s group regularity (IOI
dominated by intra-strike triggers), double-strike structure, high partials to
8 kHz (250 Hz DFT bins too coarse), the water bed, and the true bell/water
layer split (reported "tonal bed with transients" — inverted). "Sustained"
overstates decaying strikes (weak). Hallucinated: 100 ms rhythm (H2).

### A3 crickets — 2 MATCH / 3 MISS / 1 HALLUCINATION
Matched: 3.3 Hz chirp rhythm (human est. ~3-5/s), no glide. Missed: true band
center ~4.4 kHz reported as 2285.7 Hz (method ceiling 4 kHz + subharmonic
aliasing — honest boundary); harmonic traces; fade in/out framing.
Hallucinated: separate transient-event layer (H3) — the layer-separation
boundary: one AM process counted as two layers.

### I1 frost — 1 MATCH / 4 MISS / 1 HALLUCINATION
Matched: no dominant edge orientation. Missed: dendritic branching (no shape
concepts), dark background, monochrome/high contrast (withheld). Hallucinated:
"smooth, little fine detail" (H4) — analysis-scale boundary.

### I2 terraces — 1 MATCH / 4 MISS / 1 HALLUCINATION
Matched: vivid varied color (coarse). Missed: curvature (no curve concepts),
river, buildings, detail. Hallucinated: "smooth" (H5) — same scale boundary.

### V1 waves — 1 MATCH / 3 MISS / 1 PARTIAL / 1 WEAK MISS
Matched: no cuts/one shot; direction withheld (as the human did). Missed: the
static railing bars, the water band, and the actual water motion (block matcher
finds no consistent vectors in churning texture: mean 0.52 px/frame). Weak miss:
"brightens over time" (29.2->32.1) vs human "stable" — numbers support mild rise.

## Honest boundary (where the analyzer cannot go)

1. **Event grouping**: 20 ms onset triggers with no grouping stage — 2 thunder
   bursts become 102 "events"; bell double-strikes invisible.
2. **Layer/source separation**: one AM process (crickets) is split into two
   layers; bell/water split inverted. No source-separation machinery.
3. **Pitch ceiling**: autocorrelation lag floor 4 samples @16 kHz = 4 kHz max;
   content above aliases to subharmonics (A3: 4.4 kHz -> 2285.7 Hz).
4. **Rhythm floor/ceiling**: envelope autocorr spans 0.1-0.5 s only; misses 10 s
   periods, fabricates 0.1 s ones on aperiodic envelopes (H1, H2).
5. **Texture scale**: all texture judgments at 80x45; fine detail (frost
   dendrites, terrace rows) reads as smooth (H4, H5).
6. **No shape/object concepts**: curvature, bars, river, buildings — the
   analyzer has geometry statistics only, and reports none of them.
7. **Motion under chaotic texture**: 16x16 block matching fails on churning
   water; real motion reported as "near-static or chaotic".

## Bugs found and fixed during this work (all before verdict comparison)

1. RIFF parser assumed PCM data at byte 44; ffmpeg WAVs carry a LIST chunk.
   Fix: `find_data_chunk` scans chunk headers. (Would have been a total miss.)
2. `isort_copy` lost elements on early exit (percentiles corrupted).
   Fix: placed-flag insertion sort.
3. `dyn_ratio` min_es=0 poisoned by leading digital-silence window (A1: ratio
   stuck at 1.0). Fix: min over e>0.
4. Pitch octave preference picked autocorr shoulders (440 Hz -> 470 Hz).
   Fix: local-maximum peak picking + half-lag guard. Smoke: 444.4 Hz (1% high,
   integer-lag quantization — honest).
5. Edge-orientation sentence labels were inverted (gradient vs edge direction).
6. Spectral sentences editorialized ("rumbling", "hissy") — reworded to factual
   band statements.

## Novelty audit

- SHA-256 of all six source files: not present as git objects in the repo.
- No filename/source references found in the repo (`git grep`).
- All six downloaded fresh 2026-09-26 from public sources (URLs + hashes in
  `SOURCES.md`). The analyzer has no training step; thresholds were set on
  synthetic fixtures (tone/clicks/split/moving-square) before real inputs were
  inspected. Absolute novelty cannot be proven exhaustively, but no evidence of
  prior contact exists and the measurement pipeline never saw the inputs before
  the sealed runs.

## Determinism

All six inputs run twice with the frozen binary: byte-identical outputs
(6/6). Zero RNG in the analyzer; no wall-clock or address-dependent output.
