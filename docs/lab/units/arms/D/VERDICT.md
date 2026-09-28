# Arm D — Verdict (DRAFT)

## Status: IN PROGRESS (2026-09-21)

### Mechanism
Self-cut byte span + stable ID (Micah's flagship hypothesis).
Family: CUT+IDENT.

### Frozen Spec Status
**PROVISIONAL-PENDING-FREEZE**: The frozen prereg (PREREG_FREEZE.md:479) names
`REP_BAR` but supplies no numeric value. Default `REP_BAR=4` used for all runs
below unless noted. Sensitivity 3 vs 4 required.

### Kill Criteria (from brief D.json)
Any one kills:
1. Stored bytes per recall ≥ B-64 on both corpora at 10x.
2. Churn > 0.30 at 10x.
3. M1 < B-64 at equal memory budget.

**If D dies, the program thesis dies with it.**

### Results

#### M1 (1x)
- [PENDING] m1-1x-prose
- [PENDING] m1-1x-code

#### M1 (10x)
- [PENDING] m1-10x-prose
- [PENDING] m1-10x-code

#### M2 (1x)
- m2-t1-prose: 1 episode, 100.0/100.0, fast-then-flat ✅
- m2-t3-1x: 1 episode, 100.0/100.0 ✅
- [PENDING] m2-t1-code, m2-t2-prose, m2-t2-code

#### M3-M9 (1x)
- [PENDING]

### REP_BAR Sensitivity
- [PENDING] 3 vs 4 head-to-head

### Determinism
- [PENDING] Double runs, byte-identical stdout verification

### Verdict
**TBD** — awaiting complete evidence.
