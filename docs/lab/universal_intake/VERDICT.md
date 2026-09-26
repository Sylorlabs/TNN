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
| FLAC (stereo mid-side) | ❌ BUG | Mid-side decorrelation produces errors (known issue) |
| MP3 (Layer III) | ⚠️ HEADER ONLY | Frame headers parsed; full decode blocked |
| MP4 container | ✅ PARSED | 8 samples extracted, NAL units validated |
| H.264 (SPS) | ⚠️ PARAMS ONLY | 320×240 Baseline confirmed; slice decode blocked |
| Progressive JPEG | ❌ REJECTED | Explicitly unsupported (not baseline) |

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

### FLAC stereo mid-side
**Bug:** Mid-side decorrelation (ch_assign=10) produces incorrect samples. Mono (independent) works byte-identically. Root cause under investigation — likely LPC coefficient or residual handling specific to the +1-bit side channel.

### Progressive JPEG
**Status:** Explicitly rejected by design (not baseline JPEG). Decoder returns error on Ss/Se/Ah/Al progressive markers.

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
