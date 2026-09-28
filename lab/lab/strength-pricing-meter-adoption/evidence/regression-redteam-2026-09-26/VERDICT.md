# VERDICT: HOLD

Independent regression + fresh red-team against the adopted destruction-price
meter (commit `94625817c6f65e07c4ac99abde5dd533f0e810a5`). **No holes found.
The mechanism holds.**

## Bottom line

| Battery | Sequences / executions | Result |
|---|---|---|
| S1 independent regression (pre vs post, x2) | 160 executions | 0 failures; pre == post byte-for-byte on all 36 cells + 4 gates |
| Wedge battery (pre vs post, x2) | 4 runs x 628 lines | WB_VERDICT fail=0; byte-identical |
| adopt_test (independent rebuild, x2) | 50 checks | 50 ADOPT_PASS / 0 ADOPT_FAIL; byte-identical |
| meter_test (independent rebuild, x2) | 8 checks | 8 METER_PASS / 0 METER_FAIL; byte-identical |
| R1 resurrection after slot reuse | 120 | 0 fails, 0 holes |
| R2 cross-slot double-spend | 128 | 0 fails, 0 holes |
| R3 weakening + framing | 108 | 0 fails, 0 holes |
| R4 overwrite-reset | 105 | 0 fails, 0 holes |
| R5 kind-switch | 120 | 0 fails, 0 holes |
| R6 over-cite bricking | 104 | 0 fails, 0 holes |
| **Red-team total** | **685** | **0 fails, 0 holes** |

Every battery ran twice with byte-identical output. All 685 red-team sequences
are deterministic pure-Zag (zero RNG) attacks; each one's oracle was verified
twice.

## What was attacked

- **Spent-cite resurrection (R1/R2):** 248 sequences tried to fund a destruction
  with tombstoned citations — via slot-number reuse and via cross-slot
  double-spend, in both cite orders. Every attempt returned 121; the honest
  full-fresh controls succeeded, so the battery was not vacuously failing.
- **Framing (R3):** JUSTIFY tiers 1..7, absent, and stacked cannot move the
  meter; weakened-then-reframed judgments price identically (high-water +
  fought history survive WEAKEN).
- **Overwrite-reset (R4):** overwriting a strong memory to a weak strength
  never lowers the price (revision lineage adds, high-water persists); the
  packed reason bytes still report the original band.
- **Kind-switch (R5):** DELIB-kind deliberations do not bind METER-mode
  destruction (dry-run -1, destruction 122), and the independent checker
  agrees on all 120.
- **Over-cite (R6):** citing past the bound price is refused at cite time
  (122); spent cites never count toward fullness; the slot is never bricked.

## Regression

`REGRESSION.tsv`: all 36 S1 cell fingerprints and all 4 gate fingerprints are
byte-identical pre-adoption vs post-adoption, and pass1 == pass2. The wedge,
adopt, and meter batteries reproduce the committed evidence exactly.

## Method notes

Two test-oracle bugs were found and fixed during the run (both in the test
code, not the mechanism): the R4 exact-price oracle did not account for the
0..4 clamp floor, and expected a wrong r1 band constant for weak memories;
the R6 interleave attempt cited the old price instead of the re-added slot's
price. After fixing, all batteries pass clean on both runs.

No mechanism holes were found, so nothing was (or needed to be) fixed.
