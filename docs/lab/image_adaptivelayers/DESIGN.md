# Adaptive Layers + Adaptive Magnification — Design

## Order (Micah, 2026-09-26 ~11:31 PDT)
> "no-layers adaptive isn't what I think is best — I think it's layers, adaptive, with adaptive magnification as well"

## What this fork is
A pure-Zag fork combining three parent ideas:

1. **TNN-chosen layers** (from `image_tnnlayers`): Survey → affinity → TNN-selected layer order. Measured commit/revert bars (gain ≥ 9/value). Exact residual closure. The layer order is TNN's choice, recorded not steered.

2. **Content-adaptive CART splits in the structural layer** (the "adaptive"): The SMOOTH layer uses deterministic content-adaptive CART binary splits instead of a fixed midpoint quadtree. Every split position is chosen by measured energy minimization (tests all valid vertical cuts, then horizontal; 4px minimum; strict-improvement for deterministic ties). The parent-1 split bar is preserved (split iff CART-gain ≥ 27·bw·bh). Leaves keep the mean + planar-gradient representation.

3. **Per-region adaptive magnification** (the "adaptive magnification"): The SHAPES layer starts at the coarsest scale chosen by the repetition probe, assigns fixed s×s blocks, then zooms individual blocks to finer scales ONLY when measured residual energy demands it (post-atom residual > 27·w·h per block) AND the finer assignment wins on measured gain-per-byte (gf·cc > gc·c_fine).

## Key design decisions

- **"Take matches ONE vocabulary atom"**: Enforced throughout. Oversized rectangles subdivide; one TAKE = one atom. (Parent 2's critical regression was one TAKE aggregating many coarse atoms → 21.42 dB. Fixed.)
- **Coarsest sufficient scale**: The repetition probe selects the scale set. Zoom is lazy — finer vocabularies are built only for candidate regions, from those regions' full blocks.
- **No arbitrary limits**: Micah's standing law. Pending-list capacities are derived from fixture dimensions (dcap=16384 covers the 512×187 worst case; documented, not a design limit).
- **Zero RNG**: All decisions deterministic given state. Two byte-identical official runs required.

## What was NOT done
The SHAPES partition does NOT use CART. An early draft tried CART-partitioning SHAPES regions; it scored 26.98 dB (worse than all parents) because tiny CART rectangles matched poorly against coarse-scale atoms. Micah's "adaptive" refers to the SMOOTH layer's CART splits, not the SHAPES partition. SHAPES uses fixed blocks (parent 1) + zoom (parent 3). This is documented, not hidden.
