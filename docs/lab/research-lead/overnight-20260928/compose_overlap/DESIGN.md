# DESIGN: Overlapping Primed Sets

## Background

C362 (multipoison) proved poison tax is additive for DISJOINT primed sets:
two bits (m0,out,1) and (m1,out,1) justify 6 disjoint pairs, TRIES=7,
poison=6=3+3. The open question: what if two bits justify the SAME pair?

## Mechanics (from frozen multipoison PREREG)

A carried out-bit (m,out,k) justifies exactly the pairs (m,y), y != m,
whenever bit k intersects y's effective inmask.

In multipoison: every MAP has inmask {1}. Bit (m0,out,1) justifies
(0,1),(0,2),(0,3) because bit 1 (binary 01) intersects inmask {1}
(binary 01). Bit (m1,out,1) justifies (1,0),(1,2),(1,3). Disjoint
because the first element differs (0 vs 1).

## Overlapping construction

Two out-bits on the SAME map with different kind values, where the
target inmask intersects BOTH kinds.

Example:
- MAP m0 has outmask {4} (a kind never legally emitted).
- Q1a: m0 emits NODE (kind 1). U2 records (m0,out,1).
- Q1b: m0 emits NUM (kind 2). U2 records (m0,out,2).
- Both bits are in the ledger.
- Target MAPs m1,m2,m3 have inmask {1,2,3} (binary 0111).
- Bit (m0,out,1): bit 1 (001) intersects {1,2,3} (0111). Justifies
  (0,1),(0,2),(0,3).
- Bit (m0,out,2): bit 2 (010) intersects {1,2,3} (0111). Justifies
  (0,1),(0,2),(0,3).
- The two primed sets are IDENTICAL: {(0,1),(0,2),(0,3)}.
- Complete overlap.

## Key questions

1. Does wadmit_set deduplicate? If (0,1) is justified by both bits,
   does WADD log it once or twice?
2. What is TRIES? If deduplicated: 3 primed + 1 single = 4.
   If not: 6 primed + 1 single = 7.
3. Does each bit get struck independently? When (0,1) is tried,
   does it disconfirm BOTH (m0,out,1) and (m0,out,2), or just one?
4. Does U6 retire each bit independently? If both are struck by the
   same trials, do they retire at the same time or independently?

## Frozen predictions (for implementation worker to verify)

- WADD logs each pair ONCE (set semantics).
- TRIES = 4 (3 primed + 1 answering single).
- Each primed trial strikes BOTH bits (they're both (m0,out,*)).
- Both bits retire after 2 strikes each (may be simultaneous).
- Poison = 3 (not 6), because the sets overlap completely.

## Implementation notes

- Copy the multipoison lane structure.
- Modify the world: m0 outmask {4}, targets inmask {1,2,3}.
- Q1 must seed BOTH bits. This may require two seed queries or a
  world where m0 emits different kinds on different attempts.
- The implementation worker should read the frozen u4_priming code
  to confirm the set semantics before running.
