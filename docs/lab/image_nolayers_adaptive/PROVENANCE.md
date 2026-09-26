# PROVENANCE.md — image_nolayers_adaptive

## What this fork is

A variant of the no-layers image fork (`~/workspace/image_nolayers/`,
rigid commit `3a49b9c7031c51e81ab723c4dfbca14f246fe579`) that removes the
rigid dyadic grid. The single mechanism (one deliberative pass, one
shared exemplar vocabulary, per-tile best-atom matching, per-tile exact
residual contract) is unchanged. The only change is the region
decomposition: content-delimited rectangles instead of the fixed quadtree.

## The split rule (the one design decision)

For a region R, every valid vertical and horizontal pixel cut (leaving
>=4 px per side) is scored by E_flat(child1) + E_flat(child2), using exact
integer prefix sums of (sum, sumsq) per row/column band. The argmin cut is
selected; ties scan vertical-before-horizontal, lowest position first,
replaced only on strictly lower energy. This is the CART/regression-tree
rule: it maximizes flat-fit energy explained vs the one-piece baseline —
the same explained-energy currency the fork already uses for its
take/split gain-per-byte decision and its vocabulary farthest-point
selection. No thresholds, no tuned constants. Recorded in DESIGN.md
before any run.

## Deliberation (unchanged decision currency)

For each region: evaluate TAKE (tile the rect at the fit scale — largest
atom scale <= min(bw,bh) — and match every tile independently against that
scale's vocabulary) and SPLIT (the CART cut, children decided recursively
first). Choose by exact gain-per-byte,
(e0-ea)/ca vs (e0-es)/cs, cross-multiplied to avoid division; ties take.
The knowmap format (TNNKNLM1), residual contract, render paths, and the
emit (path-B understanding reconstruction) are byte-identical in format to
the parent fork.

## Determinism

Pure Zag, zero RNG. Farthest-point selection, CART scan, and the
take/split comparison are all deterministic; tie-breaks are positional.
Two independent runs must be byte-identical (verified, see SHASUMS.txt).

## Toolchain

Pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Sealed fixture

512x187 24-bit BMP, SHA-256
`4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`
(the Albi photograph). Verified before every run.

## Parent numbers (for the gap analysis)

- Layered zoom fork: 30.80 dB / 0.9620 SSIM, 19.9% residual, 1,343,354 bytes.
- Rigid no-layers: 29.27 dB / 0.9260 SSIM, 11.7% residual, 2,505,092 bytes.
- Gap: 1.53 dB / 0.0360 SSIM.
