# D-T Build Log

## 2026-09-21: Initial implementation and debugging

### Source
- `cl/arm.zag`: ~2,100 lines (grew to ~2,300 with fixes).
- Substrate: `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` (copied from B-64).

### Compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

### Key fixes
1. **Teaching repetition bug:** `s_cnt[best]` saved before `chunk_mint` (was -1).
2. **Merge threshold:** Changed `trep<2*jrep` to `jrep>2*trep` (was inverted).
3. **M1 remap probe counting:** Successful remap probes now increment `ok`
   (were not counted, causing 99.8% instead of 100%).
4. **Candidate counting:** Replaced sort-based with hash-table (1M slots,
   16-probe max) to avoid 2^25 slice limit and improve performance.
5. **Prefix/suffix omission:** Sub-token affix candidates removed for
   feasibility; documented in ARM_SPEC.md.
6. **Empty t.c:** Removed accidental empty file.

### Performance issues
- `observe_pass` originally used a hash table with 64-probe and eviction:
  too slow (44s for 542KB).
- Tried sort-based (radix sort): 16-bit variant pathologically slow;
  8-bit worked but hit 2^25 limit on 5.4MB.
- Final: fixed 1M-slot hash table, 16-probe max, no eviction. ~50s for
  542KB M2 (3 episodes).
- `revision_pass` is O(seeds × chunks) and becomes a bottleneck on large
  corpora (4.3MB t2-prose, 15MB M3). This limits battery throughput.

### Binary
`~/workspace/dt_bin` (rebuilt multiple times; final 2026-09-21 06:53).

## 2026-09-21: Battery execution (in progress)

- M1 prose: PASS (100.0%/100.0%, 359/500 revised)
- M1 code: PASS (100.0%/100.0%, 413/500 revised)
- M2 t1-prose: PASS (3 ep, 100%/100%, 488/500 revised)
- M2 t1-code: PASS (3 ep, 100%/100%, 445/500 revised)
- M2 t2-code: PASS (3 ep, 100%/100%, 419/500 revised)
- M2 t3: PASS (3 ep, 100%/100%, 28 rev + 263 killed = 58.2%)
- M2 t2-prose: SLOW (revision bottleneck; incomplete)
- M3: RUNNING
- M4 prose: RUNNING
- M4 code, M5, M6, M7, M8: PENDING
