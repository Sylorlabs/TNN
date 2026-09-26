# RUNLOG.md — image_nolayers_adaptive

## 2026-09-26

- ~09:54 PDT: order received (Micah): kill the rigid grid for no-layers,
  "for a real result".
- Built `~/workspace/image_nolayers_adaptive/` by reusing the rigid fork's
  code (common_nl.zag, R33_NATIVE_IO_V1.zag, metrics.py copied verbatim;
  vocabulary/survey/residual/render/knowmap-format untouched).
- Wrote DESIGN.md FIRST (before any run): the split-position criterion is
  the CART rule — argmin over every valid pixel cut of
  E_flat(c1)+E_flat(c2), i.e. the cut maximizing flat-fit energy explained
  vs the one-piece baseline. Same explained-energy currency as the fork's
  take/split and vocabulary decisions. No thresholds, no tuned constants.
  Regions are rectangles; entry is the whole image; TAKE tiles the rect at
  fit scale (largest atom scale <= min(bw,bh)); floor = no valid cut or no
  energy-reducing cut -> must take; min-dim-4 invariant.
- New code: nolayers_ad.zag (spliced: shared fns kept, deliberate_block
  replaced by fit_scale/fit_si/seg_e0/col_prefix/row_prefix/cart_cut/
  materialize_tiles/deliberate_rect), nlingest_ad.zag (driver: single
  deliberate_rect call on the whole image, 8MB trace ledger, regcap 32768),
  nlemit_ad.zag (import swap only — knowmap format TNNKNLM1 unchanged).
- Audit before run caught and fixed one real bug: col_prefix/row_prefix
  never zeroed the prefix-sum base (psx[0..2]) — uninitialized heap read
  in seg_e0 for a=0. Smoke tests passed by allocator luck (fresh zero
  pages); the full-fixture first run died mid-assignment (silent, likely
  OOM/environmental under load ~17 — or heap-garbage pathology; the
  evidence would have been garbage anyway). Fixed, rebuilt, relaunched.
- Smoke tests (post-fix binary): 64x48 synthetic (3 exact boundaries) —
  CART cuts landed EXACTLY on all three (H12, V20, V24 in pix coords);
  take/split gain-per-byte decided TAKE at every level (rate-distortion
  working as designed); path A == path B (16.60 dB both). 256x160 complex
  synthetic — exit 0, 12 regions.
- Fixture SHA-256 verified before runs:
  4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00.

## Timing

- Machine heavily loaded (load ~17, process at ~10% CPU): vocabulary
  ~10+ min wall, assignment TBD. run/ in progress.

## 2026-09-26 (afternoon)

- Run 1 (original design): 21.42 dB / 0.7870 SSIM — FAILURE. White-box:
  root TOOK at 64 for whole image (ea=137M); town child TOOK at 64
  (ea=300M). The gain-per-byte aggregates N tiles into one greedy
  decision; myopic recursion never goes deep. Render showed coarse
  64-blocks in town band.
- DESIGN.md amendment: structural must-split — a take matches ONE atom;
  rect bigger than fit-scale atom MUST split via CART. Only atom-sized
  rects deliberate take-vs-split by gain-per-byte.
- Rebuilt, smoke-tested (64x48: PSNR inf, perfect; CART cuts exact).
- Run 1 (fixed): 30.50 dB / 0.9183 SSIM, 8810 regions, 93.1% residual,
  3,682,332 byte knowmap. 3824 forced splits, 3820 takes, 5 split-wins.
  Path A == Path B; full render == sealed fixture.
- Gap closed: 1.23/1.53 dB (80%). SSIM -0.0077 (blocking from many tiles).
- Run 2 launched for byte-identical verification.
