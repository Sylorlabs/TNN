# Fork G3 — post-freeze implementation deviations (NOT a frozen amendment)

**Date:** 2026-09-22
**Status:** These are post-freeze concretization/deviation decisions, documented
transparently. They were NOT frozen pre-results and must NOT be read as part
of the frozen prereg (PREREG_G3.md, frozen at commit f42c11e).

## D1 — t2 colorconst: ±1-bin tolerance (was: exact bin equality)

**Frozen text said:** SAME/DIFF from 4-bit normalized-bin exact comparison.
**Implemented:** SAME_SURFACE iff every channel's 4-bit normalized bin is
within 1 (tolerance), else DIFFERENT.
**Why:** The fixture generator uses a full Bradford chromatic adaptation (not
diagonal in sRGB), so white-patch normalization leaves small residuals; exact
equality over-rejected (stage-1 readout 52.5% → 80.0% on primaries, zero false
accepts either way). Measured on the unenrolled stage-1 binary only.
**Effect on results:** Raises t2 primary readout; enrolled signatures use the
tolerant bins.

## D2 — t3 shapetrans: fixed brightness threshold (was: minority-brightness side)

**Frozen text said:** FG from the minority-brightness side of the mean.
**Implemented:** FG = pixels with (r+g+b) > 480.
**Why:** The minority heuristic latched onto bright photo regions (e.g. sky)
instead of the shape; the generator draws the shape at (235,235,235) on a
photo dimmed to ≤114/channel, so the fixed threshold isolates the shape
(stage-1 readout 36.7% → 100% on primaries).
**Known residual:** Two adversarial shape fixtures (camouflaged: extreme
exposure lowers the shape below 480) produce no graph — honest errors,
ledger-chained, counted as non-installs. This violates the fixture→percept
contract for those inputs and is reported as a limitation, not fixed
post-results.

## D3 — t6 motiondir: block matching (was: change-mask centroids)

**Frozen text said:** 2 EVENT nodes = motion-start/end changed-mask centroids
on a 4×4 grid.
**Implemented:** global translation by exhaustive block matching — downsample
frame0/frame7 to 16×16, SAD over (dx,dy)∈[−4,4] cells, ties → smallest
|dx|+|dy|. Node attrs are displacement bins (dxbin=fdx+16, dybin=fdy+16).
**Why:** A global translation changes pixels everywhere, so the change-mask
centroid sits at frame center regardless of direction; block matching recovers
the true displacement (stage-1 readout 41.7% → 96.7% on primaries).
**Effect on results:** Coarser motion bins raised enrollment collisions
(68 → 106 total); 2 collision groups mix truths.

## D4 — attack-generator parameters (src/corrupt.py)

The 90 G3-specific attack parameters (occlusion bars, harmonic boosts,
exposure factors, reversal, noise σ, brightness/contrast factors) were chosen
post-freeze as concretization of the prereg's attack-class definitions
(§5). They are documented in src/corrupt.py, not in the frozen prereg.

## What did NOT change

The memory contract (exact-signature INSTALL else WITHHOLD), the 288-bit
percept layout, the SHA-256 pinning, the kill bars, the B4 ablation design,
and the B6 determinism protocol are all as frozen. No deviation was made
after any enrolled-template (final binary) result was observed.
