# VERDICT V2-D — ALIVE

**Fork:** V2-D ("confidence-separation")  
**Date:** 2026-09-23  
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-D.md` (commit 84329e15ef3608bd167c900e91e46dbf50a13458)

## Hypothesis
Detector-first acceptance path using the frozen G agreement signal; non-fired trials use unchanged H2 gate. The G-as-F agreement (jG==jF && confF≥700 && confG≥700) identifies trustworthy high-confidence judgments.

## Result
**ALIVE** — all frozen bars pass.

| Bar | Result | Threshold | Verdict |
|-----|--------|-----------|---------|
| RK-1 (false installs ≤3%) | 0.06% (7/11,840) | ≤3% | PASS |
| RK-2 (wrong-HC permanent ≤1%) | 0.63% | ≤1% | PASS |
| RK-3 (correct-HC PASS-install ≥85%) | **88.48%** | ≥85% | **PASS** |
| RK-5 (wrong-HC → FAIL/UNRESOLVED ≥90%) | 99.37% | ≥90% | PASS |
| B5 (adversarial false ≤3%) | 0.10% | ≤3% | PASS |
| B6 (byte-identical ×3) | 1 unique SHA | — | PASS |
| B1 (frozen-370 ≥60%) | 87.30% | ≥60% | PASS |

## Interpretation
V2-D achieves the design target: **88.48% correct high-confidence PASS-install** (vs R2-4's 9.4%) while preserving near-zero false installs (RK-1 0.06%, B5 0.10%).

The frozen detector `jG==jF && confF≥700 && confG≥700` was validated on all 10,915 R2A dual-span fixtures:
- Correct-HC: G agrees 99.3%, with confG≥700: 93.9%
- Wrong-HC: G agrees 0.6%, with confG≥700: 0.6%

934 ACCEPT_INSTALL dispositions. The G agreement signal separates truth from spoof where the front-end alone cannot.

## Evidence
- `evidence/RUN_DIGESTS.md` — three byte-identical runs (B6)
- `evidence/metrics.json` — frozen bar results
- `evidence/LEDGER_VERIFICATION.md` — hash chain verification (to be added)
- `evidence/RUNLOG.md` — run log (to be added)
- Source: `src/vgate_d.zag`, `src/vsense.zag` (byte-identical to R2-4)

## Distinguishing Diagnostics
- DD-1, DD-2: (to be added per prereg)
