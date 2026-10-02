# Prereg Amendment 1: H-REVISE2 Adversary (X-RV1 R2 fixture correction)

**Date:** 2026-09-29
**Amends:** PREREG_REVISE2_ADV.md (frozen 1bbadf544)
**Status:** FROZEN (committed before the corrected attack execution)
**Reason:** setup miscalculation in the X-RV1 R2 fixture, found on first
execution. Transparent correction; kill criterion unchanged.

## Error

The prereg specified R2 counterexample ("yza"->"aaa") and stated "P0
predicts 'zzz', mismatch, expect DETECT."

This is wrong. P0 = [N C1 SUB] (broadcast-last). For input "yza"
(n=3), P0 predicts broadcast of inp[2]='a', i.e. "aaa", which MATCHES
the expected output. No DETECT occurs. The first execution confirmed:
"X-RV1 R2 UNEXPECTED MATCH". The mechanism behaved correctly; the
fixture was miscalculated by the adversary.

## Correction

R2 counterexample is ("yzb"->"yyy") (broadcast-first). Under the R1
dispatch, "yzb" routes to P0 (input[0]='y'=121 != 120). P0 predicts
broadcast of inp[2]='b', i.e. "bbb" != "yyy": mismatch, DETECT
expected. Diagnosis of "yzb" against the passing set ("abc","def",
"ghi","jkl"): p=0, 'y'=121 differs from all passing bytes at p=0,
so (0,121) expected. P2 discovered from {("yzb"->"yyy")}:
pextract gives seq=[0,0,0], n=3, so P2 = [N N SUB] (broadcast-first,
constant 0). vs_revise with (0,121) overwrites the R1 condition slot.

## Kill criterion (unchanged)

If after R2 the R1 case "xab"->"xxx" FAILS, X-RV1 SUCCEEDS
(single-slot overwrite; chained revision destroys the earlier
revision). The first (miscalculated) execution already showed the
overwrite destroys R1; this amendment makes R2 a genuine
DETECT-to-REVISE event so the test is faithful.

## What this confirms

The adversary's prereg arithmetic is auditable and was wrong on this
fixture; the correction is recorded before the corrected run. No
mechanism code is touched. X-RV2 and X-RV3 are unaffected.
