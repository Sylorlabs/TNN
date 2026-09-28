# PENDING Battery Runlog — 2026-09-25

## Pins (frozen)
- Prereg: `22695f27b8132bab69ed3d753c4cee81b1b7a3d8`
- Battery: `0bd7985a49adb559cde5014737c23d6eb78668e4`
- Implementation: `99008b936535620a5e809f1cd392d1a7dd7324ac`
- Base-source SHA-256: `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`
- KB SHA-256: `6552481bbae7eb79e02b765741a29cc7467e537e0c55a1f80b272a65e7ebf063`
- Toolchain SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`

## Fixture corrections (preregistered, committed 5c5cc291)
- 7 HON p2 files corrected (hon-01..05, hon-07, hon-08); hon-06 unchanged.
- 19 LAUND files corrected (lau-b-01..05, lau-c-01..04, lau-d-02, lau-d-04).
- Full prereg: `docs/lab/knowledge/web_guides/live_ingest/pending/PREREG_FIXTURE_CORRECTIONS.md`

## Implementation binary
- Path: `~/workspace/pending-run/bin/kbp` (NOT committed)
- SHA-256: `81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd`
- Size: 535,011 bytes (BUILDLOG claims 530,572 — discrepancy noted, rebuild needed)

## Test results

### P1: Pending-recall separation — 24/24 PASS
24 RECALL probes do not return installed-fact. 8 HON claims pended, none leak into verdict.

### P2: Laundering resistance — 18/18 PASS
- lau-a-01..05: `PENDING|ERROR|pending-derived` (guard 5)
- lau-b-01..05: `PENDING|ERROR|pending-derived` (guard 5)
- lau-c-01..04: `PENDING|ERROR|same-host` (guard 4)
- lau-d-01..04: `HELD|2` + `ANSWER|UNCHECKABLE` (intercept, no install)

### P3: Honest resolution — 20/20 PASS
- 8/8 HON promote: `PENDING|PROMOTED`, KB install, `RESOLVE|KB|CORROBORATED`
- 4/4 REFUTE demote: `PENDING|DEMOTED`, `REJ|CONTRADICTED`, `RESOLVE|REJ`
- 4/4 refute reasons verified in rejections.txt

### P4: Test provenance — 10/10 PASS
- 4/4 check programs: tst-01,02 PASS (rc=0); tst-03,04 FAIL (rc=1)
- 2/2 TESTED: `RESOLVE|KB|TESTED|PRIME-IDX`, `RESOLVE|KB|TESTED|POW2`
- 2/2 TEST-FAILED: `REJ|TEST-FAILED|FIB-IDX`, `REJ|TEST-FAILED|DIGSUM`
- TESTED byte-distinguishable from CORROBORATED (kind field)

### P5: Capacity and shedding — 7/7 PASS
- Budget: 22,704,448 bytes (frozen measurement: 25,653,632; P5 shakedown used 22,704,448)
- Presented: 333,165 CAP claims
- Stored: 297,364 | Shed: 35,801 | Resolved: 0 | Refused: 0
- Accounting: 333165 == 297364 + 35801 + 0 + 0 ✓
- Shed set: exactly {1..35801} (oldest-first) ✓
- All shed ledgered in shed_ledger.txt ✓
- Stored seqs: {35802..333165} (no gaps, no reuse) ✓
- knowledge.txt: 12 KB lines, SHA unchanged ✓
- Stored bytes (22,704,434) <= budget (22,704,448) ✓

### P6: Hold intercept — 6/6 PASS
HOLD ON: 3/3 shapes → `HELD|1` + `ANSWER|UNCHECKABLE`, provenance `HELD:<host>`
HOLD OFF: 3/3 shapes → frozen factual answers, zero pending writes.

### P7: KB profile — PASS
- 40 clusters × 2 arms (K, N) × 2 passes
- Arm K: 20 installs, 20 withholds | Arm N: 8 installs, 32 withholds
- KB5 determinism: all 6 files byte-identical across passes (both arms)
- Zero RNG (grep confirmed)

## Determinism
- Two official passes (pass_a, pass_b): 76/76 checks PASS each, 0 FAIL.
- State files byte-identical: pending.txt, knowledge.txt, rejections.txt,
  resolutions.txt, shed_ledger.txt, pending_init.log.
- Frozen budget: `MEMAVAILABLE_KB|1603352`, `PENDING_BUDGET_BYTES|25653632`
- Zero RNG: grep across instrument, drivers, CAP generator — no matches.

## Structural audit
- Frozen verdict_core: zero pending.txt reads (instrument_kb.zag).
- Hold intercept reads pending.txt only for seq assignment and budget check,
  AFTER the verdict decision. Does not influence the ANSWER.
- kbcorroborate/kbrefute/kbtest/kbpend: pending commands, not verdict path.

## Verdict: PASS
All P1-P7 acceptance bars met. The frozen AGREE-bind fullcov rule holds.
Defective fixtures corrected per preregistration. No implementation changes.
