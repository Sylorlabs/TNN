# AMENDMENT-001 — G5 DIALOGUE F2 fork prereg (item-table correction)

**Date:** 2026-09-22. **Status:** recorded before the fork's first green run;
no implementation run has passed with the unamended table.

## What changed

E22's correct action: WITH → **SUP (ANSWER-SUPPORTED)**.

E22: claim(A6,30); ev{(A1,10)}.

## Why

The frozen prereg's resolution procedure (§Domain model) is explicit:
"(2) else if a derivation rule chain resolves the claim attr to v:
SUPPORTED iff asserted==v". On E22 the chain resolves: R1 gives
A3 = 2*A1 = 20 from the evidenced A1=10; R4 gives A6 = A1+A3 = 30,
which equals the asserted 30. The table entry's annotation ("A3 absent
→ WITH") contradicted the procedure — it treated intermediate
attributes as requiring direct evidence, which would also break the E14
probe and every novel-composition item (E33 etc.), all of which depend
on chaining through non-evidenced intermediates.

The procedure is authoritative; the table entry was the bug. The
implementation (dz_resolve) followed the procedure and was correct.

## Effects on preregistered expectations

None of the frozen check expectations change: b_acq_correct stays 8/8,
b_unres_answer_n stays 1 (E22 leaves the unresolvable set),
f_elim_n stays 4, f_uncommit_n stays 0, f_audit_n stays 269. The
unamended table produced 5 check mismatches (b_acq_correct 7/8,
b_unres_answer_n 2/1, f_elim_n 5/4, f_uncommit_n 1/0, f_audit_n 271/269),
all tracing to this single entry — the committed P3 was eliminated at
the E22 demonstration because the table, not the procedure, was wrong.

## What this does NOT change

Item set otherwise unchanged; fade schedule, kill bars, predictions
P-G5-1..P-G5-5 unchanged. No implementation change was needed — only
the table entry.
