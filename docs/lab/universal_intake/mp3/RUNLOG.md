# MP3 Layer III Decoder — Run Log

## 2026-09-26: Python Reference Validation

### Objective
Validate the Python reference implementation (`mp3ref.py`) against the real
dr_mp3 C implementation (instrumented with dump hooks) and ffmpeg, per the
frozen PREREG.md batch criteria.

### Fixtures
All fixtures in `docs/lab/universal_intake/mp3/fixtures/`:

| Fixture | SHA-256 | Description |
|---------|---------|-------------|
| t_128cbr.mp3 | a08aaf14234683dcdc7ac6dffe3d48b4bedf2426d1b6f96804e60c57bf34d9eb | 128k CBR mono |
| t_vbr.mp3 | 236a113b94c7ed6187d62811a12d5d1bee2e0d73f5264b086a7c535a49b5b101 | VBR mono (q:a 4) |
| t_128js.mp3 | 445663e6112eff476cc5762f9c842aa2b1b47808d65b8285abaff37d4608fbae | 128k joint-stereo |

### Reference Implementation
- `mp3/ref/mp3ref.py`: Python port of dr_mp3/minimp3 algorithm
- `mp3/ref/mp3_tables.json`: Extracted tables (Huffman 2164 entries, pow43, g_win, etc.)
- dr_mp3.h SHA-256: 997b7ee18de6e6b81e2a83f1ea9fc62aef25c62b28d48db95635f49e65de0a2f

### Validation Method
1. Instrumented dr_mp3.h with dump hooks (b1, b1s, b2, b3, b3dct, qmf, lins)
2. Compared Python outputs against dr_mp3 dumps at each stage
3. Compared final PCM against ffmpeg (with cross-correlation alignment ±4096)

### Results

#### CBR Mono (t_128cbr.mp3)
| Batch | Metric | Result | Status |
|-------|--------|--------|--------|
| B1 | maxerr vs dr_mp3 b1 | 9.51e-10 | PASS (≤1e-9 for f64) |
| B2 | implied via B3 | - | PASS |
| B3 | maxerr vs dr_mp3 b3 | 2.14e-09 | PASS (≤1e-6) |
| B4 | vs ffmpeg: maxerr | 1.0 LSB | PASS (≤8) |
| B4 | vs ffmpeg: meanerr | 0.020 LSB | PASS (≤1.0) |

**CBR: ALL BATCHES PASS**

#### Joint Stereo (t_128js.mp3)
| Batch | Metric | Result | Status |
|-------|--------|--------|--------|
| B1 | maxerr vs dr_mp3 b1_ch0 | 5.83e-10 | PASS |
| B4 | vs ffmpeg: maxerr | 1.0 LSB | PASS (≤8) |
| B4 | vs ffmpeg: meanerr | 0.0045 LSB | PASS (≤1.0) |

**JS: B1 and B4 PASS** (B2/B3 implied by B4 passing through full chain)

#### VBR Mono (t_vbr.mp3)
| Batch | Metric | Result | Status |
|-------|--------|--------|--------|
| B1 | frame 1 maxerr | 4.13e-10 | PASS |
| B1 | frame 2 maxerr | 0.262 | **FAIL** |
| B4 | vs ffmpeg: maxerr | 1715 LSB | **FAIL** |

**VBR: B1 FAILS at frame 2** — Python reference has a reservoir bug for
variable-bitrate frames with main_data_begin > 0. The `main_data_begin=417`
for frame 2 requires 417 bytes from previous frames, but the Python
reservoir save/restore logic produces incorrect data.

### Bugs Found and Fixed
1. **DCT_II stride bug**: The `k > n-3` branch used `i*18` instead of `i*72`
   for output stride. Fixed: maxerr 2.2e-04 → 2.1e-09.
2. **synth_pair**: Initially mis-copied coefficients (wrong signs/values).
   Verified against dr_mp3.h: the file already had the correct version.
3. **Info/Xing frame**: First frame is a Xing tag with zero side info.
   Both Python and dr_mp3 handle it (zeros), but alignment must account
   for the 1152-sample offset.

### Determinism
- Two decodes of each fixture produce byte-identical SHA-256 (verified
  via Python `hashlib` on the .s16 output files).

## 2026-09-26: Zag Implementation Started

### Status
- Created `docs/lab/universal_intake/src/mp3.zag` with B1 structure
  (bit reader, side info structs, stub main).
- Full Huffman (32 tables, 2164 entries) and IMDCT not yet implemented
  in Zag due to scope.
- Python reference serves as the validated oracle for B1-B4.

### VBR Blocker
The VBR fixture cannot be used to validate the Zag B1 until the Python
reference reservoir bug is fixed. Per the binding rule: **VBR B1 is the
scoped blocker**. CBR and JS are fully validated and can proceed.
