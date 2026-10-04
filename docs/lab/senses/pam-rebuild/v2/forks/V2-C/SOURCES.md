# V2-C Sources — Build Manifest

**Fork:** V2-C (knowledge-first) | **Date:** 2026-09-23

## src/
| File | SHA256 | Provenance | Builds |
|------|--------|------------|--------|
| memgate.zag | f7fa8db1…c15566e9774 | Byte-identical to R2-4 `memgate.zag` (frozen gate) | Yes (`znc memgate.zag`) |
| vknow.zag | 5bd506be…7c67372 | Fork's attack-family detectors (K-CCN-1 validated; K-CCN-2, K-PTC-1, K-TMB-1 stubbed) | Library (no main; imported by vsense_c.zag) |
| R33_NATIVE_IO_V1.zag | e6379ddb…641e9f61d8 | Vendored byte-identical from R2-4 (memgate.zag imports it) | Yes (substrate) |
| R33_NATIVE_SHA256_V2.zag | 9824f6db…7ca683bcf | Vendored byte-identical from R2-4 (memgate.zag imports it) | Yes (substrate) |

**DEFERRED: `src/vsense_c.zag` (front-end + vknow integration).** Reason:
KD-1 FAILS by measurement (740 vs ≤537) even with a perfect K-CCN-1 detector —
the limiting factor is PTC-2/COL-2 detector design (simple thresholds overlap
clean distributions), not the Zag integration. Building the integration would
not change the verdict. Documented in VERDICT_V2-C.md.

## evidence/
- VERDICT_V2-C.md (DEAD on RK-3; KD-1 FAIL by measurement)
- KD1_SIMULATION.md (Python simulation: baseline 1,075 → 740 after K-CCN-1 caps)

## Note for red-team
V2-C's attack surface is the K-CCN-1 detector logic (per-panel channel ratio
>5 + brightness <85 → cap at 650) and the memgate (R2-4's gate, already
frozen). The novel families target F/G agreement; V2-C's memgate is
R2-4's, so its exposure is R2-4's exposure.
