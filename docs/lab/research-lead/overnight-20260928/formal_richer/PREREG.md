# PREREG: TX1 Typed Arithmetic (formal_richer)

Frozen before implementation. Any break requires fresh prereg, fresh
worlds, rerun. VOID is terminal. Kill bars below are exact.

## System TX1

A typed expression language richer than EXL (literals, ADD/MUL,
grammar, value constraint) and simpler than full Zag.

- Int literals 0..9.
- ADD (Int,Int)->Int, MUL (Int,Int)->Int, SUB (Int,Int)->Int.
  SUB results may be negative; no value<64 rule is assumed.
- LT (Int,Int)->Bool. Bool is a distinct type; Bool values are not
  valid arithmetic operands.
- Pair encoding P(a,b) = a*16+b.

Relations (eval): 41 ADD, 42 MUL, 46 SUB, 47 LT.
Relations (decomp licensors): 43 DADD, 44 DMUL, 48 DSUB, 49 DLT.
Relation 45 BUILD (task relation, as in prior work).
Grammar node type 71.

## Induction (learner machinery, tx_patch.zag)

From taught examples only. No relation ids 41,42,43,44,46,47,48,49
appear in the patch outside comments.

1. Licensor set: scan BUILD facts (T,45,P); for each, find licensor
   facts (T,r,P) with r != 45; collect distinct r.
2. Decomp->eval map: for each BUILD example, scan all facts
   (P,e,T) over any relation e; require exactly one e per licensor.
3. Type partition: for each eval op e, scan all facts with relation
   e; e is Bool-producing iff every object is in {0,1}, else Int.
   Licensor type = its eval op's type.
4. Induction succeeds iff every BUILD example has a licensor,
   every licensor maps to exactly one eval op, and nlic == 4.

Grammar node (type 71) stores: nlic, packed licensor ids,
packed type mask, literal decode sanity only (no range induction;
eval knowledge verifies values).

## Teaching (driver, world side)

- Eval: all pairs (a,b) in 0..9: (P,41,a+b), (P,42,a*b),
  (P,46,a-b), (P,47,1 if a<b else 0). 400 facts.
- Goal decomp (int targets): (10,43,P(1,9)), (10,44,P(2,5)),
  (12,43,P(3,9)), (12,44,P(3,4)), (15,43,P(6,9)), (15,44,P(3,5)),
  (24,44,P(4,6)), (24,44,P(3,8)), (30,44,P(5,6)), (42,44,P(6,7)),
  (5,48,P(8,3)), (3,48,P(7,4)).
- BUILD-support decomp: (16,43,P(7,9)), (18,43,P(9,9)),
  (20,44,P(4,5)), (28,44,P(4,7)), (7,48,P(9,2)), (4,48,P(9,5)).
- Ambiguous int-decomp: (0,43,P(0,0)), (0,48,P(5,5)),
  (1,43,P(0,1)).
- DLT decomp: (0,49,P(3,3)), (0,49,P(5,2)), (0,49,P(7,3)),
  (1,49,P(0,1)), (1,49,P(3,7)).
- Order: eval, goal int-decomp, BUILD-support decomp,
  ambiguous int-decomp, DLT decomp, then BUILD examples.
- BUILD examples (8): (16,45,P(7,9)), (18,45,P(9,9)),
  (20,45,P(4,5)), (28,45,P(4,7)), (7,45,P(9,2)), (4,45,P(9,5)),
  (1,45,P(3,7)), (0,45,P(7,3)).
  Each example's pair has exactly one eval op yielding T
  (verified: 7+9=16 only ADD; 9+9=18 only ADD; 4*5=20 only MUL;
  4*7=28 only MUL; 9-2=7 only SUB; 9-5=4 only SUB;
  3<7=1 only LT; 7<3=0 only LT).

## Goal battery (12 goals, each a (target, reqtype) pair;
## reqtype 0=Int, 1=Bool; reqtype is the goal's type ascription)

(10,0) (12,0) (15,0) (24,0) (30,0) (42,0) (5,0) (3,0)
(0,0) (0,1) (1,0) (1,1)

The 4 ambiguous goals have both int-licensor and DLT facts.

## Arms (one workspace each, classify immediately per goal)

- W1 INDUCE: teach, induce, type-directed construction.
- W2 ABLATE: teach, induce, delete grammar node, base t2_trial.
- W3 TYPEBLIND: teach, induce, construction with licensor set
  and eval map but NO type filter (first verifying candidate).
- W4 FRESH: teach, no induction, base t2_trial.

Classifier: highest-id MAP (type-20, f8==t, f4==45); classes:
1 valid (single dep, dep rel in licensor set, induced type of dep
rel == reqtype, pair decodes, eval knowledge confirms);
2 multi-dep; 3 wrong-relation dep; 4 decode failure;
5 value mismatch; 6 TYPE MISMATCH (dep rel type != reqtype);
0 no MAP.

## Frozen kill bars

- K1: W1 valid == 12/12.
- K2: W2 valid == 0/12 (errors return after ablation).
- K3: W3 valid == 10/12 AND class-6 count >= 2.
  Rationale (order-independent): for the 4 ambiguous goals both
  fact kinds exist and the first gathered candidate verifies, so
  exactly the 2 goals whose reqtype mismatches the
  first-gathered kind fail with class 6, regardless of whether
  int-decomp or DLT facts were taught first.
- K4: W4 valid == 0/12.
- K5: 3 full runs byte-identical (sha256 recorded per run).
- K6: tx_patch.zag contains zero literals 41,42,43,44,46,47,48,49
  outside comments (grep verified; 45 permitted as BUILD task
  relation per prior-work precedent).
- K7: induced grammar reports nlic == 4 with type partition
  {DADD:Int, DMUL:Int, DSUB:Int, DLT:Bool} as sets (order free).

## Honest boundaries (not claimed)

- reqtype is given as the goal's type ascription, not induced.
- Single-link construction only; no nested expressions.
- Candidate order is gather order, not learned.
- Stepping stone toward Zag, not Zag mastery.
