# R32 E55A — Native Post-Continuation Terminal Coordinate Audit

Date: 2026-08-30  
Status: `EXECUTED_VALID_NATIVE DEVELOPMENT POSITIVE — TERMINAL BASIS HAS MARGINAL VALUE AFTER CONTINUATION`  
Canonical: **R27 step 60,423**  
Validation executed: **0**  
Confirmation executed: **0**

## Authority

- native Zag v2 source SHA-256: `6b4e614100363e02d472caeb71f1ce7640f75e95233dcaa57584fa17961165ea`
- persisted compiler SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- byte-identical native binaries SHA-256: `f6a01dad0ec9cf654e9d7fe250ea72151fe889c0d8c2f215f7766891cb3f6c39`
- raw ledger SHA-256: `ded6bc9c32cc5b7a164c629e0594e18ea5af00dd07f5f199ba3142aa77e2a93f`
- stderr empty
- wall time: 291.366837391 s
- exit code: 0 (development diagnostic positive)
- terminal fit forward/reverse identity: PASS
- integrity: PASS

## Frozen continuation reproduction

C reproduced exactly:

- net utility 421,543
- observations 1,242
- opportunity loss 137,257
- known success 1,062
- known wrong 50
- no-unique UNKNOWN 384
- no-unique wrong 336
- reached states 4,482; reached hash 1251698266
- learned observation shadow price 212

## Terminal coordinate fit

Exact fitted E52A-basis coefficients on C's reached states:

`[-4887, 205, 1152, 113, -220, 1846, -841, 39]`

Generic damping candidates:

| Rate | Safety | Utility | Known success | Known wrong | No-unique wrong |
|---:|---:|---:|---:|---:|---:|
| 1 | FAIL | 436,543 | 1,185 | 47 | 431 |
| 1/2 | FAIL | 500,943 | 1,105 | 15 | 364 |
| **1/4** | **PASS** | **496,943** | **1,071** | **18** | **334** |
| 1/8 | PASS | 448,343 | 1,066 | 38 | 337 |
| ~1/16 | PASS | 436,143 | 1,063 | 42 | 338 |
| ~1/32 | PASS | 415,943 | 1,058 | 49 | 339 |

The selected 1/4 coefficients are:

`[-1221, 51, 288, 28, -55, 461, -210, 9]`

Compared with C, the selected terminal coordinate adds **+75,400** net utility with identical observation cost, raises known success by 9, reduces known wrong by 32, and reduces no-unique wrong by 2. Compared with the terminal control, it has +56 known successes and -148 known wrong commitments.

## Interpretation

E55A rejects the hypothesis that the fixed E52A terminal basis is useless. The basis has clear value **after** the continuation policy is stabilized. Therefore E53/E54 failed because terminal and continuation changes were coupled into the same conservative proposal, not because terminal structure had no marginal value.

The selected coordinate policy is frozen for E55B fresh validation. This is not promotion evidence by itself.
