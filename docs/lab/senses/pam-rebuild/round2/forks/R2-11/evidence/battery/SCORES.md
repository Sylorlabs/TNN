# R2-11 Final Scores

Frozen battery results, seed 20260923. Both forks KILLED by B5.

## Primary battery (370 frozen harness trials)

| Fork | Accuracy | Installs | False installs | KB-E1 |
|------|----------|----------|----------------|-------|
| A (replay) | 368/370 = 99.46% | 155 | 0 | PASS (370/370 equal=1) |
| B (generative) | 368/370 = 99.46% | 155 | 0 | n/a (expected divergence) |

B1 (≥60%): PASS both.

Misses (both forks, shared percept):
- `t1_colordisc/primary/p015.img`: truth SAME, predicted DIFFERENT
- `t1_colordisc/primary/p040.img`: truth DIFFERENT, predicted SAME

## 10,000-trial battery (run 1; runs 2-3 byte-identical)

| Fork | Accuracy | Installs | False installs | False rate | B5 (≤3%) |
|------|----------|----------|----------------|------------|----------|
| A (replay) | 8,449/10,000 = 84.49% | 3,548 | 415 | 4.15% | **FAIL → KILL** |
| B (generative) | 8,449/10,000 = 84.49% | 3,548 | 415 | 4.15% | **FAIL → KILL** |

### Operations and bytes (B3)

| Fork | Total ops | Ops/trial | Payload bytes | Bytes/trial |
|------|-----------|-----------|---------------|-------------|
| A | 2,561,866,383 | 256,187 | 365,809,664 | 36,581 |
| B | 2,331,006,607 | 233,101 | 365,809,664 | 36,581 |

Fork B measured FEWER ops than Fork A (not more). The renderer's synthesis
is cheaper than Fork A's double-copy emission on these payloads. Reported
as measured; not claimed as a general cost advantage.

### Fork B divergence (expected, scored)

- Divergent runs: 3,548,810
- Divergent bytes: 318,267,182 (31,827/trial)

## Determinism (B6)

- 3/3 emit-on TSVs byte-identical per fork (cmp verified).
- 4 ledgers per fork verified: 10,000 lines, 0 problems, head `310a1d70a8d1faef`.

## No-interference (B4)

- Fork A: 0/10,000 trials differ (emit-on vs emit-off). PASS.
- Fork B: 0/10,000 trials differ (emit-on vs emit-off). PASS.

## KB-E2 (no empty/phantom/unowned emission)

- Fork A: 0 bad emissions, 0 phantom ledger seqs. PASS.
- Fork B: 0 bad emissions, 0 phantom ledger seqs. PASS.

## Verdict

Both forks KILLED under §5.1 (B5: 4.15% > 3% false permanent installs).
The shared percept pipeline failed before the emission choice mattered;
replay vs generation remains unresolved by this experiment.
