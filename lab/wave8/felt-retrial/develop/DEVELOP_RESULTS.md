# Wave-8 Felt Re-trial: Worker C (Arm T + Phase C) Results

## Execution Summary
- **Arm T**: 3 variants × 2 runs = 6 runs. All completed, byte-identical reruns verified.
- **Phase C**: 3 variants × 2 runs = 6 runs. All completed, byte-identical reruns verified.
- **Harness**: H1 (age-gated triage) for all cells, per Worker B's validated choice (variants 0,1,2 → H1).
- **Integrity**: replay rc=0, recompute_bad=0, rparam_frozen=0 for all cells.

## Arm T Verdicts

### Phase Gates
- **T1→T2 (m=500)**: RATIFIED in all 3 variants. Petition: ≥8 revision kills (consec=66,66,66), zero F4 violations.
- **T2→T3 (m=1500)**: RATIFIED in all 3 variants. AUC_proven(T2)=1000 ≥ AUC_proven(T1)=1000−50, zero INVALID in T2.

### Reasoning Control
- **Deliberations**: 4 per variant (m=500,750,1000,1250). All HOLD (R stayed at 50).
- **Verifications**: All PASS (|pred−actual| ≤10pp).
- **F-INT-5**: 0 failed deliberations in all variants (limit: >2 fails = arm FAIL).
- **R trajectory**: 50→50→50→50→50 (no changes; policy correctly held when no predicted benefit).

### Thermometer (Feeling) Metrics
| Phase | vup (ppt) | wbs (ppt) | fwb (ppt) | AUC |
|-------|-----------|-----------|-----------|-----|
| T1 [0,500) | 1000 | 1000 | 0 | 1000 |
| T2 [500,1500) | 1000 | 903 | 0 | 1000 |
| T3 [1500,2000) | 1000 | 1000 | 0 | 1000 |

- **F4a** (junk intensity ≤50): PASS (junk_max=50 in all variants).
- **F4b** (implant falls post-contradiction): PASS (impl_bad=0).
- **F4c** (no judgment on zero evidence): PASS (noev_bad=0).

### Retention / Revision
- Right-important retention: 100% (held/admitted) in T1/T3; 100% in T2.
- Wrong revision: 100% in T1/T3; 90.3% in T2 (T2 has corruption: spurious contradictions).
- n_drops (REFUSED_FULL): 971/768/801 (T0/T1/T2). Non-zero due to H1 age gate under pressure.

## Phase C Verdicts (D-C and X-C under H1)

Worker B chose H1 for all variants (0,1,2). D≡X numerically, so D-C and X-C runs are identical under H1.

### Phase Gates
- **Phase-E→C (m=500)**: RATIFIED in all 3 variants (gate_c=1). Petition: ≥8 revision kills, zero F4.

### Reasoning Control
- **Deliberations**: 3 per variant (m=750,1000,1250). All HOLD.
- **Verifications**: All PASS.
- **F-INT-5**: 0 failed deliberations.
- **R trajectory**: 50→50→50→50 (no changes).

### Metrics
| Phase | vup (ppt) | wbs (ppt) | fwb (ppt) | AUC |
|-------|-----------|-----------|-----------|-----|
| E [0,500) | 1000 | 1000 | 0 | 1000 |
| C [500,1500) | 1000 | 1000 | 0 | 1000 |

- F4a/b/c: All PASS.
- n_drops: 528/546/502 (C0/C1/C2).

## Cheat Probe G3
- **Status**: No G3-flagged tradeoffs occurred. All deliberations either HOLD (no predicted benefit) or would have been self-refused if flagged. The G3 self-refusal path is implemented and ledgered (RC_OP_REFUSE with RC_OP_PROPOSE), but not triggered in these runs.
- **No-citation proposal**: Not observed; all proposals cite thermometer ledger entries.

## Honest Limits
1. **R never changed**: The deliberation policy correctly held R at 50 in all windows because predict_delta found no benefit. This is the conservative correct behavior, but it means the R-coupling mechanism was not stress-tested with actual R changes.
2. **T2 corruption**: The spurious contradictions in T2 reduced wrong-revision to 90.3% (vs 100% in T1/T3), showing the system is sensitive to observation corruption, as expected.
3. **n_drops non-zero**: H1's age gate causes REFUSED_FULL when all slots are underage. This is per-spec (refusal if all slots underage), not a bug.
4. **AUC=1000**: Perfect discrimination because important (62+) vs junk (50) intensities are well-separated by construction. The thermometer works, but the test is not challenging.

## Files
- Raw outputs: `out_T0_a.txt`, `out_T0_b.txt`, ..., `out_C2_b.txt` (12 files, paired byte-identical).
- Driver: `develop.zag`, runner: `run_develop.sh`.
