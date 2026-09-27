# MP3 RISK 1+2 Run Log

Chronological record of the intensity-stereo (RISK 1) and short/mixed-block
(RISK 2) coverage work. All times UTC, 2026-09-27.

## 04:12 — Fresh decoder build
Built pure-Zag decoder from
`~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full/`
→ `~/workspace/mp3_risks/mp3dec` (build OK).
Workdir source copy at `~/workspace/mp3_risks/src/`.
Reproduced committed `t_128cbr` PCM SHA exactly:
`f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467`.

## 04:15–04:21 — RISK 1 encoder survey (libmp3lame)
Wrote `gen_is.py` (deterministic HF/music/transient WAV synthesis, no RNG).
Generated `wavs_is/`: `is_hftones`, `is_hfwash`, `is_transient`, `is_music`,
`is_shimmer`.
Encoded with `ffmpeg -c:a libmp3lame -joint_stereo 1` at
32/40/48/64/80/96 kbps.

**Finding:** zero intensity-stereo frames in any output.
Example `is_hfwash_32k.mp3` (156 frames): 155 MS-only, 1 plain stereo,
0 intensity. Example `is_hftones_48k.mp3` (156 frames): 149 plain JS,
6 MS-only, 1 plain, 0 intensity.

Source inspection: LAME 3.100 `encoder.c` selects only `MPG_MD_LR_LR` /
`MPG_MD_MS_LR`; LAME 3.96.1 source states "intensity stereo not
implemented yet". No genuine LAME IS frame exists to cover.

## 04:20 — Intensity-band potential analysis
`analyze_is_potential.py` on unmodified `is_hfwash_32k.mp3`: 310
joint-stereo granules, all 310 with upper bands qualifying for intensity
(start bands 1–24, 4,945 bands on the pan-gain path, `ist_pos`
`{0:4925, 1:8, 2:6, 3:6}`, 279/310 short-block granules).
Conclusion: setting the IS header bit on these frames yields a
semantically valid intensity-stereo bitstream exercising the real path.

## ~04:25 — Bitstream-transformed IS fixtures
`make_is.py`: header-only `hdr[3] |= 0x10` on selected real LAME frames.
- `is1_hfwash_32k_msis.mp3`: IS→155 MS frames (0x70 MS+IS)
- `is2_hftones_48k_isonly.mp3`: IS→149 plain-JS frames (0x50 IS-only)
- `is3_shimmer_40k_all.mp3`: IS→155 JS frames (82 IS-only + 73 MS+IS)
- `is4_transient_64k_all.mp3`: IS→155 JS frames (2 IS-only + 153 MS+IS)
Labeled as bitstream-transformed, not genuine encoder output.

## 04:22 — RISK 2 WAV synthesis + encodes
Wrote `gen_sb.py`. Generated `wavs_sb/`: `sb_clicks_mono`, `sb_drums`,
`sb_split`, `sb_isolated`, `sb_rapid`, `sb_mixed`.
Encoded 6 WAVs × 64/128/192/320k CBR + 2 VBR → 26 files in `mp3_sb/`.

## ~04:30 — compare.py written; mono bug found and fixed
`compare.py`: Zag×2 determinism (SHA), Zag-vs-oracle (≤1.0 LSB gate),
Zag-vs-ffmpeg with ±4096 lag search.
**Bug:** assumed stereo de-interleaving; `t_128cbr.mp3` is mono →
spurious lag. Fixed: channel count from oracle `sideinfo.json`,
lag search in per-channel samples.
Validated on `t_128cbr.mp3`: lag −2257, max 1.0 LSB (matches EVIDENCE.md).

## ~04:35 — RISK 1 surveys complete
`survey_is.py` on all four transformed fixtures (see SURVEY.md §1c):
- is1: 155 MS+IS fr, 310/310 IS granules, start bands 1–24
- is2: 149 IS-only fr, 298/310 IS granules, start bands 2–17
- is3: 82 IS-only + 73 MS+IS fr, 310/310 IS granules, start bands 1–27
- is4: 2 IS-only + 153 MS+IS fr, 310/310 IS granules, start bands 1–33

## ~04:40 — RISK 1 comparisons: ALL PASS
| fixture | Zag×2 | Zag vs oracle | Zag vs ffmpeg |
|---|---|---|---|
| is1 | IDENTICAL | max 1.0, mean 0.00011 | max 1.0, lag −2257 |
| is2 | IDENTICAL | max 1.0, mean 0.00016 | max 1.0, lag −2257 |
| is3 | IDENTICAL | max 1.0, mean 0.00013 | max 1.0, lag −2257 |
| is4 | IDENTICAL | max 1.0, mean 0.00010 | max 1.0, lag −2257 |

**Path-activity proof:** flipped-vs-unflipped oracle PCM differs
(is1: max 9,176 LSB, 2.8% samples; is2: max 118 LSB, 6.4% samples),
so the ≤1.0 LSB matches are not vacuous.

## ~04:45 — RISK 2 block-type surveys
`survey_sb.py` (oracle sideinfo → block_type × mixed matrix).
`sb_drums_128k`: long 420, start 62, short 80, stop 62 (per ch·granule);
patterns include long×4, short→stop, start→short, stop→long.
**Zero mixed_block_flag=1 in any file at any bitrate.**

## ~04:50 — Mixed-block mechanism finding
LAME 3.100 `encoder.c` hardcodes `cod_info->mixed_block_flag = 0`
unconditionally; the flag is never set to 1 anywhere in LAME source.
`(block_type=2, mixed=1)` is unproducible by libmp3lame → uncovered,
not faked (per task directive).

## (pending) — Full 26-file RISK 2 matrix, finalist selection, comparisons

## ~05:00 — RISK 2 full matrix complete (26 files)
Key findings:
- Zero `mixed_block_flag=1` in any file (any bitrate, any content).
- Zero channel-asymmetric block types (LAME couples ch0/ch1).
- Cross-granule differences present (e.g. sb_drums 60/156, sb_rapid 95/156).
- Bitrate barely affects block decisions.
- sb_rapid: heaviest shorts (308/624). sb_mixed_vbr: most shorts in
  mixed content (124). sb_clicks_mono: mono long-dominant.

## ~05:05 — RISK 2 finalists selected (nonredundant)
- `mp3_sb/sb_rapid_128k.mp3` (64 KB): short-dominant stress
- `mp3_sb/sb_mixed_vbr.mp3` (25 KB): VBR balanced
- `mp3_sb/sb_clicks_mono_128k.mp3` (64 KB): mono long-dominant

## ~05:10 — RISK 2 comparisons: ALL PASS
| fixture | Zag×2 | Zag vs oracle | Zag vs ffmpeg |
|---|---|---|---|
| sb_rapid_128k | IDENTICAL | max 1.0, mean 0.00011 | max 1.0, lag −2257 |
| sb_mixed_vbr | IDENTICAL | max 1.0, mean 0.00008 | max 1.0, lag −2257 |
| sb_clicks_mono_128k | IDENTICAL | max 1.0, mean 0.00011 | max 1.0, lag −2257 |

## ~05:15 — Docs written
`SURVEY.md` (coverage matrices, encoder findings), `RESULTS.md`
(verdicts), this `RUNLOG.md`. All 7 finalists 17–64 KB (<1 MB).
**Zero decoder defects. No source changes.**
