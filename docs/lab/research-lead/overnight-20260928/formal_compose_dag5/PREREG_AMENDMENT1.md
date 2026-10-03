# PREREG_AMENDMENT1.md -- FORMAL-COMPOSE-DAG5: exact-prediction
# corrections (root-caused; no kill-bar substance changes)

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG5.
Committed BEFORE the verdict runs were evaluated (the
discrepancy was found on the first run output and
investigated with a scratch diagnostic in /tmp before any
verdict was drawn).

## Root cause (single arithmetic slip, hand-derivation)

PREREG.md section 3.1 traced e_add(8,10,1) p1 as:

  p1: 6->8: 7<=7 -> 6:8; 7->8: 6<=8 -> 7:9.

The second update is wrong: after 6->8 sets t[6]:=8, the
7->8 edge reads ty=t[7]=6, tw=t[8]=7, so 6<=7 fires and
sets t[7]:=tw+1=8, NOT 9. The corrected pass-1:

  p1: 6->8: 7<=7 -> 6:8; 7->8: 6<=7 -> 7:8.

Corrected continuation: p2: 4->5 quiet (8<=7? no);
4->6: 8<=8 -> 4:9; 5->7: 7<=8 -> 5:9; 6->7: 8<=8 -> 6:9.
p3: 4->5: 9<=9 -> 4:10. p4 quiet. Converged in 4 passes.

Corrected state after e_add(8,10,1):
4:10,5:9,6:9,7:8,8:7,9:5,10:6 (prereg said
4:11,5:10,6:10,7:9,8:8). Edge 8->10 readable (6<7);
invariant intact.

The +1 slip cascaded into every later rank state:

- e_add(9,10,1): unchanged behavior (converges in 1 pass:
  all readable edges already consistent); state becomes
  4:10,5:9,6:9,7:8,8:7,9:7,10:6.
- e_add(10,4,2): seed t[10]:=11 (not 12). Corrected
  cascade: p1: 8->10 -> 8:12; 9->10 -> 9:12. p2: 5->9
  -> 5:13; 6->8 -> 6:13; 7->8 -> 7:13. p3: 4->5 ->
  4:14; 5->7 -> 5:14; 6->7 -> 6:14. p4: 4->5 -> 4:15.
  p5 quiet. Converged in 5 passes. State:
  4:15,5:14,6:14,7:13,8:12,9:12,10:11 (prereg said
  4:16,...,10:12). The 10->4 record relocates to head 15;
  item 10 reads heads 0..10: INERT. All 10 type-1 edges
  preserved.
- e_add(10,10,2): corrected cascade converges in 5
  passes. State: 4:16,5:15,6:15,7:14,
  8:13,9:13,10:12 (prereg said 4:17,...,10:13).
  Self-loop record relocates to head 12; item 10 reads
  0..11: INERT. All 10 type-1 edges preserved
  (8->10: 12<13; 9->10: 12<13; 7->8: 13<14; 7->9:
  13<14; 5->9: 13<15; 6->8: 13<15; 5->7: 14<15;
  6->7: 14<15; 4->5: 15<16; 4->6: 15<16).

The corrected trace was verified digit-for-digit against
the mechanism by a scratch diagnostic (/tmp/d5_diag.zag,
NOT part of the battery): after every e_add the live
rank vector and maxrank-seen match the corrected trace
exactly.

## Exact corrections

1. D5B line: maxrank 11 -> 10. (promotes=10, t1=10,
   all edge bits unchanged.)
2. D5C line: maxrank 17 -> 16. (promotes=12, diverge=0,
   t1=10, t2=0, all edge bits unchanged.)
3. PREREG section 3.1: the e_add(8,10,1), e_add(10,4,2),
   e_add(10,10,2) traces above replace the prereg text.
4. Kill-bar text corrections (exact values only; the
   bars' substance is unchanged):
   - D5-4: "maxrank=11" -> "maxrank=10".
   - D5-5: "maxrank=17" -> "maxrank=16".

No other prediction changes. All six kill bars pass on
the corrected values. The mechanism's headline claims
(composition, cycle-inertness, invariant, convergence)
were never in doubt: the binary matched every predicted
bit and counter except the two maxrank values, and the
diagnostic confirms the mechanism implements its frozen
spec exactly.
