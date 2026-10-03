# PREREG_AMEND1: correction to Section 5.1 admitted-sequence count

Date: 2026-10-03. Worker: gen-cycles.
Status: committed BEFORE the formal build.sh battery runs (only an
exploratory smoke compile/run has occurred; no kill-bar verdicts taken).

## What was wrong

PREREG Section 5.1 predicted "16 admitted sequences (m1 in {0,1,2,3},
m2 in {0,2}, m3 in {0,2})" at k=3 and TRIES=31. The hand-derivation
erred: it applied only the first-position check (in{m1} compatible with
kin) to m1 and forgot that the chain rule ALSO constrains m1 as the left
element of the first adjacent pair (out{m1} INTERSECTS in{m2}).

## Corrected derivation (from the frozen Section 2 chain rule)

k=3, kin=1, kout=1. All in-masks are {1}; out-masks: MAP0 {1}, MAP1 {2},
MAP2 {1}, MAP3 {2}.
- m1: in{m1}∋1 (all four) AND out{m1}∩in{m2}≠∅ with in{m2}={1}
  => out{m1} must meet {1} => m1 in {0,2}.
- m2: out{m2}∩in{m3}≠∅ with in{m3}={1} => m2 in {0,2}.
- m3: out{m3}∋1 => m3 in {0,2}.
Admitted k=3 sequences: 2x2x2 = 8:
[0,0,0],[0,0,2],[0,2,0],[0,2,2],[2,0,0],[2,0,2],[2,2,0],[2,2,2].
All fail (none reaches 1005): [0,0,0]->1004; [0,0,2]->1003 via the
output==input halt at step 3; [0,2,0],[0,2,2]->1002 via the halt at
step 2; [2,*,*]->1001 via the halt at step 1. 8 tries, 14 INTER= lines
(3+3+2+2+1+1+1+1).

k=4: [0,0,0,0] (lexicographically first) admitted; stepwise
1001->1002->1003->1004->1005; end-of-pass halt; 1005==exp: SUCCESS.
1 try, 4 INTER= lines.

## Corrected predictions (Section 5.1 replaced)

- Report: `ARM=GC PROB=QC ANS=1005 TRIES=23`
  (TRIES = 14 (U prefix) + 8 (k=3) + 1 ([0,0,0,0])).
- Census unchanged from PREREG: MAP 0 n=9, inmask=1 outmask=1; others
  (m1: 1/2 n=5; m2: 1/1 n=1; m3: 1/2 n=1).
- WIDEN=2 never fires.

## What does NOT change

- The Section 2 mechanism spec (chain rule, halting, enumeration,
  recording) is untouched; the implementation already follows it.
- Kill bars C1-C3, C5-C8 are untouched. C4's TRIES clause updates
  31 -> 23 to reflect the corrected derivation; its substance
  (ANS=1005, found=1, no WIDEN=2) is unchanged.
- Sections 5.2-5.4, 6-9 are untouched.

## Why amend rather than fail C4

The implementation executes the frozen Section 2 rule exactly; the
defect was arithmetic in the prediction, not in the mechanism or the
bar's intent. Per standing governance, amend transparently and
re-freeze rather than pretend the execution was valid.
