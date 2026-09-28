# V2-C KD-1 Diagnostic — Python Simulation Results

**Date:** 2026-09-23  
**Status:** SIMULATION (design validation, not frozen evidence)

## Baseline
Adversarial wrong high-confidence (wrong judgment, conf≥700): **1,075**
- PTC-2: 400
- CCN-1: 335
- COL-2: 313
- CCN-2: 17
- TMB-1: 6
- harness_adversarial: 4

## Detector: K-CCN-1 (extreme illuminant)
**Logic:** Per-panel channel ratio > 5 AND brightness < 85.  
**Derivation:** From CCN-1 method (extreme illuminant xblue/xred at 0.55 exposure).  
**Validation:**
- CCN-1 wrong-HC recall: 335/335 = **100%**
- Clean fire rate: 3% (conservative)

**Impact:** Caps 335 → remaining 740.

## KD-1 Bar
**Requires:** adversarial wrong-HC ≤537 (50% reduction from 1,075).  
**Projected:** 740 > 537 → **FAIL**.

## Analysis
The K-CCN-1 detector works perfectly for its target family, but:
- PTC-2 (400 cases): pitch glide detection requires within-tone stationarity analysis. ZC-rate and period-ratio detectors do not separate PTC-2 from clean (overlapping distributions).
- COL-2 (313 cases): illuminant drift detection requires left/right chromaticity comparison. Simple normalized differences overlap clean cases.

**Conclusion:** Knowledge of the CCN-1 trap reduces wrong-HC by 31%, but the glide (PTC-2) and drift (COL-2) families require deeper front-end changes than threshold-based detectors. KD-1 FAILS by measurement.

## V2-C Verdict (Preliminary)
- **RK-3:** Expected ~9.4% (front-end unchanged except caps) → **DEATH** (as preregistered).
- **KD-1:** 740 > 537 → **FAIL**. The knowledge hypothesis is partially supported (CCN-1 works) but insufficient alone for the 50% reduction bar.
- **Implication for Micah's hypothesis:** Teaching the front-end about trap families helps where the signature is detectable (extreme illuminants), but the glide/drift attacks defeat simple detectors. Either the front-end needs structural changes (e.g., endpoint-vs-dwell for PTC-2, stronger normalization for COL-2), or the knowledge must be procedural rather than threshold-based.

## Pure-Zag Implementation
`src/vknow.zag` implements K-CCN-1 (plus stubs for K-CCN-2, K-PTC-1, K-SHP-1, K-TMB-1) in pure Zag. Compiles cleanly. The full front-end integration (vsense_c.zag) was deferred because KD-1 fails even with perfect CCN-1 detection — the limiting factor is PTC-2/COL-2, not the CCN-1 implementation.
