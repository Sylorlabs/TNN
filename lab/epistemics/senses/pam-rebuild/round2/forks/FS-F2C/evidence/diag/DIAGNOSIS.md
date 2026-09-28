# FS-F2C Phase-0 diagnosis — colorconst formation error modes

**Date:** 2026-09-24. **Basis:** FS-E2's committed Phase-0 TSVs
(`form_r2n_colorconst.tsv`, byte-identical x2, 2000/2000 cross-checked vs the
frozen FS-E1 ledger). `src/diag_phase0.py` recomputes the frozen formation
statistic (warm mean-chromaticity L1 x1000, DIFFERENT iff >= 80) in Python and
reaches **720/720 judgment agreement** with the committed TSVs — the diagnosis
grounds on the exact frozen judgments.

## Error-mode breakdown (311/720 wrong; 56.81% formation accuracy)

| Mode | Count | % of errors | Definition |
|---|---|---|---|
| E1 illuminant-shift false-DIFFERENT | 245 | 78.8% | truth SAME_SURFACE, judged DIFFERENT |
| E2 missed real difference | 66 | 21.2% | truth DIFFERENT, judged SAME_SURFACE |

Truth base rates: SAME_SURFACE 346 / DIFFERENT 374.

### E1 — the dominant mode (245)
- **245/245** show a clear illuminant-shift signature: per-view mean
  channel-ratio spread (max_c mB_c/mA_c / min_c ...) > 1.25, median 1.86,
  max 10.9. The two views of the same surface were rendered under different
  illuminants (d65/warm/cool draw); the frozen rule has no illuminant
  discounting, so the chromaticity shift alone crosses the threshold.
- Dominant mean-chromaticity delta sign patterns (viewB minus viewA, x1000):
  (-,-,+) 105 (B bluer: cool-ward shift), (+,+,-) 84 (B redder: warm-ward),
  (-,+,+) 33, (+,-,-) 23 — i.e. warm/cool-ward shifts relative to d65.
- Margins: 97 errors are >150 units past the threshold; 89 in 60-150; 59 in
  20-60; **0 borderline** (<=20). No threshold move on the frozen statistic
  can recover E1 — the failure is structural, not calibration.
- **d65 implication:** YES, implicated — but at the formation layer. The
  d65/warm/cool illuminant handling the generator performs (exact Bradford
  diagonal in linear RGB) is precisely what the frozen formation rule fails
  to invert. This is disjoint from FS-E1b's CH-CCN-3 challenge-quantity
  repair (count>=4 threshold defect): formation is the first-pass percept
  judgment; the challenge layer is untouched by this crew.

### E2 — missed real differences (66)
- Frozen d in [10,79]; 19 borderline (within 20 of threshold 80), 33 in
  20-60, 14 in 60-150, 0 beyond. Only 9/66 show illuminant masking
  (spread > 1.25). Mostly genuinely similar crops / sub-threshold surface
  differences.

## Design path (all on the same 720 fixtures; details in evidence/diag/)

1. sRGB von Kries (gray-world per view + per-pixel chromaticity): 70.7-79.6%
2. Linear-space von Kries (LUT gamma inversion): 77.1-83.2%
   - residual SAME_SURFACE failures traced to degenerate channels
     (e.g. fixture 331: mean blue 0.6/255 — noise-amplified normalization)
3. **Ratio-dispersion (FINAL):** per-pixel per-channel linear ratio
   viewB/viewA is CONSTANT for same-crop pairs (diagonal illuminant model)
   regardless of illuminant values — no illuminant estimation needed.
   d = sum over channels of (n^2 * var(ratio) / mean(ratio)^2) x300;
   DIFFERENT iff d >= 44. **98.75% (711/720)**; rescues E1 243/245 (99.2%),
   E2 65/66 (98.5%). Residual 9: 7 dark/low-data DIFFERENT misses + 2
   heavy-clipping SAME_SURFACE false-DIFFERENT (fixtures 37: 93.5% pixels
   clipped; 534).

## Decision

Ship the ratio-dispersion rule (exact integer spec in PREREG_FS-F2C.md §2,
T = 44). The 85% bar is evaluated on a disjoint fresh 1200-draw (§4).
