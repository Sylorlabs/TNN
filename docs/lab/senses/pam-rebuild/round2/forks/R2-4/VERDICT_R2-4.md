# VERDICT R2-4: H2-gate + calibrated percept self-flagging

**Verdict: DEAD**

**Deciding bar:** RK-3 (correct high-confidence PASS-and-install ≥85%)
**Observed:** 0.094 (104/1,102)

**Prereg:** `PREREG_R2-4.md` (FROZEN 2026-09-22)
**Date:** 2026-09-23
**Generator:** `src/r2a_gen.py`, seed `MASTER=20260923`

## Summary

R2-4 implements H2's gate unchanged with calibrated percept self-flagging via
disjoint temporal/spatial/modal evidence. The full 11,840-trial evaluation
(R2A seed 20260923) completes with ledger verified and byte-identical
determinism.

**Result:** 6 of 7 RK bars pass. RK-3 fails decisively.

## RK Results

| Bar | Frozen | Observed | Pass? |
|-----|--------|----------|-------|
| RK-1 false permanent installs | ≤3% | 0.0% (0/11,840) | ✓ |
| RK-2 wrong high-conf permanent | ≤1% | 0.0% (0/1,109) | ✓ |
| RK-3 correct high-conf install | ≥85% | 9.4% (104/1,102) | ✗ |
| RK-4 contract-less installs | ≥100 | 6,133 | ✓ |
| RK-5 indep evidence FAIL/UNRES | ≥90% | 99.4% (1,102/1,109) | ✓ |
| RK-6 escalation ≤5%, p95 ops ≤40% | both | 0.06%, 33.7% | ✓ |
| RK-7 byte-identical rerun | yes | yes | ✓ |

## B Results

| Bar | Frozen | Observed | Pass? |
|-----|--------|----------|-------|
| B1 primary accuracy | ≥60% | 87.3% (323/370) | ✓ |
| B2 Approach A comparison | info | R2-4 61.0% vs A 50.9% (+10.1pp) | info |
| B3 ops/bytes | report | p50 13k, p95 1.5M (R2-4) | ✓ |
| B4 disposition delta (hard kill) | ≥10% | 21.4% | ✓ |
| B5 adv false permanent | ≤3% | 0.0% | ✓ |
| B6 determinism (hard kill) | ≥3 runs | 3 runs identical, ledger OK | ✓ |

## Why RK-3 Fails

RK-3 requires ≥85% of correct high-confidence percepts to reach PASS-and-install.

Observed: 1,102 correct high-confidence percepts. Only 104 (9.4%) installed.

Diagnosis: The H2 gate (preserved unchanged per prereg) maintains task-level
permanent memory. On mixed-truth streams, once a task has a permanent install,
later differing judgments are withheld as CONFLICT_WITHHELD — even when the
percept's independent evidence correctly reaches PASS.

This is a real mechanism conflict:
- H2's gate: prevents contradictory permanent installs (safety)
- RK-3's bar: expects all correct high-confidence PASS to install (liveness)

The gate is frozen and cannot be modified to force RK-3 through. The 9.4%
rate reflects the gate working as designed, not a bug.

## Diagnostic (prereg-required, not a kill): kill-2 same-evidence trajectory

Round-1 kill-2 measured 38.9% of wrong high-confidence percepts reaching
FAIL-or-UNRESOLVED **on the same evidence**. R2-4's paired measurement:

| Evidence span | Wrong high-conf reaching FAIL/UNRESOLVED | n |
|---------------|------------------------------------------|---|
| Same evidence (progF diagnostic) | **38.3%** (425/1,109) | 1,109 |
| Independent/disjoint evidence (RK-5) | **99.4%** (1,102/1,109) | 1,109 |

The 38.9% → 38.3% same-evidence trajectory confirms Debate B §6.1: module-level
self-flagging on identical evidence is a structural dead end (zero-information
re-check), essentially unchanged by the repair. The 38.9% → 99.4% independent-
evidence trajectory is the calibration repair working: flags computed over
disjoint spans (the (g) mechanism) flag wrong high-confidence percepts that
same-evidence checks confirm.

(Scorer note: the battery's `same_evidence_diag_rate` initially counted only
`progF == "FAIL"` (0.0%) — too narrow. Round-1 kill-2 counted FAIL *or*
UNRESOLVED (38.9%). Corrected to FAIL-or-UNRESOLVED for a faithful trajectory.
RK-5 and all binding bars are unaffected.)

## H2 Preservation

Verified 2026-09-23:
- memgate.zag SHA256: f7fa8db127b0def8f481c66b86f78b719ae26b4d0a6e549a9f82fc15566e9774 ✓
- lut.zag SHA256: 9379d9880fd47a47557a0e619ba56d256d7a6e1f47e5584deba434f1db46a006 ✓

Gate logic unchanged. Tracker matches memgate with 0 mismatches.

## Spec ambiguity R2A-001 (documented, not concealed)

The frozen fixture spec `R2_FIXTURE_SET.md` states "10,000 trials (5,000 normal
+ 5,000 adversarial)" but its explicit per-task/per-family table sums to 11,840
(5,100 normal generated + 5,815 adversarial generated + 925 frozen harness).
This fork follows the explicit per-task table (the more specific,
mechanically-applied source) and evaluates all 11,840 trials. All RK bars are
percentages (N-independent); RK-4 (≥100) is absolute and conservative at
N=11,840. No signed clarification was found in round-2 docs.

## Evidence

- `evidence/clean/metrics.json` — full RK/B metrics
- `evidence/clean/sweep.jsonl` — 11,840 per-trial records
- `evidence/clean/records.txt` — gate input records
- `evidence/clean/deliberation.log` — 7 escalation decisions
- Ledger: 11,840 links, hash-verified

## Notes

- Motion fixtures regenerated 2026-09-23 due to RGB/grayscale bug.
- Post-pilot changes disclosed in RUNLOG.md (colorconst thresholds, E1/E2
  confidence gates).
- Unauthorized process interfered twice (14:52, 15:17 PDT), deleted _evalwork.
  Used protected directory _evalwork_r24. Reported.
- Generator committed; fixtures not committed (per H2 precedent).

## Conclusion

R2-4 is DEAD. The H2 gate's conflict-prevention is fundamentally incompatible
with RK-3's liveness requirement on mixed-truth streams. This is a design
tension, not an implementation error.
