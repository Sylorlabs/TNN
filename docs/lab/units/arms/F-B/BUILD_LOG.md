# F-B Build Log — 2026-09-21

## Mechanism
Branching-continuation cuts. For each position, longest span L in 2..64 with
rep >= 2 (REP_BAR=2, provisional). Cut before i if contdiv >= 3 (BR_BAR=3, frozen).
Polynomial rolling hash P=91138233. 4-way set-associative candidate table
(1024 sets x 4 ways = 4096 slots). Per-set min-(rep,seq) eviction.
Chunk justification code 5.

## Validation
Python reference (ref_4way.py) and Zag implementation match exactly on 2KB:
- chunks=311
- checksum=3976909433127229168

Variants tested:
- 1-way direct-mapped: 63 chunks (thrashing, too few).
- 2-way: 296 chunks.
- 4-way: 311 chunks (selected).
- D-style clear-on-full: 20 chunks (too destructive).

## Performance blocker
4-way LRU suffers 46x slowdown when table fills:
- 4KB empty table: 2.5s.
- 4KB full table: 115s (positions 4096-8192 of 8KB input).
- Root cause: random access to 208KB table thrashes cache under VM
  memory pressure (191MB free, high steal).
- Full corpus (15MB = 945M observations) infeasible.
- Even t1 corpora (563KB) time out.

Optimizations attempted:
- Split keys/values for 1-cache-line lookup.
- Moved popcnt out of L loop (was 256 iterations per hit).
- All validated but insufficient.

## Spec compliance notes
- Uses polynomial hash (P=91138233), not FNV. D's implementation also uses
  polynomial (not FNV), despite spec saying "rolling FNV". Documented as
  prereg/catalog mismatch (see D's BUILD_LOG).
- 4-way set-associative is a form of open-addressed table. Spec says "linear
  probing"; 4-way was chosen for O(1) eviction. Per-set (not global) min
  eviction is a deviation from "global min-(rep,seq)".
- Content verification (memcmp) not implemented; hash-only matching.
  Spec requires FNV+memcmp. Documented as gap.

## Files
- cl/arm.zag: complete implementation (M1 modes for prose/code/t1).
- Validation: ~/workspace/scratch/fb/ref_4way.py, seg_4way2.zag.

## Outcome
Mechanism validated on small inputs. Full battery BLOCKED by performance.
See VERDICT.md.
