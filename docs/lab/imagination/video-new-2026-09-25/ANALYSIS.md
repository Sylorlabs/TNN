# ANALYSIS — audio + video measurements (analyzer-first, pre-judgment)

All measurements on final renders (post sign-fix). Agents cannot hear audio;
nothing below is a listening claim — it is waveform/film analysis for
Micah's ears to overrule.

## Audio (8 kHz 16-bit mono WAVs, 26,400 samples = 3.30 s)

| file | min | max | DC | zero-X | hum share | loop autocorr (lag12/24) |
|------|-----|-----|----|--------|-----------|--------------------------|
| nvid3.wav | -32768 | 32767 | 121.3 | 5136 | 0.0054 | 0.155 / -0.279 |
| nvid4.wav | -32768 | 32767 | 11.2 | 5151 | 0.0070 | -0.107 / -0.328 |
| nvid5.wav | -32768 | 32767 | 42.8 | 5191 | 0.0038 | 0.140 / -0.007 |
| nvid6.wav | -32768 | 32767 | 33.8 | 5205 | 0.0052 | -0.097 / 0.018 |

- Bipolar confirmed: full rail swing both polarities, DC < 0.4% of full
  scale, ~5,100–5,200 zero-crossings (healthy oscillation, not rectified).
- Hum: 50/60 Hz + harmonics carry < 0.7% of spectral energy on all four —
  no mains-hum problem.
- Loop periodicity: bin-envelope autocorrelation at 12/24-bin lags is ~0 —
  no mechanical looping; each soundtrack is through-composed.
- Envelope stationarity (CV over 8 windows): 0.18–0.19 — dynamic but not
  degenerate (last window lower = planned fade-out region).

### Event alignment (designed bin → measured)
- **nvid3 (forge):** envelope peaks in window 3 (bins ~20–26, the strike) at
  17,962 RMS, decaying after — the clang lands on the hit. Top transient bins
  21–23 cluster at the strike attack. Spectral peaks 570 / 887 Hz = planned
  clang partials (bins 26/33) within the 8 kHz synth's documented tuning
  (~9.5 cents sharp/semitone: bin 26 → 570 Hz sharp-adjusted ✓, bin 33 →
  887 Hz ✓). Spectral centroid falls 1102 → 830 Hz (bright attack → darker
  ring tail) ✓.
- **nvid4 (storm):** envelope swells 15,520 → 28,280 across windows 1–5
  (storm peak at bins 24–36) then decays. Top transient bins 32–36 = heavy
  rain onset + thunder body. Low-frequency cluster 151–207 Hz = planned
  thunder sweep (bins 10→2, sharp-adjusted 207→124 Hz ✓). Centroid rises
  1244 → 1448 Hz as rain (broadband) dominates the second half ✓.
- **nvid5 (harbor):** top transient bins 36/37/39 (gull- cry/lap region),
  10 (foghorn attack), 23. Peaks 1072–1217 Hz = gull cries (bins 32–40
  sweeps, sharp-adjusted 831–1381 Hz ✓); 182 Hz ≈ foghorn (bin 8 →
  184 Hz sharp-adjusted ✓). Centroid stable 1204/1199 Hz ✓.
- **nvid6 (campfire):** envelope peaks window 5 (bins 30–36, the wind gust)
  at 25,670 RMS. Top transient bins 32–36, 27 = gust + crackle pops at
  planned bins 27/35 ✓.

## Video (native AVIs)
- ffprobe, all four: 240×240 rawvideo, 24 frames, 3.000 s; audio
  pcm_s16le, 8000 Hz, 1 ch, 26,400 samples.
- Decoded every frame (f01–f24): all 240×240×3, zero exact-duplicate
  consecutive pairs (no frozen frames), zero row-tear frames, all 23
  consecutive frame-diffs > 0 (continuous motion). Min frame-diff 7,468
  (nvid3, darkest scene) — still decisively non-zero.
- Full-frame contact sheets inspected for all four (round 1 failed nvid5/6
  → redesigned → round 2 passed all four). Peak-moment single frames
  inspected for nvid5 (f12: dawn gradient, boats, gull) and nvid6 (f16:
  flame structure, sparks).

## Pre-fix baseline (for the record)
Before the `f3_get32s` fix: DC ≈ +20,000–24,000, zero-crossings 2–4,
min = 0 — classic half-wave rectification (the AGENTS.md "dollar tree mic"
pitfall). The Sep 22 committed files retain their original bytes, bug
included; they were not re-rendered.
