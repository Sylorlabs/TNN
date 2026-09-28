# Broker score record — native epistemics, Train-LOO (Phase 1)

Scored once by the coordinator (honest broker) against the sealed mapping.
The label-blind implementer never saw these numbers.

- Verdict file: `docs/lab/epistemic_native/phase1/loo5/loo_verdicts.tsv`
  (SHA-256 `4eb826267ce9cad643aad9765b0dca91ff7de8d39245ab3602f973f7b099ab0e`;
  byte-identical to `loo6/loo_verdicts.tsv`)
- Mapping: `~/workspace/epi_a3/_coordinator/MAPPING.sealed` (broker-only, never committed)

## Confusion matrix (rows = true class, cols = verdict)

| true \ verdict | FACT | OPINION | LIE | UNDETERMINED | n |
|---|---|---|---|---|---|
| fact | 42 | 0 | 41 | 85 | 168 |
| opinion | 37 | 0 | 9 | 94 | 140 |
| lie | 25 | 0 | 13 | 46 | 84 |
| skepticism | 23 | 0 | 1 | 32 | 56 |

## Prereg Train-LOO bars

| Bar | Result | Required | Verdict |
|---|---|---|---|
| Lie recall | 0.1548 (13/84) | > 0.048 | **PASS** |
| Opinion recall | 0.0000 (0/140) | ≥ 0.957 | **FAIL** |
| Fact→lie false positives | 41 | 0 | **FAIL** |

Net: 2 of 3 bars fail → **NO-GO** per the frozen prereg. See `NO_GO_REPORT.md`
for mechanism-level causes. No held-out run was performed (prereg: stop on NO-GO).
