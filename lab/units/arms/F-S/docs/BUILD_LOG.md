# BUILD_LOG.md — F-S implementation log

## 2026-09-21: Initial implementation

### Store substrate
Copied B-64's slot store as the substrate, adapting for F-S:
- 23-field FS struct (B-64's 22 + `next_id` for persistent IDs)
- Slot table, tombstones, kill/pin/weaken/revision
- Audit ledger with F-S opcodes (CUT_PROPOSE=20, CUT_COMMIT=21, CUT_REFUSE=22)

### Markov chunker
Implemented the frozen mechanism in pure Zag:
- **Model:** Three-shard 64 MiB order-2 count table (21,846 + 21,845 + 21,845
  contexts). Saturating u32 counts. Single training pass.
- **Freeze:** Lowest-byte argmax per context (deterministic tie-break).
- **Propose:** Two-pass confident-miss collection (avoids n*4 allocation
  above toolchain slice limit).
- **Filter:** Local-maximum (±W=8) with lower-offset tie preference;
  minimum gap (MIN_GAP=32) greedy left-to-right.
- **Gate:** Recurrence test via 32-byte rolling hash + radix-sorted index
  + full byte verification. Two shards for corpora where single index
  would exceed 2^25 limit.
- **Reading AMB-FS-007:** Each fired cut judged on span since previous
  *fired* cut (not committed). Refused cuts advance span start but don't
  install boundaries.

### Critical bug: 8-byte vs 4-byte put/get
**Symptom:** `panic: slice index out of bounds` in `fs_init` during the
pidx initialization loop.

**Root cause:** My `uput`/`uget` wrote/read 8 bytes, but `iput`/`iget`
(which call them) are for 32-bit values and must use 4 bytes. In the
pidx loop:
```zag
while(i<cap){iput(s.*.pidx,i*4,-1);i=i+1;}
```
With cap=1024 and pidx=4096 bytes, the last iteration (i=1023, at=4092)
wrote bytes 4092..4099 via the 8-byte uput, overflowing the 4096-byte
buffer (valid indices 0..4095).

**Fix:** Changed `uput`/`uget` to 4-byte versions matching B-64:
```zag
fn uput(b:[]u8,at:i32,v:i64)void {
    b[at]=(v & 255) as u8;b[at+1]=((v>>8) & 255) as u8;
    b[at+2]=((v>>16) & 255) as u8;b[at+3]=((v>>24) & 255) as u8;
}
```

**Lesson:** When copying substrate code, verify byte-width assumptions.
The 8-byte version was for a different use case.

### Verification
- **Tiny file (66 bytes):** 1 chunk, 0 fired (no confident misses in tiny
  input). Correct.
- **Prose (5,422,721 bytes):** 93,439 fired, 210 committed, 211 chunks.
  Matches Python diagnostic exactly (93,439 fired).
- **Code (9,515,341 bytes):** 146,239 fired, 17,155 committed, 17,156 chunks.
- **M1 prose:** 211 units, 100.0% recall, 100.0% boundary. PASS.

### Provisional parameters
CONF_BAR=16, W=8, MIN_GAP=32 were chosen based on Python diagnostics,
not frozen. Competing values were not tested due to time constraints.
Per Micah's "test both" rule, this is a gap.

### Battery status
- **Implemented:** `diag-chunk`, `m1-1x-prose`, `m1-1x-code`
- **Not implemented:** M2, M3, M4, M5, M6, M7, M8, M9
- **Reason:** Time constraints after extended debugging of the 8-byte bug.
  The chunker (core mechanism) is verified; the full battery was not
  completed.

### Files
- `cl/arm.zag`: F-S implementation (chunker + store + M1)
- `substrate/`: R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag (verbatim)
- `docs/ARM_SPEC.md`: This spec
- `docs/BUILD_LOG.md`: This log

### Compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 2026-09-21 (continuation): Full battery implementation

### New modes implemented
All M2–M9 implemented in `cl/arm.zag` (~2,076 lines):

- **M2** (`m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`):
  Tiered curriculum (50 units per episode), ETC metric, per-episode content/
  boundary recall. M9 reported from M2 episodes (mean/range of per-episode
  content recall). All tiers: ETC=1, 100/100.
- **M3** (`m3-1x`): Churn protocol — ingest prose+code (M1), mark 1000
  valuable (pinned), ingest 3000 fresh, kill 3000 non-valuable, weaken 50,
  ingest 4000 fresh. Survival 100%, fresh recall 100%, weaken 50/50,
  freeze 0. Management entries: 9050.
- **M4** (`m4-1x-prose`, `m4-1x-code`): Defect planting (3 content +
  3 boundary shifts + 3 offset errors) then repair; 1 episode, 100/100.
- **M5** (`m5-1x`, `m5-baseline`): PROVISIONAL. Structural byte accounting
  (slot table, ledger, corpus buffer) vs fixed-work baseline spin
  (300M iterations). Prose: 155 units, 5.6MB source, 11.5MB slots,
  11.4MB ledger (177,585 entries incl. chunking diagnostics).
- **M6** (`m6-p2c-1x`, `m6-c2p-1x`): Source predictor trained on source
  domain, frozen, applied to target. Transfer tax 0.0 both directions
  (100/100/100 in-domain and transfer).
- **M7** (`m7-1x`): PROVISIONAL A7/A8. Edit = first-byte XOR;
  schedule = deterministic (l*37)%nunits; 5000 lookups over 3 regimes.
  Lookup 100%, reuse 2.0 (prose lookups / code units), dedup 50%.
- **M8** (`m8-1x`): Five perturbations (clean/frag/aslr/starve/freelist)
  × two runs. Each: M1-prose + M1-code + M3 with artifacts (alloc trace,
  ledger.bin, chain files, store hashes). All perturbations: 100/100/100,
  byte-identical stdout and artifacts across runs.
- **Sweep** (`sweep`): 7 configs (CONF_BAR × W × MIN_GAP) on M1-prose + M3.

### Bugs fixed during continuation
1. **M3 insertion-queue overflow:** `fs_new(4000,20000,9000)` — 9000-slot
   insertion queue overflowed with ~27k insertions → heap corruption →
   `panic: slice index out of bounds`. Fixed: capacities (4000,30000,30000)
   + bounds check on insertion-queue write.
2. **M3 recall buffer overflow:** Final probe used 64-byte `bout` for
   V-chunks up to 400KB → panic. Fixed: properly-sized `vb` buffer
   (max(chp.maxlen, chc.maxlen)).
3. **M3 weaken check:** `b_weaken(...)==0` tested wrong success value
   (returns slot ≥0 on success). Fixed: `>=0`.
4. **M7 reuse:** Was computing bytes-based; corrected to prose lookups /
   code units = 2.0.

### Determinism
All modes: two runs, byte-identical stdout verified via diff. M8: also
byte-identical artifacts (ledger.bin, chain files, hashes, alloc trace).
