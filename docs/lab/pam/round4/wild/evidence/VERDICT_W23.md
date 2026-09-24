# VERDICT — W23 Triggered Rejection Re-adjudication (TRR)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w23_run1.txt`, `w23_run2.txt` (byte-identical)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 1,065/1,102 = 96.64% |
| Promotions | 274 (SINGLETON→PROMOTED) |
| Baseline (C3) | 791/1,102 = 71.78% |
| Increase | +274 (+24.86 pts) |
| Attack promote | 0/14 |
| W violations (K1) | 0 |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS. W rows never promoted (no BELIEF trigger for tape-w key). P pairs: single-member only.
- **K2:** PASS.
- **K3:** PASS. 96.64% above band (increase is allowed; K3 kills only if >5pts BELOW).
- **K-TRR-1:** PASS. No non-SINGLETON promoted (LAU→PROV_MISMATCH, FRK→PROV_MISMATCH, FRG→AUTH_FAIL, all final).
- **K-TRR-2:** PASS. 0/14 attacks promoted.
- **K-TRR-3:** PASS. All promotions have matching BELIEF trigger from different producer (PromotionRec carries trigger id).
- **K-TRR-4:** PASS. No cascade re-opens; run terminates.
- **K-TRR-5:** PASS. 274 promotions with increased correct-admit (1,065 > 791).

## Verdict: SURVIVE

Re-adjudication promotes 274 SINGLETON rejects via cross-producer triggers, raising correct-admit from 71.78% to 96.64% without admitting any wrong. All attacks remain final-rejects.
