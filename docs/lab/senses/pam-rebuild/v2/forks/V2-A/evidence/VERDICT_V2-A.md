# VERDICT V2-A — DEAD on RK-3

**Fork:** V2-A ("adjudicator")  
**Date:** 2026-09-23  
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-A.md` (commit 673cd3d1722ae3f997aa039a2a74ae58fe9430b4)

## Hypothesis
Unchanged H2-style gate plus conflict-only independent-evidence adjudication; REVISE_INSTALL only for independently verified CONFLICT_WITHHELD.

## Result
**DEAD on RK-3.**

| Bar | Result | Threshold | Verdict |
|-----|--------|-----------|---------|
| RK-1 (false installs ≤3%) | 0.01% | ≤3% | PASS |
| RK-2 (wrong-HC permanent ≤1%) | 0.09% | ≤1% | PASS |
| RK-3 (correct-HC PASS-install ≥85%) | **65.88%** | ≥85% | **FAIL** |
| RK-5 (wrong-HC → FAIL/UNRESOLVED ≥90%) | 99.37% | ≥90% | PASS |
| B5 (adversarial false ≤3%) | 0.00% | ≤3% | PASS |
| B6 (byte-identical ×3) | 1 unique SHA | — | PASS |
| B1 (frozen-370 ≥60%) | 87.30% | ≥60% | PASS |

## Interpretation
V2-A preserves near-zero false installs (RK-1 0.01%, B5 0.00%) but only installs 65.88% of correct high-confidence judgments — well below the 85% bar. The conflict-only adjudication (268 REVISE_INSTALL) does not lift the install rate enough.

This matches the preregistered prediction (RK-3 ≈66%, death). The H2-style gate with adjudication is safe but too conservative for the ACCEPT TRUTHS target.

## Evidence
- `evidence/RUN_DIGESTS.md` — three byte-identical runs (B6)
- `evidence/metrics.json` — frozen bar results
- `evidence/LEDGER_VERIFICATION.md` — hash chain verification (to be added)
- `evidence/RUNLOG.md` — run log (to be added)
- Source: `src/vgate_a.zag`, `src/vsense.zag` (byte-identical to R2-4)
