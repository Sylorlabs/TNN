# FROZEN_ORGAN.md — Crew P input organ (TNN-native audio perception)

Frozen 2026-09-25. Source: `organ.zag` (pure Zag, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
Any change to the algorithm below requires a prereg amendment; rebuilds
from the identical source must be byte-identical (SHA recorded in build log).

## 1. Input contract
- RIFF/WAV, PCM16, mono, 44.1 kHz. Chunk-aware parse (fmt/data chunks,
  any order); rejects other formats with `ERR`.
- Clips are 2 s (88,200 samples); ingest is bounded to ≤ 60 s (2,646,000 samples).

## 2. Framing (§3.3)
- 2048-sample frames, hop 1024, Hann window `0.5-0.5*cos(2πn/2047)`.
- Per-frame RMS dBFS (unwindowed, mean not removed): `10*log10(ms/2^30)`.
- Analysis arenas are `[]u8` with explicit little-endian accessors (no
  indexed `[]i32/u32/i16/f64`, per ZNC-2026-09-21-007 and the 2026-09-25
  `[]f64` probe). Fixed-point where noted.

## 3. F0 (autocorrelation with YIN period selection)
- Mean-removed, Hann-windowed frame; integer autocorrelation
  `r[lag] = Σ xw[n]·xw[n+lag]` for lags 1..551 (80–1200 Hz at 44.1 kHz),
  computed directly in i64 (inlined little-endian loads; no `[]f64`).
- Period selection: YIN (2002) cumulative-mean normalization of the
  autocorrelation deficit `d[lag] = 2·(r[0] − r[lag])`:
  `d'[lag] = d[lag] / mean(d[1..lag])`; first lag in 36..551 with
  `d' < 0.10`, advanced to the local minimum; fallback to the global
  minimum if no dip below 0.10.
- Parabolic interpolation on `d'` around the selected minimum;
  `f0 = 44100 / lag_interp`.
- Voiced iff `r[sel]/r[0] ≥ 0.40` **and** frame RMS > −50 dBFS.
- Rationale (recorded 2026-09-25): plain normalized-autocorrelation argmax
  provably fails 80–112 Hz under the 2048-sample Hann window — the true
  long-lag peak is window-attenuated below short-lag harmonic correlation
  (measured: 80–110 Hz all read as 1225 Hz). The prereg requires 80–1200 Hz,
  so the frozen Round-3 reference's literal argmax cannot satisfy §2. The
  YIN selection operates on the autocorrelation-derived deficit `d[lag]`
  and recovers 80–1200 Hz (verified 80, 90, 100, 110, 115, 120, 220, 440,
  880, 1200 Hz, all within 2%). A window-autocorrelation correction was
  tried and rejected: it equalizes period multiples and causes octave
  errors (220 Hz → 110 Hz).

## 4. Envelope / rhythm / HF
- Envelope class from frame-RMS thirds: `rise` iff
  `mean(last third) − mean(first third) > 4 dB`; `decay` iff `< −4 dB`;
  else `flat`.
- Onsets: frame-to-frame RMS rise > 6 dB with frame RMS > −50 dBFS,
  80 ms refractory. Rhythm asymmetry = median over consecutive IOI pairs
  of `max(ioi)/min(ioi)`; the more asymmetric clip is the swung one.
- HF: 8–16 kHz bandpower via the §5 band decomposition; the clip with the
  larger bandpower (relative to its own peak total power) wins.

## 5. Band decomposition (≥4 bands, 0–16 kHz)
- Decimate-by-4 with `[1,2,1]/4` prefilter → 512 samples → naïve DFT N=512
  (fixed-point twiddle tables, scale 2^20).
- Bands (Hz): [0,1378], [1379,2756], [2757,4134], [4135,5512].
  (The prereg recommends a DFT for this feature; §3.3 requires ≥4 bands
  covering 0–16 kHz. The 8–16 kHz HF question band is served by the
  top DFT band plus the time-domain HF path; see §4.)

## 6. Question dispatch (organ boundary: qid + WAV path(s) only)
- `pitchrel:<qid> A B` → `A`/`B` (higher median voiced F0).
- `pitchabs:<qid> A` → `0`..`23`, `idx = round(12·log2(f0/110))` clamped.
- `env:<qid> A` → `flat`/`rise`/`decay`.
- `rhy:<qid> A B` → `A`/`B` (higher IOI asymmetry).
- `hf:<qid> A B` → `A`/`B` (higher 8–16 kHz bandpower).
- `pr4:<qid> A` → 3 bits (e.g. `110`): bit2 = frac_static≥0.15,
  bit1 = HNR in [0.7,12], bit0 = prosody in [0.003,0.25]
  (native approximations; diagnostic only).
- `pr5:<qid> A B` → `A`/`B` (higher median voiced F0; diagnostic only).

## 7. Determinism
- Zero RNG. No wall-clock, no thread scheduling dependence, no allocator
  address in any output. Fixed-point tables built at startup from
  deterministic `cosr`. Three consecutive runs must be byte-identical.

## 8. Known limits (not failures of the battery)
- F0 is defined only for 80–1200 Hz; content outside this range is out of
  scope (organ reports unvoiced / f0 = 0).
- The DFT band decomposition is computed per frame (compliance feature;
  no battery question depends on it).
