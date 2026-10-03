# VERDICT.md — H.264 CAVLC Parser Bug

**Status:** `CLOSED-parser-bug`  
**Date:** 2026-09-26

## Exact Mechanism

The parser's `neigh_block_4x4()` interpreted `luma4x4BlkIdx` in **raster order**:

```python
bx = blkIdx % 4
by = blkIdx // 4
```

H.264 specifies `luma4x4BlkIdx` in **8x8-grouped order** (Fig 6-??):

```
 0  1 | 4  5
 2  3 | 6  7
------+------
 8  9 |12 13
10 11 |14 15
```

**Chain of failure:**
1. Wrong neighbor blocks selected for nC derivation (§9.2.1).
2. Wrong nC → wrong `coeff_token` VLC table.
3. **First material divergence:** MB4, luma block y11, bit 806.  
   Old: nC=3, 2-bit token → (TotalCoeff=0).  
   Fixed: nC=5, 4-bit token → (TotalCoeff=1).
4. Bitstream desynchronization from bit 806 onward.
5. **Manifestation:** MB4 Cb AC3, bit 1009: `TotalCoeff=16` with `maxNumCoeff=15` — impossible. FFmpeg's `decode_residual()` rejects `total_coeff > max_coeff`; chroma AC uses `max_coeff=15`.

## MB4 Confirmation (FFmpeg Ground Truth)

Reconstructed the first IDR (NAL 3) from the **fixed** parser's CAVLC output using a spec-compliant H.264 reconstructor (`recon.py`: §8.5.10/8.5.11/8.5.12 dequant+transform, §8.3.1.2/8.3.3/8.3.4 intra prediction).

**Compared against ffmpeg 8.1 no-deblock decode** (`/tmp/idr0_nodeblock.yuv`, SHA-256 `5ce87b07...`):

| MB | Pixels differing |
|----|------------------|
| MB0 | 0/256 ✅ |
| MB1 | 0/256 ✅ |
| MB2 | 0/256 ✅ |
| MB3 | 0/256 ✅ |
| MB4 | 0/256 ✅ |

**All 1,280 pixels match bit-exact.** The fixed parser's MB4 (including the y11 divergence point and the full chroma AC sequence through bit 1075) is confirmed correct by ffmpeg.

The old parser cannot produce a reconstruction for MB4 — it desyncs at bit 806 and yields an impossible coefficient count at bit 1009.

## Fix Applied

`h264fix.py` (and backed-up `h264ref.py`) now use:

```python
def _l4_xy(idx):
    # 8x8-grouped order
    return ((idx % 2) + 2 * ((idx // 4) % 2),
            ((idx // 2) % 2) + 2 * (idx // 8))

def _l4_idx(x, y):
    return 4 * ((y // 2) * 2 + (x // 2)) + (y % 2) * 2 + (x % 2)
```

## Scope Notes

- **Closed for:** CAVLC nC derivation / neighbor-order bug affecting MB0–MB4 (and the full first IDR: 300/300 MBs parse).
- **Not in scope:** 81/300 MBs in the full-frame reconstruction differ due to separate intra-prediction edge-case bugs (e.g., I_4x4 Horizontal-Up `zHU>5` fallback, left-edge mode constraints). These do not affect the CAVLC verdict for MB0–MB4.
- **Not committed:** Per task instructions, no commit made. `h264ref.py` fix applied to workdir only.

## Honest Blocker Assessment

None for this verdict. The ffmpeg ground-truth experiment was decisive: pixel-perfect MB0–MB4 match with the fixed parser, impossible-coefficient failure with the old parser, and a precisely localized first divergence (bit 806) with a verified mechanistic chain.
