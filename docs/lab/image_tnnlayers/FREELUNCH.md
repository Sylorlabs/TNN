# FREELUNCH.md — the image knowledge size free-lunch hunt

Micah order 2026-09-26 ~10:55 PDT: *"you can't always have free lunch — see
if there's free lunch to reduce size with no cost anywhere else."*

## The bar (preregistered before implementation)

Knowledge bytes DOWN with NO cost anywhere else: PSNR/SSIM
identical-or-better vs the 43.43 dB / 0.9937 baseline, residual share
identical-or-lower (8.2%), determinism kept, byte-identical reruns x2,
understanding render byte-identical, full closure byte-identical.
Anything trading quality for bytes is a TRADE — reported, never claimed.

## What was measured (Python parse of the baseline knowmap)

Byte accounting of the 1,963,911-byte baseline knowmap:

| section | bytes | share |
|---|---|---|
| SHAPES vocab pixel data | 1,775,136 | 90.4% |
| residual channel | 109,292 | 5.6% |
| SHAPES per-atom exemplar ids | 44,800 | 2.3% |
| SMOOTH quadtree | 25,298 | 1.3% |
| SHAPES usage records | 8,580 | 0.4% |
| LINES segments | 672 | 0.03% |
| headers/counts | 134 | — |

The firing census — how many of the 5,600 SHAPES atoms ever fire:

| scale | atoms built | atoms fired | atoms dead | dead bytes |
|---|---|---|---|---|
| 32 | 73 | 72 | 1 | 6,152 |
| 16 | 310 | 39 | 271 | 418,424 |
| 8 | 1214 | 96 | 1118 | 438,256 |
| 4 | 4003 | 83 | 3920 | 407,680 |
| **total** | **5600** | **290** | **5310** | **1,270,512** |

95% of the vocabulary never fires. The farthest-point builder builds for
coverage; the take/split deliberation only takes what regions need.

## Free lunches found and kept

**L1 — prune the 5,310 unfired atoms (1,270,512 bytes).** Writer-side
compaction after the deliberation: fired atoms keep their relative order,
usage indices are renumbered deterministically, the deliberation itself is
untouched. Unfired atoms are never indexed by any usage record, so every
render is byte-identical. The knowmap format needs no change for this
(the per-scale atom count simply drops); the DELIBTRACE.txt records the
prune with kept/built counts per scale.

**L2 — recode the residual channel (62,250 bytes).** The residual positions
are strictly increasing (row-major scan) with max gap 56,994 < 65,535, so
u32-first + u16 gaps reconstructs them exactly. The delta triples span
[-95,103], so i8 storage reconstructs them exactly; the writer measures the
range and records a mode flag (dmode/pflag) so the coding stays exact on
any data. Closure stays byte-identical. Magic bumped TNNKTLM1 -> TNNKTLM2
to mark the format change.

**Total: 1,963,911 -> 623,149 bytes (1,340,762 saved, 68.3%), with
byte-identical understanding renders, byte-identical closure, identical
43.43 dB / 0.9937 SSIM, identical 8.2% residual share, byte-identical
reruns x2.** Both lunches verified against the preregistered bar.
(Section-exact: SHAPES 1,828,599 -> 558,087; residual 109,292 -> 39,042.)

## Candidates killed or rejected (with reasons)

| id | candidate | outcome | reason |
|---|---|---|---|
| K1 | atom pixels i16 -> i8 | KILLED | values span [-168,185]: 353 distinct values, not losslessly representable in i8 |
| K2 | drop per-atom exemplar u64s | REJECTED | only 2,320 B post-prune; the exemplar id (which block each atom came from) has white-box provenance value exceeding its byte value |
| K3 | usage mean i16 -> i8 | REJECTED | 1,980 B; fixture-fragile format churn for 2 KB |
| K4 | share atoms across scales | REJECTED | changes the deliberation/selection; not provably zero-cost — a redesign, not a lunch |
| K5 | tighter SMOOTH quadtree coding | REJECTED | 25,298 B total, ~10 KB max saving at real complexity; the quadtree's legibility IS the understanding |
| T1 | drop 58 once-fired atoms | TRADE (rejected) | saves ~11 KB vocab, costs ~0.2 dB measured — fails the identical-or-better bar |

## Byte-accounting: which bytes buy the dB

Layer-cumulative ablation (Python port of the renderers, verified
byte-identical to the fork's own renders):

| stage | cum. bytes | PSNR (dB) | SSIM | marginal dB |
|---|---|---|---|---|
| SMOOTH | 25,298 | 22.54 | 0.6225 | — |
| +SHAPES | 1,853,814 | 42.84 | 0.9934 | +20.30 |
| +LINES | 1,854,486 | 43.43 | 0.9937 | +0.59 |

Fired-atom texture ablation (region means kept, textures zeroed):
- zeroing all 280 single-fire atoms -> 22.58 dB / 0.6251
- zeroing the 10 multi-fire atoms -> 42.18 dB / 0.9925
- per firing-decile (29 atoms each): -0.06 dB to -18.2 dB — every fired
  decile is load-bearing to some degree.

The honest understanding-vs-memorization split: SMOOTH (25 KB) and LINES
(672 B) are understanding — compact mechanisms that earn 23.1 dB between
them. SHAPES' 290 fired atoms are *mechanistic* memorization — exemplar
patches, 280 of them single-instance — and they buy 20.3 dB; every fired
atom is load-bearing. The 5,310 unfired atoms (1.27 MB) buy nothing: pure
dead weight, and the free lunch.

## The size floor

After the two lunches: 623,149 bytes for the 287,232-byte image (~2.2x,
down from ~6.8x). The remaining bytes and why each is load-bearing:

| section | bytes | why it stays |
|---|---|---|
| SHAPES fired-atom vocab (290 atoms) | 549,424 | every fired atom's texture is load-bearing (ablation: zeroing all 280 single-fire textures drops 43.43 -> 22.58 dB); i16 values don't fit i8 (K1 killed) |
| SMOOTH quadtree | 25,298 | buys 22.54 dB alone; recoding saves ~10 KB at real complexity (K5 rejected) |
| residual channel | 39,042 | exact per-pixel error data for closure; already gap/i8-coded |
| SHAPES usage records | 8,580 | 660 placements x 13 B; the placement map itself |
| per-atom exemplar ids | 2,320 | kept deliberately: white-box provenance (K2 rejected) |
| LINES segments | 672 | +0.59 dB for 672 B |
| headers/counts | ~213 | format overhead |

No further free lunch was found: every remaining byte is either measured
load-bearing (fired atoms, layers) or kept for a recorded reason
(provenance, format honesty). The floor is ~623 KB on this fixture —
2.2x the image bytes, down from 6.8x, with zero quality cost.
...[truncated 1148 chars]