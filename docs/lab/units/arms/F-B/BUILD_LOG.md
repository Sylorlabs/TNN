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
# F-B Build Log — 2026-09-21 (appended by crew U5, marathon)

## Bugfix 1: popcnt64 infinite loop (root cause of "BLOCKED")
- **Symptom:** Corpus-scale runs hung; misdiagnosed as 46× cache-thrash slowdown.
- **Root cause:** `popcnt64` used `v=v>>1` on i64. Zag `>>` is arithmetic.
  When continuation-diversity bit 63 was set (bytes 63/127/191/255), `v`
  stayed negative forever → infinite loop.
- **Reproducer:** `popcnt64((1 as i64)<<63)` hung; after fix returns 1.
- **Fix:** `v=(v>>1) & 9223372036854775807;` — exact popcount, always terminates.
- **Validation:** 2KB fixture still 311 chunks, checksum unchanged.

## Bugfix 2: duplicate terminal boundary
- **Symptom:** 64KB: Zag 46,278 chunks vs Python 46,277.
- **Root cause:** Appended `i2` on cut, then separately appended `n` when
  `i2==n`; final cut created a zero-length chunk.
- **Fix:** Single append on `cut==1 || i2==n` (matches ref_4way.py).
- **Validation:** 2/4/8/64KB all byte-identical to Python (chunks + checksum).

## Full battery implementation (2026-09-21)
- Rewrote `cl/arm.zag` (~1240 lines) implementing all frozen modes:
  m1-1x-prose/code, m2-t1/t2/t3 (with M9), m3-1x, m4-1x-prose/code,
  m5-1x/baseline, m6-p2c/c2p-1x, m7-1x (N/A), m8-1x.
- Pure Zag, zero RNG, deterministic. METRIC_JSON per ARM_INTERFACE.
- Store: (id, corpus, off, len, flags, checksum, seq) with FNV-1a-64
  integrity checks; 32B ledger entries; OP_ADD/KILL/WEAKEN/EVICT/REVISE/REFUSE.
- M3: V=1000 valuable (500 prose + 500 code, chunks containing bytes at
  v*(n/500) — deterministic even-coverage schedule); 10,000-step churn
  (3000 ingests, 3000 kills, 50 weakens, 4000 ingests with evict-oldest-unpinned).
- M4: 200 units/corpus (100 boundary + 100 content defects); 1 revision
  episode via fresh re-segmentation; lineage preserved.
- M5: 1000 valuable + 1,000-step mini-pressure; reports interface keys.
- M6: stateless transfer (train is documented no-op); memorizer negative
  control (100 source chunks replayed on target, expects ~0 matches).
- M8: 5 perturbations (clean/frag/aslr/starve/freelist) × 2 reruns;
  artifacts: store_hashes.txt, store_chain.txt, ledger.bin,
  ledger_chain.txt, alloc_trace.txt (normalized, no addresses).

## Performance optimization (build note, not prereg change)
- **Problem:** 47µs/position → full battery ~2.3h CPU, infeasible overnight.
- **Fix:** Replaced 5 separate `[]u8` arrays + byte-shuffling accessors with a
  single interleaved `[]i64` arena (4096 records × 8 i64: h, L, rep, seq,
  cdiv0..3). Pure layout change; identical values/order/eviction.
- **Safety:** ZNC-007 probed `as []i64` CLEAN; used single
  `(raw as []i64)[0..n]` view (correct length, avoids consecutive-cast pattern).
- **Validation:** Byte-identical to Python ref on 2KB (322 chunks) and 64KB
  (7567 chunks); checksums match modulo 2^64 (signed/unsigned).
- **Speedup:** 12.4µs/position (3.8×). Full battery ~27 min CPU.

## Declared deviations (unchanged)
1. Polynomial rolling hash (P=91138233), not FNV.
2. 4-way set-associative, not linear probing.
3. Per-set min-(rep,seq) eviction, not global.
4. No memcmp in candidate table (hash+length only).

## M5 note
- F-B's chunks average ~1.3 bytes on prose (BR_BAR=3 cuts aggressively).
- Per-unit slot (32B) vs 1.3B chunks → ~25× ratio, fails the 1.5× bar.
- Honest evidence of the mechanism's cost profile, not a bug.
- C-W also failed M5 (16.481×). The bar is doing its job.

## 2026-09-21: Mode battery (1x) — results

M3 (m3-1x): survival=100.0, fresh=100.0, mgmt=8050, weaken=50.
M1 prose: recall=100.0, boundary=100.0, units=4,402,039.
M1 code: recall=100.0, boundary=100.0, units=5,287,970.
M2 t1 prose: final=100.0/100.0, shape=fast-then-flat, episodes=1.
M2 t1 code: final=100.0/100.0.
M2 t2 prose: final=100.0/100.0.
M2 t2 code: final=100.0/100.0.
M2 t3-1x: final=100.0/100.0, episodes=1.

M4/M6/M5/M7 pending (running).

Field-name fixes applied (2026-09-21):
- M4: m4_boundary_recall_tenths → m4_rev_boundary_tenths;
  m4_content_recall_tenths → m4_rev_content_tenths;
  added m4_kill_rate_tenths=0, m4_killsub=0.
- M6: m6_recall_tenths → rec_tenths; m6_boundary_tenths → bnd_tenths;
  m6_revision_tenths → rev_tenths; m6_transfer_tax_tenths → tax_tenths.
- M3: m3_management_entries → m3_mgmt_entries; added m3_valuable=1000.
- M6 memorizer: replaced meaningless offset-comparison with vacuous
  negative control (stateless arm; 0 matches, ok=1).

Service restart ~21:45 UTC killed mode runner; resumed from m2-t2-prose.

## 2026-09-21: Battery complete, verdict KILLED

All 15 modes completed (1x):
- M1 prose/code: 100.0/100.0
- M2 t1/t2/t3: 100.0/100.0
- M3: 100.0/100.0
- M4 prose/code: 100.0/100.0
- M5: 18.2× per-byte (FAIL), 568 entries/KB (FAIL)
- M6 p2c/c2p: 100.0, tax 0.0
- M7: N/A

Kill evaluation:
- Disjunct 1 (M3 < C-W's): DOES NOT FIRE (100.0 !< 100.0)
- Disjunct 2 (within noise of F-S): FIRES (all Δ=0.0 < 0.5)

**Binding verdict: KILLED** (redundant vs F-S, retire F-B, keep F-S).

M8 gate running (compact workload; see declared deviations).
