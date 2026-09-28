# FORMAL-LEG SPEC EXTRACT — R-3 / R-4 / R-5
# Extracted programmatically from units/PREREG_FREEZE.md (frozen, Micah signed 2026-09-21)
# Extraction date: 2026-09-21. No transcription; verbatim sed ranges below.

## §0 I — R31 redo track sign-off items (verbatim, lines 321-325):
  range); compression-term cap/weighting so grounding dominates. Approve.
- **R-3** Dual≈raw tolerance ε (B-T2) + minimum compression ratio the dual route must add.
  Approve both.
- **R-4** Dose-curve bar: flatness/degradation tolerance across 250 → 8000. Approve.
- **R-5** Support-gap floor: minimum hard-battery score across 1–16 exposures. Approve.

## §2 R0.2 replication-fidelity bars (verbatim, lines 399-413):
### R0.2 Replication-fidelity bars (qualitative orderings — pass/fail)

- **B-T1 Tournament:** `predictive_surprise > fixed_window > raw_micro`, raw_micro (no
  chunking) **dead last**. (Full reference ordering, REFERENCE_ONLY:
  predictive_surprise ≫ random_chunks ≈ fixed_window_4 > MDL variants > raw_micro.)
- **B-T2 Ablation:** `dual_route ≈ raw_active` on hard grounding (within tolerance ε,
  R-3) **while adding compression** (minimum ratio, R-3); **chunk-only is rejected**
  (must lose to dual/raw on hard grounding).
- **B-T3 Dose curve:** flat or non-decreasing across 250 → 8000; no degradation
  (tolerance, R-4).
- **B-T4 Support-gap:** hard-battery score at or above floor (R-5) across 1–16 exposures;
  no collapse at 1 exposure.
- **B-T5 Dynamics:** split/merge fire under recovered conditions and are auditable; exact
  counts are REFERENCE_ONLY.


## §2 R0.1 run rules (verbatim, from R0.1 scope tail):
396:All five run at **1x first; 10x only after the 1x replication bars pass** (R-9). Pure Zag,
All five run at **1x first; 10x only after the 1x replication bars pass** (R-9). Pure Zag,
zero RNG in AI decision paths, N=5 + adversarial perturbations hard gate.
