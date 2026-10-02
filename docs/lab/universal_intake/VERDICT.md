# Workstream A: Universal Format Intake — VERDICT

**Date:** 2026-09-26  
**Branch:** tnn-native-lab  
**Toolchain:** znc_linux_x86_64_abed8aa1

## Coverage Table

| Format | Status | Proof |
|--------|--------|-------|
| PNG (all color types, interlaced) | ✅ BYTE-IDENTICAL | SHA-256: 9362aaf61baf7cf368b08efe502af978b392e375f59d1a2b7929c03a6c849f73 (16×16) |
| JPEG baseline (gray, 4:4:4) | ✅ DECODED (honest lossy) | maxdiff ≤3, meandiff <0.4 (IDCT + RGB rounding) |
| JPEG baseline (4:2:0) | ✅ DECODED (honest lossy) | Y meandiff 0.3; RGB gap from chroma upsampling (replication vs smooth) |
| WAV (PCM 8/16/24/32, float32/64, extensible) | ✅ BYTE-IDENTICAL | SHA-256: 17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1 |
| FLAC (mono 16/24-bit) | ✅ BYTE-IDENTICAL | Matches WAV SHA-256 exactly |
| FLAC (stereo all assignments) | ✅ BYTE-IDENTICAL | 10 fixtures (assign 1/8/9/10, verbatim/fixed/wasted/const) match ffmpeg 0/88200; reruns byte-identical |
| MP3 (Layer III) | ⚠️ REFERENCE VALIDATED | Python oracle passes B1-B4 for CBR mono + Joint Stereo vs dr_mp3/ffmpeg; VBR blocked (reservoir bug); Zag B1 started |
| MP4 container | ✅ PARSED | 8 samples extracted, NAL units validated |
| H.264 (SPS) | ⚠️ PARAMS ONLY | 320×240 Baseline confirmed; slice decode blocked |
| Progressive JPEG | ✅ SUPPORTED | T.81 Annex G: 0 coeff mismatches vs libjpeg; 3 sealed fixtures |

## Byte-Identity Proofs

### PNG vs BMP (raw path)
```
PNG 16×16 held:  9362aaf61baf7cf368b08efe502af978b392e375f59d1a2b7929c03a6c849f73
BMP 16×16 held:  9362aaf61baf7cf368b08efe502af978b392e375f59d1a2b7929c03a6c849f73
→ IDENTICAL

PNG 320×240 held: 255682bfd35357dc4ee5ea44c56fd82b8f4b1eef0a46cf2e7813218b09904508
BMP 320×240 held: 255682bfd35357dc4ee5ea44c56fd82b8f4b1eef0a46cf2e7813218b09904508
→ IDENTICAL
```

### WAV (PCM16)
```
WAV held: 17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1
RAW held: 17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1
→ IDENTICAL
```

### FLAC mono vs WAV
```
FLAC held: 17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1
WAV held:  17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1
→ IDENTICAL (16-bit and 24-bit mono)
```

## JPEG Honest Lossy Differences

| Fixture | Max diff | Mean diff | Mechanism |
|---------|----------|-----------|-----------|
| Gray 16×16 | 1 | 0.109 | Integer IDCT rounding (±1) |
| Gray 127×65 | 1 | 0.076 | Integer IDCT rounding |
| Gray 320×240 | 1 | 0.062 | Integer IDCT rounding |
| 4:4:4 q95 16×16 | 3 | 0.346 | IDCT + YCbCr→RGB fixed-point |
| 4:4:4 q95 320×240 | 3 | 0.210 | IDCT + YCbCr→RGB fixed-point |
| 4:2:0 q90 320×240 | 145 | 7.652 | Chroma upsampling: replication (mine) vs smooth (PIL) |
| 4:2:0 q90 127×65 | 137 | 8.682 | Chroma upsampling difference |

**White-box explanation:** For 4:2:0, the Y channel matches (meandiff 0.3), proving entropy/IDCT/dequant are correct. The RGB gap is entirely the chroma upsampling filter: I use nearest-neighbor replication, PIL uses a smooth filter. This is an honest, documented consequence of the chosen upsampling policy, not a decode error.

## Determinism (2 runs, byte-identical)
- PNG: ✅
- WAV: ✅  
- FLAC: ✅
- JPEG: ✅

## Negative Tests
- PNG corrupt CRC: rejected ✅
- PNG corrupt Adler: rejected ✅
- PNG truncated: rejected ✅
- JPEG truncated: rejected ✅
- FLAC bad CRC: rejected ✅

## Unreachable Mechanisms

### MP3 Layer III full decode
**Blocker:** Huffman decoding (32 variable-length tables), 18/36-point IMDCT with alias reduction, 512-point polyphase synthesis filterbank with windowing. Estimated ~1500 lines of DSP code. Frame headers parse correctly (verified).

### H.264 baseline slice decode  
**Blocker:** CAVLC residual decoding, intra 4×4/16×16 prediction (9+4 modes), inter P-frame motion compensation (sub-pixel interpolation), deblocking filter (boundary strength computation). Estimated ~2000 lines. SPS parses correctly (320×240 Baseline confirmed), MP4 container extracts NALs correctly.

### FLAC stereo (RESOLVED 2026-09-26)
**Status:** ✅ BYTE-IDENTICAL. All stereo channel assignments (1=independent, 8=left-side, 9=right-side, 10=mid-side) decode byte-identical to `ffmpeg -acodec pcm_s16le` across 10 deterministic fixtures (verbatim, fixed-order 2/3/4, wasted-bits, constant), 0/88200 differing samples, with byte-identical reruns. FFmpeg-generated LPC stereo also byte-identical. Mono 16/24-bit regress clean.

**Root causes found (white-box):**
1. **Legal `-1` treated as error:** `fr_takes()` returned `-1` on I/O error, but `-1` is a legal sample/warmup/coefficient/shift/residual/side-channel value. Any frame with a `-1` (common in side channel) aborted before decorrelation. Fixed with explicit status + output slice API.
2. **Independent stereo rejected:** assignments 1-7 were skipped; correct is `fch = ch_assign + 1` for 0-7, validated against STREAMINFO channels.
3. **Escape residuals mishandled (pre-existing):** the 5-bit escape field's `+1` was missing and the bit was mis-consumed, desyncing the stream. Fixed per FLAC spec (`rawbps = field + 1`).

See `evidence/flac_stereo_2026-09-26.md` for the full proof table and SHAs.

### Progressive JPEG
**Status:** SUPPORTED (2026-09-26). T.81 Annex G implemented in pure Zag: SOF2, multi-scan SOS,
spectral selection + successive approximation (DC first/refine, AC first/refine), EOB runs,
per-scan Huffman tables, deferred IDCT from full-frame coefficient buffer.

**Proof:** 0 coefficient mismatches vs libjpeg-turbo 2.1.5 on 3 fixtures (4:4:4, 4:2:0, grayscale);
Zag RGB within IDCT rounding of proven prototype (maxdiff ≤4); byte-identical reruns;
baseline regression byte-identical.

**Cost:** ~400 new Zag lines (`src/prog_scan.zag` + `src/jpeg.zag` mods); 0.92–1.84 MB coefficient
buffer for 320×240 fixtures.

**Prevalence:** 7% historical (Data Center Knowledge); 19/19 current image-service samples progressive.
Rejection was a format barrier; Micah's "no format barrier" direction requires support.

**Limitations:** Coefficient buffer not yet chunked (2^25 slice ceiling for very large images);
basic RSTn handling; 4:2:0 uses inherited nearest-neighbor chroma replication.

See `evidence/progressive_jpeg_2026-09-26.md` for the full proof table, SHAs, and honest Pillow comparison.
Implementation commit: `1498e3208`.

## Audio Samples 0..63 Retention
Verified for WAV: all PCM variants retain samples 0..63 exactly (ndiff=0 in oracle comparison).

## Scale / Chunking
- Current implementation uses whole-file reads (file_read_all capped at 2^25-1).
- **TODO:** Replace with chunked streaming to satisfy no-scale-degradation requirement.
- znc 2^25 slice ceiling acknowledged; chunking design pending.

## Files
- Sources: `src/*.zag` (common, png, jpeg, wav, flac, mp4, mp3hdr, sps, raw_bmp, raw_pcm)
- Fixtures: `fixtures/` (sealed test files)
- Binaries: `scratch/` (NOT for commit)
