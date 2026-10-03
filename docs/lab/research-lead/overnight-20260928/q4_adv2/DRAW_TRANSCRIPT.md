# F-RECFOLD Draw Transcript (Sealed)

## Status

SEALED. Draw performed by independent adversary after prereg P (efbc9ad9e).
Contents hidden from learner until after scoring completes.
SHA256 of sealed parameters published below; contents revealed post-scoring.

Prereg: efbc9ad9e
Design: 808ed196d
Seed: 770404483
Seed SHA256: 5426835ee69f290cb98f12cbc94e7a03fe6de2ada5de91745259ad4ee20fda02 (verified)

## LCG Log

s_{n+1} = (1664525 * s_n + 1013904223) mod 2^32, s_0 = 770404483

### Instance 1 (easy, R1)
- motif draw: s=1560468486, v=0 -> AND (accepted)
- top draw: s=2513732525, v=2 -> XOR3
- pairing draw: s=1620414760, idx=10 -> (1,5)(2,4)(3,6)
- decoy draw: s=3905241703 -> Xd=X2
- Xj draw: s=586636442 -> Xj=X3

### Instance 2 (medium, R2)
- motif draw: s=2632844081, v=2 -> reject, retry
- motif draw: s=1502847708, v=0 -> AND (accepted)
- permutation draw: s=2202919051, idx=571 -> (5,4,6,1,3,2)
- decoy draw: s=3698179182 -> Xd=X1
- Xj draw: s=2379438325 -> Xj=X2

### Instance 3 (hard, R1)
- motif=XOR (fixed), top=XOR3 (fixed)
- pairing draw: s=1435047376, idx=1 -> (1,2)(3,5)(4,6)
- decoy draw: s=1415966447 -> Xd=X6
- Xj draw: s=2015776642 -> Xj=X5

## Drawn Parameters (Sealed)

### Instance 1
- Subfamily: R1 (REPEAT, flat k-fold)
- Motif: AND
- Top: XOR3
- Pairing: (1,5)(2,4)(3,6)
- Canonical form: D = XOR3( AND(X1,X5), AND(X2,X4), AND(X3,X6) )
- Operators: 3 AND + 2 XOR = 5 ops
- Decoy Xd: X2
- Phase-2 Xj: X3

### Instance 2
- Subfamily: R2 (RECURSE, nested fold)
- Motif: AND
- Permutation: (5,4,6,1,3,2)
- Canonical form: D = AND(AND(AND(AND(AND(X5,X4),X6),X1),X3),X2)
- Operators: 5 AND = 5 ops
- Decoy Xd: X1
- Phase-2 Xj: X2

### Instance 3
- Subfamily: R1 (REPEAT, flat k-fold)
- Motif: XOR (fixed)
- Top: XOR3 (fixed)
- Pairing: (1,2)(3,5)(4,6)
- Canonical form: D = XOR3( XOR(X1,X2), XOR(X3,X5), XOR(X4,X6) )
- Operators: 3 XOR + 2 XOR = 5 ops
- Decoy Xd: X6
- Phase-2 Xj: X5

## Fairness Gate (Section 7.4)

Per instance, mechanically verify canonical compact form uses at most 7
operators from {AND, OR, NOT, XOR}.

- Instance 1: 5 ops (3 AND, 2 XOR) <= 7. PASS.
- Instance 2: 5 ops (5 AND) <= 7. PASS.
- Instance 3: 5 ops (5 XOR) <= 7. PASS.

All operators in {AND, OR, NOT, XOR}. Gate passes. No halt, no redraw.

## Truth Tables (Sealed)

64-row truth tables generated and stored:
- /tmp/truth_i1.txt (28 rows with D=1)
- /tmp/truth_i2.txt (1 row with D=1)
- /tmp/truth_i3.txt (32 rows with D=1)

Contents sealed until after scoring.

## Sealed Parameter Hashes

SHA256 of concatenated sealed parameters per instance:
(to be computed after implementation)

## Governance

- Draw performed by independent agent (did not build Q4 learner).
- All tooling shell only. Zero Python.
- Zero em dash bytes.
- Prereg efbc9ad9e strictly precedes this transcript.
