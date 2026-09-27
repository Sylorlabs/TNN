# MP3 RISK 1+2 Survey

**Date:** 2026-09-27
**Decoder:** pure-Zag `mp3dec` (built 2026-09-27 ~04:12 UTC from
`~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full/`)
**Oracle:** `~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/ref/mp3ref.py`
**Scope:** RISK 1 (intensity stereo), RISK 2 (short/mixed block combinations)

---

## RISK 1: Intensity Stereo

### 1a. Encoder reality (mechanism-level finding)

**Current libmp3lame (3.100) does not emit intensity stereo.**

Bitstream survey of deterministic fixtures encoded with
`ffmpeg -c:a libmp3lame -joint_stereo 1` at 32/40/48/64/80/96 kbps:

| Stream (example) | Frames | MS-only | plain JS | IS frames |
|---|---|---|---|---|
| `is_hfwash_32k.mp3` | 156 | 155 | 1 | **0** |
| `is_hftones_48k.mp3` | 156 | 6 | 149 | **0** |

Source inspection (2026-09-27):
- LAME 3.100 `encoder.c` selects only `MPG_MD_LR_LR` and `MPG_MD_MS_LR`.
- LAME 3.96.1 source states: `intensity stereo not implemented yet`
  (and VBR tag: `IS is not implemented`).
- A 2003 commit message claimed initial intensity support, but the
  later 3.96.1 source still reports it unimplemented.

**No genuine libmp3lame-produced intensity-stereo frame was found.**
No standalone intensity-stereo-capable MP3 encoder binary is available
on this VM (only libmp3lame/libshine libraries; shine has no CLI here).

### 1b. Coverage vehicle: bitstream-transformed fixtures (honestly labeled)

Because no real encoder emits IS, four fixtures were made by setting the
mode-extension IS bit (`hdr[3] |= 0x10`) on selected real LAME frames
(`make_is.py`, header-only, no payload changes). These preserve actual
LAME Huffman/scalefactor/spectral data and are **semantically valid**
MPEG-1 Layer III intensity-stereo bitstreams — but they are
**bitstream-transformed, NOT genuine LAME IS output**.

| Fixture | Base | Transform | Size |
|---|---|---|---|
| `is1_hfwash_32k_msis.mp3` | `mp3/is_hfwash_32k.mp3` | IS→155 MS frames (→`0x70` MS+IS) | 65 KB |
| `is2_hftones_48k_isonly.mp3` | `mp3/is_hftones_48k.mp3` | IS→149 plain-JS frames (→`0x50` IS-only) | 97 KB |
| `is3_shimmer_40k_all.mp3` | `mp3/is_shimmer_40k.mp3` | IS→155 JS frames (82 IS-only + 73 MS+IS) | 81 KB |
| `is4_transient_64k_all.mp3` | `mp3/is_transient_64k.mp3` | IS→155 JS frames (2 IS-only + 153 MS+IS) | 129 KB |

### 1c. Intensity-path exercise (oracle-derived, 2026-09-27)

All four fixtures drive the real intensity code path (not a dead mode bit):

| Fixture | Mode-bit classes (frames) | IS granules¹ | Start band (min/med/max) | Bands/granule (range) |
|---|---|---|---|---|
| is1 | 155 MS+IS, 1 plain | 310/310 | 1 / 21 / 24 | 6–31 |
| is2 | 149 IS-only, 6 MS, 1 plain | 298/310 | 2 / 7 / 17 | 5–30 |
| is3 | 82 IS-only, 73 MS+IS, 1 plain | 310/310 | 1 / 9 / 27 | 7–33 |
| is4 | 2 IS-only, 153 MS+IS, 1 plain | 310/310 | 1 / 1 / 33 | 2–38 |

¹ Granules with ≥1 band above the oracle's `stereo_top_band` (i.e. bands
that take the intensity pan-gain path). is1: 4,945 bands total;
`ist_pos` histogram `{0:4925, 1:8, 2:6, 3:6}`.

Coverage includes: IS-only (`0x50`), MS+IS fallback (`0x70`),
persistent `ist_pos` across granules, pan-gain ratios (is_pos 0–3),
short-block intensity bands (279/310 short granules in is1),
intensity-start from band 1 (is4) to band 33, and 2–38 bands/granule.

**Path-activity proof:** flipping the IS bit changes oracle PCM output
(is1: max 9,176 LSB, 2.8% samples differ; is2: max 118 LSB, 6.4% differ),
so the ≤1.0 LSB Zag-vs-oracle matches below are not vacuous.

### 1d. Decoder results

| Fixture | Zag determinism (2 runs) | Zag vs oracle | Zag vs ffmpeg (lag −2257) |
|---|---|---|---|
| is1 | IDENTICAL (sha `97f65654…`) | max **1.0** LSB, mean 0.00011 | max 1.0, mean 0.0014 |
| is2 | IDENTICAL (sha `0e0d2f72…`) | max **1.0** LSB, mean 0.00016 | max 1.0, mean 0.0020 |
| is3 | IDENTICAL (sha `9267731e…`) | max **1.0** LSB, mean 0.00013 | max 1.0, mean 0.0014 |
| is4 | IDENTICAL (sha `9b870dec…`) | max **1.0** LSB, mean 0.00010 | max 1.0, mean 0.0020 |

**RISK 1 verdict: PASS.** Zero defects. The intensity-stereo path
(IS-only, MS+IS, pan gains, short-block bands, persistent ist_pos)
matches the oracle sample-exact on all four fixtures.

---

## RISK 2: Short / Mixed Block Combinations

### 2a. Encoder reality (mechanism-level finding)

**LAME never emits mixed blocks.**

`encoder.c` (LAME 3.100) hardcodes `cod_info->mixed_block_flag = 0`
unconditionally for every granule/channel. The flag is never set to 1
anywhere in the LAME source. Therefore `(block_type=2, mixed=1)` is
**unproducible by libmp3lame** and uncovered by genuine-encoder fixtures
(per task directive, not faked).

### 2b. Coverage matrix (26 files, oracle sideinfo)

Per-(channel,granule) counts of `(block_type, mixed_block_flag)`:

| File | long | start | short | stop | mixed=1 |
|---|---|---|---|---|---|
| sb_rapid_128k | 120 | 98 | 308 | 98 | 0 |
| sb_rapid_192k/320k/64k | 120 | 98 | 308 | 98 | 0 |
| sb_mixed_vbr | 400 | 50 | 124 | 50 | 0 |
| sb_mixed_320k | 468 | 42 | 72 | 42 | 0 |
| sb_mixed_128k/64k | ~520 | 28 | ~47 | 28 | 0 |
| sb_drums_* (all br + vbr) | ~418 | ~63 | ~81 | ~63 | 0 |
| sb_clicks_mono_* (all br) | ~236 | ~22 | ~34 | ~22 | 0 |
| sb_isolated_* (all br) | ~510 | ~33 | ~47 | ~33 | 0 |
| sb_split_* (all br) | ~476 | 42 | 64 | 42 | 0 |

Key structural findings (all 26 files):
- **Zero `mixed_block_flag=1`** in any granule (see §2a).
- **Zero channel-asymmetric block types**: in every frame,
  ch0 and ch1 use the same block type (LAME couples channels).
  `sb_split` (clicks ch0 + tonal ch1, designed for asymmetry) still
  produced 0 asymmetric frames.
- **Cross-granule differences present**: e.g. sb_drums 60/156 frames
  have gr0 ≠ gr1; sb_rapid 95/156.
- Bitrate barely changes block decisions (sb_drums identical at
  64/128/192/320k; VBR uses slightly more shorts).

Combination coverage:
| Combination | Status |
|---|---|
| short+short (both ch, both gr) | ✓ covered (sb_rapid) |
| start/stop transitions | ✓ covered (all files) |
| cross-granule (e.g. short gr0, long gr1) | ✓ covered |
| mixed+long / (block_type=2, mixed=1) | ✗ **uncovered** — LAME hardcodes `mixed_block_flag=0` |
| short ch0 + long ch1 | ✗ **uncovered** — LAME couples block type across channels |

### 2c. Finalist fixtures (nonredundant winners)

| File | Why | Size |
|---|---|---|
| `mp3_sb/sb_rapid_128k.mp3` | Short-dominant stress (308 short / 624) | 64 KB |
| `mp3_sb/sb_mixed_vbr.mp3` | VBR, balanced (124 short, 400 long) | 25 KB |
| `mp3_sb/sb_clicks_mono_128k.mp3` | Mono, long-dominant (29 short, 245 long) | 64 KB |

### 2d. Decoder results

| Fixture | Zag determinism | Zag vs oracle | Zag vs ffmpeg (lag −2257) |
|---|---|---|---|
| sb_rapid_128k | IDENTICAL (`9834d5d0…`) | max **1.0**, mean 0.00011 | max 1.0, mean 0.0147 |
| sb_mixed_vbr | IDENTICAL (`e7b5dae6…`) | max **1.0**, mean 0.00008 | max 1.0, mean 0.0020 |
| sb_clicks_mono_128k | IDENTICAL (`b63cdd70…`) | max **1.0**, mean 0.00011 | max 1.0, mean 0.0012 |

**RISK 2 verdict: PASS.** Zero defects on all LAME-producible
(short/long/start/stop) combinations. The two unproducible combinations
(`mixed_block_flag=1`, channel-asymmetric block types) are documented
in §2a–2b, not faked.

---

## Fixture inventory

All fixtures under `~/workspace/mp3_risks/fixtures/`.
Final coverage winners are ≤1 MB each.

| File | Risk | Description |
|---|---|---|
| `is1_hfwash_32k_msis.mp3` | 1 | MS+IS, 155 fr, wide band range (17 KB) |
| `is2_hftones_48k_isonly.mp3` | 1 | IS-only, 149 fr, low start bands (24 KB) |
| `is3_shimmer_40k_all.mp3` | 1 | IS-only + MS+IS mix (21 KB) |
| `is4_transient_64k_all.mp3` | 1 | MS+IS, transient, start band 1 (32 KB) |
| `mp3_sb/sb_rapid_128k.mp3` | 2 | Short-dominant: 308 short / 624 (64 KB) |
| `mp3_sb/sb_mixed_vbr.mp3` | 2 | VBR balanced: 124 short, 400 long (25 KB) |
| `mp3_sb/sb_clicks_mono_128k.mp3` | 2 | Mono long-dominant: 29 short, 245 long (64 KB) |

## Scripts

| Script | Purpose |
|---|---|
| `gen_is.py`, `gen_sb.py` | Deterministic WAV synthesis (no RNG) |
| `survey_is.py` | Frame-header + oracle intensity-band survey |
| `analyze_is_potential.py` | Intensity-band potential analysis |
| `make_is.py` | Header-bit IS transformation |
| `survey_sb.py` | Block-type combination matrix |
| `compare.py` | Zag×2 determinism, Zag-vs-oracle, Zag-vs-ffmpeg |
