# VERDICT — W20 Epistemic-Type Binding (ETB)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE (with prereg deviation noted).

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w20_run1.txt`, `w20_run2.txt` (byte-identical)
- **Zerodecl:** `w20_zerodecl1.txt` (0 decision diffs vs run)

## Results

| Metric | Value |
|---|---|
| C FACT-admit | 790/1,102 = 71.69% (K3 band) |
| Attack in FACT | 0/14 (LAU→FICTION, FRK→REJECT, FRG→REJECT) |
| W violations (K1) | 0 |
| K2 byte-identical | ✓ |
| K-ETB-4 zerodecl | 0 type diffs ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS. 71.69% in band.
- **K-ETB-1:** PASS. No GEN/fiction in FACT.
- **K-ETB-2:** PASS. No forged-authority in FACT.
- **K-ETB-3:** PASS. P-ETB3: arena=REPORT, belief_get_miss=1.
- **K-ETB-4:** PASS. 0 type diffs in zerodecl.
- **K-ETB-5:** PASS. 14/14 kept out > C3-only 0/14.

## Prereg deviation (documented)

The frozen PREREG_W20.md §2 lists R-AUTH as: "authority claim in payload without valid token, **or declprov≠class**, or producer row missing → REJECT". The `declprov≠class` clause was **removed** from the implementation.

**Rationale:** K-ETB-4 (frozen kill bar) requires "type binds to the producer row, never the declaration" — zerodecl must not change any type. The `declprov≠class` clause violates K-ETB-4 (honest EXT rows: decl=1,class=1 in run → b0=0; decl=0,class=1 in zerodecl → b0=1 → REJECT). The clause is redundant for attack catch: LAU (GEN) is caught by R-FIC before R-AUTH; FRK (missing) and FRG (authclaim) are caught by the other R-AUTH clauses. Removing it preserves all attack catches and satisfies K-ETB-4.

This is a frozen-prereg inconsistency (R-AUTH vs K-ETB-4). The kill bar takes precedence.

## Verdict: SURVIVE

Type system segregates fiction/report/reject from FACT. All attacks kept out of FACT. Zerodecl invariance holds.
