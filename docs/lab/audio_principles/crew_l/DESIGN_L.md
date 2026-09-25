# CREW L — CLOSED LOOP: design doc (FROZEN with first commit)

## Question
Can TNN take its own rendered output as input, detect deviation from intent,
and correct it — natively in Zag?

## Architecture

```
intent (pitch:440 env:rise)
   │  open-loop planner (coarse: semitone-grid quantization — documented below)
   ▼
render0.wav ──► [INPUT ORGAN: WAV ingest → measure F0, env] ──► deviation
   ▲                                                              │
   │                    re-plan (deadbeat proportional)           ▼
   └────────────────────── re-render ◄────────────────────── correction
   ... up to 3 correction iterations (4 renders: iter0..iter3)
```

All four boxes (planner, renderer, organ, corrector) are pure Zag in ONE
binary (`loop`). The organ reads the render file from disk through the full
WAV-ingest path (byte-identical file). No Python in the decision path.
Python only scores frozen criteria afterward (ERR via frozen scorer_l.py).

## Why a coarse open-loop planner (honest, not gaming)

A feedback loop is only testable if there is a real, sensor-visible residual
to close. Rendering iteration-0 at best-effort exact frequency would put
ERR(0) at the measurement noise floor, where no feedback law driven by a
noisy sensor can reduce it (it would amplify noise — correctly failing the
battery). The open-loop planner therefore quantizes the target F0 to the
nearest **semitone-grid frequency** (MIDI 40..87, i.e. 82.41..1174.66 Hz,
computed at runtime as 440×2^(k/12), ties → lower k). This models the real
architectural situation the loop exists to fix (cf. B-F1: coarse feedforward
planning leaves a systematic residual; the loop's job is to close it).

- The grid is a frozen design constant, not a target table (targets are the
  sealed 20-case held-out list; dev targets disjoint).
- The residual is REAL: scorer-measured ERR(0) ≈ |quantization error| ∈
  [1.0%, 2.9%] by target selection (see manifest).
- The correction is REAL: driven entirely by the organ's native measurement
  of the render file. The planner never sees the scorer.

## Input organ (prereg §3)

- Ingest: RIFF/WAV parser, 16-bit PCM mono 44100 Hz, header-validated, samples
  as i64 in a `[]i64` table (`(p[0..N*8]) as []i64` idiom — verified
  non-aliasing on this toolchain 2026-09-25; NEVER `as []i32/u32/u16`).
- Framing: 2048-sample Hann (Q8 fixed, matches np.hanning), hop 1024 — same
  grid as the frozen Round-2 analyzer.
- RMS: per-frame integer (Newton isqrt), linear.
- F0: direct time-domain normalized autocorrelation, lags 36..551
  (= int(44100/1200)..int(44100/1200), same as frozen analyzer), first-max
  wins, parabolic interpolation with the frozen formula
  shift = 0.5·(a−c)/(a−2b+c) when interior; VOICED iff r ≥ 0.40 and
  rms > 104 (≈ −50 dBFS, no log needed: 32768·10^(−2.5) = 103.6).
  File F0 = median over voiced frames (lower-middle, deterministic).
- ZCR: per-frame sign-change count, mean.
- Bands: naive DFT N=512 on full-rate 512-sample sub-frames (every 8th frame
  for CLI; precomputed Q30 twiddle table), 4 bands 0–2k / 2–4k / 4–8k /
  8–16 kHz. DEVIATION from prereg recommendation (decimate-by-4): decimation
  to 11.025 kHz cannot reach 8–16 kHz, and the HF band is needed for the G4c
  bearing. Documented here.
- Onsets: frame-RMS derivative threshold → onset times + count.
- Env class: thirds mean-RMS ratio ≥ 2.0 → rise (E3≥2·E1) / decay
  (E1≥2·E3) / flat; silence guard (max(E1,E3) < 200 → flat). Same definition
  in the frozen scorer (public measurement definition, §3.4-compliant).

## Render path

2 s, 44100 Hz, 16-bit mono. Cosine oscillator with phase accumulation,
amplitude 16384 (0.5), envelope flat / linear rise 0.05→0.9 / linear decay
0.9→0.05, 5 ms raised-cosine edge fades. `shape_boost` (env correction)
halves the quiet end per step. HF variant: adds fhf sine at gain g.

## Correction law (deadbeat proportional, gain 1.0)

Per iteration k≥1, natively:
- `(meas_mhz, meas_env) = organ(iter{k-1}.wav)` (bands off for pitch loop)
- `dev_mhz = target_mhz − meas_mhz`; `f_render += dev_mhz`
- if `meas_env ≠ target_env`: `shape_boost += 1`
- render → `iter{k}.wav`

Sign convention (for the §2.3(c) sign-agreement audit): deviation_d =
target − measured (the error to close); correction_c = f_{k+1} − f_k (applied
change). Deadbeat ⇒ c = d ⇒ agreement 100% by construction on
|dev|>1% cases — the directionality the prereg asks for, with the ERR
reduction and Wilcoxon carrying the evidential weight.

Exactly 3 correction iterations per case (within "up to 3"), no early stop.

## Binaries (all from src/core.zag + main_*.zag, concatenated; pinned znc)

- `organ`: `organ measure <wav>` → `f0_mhz=… voiced=…/… env=… rms=… zcr=…
  b0r=… b1r=… b2r=… b3r=… onsets=…` (all integers; b*r = band ratio ×1e6)
- `render`: `render pitch:<hz> env:<flat|rise|decay> <out.wav>`
  (+ `hf:<fhz>:<gain_milli>` optional) — standalone; used for dev renders.
- `loop`: `loop <case_id> pitch:<hz> env:<class> <outdir>` → 4 renders +
  per-iteration measurement/correction lines.
- `hfloop`: `hfloop <case_id> <fhf_hz> <g0_milli> <outdir>` → HF-reduction
  variant (diagnostic): render 440 Hz + fhf sine, natively measure 8–16 kHz
  ratio, attenuate g ← g·sqrt(1e-4/ratio), re-render, 3 iterations.

## Frozen scorer (frozen/scorer_l.py, committed in first commit, never changed)

- F0: 2048 Hann / hop 1024, mean-remove, FFT autocorr, lags 36..551,
  parabolic interp (frozen formula), voiced r≥0.40 & rms>−50 dBFS, median
  (lower-middle) over voiced frames.
- Env: thirds mean-RMS ratio ≥ 2.0 (same def as organ).
- ERR(k) = |F0_scorer − F0_target|/F0_target + 0.5·[env_scorer ≠ env_target].

## Test material (first commit seals; generated after)

- `ref_wavs/`: 10 Python-generated deterministic reference WAVs (varied F0,
  envs, vibrato/two-tone/noise/tremolo) — organ self-check (§3.5).
- `manifests/intent_manifest.json`: 20 held-out cases — integer-Hz targets in
  [90, 1175] with semitone-quantization error ∈ [1.0%, 2.9%], env cycling
  flat/rise/decay; per-case planner iter0 frequency recorded for audit.
- Dev renders (440 flat / 220 rise / 880 decay) — disjoint; SHAs in
  dev_manifest.json. Build tuning uses dev only.

## Statistics (h/h_score.py)

- (a) mean_k ERR(3)/ERR(0) ≤ 0.80
- (b) Wilcoxon signed-rank, one-sided ERR(3)<ERR(0), α=0.01 (exact)
- (c) ≥16/20 strictly improve; SHA(iter3)≠SHA(iter0) ∀cases; sign agreement
  ≥80% on |dev|>1% cases (convention above)
- L-R1: per-iteration error curve; LOOP-UNSTABLE flag on sawtooth
- Dither spot check (§5.3): 20 iter0 renders ×1.001 gain → organ re-measure;
  stable = same env AND ΔF0 ≤ 0.5%; need ≥19/20.

## Zero-RNG / determinism

No RNG anywhere. Ties → lowest index. 3× full-battery reruns, byte-identical
SHAs required. znc constraints honored: []i64/[]u8 tables only, no slice >
2^25 B, argc ignored, `_zag_arg` non-owned, no `};`, no `.*` on non-pointers,
≤4-deep else nesting, no bare blocks, no identifier `try`.
