# Arm D — Build Log

## Session: 2026-09-21

### Implementation Status
- **File**: `~/workspace/tnn-lab/units/arms/D/cl/arm.zag` (75KB, ~2,100 lines)
- **Status**: Compiles successfully. All 17 modes implemented.
- **Binary**: `/tmp/d_smoke` (250KB native)

### Modes Implemented
m1-1x-prose, m1-1x-code, m2-t1-prose, m2-t1-code, m2-t2-prose, m2-t2-code,
m2-t3-1x, m3-1x, m4-1x-prose, m4-1x-code, m5-baseline, m5-1x, m6-p2c-1x,
m6-c2p-1x, m7-1x, m8-1x

### Mechanism
- Self-cut byte spans with stable monotonic IDs (257+ for learned, 1..256 literals)
- Candidate table: 4,096 slots, 56B records, polynomial rolling hash (NOT FNV-1a — see issue)
- Proposal: rep>=4 (PROVISIONAL), len>=3, contdiv>=2
- Greedy longest-match segmentation with literal fallback
- ID-list unit encoding, persistent ID→slot mapping
- Streamed ledger, corpus reader
- Reasoning-control: inspect/propose/commit/refuse/rollback
- Native split/merge/rollback, tombstoned IDs never reused

### Bugs Fixed During Build
1. **cand_evict_half infinite loop**: Only evicted state=1, but state=2 (committed)
   slots kept cand_used high. Fixed to evict both states.
2. **cidx_insert infinite loop**: Unbounded `while(1==1)` probe. If table full,
   looped forever. Fixed with probe counter bound (drops insert if full).
3. **cand_observe infinite loop**: Table-full check was inside `if(st==0)` branch.
   If table full with no empty slots, probe looped forever. Fixed to clear
   table BEFORE probing, with bounded probe count.

### Remaining Issues (BLOCKING official battery)
1. **Performance hang on repetitive data**: 1200-byte repetitive input
   ('hello world '*100) hangs >30s in Phase A candidate scanning. Root cause
   not isolated. Possibly hash collision pathology or excessive candidate
   tracking.
2. **Panic on larger random data**: 1200-byte random input panics with
   "slice index out of bounds" after ~1.8s. 64-byte random works. Bug not
   isolated. Likely in ingest_unit list allocation or recall decoding.
3. **Identity hash mismatch**: Implementation uses polynomial rolling hash.
   Prereg/catalog requires FNV-1a + byte-loop collision verification.
   Must be replaced before official evidence.
4. **REP_BAR provisional**: `D_REP_BAR_PROVISIONAL=4` is fenced for compilation
   only. NOT authorized for official runs. Awaiting coordinator/freeze value.
5. **M9 late gain**: Contains placeholder `late = er-er`. Must implement
   actual late-gain (recall@ETC - recall@takeoff).
6. **Candidate record layout**: 56-byte record with continuation words at
   offset 60+ (requires 68B). Layout inconsistency not resolved.
7. **Open-address deletion**: Eviction clears slots but probe chains may break.
   Not audited.

### Test Results
- 64-byte single unit (repetitive): PASS (4s, 100% recall)
- 64-byte random: PASS (3.5s, 100% recall)
- 128-byte repetitive: PASS (0.25s)
- 1200-byte repetitive: HANG (>30s, no output)
- 1200-byte random: PANIC (slice index out of bounds)

### Corpus Verification
- `~/workspace/tnn-lab/units/arms/harness/corpora/r1/prose.bin`: SHA256 matches MANIFEST
- `~/workspace/tnn-lab/units/arms/harness/corpora/r1/code.bin`: SHA256 matches MANIFEST

### Recommendation
**DO NOT RUN official battery.** Implementation is structurally complete but has
blocking performance and correctness bugs. Requires further debugging:
- Isolate Phase A hang (add progress counters, profile hash distribution)
- Fix slice OOB panic (likely list allocation bounds)
- Replace polynomial hash with FNV-1a + byte verification
- Resolve REP_BAR authorization
- Fix M9 late gain computation

### Files
- Implementation: `~/workspace/tnn-lab/units/arms/D/cl/arm.zag`
- This log: `~/workspace/tnn-lab/units/arms/D/BUILD_LOG.md`

## 2026-09-21 — Performance Optimizations (D-DBG)

### Problem
M1 1x prose (5.4MB) projected at 2.4 hours real time (12.2s user per 100KB).
Full M1-M9 battery infeasible.

### Root Causes
1. **Candidate table wholesale clear**: Cleared 4096 slots (O(cap)) on every
   table-full event, and wiped all rep counts (breaking "candidates accumulate
   rep" — REP_BAR could never fire under churn).
2. **Tombstone eviction livelock**: Attempted half-eviction with tombstones
   caused full-table probes (no state-0 terminators) and risked livelock.
3. **iget64/iput64 function call overhead**: Rolling hash update did 512
   function calls per byte (6.4M calls per 100KB).

### Fixes
1. **Generation-counter clear (O(1))**: Added 4-byte generation to 68B record
   (now 72B). Clear = bump generation counter; stale generations read as empty.
   No O(cap) loop.
2. **Clear at 50% load**: Table capacity 4096→16384, clear when used>=8192.
   Keeps probe lengths short (~1.3 steps avg).
3. **[]i64 direct indexing**: Changed hh1/hh2/pow1/pow2 from []u8 with
   iget64/iput64 to []i64 with direct indexing. Verified ZNC-007: `as []i64`
   is CLEAN (no aliasing). M1 output byte-identical.

### Results
- 100KB prose: 12.2s → 2.95s user (4.1x speedup).
- M1 1x prose (5.4MB): ~11 min → ~2.7 min user (projected).
- All smoke tests pass with identical M1 output.

### 10x Modes Added
- m1-10x-prose, m1-10x-code dispatch (r10 corpora).
- r10 = r1 repeated 10x (verified via tile_sha256).
- Capacities scaled 10x; idlist kept at 32MB (under 2^25 ceiling).

### Critical Fix: Candidate Table Probe Termination (2026-09-21)
**Symptom**: 100KB M1 = 3s, 200KB M1 >160s (50x slowdown for 2x data).
**Root cause**: The generation-bump "O(1) clear" left stale entries physically
in the table. Probes had to walk through stale entries to find current-gen
slots. After many clears, the table filled with stale entries and probes
traversed O(cap) per observation → O(n^2) total.
**Fix**: Physical clear of the 4-byte generation fields (64KB memset) on each
clear. All slots read as empty (gen=0 != cur_gen); probes terminate immediately.
**Result**: 200KB M1 = 6.1s (linear scaling restored). 100KB unchanged at 3s.

### Critical Fix 2: CIDX Unbounded Probes (2026-09-21)
**Symptom**: 400KB M1 >146s (vs 11s expected); 1MB M1 >265s.
**Root cause**: Two issues:
1. `cidx_insert` and `cidx_lookup` used unbounded `while(n<cap)` probes.
   When the table filled during large ingests, inserts/lookups became O(cap).
2. `d_index_ensure` sized the table for `chunk_next=257` (empty at ingest
   start) → 1024-slot table. During 400KB ingest, thousands of chunks filled
   it. With the 32-probe bound (fix 1), inserts dropped, lookups missed, and
   segmentation did 62 lengths × 32 probes = 1984 steps per byte position.
**Fix**: 
- Bound both probes to 32 slots (dropped inserts acceptable; misses fall back
  to literal).
- Size cidx for `chunk_cap` (32768) not current count → 65536-slot table,
  stays sparse.
**Result**: 400KB M1 = 11.4s (was >146s); 1MB M1 = 136s (was >265s). Linear
scaling restored through 400KB.
**Binary**: `/home/hatch/workspace/d_test5` (includes both fixes + M1 10x).
