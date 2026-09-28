# F-B Arm Specification

## Identity
- **ID**: F-B
- **Name**: Branching-continuation cuts
- **Family**: CUT
- **Track**: A

## Frozen parameters
- BR_BAR = 3 (cut threshold: contdiv >= 3)
- Justification code = 5
- LMAX = 64
- Candidate slots = 4096
- W = 256 (window, not enforced in this implementation)

## Arm-choice parameters (provisional)
- REP_BAR = 2 ("repeated" = seen >= 2)

## Mechanism
For each position i in the corpus:
1. For L = 2..64 (or up to i), compute polynomial rolling hash of buf[i-L..i-1].
2. Look up (h, L) in 4-way set-associative candidate table.
   - Set = (h ^ (L * K2)) & 1023.
   - On hit: rep++, update contdiv bitset with buf[i] (if i < n).
   - On miss: insert into empty way, or evict per-set min-(rep,seq).
3. Track longest L with rep >= 2.
4. After L loop: if maxL > 0 and contdiv(maxE) >= 3, cut before i.
5. Always cut at n (end of corpus).

## Data structures
- kh: 4096 x 8B (hash)
- kl: 4096 x 4B (length)
- kr: 4096 x 4B (rep count, 0 = empty)
- vs: 4096 x 4B (insertion sequence)
- vc: 4096 x 32B (continuation bitset, 256 bits)

## Battery modes
- m1-prose: segment prose.bin, store, recall, verify.
- m1-code: segment code.bin, store, recall, verify.
- m1-t1p: segment t1_prose.bin (10% held-out).
- m1-t1c: segment t1_code.bin (10% held-out).

## Kill criterion
M3 < C-W's on both corpora; OR within noise of F-S on all metrics both corpora.

## Known gaps
1. Performance: 46x slowdown on full table; full-corpus infeasible.
2. No content verification (hash-only).
3. Per-set (not global) eviction.
4. Polynomial hash (not FNV).
5. M2-M9 not implemented (M1 only).
