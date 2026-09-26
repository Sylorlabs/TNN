# RUNLOG_FL.md — FREE-LUNCH HUNT (image_tnnlayers)
Micah order 2026-09-26 ~10:55 PDT: "you can't always have free lunch — see if
there's free lunch to reduce size with no cost anywhere else."

## The bar (preregistered before any implementation)

Knowledge bytes DOWN with NO cost anywhere else:
- PSNR/SSIM identical-or-better vs baseline (43.43 dB / 0.9937),
- residual share identical-or-lower (8.2%),
- determinism kept, byte-identical reruns x2,
- understanding render byte-identical (SHA-256
  `a83417476fbbed156b784476b6c3ecf58e7db08e33ae2839a1f10fd6e27524a9`),
- full closure byte-identical (renderA/B == fixture
  `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`).
Anything trading quality for bytes is a TRADE — reported, never claimed.

## Measurement (Python parse of run/knowmap.bin, 2026-09-26 ~11:10 PDT)

Byte accounting (total 1,963,911):
- SMOOTH: 25,298 B (973 leaves x 26 B)
- SHAPES vocab pixel bytes: 1,775,136 B; exemplar u64s: 44,800 B; usage: 8,580 B
- LINES: 672 B
- Residual: 109,292 B (7,806 entries x 14 B)
- Headers/counts: ~134 B

Atom firing (the key measurement):
| scale | atoms | fired | unfired | unfired bytes |
|---|---|---|---|---|
| 32 | 73 | 72 | 1 | 6,152 |
| 16 | 310 | 39 | 271 | 418,424 |
| 8 | 1214 | 96 | 1118 | 438,256 |
| 4 | 4003 | 83 | 3920 | 407,680 |
| total | 5600 | 290 | **5310** | **1,270,512** |

Atom value ranges per scale: [-168,185] — do NOT fit i8.
Usage mean range: [-20,16] (fits i8, but only 1,980 B at stake).
Residual positions: sorted, max gap 56,994 (< 65,535). Deltas: [-95,103] (fits i8).
No exact-duplicate atoms at any scale.

## Candidates — preregistered expectations

| id | candidate | expected saving | expected quality delta | verdict |
|---|---|---|---|---|
| L1 | prune 5,310 unfired atoms (writer-side compaction, same format) | 1,270,512 B | ZERO (never indexed by any usage record) | KEEP iff renders byte-identical |
| L2 | residual recode: u32 first pos + u16 gaps; i8 deltas w/ range-checked mode flag (format TNNKTLM2) | 62,250 B | ZERO (exact reconstruction) | KEEP iff closure byte-identical |
| K1 | atom pixels i16->i8 | — | — | KILLED: values span [-168,185], 353 distinct values, not losslessly representable |
| K2 | drop per-atom exemplar u64 | 2,320 B post-prune | ZERO | REJECTED: provenance (which exemplar block each atom came from) has white-box value exceeding byte value |
| K3 | usage mean i16->i8 | 1,980 B | ZERO | REJECTED: fixture-fragile format churn for 2 KB |
| K4 | share atoms across scales | — | — | REJECTED: changes deliberation/selection; not provably zero-cost; a redesign, not a lunch |
| K5 | tighter SMOOTH quadtree coding | ~10 KB | ZERO | REJECTED: 25 KB total; complexity not worth it; quadtree legibility IS the understanding |
| T1 | drop 58 once-fired atoms | ~11 KB | -0.2 dB (measured) | TRADE, rejected per the bar |

Expected total: 1,963,911 -> ~631,149 B (1,332,762 B saved, 67.9%).

## Results (2026-09-26 ~18:25 PDT, fl1 run)

- knowmap.bin: **623,149 B** (saved **1,340,762 B**, 68.3%) — beats the
  preregistered estimate by 8,000 B (my hand-arithmetic on the residual
  section was off; the measured section sizes are exact: SHAPES saved
  1,270,512 = prereg exactly; residual 109,292 -> 39,042 = 70,250 saved).
- render_understanding.bmp SHA-256 =
  `a83417476fbbed156b784476b6c3ecf58e7db08e33ae2839a1f10fd6e27524a9`
  — byte-identical to the baseline understanding render.
- renderB_understanding.bmp identical (path A == path B).
- renderA.bmp == renderB.bmp == fixture `4ee3414b...` — closure exact.
- metrics.py: 43.43 dB / 0.9937 SSIM — identical to baseline.
- residual: 7,806 / 95,744 px = 8.153% — identical share.
- Residual section independently verified: 7,806 positions + delta triples
  bit-exact vs the baseline knowmap's residual.
- Pruned atom counts in knowmap: 72/39/96/83; every usage index < its
  scale's pruned count (renumbering consistent).
- DELIBTRACE.txt records the prune: "1270512 bytes dropped; kept/built per
  scale: s32:72/73 s16:39/310 s8:96/1214 s4:83/4003".
- fl2 rerun: byte-identical to fl1 on all six artifacts (knowmap
  49c58b74..., understanding renders a8341747..., renderA/B 4ee3414b...,
  DELIBTRACE 5ba60ab0...). Determinism confirmed.

## Byte-accounting ablation (measured, Python port verified byte-identical to fork renders)

| stage | cum. bytes | PSNR | SSIM | +dB |
|---|---|---|---|---|
| SMOOTH | 25,298 | 22.54 | 0.6225 | — (understanding: quadtree+planar) |
| +SHAPES | 1,853,814 | 42.84 | 0.9934 | +20.30 (mechanistic memorization: exemplar patches) |
| +LINES | 1,854,486 | 43.43 | 0.9937 | +0.59 (understanding: straight segments) |

Fired-atom texture ablation (region means kept):
- zero all 280 single-fire atoms' textures -> 22.58 dB / 0.6251 (the
  single-instance "memorization tail" carries ~20 dB — load-bearing)
- zero 10 multi-fire atoms' textures -> 42.18 dB / 0.9925 (-1.25 dB)
- per-decile (29 atoms each): -0.06 dB .. -18.2 dB; every fired decile is
  load-bearing to some degree.

Honest split: SMOOTH (25 KB) and LINES (672 B) are understanding;
SHAPES' 290 fired atoms (~1.79 MB pre-prune) are mechanistic memorization
that buys 20.3 dB; the 5,310 unfired atoms (1.27 MB) buy nothing — dead
weight, the free lunch.

## Implementation (2026-09-26)

- `tnnlayers.zag`: `si_of_b` helper; `tl_prune_shapes` (in-place compaction
  of vocabularies + usage renumber, deterministic); `tl_res_modes` +
  `tl_res_size` (residual coding measurement); `tlk_write` writes pruned
  vocabularies and the TNNKTLM2 residual section (u64 nr, u8 dmode, u8 pflag,
  u32 first, u16/u32 gaps, i8/i16 deltas).
- `tlingest.zag`: prune call after `tl_shapes_build`; PRUNE lines in
  DELIBTRACE.txt; KB numbers from pruned sizes.
- `tlemit.zag`: TNNKTLM2 magic; new residual-section reader.
