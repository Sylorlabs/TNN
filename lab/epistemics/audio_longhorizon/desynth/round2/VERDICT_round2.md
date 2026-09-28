# Audio De-synth Round 2 — Verdict

**Date:** 2026-09-27
**Base:** closure commit 8fe78063e655 (mean err_pm 775→425, 20/20 byte-identical)
**Task:** Attack 4 residuals with broad mechanism-level fixes.

## Summary

| Residual | Mechanism found | Fix | Measured effect | Ship? |
|----------|----------------|-----|-----------------|-------|
| D2: 0.59× contour mean | Command-corruption × hearing-failure: 16-pt CON carries octave spikes → verbatim render sweeps >100 Hz/frame → YIN drops frames → heard mean collapses to clean portion | render_plan winsorize (median/4–4× band) + fr clamp | t17: 381→525, t1: 0→500 (NET HARMFUL) | NO |
| t8/t12/t14 regressions | Dishonest contour-action predictions: shootout/consult predict from flat-probe CALIB bias (fantasy) ignoring measured probe bias; "cvt=0 by construction" hides CV shortfalls | 3-part: honest shootout + consult VOCAB@64 + rescale measured bias | Mean 425→380.5; t8 816→500, t12 172→0, BUT t14 146→513, t11 80→588 | NO (regressions) |
| t17 octave outliers | 17/109 frames are 3rd–9th harmonic captures (verified organ error); body median 144.4 Hz (laryngograph 130.3 not reproducible) | Cross-frame suppressor (quorum + harmonic-consistency + isolation gates) | Fires on legitimate rises (t1); small benefit (148.5→146.4), destructive side effects | NO |
| Extractor NBINS crash | NBINS=round(sr/f0); texture step zero-pads into fixed 256-sample buffer; F0<171.9 Hz → NBINS>256 → broadcast crash | Adaptive spectral grid (256 if fits, else next pow2) | 11/11 byte-identical on existing atoms; works to 80 Hz | YES |

## Shipped

**Extractor fix** (`round2/extract_atom_v2.py`):
- Root cause: `NBINS = round(sr/f0)` is the F0-determined period length; the texture-shaping step does `h_padded[:NBINS] = harm` into a fixed 256-sample FFT buffer. At 44.1 kHz, F0 ≲ 171.9 Hz → NBINS > 256 → `ValueError: could not broadcast input array from shape (551,) into shape (256,)`. Reproduced at 80/140 Hz.
- Fix: adaptive spectral grid — 256 when NBINS ≤ 256 (bit-identical ops), else next power of two ≥ NBINS; texture segment zero-padded to common grid, inverse-transformed, truncated to TEXLEN. Atom binary format untouched.
- Verification: 11/11 byte-identical (4 Wall-3 atoms direct, atom0, atom1, NBINS=256 boundary, 4 additional sources). Valid atoms at 80/90/120/140/160/170/171/200 Hz. Deterministic.
- See `ANALYSIS_extractor.md`, `RESULTS_extractor.md`, `extract_atom_v2.patch`.

## Not shipped (honest residuals)

**D2 (w1):** The 0.59× is NOT a renderer math defect — period placement is exact (flat 220 Hz renders hear at 220.45 Hz). It's a command-corruption × hearing-failure interaction. The winsorize fix is mechanism-correct but the scoreboard's cv term (+500) penalizes the cleaned render, and it flattens legitimate rises (t1: 0→500). The fix needs a cv-term rethink before shipping.

**t8/t12/t14 (w2):** The shared mechanism is real (dishonest contour predictions). The 3-part fix improves the mean (425→380.5) and fixes t8/t12, but regresses t14 (+367) and t11 (+508). The probe bias doesn't generalize to all contours. Needs refinement.

**Octave outliers (w3):** The suppressor is well-designed (quorum + harmonic + isolation gates) but fires on legitimate high-F0 content (t1's rise, t05's alternation). The honest ceiling is ~144 Hz, not 130 Hz (laryngograph not reproducible). Benefit too small for the risk. Proven: cannot be safely fixed without altering the frozen organ at the current design.

## Validation

- Frozen organ byte-identical (not modified).
- Extractor: deterministic, 11/11 byte-identical.
- Planner: NO changes shipped (closure binary unchanged).
- Full 20-target batteries run for w2-only (mean 380.5) and integrated (mean 457.75, regressed — NOT shipped).

## Remaining residuals

1. D2: needs cv-term redesign to not penalize glitch removal.
2. t8/t12/t14: w2's honest-prediction mechanism needs probe-generalization fix for t14/t11.
3. t17 octaves: unfixable at planner level without organ changes (proven).
4. Extractor: CLOSED.
