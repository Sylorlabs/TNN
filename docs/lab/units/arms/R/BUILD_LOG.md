# BUILD_LOG.md — Arm R (Compression cuts, MDL/DP)

## Authority
- Arm: **R — Compression cuts (MDL/DP)**, family CUT
- Brief: `units/arms/briefs/R.json`
- Mechanism: "Chunks are compression units: cut where description length is minimized (suffix-array/LCP + DP over cost)."
- Binding kill: boundary F1 against whitespace/punctuation joints and arm O's taught spans, separately, must beat fixed-64B by ≥10 points on both corpora; **or** held-out M1 recall with R-cuts must beat the 64B baseline.
- C9: compression is dominant; R is the anti-R31 control, not R31's continuation.

### Coordinator corrections acknowledged
1. The original dispatched "Deliberate boundary revision" definition was wrong and is **VOID**.
2. An earlier coordinator paraphrase of frozen §3 was superseded.
- Authority order: (1) `units/arms/briefs/R.json`, (2) verbatim frozen §3 row, (3) nothing else.
- On 2026-09-21, the brief's `mechanism` and `kill` strings were programmatically compared with the corrected row and matched exactly.

## Build
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Source: `units/arms/R/cl/arm.zag`
- Command:
  ```bash
  znc cl/arm.zag --no-zagd --no-analyze --no-foreground-cache -o work/r_bin
  ```
- Result: **SUCCESS** — binary `work/r_bin` (261,727 bytes) written 2026-09-21.
- One binary, mode dispatch via `argv[1]`:
  - `m1-prose`, `m1-code`, `m2-prose`, `m2-code`, `m2-m9`, `m3`, `m4`, `m5`,
    `m6-prose`, `m6-code`, `m7`, `m8` (with `[perturbation]`), `x-segcheck`,
    `x-segcal`, `x-bound`

## Implementation
- Pure Zag, deterministic, zero RNG.
- Suffix array: deterministic prefix-doubling with counting sort (O(n log n)).
- LCP: folded Kasai, repeat lengths capped at L.
- DP: backward description-length minimization; repeated-substring cost = `ref_cost` (2), literal cost = chunk length; tie-break by longer chunk, then earlier cut.
- Parameters: `R_L=64`, `R_REF=2` (provisional, not frozen — per §3, L=64 and ref_cost=2 were examples).
- Memory: ID-to-slot map, batched SCAN_COMMIT, traced allocation with alloc/free balance audit.
- Policy audit: corpus SHA-256, L, ref_cost, tiebreak rule, chunk count, spot-check hashes printed per run.

## Compiler issues resolved
1. Arity errors and undefined `mark_valuable` — fixed.
2. `Cuts` struct caused native-codegen failures — removed entirely; boundaries passed as explicit `(b0,b1,bse,n)` slices.
3. Local struct field access: Zag native codegen rejects `s.field` and `s.*.field` on local struct values. Workaround: `let ps:*R=&s;` then `ps.*.field` (verified with minimal reproducers).
4. Slice-base indexing: `ps.*.led[0..N]` rejected; bind to local `let led:[]u8=ps.*.led;` first.
5. **Runtime panic "slice index out of bounds"**: counting-sort scratch arrays `cn0/cn1` in `seg_build_sa` were allocated as `se*4` where `se=(n+2)/2`, but the first prefix-doubling iteration uses `maxr=255` requiring 257 slots. For n < 510, this overflowed. Fixed by allocating `cn0/cn1` with `se_c=max(se,129)` (129 gives 258 slots via cget/cset), covering both the initial maxr=255 and later maxr<=n-1 cases.

## Smoke tests (2026-09-21)
- `x-segcheck` on 240-byte tiny corpus: `X-SEGCHECK,4,1` — 4 chunks, byte-identical rerun confirmed.
- `m1-prose` on tiny corpus: `M1,prose.bin,100.0,100.0,4` — 100% recall, 100% boundary.

## Battery status
- 1x battery on full corpora (r1: prose 5.4MB, code 9.5MB) — **BLOCKED ON PERFORMANCE**.
- `m1-prose` on 5.4MB prose timed out after 15 minutes during suffix-array construction.
- The prefix-doubling SA implementation (O(n log n) with ~946M cget/cset operations for n=5.4M) has too high constant factors in Zag for the full corpora.
- Correctness VERIFIED on tiny corpora (240B): segmentation, DP, ingest, recall all work.
- Full battery cannot complete in available time without SA optimization.

## Performance analysis
- SA construction dominates runtime.
- For n=5.4M: 22 prefix-doubling iterations × 2 counting sorts × ~21.6M ops = ~946M cget/cset calls.
- Each cget/cset is a Zag function call with bounds checking.
- Estimated time: >15 min for 5.4MB prose, >30 min for 9.5MB code.
- Full 1x battery (20+ runs) would require 10+ hours; 10x would require 100+ hours.
- Optimization needed: inline array accesses, or use SA-IS linear-time algorithm.

## Provisional / non-frozen items
- `L=64`, `ref_cost=2` are provisional examples, not frozen constants.
- Boundary-F1 formula, tolerance, endpoint handling: proposed, not frozen.
- Arm O taught-span artifact absent — taught-span kill leg BLOCKED.
- Held-out M1 recall protocol underdetermined; strict "beat" problematic if both reach 100%.
- A15 swap schedule: PROVISIONAL-PENDING-FREEZE.
- M7 reuse formula, C′ edit, M6 frozen-dictionary interpretation, A17 M8 interpretation: provisional.

## 2026-09-21: Optimization port to production (cl/arm.zag)

### Head-to-head results (mid-size 1 MiB fixture)
- Candidate C (truncated prefix doubling + inlined access): 55.1s wall, 4.2s CPU.
- Candidate D (end-aware 64-pass LSD radix): 161.0s wall, 10.3s CPU.
- Candidate F (self-repeat suffix automaton): >245s (killed), not competitive.
- Winner: Candidate C.

### Ported to cl/arm.zag (exact, proven by x-segcheck on all fixtures)
1. `seg_build_sa`: truncated prefix doubling (stops at L=64), inlined little-endian paired-array access.
2. `seg_maxlen`: capped from-scratch adjacent LCP fold (replaces Kasai).
3. `seg_dp`: windowed DP (128-entry ring) with split literal/repeat loops.
4. `seg_frozen_maxlen`: suffix-automaton over reversed train (replaces SA narrowing; corrects >=2 to >=1 occurrence).

### Fixture verification (port_test_bin x-segcheck)
- tiny (240B): 4 chunks, MATCH.
- fx-rand (64KB): 1610 chunks, MATCH.
- fx-repeat (64KB): 1024 chunks, MATCH.
- fx-nul (32KB): 513 chunks, MATCH.
- fx-edge (16B): 6 chunks, MATCH.

### Full prose timing (5.6MB)
- Before split-loop DP: 17m08s wall, 74.0s CPU.
- After: 14m18s wall, 68.1s CPU (same 547,545 chunks).

### Interface fixes
- main() rewritten: official mode names (m1-1x-prose, m2-t1-prose, ..., m8-1x).
- t_m3: official M3 fields (survival, fresh_recall, mgmt_entries, weaken_handled, freeze, valuable).
- t_m4: official M4 fields (units, attempts, repairs, recall_post_repair, salvage, unrepaired_ids).
- t_m5: official M5 (learned units, ledger.bin to CWD).
- t_m5_baseline: same-sized empty store + ledger.
- t_m6: official M6 (rec/bnd/rev/tax tenths).
- t_m8: official M8 (5 artifacts, 5 perturbations).
- j_begin now takes scale param.

## 2026-09-21: 2^25 slice limit bug fix (code corpus)

**Bug:** m1-1x-code (9.5MB) panicked with "slice index out of bounds". Root cause:
cut-boundary arrays (b0/b1) were allocated as `(n+1)*4` bytes. For n=9,515,341,
this is 38MB > 33,554,432 (2^25), the znc maximum indexable slice size.

**Fix:** Changed all cut-array allocations from `bse=n+1` to `bse=(n+2)/2`
(split point), with b0/b1 each `bse*4` bytes. The existing `cget`/`cset`
already handle split arrays. For n=9.5M: bse=4,757,671, each half 19MB < 33.5MB.

**Verification:**
- x-segcheck on 9.5MB code: `X-SEGCHECK,545132,1` (exact match)
- m1-1x-code: 545,132 chunks, 100% recall, 64/64 tamper caught
- All 18 cut-array allocation sites updated in cl/arm.zag
