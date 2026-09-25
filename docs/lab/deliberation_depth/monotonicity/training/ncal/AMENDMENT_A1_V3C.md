# AMENDMENT A1 (pre-implementation) — PREREG_NCAL_V3C_B13FIX_FROZEN.md §3.4

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN. Amends the v3c prereg (commit
  `567b399f`) BEFORE any implementation or scored run. No other section changes.

## §3.4 Design D (diagnostic, s1-only) — seed expiry [CORRECTED MECHANISM]

The frozen text ("latch seeded at d1prior-equivalent 0.95 as m20") was confused:
a design with no latch has no latch to seed. The corrected mechanism:

- tp=0: conf = schema seed (identical lookup to S, §3.1, min_n=1). Emitted.
- tp≥1: conf = p_raw (the item's direct personal correctness rate, cp/tp) with NO
  minimum latch of any kind. The seed is not retained.
- Everything else (nopool=1, traces, determinism) identical to S.

Predicted (pre-registered): per-item confidence rises wherever p_raw exceeds the tp=0
seed (mixed cells), producing strict G rises on some family×depth → B3 Gviol > 2
(m20's 2) → B3-kill. Purpose: empirically confirm the §2 lemma's B3 half
(any post-seed rise breaks B3). s1 matrix only; not adoption-eligible.

Reason for amendment: the original §3.4 described a hybrid that would have produced a
confidence FALL (0.95 latch under a 1.0 seed), not the rise the diagnostic is meant to test.
Caught on re-read before implementation; no runs exist.
