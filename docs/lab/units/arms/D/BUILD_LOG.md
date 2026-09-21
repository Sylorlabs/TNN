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
