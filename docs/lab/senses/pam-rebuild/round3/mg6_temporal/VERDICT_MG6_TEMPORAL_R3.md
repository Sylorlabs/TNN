# VERDICT — MG6 Temporal-Arm Recalibration, Round 3 (Crew 2)

## Verdicts

- **T0** (original Δseq ≥20): KILL — 0 false, 0/34 retention, CC1 0/9 + 5/5.
- **T1** (temporal arm removed; margin+span retained): KILL — 0 false, 2/34 retention, CC1 0/9 + 5/5.
- **T2lo** (Δseq ≥2): KILL — 1 false (D1 idx 19), 2/34 retention, CC1 0/9 + 5/5.
- **T2hi** (Δseq ≥6): KILL — 1 false (D1 idx 19), 0/34 retention, CC1 0/9 + 5/5.
- **T3** (same-task/same-judgment seq range ≥20): KILL — 0 false, 1/34 retention, CC1 0/9 + 5/5.
- **T4** (≥3 same-task/same-judgment historical seqs): KILL — 1 false (D1 idx 22), 2/34 retention, CC1 0/9 + 0/5 throughput.

## Summary

**All six temporal-arm candidates are KILLED. Retention was not recovered.**

The best local tradeoff is **T1** (remove the temporal arm, keep margin+span):
safety preserved (0 false installs), CC1 throughput preserved (5/5), but retention
only 2/34 against the ≥26/34 bar. It is still KILL per the frozen bar.

## Structural finding (preregistered)

The retention bottleneck is **not** the temporal arm. Under G1, only 4 of the 34
true D1 candidates ever reach the guard; with an allow-all guard the complete
stack retains only 3/34. Therefore **no guard-only or temporal-only change can
meet ≥26/34**. Recovery requires retuning G1 proposal formation and re-anchoring
— a gate-level change outside this crew's temporal-arm scope.

The guard is not abandoned: the margin arm is proven (KB-R3c passes for T0–T3,
0/9 false installs on CC1 throughout). T4 is additionally unsafe: its false
install resets gate state and preempts later proposals, breaking CC1 throughput
(0/5).

## Evidence

- Prereg (alone): `9644a1cf44749da0f6aa8a53c6c01b939a4141ae`
- Build/verdict: see commit SHA in parent report.
- D1 battery: 3× byte-identical (sha256 b6dca786…), 4,548/4,548 vs EXPECT_R3.tsv.
- CC1 battery: 3× byte-identical (sha256 97cd43de…), 474/474 vs EXPECT_R3_CC1.tsv.
- Pure Zag, zero randomness, pinned toolchain.
- Runlog: RUNLOG_MG6_TEMPORAL_R3.md.
