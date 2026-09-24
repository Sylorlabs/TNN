# MEASUREMENT_PLAN_V11 — AUDIO V11 Crew A (DIAGNOSIS)

**Frozen:** 2026-09-23, BEFORE any instrument runs. Committed before measurement.
**Question:** What is the precise acoustic distance between the three V10
renders and real children, in numbers? Ranked hypotheses for the missing
"child" signature, each backed by measurements.

## 1. Files under test (verified SHAs, 2026-09-23)

Real children (CC BY-NC-ND 3.0 — measurements ONLY, never render source,
never committed):
- `consistency_gate/calibration/aporee_kids_play_area_30s.wav` — primary anchor
  SHA-256 `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`
- `consistency_gate/calibration/aporee_kids_play_area.wav` (134 s) — stability reference
  SHA-256 `24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77`
- `consistency_gate/calibration/garry_point_park_30s.wav` — park ambience control
  SHA-256 `61063e66d6b9d1789bdfa21c2235cae0683732f48fbf6c3279267694c3cfa866`

Renders (V10, all 30 s / 44.1 kHz / 16-bit mono):
- `clips/b_alpha_kids_1e_j_v10_artic.wav`
  SHA-256 `57df7aa4015b3cde88615d34aa96ea1ac994845e0613bb96144ac990292ccd41`
- `clips/b_alpha_kids_1e_j_v10_paradd.wav`
  SHA-256 `80af8b57e9ba181d1b3c9d79ad3f8e7a7c86a7569254f7a26a40c69c4ba58d73`
- `clips/b_alpha_kids_1e_j_v10_specstat.wav`
  SHA-256 `05988a5ab88fcdeb6b6b5fc2c82a0cae7a5010bd9370bb9f031c9194b4c54c2e`

Renderer sources already read (formant/F0 tables extracted for the report):
- `src/render_v10_artic.zag`: base F0 270/300/340/420 Hz; formants per voice
  F1 644–875, F2 1656–2250, F3 2576–3500, F4 3680–5000 Hz (at default mouth),
  bandwidths 90–205 Hz. → i.e. child-range F0 with ADULT-MALE-sized formants
  (child /a/ 4–7 y: F1 ~1100–1300, F2 ~1700–2200, F3 ~3700+).
- `src/render_v10_paradd.zag`: 3 voice channels, sine-LUT + 4 harmonic partials,
  F0 280–520 Hz — NO formant resonators at all (flat-ish harmonic spectra);
  laughter = bandpass 800–1800 Hz noise; aspiration LP ~1.8 kHz.
- `src/render_v10_specstat.zag`: 12-band resonator bank (180–8360 Hz) driven by
  ONE continuous noise excitation; per-band energies from real-recording
  statistics — NO glottal source, NO voicing by construction.

## 2. Instrument: diag.zag (pure Zag, zero RNG, deterministic)

Single binary, `diag <mode> <clip.wav>`, compiled with the pinned znc
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` from
`aud/b_alpha/` (imports `src/common_v5.zag` for `file_read`/`wav_parse`/
`get16s`; WAV IO pattern copied from `consistency_gate/src/gate.zag`).
All floats f64; all aggregates integer-exact; two runs per (mode,file) must
be byte-identical (`cmp` on stdout) before any number is trusted.

Shared front-end: 16-bit mono PCM via `wav_parse`; analysis frames hop
10 ms (441 samples). Voiced-frame gate (used by lpc/voice/laugh/pros):
30 ms frame, ×4 decimation (→11025 Hz, 331 samples), normalized
autocorrelation lags 14–184 (60–787 Hz), parabolic interpolation of the
peak; VOICED iff peak ≥ 0.45 AND frame RMS ≥ −55 dBFS. F0 = 11025/lag.

Modes (each prints `M <name> <value>` lines + `DIAG-END`):

1. **f0** — F0 distribution over voiced frames: count, voiced fraction,
   median/p10/p90 (10 Hz histogram bins, 0–1000 Hz), excursion p90−p10 in
   semitones, HNR = 10·log10(r/(1−r)) from the autocorr peak (median).
2. **lpc** — Formants on voiced frames: 25 ms frame, pre-emphasis 0.97,
   Hamming, LPC order 14 (Levinson-Durbin), |1/A(e^jw)|² on a 128-point
   grid 0–8000 Hz (cos/sin recurrence per grid point, no per-k trig),
   local-maximum peak picking with ≥6 dB prominence, −3 dB bandwidths by
   linear interpolation. Reports: voiced frames, frames with ≥3 formants,
   median/p25/p75 of F1–F4 (25 Hz bins), median bandwidths B1–B4
   (10 Hz bins). Frames with <3 peaks are excluded and counted.
3. **voice** — Breathiness on voiced frames: H1–H2 via Goertzel at F0/2F0
   (median dB); spectral tilt = E(4–8 kHz)/E(0.2–1 kHz) in dB (median);
   HNR median (same estimator as f0 mode).
4. **ltas** — Long-term average spectrum: 24 log-spaced Goertzel bands
   100 Hz–8 kHz per 1 s window; accumulated over ALL windows and over
   windows with ≥50% voiced frames; each normalized to 0 dB max; printed
   as two 24-value CSV lines.
5. **laugh** — Laugh-syllable structure: 20 ms RMS envelope (10 ms hop);
   bursts = contiguous ≥ −30 dBFS runs of 60–500 ms (gaps <60 ms merged);
   episodes = bursts with <1.2 s gaps. Reports: n bursts, n episodes,
   mean burst dur, mean within-episode gap, syllabic rate (bursts/s in
   episodes), mean per-burst F0 start→mid→end (semitones vs burst start),
   mean burst F0 range (semitones). ARTIC/PARADD detections cross-checked
   against `src/events_v10_{artic,paradd}.txt` laugh-syllable onsets
   (Python glue: count + rate only — detection itself stays in Zag).
6. **pros** — Prosody: syllable rate = envelope peaks (10 ms RMS,
   ≥120 ms separation, ≥3 dB prominence) per second; pitch excursion =
   p90−p10 of the F0 histogram in semitones; pauses = fraction of 50 ms
   frames < −50 dBFS, pause-segment count and mean duration.

## 3. Run matrix

All 6 modes × 6 files, ×2 runs byte-identical:
aporee_30s, garry_30s, artic, paradd, specstat → full matrix.
aporee_134s → f0, lpc, ltas only (stability reference for the headline
dimensions; 4.5× the samples).
Total 72 + 6 = 78 runs. Results in `~/workspace/aud_v11/diag/results/`
(not committed — numbers live in DIAGNOSIS_V11.md).

## 4. Analysis (Python glue only — counting, table formatting, plotting)

- Table: real-30s (primary) vs artic/paradd/specstat per dimension;
  garry_30s as control; aporee_134s as stability check.
- Acoustic distance per dimension: |median_render − median_real| in
  native units + ratio where meaningful (formant ratios vs child
  1.6–2.0× adult-male scaling law).
- Laughter cross-check: detected burst rate vs events-file syllable
  onsets for ARTIC/PARADD.
- Ranked hypotheses H1..Hn, each citing the measurements that back it.
  No hypothesis without a number.

## 5. Deliverable

`DIAGNOSIS_V11.md`: the full real-vs-render table, per-dimension acoustic
distances, ranked missing-signature hypotheses with backing numbers, exact
anchor/render paths + SHAs, instrument build/run log (byte-identical
proofs), and explicit notes on what the instruments CANNOT measure
(listening gaps for fork crews).

## 6. Commit plan (two commits, branch tnn-native-lab ONLY)

1. This file → `imagination_discovery/aud/b_alpha/MEASUREMENT_PLAN_V11.md`
   (commit BEFORE any instrument runs).
2. `imagination_discovery/aud/b_alpha/v11_diag/diag.zag` (instrument source)
   + `imagination_discovery/aud/b_alpha/DIAGNOSIS_V11.md`.
Never committed: binaries, .zagd caches, .zag-cache/, anchor WAV/MP3 files,
results/ scratch.
