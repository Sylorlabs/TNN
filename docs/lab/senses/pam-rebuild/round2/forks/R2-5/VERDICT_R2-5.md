# VERDICT_R2-5: Withholding-first ablation

## Outcome: DEAD (promotion precision bar failed)

R2-5 implements a perceptual system with NO self-result field. Every percept begins UNRESOLVED. Promotion requires (1) successful prediction outside the source span (predictive contract), OR (2) deliberation ratification citing its warrant.

## Deciding bar

Per PREREG_R2-5.md, the deciding question: does removing the self-result field lose anything vs R2-4? If R2-5 matches/beats R2-4 on safety, promotion recall, and B4 with less machinery, the result field is decorative.

R2-4 has not landed (no verdict found as of 2026-09-23). Comparison PENDING.

## Bar numbers (full R2A battery)

| Bar | Required | Achieved | Status |
|-----|----------|----------|--------|
| Promotion precision (normal) | ≥95% | 86% (4286/4949) | **FAIL** |
| Promotion recall (normal) | ≥80% | 98% | PASS |
| Escalation (normal) | ≤5% | 2% (151/5100) | PASS |
| RK-1 false installs (normal) | ≤3% | 13% (663/5100) | **FAIL** |
| RK-4 ablation installs (adv) | ≥100 | 5810/5815 | PASS |
| B4 contract delta (adv) | ≥10% | 10.06% (585/5815) | PASS |
| B4 reduces false installs | yes | 3293 < 3498 | PASS |
| B6 determinism | 3x identical | Not run | - |
| B1 primary accuracy | ≥60% | Not run | - |

Per-task precision (normal):
- colordisc: 51% (520/1010) — hard DIFFERENT (de 2.4-4.0) vs SAME-near (de 0.4-1.6)
- colorconst: 90% (628/692)
- shapetrans: 100% (1279/1279)
- pitchdisc: 84% (575/684) — near-threshold 0.5% frequency differences
- timbredisc: 100% (720/720)
- motiondir: 100% (564/564)

Adversarial full mode (for reference):
- Accuracy: 39% (2312/5815)
- Precision: 36% (1932/5225)
- Recall: 83% — PASS
- Escalation: 10% (585/5815)

## Why it died

The withholding mechanism (predictive contract + deliberation) is insufficient to achieve 95% promotion precision on the full normal set. The classifiers for colordisc, pitchdisc, and colorconst make systematic errors on near-threshold cases that the contract does not catch:

1. **Colordisc** (51% precision): Hard DIFFERENT cases (Delta E 2.4-4.0) produce RGB distances (~30-38) that overlap with SAME-near cases. The contract (left/right halves must agree) does not help because both halves see the same subtle difference.

2. **Pitchdisc** (84% precision): Near-threshold frequency differences (0.5%, ~2Hz at 440Hz) are below the autocorrelation resolution (integer lags). Spans agree on the wrong answer.

3. **Colorconst** (90% precision): Similar near-threshold issues.

The contract works for B4 (reduces false installs on adversarial: 3293 vs 3498), but not enough for the 95% precision bar on normal.

## Fixture count contradiction (MATERIAL)

PREREG_R2-5 summary states: 5,000 normal (740 old + 4,260 generated) + 5,000 adversarial (185 old + 4,815 generated) = 10,000 total.

Detailed tables (followed by generator): 5,100 normal + 5,815 adversarial = 10,915 generated. With 925 old fixtures: 11,840 total.

The generator honored the detailed tables, not the summary. This is a prereg internal contradiction. Results are on the 10,915 R2A fixtures actually generated.

## Design

Pure Zag, zero RNG in decision paths. Six task front-ends. Predictive contract: span A must predict span B (confidence ≥100). Deliberation: ratify with cited warrant. Hash-chained ledger.

## Evidence

- Source: `src/sense.zag`
- Prereg: `PREREG_R2-5.md`
- Battery: `evidence/battery_full_r2n.txt`, `evidence/battery_full_r2a.txt`, `evidence/battery_ablate_r2a.txt`

## Conclusion

R2-5 DIES on the promotion precision bar (86% < 95%). The no-self-result design does not achieve the required safety. The contract mechanism helps (B4 passes) but is insufficient for near-threshold perceptual discriminations.


