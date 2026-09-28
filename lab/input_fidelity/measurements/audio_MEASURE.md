# Audio Input-Fidelity Measurement — MEASURE.md

**Battery:** input_fidelity (frozen prereg 5b661730) · **Modality:** audio · **Worker run:** 2026-09-27 ~01:07–01:30 PDT
**Scope:** committed state ONLY (`origin/tnn-native-lab`). The dirty-worktree MP3 changes (`mp3dec.zag`, `mp3tab64.zag`) were NOT built, run, or measured — recorded as pending per prereg scope.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned). **Fixture SHAs:** all 5 verified against `docs/lab/universal_intake/MANIFEST.sha256` before use — exact match.

## Bar results

### B2 — audio lossless byte-identical (WAV + both FLAC)

| Fixture | Decoder (committed) | Held SHA-256 | Committed claim | Verdict |
|---|---|---|---|---|
| `fixtures/t_pcm16.wav` | `src/wav.zag` | `17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1` | VERDICT.md: `17f57ff5…` | **PASS** |
| `fixtures/t.flac` (16-bit mono) | `src/flac.zag` | `17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1` | evidence: matches WAV SHA | **PASS** |
| `fixtures/t24.flac` (24-bit mono) | `src/flac.zag` | `ece6870f199822d02b777def56b5a20a828b55857df6ec6d407b419002182fc0` | evidence/flac_stereo_2026-09-26.md: `ece6870f…`, 0/66150 vs ffmpeg | **PASS** |

Independent cross-checks vs ffmpeg (not just self-consistency):
- WAV held vs `ffmpeg -f s16le`: **0/66150 samples differ**.
- FLAC-16 held vs ffmpeg: **0/66150 differ**.
- FLAC-24 held vs ffmpeg s32le≫8 (ffmpeg sign-extends 24-bit into the top 24 bits, i.e. value≪8; the held i64 carries the true 24-bit value): **0/66150 differ**.
- Determinism: all three re-run → byte-identical (cmp clean).

**Wording caution (honest, not a gap):** VERDICT.md's summary line reads "FLAC (mono 16/24-bit) → IDENTICAL (16-bit and 24-bit mono)" next to the WAV SHA. Taken literally that would demand `t24.flac`'s held SHA equal the WAV SHA — impossible, because `t24.flac` holds genuinely different 24-bit content (held samples ≈ WAV×256 ± up to 306 in 24-bit units, mean |Δ| 75.6 — real low-byte content, not a shifted copy). The precise per-fixture claim in `evidence/flac_stereo_2026-09-26.md` (`ece6870f…`, 0/66150 vs ffmpeg) reproduces exactly. The decoder is byte-faithful; the summary line is shorthand.

### B4 — MP3 within validated bounds (oracle/ffmpeg LSB)

Committed PCM SHAs from `mp3/zag_full/BUILD.md` reproduced exactly:
- `t_128cbr.mp3` → `f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467` ✔
- `t_128js.mp3` → `711f0f067397f1439f62f18275b88e0e25df86875936e11f27be0d65318209b0` ✔
- Determinism: both re-run → byte-identical.

| Fixture | vs committed oracle `mp3/ref/mp3ref.py` | Committed claim | vs ffmpeg | Committed claim | Gate |
|---|---|---|---|---|---|
| t_128cbr (mono) | max **1.0** LSB, mean **1.45e-04** LSB | RUNLOG: max 1.0, mean 0.00014 | — | EVIDENCE table: 1.0 / 0.0195 | **PASS** |
| t_128js (JS stereo) | max **1.0** LSB, mean **7.23e-05** LSB | RUNLOG/EVIDENCE: max 1.0, mean 7.2e-05 | max **1.0** @lag 2257, mean **0.00449** | RUNLOG: max 1.0, mean 0.0045 | **PASS** |

Gate (frozen PREREG B4): max ≤ 8 LSB, mean ≤ 1.0 LSB — passing with ~8× headroom on max.

**Internal inconsistency flagged (committed records disagree):** `mp3/EVIDENCE.md`'s stereo-fix summary table lists t_128cbr as "0 (byte-identical)" vs oracle, but the same file's RUNLOG section records "max 1.0 LSB, mean 0.00014 LSB". My re-run of the committed decoder vs the committed oracle gives **max 1.0, mean 1.45e-04** — matching the RUNLOG, not the table. Both are inside the gate; the table's "0" is wrong or mislabeled (it may conflate Zag-vs-Zag determinism with Zag-vs-oracle). Recommend the coordinator correct the table.

## Waveform analysis (input vs held) — measured before any verdict

Method: `waveform_analysis.py` (scratch copy of the `audio_longhorizon/phase3/src/analyze2.py` approach: comb-filter HNR, Hann-windowed power spectra, thirds-RMS/crest/ZCR, per-third centroid drift, FFT autocorrelation loop peak, log-flux transient onsets, 50/60 Hz ×6-harmonic energy). FFT-based autocorrelation (the naive O(n²) correlate was killed after 3.5 min).

### Pair 1 — lossless: input `t_pcm16.wav` vs held (committed `wav.zag`)

Residual: max **0.0** LSB, rms **0.0** LSB. Every metric identical to all printed digits:

| Metric | Input | Held |
|---|---|---|
| f0 (autocorr) | 227.3 Hz | 227.3 Hz |
| HNR | 8.67 dB | 8.67 dB |
| Spectral centroid / 85% rolloff / >16 kHz frac | 19318.2 Hz / 22050 Hz / 0.84887 | identical |
| Thirds RMS | [11584.9, 3656.5, 23377.7] | identical |
| Thirds crest | [1.41, 8.07, 1.4] | identical |
| Thirds ZCR | [0.0906, 0.0, 0.5039] | identical |
| Centroid drift (thirds) | [1504.6, 5015.5→5013.5, 21546.9] Hz | identical |
| Loop periodicity | peak 0.80 @ lag 14 | identical |
| Transients | 1 onset | 1 onset |
| Hum 50/60 Hz (×6 harmonics) | 2e-06 / 3e-06 of energy | identical |

Content note: the fixture is a bright nonstationary test signal — 84.9% of energy above 16 kHz, strongest tonal peak at Nyquist 22050 Hz (43% of energy, a test-signal artifact present in the input itself), envelope swings 3.7k→23k RMS across thirds. Hum negligible. All of it is preserved bit-exactly.

### Pair 2 — MP3: input = ffmpeg reference decode of `t_128js.mp3` (lag-2257 aligned, mono mix) vs held = committed `mp3dec.zag` PCM

Residual: max **1.0** LSB, rms **0.067** LSB.

| Metric | Input (ffmpeg ref) | Held (Zag) |
|---|---|---|
| f0 | 227.3 Hz | 227.3 Hz |
| HNR | 8.66 dB | 8.66 dB |
| Centroid / 85% rolloff / >16 kHz frac | 4053.0 / 6125.3 Hz / 0.000381 | identical |
| Thirds RMS | [7782.4, 2388.4, 2103.2] | identical |
| Thirds crest | [1.47, 10.36, 4.89] | identical |
| Thirds ZCR | [0.0907, 0.2217, 0.0246] | [0.0906, 0.2199, 0.0228] |
| Centroid drift (thirds) | [1504.6, 4145.5, 281.7] Hz | identical |
| Loop periodicity | peak 0.15 @ lag 194 | identical |
| Transients | 3 onsets, IOI CV 0.923 | 3 onsets, CV 0.923 |
| Hum 50/60 Hz (×6) | 1.6e-05 / 1.8e-05 | identical |
| Peak tone | 1818.7 Hz, 1.16% of energy | identical |

The only deltas vs the reference decode are the ±1 LSB quantization flips (10 samples in 138240), which nudge near-zero-crossing counts in the 4th decimal of ZCR. No spectral, envelope, periodicity, transient, or tonal structure is altered. (The 128 kbps encode itself rolls the input's 19.3 kHz centroid to 4.05 kHz — that is the MP3 format's doing, identical in both decodes.)

## Gap mechanisms, ranked by size

1. **MP3 final-quantization rounding — 10 samples/fixture flip by exactly 1 LSB** (max 1.0, mean ~1e-04 LSB). White-box: the Zag f64 DSP chain (IMDCT/synthesis) is bit-exact vs strict IEEE (per the committed port validation); the residual appears only at the final float→s16 step, where the decoder's dr_mp3-compatible away-from-zero rounding and the oracle's `astype('<i2')` conversion disagree at half-LSB boundaries. Sub-contributor: the intensity-stereo pan table stored as f32 bit patterns widened to f64 contributes ~0.001 LSB (documented in EVIDENCE.md, negligible). This is quantization policy, not a decode error; 8× inside the frozen gate.
2. **MP3 encoder delay/padding alignment** — ffmpeg trims to 132300 samples; the Zag decoder emits all 60 frames (138240 samples). Alignment is by cross-correlation (lag 2257, committed). Not a decoder gap; a container-metadata convention.
3. **t24.flac SHA ≠ WAV SHA** — not a gap (see wording caution above): distinct 24-bit content, decoded byte-faithfully vs ffmpeg.

No other gaps found. No repair attempted (measurement only, per task).

## Not measured (honest gaps in coverage)

- `t_vbr.mp3` — committed fixture but NOT in the frozen battery fixture list; out of scope (committed RUNLOG covers it: max 1.0/mean 0.00019 vs oracle).
- `src/raw_pcm.zag` baseline path — not a B2 fixture path; not re-run.
- The dirty-worktree MP3 sources — explicitly out of scope; pending audio-round-3 line owns them.

## Deliverables

- `assets/cmp_lossless_wav.png` — waveform + residual + spectrum + residual-histogram, input vs held, lossless WAV.
- `assets/cmp_mp3_js.png` — same four panels, MP3 joint-stereo (ffmpeg ref vs committed Zag).
- `assets/excerpt_01_input_ffmpeg-ref_t128js.wav` — **INPUT** (ffmpeg reference decode, mono mix, 1.5 s, 16-bit).
- `assets/excerpt_02_held_zag-committed_t128js.wav` — **HELD** (committed `mp3dec.zag` decode, mono mix, lag-aligned to input, 1.5 s, 16-bit).
- (Lossless pair excerpts omitted deliberately: input and held are bit-identical, so there is nothing for ears to compare.)

**Bottom line:** B2 PASS on all three lossless fixtures (SHA claims reproduce; ffmpeg cross-checks 0/66150; deterministic). B4 PASS on both MP3 fixtures (oracle/ffmpeg bounds reproduce to the printed digit; gate passed with headroom). One committed-record inconsistency to fix: EVIDENCE.md's "0 (byte-identical)" vs oracle for t_128cbr contradicts its own RUNLOG (max 1.0) and this re-measurement (max 1.0, mean 1.45e-04).
