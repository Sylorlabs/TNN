# Fresh disjoint adversary byte set (frozen wave-20261001-0221pdt)

Purpose: bank the next allowed adversary byte set for the H-PI-REV2
pipeline (steps 6 onward: alternative-explanation attack, OOD, and any
future F-run needing a fresh disjoint byte). This document declares the
set only; it does not select a byte for a specific run and does not
freeze any new experiment. A future prereg executes the selection rule
below.

## Derivation (zero discretion)

1. Alphabet: lowercase a-z.
2. Exclude every lowercase byte occurring in any frozen fixture input:
   T ("abc","xy","defg"), F1 ("xab"), F1-reuse ("xqw"),
   R ("zag","12","q","hello","ptc","s","eghjjupazbnf","q"),
   V1 (PI-1a/PI-1b inputs), and the frozen adversary instances
   "iab" (F2), "wab" (F3a), "vab" (F3a2/F3a3).
   Mechanical union (audited 2026-10-01 from the fixture strings):
   abcdefghijlnopqstuvwxyz.
3. Exclude previously used adversary bytes not already covered: none
   (i, w, v are all in the union above).
4. Exclude 'z' (designated for the F3b non-first-letter world
   ("abz"->"zzz") in the F3a3 prereg; reserved, not available).

Result: **{k, m, r}** (sorted byte order: k=107, m=109, r=114).

Each of k, m, r occurs in no frozen fixture input and was never an
adversary byte; the class is disjoint from all frozen evidence by
construction.

## Selection rule (standing convention)

When the next adversary prereg needs a byte, it executes the rule
declared in F3a2 and re-used in F3a3: the last letter of this set in
sorted byte order, i.e. **'r'** (114). No re-selection and no human
choice intervene; the prereg cites this document.

Note: this continues the correction history. The F2 set
{i,j,k,l,m,n,o,r,t,u,v,w} contained fixture bytes (j, l, n, o, t, u
all occur in R inputs); F3a2 corrected it to {k,m,r,v}; 'v' was then
consumed by F3a2/F3a3, leaving this set.

Frozen by wave-20261001-0221pdt coordinator, 2026-10-01.
