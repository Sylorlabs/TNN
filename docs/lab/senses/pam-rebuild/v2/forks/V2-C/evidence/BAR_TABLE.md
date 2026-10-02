# Bar table — V2-C measured (3 runs byte-identical)

| Bar | Frozen bar | Measured | Verdict |
|-----|-----------|----------|---------|
| KD-1 adversarial wrong-high-conf | ≤537 | 675 | FAIL |
| KD-2 per-family | reported | see KD1_FAMILY_TABLE.md | reported |
| RK-1 false permanent installs / 11,840 | ≤3% | 0.000% | PASS |
| RK-2 wrong-HC reaching permanent install | ≤1% | 0.000% | PASS |
| RK-3 correct-HC reaching PASS+install | ≥85% | 14.56% | FAIL (expected death) |
| RK-5 wrong-HC → FAIL/UNRESOLVED over indep. evidence | ≥90% | 99.01% | PASS |
| B5 false permanent installs, adversarial | ≤3% | 0.000% | PASS |
| B1 frozen-370 primary judgment accuracy | ≥60% | 87.30% | PASS |
| B6 3× byte-identical + ledger verified | required | PASS (see RUN_DIGESTS.md) | PASS |
