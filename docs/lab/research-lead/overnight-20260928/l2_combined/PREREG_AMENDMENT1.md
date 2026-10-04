# PREREG_AMENDMENT1.md: node-id derivation correction (pre-verdict)

Date: 2026-10-02. Status: pre-implementation-verdict, pre-any-PASS/FAIL
claim. This amendment corrects an arithmetic error in PREREG.md
sections 4 and 6; no kill bar is weakened, no threshold moved, no
claim changed.

## The error

PREREG.md hand-derived substitute/extension MAP ids as m2=55,
ext1=77, ext2=103, final=133. That derivation forgot that the killed
fact node 3 (ns(W,3,36,0) sets its live flag to 0) becomes available
to alloc_node, which scans for the lowest free slot. The first
allocation after the kill therefore reuses node 3, shifting every
later id down by one.

## Corrected derivation

After setup + kill, node 3 is free. Substitute t2_asm_chain (16
cells) allocates 3,38..52; the t2_exec frame takes 53;
adapt_promote takes 54. So m2=54.

- ext1: 20 cells 55..74, frame 75, id=76.
- ext2: 24 cells 77..100, frame 101, id=102.
- ext3 (final): 28 cells 103..130, frame 131, id=132.

The behavior is deterministic: in every arm the first post-kill
allocation is the substitute's (FULL, REUSE q1, SUBONLY) or the
trial's (EXTONLY, EXACT, FRESH), and only the adaptation arms assert
on MAP ids.

## Corrected frozen values

- Section 4 trace: SUB-PROMOTE m2=54;
  EXTN-STEP n=1 parent=54 id=76 plen=5 lic=104,1,105 term=105;
  EXTN-STEP n=2 parent=76 id=102 plen=6 lic=105,1,106 term=106;
  EXTN-STEP n=3 parent=102 id=132 plen=7 lic=106,1,107 term=107;
  EXTN-STOP reason=0 ext=3 ans=107 final=132;
  L2C-ANS via=132 val=107.
- K1: final=133 -> 132; relseq(132); hops(132)=4; ult_native(132)=23.
- K2: t16 pairs {(54,23),(54,37),(76,54),(102,76),(132,102)};
  t14 from 132 to {23,37,54};
  t15 pairs {(23,37),(37,54),(54,76),(76,102),(102,132)}.
- K5: m2=55 -> 54; t16 pairs {(54,23),(54,37)}; ng(54,28)=104.
- K8: q2 final=133 -> 132.
- REUSE q2 trace: L2C-SEL m=132 plen=7 term=107; L2C-ANS via=132.

All other bars, the world spec, the pipeline, the falsifiers, and
the 0-new-machinery audit are unchanged. The amendment was written
before any verdict was computed; the implementation now matches the
corrected derivation.
