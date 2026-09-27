# Deliberation v1 — Bar Results (repair cycle #4)

**Frozen source SHA:** 7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787
(`build/deliberate_frozen_r4.zag`; voided base `build/deliberate_frozen.zag` retained)
**Date:** 2026-09-27

## Validity
- Pure Zag, zero RNG: PASS
- Byte-identical reruns: PASS (R4 + B20 + heldout, stdout+stderr, 2 runs each)
- Frozen-path rebuild byte-identical to pre-freeze binary: PASS

## K1 — Order Invariance
- Own 12-action-GEN reversal variant; 77 turns (29 R4 + 28 B20 + 20 heldout), 0 A-line diffs: PASS

## K2 — Counterfactual Covariance
- 23 fresh KB flips (this cycle): 23/23 covariant, 23/23 surgical, 0 silent: PASS
- Covers content changes and winner-identity changes (hid 24→22, 23→24, 24→22)

## K3 — Trace-Ledger Bijection
- Own parser; 269 turns (77 base + 77 K1 + 115 K2-sample), 0 errors: PASS
- Content phash == sha256(A-line): 77/77: PASS

## K4 — Accuracy
- Round4: 27/29 turns (2 known-unachievable): PASS
- Trace-trial: 28/28 turns: PASS
- Heldout: 20/20 turns: PASS

## R2 Fix (red-team-3 finding)
- All 10 reading rows branch-read by action GEN preconditions (static audit): PASS
- Neuter test: 31/77 answers change, no crash: PASS
- Behavior-preserving: 0/77 A-line diffs vs voided base: PASS

## Close-Call
- Mechanism implemented, scoring allows <5 margins: PARTIAL
- Natural trigger not observed; synthetic demonstration pending

## K5
- NOT self-certified — fourth independent red team owns K5
