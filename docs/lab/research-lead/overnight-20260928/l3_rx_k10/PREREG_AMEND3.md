# L3-RX-K10 PREREG AMENDMENT A3 (pre-verdict)

Date: 2026-10-03. Amends PREREG.md (b0b94bfc4) + A1 + A2. Run 2 (under A2)
showed W3 still scoring 6/6 (rk HOLD): white-box analysis of the
committed perm revealed the tie-break only arbitrates among out-degree
ties, and my A2 design left z's od=0 tied solely with the true-last item
while every heldout pair (z,x) had od[x] >= 1, so the tournament placed
z correctly from genuine evidence. The A2 withhold did not isolate the
tie-break. This amendment redesigns W3 to isolate it properly. Kill bar,
kill condition, and predicted outcome (COMMIT, 0/6) are unchanged.

## Root cause of A2's failure

In A2's W3, c1 withheld only z's pairs. Then od[z]=0, and the only
out-degree tie was z vs the true-last item; all heldout pairs (z,x) had
od[x] >= 1, so z sorted after x by evidence, matching the truth. The
tie-break never decided a heldout pair. Lesson: sparsity alone does not
make the induction fabricate; the fabrication happens exactly on
out-degree ties, so the attack must manufacture ties on the heldout
pairs themselves.

## New W3 design (replaces A2's)

Roles (item indices; ids from the frozen items table):
- z1=2 (id 7), z2=0 (id 23), z3=1 (id 41) — the three smallest ids
- x1=5 (id 55), x2=6 (id 90), x3=4 (id 112)
- r1=3 (id 198), r2=7 (id 164)
- S = {0,1,2,4,5,6} (all except r1,r2)

Orders: O1C = [5,6,4,3,7,2,0,1] (x's, then r's, then z's last);
O2C = [1,0,2,7,3,4,6,5] (exact reverse). |D| = 28.

Withhold: in c1, ALL pairs involving any S item (27 pairs x 2 = 54
triples). c1 training = 2 triples (the {r1,r2} pair, both orientations).
train = 58. c2 training = full 56.

Mechanism (frozen prediction): the {r1,r2} conflict fires inadequacy
(Dslots={0}); expansion lifts slot 0. In the c1 partition the only
known pair is {r1,r2}; od[r1]=1, all others od=0. The 7-way od=0 tie is
broken purely by id ascending, placing z1,z2,z3 before x1,x2,x3. The
committed c1 perm is [198,7,23,41,55,90,112,164]. Heldout (frozen):
(c1,z1,x1),(c1,x1,z1),(c1,z2,x2),(c1,x2,z2),(c1,z3,x3),(c1,x3,z3) —
predictions 1,0,1,0,1,0; truth (z's last in O1C) 0,1,0,1,0,1.
Predicted: COMMIT guarded, heldout 0/6, deterministic.

W6 (p6 recode of W3) inherits the structure; the amended p6 (A1) keeps
index 2 at the smallest id, preserving the tie-break direction.

## Why this is fair

The heldout pairs are evidentially undetermined in c1 (no known edge,
no 2-step path: every path needs an S-edge and none is known). The
builder's prereg (160f138cc 5.1(b)) specifies the tie-break
("ties -> lowest id") as the documented determiner, and the trace
shows COMMIT with "mismatch 0" — identical confidence to the
evidence-determined case. The attack discriminates fabrication from
evidential support, which is RK-B's frozen thesis. The builder's own
F1 worlds never tested the expansion path on evidentially
undetermined pairs (their heldout pairs always appeared in training).

## Unchanged

Kill bars, thresholds, verdict rule, determinism protocol, all other
worlds. W3 train size is now 58 (was 98 under A2).
