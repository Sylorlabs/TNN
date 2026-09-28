# MP3 RISK 1+2 Results

**Date:** 2026-09-27
**Decoder:** pure-Zag `mp3dec` (fresh build 2026-09-27 ~04:12 UTC)
**Oracle:** `mp3ref.py` (Python reference)
**Gate:** Zag-vs-oracle PCM difference ≤ 1.0 LSB (any excess = decoder defect)

---

## Summary

| Risk | Fixtures | Result | Defects |
|---|---|---|---|
| RISK 1 (intensity stereo) | 4 | **PASS** — all ≤1.0 LSB | 0 |
| RISK 2 (short/mixed blocks) | 3 | **PASS** — all ≤1.0 LSB | 0 |

**Zero decoder defects found.** No workdir source changes were needed;
`~/workspace/mp3_risks/src/mp3dec.zag` is untouched.

---

## RISK 1: Intensity Stereo — PASS

### Encoder reality
Current libmp3lame (3.100) **does not emit intensity stereo**
(source: `encoder.c` selects only `MPG_MD_LR_LR`/`MPG_MD_MS_LR`;
3.96.1 source: "intensity stereo not implemented yet").
No genuine LAME IS frame exists. Coverage via four
**bitstream-transformed** fixtures (IS header bit set on real LAME
frames; honestly labeled, not genuine encoder output). No other
IS-capable MP3 encoder obtainable on this VM.

### Fixture results

| Fixture | Mode bits | IS granules | Zag×2 | Zag vs oracle | Zag vs ffmpeg |
|---|---|---|---|---|---|
| `is1_hfwash_32k_msis.mp3` | 155 MS+IS | 310/310 | IDENTICAL | max **1.0**, mean 0.00011 | max 1.0 |
| `is2_hftones_48k_isonly.mp3` | 149 IS-only | 298/310 | IDENTICAL | max **1.0**, mean 0.00016 | max 1.0 |
| `is3_shimmer_40k_all.mp3` | 82 IS-only + 73 MS+IS | 310/310 | IDENTICAL | max **1.0**, mean 0.00013 | max 1.0 |
| `is4_transient_64k_all.mp3` | 2 IS-only + 153 MS+IS | 310/310 | IDENTICAL | max **1.0**, mean 0.00010 | max 1.0 |

Coverage: IS-only (`0x50`), MS+IS fallback (`0x70`), intensity-start
bands 1–33, 2–38 bands/granule, pan-gain `is_pos` 0–3, persistent
`ist_pos`, short-block intensity bands (279/310 short in is1).

**Non-vacuous:** flipping the IS bit changes oracle output
(is1: max 9,176 LSB, 2.8% samples differ), proving the path is active.

---

## RISK 2: Short/Mixed Blocks — PASS

### Encoder reality
LAME **never emits mixed blocks** (`encoder.c` hardcodes
`mixed_block_flag = 0`). LAME also **couples block types across
channels** (0 asymmetric frames in 26 files, including a purpose-built
asymmetric WAV). Both combinations are uncovered and reported honestly,
not faked.

### Fixture results

| Fixture | Block mix (per ch·granule) | Zag×2 | Zag vs oracle | Zag vs ffmpeg |
|---|---|---|---|---|
| `mp3_sb/sb_rapid_128k.mp3` | 308 short, 98 start/stop, 120 long | IDENTICAL | max **1.0**, mean 0.00011 | max 1.0 |
| `mp3_sb/sb_mixed_vbr.mp3` | 124 short, 50 start/stop, 400 long | IDENTICAL | max **1.0**, mean 0.00008 | max 1.0 |
| `mp3_sb/sb_clicks_mono_128k.mp3` | 29 short, 22 start/stop, 245 long (mono) | IDENTICAL | max **1.0**, mean 0.00011 | max 1.0 |

Coverage: short+short, start→short→stop transitions, cross-granule
differences (e.g. short gr0 / long gr1), mono short blocks, VBR.

### Uncovered (mechanism-level reasons)
| Combination | Why uncovered |
|---|---|
| `(block_type=2, mixed_block_flag=1)` | LAME hardcodes the flag to 0 |
| short ch0 + long ch1 | LAME uses one block type for both channels |

---

## Cross-checks
- **Determinism:** all 7 fixtures byte-identical across 2 Zag runs.
- **ffmpeg:** all 7 match ffmpeg (lag −2257 samples) within 1.0 LSB.
- **Sizes:** all fixtures 17–64 KB (well under 1 MB).

## Defects / fixes
None. The decoder required no changes.
(One harness bug fixed: `compare.py` assumed stereo; now reads channel
count from oracle sideinfo. Not a decoder defect.)
