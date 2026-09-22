# Addendum SI-A1 — resolution measurement for the Arm 1 epistemic PARTIAL
Frozen 2026-09-22, before any resolution run. No bar, clause, or verdict
rule of frozen PREREG §3e (commit 43eceed2100c73b1b065f0685644d171a5837a4a)
is changed by this addendum.

Open cell: epistemic knee clause (a), failed 0<0 on a hard plateau
(29/94 → 59/94 → 59/94 → 59/94; 4x recon 0/94; 8x vflips 0/94).

Resolution measurement (preregistered):
1. Build a FRESH, DISJOINT 94-item epistemic battery using the same
   construction procedure as work_a1/battery_si_notes.md. Item IDs disjoint
   from the original 94. Construction script + item list committed.
2. Rerun the epistemic slice ONLY (delib_si.zag UNCHANGED, same 4 budget
   rungs, 3 reruns, canonical logs byte-identical). Gate battery 6/6.
3. Resolution rule: PLATEAU-CONFIRMED iff gain(1x→2x) > 10pp AND
   gain(2x→4x) ≤ 1pp AND gain(4x→8x) ≤ 1pp on the fresh battery.
   Otherwise PLATEAU-REFUTED.
4. Reporting:
   - CONFIRMED → "epistemic plateau replicates; knee at 2x confirmed;
     Arm 1 verdict remains PARTIAL per frozen §3e strict clause (a).
     Relaxing the strict clause needs Micah-signed amendment."
   - REFUTED → full Arm 1 epistemic re-run, corrected bar table,
     verdict recomputed per frozen §3e.

Scope: epistemic replication only. delib_si.zag, driver_si.py, budgets,
gates, and all other arms untouched.
