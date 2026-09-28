# VERDICT — W18 Negative-Knowledge Ledger (NKL)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w18_run1.txt`, `w18_run2.txt` (byte-identical)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| Attack admit | 14/14 (preregistered: 0% catch, honestly reported) |
| W violations (K1) | 0 |
| Tags fired | ≥1 (G1 filled on honest C) |
| Vetoes | 0 on tape (probe P-NKL2 vetoes correctly) |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS.
- **K-NKL-1:** PASS. No c3=0 row published; dec=c3 always.
- **K-NKL-2:** PASS. P-NKL2: decA=1, decB=0, vetoB=1.
- **K-NKL-3:** PASS. Tags fire (G1 fills); zero vetoes on tape is allowed (bar requires zero vetoes AND zero tags to kill).

## Corrigendum note

Per `TAPE_WILDC_CORRIGENDUM.md`: G1's domain `FNV("tape")` intentionally matches honest C rows (exercises gap-fill on honest traffic), disjoint from attack/W/P/B only. G2 is fully synthetic.

## Verdict: SURVIVE

Veto/tag machinery exercises correctly. Attack catch 0% is preregistered (no kill bar requires it of W18).
