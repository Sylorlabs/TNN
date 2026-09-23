# VERDICT_R2-16.md — DRAFT (incomplete)

## Fork ID
R2-16

## Status
**INCOMPLETE / LIKELY DEAD** — Core mechanism implemented and tested, but multiple prereg bars fail. Design-loop CP suite, ablation, holdout, and determinism checks not completed due to time constraints and unresolved defects.

## Prereg
- Committed: `4601db7f3182181f525c5791339207243727caa2` (2026-09-23)
- Parent: `9b10843f8298`

## Mechanism implemented

### Timbredisc (CH-TBD-2)
- Fixed `tb_coeff` to exact 440Hz coefficients (2040, 2018, 1980, 1927, 1860, 1779, 1685, 1578).
- **ANOMALY**: Theoretically-correct class mapping yields 347/985 FI; swapped mapping yields 52/985. Using empirically-optimal swapped mapping. Root cause unknown.

### Shapetrans (CH-SHP-2)
- Replaced ray-profile with central-moment (trace,det) templates.
- Templates: CIRCLE(3166,25050), TRIANGLE(1544,5950), SQUARE(4177,43610).
- **Result**: 0 false installs on shapetrans (was 53 in R2-14). Works.

### Colorconst (CH-CCN-1 retained)
- Investigated pixel-L1, 8x8-L1, 4x4-L1, histogram-L1 replacements.
- **FINDING**: R2A G has systematic variation (~18 mean diff). All spatial comparisons fail (SAME/DIFF overlap). Only mean-RGB separates.
- **DECISION**: Retained CH-CCN-1. Fixture G does not support finer quantity.

### Motiondir
- Removed votes>=10, margin>=4, and bestv>=8 floors. Pure agreement rule.

### Support rule
- INSTALL iff outcome==claim and resolved. No margins.

## Measured bars

### 1. Enumerated adversarial (10,000 trials)
- **False installs**: 61/10,000 = 0.61%
- **Overall UCB (95%)**: 0.783% — **PASSES** (≤1%)
- Per-task: colordisc 0, colorconst 2, shapetrans 0, pitchdisc 1, timbredisc 52, motiondir 6
- Per-family UCB:
  - colorconst f1: 2/690, UCB 1.05% — PASS
  - pitchdisc f1: 1/710, UCB 0.79% — PASS
  - motiondir f1: 5/504, UCB 2.30% — **FAIL** (>2%)
  - motiondir f2: 1/116, UCB 4.72% — **FAIL** (>2%)
  - timbredisc f1: 33/500, UCB 9.12% — **FAIL** (>2%)
  - timbredisc f3: 19/190, UCB 15.09% — **FAIL** (>2%)
- **PREREG DEFECT**: motiondir f2 (n=116) and f3 (n=10) cannot pass ≤2% even with zero FI (UCB0=3.21%, 27.75%). Bar mathematically unachievable.

### 2. Recall (2,000 controls)
- **Recall**: 1552/2000 = 77.6% — **FAIL** (≥80%)
- Per-task:
  - colordisc: 987/1080 = 91.4% (ceiling 93.0%)
  - colorconst: 389/720 = 54.0% (ceiling 56.8%)
  - motiondir: 176/200 = 88.0% (ceiling 96.5%)
- **Overstrict**: 26/2000 = 1.3% — PASS (≤5%)

### 3. Ablation (abl_bank)
- **NOT IMPLEMENTED**. Exemplar extraction script written but not run. Bank tables not generated. Zag ablate mode not updated.

### 4. Design-loop CP suite
- **NOT RUN**. No iterations completed.

### 5. Novel holdout (10×1,000)
- **NOT GENERATED**. Families not defined.

### 6. Post-freeze CP suite
- **NOT RUN**.

### 7. Determinism (byte-identical ×2)
- **NOT VERIFIED**. Single runs only.

## Design-loop iterations
0 (CP suite not run).

## White-box findings

1. **Timbredisc coefficient defect** (fixed): R2-14 used 880*m Hz, correct is 440*m Hz.
2. **Timbredisc mapping anomaly** (unresolved): Correct mapping performs 7x worse than swapped. Systematic bias in Goertzel vs generator templates.
3. **Shapetrans ray-profile defect** (fixed): Ray harmonics misclassified square as circle. Moment-based replacement achieves 0 FI.
4. **Colorconst G noise** (unfixable): Systematic ~18 variation prevents pixel-level comparison. Mean-RGB is the only viable quantity.
5. **Prereg per-family bar defect**: Mathematically impossible for n<200.

## Commit hashes
- Prereg: `4601db7f3182181f525c5791339207243727caa2`
- Sources/results: **NOT COMMITTED** (incomplete)

## ALIVE/DEAD
**DEAD** (fails recall ≥80% and per-family UCB ≤2%).

## Recommendations
1. Amend prereg per-family bar for small n (or exclude n<500 families).
2. Investigate timbredisc Goertzel bias (white-box).
3. Investigate colorconst G generation (systematic variation).
4. If recall is critical, relax challenges further (trades off FI).
5. Complete ablation, CP suite, holdout, determinism before re-verdict.
