# RED TEAM SCORECARD — RNGSCAN-2026-09-20-v2 (blind round)

Status: SCORED — K2 FIRED. Version RNGSCAN-2026-09-20-v2 is DEAD.

Frozen checker: `ee962e53817c81721996a8086c5e42530da07316250b1a4906ab74a56a3d9e5d`
Rebuilt binary: `9bbaf5390f140a88516d6f1912bc060610bd773af32406f7fd935c5281c41943`
(matches freeze record — deterministic toolchain confirmed)
Runner: `runner/run_audit.sh` (RUNAUDIT-2026-09-20-v1)
Fixtures: `fixtures/state1.bin`, `fixtures/state2.bin`, `fixtures/input.bin`
Report: `REDTEAM_REPORT.md` (this directory)

Scored 01–14 in order, checker+runner unmodified throughout; round halted
after K2 fired (scorer kill landed after plant14). Plants 15–20 unscored.

| # | plant file | planted category | verdict | rules named | planted rule named? |
|---|---|---|---|---|---|
| 1 | plant01.zag | 4.1 entropy | FAIL | 4.3 (spurious), REPLAY | no |
| 2 | plant02.zag | 4.1 entropy | FAIL | REPLAY | no |
| 3 | plant03.zag | 4.1 entropy | FAIL | 4.1, 4.3, 4.6/4.1, REPLAY | YES |
| 4 | plant04.zag | 4.2 wall-clock | FAIL | REPLAY | no |
| 5 | plant05.zag | 4.2 wall-clock | FAIL | REPLAY | no |
| 6 | plant06.zag | 4.2 wall-clock | FAIL | REPLAY | no |
| 7 | plant07.zag | 4.3 uninit | **PASS — MISS** | — | **MISS** |
| 8 | plant08.zag | 4.3 uninit | FAIL | 4.3 | YES |
| 9 | plant09.zag | 4.3 uninit | FAIL | 4.3 | YES |
| 10 | plant10.zag | 4.4 hash-iter | **PASS — MISS** | — | **MISS** |
| 11 | plant11.zag | 4.4 hash-iter | **PASS — MISS** | — | **MISS** |
| 12 | plant12.zag | 4.5 impure | FAIL | 4.5 ×2 | YES |
| 13 | plant13.zag | 4.5 impure | FAIL | 4.5 ×2, REPLAY | YES |
| 14 | plant14.zag | 4.5 impure | FAIL | 4.5 ×2 | YES |
| 15 | plant15.zag | 4.5 impure | not scored | — | round halted |
| 16 | plant16.zag | 4.8 dispatch | not scored | — | round halted |
| 17 | plant17.zag | 4.8 dispatch | not scored | — | round halted |
| 18 | plant18.zag | 4.9 comment | not scored | — | round halted |
| 19 | plant19.zag | 4.1 entropy | not scored | — | round halted |
| 20 | plant20.zag | 4.3 uninit | not scored | — | round halted |

Score: **3 misses / 14 scored** (miss rate ≥ 3/20) → K2 FIRED → v2 KILLED.
K3 also fires (07, 10, 11 carry planted constructs on PASS paths). K1 did not fire.
