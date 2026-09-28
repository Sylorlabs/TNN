# VERDICT V2-C — DEAD on RK-3 (preregistered); KD-1 FAILS by measurement

**Fork:** V2-C ("knowledge-first")  
**Date:** 2026-09-23  
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-C.md` (commit 61a6b87749f1c3bfae4dbe75424b3f033221cac4)

## Hypothesis (Micah's)
The R2-4 front-end was fooled because it lacked knowledge of the trap families. Teaching it proper attack-family knowledge (via vknow.zag detectors that cap confidence at 650 when trap signatures fire) will reduce adversarial wrong high-confidence judgments.

## Result
**DEAD on RK-3** (preregistered expectation: RK-3 ≈9.4%).

**KD-1: FAIL** — Adversarial wrong-HC projected 740 vs ≤537 required.

## KD-1 Measurement (Python simulation)
Baseline adversarial wrong-HC: 1,075
- PTC-2: 400, CCN-1: 335, COL-2: 313, CCN-2: 17, TMB-1: 6, harness: 4

K-CCN-1 detector (per-panel ratio>5 + bright<85):
- Recall on CCN-1 wrong-HC: 335/335 = 100%
- Clean fire rate: 3%
- Caps 335 → remaining 740 > 537 → **KD-1 FAIL**

## Interpretation
The CCN-1 detector works perfectly, but PTC-2 (pitch glide) and COL-2 (illuminant drift) defeat simple threshold-based detectors:
- PTC-2: ZC-rate and period-ratio distributions overlap clean (glide is within-tone, not cross-tone).
- COL-2: Left/right chromaticity differences overlap clean cases.

**For Micah:** Knowledge of the trap helps where the signature is detectable (extreme illuminants: 31% reduction), but the glide/drift families need structural front-end changes (endpoint-vs-dwell measurement for PTC-2; stronger illuminant normalization for COL-2), not just threshold detectors. The "knowledge gap" hypothesis is partially supported but insufficient alone.

## Implementation Status
- `src/memgate.zag`: byte-identical to R2-4 (SHA f7fa8db127b0def8f481c66b86f78b719ae26b4d0a6e549a9f82fc15566e9774) ✓
- `src/vknow.zag`: pure-Zag detectors (K-CCN-1 validated, others stubbed). Compiles cleanly. ✓
- `src/vsense_c.zag`: **NOT BUILT** — integration deferred because KD-1 fails even with perfect CCN-1 detection. The limiting factor is PTC-2/COL-2 detector design, not the Zag implementation.
- `evidence/KD1_SIMULATION.md`: full simulation results.

## Evidence
- `evidence/KD1_SIMULATION.md` — Python simulation of KD-1
- `evidence/VERDICT_V2-C.md` — this file
- Source: `src/vknow.zag`, `src/memgate.zag` (byte-identical)
