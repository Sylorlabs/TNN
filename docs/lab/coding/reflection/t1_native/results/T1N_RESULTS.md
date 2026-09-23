# T1N bar table

## Mastery per tier (pass/total)

| tier | baseline | informed | scratch |
|---|---|---|---|
| T1 | 10/10 | 0/10 | 0/10 |
| T2 | 8/8 | 0/8 | 0/8 |
| T3 | 10/10 | 0/10 | 0/10 |
| T4 | 12/12 | 1/12 | 1/12 |
| T4M | 4/4 | 1/4 | 1/4 |
| T4X | 0/8 | 1/8 | 1/8 |
| T5 | 6/6 | 5/6 | 5/6 |

## Bars

| bar | informed | scratch |
|---|---|---|
| KB-R1 | FAIL | FAIL |
| KB-R2 | challenger mean-iters=0.57 znc=17 on T3+T4+T4X; baseline efficiency not pinned in prereg §5 | challenger mean-iters=0.57 znc=17 on T3+T4+T4X; baseline efficiency not pinned in prereg §5 |
| KB-R3 | FAIL (1/8 T4X first-attempt) | FAIL (1/8 T4X first-attempt) |
| RK1 | FAIL | FAIL |
| RK2 | FAIL | FAIL |
| RK3 | PASS (5 reps byte-identical) | PASS (5 reps byte-identical) |
| RK4 | PASS | PASS |
| RK5 | FAIL | FAIL |
| IV-P0 | PASS | PASS |
| IV-P1/P2 | FAIL | FAIL |

## Notes

- Baseline: prereg §5 pinned numbers (T1 10/10, T2 8/8, T3 10/10, T4 12/12, T4m 4/4, T4x 0/8, T5 6/6).
- KB-R2 baseline efficiency (mean iters / znc on T3+T4+T4X) is not pinned in prereg §5; challenger values reported for the coordinator's comparison against the Task-1 final report.
- RK4 detail:
  - AUDIT PASS: driver + wrapper are decision-free plumbing
- IV-P1/P2 are the driver's mechanical checks; coordinator manual review follows (grep is necessary, not sufficient).
- Invention-claim FAIL (IV-P1/P2) does not void the mastery numbers (prereg §6.1: separate finding).
