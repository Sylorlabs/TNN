# INDEPENDENT BATTERY — SCORES

determinism_5x: PASS

| cap | n | correct | score | coupled | gap (coupled-indep) |
|---|---|---|---|---|---|
| contra | 12 | 12 | 1.0000 | 1.0000 | +0.0000 |
| false | 12 | 12 | 1.0000 | 1.0000 | +0.0000 |
| para | 12 | 1 | 0.0833 | 0.9649 | +0.8816 |
| truth | 12 | 8 | 0.6667 | n/a | n/a |
| abstain | 12 | 12 | 1.0000 | n/a | n/a |
| prov | 12 | 12 | 1.0000 | n/a | n/a |

mirror_baseline_truth: 0.5000
learner_truth: 0.6667

## Kill bars
- KB-GAP(contra): HOLD — gap +0.0000
- KB-GAP(false): HOLD — gap +0.0000
- KB-GAP(para): TRIPPED — gap 0.8816 > 0.30 → headline GENERATOR-COUPLED, revised to independent number
- KB-TRUTH: HOLD — learner 0.6667 > mirror 0.5000
- KB-DET: HOLD
