# Smoke tests (pre-prereg engineering, NOT result evidence)

Performed 2026-09-24 on throwaway sentences before the PREREG_KB freeze.
Three synthetic verdicts verified the retrieval prior's three paths fire:

1. AGREE: candidate == committed claim 3 (water/100C/sea level)
   -> KB|AGREE|3, KB|CORROBORATED|3, ANSWER + CLAIM + 2 PROVs. PASS.
2. CONTRA: same sentence with 80C substituted
   -> KB|CONTRADICT|3, GATE|KB_CONTRADICTION|3, ANSWER|UNCHECKABLE. PASS.
3. UNKNOWN: unrelated topic ("honey perishable sealed")
   -> frozen path: ANSWER|UNCHECKABLE + UNCHECKED. PASS.
4. Arm-N equivalence: with knowledge.txt absent, verdict output on all
   three inputs was BYTE-IDENTICAL to a fresh compile of frozen BF1
   (forkbase/webg_bf1.zag). PASS.

Bug found and fixed in shakedown: `digits_eq` was called with the
content arena `sab` instead of the digit arena `sdb` (digit-table offsets
index the digit arena), making deq always 0 -> true agreements were scored
CONTRADICT. One-line fix in instrument_kb.zag; recompiled; all four checks
above are post-fix.

No battery cluster was authored or run before the prereg freeze.
