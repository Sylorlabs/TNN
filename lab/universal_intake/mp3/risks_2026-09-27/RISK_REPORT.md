# MP3 Remaining Risks — Closure Report (2026-09-27)

Closes the four open risks from the pure-Zag decoder trial. Workdir:
`~/workspace/mp3_risks/` (not committed; reports + sealed fixtures below).

## Risk 1 — Real intensity-stereo fixtures: PASS

| Fixture | Mode bits | IS granules | Zag vs oracle (max LSB) |
|---|---|---|---|
| is1_hfwash_32k_msis.mp3 | 155 MS+IS | 310/310 | 1.0 |
| is2_hftones_48k_isonly.mp3 | 149 IS-only | 298/310 | 1.0 |
| is3_shimmer_40k_all.mp3 | 82 IS-only + 73 MS+IS | 310/310 | 1.0 |
| is4_transient_64k_all.mp3 | 2 IS-only + 153 MS+IS | 310/310 | 1.0 |

Coverage: IS-only (`0x50`), MS+IS fallback (`0x70`), intensity-start
bands 1–33, 2–38 bands/granule, pan-gain `is_pos` 0–3, persistent
`ist_pos`, short-block intensity bands. Non-vacuous: flipping the IS bit
changes oracle output (is1: max 9,176 LSB), proving the path is active.
All byte-identical across 2 Zag runs; all match ffmpeg within 1.0 LSB.

**Caveat (honest):** current libmp3lame (3.100) does not emit intensity
stereo (`encoder.c` selects only LR/MS modes; "intensity stereo not
implemented yet"). No genuine LAME IS frame exists. Coverage is via
bitstream-transformed fixtures (IS header bit set on real LAME frames),
honestly labeled — not genuine encoder output.

## Risk 2 — Short/mixed-block combinations: REAL BUG FOUND AND FIXED

Short-block fixtures (308 short + start/stop transitions, VBR, mono):
3/3 PASS, ≤1.0 LSB.

Mixed-block fixtures (mixed flag flipped on pure-short encodings):
**failed at 65,535 LSB max error** — a genuine decoder defect, not a
fixture artifact:

- **Root cause:** `t_scf_mixed_rows` in `zag_full/mp3tab64.zag` stored
  the MPEG-1 mixed scalefactor-band table as variable-length rows
  (37/40/37/37/37/39/39/39 bytes incl. 0-terminator) but
  `mixed_row_get` indexed with a fixed **39-byte stride**
  (`row * 39 + i`). Every row after the first was misaligned; row 5
  (44.1 kHz) started with a `0` byte, which the copy loop reads as
  end-of-table → effectively empty mixed band table → wrong band
  boundaries → wrong scalefactor application, Huffman partitioning,
  and reorder.
- **Fix (2 lines + table re-pad):** rebuilt the table at a correct
  **40-byte stride** (fits the longest row), `mixed_row_get` uses
  `row * 40 + i`, copy-loop bound `k < 39` → `k < 40`.
  Per ISO 11172-3 Table 19: 38 bands = 8 long (sfb 0–7) + 10 short
  (sfb 3–12) × 3 windows; 35 transmitted.

| Fixture | Before (max LSB) | After (max LSB) | After (mean LSB) |
|---|---|---|---|
| mxflip_rapid_all | 65,535 | 1 | 0.0003 |
| mxflip_rapid_alt | 65,535 | 1 | 0.0001 |
| mxflip_drums_all | 65,535 | 1 | 0.0001 |
| mxflip_drums_alt | 65,535 | 1 | 0.0001 |

Regression: `t_128cbr` reproduces the committed SHA; all standard
fixtures ≤1 LSB vs oracle.

**Caveats (honest):** mixed fixtures are header-transformed, not genuine
encoder mixed streams (LAME hardcodes `mixed_block_flag = 0`); asymmetric
cross-channel block types uncovered (LAME couples block type across
channels); the 32 kHz `n_long_bands` hardcoded-2 vs oracle shift
discrepancy was **not** addressed — separate investigation needed.

## Risk 3 — Max-Huffman-value stress (`pow_43_z`): PASS, no defects

- Full-domain sweep of `pow_43_z` (x ∈ [0, 8206], 8207 outputs):
  0 NaN, 0 inf, 0 negatives; max rel err vs strict `x**(4/3)` is
  1.32e-6 (pre-existing quadratic-approximation interior error, not a
  boundary defect).
- B1 Huffman stage bit-exact across all 16 linbits tables; max
  `one × pow_43_z(lsb)` ≈ 2.02e8 — nowhere near overflow.
- 33 synthetic extreme frames: PCM matches stock oracle ±1 LSB.
- No source changes needed.

## Risk 4 — Diagnostician precision: FIXED (v3)

| Metric | v2 baseline | v3 |
|---|---|---|
| Total hits on decoder (1345 lines) | 323 hits / 225 lines | **1 hit / 1 line** |
| Genuine pan-table defect rank | 7th (score) / 40th (raw) | **1st** |
| Genuine-only precision | 0.31% | **100%** |

All v3 mechanisms are generic (structural features, integer log-IDF
background model, score ranking) — no decoder-specific hardcodes.
Deterministic, byte-identical reruns. Honest limit: the unguarded
bitrate-table defect class is correctly *not* flagged — precision
cannot invent a missing defect class.

## Files

- `zag_full/mp3dec.zag`, `zag_full/mp3tab64.zag` — the mixed-block fix
- `risks_2026-09-27/fixtures/` — RESULTS.md, SURVEY.md, RUNLOG.md +
  sealed MP3 fixtures (is1–is4, mxflip×4, sb×3)
- `risks_2026-09-27/huffstress/` — STRESS_REPORT.md, RUNLOG.md
- `risks_2026-09-27/diagprec/` — PRECISION_REPORT.md, RUNLOG.md,
  `tnn_mp3diag_v3.zag`
