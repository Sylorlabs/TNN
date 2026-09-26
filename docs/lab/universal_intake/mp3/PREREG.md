# MP3 Layer III — Preregistration (frozen 2026-09-26)

Decoder-completion fork for the universal-format intake order (Micah, 2026-09-26).
This document is written BEFORE any decoder implementation. It fixes the batch
contracts, fixtures, numeric rules, tolerances, and kill bars. If any batch
fails its kill bar, work STOPS and the batch is reported as the scoped blocker.
Bars are never silently lowered.

## 1. Scope

- Format: MPEG-1 Layer III (MP3), 44.1 kHz, mono and stereo.
- Stereo modes exercised: plain, Mid/Side, intensity stereo (as produced by the
  fixtures below).
- Block types exercised: long, short, mixed (as produced by the fixtures).
- OUT OF SCOPE (decoder may parse but verdict does not cover): MPEG-2/2.5,
  CRC-protected frames, free format, multilingual extensions. The final verdict
  row must state this scope explicitly and must not overclaim.

## 2. Fixtures (sealed, committed)

Source: `docs/lab/universal_intake/fixtures/t_pcm16.wav`
(1.50 s, mono, 44.1 kHz, s16 — the committed universal fixture).

Generated 2026-09-26 with ffmpeg 8.1.2 (`ffmpeg version 8.1.2 Copyright (c)
2000-2026 the FFmpeg developers`, libmp3lame), zero RNG involved
(libmp3lame is deterministic for fixed settings):

| File | Command | SHA-256 |
|---|---|---|
| `mp3/fixtures/t_128cbr.mp3` | `ffmpeg -i t_pcm16.wav -codec:a libmp3lame -b:a 128k -ac 1 -ar 44100` | `a08aaf14234683dcdc7ac6dffe3d48b4bedf2426d1b6f96804e60c57bf34d9eb` |
| `mp3/fixtures/t_vbr.mp3` | `ffmpeg -i t_pcm16.wav -codec:a libmp3lame -q:a 4 -ac 1 -ar 44100` | `236a113b94c7ed6187d62811a12d5d1bee2e0d73f5264b086a7c535a49b5b101` |
| `mp3/fixtures/t_128js.mp3` | `ffmpeg -i t_pcm16.wav -codec:a libmp3lame -b:a 128k -ac 2 -ar 44100` (joint stereo) | `445663e6112eff476cc5762f9c842aa2b1b47808d65b8285abaff37d4608fbae` |

Reference PCM (NOT committed; regenerable): each fixture decoded with
`ffmpeg -i <f>.mp3 -f s16le -acodec pcm_s16le`, 2026-09-26:
- t_128cbr → 66150 samples, sha256 `6698d2a5b744f2f24142c51b82c0f87f454723a25e6329d752213a838d030820`
- t_vbr    → 66150 samples, sha256 `b79694a0563373eacb043e8f0db4cd1f457e0b3f6b3f6f91f82fb9ba76035243`
- t_128js  → 132300 samples (stereo), sha256 `855e7dc5e9d97d72644038bd262dc2fd7d35baec3fce85d32223321291def864`

## 3. Numeric representation (preregistered)

- The Zag implementation uses IEEE-754 **f64** (double) for ALL signal values.
  Rationale: znc supports f64 reliably (proven in `wav.zag`); f32 literals have
  limited magnitude in znc; f64 rounding (~1e-16) is ~300 dB below full scale,
  far below any audibility or tolerance bar.
- All constant tables (Huffman tables are integers; pow43, windows, twiddles,
  antialias coefficients, synthesis window) are stored as f64, converted from
  the published dr_mp3 (public-domain, minimp3-derived) f32 values by EXACT
  f32→f64 widening (lossless). Table values are extracted programmatically
  from the fetched dr_mp3.h (sha256
  `997b7ee18de6e6b81e2a83f1ea9fc62aef25c62b28d48d95635f49e65de0a2f`),
  never hand-transcribed.
- Bitstream/integer logic (side info, Huffman symbols, scalefactor indices)
  uses i64/u8 integer arithmetic only.
- PCM output: s16, rounded "away from zero … to be compliant" per dr_mp3's
  `drmp3d_scale_pcm` (clamp at ±32766.5/32767.5, `(int)(x+0.5)`, subtract 1 if
  negative), then clamped to [-32768, 32767].
- Zero RNG. Pure Zag. Deterministic: two runs per fixture must be
  byte-identical (SHA-256 compared).

## 4. Reference independence

- The Python reference (`mp3/ref/mp3ref.py`) is an independent from-scratch
  port of the published dr_mp3 Layer III algorithm (public domain) to
  Python/numpy float64. It is written separately from the Zag code; the two
  share only table values and the published algorithm.
- B1 additionally cross-checks the integer Huffman symbol stream, which is
  pure integer logic with no float involvement.

## 5. Batch contracts and kill bars

### B1 — side info + scalefactors + Huffman decode
Input: fixture MP3 bytes.
Output per granule/channel:
  (a) integer Huffman symbol stream: big_values (x, y, sign) pairs and
      count1 (v, w, x, y, signs) quadruples, in decode order;
  (b) dequantized f64 spectral values (576 per channel) after Huffman;
  (c) all side-info fields and scalefactor values.
Kill bar: (a), (b) (as f64 bit patterns), and (c) must match the Python
reference BIT-EXACTLY on all three fixtures, every frame, every granule,
every channel. Any mismatch → STOP, B1 is the scoped blocker.

### B2 — reorder + stereo (MS / intensity)
Input: B1 spectral values.
Output: spectral values after stereo processing and short-block reorder,
in subband order (576 per channel).
Kill bar: max absolute difference vs Python reference ≤ 1e-9 on all
fixtures/frames/granules/channels. Any excess → STOP, B2 is the scoped blocker.

### B3 — alias reduction + IMDCT (+ sign flip)
Input: B2 spectral values.
Output: 576 time-domain subband samples per channel per granule
(after antialias, IMDCT36/IMDCT12, overlap-add, change_sign).
Kill bar: max absolute difference vs Python reference ≤ 1e-6 on all
fixtures/frames/granules/channels. (IMDCT accumulates ~100 f64 ops/value;
1e-6 is ~1e10× the f64 rounding floor — generous but still 300× below
1-LSB audibility.) Any excess → STOP, B3 is the scoped blocker.

### B4 — polyphase synthesis + PCM output
Input: B3 subband samples.
Output: s16 PCM for the whole file (all frames, all granules).
Method: align Zag output to ffmpeg's s16 reference by cross-correlation over
±4096 samples (accounts for encoder-delay trimming differences), then compare
the overlapping region.
Kill bar (preregistered, not fit to data): max abs diff ≤ 8 LSB,
mean abs diff ≤ 1.0 LSB, on all three fixtures. (Two correct float decoders
typically agree within ±2; 8/1.0 is conservative headroom for ffmpeg's
internal float path.) Any excess → STOP, B4 is the scoped blocker.

### Determinism gate (all batches)
Each fixture decoded twice; SHA-256 of both runs must be byte-identical.
Failure → STOP, report as blocker.

## 6. Algorithm reference (what is being ported)

Pure-Zag scalar port of the dr_mp3/minimp3 Layer III core:
side-info parse → bit-reservoir restore → per granule/channel:
scalefactor decode → Huffman + dequant (pow43 × scalefactor gain) →
intensity/MS stereo → short-block reorder → alias reduction →
IMDCT (36/12) with overlap → sign flip → 32-point DCT-II →
polyphase synthesis (240-tap window, integer-coefficient pairs) →
s16 scaling. Frame loop with reservoir save/restore across frames.

## 7. Commit hygiene

- Commit ONLY: `mp3/PREREG.md`, `mp3/fixtures/*.mp3`, `src/mp3.zag` (new),
  `mp3/ref/*` (Python reference + table extractor), `mp3/RUNLOG.md`,
  `mp3/EVIDENCE.md`, updated `VERDICT.md` MP3 row, updated `MANIFEST.sha256`.
- NEVER commit: binaries, `.zagd`, `.zag-cache`, derived PCM, `/tmp` outputs.
- Branch `tnn-native-lab` only. Never main.

## 8. Verdict update rule

The MP3 row in `VERDICT.md` moves from ⚠️ HEADER ONLY to ✅ FULL DECODE
only if B1–B4 all pass on all three fixtures plus the determinism gate.
Anything less → the row names the failed batch as the scoped blocker.
