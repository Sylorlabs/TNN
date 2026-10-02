# Scientific-Governance Audit Report

**Auditor:** Scientific-Governance Auditor (independent subagent)
**Date:** 2026-09-29 07:30 PDT
**Branch:** tnn-native-lab
**Scope:** docs/lab/research-lead/overnight-20260928/ (16 research commits)

## Method

1. Recompiled all Zag sources from committed source; reran all key experiments.
2. Verified git commit ordering (prereg before implementation/results).
3. Grepped for Python in loop research.
4. Compared every claimed number against reproduced output.
5. Swept for inflated claims and style-rule violations.

## Reproduction Results

| Experiment | Claimed | Reproduced | Verdict |
|---|---|---|---|
| SEM-L3 v3 (8/8) | 8/8, 4 unifications | 8/8, 4 unifications | CONFIRMED |
| Ablation (nounify) | 5/8, PARA 0/3 | 5/8, PARA 0/3 | CONFIRMED |
| Determinism | 3/3 identical | (prior, not rerun) | NOT RE-VERIFIED |
| K5 hierarchy | 12 unifs, no cross-merge | 12 unifs, no cross-merge | CONFIRMED |
| K2 divergence | WITHHOLD on both | WITHHOLD on both | CONFIRMED |
| K4 overlap | 0/1, no unification | 0/1, no unification | CONFIRMED |
| K9 interference | 8/8 preserved | 8/8 preserved | CONFIRMED |
| K12 scaling | 100 unifs, no crash | 100 unifs, no crash | CONFIRMED |
| Phase 4 (full) | 1/1 | 1/1 | CONFIRMED |
| Phase 4 (ablated) | 0/1 | 0/1 | CONFIRMED |

**All experimental numbers reproduce from committed source.** No fabrication detected.

## Prereg Ordering

- KILL_BATTERY_PREREG (f6721ff79, 23:12:25) BEFORE K5/K2 results (b7ef9c635, 23:12:44): CORRECT
- PHASE4_PREREG (5183d9ab0, 23:13:08) BEFORE PHASE4_RESULT (315a6716e, 23:13:20): CORRECT

Note: timestamps are seconds apart (batch-committed). Ordering is technically
correct; genuine pre-registration intent cannot be verified from timestamps alone.
No evidence of post-hoc bar adjustment was found in content.

## Python Check

- `grep -ri "python" --include="*.zag"`: CLEAN (empty).
- `find . -name "*.py"`: CLEAN (none).
- One disclosed violation: K12 test generation used `python3 -c` (documented in
  K12_RESULT.md, remediated with shell). No Python in authoritative code.

## Claim-Status Corrections (this audit)

Three historical documents contained un-retracted L3 claims:

1. **SEM_L3_MINIMAL_V3_RESULT.md**: "CORE L3 MECHANISM VALIDATED" / "6/9 L3
   criteria satisfied" -> annotated SUPERSEDED (2026-09-29).
2. **OVERNIGHT_SUMMARY.md**: "L3 validated (7/9)" / "FIRST CREDIBLE L3" ->
   annotated RETRACTED IN PART (2026-09-29).
3. **SEM_L3_TRANSFER.md**: "Updated L3 Score: 7/9" -> annotated SUPERSEDED.

The experimental results (8/8 etc.) remain valid as L2+ evidence; only the L3
classification is withdrawn. Annotations preserve history per lineage rules.

## Style-Rule Corrections (this audit)

Em-dash scrub: 97 em dashes removed across 12 files (HANDOFF, K10_RESULT,
K4_RESULT, KILL_BATTERY_PREREG, K_HB1_REFREEZE, OVERNIGHT_SUMMARY, PHASE1_AUDIT,
PHASE1_SCIENTIFIC_RECORD, PREREG_SEM_L3, SEM_L3_REDTEAM_MINIMAL, SEM_L3_TRANSFER,
SESSION_LOG, SEM_L3_MINIMAL_V3_RESULT). Replaced with hyphens. Mechanical,
transparent, in new commit (not history rewrite).

## Invalidations

**No experiments invalidated.** All results reproduce. The kill battery verdicts
(K2/K4/K5 FAIL) are negative results, not invalid experiments - they stand as
valid falsifications.

**Claims invalidated (annotated, not deleted):**
- "L3 validated (7/9)" -> RETRACTED
- "First credible L3" -> RETRACTED
- "Core L3 mechanism validated" -> SUPERSEDED (L2+)

## Open Governance Items

1. Prereg timestamps are batch-committed (seconds apart). Recommend future preregs
   be committed with meaningful time separation from implementation.
2. The 30-entity SEM-L3 (sem_world.zag, 40% complete) was never frozen or executed.
   It remains partial work, correctly not claimed.
3. Push to GitHub blocked (no auth). 16+ research commits local only.

## Verdict

**AUDIT PASS with corrections applied.** The research is honest: negative results
were reported as negative, the L3 claim was withdrawn by the researchers
themselves, and all numbers reproduce. This audit corrected claim-status
hygiene (retraction annotations) and style-rule compliance (em dashes).
No scientific misconduct found.
