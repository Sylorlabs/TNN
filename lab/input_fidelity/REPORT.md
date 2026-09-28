# Input Fidelity Battery — REPORT (2026-09-27)

**Mission** (Micah): measure input faithfulness with real fixtures and show
input-vs-held side by side for his eyes and ears **before** any imagination is
judged. Exact replication is the gate before imagination.

**Prereg:** `docs/lab/input_fidelity/PREREG.md` — frozen and committed FIRST
(commit `5b661730da28fe61e5c9e4477786bfd606639910`, parent on the then-current
origin head). No measurements began before the freeze.

**Method:** committed sources only (`origin/tnn-native-lab`, dirty worktree never
used), pinned toolchain `znc_linux_x86_64_abed8aa1`, sealed fixtures SHA-verified
against `docs/lab/universal_intake/MANIFEST.sha256` before every run, pure Zag /
zero RNG, every intake re-run twice for byte-identical determinism. Three
independent measurement workers (image / audio / video); full per-worker logs in
`measurements/`.

## Scoreboard

| Modality | Bar | Fixtures | Result |
|---|---|---|---|
| Image lossless (PNG/BMP) | B1 byte-identical | 4 | ✅ PASS — held SHAs reproduce committed claims exactly |
| Image knowledge-path v3 | byte-identical | 1 | ✅ PASS — renderB SHA `4ee3414b…` reproduced from committed sources |
| JPEG 4:4:4 | max ≤3, mean <0.4 | 1 | ✅ PASS — 3 / 0.21 |
| JPEG 4:2:0 | mechanism named + bounded | 1 | ✅ PASS — 145 / 7.65, replication-vs-smooth, proven from pixels |
| Audio lossless (WAV/FLAC) | B2 byte-identical | 3 | ✅ PASS — held SHAs reproduce; 0/66150 vs ffmpeg on all three |
| MP3 | max ≤8, mean ≤1.0 LSB | 2 | ✅ PASS — max 1.0, mean ~1e-4 (~8× headroom) |
| Video MP4 container | parsed | 1 | ✅ PASS — 8 samples, byte-identical reruns |
| Video H.264 SPS | params | 1 | ✅ PASS — 320×240 Baseline confirmed |
| Video H.264 slices → frames | none (B5: no bar) | 1 | ❌ BLOCKED — no slice decoder in committed Zag |

## Image

Re-ran committed `png.zag` / `raw_bmp.zag` / `jpeg.zag`:

- `img_s16.png` held SHA `9362aaf6…849f73`, `img_m320.png` held
  `255682bf…9904508` — both match committed claims exactly.
- BMP held == PNG held on both fixtures (the verdict's identity claim holds).
- `img_odd.png` (127×65, no committed SHA) independently verified vs PIL:
  byte-identical, 0 diff on all 24,765 pixels.
- JPEG 4:4:4 q95: maxdiff 3, meandiff 0.2103 (bar ≤3, <0.4).
- JPEG 4:2:0 q90: maxdiff 145, meandiff 7.6520 — reproduces the committed
  numbers to the printed digit.

**v3 knowledge-path re-verification:** built committed
`image_exact_work/{common,ingest,emit}.zag` with the pinned toolchain, ran the
full pipeline on the committed fixture: ingest reproduced the RUNLOG's exact
intermediate counts (1849 leaves, 3998 edges, 45,563 residuals); renderB SHA
`4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00` ==
claim, `cmp` byte-identical to original_512.bmp. One honest caveat:
`common.zag` imports `./R33_NATIVE_IO_V1.zag`, never committed under
`image_exact_work/` — supplied from a byte-identical committed copy elsewhere
in the repo (SHA `e6379ddb…`, V1).

## Audio

Re-ran committed `wav.zag`, `flac.zag`, and the committed `mp3/zag_full`
sources (dirty-worktree MP3 changes explicitly out of scope):

- WAV held SHA `17f57ff5…3e1` — matches. Both FLAC fixtures byte-faithful:
  `t.flac` reproduces the WAV SHA; `t24.flac` reproduces its own evidence SHA
  `ece6870f…` (0/66150 vs ffmpeg; see wording caution below).
- MP3 vs committed oracle `mp3ref.py`: cbr max 1.0 / mean 1.45e-04; js max 1.0 /
  mean 7.23e-05. vs ffmpeg @lag 2257: max 1.0 / mean 0.00449. All match the
  RUNLOG to the printed digit; gate passed with ~8× headroom.
- **Waveform analysis first** (comb-filter HNR, spectra, thirds-RMS/crest/ZCR,
  spectral drift, loop periodicity, transient onsets, 50/60 Hz hum ×6
  harmonics): lossless residual 0.0 LSB, every metric identical to all printed
  digits. MP3 residual max 1.0 / rms 0.067 LSB; only near-zero-crossing counts
  move in the 4th decimal. No spectral, envelope, periodicity, transient, or
  tonal structure is altered by the decoder.

## Video

Re-ran committed `mp4.zag` and `sps.zag`:

- Container: 8 samples extracted (60,112 bytes, SHA `48605675…`), reruns
  byte-identical. Honest caveat: `mp4.zag` copies sample byte ranges; the
  9-NAL enumeration (1 SEI, 1 P-slice, 7 IDR) was done externally, and
  SPS/PPS in `avcC` are located but never emitted by the binary.
- SPS: profile 66, level 11, 320×240 Baseline — confirmed.
- **The precise blockage: no slice decoder exists in committed Zag.** PPS parse,
  slice headers, CAVLC, dequant+itrans, intra/inter prediction, deblocking —
  all absent. What exists beyond SPS is a Python prototype (`h264ref.py` +
  `recon.py`) verified only on MB0–MB4 of the first IDR; 81/300 MBs differ on
  the full IDR, the fixture's P-slice is parsed but never reconstructed, and
  deblocking exists nowhere.
- **End-to-end: TNN cannot get from a real .mp4 to faithful frames.** The
  current working video input is raw PPM frames only (committed P6
  reader/writer in `video-fusion-v4`), no codec.
- Honest gap decomposition (from the actual prototype gaps, no guessing):
  port slice-header+CAVLC to pure Zag → fix the 81/300 intra edge bugs →
  P-frame pixel reconstruction → deblocking. Nothing here is a small patch.

## Gap mechanisms, ranked by size (all modalities)

1. **Video slice decode absent** — complete loss of coded-video pixels. The
   largest gap by far: the .mp4→frames path ends at metadata.
2. **JPEG 4:2:0 chroma upsampling: replication (Zag) vs smooth (PIL)** — max
   145 LSB, mean 7.65. Proven from the pixels: held chroma block-constant in
   2×2 cells (std 0.04/0.06) vs PIL smooth (6.58/2.94); hybrid rebuilds put
   the error on chroma, not Y. Honest policy difference, bounded.
3. **JPEG 4:4:4 fixed-point YCbCr→RGB + integer IDCT** — max 3, mean 0.21.
   Within bar, deterministic.
4. **MP3 final-quantization rounding** — 10 samples/fixture flip exactly 1
   LSB. White-box: f64 DSP chain bit-exact vs strict IEEE; residual only at
   float→s16 (away-from-zero vs truncation at half-LSB boundaries) plus
   ~0.001 LSB from the f32 pan-table widening. Quantization policy, not a
   decode error.

## Committed-record inconsistencies flagged (recommend correction)

1. `mp3/EVIDENCE.md`'s summary table says t_128cbr is "0 (byte-identical)" vs
   the oracle; the same file's RUNLOG says max 1.0 / mean 0.00014. This
   battery's re-run matches the RUNLOG (max 1.0, mean 1.45e-04). The table
   entry is wrong or mislabeled.
2. `VERDICT.md`'s "FLAC (mono 16/24-bit) → IDENTICAL" summary line next to the
   WAV SHA reads as if t24.flac should share the WAV SHA — impossible, it
   holds genuinely different 24-bit content. The per-fixture evidence
   (`ece6870f…`, 0/66150 vs ffmpeg) reproduces exactly; the summary line is
   shorthand.

## Honest coverage gaps

- t_vbr.mp3 not measured (committed but not a frozen battery fixture).
- `src/raw_pcm.zag` baseline path not re-run (not a B2 fixture).
- VERDICT's JPEG 4:2:0 127×65 row has no sealed fixture in MANIFEST; not measured.
- Dirty-worktree MP3 sources untouched (audio-round-3 line owns them).
- v3 PSNR/SSIM/determinism-×2 taken from RUNLOG (byte-identity re-verified directly).
- sps.zag skips emulation-prevention unescaping (no effect on this fixture;
  a hostile SPS could misparse — flagged for the record).

## Gallery

`gallery.html` — self-contained (every image and audio clip embedded as a
data URI; zero external loads). For Micah's eyes and ears: input-vs-held
side-by-sides (lossless, JPEG 4:4:4, JPEG 4:2:0 with error heatmaps), waveform
+ spectrum + residual panels, and AB audio excerpts (ffmpeg reference INPUT vs
committed Zag HELD, lag-aligned). Lossless audio excerpts omitted deliberately
(bit-identical — nothing to hear). Video panel shows the pipeline stage
table and the reference frame, plus the honest statement that no frames can
currently be produced from .mp4.

## Bottom line

Image and audio intake are faithful: lossless paths byte-identical, honest
codecs inside committed bounds with mechanisms named and bounded. Video coded
input stops at the container/SPS — the slice decoder is the frontier. Exact
replication holds where it was claimed; where it can't hold yet (H.264), the
blockage is named stage by stage.
